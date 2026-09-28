#!/usr/bin/env python3
"""Audit shipped narrative catalog content and release-scale RPG quotas.

This intentionally counts only player-facing strings in Resources/Content JSON.
IDs, code, numeric values, design documents and repeated literal strings are
excluded from the authored-word total.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "Assets" / "Resources" / "Content"
APK_CANDIDATES = (
    ROOT / "Build" / "AshenOath-Offline-Preview.apk",
    ROOT / "Build" / "AshenOath-Development.apk",
)

# Deliberately allowlist fields: technical identifiers and configuration values
# should never inflate the prose count.
TEXT_FIELDS: dict[str, tuple[str, ...]] = {
    "dialogue_catalog.json": ("speakerName", "lines"),
    "item_catalog.json": ("name", "description"),
    "prologue_quests.json": (
        "title", "objective", "choiceSpeaker", "choicePrompt",
        "choices.label", "objectives.description",
    ),
    "monster_catalog.json": ("displayName",),
    "recipe_catalog.json": ("displayName",),
    "farm_catalog.json": ("cropDisplayName",),
    "fishing_catalog.json": ("displayName",),
    "codex_catalog.json": ("title", "category", "writtenBy", "body"),
}
ID_CATALOGS = (
    "dialogue_catalog.json", "item_catalog.json", "prologue_quests.json",
    "monster_catalog.json", "encounter_catalog.json", "recipe_catalog.json",
    "farm_catalog.json", "fishing_catalog.json", "codex_catalog.json", "quest_landmarks.json",
)
CANONICAL_ARCS = {
    "ashes_of_ashfall", "the_order_of_the_dawn", "crown_of_empty_fields",
    "the_salt_road", "the_choir_beneath_the_lake", "the_hundredth_champion",
    "archive_beyond_veil", "two_last_oaths",
}
OBJECTIVE_KINDS = {
    "talk", "defeat", "interact", "choice", "collect", "craft",
    "fish", "grow", "inspect", "escort",
}
LANDMARK_OBJECTIVE_KINDS = {"inspect", "interact", "grow", "talk", "choice"}
LANDMARK_VISUAL_IDS = set("""
    chalk_tally witness door_brace document noticeboard sealed_case herb_ledger
    remedy_shelf waymarker root_graft seed_cradle cycle_tablet stone_rill choir_diver
    wind_keeper signal_frame signal_vane signal_mark signal_well signal_ridge
    signal_bell_test signal_flag_test sluice_wheel pressure_gauge filter_housing
    clinic_house field_satchel cart_wheel cart_rut cart_spokes cart_test cart_bay
    cart_kit tomas_reed rootwall_joint pella_quinn kitchen_hearth kitchen_millstone
    broth_sample common_table glassplum_tree
