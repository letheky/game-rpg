#!/usr/bin/env python3
"""Import the reviewed CC0 Crawl sprite set as eleven regional field chains."""

import hashlib
import json
import struct
import zipfile
from pathlib import Path

from crawl_creature_data import CASES, CODEX, CREATURES, SOURCE_COMMIT, SOURCE_RELEASE
from import_tiny_creatures_fieldbook import ART, CONTENT, REGIONS, ROOT, read_catalog

ARCHIVE = ROOT / "Docs/AssetArchives/crawl-cc0-creatures.zip"
LICENSE_DOC = "license/TILES_UNDER_UNKNOWN_LICENSE.md"
CATALOGS = (
    "monster_catalog.json", "encounter_catalog.json", "prologue_quests.json",
    "item_catalog.json", "dialogue_catalog.json", "codex_catalog.json",
)
REGION_LABELS = {
    "af": "Ashfall", "do": "Dawnkeep", "db": "Barracks Annex",
    "cw": "Cinderwell", "cc": "Lower Cistern", "sr": "Salt Road",
    "sl": "Lockhouse", "ch": "Choir", "gw": "Greenwake",
    "ow": "Outer-Wake", "lo": "Crownfall",
}
FIELD_AREAS = {
    "af": "the well lane", "do": "the drill yard", "db": "the barracks gallery",
    "cw": "the seed-store path", "cc": "the lower cistern", "sr": "the ridge road",
    "sl": "the lockhouse aisle", "ch": "the sounding posts", "gw": "the orchard",
    "ow": "the archive floor", "lo": "the oath chamber",
}
SLOTS = ("weapon", "armor", "charm")
SLOT_LABELS = {"weapon": "Field Edge", "armor": "Field Mantle", "charm": "Field Token"}
MOVE_BY_SPECIES = {
    "anubis_guard": "marked_strike", "cyclops": "shockwave", "ettin": "shockwave",
    "death_knight": "line_charge", "iron_golem": "shockwave", "juggernaut": "line_charge",
    "glowing_shapeshifter": "marked_strike", "caustic_shrike": "ranged_bolt",
    "elephant_slug": "siphon", "death_yak": "line_charge", "catoblepas": "marked_strike",
    "electric_eel": "ranged_bolt", "shark": "line_charge", "death_ooze": "siphon",
    "apocalypse_crab": "hook", "electric_golem": "shockwave", "basilisk": "ranged_bolt",
    "polar_bear": "line_charge", "shock_serpent": "ranged_bolt", "hell_beast": "shockwave",
    "rust_devil": "hook", "macabre_mass": "siphon", "unseen_horror": "marked_strike",
    "wretched_star": "ranged_bolt", "eye_of_devastation": "ranged_bolt",
    "ancient_zyme": "siphon", "tentacled_starspawn": "hook", "starcursed_mass": "siphon",
    "worldbinder": "ranged_bolt", "lurking_horror": "marked_strike",
    "eye_of_draining": "siphon", "deathcap": "siphon", "plant_demonic": "ranged_bolt",
    "thorn_hunter": "hook", "vine_stalker": "hook", "entropy_weaver": "hook",
    "crystal_guardian": "shockwave", "iron_elemental": "line_charge",
    "mutant_beast": "line_charge", "fire_giant": "shockwave", "frost_giant": "shockwave",
    "balrug": "ranged_bolt", "blizzard_demon": "ranged_bolt", "brimstone_fiend": "shockwave",
}


def slug(source_path: str) -> str:
    return Path(source_path).stem


