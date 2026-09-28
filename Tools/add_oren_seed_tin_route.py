#!/usr/bin/env python3
"""Add Oren Bell's branching seed-tin story and a usable field-kitchen recipe."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"
PREFIX = "side_oren_seed_tin_"


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


# key, title, kind, target, objective, giver, speaker, lines, codex title/body, landmark (visual, x, y)
before_choice = [
    ("open", "The Tin Behind the Scale", "talk", "oren_bell",
     "Ask Oren Bell about the seed tin he has kept behind the warehouse scale.", "oren_bell", "OREN BELL",
     ["The tin was my mother's. I kept it behind the scale for years and told myself it was only a spare container.",
      "There is one small packet inside. I want to know what she meant to do with it before I decide where it belongs."],
     "The Tin Behind the Scale", "Oren asks Rowan to recover a seed tin hidden behind the warehouse scale. His mother gave it to him before the Cinderwell store was reorganized, and he has avoided opening it since. The last packet is small enough for one planted row. Oren wants to learn what she intended for it before he chooses whether the seed should remain a family keepsake or return to the community garden.", None),
    ("hinge", "A Hinge Mended Twice", "inspect", "oren_seed_tin_hinge",
     "Inspect the bent hinge and find where Oren's mother repaired the tin by hand.", "rowan_hale", "ROWAN HALE",
     ["The hinge has two kinds of solder. The older patch is neat; the newer one was done quickly and still holds.",
      "Someone fixed this before the tin was hidden. The repair marks are careful enough to have been made at home."],
     "Two Repairs on One Hinge", "The tin's lid carries two repairs. The first was made with a smooth bead of solder; the second leaves a thumb-shaped ridge beside the clasp. Oren recognizes his mother's work in the older patch and remembers trying to repair the hinge himself after a flood. Both repairs kept the lid shut. Neither one explains why the tin was hidden behind a public warehouse scale.", ("sealed_case", -8.2, 2.4)),
    ("paper", "The Note Under the Felt", "inspect", "oren_seed_tin_note",
     "Lift the felt lining and read the note folded beneath the tin's base.", "rowan_hale", "ROWAN HALE",
     ["The ink has run at one corner, but the sentence is still clear: 'Plant one row where someone can see it.'",
      "The note gives no date and no name. Oren will know the handwriting."],
     "A Note Under the Lining", "A short note sits beneath the felt lining: plant one row where someone can see it. The ink matches the pressure and slant of the mother's letters Oren keeps at home. The sentence is an instruction about a visible planting, not a claim that one row could feed the whole basin. Rowan returns the note with the tin rather than separating a family object from its words.", ("document", -5.5, -3.3)),
    ("date_marks", "The Marks That Are Not Dates", "inspect", "oren_seed_tin_marks",
     "Compare the scratches inside the tin with the seed season marks on Oren's old shelf.", "rowan_hale", "ROWAN HALE",
     ["These scratches count openings, not seasons. Three packets came out of the tin before this one.",
      "The shelf marks are later. The tin may have travelled with Oren's family before it reached the warehouse."],
     "Openings, Not Years", "Three shallow cuts run along the tin's inner rim. Oren says his mother used them to remember how many packets she had taken out, not which year she opened it. A separate set of marks on the warehouse shelf records seasonal inventory. Keeping those marks apart lets the family object speak for itself without turning it into an official store count.", ("herb_ledger", 0.7, 3.8)),
    ("june_memory", "June Remembers the Stove", "talk", "sister_june",
     "Ask Sister June what Oren's family cooked when the public kitchen was closed.", "sister_june", "SISTER JUNE",
     ["His mother used to press barley cakes flat so they would cook through on the little stove. Oren always wanted them crisp at the edge.",
      "I remember the food. I do not remember how much seed she kept, and I would not turn a supper memory into a store record."],
     "June's Kitchen Memory", "June remembers Oren's mother cooking thin barley cakes on a little stove after the public kitchen had closed for the night. Oren preferred the crisp edges and his mother gave him the first one to turn. June remembers a meal and a habit, not a quantity of stored grain. She offers to let Rowan use the Cinderwell kitchen if the old tin's barley is still viable.", None),
    ("first_row", "One Row in the Warm Bed", "grow", "cinderwell_barley",
     "Plant and harvest one kitchen row of Cinderwell Barley from the seed tin.", "oren_bell", "OREN BELL",
     ["One row is enough to learn whether this packet will grow. Keep it in the kitchen bed, where June can see it each day.",
      "If it sprouts, we can decide what to do with the next packet after we see the harvest."],
     "The Tin's First Row", "Rowan planted the tin's barley in the warm kitchen bed and harvested it after it matured. The crop grew, but one row is a single result under one set of conditions. June keeps the barley separate from both the protected reserve and the larger kitchen crop. Oren is relieved to see green shoots in the bed; he still wants the next packet's destination to be a choice made in daylight.", None),
    ("first_heads", "Heads Kept for the Table", "inspect", "oren_seed_tin_harvest_board",
     "Inspect the first harvest and separate the barley heads from the seed-bearing stems.", "rowan_hale", "ROWAN HALE",
     ["The heads are dry enough for the mill, but a few stems still carry whole kernels.",
      "June can cook the grain. Oren can decide whether the intact stems belong in the next planting."],
     "A Harvest with Two Uses", "The small harvest can be split between the kitchen and a later planting, but the portions have different uses. June selects dry barley for cooking while Oren sets aside stems that still carry intact kernels. The family packet has produced enough grain for a recipe trial and a modest second row. It has not replaced the basin reserve or demonstrated a dependable yield beyond this bed.", ("noticeboard", -8.1, -0.6)),
]

branch_steps = [
    ("exchange", "The Open Seed Shelf", "inspect", "oren_open_seed_shelf",
     "Place the tin's next packet on the open exchange shelf for any kitchen grower to use.", "oren_bell", "OREN BELL",
     ["The shelf is unlocked. Anyone taking the packet can leave a note about where they plant it, but no one owes us a name.",
      "I used to think giving a seed away meant losing it. The crop can carry the story farther than the tin."],
     "An Open Packet", "Oren places the next packet on an unlocked shelf beside the kitchen seed beds. He invites growers to leave a note about the planting conditions, but does not require a name or a promised return. The packet remains scarce; the choice gives several households a chance to grow it rather than preserving it in one locked container. The family tin stays with Oren.", ("seed_cradle", 8.0, -2.8), "open_exchange"),
    ("reserve", "A Place in the Winter Case", "inspect", "oren_winter_seed_case",
     "Store the tin's next packet in the dry winter case beside Oren's household seed lot.", "oren_bell", "OREN BELL",
     ["This case will keep the packet dry through the cold months. June can still cook from the first harvest we already set aside.",
      "Keeping this one safe is not a promise that every later packet will stay here."],
     "A Packet for Winter", "Oren stores the packet in a dry case beside his household seed lot. The choice protects a small amount for winter and leaves the already harvested barley available to June's kitchen. Oren labels the case with the tin's origin so a later keeper can find the packet without mistaking it for the strategic reserve. The decision is a seasonal safeguard, not a permanent rule for the basin.", ("sealed_case", 8.0, -2.8), "winter_case"),
]

after_choice = [
    ("custody", "The Choice Kept in Its Own Words", "talk", "oren_bell",
     "Tell Oren how the next seed packet will be kept and hear what the choice means to him.", "oren_bell", "OREN BELL",
     ["I can live with this. The important thing is that we chose while the packet was in front of us, instead of letting a shelf decide for us.",
      "My mother gave me a tin, not a rule. I should have asked what she wanted before making one out of it."],
     "Oren's Seed Custody Choice", "Oren accepts Rowan's decision about the second packet. He had turned his mother's tin into a private rule by keeping it closed, even though the note asked for a visible row. The new arrangement gives the seed a chosen place, either among the growers or in the winter case. Oren writes the reason beside the location so a future change can be discussed rather than inherited as an unexplained restriction.", None),
    ("perch", "A Perch for the Old Recipe", "fish", "emberscale_perch",
     "Catch one Emberscale Perch from the Cinderwell Warm Run for June's barley cakes.", "rowan_hale", "ROWAN HALE",
     ["The warm outlet is running clear enough to fish today. This catch gives June something local to fold into the barley cakes.",
      "One fish is one meal ingredient. It does not tell us how many are in the run."],
     "Fish for the Kitchen Trial", "Rowan catches an Emberscale Perch from the Cinderwell Warm Run for June's recipe. The fish gives the barley cakes a savory filling and uses the same local catch already available to the kitchen. The catch is an ingredient, not a survey of fish abundance or a judgment about the outlet's water. June asks Rowan to bring it straight to the brazier while it is fresh.", None),
    ("june_recipe", "The Recipe June Can Change", "talk", "sister_june",
     "Give June the harvested barley and ask her to adapt Oren's mother's barley cakes for the kitchen.", "sister_june", "SISTER JUNE",
     ["I can use the thin shape and the crisp edge she liked. The filling is new; the recipe belongs to the people who make it now.",
      "Let us write down what we actually cooked, then change it again if the next batch asks for something different."],
     "A Recipe Adapted for Cinderwell", "June adapts the family's thin barley cake for the Cinderwell kitchen. She keeps the quick-cooking shape and adds Emberscale Perch as a filling, while leaving room to change the seasoning later. The recipe records the meal Rowan and June actually prepare; it does not claim to reconstruct every version Oren's mother made. Cooking lets the family memory enter the shared kitchen without making the recipe a fixed inheritance.", None),
    ("cook", "The First Tin-Keeper's Cake", "craft", "oren_seedkeepers_cake",
     "Cook one Tin-Keeper's Barley Cake at Sister June's kitchen from Cinderwell Barley and Emberscale Perch.", "sister_june", "SISTER JUNE",
     ["Keep the cake thin, turn it once, and let the edges crisp before the filling dries.",
      "This batch is a kitchen meal Rowan can carry. We can make another when people ask for it."],
     "Tin-Keeper's Barley Cake", "The first Tin-Keeper's Barley Cake combines the old thin shape with a filling June chose for the present kitchen. The field recipe uses two measures of Cinderwell Barley and one Emberscale Perch, producing a single restorative meal for Rowan. June's notes describe the pan heat and turning time so the dish can be repeated or changed. The tin supplied the seed; the recipe belongs to everyone who cooks it.", None),
    ("cooling_rack", "The Edge Before the Middle", "inspect", "oren_seed_cake_rack",
     "Inspect the cake on the cooling rack and check that its center has finished cooking.", "rowan_hale", "ROWAN HALE",
     ["The edge has browned before the middle. June lowers the heat and gives it another turn.",
      "Now the filling is hot through, and the cake can travel without breaking apart."],
     "Cooling Rack Check", "The first cake browned at the edge before its middle had cooked through. June lowered the heat and turned it once more. The correction matters because the old recipe's thin shape is easy to scorch when a heavier filling is added. Rowan records the adjustment beside the dish rather than changing the inherited memory: the kitchen method can improve without deciding what Oren's mother must have done.", ("document", 6.5, -2.8)),
    ("taste", "A Taste Oren Recognizes", "talk", "oren_bell",
     "Let Oren taste the finished barley cake and ask what part of the old meal he remembers most.", "oren_bell", "OREN BELL",
     ["The crisp edge. She always waited until I stopped watching the pan, then gave me the browned piece.",
      "It tastes different from hers. That is fine. June cooked this one with us here."],
     "A Taste Recognized", "Oren recognizes the crisp edge and recalls waiting beside his mother's pan for the browned piece. He notices that June's filling and seasoning are different from the meal he remembers. The difference does not spoil the memory; it gives him a new meal to associate with it. Oren asks Rowan to keep the recipe with the tin's note so neither one is mistaken for the other.", None),
    ("second_packet", "A Packet for a Second Row", "talk", "oren_bell",
     "Ask Oren for another Cinderwell barley packet so the family seed can be planted one more time.", "oren_bell", "OREN BELL",
     ["Here is one packet from the kitchen trial lot. It is separate from the tin's last packet and the protected reserve.",
      "Plant it only if you have room to watch the row through harvest. A seed needs attention after it leaves the shelf."],
     "The Second Kitchen Packet", "Oren supplies one packet from a small kitchen trial lot, separate from both the family tin and the basin reserve. This seed lets Rowan repeat the warm-bed planting after learning how the first crop matured. Oren is more comfortable offering it now that the first packet has a chosen home and a recipe has been made. The packet still needs a gardener's attention; its label cannot promise a harvest.", None),
    ("empty_tin", "The Tin Can Breathe", "inspect", "oren_seed_tin_open",
     "Inspect the empty tin after Oren removes its last family packet and leaves the lid unlatched.", "rowan_hale", "ROWAN HALE",
     ["With the packet gone, the felt lining lies flat. The tin is no longer hiding anything from its owner.",
      "Oren leaves the lid open on the kitchen shelf beside the recipe."],
     "An Open Tin", "Oren removes the final family packet and leaves the tin unlatched on the kitchen shelf. Its felt lining no longer holds the folded note in a hidden space. The tin can carry seeds again if Oren chooses, but it no longer has to remain a closed memorial. He places the recipe beside it so the container and the meal can share a shelf without becoming the same kind of record.", ("sealed_case", -8.0, 2.2)),
    ("second_row", "A Second Row, Watched Together", "grow", "cinderwell_barley",
     "Plant and harvest a second kitchen row of Cinderwell Barley from Oren's trial packet.", "oren_bell", "OREN BELL",
     ["The first row taught us how the warm wall holds heat. This time June and I will watch it together.",
      "Keep the seed and the grain separate at harvest, then we can decide what another planting should use."],
     "The Second Kitchen Row", "Rowan, June and Oren grow a second row from the separate kitchen trial packet. They watch the bed together and keep seed-bearing stems apart from barley intended for cooking. The crop gives Oren a new experience to remember beside his mother's tin: this time he does not tend the row alone. Two small harvests still do not prove that every bed will behave alike, but the second planting is a practice the kitchen can choose to repeat.", None),
    ("new_shoots", "Green at the Warm Wall", "inspect", "oren_second_row_shoots",
     "Inspect the new shoots and compare how the two rows responded to the kitchen bed.", "rowan_hale", "ROWAN HALE",
     ["The second row is shorter near the stone seam, where the soil dries first.",
      "Oren says his mother's row had the same bare patch. June adds water there, not across the whole bed."],
     "Two Rows in One Bed", "The second row has a short patch near a seam in the warm wall. Oren remembers the same bare patch from his mother's old garden, and June finds that this strip of soil dries sooner than the rest. She waters only the affected part rather than increasing the whole bed's use. The observation helps them care for this garden; it is not a universal rule about Cinderwell soil or the barley variety.", ("waymarker", -8.4, -1.7)),
    ("june_aftertaste", "June Sets Out Three Plates", "talk", "sister_june",
     "Ask June who she would invite to share the next batch of barley cakes.", "sister_june", "SISTER JUNE",
     ["Oren can bring someone who remembers his mother. I can invite the late cistern shift, and Rowan can bring whoever is still on the road.",
      "No one has to explain why they came for food. That was the part of the old kitchen I want to keep."],
     "Three Plates for a Later Meal", "June suggests inviting one person who remembers Oren's mother, the late cistern shift and someone returning along the road. She does not ask the guests to explain why they need a meal or to prove a connection to the old kitchen. Oren likes that the recipe can be shared without requiring the family story as its entry price. The next batch will depend on who comes and what the pantry can spare.", None),
    ("note_return", "The Note in Daylight", "inspect", "oren_seed_tin_note_display",
     "Place the folded family note beside the open tin where Oren can read it in daylight.", "rowan_hale", "ROWAN HALE",
     ["The sentence looks less like a warning in the daylight. It reads like an invitation to plant where neighbors could see.",
      "Oren smooths the fold but leaves the note unsigned."],
     "The Family Note in Daylight", "Oren lays the note beside the open tin instead of beneath its lining. In the kitchen's daylight, the sentence about a visible row reads as an invitation rather than a private command. He smooths the fold without adding a signature or date that was not there before. The family object is easier to share when its words can be read, while their meaning remains open to the people who use the garden.", ("document", 8.3, 0.6)),
    ("next_season", "What the Next Season Needs", "talk", "oren_bell",
     "Ask Oren what he wants the kitchen to do when the next seed season begins.", "oren_bell", "OREN BELL",
     ["I want the growers to look at the beds with June before deciding which seed can spare a packet.",
      "My mother left me a tin and a sentence. I can keep both without making either one the only voice in the garden."],
     "Oren's Next-Season Intention", "Oren wants the kitchen growers to review the beds with June before deciding whether any crop can spare seed for another planting. He will keep his mother's tin open and the note beside it, and he will let the next group decide how much of the kitchen lot can travel. The seed's future now includes a shared meal and a garden practice, while Oren's family memory stays his to tell on his own terms.", None),
    ("afterword", "The Tin Stays Open", "talk", "oren_bell",
     "Speak with Oren after the second harvest and agree to leave the family tin open beside June's recipe.", "oren_bell", "OREN BELL",
     ["The tin is lighter, but I don't feel that I have lost it. We planted what was inside, and people have eaten from it.",
      "Leave the recipe nearby. Someone else can make the cakes while I decide what the next row should be."],
     "Afterword: A Seed Memory Shared", "Oren leaves the tin open beside June's adaptable barley cake recipe. The family packet grew twice in the warm bed, and its grain became a meal the kitchen can repeat. Oren remains the keeper of his mother's story, but the seed no longer has to stay hidden for the story to survive. The growers can revisit where future packets belong as each season arrives and the kitchen's needs become clear.", None),
]


def objective(key, kind, target, description, dialogue):
    return {"id": "resolve_" + key, "kind": kind, "targetId": target,
            "requiredCount": 1, "description": description, "dialogueId": dialogue}


def make_quest(key, title, kind, target, description, giver, dialogue_id, previous,
               reward=None, branch=None, branch_prereq=None, any_of=None):
    quest = {
        "id": PREFIX + key, "arcId": "crown_of_empty_fields", "stage": -1, "type": "side",
        "locationId": "cinderwell_basin", "giverId": giver, "title": title,
        "objective": description,
        "objectives": [objective(key, kind, target, description, dialogue_id)],
        "reward": reward or {"gold": 8 if kind in ("talk", "choice") else 6, "items": []},
    }
    if previous:
        quest["prerequisiteIds"] = [previous]
    if branch:
        quest["branchFlag"], quest["branchValue"] = branch
    if branch_prereq:
        quest["prerequisiteIds"] = [branch_prereq]
    if any_of:
        quest.pop("prerequisiteIds", None)
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": any_of}]
    return quest


quests, dialogues, codex, landmarks = [], [], [], []
previous = "side_june_pantry_afterword"


def add_step(step, previous_id):
    key, title, kind, target, description, giver, speaker, lines, record_title, body, marker = step
    qid = PREFIX + key
    did = "oren_seed_tin_" + key
    quests.append(make_quest(key, title, kind, target, description, giver, did, previous_id,
                             reward={"gold": 8 if kind in ("talk", "choice") else 6, "items": []}))
    dialogues.append({"id": did, "speakerName": speaker, "lines": lines})
    codex.append({"id": "oren_seed_tin_" + key + "_record", "title": record_title,
                  "category": "Oren Bell", "writtenBy": speaker.title(), "unlockQuestId": qid, "body": body})
    if marker:
        visual, x, y = marker
        landmarks.append({"id": "oren_seed_tin_" + key + "_marker", "locationId": "cinderwell_basin",
                          "displayName": title[:58], "targetId": target, "visualId": visual,
                          "positionX": x, "positionY": y, "scale": 0.085})
    return qid


for step in before_choice:
    next_id = add_step(step, previous)
    if step[0] == "open":
        quests[-1]["reward"]["items"] = [{"itemId": "cinderwell_barley_seed", "quantity": 1}]
    previous = next_id

choice = {
    "id": "seed_custody", "title": "Where the Next Packet Will Sleep", "kind": "choice",
    "target": "oren_seed_custody_choice",
    "description": "Choose whether the tin's next packet goes to the open kitchen exchange or the dry winter case.",
    "giver": "oren_bell", "speaker": "OREN BELL",
    "lines": ["This packet came from my family's tin. The first row has already grown, and June has grain for the kitchen.",
              "Where should this next packet stay until someone is ready to plant it?"],
    "record_title": "Where the Next Packet Will Sleep",
    "body": "The second packet can go to an unlocked kitchen exchange shelf or a dry winter case beside Oren's household seed lot. Both choices keep it apart from the protected basin reserve and leave the first harvest available to the kitchen. Oren asks Rowan to choose its temporary home rather than treating the tin's hidden location as an inherited rule.",
    "marker": ("noticeboard", -0.5, -4.1),
}
qid = PREFIX + "choice"
did = "oren_seed_tin_choice"
choice_quest = make_quest("choice", choice["title"], choice["kind"], choice["target"], choice["description"],
                          choice["giver"], did, previous)
choice_quest["choiceFlag"] = "oren_seed_custody"
choice_quest["choiceSpeaker"] = choice["speaker"]
choice_quest["choicePrompt"] = choice["description"]
choice_quest["choices"] = [
    {"id": "exchange", "label": "Leave the packet on the unlocked shelf for kitchen growers.",
     "flagValue": "open_exchange", "dialogueId": "oren_seed_tin_choice_exchange",
     "reward": {"gold": 0, "items": [{"itemId": "open_seed_loop_charm", "quantity": 1}]}},
    {"id": "reserve", "label": "Store the packet in the dry winter case beside Oren's lot.",
     "flagValue": "winter_case", "dialogueId": "oren_seed_tin_choice_reserve",
     "reward": {"gold": 0, "items": [{"itemId": "winter_tin_hook_charm", "quantity": 1}]}},
]
quests.append(choice_quest)
dialogues.append({"id": did, "speakerName": choice["speaker"], "lines": choice["lines"]})
codex.append({"id": "oren_seed_tin_choice_record", "title": choice["record_title"], "category": "Oren Bell",
              "writtenBy": "Oren Bell", "unlockQuestId": qid, "body": choice["body"]})
visual, x, y = choice["marker"]
landmarks.append({"id": "oren_seed_tin_choice_marker", "locationId": "cinderwell_basin",
                  "displayName": choice["title"], "targetId": choice["target"], "visualId": visual,
                  "positionX": x, "positionY": y, "scale": 0.085})
previous = qid

branch_ids = []
for key, title, kind, target, description, giver, speaker, lines, record_title, body, marker, branch_value in branch_steps:
    did = "oren_seed_tin_" + key
    branch_qid = PREFIX + key
    quests.append(make_quest(key, title, kind, target, description, giver, did, None,
                             branch=("oren_seed_custody", branch_value), branch_prereq=previous))
    dialogues.append({"id": did, "speakerName": speaker, "lines": lines})
    codex.append({"id": "oren_seed_tin_" + key + "_record", "title": record_title,
                  "category": "Oren Bell", "writtenBy": speaker.title(), "unlockQuestId": branch_qid, "body": body})
    visual, x, y = marker
    landmarks.append({"id": "oren_seed_tin_" + key + "_marker", "locationId": "cinderwell_basin",
                      "displayName": title, "targetId": target, "visualId": visual,
                      "positionX": x, "positionY": y, "scale": 0.085})
    branch_ids.append(branch_qid)

previous = None
for index, step in enumerate(after_choice):
    key = step[0]
    if index == 0:
        qid = add_step(step, None)
        quests[-1]["prerequisiteGroups"] = [{"anyOfQuestIds": branch_ids}]
        previous = qid
        continue
    next_id = add_step(step, previous)
    if key == "second_packet":
        quests[-1]["reward"]["items"] = [{"itemId": "cinderwell_barley_seed", "quantity": 1}]
    previous = next_id

dialogues.extend([
    {"id": "oren_seed_tin_choice_exchange", "speakerName": "OREN BELL", "lines": [
        "Put it on the open shelf. A grower can take it without asking me for permission first.",
        "I will leave a blank card beside it for planting notes, not names." ]},
    {"id": "oren_seed_tin_choice_reserve", "speakerName": "OREN BELL", "lines": [
        "Keep it in the winter case. The first packet has already given June grain for the kitchen.",
        "I want this one dry until the growers can look at the beds together." ]},
])

items = [
    {"id": "oren_seedkeepers_cake", "name": "Tin-Keeper's Barley Cake",
     "description": "A thin, crisp-edged field-kitchen meal adapted from Oren Bell's family memory. Restores 44 health when used.",
     "category": "consumable", "equipmentSlot": "", "maxStack": 10,
     "attackBonus": 0, "guardBonus": 0, "healAmount": 44, "sellValue": 0},
    {"id": "open_seed_loop_charm", "name": "Open Seed Loop",
     "description": "A copper loop from the kitchen exchange shelf, shaped to hang an unsealed seed packet where growers can reach it.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
    {"id": "winter_tin_hook_charm", "name": "Winter Tin Hook",
     "description": "A felt-wrapped hook for hanging Oren's dry seed tin above the wash basin through the cold season.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 0, "guardBonus": 3, "healAmount": 0, "sellValue": 0},
]
recipe = {
    "id": "cook_oren_seedkeepers_cake", "displayName": "Cook Tin-Keeper's Barley Cake",
    "stationId": "cinderwell_kitchen", "discipline": "cooking",
    "outputItemId": "oren_seedkeepers_cake", "outputQuantity": 1,
    "ingredients": [{"itemId": "cinderwell_barley", "quantity": 2},
                    {"itemId": "emberscale_perch", "quantity": 1}],
}

for filename, additions in [
    ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", codex), ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items), ("recipe_catalog.json", [recipe]),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} Oren quests, {len(codex)} codex records, {len(dialogues)} dialogues, "
      f"{len(landmarks)} landmarks, and one kitchen recipe.")