""".split())

WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def field_values(value: Any, path: str) -> list[str]:
    """Resolve a dotted allowlisted path across nested entry dictionaries."""
    parts = path.split(".")
    if not parts:
        return []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(field_values(item, path))
        return result
    if not isinstance(value, dict) or parts[0] not in value:
        return []
    child = value[parts[0]]
    if len(parts) > 1:
        return field_values(child, ".".join(parts[1:]))
    if isinstance(child, str):
        return [child]
    if isinstance(child, list):
        return [item for item in child if isinstance(item, str)]
    return []


def read_catalogs() -> dict[str, dict[str, Any]]:
    catalogs: dict[str, dict[str, Any]] = {}
    for name in TEXT_FIELDS:
        path = CONTENT / name
        if not path.is_file():
            raise FileNotFoundError(f"Required catalog is missing: {path}")
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
            raise ValueError(f"Expected an entries array in {path}")
        catalogs[name] = data
    return catalogs


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split()).casefold()


def collect_unique_text(catalogs: dict[str, dict[str, Any]]) -> tuple[list[str], Counter[str]]:
    unique: dict[str, str] = {}
    field_counts: Counter[str] = Counter()
    for catalog_name, fields in TEXT_FIELDS.items():
        for entry in catalogs[catalog_name]["entries"]:
            for field in fields:
                for text in field_values(entry, field):
                    clean = " ".join(text.split())
                    if not clean:
                        continue
                    field_counts[field] += 1
                    unique.setdefault(normalized(clean), clean)
    return list(unique.values()), field_counts


def catalog_entries(name: str) -> list[dict[str, Any]]:
    path = CONTENT / name
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data["entries"]


def get_apk_size() -> tuple[Path | None, int]:
    for path in APK_CANDIDATES:
        if path.is_file():
            return path, path.stat().st_size
    return None, 0


def invalid_objective_kinds(quests: list[dict[str, Any]]) -> list[str]:
    """Catch catalog verbs that gameplay services never emit."""
    problems: list[str] = []
    for quest in quests:
        for objective in quest.get("objectives", []) or []:
            kind = objective.get("kind", "")
            if kind not in OBJECTIVE_KINDS:
                problems.append(f"{quest.get('id', '<unknown>')}: {kind or '<missing>'}")
    return problems


def invalid_quest_references(quests: list[dict[str, Any]]) -> list[str]:
    """Catch missing, duplicated, or self-referencing prerequisite IDs."""
    quest_ids = {quest.get("id") for quest in quests}
    problems: list[str] = []
    for quest in quests:
        quest_id = quest.get("id", "<unknown>")
        prerequisites = quest.get("prerequisiteIds", []) or []
        if len(prerequisites) != len(set(prerequisites)):
            problems.append(f"{quest_id}: duplicate prerequisite ID")
        for prerequisite_id in prerequisites:
            if prerequisite_id not in quest_ids or prerequisite_id == quest_id:
                problems.append(f"{quest_id}: invalid prerequisite {prerequisite_id}")
        for group_index, group in enumerate(quest.get("prerequisiteGroups", []) or []):
            alternatives = (group or {}).get("anyOfQuestIds", []) or []
            if not alternatives:
                problems.append(f"{quest_id}: empty prerequisite group {group_index}")
            if len(alternatives) != len(set(alternatives)):
                problems.append(f"{quest_id}: duplicate alternative prerequisite {group_index}")
            for prerequisite_id in alternatives:
                if prerequisite_id not in quest_ids or prerequisite_id == quest_id:
                    problems.append(f"{quest_id}: invalid alternative prerequisite {prerequisite_id}")
    return problems


def is_stable_id(value: Any) -> bool:
    return (isinstance(value, str) and 0 < len(value) <= 64 and
            "a" <= value[0] <= "z" and
            all("a" <= char <= "z" or "0" <= char <= "9" or char == "_" for char in value))


def invalid_landmarks(landmarks: list[dict[str, Any]], quests: list[dict[str, Any]],
                      dialogues: list[dict[str, Any]]) -> list[str]:
    """Mirror QuestLandmarkCatalogService.Validate for authored world markers."""
    problems: list[str] = []
    dialogue_ids = {entry.get("id") for entry in dialogues if isinstance(entry, dict)}
    objectives_by_target: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for quest in quests:
        for objective in quest.get("objectives", []) or []:
            if isinstance(objective, dict):
                objectives_by_target.setdefault(objective.get("targetId", ""), []).append((quest, objective))

    ids: set[str] = set()
    targets: set[str] = set()
    for entry in landmarks:
        label = entry.get("id", "<unknown>") if isinstance(entry, dict) else "<null>"
        if not isinstance(entry, dict):
            problems.append(f"{label}: landmark definition is not an object")
            continue
        landmark_id = entry.get("id")
        target_id = entry.get("targetId")
        location_id = entry.get("locationId")
        if not is_stable_id(landmark_id) or landmark_id in ids:
            problems.append(f"{label}: invalid or duplicate landmark ID")
        ids.add(landmark_id)
        if not is_stable_id(location_id):
            problems.append(f"{label}: invalid location ID")
        if not is_stable_id(target_id) or target_id in targets:
            problems.append(f"{label}: invalid or duplicate target ID")
        targets.add(target_id)
        name = entry.get("displayName")
        if not isinstance(name, str) or not name.strip() or len(name) > 60:
            problems.append(f"{label}: invalid display name")
        if entry.get("visualId") not in LANDMARK_VISUAL_IDS:
            problems.append(f"{label}: unsupported visual ID {entry.get('visualId')!r}")
        for field, minimum, maximum, fallback in (
            ("positionX", -11.3, 11.3, None), ("positionY", -5.2, 5.0, None),
            ("scale", 0.04, 0.2, 0.085),
        ):
            value = entry.get(field, fallback)
            if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                    not math.isfinite(value) or value < minimum or value > maximum):
                problems.append(f"{label}: invalid {field} {value!r}")

        matches = objectives_by_target.get(target_id, [])
        if not matches:
            problems.append(f"{label}: no quest objective for target {target_id!r}")
            continue
        matched = False
        for quest, objective in matches:
            kind = objective.get("kind")
            quest_id = quest.get("id", "<unknown>")
            if kind not in LANDMARK_OBJECTIVE_KINDS:
                problems.append(f"{label}: unsupported objective kind {kind!r} on {quest_id}")
                continue
            if quest.get("type") == "side" and quest.get("locationId") != location_id:
                problems.append(f"{label}: target is outside side quest region on {quest_id}")
            if kind == "choice":
                choices = quest.get("choices") or []
                if len(choices) < 2:
                    problems.append(f"{label}: choice objective has fewer than two choices on {quest_id}")
                for choice in choices:
                    if not isinstance(choice, dict) or choice.get("dialogueId") not in dialogue_ids:
                        problems.append(f"{label}: choice result dialogue is missing on {quest_id}")
            elif kind != "grow" and objective.get("dialogueId") not in dialogue_ids:
                problems.append(f"{label}: objective dialogue is missing on {quest_id}")
            matched = True
        if not matched:
            problems.append(f"{label}: no supported quest objective for target {target_id!r}")
    return problems


def invalid_encounters(encounters: list[dict[str, Any]], quests: list[dict[str, Any]],
                       monsters: list[dict[str, Any]], items: list[dict[str, Any]],
                       dialogues: list[dict[str, Any]]) -> list[str]:
    """Check persistent fight links that the Unity content validator requires."""
    problems: list[str] = []
    quest_ids = {entry.get("id") for entry in quests if isinstance(entry, dict)}
    monster_ids = {entry.get("id") for entry in monsters if isinstance(entry, dict)}
    item_ids = {entry.get("id") for entry in items if isinstance(entry, dict)}
    dialogue_ids = {entry.get("id") for entry in dialogues if isinstance(entry, dict)}
    defeat_targets = {
        objective.get("targetId")
        for quest in quests for objective in (quest.get("objectives", []) or [])
        if isinstance(objective, dict) and objective.get("kind") == "defeat"
    }
    encounter_ids: set[str] = set()
    for encounter in encounters:
        if not isinstance(encounter, dict):
            problems.append("<null>: encounter definition is not an object")
            continue
        encounter_id = encounter.get("id", "<unknown>")
        if not is_stable_id(encounter.get("id")) or encounter.get("id") in encounter_ids:
            problems.append(f"{encounter_id}: invalid or duplicate encounter ID")
        encounter_ids.add(encounter.get("id"))
        if encounter.get("monsterId") not in monster_ids:
            problems.append(f"{encounter_id}: monster is missing")
        if encounter.get("requiredQuestId") not in quest_ids:
            problems.append(f"{encounter_id}: required quest is missing")
        blocked_quest = encounter.get("blockedQuestId", "")
        blocked_dialogue = encounter.get("blockedDialogueId", "")
        if bool(blocked_quest) != bool(blocked_dialogue):
            problems.append(f"{encounter_id}: blocked quest and dialogue must be paired")
        if blocked_quest and blocked_quest not in quest_ids:
            problems.append(f"{encounter_id}: blocked quest is missing")
        for field in ("defeatDialogueId", "downDialogueId"):
            if encounter.get(field) not in dialogue_ids:
                problems.append(f"{encounter_id}: {field} does not resolve")
        if blocked_dialogue and blocked_dialogue not in dialogue_ids:
            problems.append(f"{encounter_id}: blocked dialogue does not resolve")
        if encounter.get("contributesToQuest", True):
            if encounter.get("defeatObjectiveTargetId") not in defeat_targets:
                problems.append(f"{encounter_id}: defeat objective target does not resolve")
        elif encounter.get("defeatObjectiveTargetId"):
            problems.append(f"{encounter_id}: non-contributing encounter has a defeat target")
        reward = encounter.get("reward") or {}
        if reward.get("gold", 0) < 0:
            problems.append(f"{encounter_id}: negative gold reward")
        for reward_item in reward.get("items", []) or []:
            if not isinstance(reward_item, dict) or reward_item.get("itemId") not in item_ids:
                problems.append(f"{encounter_id}: reward item does not resolve")
            elif reward_item.get("quantity", 1) < 1:
                problems.append(f"{encounter_id}: reward item quantity is below one")
    return problems


def audit() -> dict[str, Any]:
    catalogs = read_catalogs()
    unique_strings, field_counts = collect_unique_text(catalogs)
    word_count = sum(len(WORD_RE.findall(text)) for text in unique_strings)

    quests = catalog_entries("prologue_quests.json")
    dialogues = catalog_entries("dialogue_catalog.json")
    encounters = catalog_entries("encounter_catalog.json")
    monsters = catalog_entries("monster_catalog.json")
    items = catalog_entries("item_catalog.json")
    bad_objective_kinds = invalid_objective_kinds(quests)
    bad_quest_references = invalid_quest_references(quests)
    landmarks = catalog_entries("quest_landmarks.json")
    bad_landmarks = invalid_landmarks(landmarks, quests, dialogues)
    bad_encounters = invalid_encounters(encounters, quests, monsters, items, dialogues)
    quest_types = Counter(entry.get("type", "unknown") for entry in quests)
    quests_by_arc = Counter(entry.get("arcId", "unassigned") for entry in quests)
    equipment = sum(entry.get("category") == "equipment" for entry in items)
    species_by_rank = Counter(entry.get("rank", "unknown") for entry in monsters)
    apk_path, apk_bytes = get_apk_size()

    duplicate_ids: dict[str, int] = {}
    for name in ID_CATALOGS:
        ids = [entry.get("id") for entry in catalog_entries(name)]
        duplicate_ids[name] = len(ids) - len(set(ids))
    landmark_targets = [entry.get("targetId") for entry in landmarks]
    duplicate_landmark_targets = len(landmark_targets) - len(set(landmark_targets))

    return {
        "word_count": word_count,
        "unique_strings": len(unique_strings),
        "dialogue_entries": len(dialogues),
        "codex_entries": len(catalog_entries("codex_catalog.json")),
        "quest_count": len(quests),
        "invalid_objective_kinds": bad_objective_kinds,
        "invalid_quest_references": bad_quest_references,
        "invalid_landmarks": bad_landmarks,
        "invalid_encounters": bad_encounters,
        "quest_types": quest_types,
        "quests_by_arc": quests_by_arc,
        "unknown_arc_ids": sorted(set(quests_by_arc) - CANONICAL_ARCS),
        "item_count": len(items),
        "equipment_count": equipment,
        "species_count": len(monsters),
        "species_by_rank": species_by_rank,
        "encounter_count": len(encounters),
        "recipe_count": len(catalog_entries("recipe_catalog.json")),
        "farm_plot_count": len(catalog_entries("farm_catalog.json")),
        "fishing_spot_count": len(catalog_entries("fishing_catalog.json")),
        "duplicate_ids": duplicate_ids,
        "duplicate_landmark_targets": duplicate_landmark_targets,
        "apk_path": apk_path,
        "apk_bytes": apk_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a nonzero exit code until every release content quota is met",
    )
    args = parser.parse_args()
    result = audit()
    word_target = 1_000_001  # release brief requires more than one million words
    goals = [
        ("Edited, deduplicated player-facing words", result["word_count"], word_target),
        ("Quest definitions", result["quest_count"], 1_000),
        ("Monster types", result["species_count"], 200),
        ("Elite species", result["species_by_rank"].get("elite", 0), 50),
        ("Boss species", result["species_by_rank"].get("boss", 0), 16),
        ("Equipment", result["equipment_count"], 200),
        ("Android APK bytes", result["apk_bytes"], 400_000_001),
    ]

    print("Ashen Oath content audit")
    print(f"Project: {ROOT}")
    print(f"Unique player-facing strings: {result['unique_strings']:,}")
    print(f"Dialogue entries: {result['dialogue_entries']:,}")
    print(f"Content counts: {result['quest_count']:,} quests ({dict(result['quest_types'])}), "
          f"{result['item_count']:,} items, {result['species_count']:,} species, "
          f"{result['encounter_count']:,} placements, {result['recipe_count']:,} recipes, "
          f"{result['codex_entries']:,} field records")
    print(f"Invalid objective event kinds: {len(result['invalid_objective_kinds'])}")
    for problem in result["invalid_objective_kinds"]:
        print(f"  {problem}")
    print(f"Invalid quest prerequisite references: {len(result['invalid_quest_references'])}")
    for problem in result["invalid_quest_references"]:
        print(f"  {problem}")
    print(f"Invalid quest landmarks: {len(result['invalid_landmarks'])}")
    for problem in result["invalid_landmarks"]:
        print(f"  {problem}")
    print(f"Invalid encounter links: {len(result['invalid_encounters'])}")
    for problem in result["invalid_encounters"]:
        print(f"  {problem}")
    print("Quest definitions by arc:")
    for arc, count in sorted(result["quests_by_arc"].items()):
        print(f"  {arc}: {count}")
    if result["unknown_arc_ids"]:
        print(f"Unknown/noncanonical arc IDs: {', '.join(result['unknown_arc_ids'])}")
    print("Species by rank:")
    for rank, count in sorted(result["species_by_rank"].items()):
        print(f"  {rank}: {count}")
    apk_label = f"{result['apk_path'].relative_to(ROOT)} ({result['apk_bytes']:,} bytes)" if result["apk_path"] else "not found"
    print(f"Measured APK: {apk_label}")
    print("Release quota status:")
    all_met = True
    for label, actual, target in goals:
        met = actual >= target
        all_met &= met
        mark = "PASS" if met else "OPEN"
        print(f"  {mark:4} {label}: {actual:,} / {target:,}")
    duplicates = sum(result["duplicate_ids"].values())
    print(f"Duplicate catalog IDs: {duplicates}")
    print(f"Duplicate landmark targets: {result['duplicate_landmark_targets']}")
    if duplicates:
        for name, count in result["duplicate_ids"].items():
            if count:
                print(f"  {name}: {count}")
    if args.strict and (not all_met or duplicates or result["unknown_arc_ids"] or
                        result["invalid_objective_kinds"] or result["invalid_quest_references"] or
                        result["invalid_landmarks"] or result["invalid_encounters"] or
                        result["duplicate_landmark_targets"]):
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(f"Audit failed: {error}", file=sys.stderr)
        raise SystemExit(2)