def atomic_write(path: Path, data: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    if len(CREATURES) != 55 or len({row[1] for row in CREATURES}) != 55:
        raise SystemExit("The curated list must contain 55 distinct sprite files.")
    if set(CASES) != set(REGIONS) or set(CODEX) != set(REGIONS):
        raise SystemExit("Every existing campaign region needs two cases and one field record.")
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing reviewed source bundle: {ARCHIVE}. Run Tools/prepare_crawl_cc0_bundle.py first.")

    paths, catalogs = {}, {}
    for file_name in CATALOGS:
        paths[file_name], catalogs[file_name] = read_catalog(file_name)

    planned_ids = []
    for region_code, source_path, *_ in CREATURES:
        creature_slug = slug(source_path)
        planned_ids.extend((
            f"crawl_{creature_slug}", f"crawl_{creature_slug}_site",
            f"rowan_crawl_{creature_slug}_record", f"fieldgear_crawl_{creature_slug}",
        ))
    planned_ids.extend(f"side_crawl_{code}_{number}" for code in REGIONS for number in (1, 2))
    planned_ids.extend(f"crawl_codex_{code}" for code in REGIONS)
    if len(planned_ids) != len(set(planned_ids)):
        raise SystemExit("The curated IDs are not unique.")
    existing_ids = {entry.get("id", "") for data in catalogs.values() for entry in data["entries"]}
    present = [entry_id for entry_id in planned_ids if entry_id in existing_ids]
    sprite_paths = [ART / f"crawl_{slug(row[1])}.png" for row in CREATURES]
    if present:
        if len(present) == len(planned_ids) and all(path.is_file() for path in sprite_paths):
            print("Crawl field species are already imported; no changes made.")
            return
        raise SystemExit("Partial Crawl import detected; inspect catalogs and sprites before retrying.")

    additions = {name: [] for name in CATALOGS}
    art_payloads: list[tuple[Path, bytes]] = []
    mapping_rows = []
    region_indexes = {code: 0 for code in REGIONS}
    region_members: dict[str, list[tuple[str, str, str]]] = {code: [] for code in REGIONS}
    quest_objectives: dict[str, list[list[dict]]] = {code: [[], []] for code in REGIONS}
    quest_rewards: dict[str, list[list[dict]]] = {code: [[], []] for code in REGIONS}

    with zipfile.ZipFile(ARCHIVE) as bundle:
        names = set(bundle.namelist())
        if LICENSE_DOC not in names:
            raise SystemExit("The archived upstream unclear-license exclusion list is missing.")
        unknown_text = bundle.read(LICENSE_DOC).decode("utf-8")
        unknown_files = {line[2:].strip().casefold() for line in unknown_text.splitlines()
                         if line.startswith("- ")}

        for region_code, source_path, display_name, observation, follow_up in CREATURES:
            creature_slug = slug(source_path)
            source_entry = f"{SOURCE_RELEASE}/{source_path}"
            if Path(source_path).name.casefold() in unknown_files:
                raise SystemExit(f"Excluded by upstream license list: {source_path}")
            if source_entry not in names:
                raise SystemExit(f"Source sprite is missing from the reviewed bundle: {source_entry}")
            pixels = bundle.read(source_entry)
            if not pixels.startswith(b"\x89PNG\r\n\x1a\n") or len(pixels) < 24:
                raise SystemExit(f"Invalid PNG data: {source_entry}")
            width, height = struct.unpack(">II", pixels[16:24])
            if (width, height) != (32, 32):
                raise SystemExit(f"Expected a 32x32 sprite, got {width}x{height}: {source_entry}")
            region = REGIONS[region_code]
            level = region["level"]
            local_index = region_indexes[region_code]
            region_indexes[region_code] += 1
            quest_number = 1 if local_index < 3 else 2
            quest_id = f"side_crawl_{region_code}_{quest_number}"
            monster_id = f"crawl_{creature_slug}"
            encounter_id = f"crawl_{creature_slug}_site"
            dialogue_id = f"rowan_crawl_{creature_slug}_record"
            item_id = f"fieldgear_crawl_{creature_slug}"
            slot = SLOTS[(sum(region_indexes.values()) - 1) % len(SLOTS)]
            attack_bonus = level + 1 if slot == "weapon" else max(1, level // 2) if slot == "charm" else 0
            guard_bonus = max(1, (level * 3 + 2) // 4) if slot == "armor" else max(1, level // 3) if slot == "charm" else 0
            region_label = REGION_LABELS[region_code]
            equipment_name = f"{region_label} {display_name} {SLOT_LABELS[slot]}"
            if slot == "weapon":
                equipment_description = (
                    f"A compact field weapon assembled in {region_label} after Rowan cleared the route. "
                    f"{observation} The close grip keeps its weight steady in a narrow passage. "
                )
            elif slot == "armor":
                equipment_description = (
                    f"A light field layer fitted in {region_label} for work near the {display_name.lower()}. "
                    f"{observation} Its lining can be shaken clean before another patrol. "
                )
            else:
                equipment_description = (
                    f"A pocket survey token made in {region_label} after the encounter with the {display_name.lower()}. "
                    f"{observation} It reminds its bearer to keep the mark and its cause in separate notes. "
                )
            equipment_description += f"Tăng {attack_bonus} Công và {guard_bonus} Giáp."
            move_id = MOVE_BY_SPECIES.get(creature_slug, "")
            move_reach = round(max(2.8, 2.8 + level * 0.15), 2) if move_id else 0.0
            additions["monster_catalog.json"].append({
                "id": monster_id, "displayName": display_name, "rank": "common",
                "maxHealth": 40 + level * 8, "attackDamage": 5 + level,
                "attackReach": 1.25, "approachSpeed": round(0.88 + min(level, 10) * 0.028, 3),
                "lungeDistance": 1.65, "lungeSeconds": 0.34, "lungeStopDistance": 0.68,
                "openingDelay": round(1.3 - min(level, 8) * 0.035, 3), "closingSeconds": 1.12,
                "telegraphSeconds": 0.92, "recoverySeconds": 0.98, "counterBonusDamage": 12,
                "hitCooldown": round(0.7 - min(level, 5) * 0.025, 3),
                "spriteResource": f"crawl_{creature_slug}", "lungeSpriteResource": "",
                "spriteScale": 2.55, "spritePixelsPerUnit": 32,
                "specialMoveId": move_id, "specialMoveReach": move_reach,
            })
            position = region["positions"][(local_index - (0 if quest_number == 1 else 3)) % len(region["positions"])]
            additions["encounter_catalog.json"].append({
                "id": encounter_id, "monsterId": monster_id, "locationId": region["location"],
                "positionX": position[0], "positionY": position[1], "requiredQuestId": quest_id,
                "blockedQuestId": "", "blockedDialogueId": "", "contributesToQuest": True,
                "defeatObjectiveTargetId": monster_id, "defeatDialogueId": dialogue_id,
                "downDialogueId": "rowan_field_retreat",
                "reward": {"gold": 9 + level * 3, "items": []},
            })
            additions["item_catalog.json"].append({
                "id": item_id, "name": equipment_name, "description": equipment_description,
                "category": "equipment", "equipmentSlot": slot, "maxStack": 1,
                "attackBonus": attack_bonus, "guardBonus": guard_bonus, "healAmount": 0,
                "sellValue": 48 + level * 10,
            })
            objective_area = FIELD_AREAS[region_code]
            region_members[region_code].append((monster_id, item_id, display_name))
            case_title, _ = CASES[region_code][quest_number - 1]
            objective_description = (
                f"Defeat {display_name} near {objective_area}; record the evidence for {case_title.lower()}."
            )
            quest_objectives[region_code][quest_number - 1].append({
                "id": f"defeat_{creature_slug}", "kind": "defeat", "targetId": monster_id,
                "requiredCount": 1, "description": objective_description,
            })
            quest_rewards[region_code][quest_number - 1].append({"itemId": item_id, "quantity": 1})
            area = FIELD_AREAS[region_code]
            first_line = (
                f"The field sheet names this creature {display_name}. {observation} "
                f"I marked the time and cleared {area}, but I cannot infer how it reached the site from this trace alone."
            )
            additions["dialogue_catalog.json"].append({
                "id": dialogue_id, "speakerName": "ROWAN HALE",
                "lines": [first_line, follow_up],
            })
            art_payloads.append((ART / f"crawl_{creature_slug}.png", pixels))
            digest = hashlib.sha256(pixels).hexdigest()
            mapping_rows.append((f"crawl_{creature_slug}", source_entry, monster_id, region["location"], digest))

    # Reject duplicate pixels: a different filename or recolour is not a new field species.
    sprite_hashes = [row[-1] for row in mapping_rows]
    if len(sprite_hashes) != len(set(sprite_hashes)):
        raise SystemExit("Two selected species use identical source pixels; remove the duplicate before import.")
    if any(len(region_members[code]) != 5 for code in REGIONS):
        raise SystemExit("Each existing map must receive five distinct new species.")

    # Rebuild the authored records now that every creature entry is known.
    for code, region in REGIONS.items():
        for number in (1, 2):
            quest_id = f"side_crawl_{code}_{number}"
            title, brief = CASES[code][number - 1]
            prerequisite = f"side_verdant_{code}_2" if number == 1 else f"side_crawl_{code}_1"
            objectives = quest_objectives[code][number - 1]
            rewards = quest_rewards[code][number - 1]
            if len(objectives) != (3 if number == 1 else 2):
                raise SystemExit(f"The {quest_id} case does not contain its expected distinct targets.")
            additions["prologue_quests.json"].append({
                "id": quest_id, "arcId": region["arc"], "stage": -1, "type": "side",
                "locationId": region["location"], "giverId": region["giver"],
                "title": title, "objective": brief, "prerequisiteIds": [prerequisite],
                "objectives": objectives,
                "reward": {"gold": 30 + region["level"] * 5, "items": rewards},
            })
        author, title, body = CODEX[code]
        additions["codex_catalog.json"].append({
            "id": f"crawl_codex_{code}", "title": title, "category": "Field Survey",
            "writtenBy": author, "unlockQuestId": f"side_crawl_{code}_2", "body": body,
        })

    for file_name, catalog in catalogs.items():
        old_ids = {entry.get("id", "") for entry in catalog["entries"]}
        new_ids = [entry["id"] for entry in additions[file_name]]
        if len(new_ids) != len(set(new_ids)) or old_ids.intersection(new_ids):
            raise SystemExit(f"Duplicate ID while preparing {file_name}.")

    for destination, pixels in art_payloads:
        if destination.exists():
            raise SystemExit(f"Sprite already exists: {destination}")
    for file_name, catalog in catalogs.items():
        catalog["entries"].extend(additions[file_name])
    try:
        for destination, pixels in art_payloads:
            destination.write_bytes(pixels)
        for file_name, catalog in catalogs.items():
            atomic_write(paths[file_name], catalog)
    except Exception:
        for destination, _ in art_payloads:
            destination.unlink(missing_ok=True)
        raise

    mapping_path = ROOT / "Docs/AssetArchives/crawl-creatures-map.tsv"
    with mapping_path.open("w", encoding="utf-8") as stream:
        stream.write("resource\tsource_archive_path\tmonster_id\tlocation\tsprite_sha256\n")
        for row in mapping_rows:
            stream.write("\t".join(row) + "\n")

    print("Imported 55 pinned CC0 Crawl sprites as 55 common monsters, encounters, two-line field records and unique equipment.")
    print("Added 22 chained regional contracts with 55 defeat objectives and 11 unlockable field studies.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeDecodeError, zipfile.BadZipFile, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"Crawl field import failed: {error}") from error
