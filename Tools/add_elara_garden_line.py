#!/usr/bin/env python3
"""Install Elara Wren's playable Dawnkeep garden side story into content catalogs."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


def quest(qid, title, objective, objective_id, kind, target, description, dialogue_id,
          prerequisite, reward_gold, reward_items=None):
    return {
        "id": qid,
        "arcId": "the_order_of_the_dawn",
        "stage": -1,
        "type": "side",
        "locationId": "dawnkeep_outpost",
        "giverId": "elara_wren",
        "title": title,
        "objective": objective,
        "prerequisiteIds": [prerequisite] if prerequisite else [],
        "objectives": [{
            "id": objective_id,
            "kind": kind,
            "targetId": target,
            "requiredCount": 1,
            "description": description,
            **({"dialogueId": dialogue_id} if dialogue_id else {}),
        }],
        "reward": {"gold": reward_gold, "items": reward_items or []},
    }


dialogues = [
    {"id": "elara_garden_open", "speakerName": "ELARA WREN", "lines": [
        "The cadet garden used to sit below the east gutter. Each shift was meant to water one bed and leave the next to the person coming after.",
        "I archived the rotation as a table of duties. When the barracks emptied, the table remained and the garden dried out. I kept the record; I never learned how the water reached the roots.",
        "If we can make the bed work again, the next cadets can learn it with their hands. I want them to see what one careful shift leaves for another."
    ]},
    {"id": "rowan_garden_shift_notes", "speakerName": "ROWAN HALE", "lines": [
        "The old slate lists a morning turn, a late turn, and one blank interval after rain. It records where the water was sent, not who stood beside the trough.",
        "A smear of mint green crosses the last entry. Someone added a leaf beside the missing interval, then rubbed the drawing away with a wet thumb.",
        "The empty space can remain empty. The note still tells us that the bed used to be tended after a storm."
    ]},
    {"id": "elara_garden_shift_response", "speakerName": "ELARA WREN", "lines": [
        "I thought the blank interval meant a keeper had failed to report. Now I think the slate only stopped when the work changed hands.",
        "The gutter is still here. If the drain is sound, a new rotation can begin without pretending we know who planted the last bed."
    ]},
    {"id": "rowan_garden_drain_frame", "speakerName": "ROWAN HALE", "lines": [
        "The drain frame is bent at the lower hinge. Rain ran past the garden wall instead of entering the open channel.",
        "The mud holds two parallel grooves. One may be from a tool dragged across the stone; neither groove says who left it there.",
        "I can measure the slope after we clear the mint bed. The frame will need a removable clip so the next person can inspect it."
    ]},
    {"id": "elara_garden_seed", "speakerName": "ELARA WREN", "lines": [
        "The old mint still grows in one crack near the eastern step. I saved seed from the patch before the passage was closed.",
        "Plant a small bed and let it finish a full cycle. If the runoff misses it, we will know before anyone uses the slate as a promise."
    ]},
    {"id": "rowan_garden_trout", "speakerName": "ROWAN HALE", "lines": [
        "This Blackreed Trout came from the same lakeshore pool where the gutter drains. Its scales can mark a removable clip, but one fish cannot tell us how clean the water is.",
        "I will keep the catch and the place beside each other in the field note. The mint needs a separate inspection before we call the bed healthy."
    ]},
    {"id": "rowan_garden_waterline", "speakerName": "ROWAN HALE", "lines": [
        "The lower stone has a pale line where water reached it after the last rain. The upper scratch may come from the roof hinge, not the channel.",
        "I marked both heights without joining them into a single level. We will compare the next flow after the clip is fitted.",
        "The Blackreed Trout was caught downstream. That confirms its location at the time of the catch, not the source of the water above us."
    ]},
    {"id": "nia_garden_shift_review", "speakerName": "NIA PORTER", "lines": [
        "A rotation works only if the person on the next turn can change it when the weather changes. The old slate has a blank interval because there was no night shift after rain.",
        "Keep one line for the work and another for a handoff. No one should inherit a duty from a name scratched into stone."
    ]},
    {"id": "elara_garden_brace_complete", "speakerName": "ELARA WREN", "lines": [
        "The Runoff Clip is ready. The mint fiber pads its jaw, while the trout scale marks the edge that must remain visible above the gutter.",
        "It can be removed without breaking the drain. A keeper should be able to check what passed through, not seal the channel and call it repaired."
    ]},
    {"id": "rowan_garden_housing", "speakerName": "ROWAN HALE", "lines": [
        "The clip fits the bent frame and leaves a narrow gap for leaves and sediment to pass. The marker will remain visible at low water.",
        "This fitting is a maintenance aid, not a water filter. I will compare its mark with the garden bed after the next measured run."
    ]},
    {"id": "rowan_garden_trial", "speakerName": "ROWAN HALE", "lines": [
        "The first runoff reached the upper bed in the short test. A second pour carried grit into the catch pocket; the clip held but needs cleaning after heavy rain.",
        "Elara recorded the time it took to clear the pocket. We have one day of observation, not a seasonal water plan.",
        "The mint is still upright. That is a result from this plot, not proof that every bed on the slope will grow the same way."
    ]},
    {"id": "elara_garden_common_response", "speakerName": "ELARA WREN", "lines": [
        "A shared bed could let any cadet plant a cutting when they have a free hour. Someone would still need to clear the catch pocket after rain.",
        "I can put the care steps on the slate and leave the next row open for a different plant. The people who use it can decide what belongs there."
    ]},
    {"id": "elara_garden_rotation_response", "speakerName": "ELARA WREN", "lines": [
        "We could mark three short turns on the slate and let each training group choose a week. The plot would have a keeper for a while, then return to the next group.",
        "The schedule needs a blank line for weather and a way to step out. A rotation is useful only while it can be changed."
    ]},
    {"id": "rowan_garden_shared_plan", "speakerName": "ROWAN HALE", "lines": [
        "The common-bed sheet lists the water route and the removable clip, then leaves the crop row open. It gives no one a permanent claim over the soil.",
        "I added the day of our runoff test and left a space for the next keeper to repeat it."
    ]},
    {"id": "rowan_garden_rotation_plan", "speakerName": "ROWAN HALE", "lines": [
        "The rotation sheet shows three short turns and a pause after heavy rain. Its marks follow the gutter, not the names of the cadets who once carried water.",
        "Anyone taking a turn can amend the day or step out. The unfilled row is part of the schedule, not a missing person."
    ]},
    {"id": "elara_garden_afterword", "speakerName": "ELARA WREN", "lines": [
        "I used to think an archive began after the work was finished. The garden taught me that a handoff can be part of the record while the water is still moving.",
        "Next week I will ask the cadets to build a second catch pocket, then I will let them decide what to plant beside the mint.",
        "The slate will stay by the door. Anyone can leave a correction before the next turn begins."
    ]},
]

quests = [
    quest("side_elara_garden_open", "The Bed Beneath the East Gutter",
          "Elara Wren wants to restore a cadet garden whose water rotation was recorded but never taught. Help her check the old slate before choosing a new way to tend the bed.",
          "ask_elara", "talk", "elara_wren", "Hear why Elara wants to reopen the cadet garden.",
          "elara_garden_open", "order_cadet_oath", 8,
          [{"itemId": "dawnmeadow_mint_seed", "quantity": 1}, {"itemId": "earthworm_bait", "quantity": 6}]),
    quest("side_elara_garden_shift_notes", "A Blank Turn After Rain",
          "Read the duty slate beside the garden. The missing interval may describe a change in work rather than a cadet who failed to report.",
          "read_shift_slate", "inspect", "elara_garden_shift_notes", "Read the watering turns and the blank interval.",
          "rowan_garden_shift_notes", "side_elara_garden_open", 7),
    quest("side_elara_garden_shift_talk", "The Keeper Who Never Took a Turn",
          "Elara has spent years preserving the old rotation without trying it herself. Ask what she learned from the blank interval.",
          "ask_about_blank_turn", "talk", "elara_wren", "Ask Elara how she now reads the blank turn.",
          "elara_garden_shift_response", "side_elara_garden_shift_notes", 8),
    quest("side_elara_garden_drain", "The Bent Lower Hinge",
          "Inspect the drain frame and decide where a removable fitting can sit without sealing the runoff channel.",
          "inspect_drain_frame", "inspect", "elara_garden_drain_frame", "Check the hinge and parallel grooves.",
          "rowan_garden_drain_frame", "side_elara_garden_shift_talk", 8),
    quest("side_elara_garden_mint", "Mint in the Crack by the Step",
          "Plant the saved Dawnmeadow Mint seed in the new bed. Let one crop cycle finish before using the runoff slate as a guide.",
          "grow_mint", "grow", "dawnmeadow_mint", "Plant and harvest Dawnmeadow Mint at the east garden bed.",
          "elara_garden_seed", "side_elara_garden_drain", 10),
    quest("side_elara_garden_fish", "A Catch from the Same Shore",
          "Catch a Blackreed Trout at the Dawnkeep lakeshore. Elara wants a scale for the edge of a removable waterline clip.",
          "catch_scale_sample", "fish", "blackreed_trout", "Catch a Blackreed Trout at the Dawnkeep lakeshore.",
          "rowan_garden_trout", "side_elara_garden_mint", 9),
    quest("side_elara_garden_waterline", "Two Scratches, Two Heights",
          "Read the stones by the gutter. The pale waterline and the upper scratch may have different causes, so keep their measurements separate.",
          "read_root_scale", "inspect", "elara_garden_level_board", "Compare the two marks without combining their causes.",
          "rowan_garden_waterline", "side_elara_garden_fish", 9),
    quest("side_elara_garden_nia", "A Turn That Can Be Changed",
          "Nia Porter remembers how the garden shift was handed over. Ask her how the next keeper should record a turn without inheriting a fixed duty.",
          "ask_nia_handoff", "talk", "nia_porter", "Hear Nia's suggestion for a flexible garden handoff.",
          "nia_garden_shift_review", "side_elara_garden_waterline", 9),
    quest("side_elara_garden_brace", "The Removable Runoff Clip",
          "At Dawnkeep Forge, join one Dawnmeadow Mint and one Blackreed Trout scale into a small removable clip. It should mark the gutter without sealing it.",
          "craft_runoff_clip", "craft", "dawnkeep_runoff_clip", "Forge the Runoff Clip at Dawnkeep Forge.",
          "elara_garden_brace_complete", "side_elara_garden_nia", 10),
    quest("side_elara_garden_install", "Set the Clip Above the Gutter",
          "Fit the Runoff Clip into the repaired frame. It will stay there to mark the waterline and can be removed for cleaning.",
          "install_runoff_clip", "interact", "elara_garden_rain_housing", "Install the Runoff Clip in the east gutter frame.",
          "rowan_garden_housing", "side_elara_garden_brace", 10),
    quest("side_elara_garden_trial", "One Test Pour",
          "Read the first catch-pocket trial. The fitting held in two pours, but grit gathered at its edge and only one short observation was recorded.",
          "read_trial_sheet", "inspect", "elara_garden_trial_sheet", "Read the two pours and the recorded cleaning time.",
          "rowan_garden_trial", "side_elara_garden_install", 12),
    quest("side_elara_garden_policy", "A Shared Bed or a Short Rotation",
          "Elara can leave the new bed open to anyone who wants to plant, or set short, changeable turns for training groups. Choose how she will teach its upkeep.",
          "choose_bed_care", "choice", "elara_garden_policy_board", "Choose a way to share responsibility for the garden.",
          None, "side_elara_garden_trial", 12),
]

choice = quests[-1]
choice["choiceFlag"] = "elara_garden_care"
choice["choiceSpeaker"] = "ELARA WREN"
choice["choicePrompt"] = (
    "The old shift slate made the garden look like a duty that had to be completed by whoever came next. "
    "I could leave a common bed open and post the care steps, so anyone can add a plant when they have time. "
    "Or I could offer short turns to training groups and let each group change or leave its week. "
    "The gutter still needs cleaning after heavy rain either way. The sign cannot assign a keeper who has not agreed to take a turn."
)
choice["choices"] = [
    {"id": "common_bed", "label": "Open one shared bed and post the care steps.",
     "flagValue": "common_bed", "dialogueId": "elara_garden_common_response",
     "reward": {"gold": 0, "items": [{"itemId": "dawnkeep_common_soil_charm", "quantity": 1}]}},
    {"id": "short_rotation", "label": "Offer short turns that each group may change or leave.",
     "flagValue": "short_rotation", "dialogueId": "elara_garden_rotation_response",
     "reward": {"gold": 0, "items": [{"itemId": "dawnkeep_rotating_bed_knot", "quantity": 1}]}},
]

shared = quest("side_elara_garden_shared_bed", "The Open Row beside the Mint",
               "Read the care sheet for the shared bed. It leaves crop choice open and records a test date without assigning the soil to a permanent keeper.",
               "read_shared_bed_plan", "inspect", "elara_garden_shared_bed_plan",
               "Read the shared-bed care sheet and its runoff test date.",
               "rowan_garden_shared_plan", "side_elara_garden_policy", 12)
shared["branchFlag"] = "elara_garden_care"
shared["branchValue"] = "common_bed"
quests.append(shared)

rotation = quest("side_elara_garden_rotation_plan", "Three Turns with a Weather Pause",
                 "Read the short rotation plan. Each group can change its week or step out, and the garden pauses after heavy rain.",
                 "read_rotation_plan", "inspect", "elara_garden_rotation_plan",
                 "Check the three changeable turns and the weather pause.",
                 "rowan_garden_rotation_plan", "side_elara_garden_policy", 12)
rotation["branchFlag"] = "elara_garden_care"
rotation["branchValue"] = "short_rotation"
quests.append(rotation)

afterword = quest("side_elara_garden_afterword", "The Slate beside the Door",
                  "The chosen care plan is filed beside the measured runoff test. Speak with Elara about how she will teach the next group to maintain the bed.",
                  "talk_after_garden", "talk", "elara_wren", "Hear Elara's plan for the next planting lesson.",
                  "elara_garden_afterword", None, 15)
afterword["prerequisiteGroups"] = [{"anyOfQuestIds": [
    "side_elara_garden_shared_bed", "side_elara_garden_rotation_plan"
]}]
quests.append(afterword)

items = [
    {"id": "dawnmeadow_mint_seed", "name": "Dawnmeadow Mint Seed", "description": "A seed saved from the crack by the Dawnkeep east step. Elara kept it after the cadet garden stopped receiving water.", "category": "material", "equipmentSlot": "", "maxStack": 99, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 1},
    {"id": "dawnmeadow_mint", "name": "Dawnmeadow Mint", "description": "A small silver-edged leaf grown below the east gutter. Its harvest marks one completed crop cycle; it does not certify the runoff as safe.", "category": "material", "equipmentSlot": "", "maxStack": 99, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 3},
    {"id": "dawnkeep_runoff_clip", "name": "East Gutter Runoff Clip", "description": "A removable bronze clip padded with Dawnmeadow fiber and marked with one Trout scale. The open jaw records a waterline without sealing the drain.", "category": "quest", "equipmentSlot": "", "maxStack": 1, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "dawnkeep_common_soil_charm", "name": "Common Soil Knot", "description": "A charm woven from the first garden mint, given to a keeper of the shared bed. Its loose end can be retied by the next gardener. Tăng 1 Công và 1 Giáp.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 38},
    {"id": "dawnkeep_rotating_bed_knot", "name": "Garden Turn Knot", "description": "A bronze loop with three movable marks for short garden turns. No mark is fixed to a cadet's name. Tăng 1 Công và 2 Giáp.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 2, "healAmount": 0, "sellValue": 38},
]

recipes = [{
    "id": "forge_dawnkeep_runoff_clip", "displayName": "Forge the East Gutter Runoff Clip",
    "stationId": "dawnkeep_forge", "discipline": "smithing", "outputItemId": "dawnkeep_runoff_clip",
    "outputQuantity": 1,
    "ingredients": [{"itemId": "dawnmeadow_mint", "quantity": 1}, {"itemId": "blackreed_trout", "quantity": 1}],
}]

farm = [{
    "id": "dawnkeep_dawnmeadow_bed", "locationId": "dawnkeep_outpost", "positionX": -7.0, "positionY": 3.4,
    "cropId": "dawnmeadow_mint", "cropDisplayName": "Dawnmeadow Mint",
    "seedItemId": "dawnmeadow_mint_seed", "harvestItemId": "dawnmeadow_mint",
    "harvestQuantity": 2, "growSeconds": 110,
}]

landmarks = [
    {"id": "elara_garden_shift_notes_marker", "locationId": "dawnkeep_outpost", "displayName": "Garden Shift Slate", "targetId": "elara_garden_shift_notes", "visualId": "document", "positionX": -3.4, "positionY": 3.5, "scale": 0.085},
    {"id": "elara_garden_drain_frame_marker", "locationId": "dawnkeep_outpost", "displayName": "Bent East Gutter Frame", "targetId": "elara_garden_drain_frame", "visualId": "door_brace", "positionX": 0.7, "positionY": -1.8, "scale": 0.085},
    {"id": "elara_garden_level_board_marker", "locationId": "dawnkeep_outpost", "displayName": "Garden Waterline Board", "targetId": "elara_garden_level_board", "visualId": "stone_rill", "positionX": 6.8, "positionY": 3.5, "scale": 0.085},
    {"id": "elara_garden_rain_housing_marker", "locationId": "dawnkeep_outpost", "displayName": "East Gutter Clip Frame", "targetId": "elara_garden_rain_housing", "visualId": "signal_frame", "positionX": 2.0, "positionY": 3.5, "scale": 0.085},
    {"id": "elara_garden_trial_sheet_marker", "locationId": "dawnkeep_outpost", "displayName": "Catch Pocket Trial Sheet", "targetId": "elara_garden_trial_sheet", "visualId": "document", "positionX": 8.6, "positionY": 1.8, "scale": 0.085},
    {"id": "elara_garden_policy_board_marker", "locationId": "dawnkeep_outpost", "displayName": "Garden Care Board", "targetId": "elara_garden_policy_board", "visualId": "noticeboard", "positionX": -2.1, "positionY": -4.5, "scale": 0.085},
    {"id": "elara_garden_shared_bed_marker", "locationId": "dawnkeep_outpost", "displayName": "Open Garden Row Sheet", "targetId": "elara_garden_shared_bed_plan", "visualId": "seed_cradle", "positionX": 5.3, "positionY": -4.4, "scale": 0.085},
    {"id": "elara_garden_rotation_plan_marker", "locationId": "dawnkeep_outpost", "displayName": "Changeable Garden Turns", "targetId": "elara_garden_rotation_plan", "visualId": "herb_ledger", "positionX": -10.4, "positionY": 1.1, "scale": 0.085},
]

codex = [
    {"id": "dawnkeep_garden_runoff_record", "title": "The East Gutter Catch Pocket", "category": "Maintenance record", "writtenBy": "Elara Wren", "unlockQuestId": "side_elara_garden_trial", "body": "Elara Wren reopened the bed below Dawnkeep's east gutter after finding a slate of watering turns and one blank interval after rain. The blank row was not a cadet roster. It described a pause in the rotation when the night shift had no reason to water. A patch of old mint survived in a crack beside the step, and a saved seed grew through one new crop cycle.\n\nRowan checked the lower hinge, the pale waterline on the garden stone, and an upper scratch that may have come from the roof hinge. He kept those marks separate. A removable bronze clip, padded with mint fiber and marked with one Blackreed Trout scale, held in two short pours. Grit gathered at the catch pocket and required cleaning. The trial records one plot and one day of observation. It does not certify the runoff, the lakeshore water, or other beds on the slope."},
    {"id": "dawnkeep_garden_shared_bed_record", "title": "Care Steps for a Shared Bed", "category": "Garden practice", "writtenBy": "Elara Wren", "unlockQuestId": "side_elara_garden_shared_bed", "body": "The shared-bed sheet begins with a water route, a removable gutter clip, and the date of the last catch-pocket test. The crop row remains open. A gardener may add a plant without being assigned a permanent duty, and anyone using the bed can amend the care steps after observing a new runoff.\n\nThe first mint harvest came from the seed Elara saved near the eastern step. It shows that this small plot completed a crop cycle. It does not show that every seed will take, that the drain stays clear in heavy rain, or that the lakeshore is safe to drink. The next person should compare the clip's mark after a new pour and clean the pocket before planting again. An empty row on the slate is available space, not a missing report."},
    {"id": "dawnkeep_garden_rotation_record", "title": "Three Short Turns and a Weather Pause", "category": "Garden practice", "writtenBy": "Elara Wren", "unlockQuestId": "side_elara_garden_rotation_plan", "body": "The rotating-bed sheet divides the care into short turns: prepare the soil, inspect the gutter, then clear the catch pocket after rain. Each training group can change the day or step out of its turn. A blank interval follows heavy weather so the next keeper can inspect the drain before sending water through it again.\n\nThe marks follow the task instead of a cadet's name. The rotation may help a class remember what has been checked, but it cannot assign work to someone who has not agreed to take a turn. Elara keeps the earlier watering slate beside the new version so a future gardener can compare both plans and replace either one. The mint bed has one recorded harvest and one short runoff test; neither result fixes the garden's next schedule."},
    {"id": "dawnkeep_garden_afterword", "title": "The Slate beside the Door", "category": "Workshop note", "writtenBy": "Elara Wren", "unlockQuestId": "side_elara_garden_afterword", "body": "Elara moved the care slate beside the garden door rather than storing it with the old cadet roster. A person approaching the bed can see where the gutter drains, when the pocket was cleaned, and how to leave a correction. The chosen plan opens the shared row to anyone who wants to plant, or offers short turns that each group can change or leave. Both keep the runoff test visible and the clip removable.\n\nThe first crop was modest. Elara chose to treat it as a lesson that can be repeated, not as proof that the old garden has returned unchanged. She will teach the next cadets to check the waterline, clear grit, and decide together what to plant beside the mint. A later group may choose a different crop, change the turn, or leave the bed quiet until the drain is checked again."},
]

for name, entries in [
    ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", codex), ("item_catalog.json", items),
    ("recipe_catalog.json", recipes), ("farm_catalog.json", farm),
    ("quest_landmarks.json", landmarks),
]:
    catalog = read(name)
    upsert(catalog["entries"], entries)
    write(name, catalog)

print(f"Installed {len(quests)} Dawnkeep quests, {len(dialogues)} dialogues, {len(codex)} field records,")
print(f"{len(items)} items, {len(recipes)} recipe, {len(farm)} farm bed and {len(landmarks)} landmarks.")
