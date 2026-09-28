#!/usr/bin/env python3
"""Add Sister June's Cinderwell kitchen and field-to-table side story."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, catalog):
    (CONTENT / name).write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    positions = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in positions:
            entries[positions[entry["id"]]] = entry
        else:
            positions[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, kind, target, objective, giver, speaker, dialogue, codex title, codex body, target visual, xy
steps = [
    ("open", "A Pot for the Road Back", "talk", "sister_june",
     "Ask Sister June why the Cinderwell kitchen has stayed cold after the convoy report.", "sister_june", "SISTER JUNE",
     ["The pot is clean. The people who used it have gone in three directions, and I will not pretend one supper brings them back together.",
      "Still, the workers keeping the cistern open need a meal that was made here, with food grown and caught here. Will you help me make one?"],
     "June Reopens the Kitchen", "Sister June does not describe the meal as payment for work or proof that the displaced people have been accounted for. She wants the kitchen fire lit again because the sluice crew and the remaining households still need to eat. The convoy report has been delivered, but its list does not describe who is hungry at this hour. June keeps one cooking place open and invites each person to take food without giving a reason.", "", None),
    ("hearth", "The Hearth Has a Split Lip", "inspect", "june_kitchen_hearth",
     "Inspect the cracked edge of the old stone hearth before building a fire beneath it.", "rowan_hale", "ROWAN HALE",
     ["The crack starts at the iron pot ring and runs toward the water channel. A hard fire could spread it.",
      "The stone is not ready for heat. We can use the small brazier while Talia checks the draft."],
     "Hearth Inspection", "A thin crack runs from the iron pot ring to the hearth's drainage groove. The stone remains level, but the crack could lengthen if the pot is heated unevenly. June chooses the portable brazier until a mason can inspect the full hearth. Rowan records the safe limit as a cooking precaution, not as a claim that the structure has been repaired.", "kitchen_hearth", (7.1, 2.7)),
    ("pantry", "A Muck in the Grain Locker", "defeat", "tiny_cw_cinderwell_muck",
     "Clear the Cinderwell Muck from the grain locker so June can reach the dry sacks.", "sister_june", "SISTER JUNE",
     ["It slipped through the drain when the old locker door swelled. I can reach the dry sacks, but not without putting my hand beside that mouth.",
      "Clear it out. Keep the door closed until I have checked which grain stayed dry."],
     "Pantry Muck Cleared", "The Cinderwell Muck has left the grain locker, and the access path is open again. June inspects the remaining sack seams herself and separates those that stayed dry from the ones softened by the drain. The creature's presence explains why the door was left shut; it does not explain how the grain was stored before the flood or who last used each sack.", "", None),
    ("draft", "A Flame That Does Not Fight the Sluice", "talk", "talia_mercer",
     "Ask Talia how to keep the brazier's draft from pulling smoke toward the workers' water channel.", "talia_mercer", "TALIA MERCER",
     ["The channel draws air when the lower gate opens. Put the brazier on the uphill side and leave this gap clear.",
      "I can tell you where smoke will travel in this room. I cannot certify a kitchen wall by looking at one afternoon's airflow."],
     "Brazier Draft Notes", "Talia marks the path between the lower gate, the air gap and the portable brazier. The draft changed while the sluice wheel was moving, so she recommends leaving the gap open and moving the flame uphill. It is a practical arrangement for the current work shift, not a building inspection or a promise that every later fire will draw the same way.", "", None),
    ("oren", "A Seed Kept for Eating", "talk", "oren_bell",
     "Ask Oren Bell for a small barley seed lot that may be harvested for a meal and replanted later.", "oren_bell", "OREN BELL",
     ["This is a kitchen lot, not a replacement for the reserve. Take one packet and keep the planting row separate from the sacks set aside for next season.",
      "The harvest can feed someone or provide seed. It cannot do both unless we leave enough grain untouched."],
     "Oren's Barley Lot", "Oren gives Rowan a small packet of Cinderwell barley from a lot reserved for kitchen trials. He asks June to keep the crop apart from the protected seed store, since the same grain cannot be eaten and replanted. The packet is not a share of the strategic reserve and does not change the basin's official allocation. It gives the kitchen a local ingredient and a chance to save seed if the harvest permits it.", "", None),
    ("grow", "Barley Beneath the Warm Wall", "grow", "cinderwell_barley",
     "Plant and harvest Cinderwell barley in the kitchen bed beside the warm wall.", "sister_june", "SISTER JUNE",
     ["This bed catches the late warmth from the stone. Give it water from the kitchen jar, not the sluice bucket marked for the canal.",
      "When the heads are ready, save the dry grain before the rain returns."],
     "First Barley Harvest", "The barley was planted in the kitchen bed and harvested after reaching maturity. The bed's position beside the stone wall kept it warmer than the open basin, although one crop does not establish a dependable yield. June sets aside two measures for cooking and returns any intact seed heads to Oren for review. The kitchen lot remains separate from the reserve crop, so the harvest does not silently alter the basin's seed ledger.", "", None),
    ("fish", "A Perch from the Warm Run", "fish", "emberscale_perch",
     "Catch one Emberscale Perch from the Cinderwell Warm Run using Earthworm Bait.", "rowan_hale", "ROWAN HALE",
     ["The fish are holding where the warm outlet meets the basin. The bright scales make this one easy to see when it turns.",
      "I have one perch. It is enough for the pot, though it tells us nothing about how many fish the outlet can support."],
     "Cinderwell Warm Run Catch", "Rowan caught an Emberscale Perch where warm outlet water meets the basin. The Cinderwell spot has a weighted catch table and uses one unit of Earthworm Bait per cast. A single successful catch gives the kitchen one ingredient; it is not a population survey and does not establish that the outlet is safe for drinking. The fish goes to June for cooking rather than to the water ledger.", "", None),
    ("grindstone", "The Millstone Still Turns", "inspect", "june_kitchen_millstone",
     "Inspect the small kitchen millstone and confirm it turns without grinding grit into the barley.", "rowan_hale", "ROWAN HALE",
     ["The stone turns evenly when it is dry. A little sand has collected under its lip, but the channel did not reach this shelf.",
      "I have brushed the grit away. June can grind a small batch here and check each measure before it goes into the pot."],
     "Kitchen Millstone", "The hand mill turns evenly after grit is brushed from the lower lip. The shelf stayed above the last visible water mark, though June will still inspect each measure before cooking. The mill is suited to a small batch; using it for the whole reserve would create a different job and require a separate cleaning and storage plan.", "kitchen_millstone", (5.2, -0.2)),
    ("cook", "The First Cinderwell Stone Pot", "craft", "cinderwell_stonepot_broth",
     "Cook two bowls of Stone-Pot Broth at Sister June's kitchen from barley and Emberscale Perch.", "sister_june", "SISTER JUNE",
     ["The barley is local, the fish came from the warm run, and the brazier is drawing away from the water channel.",
      "Stir slowly. We will make two bowls so one can stay here and one can travel, depending on what the workers ask for."],
     "Stone-Pot Broth Recipe", "The first Cinderwell Stone-Pot Broth uses two measures of local barley and one Emberscale Perch. The kitchen recipe produces two bowls, allowing one serving to be shared while Rowan keeps another for recovery. June records the ingredients and brazier position so that the meal can be repeated. The recipe is a field kitchen dish; it is not a claim about nutrition beyond its in-game restorative effect.", "", None),
    ("sample", "Taste Before the Shift Changes", "inspect", "june_broth_sample",
     "Inspect the broth before it is portioned and note whether the fish has cooked through.", "rowan_hale", "ROWAN HALE",
     ["The barley has softened, and the perch flakes apart at the edge. The small brazier kept the pot at a steady simmer.",
      "June tastes it before serving. She wants the meal judged by the people eating it, not by the recipe's neat handwriting."],
     "First Pot Check", "The barley has softened and the perch flakes apart, showing that this batch reached June's current cooking standard. The dish has only been made once, so the timing is a starting point. June asks for feedback from the people eating the meal and leaves room to change the recipe. A clean pot and a repeatable procedure matter, but neither substitutes for asking whether the food is welcome.", "broth_sample", (6.0, -2.8)),
    ("choice", "Who Gets the First Bowl?", "choice", "june_service_priority",
     "Choose whether June serves the people staying by the cistern first or packs the first bowl for the departing road crew.", "sister_june", "SISTER JUNE",
     ["There are two bowls and more than two people who could use them. We can serve the kitchen shift that remains, or pack one for the crew leaving before dawn.",
      "I will not call either group more deserving. Choose where the first bowl goes, and keep the second for yourself."],
     "First Bowl Decision", "June offers the first bowl to either the people remaining at the cistern kitchen or the road crew preparing to leave before dawn. The choice affects who receives the first serving and the token Rowan carries afterward. It does not determine who is more deserving, change the water allocation or settle the convoy's destination. One bowl stays with Rowan and can restore health through the inventory menu.", "noticeboard", (0.2, -4.3)),
    ("table", "A Bowl at the Common Table", "interact", "june_common_table",
     "Serve one bowl of Stone-Pot Broth at the Cinderwell common table for the kitchen shift.", "rowan_hale", "ROWAN HALE",
     ["The bowls are on the table. June asks each worker whether they want a serving before she ladles it out.",
      "The people who stay can eat before the next sluice check. No one has to sign for a meal."],
     "Common Table Serving", "One bowl of Stone-Pot Broth was served at the common table to workers who chose to remain for the meal. June leaves the ladle in reach and does not collect names or signatures. This option gives the staying shift food before the next sluice check. The table record describes a serving event, not the number of people who ate or the amount each person needed.", "common_table", (7.4, -3.6)),
    ("departure", "A Bowl Packed for the Road", "interact", "june_departure_crate",
     "Pack one bowl of Stone-Pot Broth with the road crew's provisions before its dawn departure.", "rowan_hale", "ROWAN HALE",
     ["The clay cup fits inside the provision crate. Leave the lid loose enough to vent while the broth cools.",
      "The crew can decide who carries it. We are packing one serving, not estimating what the road will demand."],
     "Road Crew Provision", "One bowl of Stone-Pot Broth was packed with the road crew's provisions. The cup was left to vent while cooling, then secured inside the crate. June does not assign the food to a named traveler; the crew will decide who carries it. The entry records one packed serving and leaves the road's length, crew size and future food needs outside its claim.", "sealed_case", (5.8, 3.4)),
    ("table_report", "The Shift Has Its Own Recipe", "talk", "sister_june",
     "Tell Sister June how the common-table serving went and let the shift adjust the next batch together.", "sister_june", "SISTER JUNE",
     ["They asked for a little more barley and less salt. The person who tends the late gate said the warm run fish held its texture.",
      "I will write both comments beside the recipe. Next time the kitchen decides whether they still want the change."],
     "Common Table Feedback", "The Cinderwell shift asked for more barley and less salt in the next batch. A worker tending the late gate liked the perch's texture. June records both comments as feedback from this meal rather than a vote by the whole basin. The recipe stays adjustable; anyone eating it later can ask for a different serving or decline it without losing access to the kitchen.", "", None),
    ("departure_report", "The Road Crew Can Carry Its Own Meal", "talk", "sister_june",
     "Tell Sister June how the crew packed the serving and agree to leave the carrier's place undecided.", "sister_june", "SISTER JUNE",
     ["The crate is ready. The crew chose who will carry the cup, and I did not need to write a name on it.",
      "That is enough for the handoff. They can open it when they stop, or give it to someone who needs it sooner."],
     "Road Meal Handoff", "The crew secured one serving for travel and chose its carrier among themselves. June did not assign the bowl to a particular person or add it to the cargo count as a person marker. The handoff is complete when the food leaves the kitchen under the crew's care. Its eventual use remains with the travelers, who may eat, share or pass it on.", "", None),
    ("afterword", "The Kitchen Stays Open", "talk", "sister_june",
     "Speak with Sister June after the first service and agree to keep the kitchen available for anyone who wants a meal.", "sister_june", "SISTER JUNE",
     ["The fire is small, the recipe can change, and the table does not ask why someone came late.",
      "That is what I can keep open tonight. Tomorrow the people here can decide what the kitchen should become."],
     "Afterword: A Kitchen Without a Roll Call", "June keeps the portable brazier available for another meal service. The first pot connected a local crop, a caught fish and a cooking station, while the branch decision determined whether its first bowl stayed with the kitchen shift or traveled with the road crew. Rowan retains a second bowl as a usable healing item. The kitchen's continued use depends on the people who choose to come back; this entry does not promise steady food supply or repair the cracked permanent hearth.", "", None),
]

quests, dialogues, codex, landmarks = [], [], [], []
previous = "cinder_june_report"
positions = {
    "hearth": (4.8, 3.8), "grindstone": (-9.1, -4.5), "sample": (9.2, -0.6),
    "choice": (0.2, -4.3), "table": (-0.5, -4.4), "departure": (9.2, 3.0),
}
# Landmark visual IDs are stored on each authored step above.
for key, title, kind, target, objective, giver, speaker, lines, record_title, body, visual, position in steps:
    qid = "side_june_pantry_" + key
    dialogue_id = "june_stonepot_" + key
    quest = {
        "id": qid, "arcId": "crown_of_empty_fields", "stage": -1, "type": "side",
        "locationId": "cinderwell_basin", "giverId": giver, "title": title,
        "objective": objective, "prerequisiteIds": [previous],
        "objectives": [{"id": "resolve_" + key, "kind": kind, "targetId": target,
                        "requiredCount": 1, "description": objective, "dialogueId": dialogue_id}],
        "reward": {"gold": 8 if kind in ("talk", "choice") else 6, "items": []},
    }
    if key == "open":
        quest["reward"]["items"] = [
            {"itemId": "earthworm_bait", "quantity": 2},
        ]
    if key == "oren":
        quest["reward"]["items"] = [{"itemId": "cinderwell_barley_seed", "quantity": 1}]
    if key == "choice":
        quest["choiceFlag"] = "june_service_priority"
        quest["choiceSpeaker"] = "SISTER JUNE"
        quest["choicePrompt"] = "Where should June send the first bowl of the kitchen's two-serving batch?"
        quest["choices"] = [
            {"id": "common_table", "label": "Serve the Cinderwell kitchen shift at the common table.",
             "flagValue": "common_table", "dialogueId": "june_stonepot_choice_table",
             "reward": {"gold": 0, "items": [{"itemId": "june_hearth_shift_button", "quantity": 1}]}},
            {"id": "road_crew", "label": "Pack the first bowl with the dawn road crew's provisions.",
             "flagValue": "road_crew", "dialogueId": "june_stonepot_choice_road",
             "reward": {"gold": 0, "items": [{"itemId": "june_travel_ladle_charm", "quantity": 1}]}}
        ]
    if key in ("table", "table_report"):
        quest["prerequisiteIds"] = ["side_june_pantry_choice"]
        quest["branchFlag"] = "june_service_priority"
        quest["branchValue"] = "common_table"
    elif key in ("departure", "departure_report"):
        quest["prerequisiteIds"] = ["side_june_pantry_choice"] if key == "departure" else ["side_june_pantry_departure"]
        quest["branchFlag"] = "june_service_priority"
        quest["branchValue"] = "road_crew"
    if key == "table_report":
        quest["prerequisiteIds"] = ["side_june_pantry_table"]
    if key == "afterword":
        quest.pop("prerequisiteIds")
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": ["side_june_pantry_table_report", "side_june_pantry_departure_report"]}]
    quests.append(quest)
    dialogues.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex.append({"id": "june_stonepot_" + key + "_record", "title": record_title,
                  "category": "Cinderwell Kitchen", "writtenBy": speaker.title(),
                  "unlockQuestId": qid, "body": body})
    if visual and position:
        landmarks.append({"id": "june_stonepot_" + key + "_marker", "locationId": "cinderwell_basin",
                          "displayName": title[:58], "targetId": target, "visualId": visual,
                          "positionX": position[0], "positionY": position[1], "scale": 0.085})
    previous = qid

# Choice branch dialogues are separate entries so each selected route has its own readable result.
dialogues.extend([
    {"id": "june_stonepot_choice_table", "speakerName": "SISTER JUNE", "lines": [
        "Set the first bowl at the common table. The people staying near the cistern can eat before the next sluice check.",
        "Leave the second bowl with Rowan. The shift can decide tomorrow whether to make another pot." ]},
    {"id": "june_stonepot_choice_road", "speakerName": "SISTER JUNE", "lines": [
        "Pack the first bowl for the crew leaving before dawn. They can choose who carries and shares it.",
        "Leave the second bowl with Rowan. No cargo entry needs to turn a serving into a headcount." ]},
    {"id": "june_stonepot_muck_down", "speakerName": "ROWAN HALE", "lines": [
        "The Cinderwell Muck has left the grain locker. The sacks are still closed, and June can check the seams herself.",
        "The drain is clear for now. Keep the wet sacks apart from the barley we are about to grow." ]},
    {"id": "june_stonepot_muck_retry", "speakerName": "ROWAN HALE", "lines": [
        "The Muck caught me beside the swollen pantry door. I need to recover before I try the drain again.",
        "June can keep the dry sacks closed until I return. The pantry route is still marked." ]},
])

items = [
    {"id": "cinderwell_barley_seed", "name": "Cinderwell Barley Seed", "description": "A small kitchen-trial lot from Oren Bell. The grain can be eaten or replanted, so each harvest needs an explicit use.", "category": "material", "equipmentSlot": "", "maxStack": 20, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "cinderwell_barley", "name": "Cinderwell Barley", "description": "A small warm-wall harvest for the communal kitchen. It is a cooking ingredient, not a measure of basin-wide yield.", "category": "material", "equipmentSlot": "", "maxStack": 20, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "cinderwell_stonepot_broth", "name": "Stone-Pot Broth", "description": "A two-serving field-kitchen meal made from Cinderwell barley and Emberscale Perch. Restores 36 health when used.", "category": "consumable", "equipmentSlot": "", "maxStack": 10, "attackBonus": 0, "guardBonus": 0, "healAmount": 36, "sellValue": 0},
    {"id": "june_hearth_shift_button", "name": "Hearth Shift Button", "description": "A brass button from the common kitchen apron, returned to June after the meal shift. Its smooth back is easier to grip than a coin.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 0, "guardBonus": 2, "healAmount": 0, "sellValue": 0},
    {"id": "june_travel_ladle_charm", "name": "Road Meal Ladle Charm", "description": "A small ladle token marked for travel provisions. It carries the memory of a bowl shared by the road crew without naming its bearer.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
]
recipe = {
    "id": "cook_cinderwell_stonepot_broth", "displayName": "Cook Stone-Pot Broth",
    "stationId": "cinderwell_kitchen", "discipline": "cooking",
    "outputItemId": "cinderwell_stonepot_broth", "outputQuantity": 2,
    "ingredients": [{"itemId": "cinderwell_barley", "quantity": 2},
                    {"itemId": "emberscale_perch", "quantity": 1}],
}
farm = {"id": "cinderwell_barley_bed", "locationId": "cinderwell_basin", "positionX": -8.8, "positionY": 3.5,
        "cropId": "cinderwell_barley", "cropDisplayName": "Cinderwell Barley",
        "seedItemId": "cinderwell_barley_seed", "harvestItemId": "cinderwell_barley",
        "harvestQuantity": 2, "growSeconds": 120}
fishing = {"id": "cinderwell_warm_run", "locationId": "cinderwell_basin", "displayName": "Cinderwell Warm Run",
           "positionX": 4.8, "positionY": 4.2, "baitItemId": "earthworm_bait",
           "biteDelayMinSeconds": 2.6, "biteDelayMaxSeconds": 4.8, "biteWindowSeconds": 1.15,
           "catches": [{"itemId": "emberscale_perch", "weight": 78},
                       {"itemId": "blackreed_trout", "weight": 22}]}
encounter = {"id": "june_pantry_cinderwell_muck", "monsterId": "tiny_cw_cinderwell_muck",
             "locationId": "cinderwell_basin", "positionX": 1.1, "positionY": 3.6,
             "requiredQuestId": "side_june_pantry_pantry", "blockedQuestId": "",
             "blockedDialogueId": "", "contributesToQuest": True,
             "defeatObjectiveTargetId": "tiny_cw_cinderwell_muck",
             "defeatDialogueId": "june_stonepot_muck_down", "downDialogueId": "june_stonepot_muck_retry",
             "reward": {"gold": 0, "items": []}}

for filename, additions in [
    ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", codex), ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items), ("recipe_catalog.json", [recipe]),
    ("farm_catalog.json", [farm]), ("fishing_catalog.json", [fishing]),
    ("encounter_catalog.json", [encounter]),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} Sister June quests, {len(codex)} codex entries, {len(landmarks)} landmarks, "
      f"{len(items)} items, a cooking recipe, a farm plot, a fishing spot and an encounter.")
