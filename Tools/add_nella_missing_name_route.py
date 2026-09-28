#!/usr/bin/env python3
"""Add Nella Pike's family-led missing-name archive route to Ashen Oath."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, location, giver, kind, target, objective, speaker, spoken lines,
# codex title/body, landmark visual and position, rewards.
steps = [
    ("open", "The Blank Name That Stays Blank", "salt_road", "nella_pike", "talk", "nella_pike",
     "Ask Nella to preserve her younger sibling's missing place in the crossing record without guessing where they went.", "NELLA PIKE",
     ["My younger sibling's pass card came back. They did not. I want the record to keep those two facts apart.",
      "The family can ask for a copy later. No public list gets to turn that empty place into a headcount."],
     "Nella Opens a Family Search", "Nella carries the pass card of a younger sibling who did not return from the Salt Road crossing. She asks Rowan to preserve the card and the gap between its stamped passage and the missing person's later route. No name is added to the public count, and no destination is inferred from the card. The family may request, correct or withdraw a copy. The investigation records where each mark was found and who could see it, leaving the search open for evidence that can still be checked.", "", None, []),
    ("card", "The Card Records One Crossing", "salt_road", "rowan_hale", "inspect", "nella_pass_card_notches",
     "Inspect the pass card's lower edge and list only the checkpoint stamp, two notches and surviving cord hole.", "ROWAN HALE",
     ["The stamp confirms one passage through this checkpoint. The missing corner cannot tell us who carried the card afterward.",
      "I will copy the notch spacing and leave the next route blank until another source supports it."],
     "Pass Card: A Bounded Record", "The pass card establishes that one person crossed a named checkpoint and that two notches were scratched beside its stamp. A trimmed corner and an empty cord hole show the card was handled, but not by whom or at what later time. Rowan makes a line drawing rather than writing a presumed destination. The card is not a list of the travelers who followed it, and a matching route mark cannot stand in for the missing person's own account. Nella approves a family copy with space for correction.", "", None, []),
    ("wall", "Nine Missing Tags and Broken Plaster", "salt_road", "rowan_hale", "inspect", "salt_wall_name_slots",
     "Inspect the wall of missing tags and distinguish the nine empty hooks from the plaster removed around them.", "ROWAN HALE",
     ["Nine hooks are empty, but the broken plaster spreads wider than their spacing. We cannot tell whether every hook held a traveler tag.",
      "I'll record nine empty positions and a damaged wall, not nine people and a cause."],
     "The Wall Does Not Supply Nine Names", "Nine hook positions on the shelter wall are empty. A larger section of plaster has broken away, so the original arrangement is uncertain. Nella remembers seeing several tags here but cannot identify which one belonged to her sibling from this wall alone. The count describes hooks that are empty now; it does not establish how many travelers stayed in the shelter or when the tags disappeared. The wall map preserves the damaged area beside the empty positions and leaves every identity unassigned.", "", None, []),
    ("ruth", "Ruth's Dispatch Is Not the Tag List", "salt_road", "ruth_calder", "talk", "ruth_calder",
     "Ask Ruth whether the order she concealed included a named list of the people who reached the lower road.", "RUTH CALDER",
     ["The dispatch named a return direction and a bell interval. It did not name each person at the bend.",
      "I hid the paper. That is mine to answer for; it does not let me fill Nella's missing name."],
     "The Dispatch and the Missing Place", "Ruth confirms that the recovered dispatch contains a route instruction but no complete passenger list. Her admission that she hid the page is preserved separately from Nella's account of a missing younger sibling. The document cannot show who was beyond the road bend, and it does not provide a name for the empty place on the shelter wall. Rowan links the dispatch to the investigation as one source among several, without treating the two families' records as a single case or allowing Ruth's responsibility to overwrite Nella's evidence.", "", None, []),
    ("docket", "The Docket Counts Transfers", "salt_lockhouse", "rowan_hale", "inspect", "salt_lockhouse_docket",
     "Read the Lockhouse transfer docket and separate each cargo count from the unnamed person markers in its margin.", "ROWAN HALE",
     ["These totals describe bundles moved between shelves. The docket never says that each bundle belonged to one traveler.",
      "The margin has room for a marker, not a name. We should preserve that difference."],
     "Transfer Docket: Cargo Is Not a Person", "The Lockhouse docket records bundles transferred between shelves and a small number of unlabelled margin marks. Its units refer to containers, not people. One line is overwritten and the surviving tally cannot be reconciled with the total in the dispatch. Rowan copies the entry with the overwritten line visible and marks the mismatch as unresolved. The docket has no sibling name and no destination field. Its value is in showing how records were moved through the Lockhouse, not in turning cargo counts into a count of missing travelers.", "", None, []),
    ("return_mark", "The Salt Mark on the Return Rail", "salt_road", "rowan_hale", "inspect", "pike_tag_return_mark",
     "Inspect the salt-dark mark on the return rail and compare its width with the pass card's worn edge without calling it a match.", "ROWAN HALE",
     ["The widths are close. Salt and handling can change both edges, so similarity is not identification.",
      "The shard in the rail can help us make a safer sleeve, but it cannot tell us whose mark this was."],
     "Rail Mark: Similar Width, Different Claim", "A dark mark on the return rail is close in width to the worn edge of Nella's pass card. Salt deposits can widen a stain, and a card can be trimmed after its original use; the comparison therefore does not establish that the two marks came from the same object. A dryglass chip can be recovered from the rail casing for a protective sleeve. Rowan logs the chip as material from the Lockhouse return rail, not as evidence of who handled the pass card.", "document", (-2.7, 2.2), [{"itemId": "dryglass_shard", "quantity": 1}]),
    ("skate", "Saltspool Scale for a Surface Test", "salt_road", "silas_vane", "fish", "saltspool_skate",
     "Catch a Saltspool Skate at the sheltered pool for a practice surface test of the salty residue around the rail mark.", "SILAS VANE",
     ["The fish leaves a thin film on a practice strip. We'll test how a loose fiber catches it before touching the pass card.",
      "Keep the catch logged as a sample. A surface test can compare texture; it cannot identify a person."],
     "Saltspool Sample Receipt", "One Saltspool Skate was caught at the sheltered Salt Road pool using earthworm bait. Its oily scale film is used on a practice strip to see whether a Windglass fiber can lie flat beside a salt-marked surface. The test is about contact and preservation, not chemical dating or personal identification. Rowan records the catch location, date and bait so that this material cannot be confused with a fish taken during the earlier dispatch investigation. The whole specimen is consumed by the sleeve recipe as a recorded sample.", "", None, []),
    ("reed", "A Fresh Reed for the Sleeve", "salt_road", "rowan_hale", "grow", "windglass_reed",
     "Grow one Windglass Reed at the Salt Road plot to make a soft inner layer that will not abrade the pass card.", "NELLA PIKE",
     ["A reed fiber will keep the card from rubbing against the glass case. Please harvest it cleanly and note which plot it came from.",
      "The sleeve is for safekeeping. It does not make the card more complete than it is."],
     "Windglass Fiber for Safe Storage", "A Windglass Reed grown at the Salt Road plot provides the soft inner layer for a removable pass-card sleeve. The crop was planted from a seed Nella supplied after the route opened and harvested after the configured growing interval. Its fiber protects the card from abrasion; it does not restore the trimmed corner or reveal what was written there. Rowan records seed, plot and harvest together so a future conservator can replace the liner without claiming that a natural fiber has authenticated the card's owner.", "", None, []),
    ("fiber_check", "The Fiber Must Release Cleanly", "salt_road", "rowan_hale", "inspect", "pike_windglass_fiber_sample",
     "Check the harvested fiber on a dryglass practice strip and confirm it can be removed without leaving adhesive or residue.", "ROWAN HALE",
     ["It lifts without tearing the strip. That means the sleeve can be opened for inspection instead of sealing the card forever.",
      "We should preserve the right to review and revise, not just the object."],
     "A Reversible Liner", "The harvested fiber holds the practice strip without glue and can be lifted without leaving residue. This small test makes the proposed sleeve reversible: a family member or conservator can inspect the card later, change the liner or withdraw it from display. It is not a test of archival durability over generations. Rowan records the dry conditions and one successful removal, then asks Talia to build the sleeve with a clear inspection edge. No permanent seal should prevent the family from asking questions that the current record cannot answer.", "sealed_case", (9.0, 2.0), []),
    ("craft", "Talia's Removable Tag Sleeve", "cinderwell_basin", "talia_mercer", "craft", "pike_tag_sleeve",
     "Craft a removable tag sleeve at Cinderwell's assay bench from Windglass fiber, one Saltspool sample and the recovered dryglass chip.", "TALIA MERCER",
     ["The dryglass holds a narrow viewing edge; the fiber keeps it from scraping the card. The fish sample is a surface test, not a binding agent.",
      "I'll leave the seam openable and put the recipe on the receipt so it can be rebuilt or changed."],
     "Removable Sleeve Bench Record", "Talia assembled a narrow dryglass frame with a Windglass fiber liner and recorded the Saltspool surface sample used during the practice test. The recipe produces one removable sleeve with an openable seam. It is designed to prevent rubbing while keeping the pass card visible and accessible; it is not a secure evidence vault or a device for revealing erased marks. Rowan stores the recipe with the object so the family can request a replacement, refuse display or ask for the liner to be removed without losing the original card.", "", None, []),
    ("june", "June's Rule for Family Copies", "cinderwell_basin", "sister_june", "talk", "sister_june",
     "Ask Sister June how to keep a public crossing method separate from a family-held copy about one missing person.", "SISTER JUNE",
     ["A public method should teach how the count was made. It should not expose a household's private search without consent.",
      "Keep a receipt for every copy. The family can correct it, request it or take it back."],
     "Copy Rule: Method Public, Search by Consent", "Sister June proposes two layers of record. A public copy may describe how the checkpoint count and transfer mismatch were measured, with names and household details excluded. A separate copy about Nella's sibling remains under family control and can be corrected, requested or withdrawn. June's rule is a procedure, not proof that every family wants the same privacy. Rowan records who authorizes each copy and dates the request. The two layers should never be joined merely because they use the same road map or shelter-wall diagram.", "", None, []),
    ("seal", "The Unmarked Family Seal", "cinderwell_basin", "rowan_hale", "inspect", "pike_name_seal_rule",
     "Inspect the blank seal pouch and record who may open the private copy, what request can change it and how it can be withdrawn.", "ROWAN HALE",
     ["The pouch has no household name on its outside. The request slip names the person who may ask for it to be opened.",
      "A seal without a review rule is just another lock. The rule belongs beside it."],
     "Review and Withdrawal Rule", "The pouch stores no household name on its exterior. Its accompanying request slip states who may ask for the private copy to be opened, how a correction is attached and how the family can withdraw the copy from the archive. The seal protects access only while that rule remains available and understandable. It does not make the material more accurate, and it is not a substitute for a date or custody receipt. Rowan files the opening rule next to the pouch so that a later keeper cannot mistake secrecy for consent.", "noticeboard", (0.3, 3.0), []),
    ("install", "Fit the Sleeve without Closing the Case", "salt_lockhouse", "nella_pike", "interact", "pike_tag_sleeve_frame",
     "Fit the removable Tag Sleeve into the Lockhouse frame and place Nella's pass card inside without closing the family review seam.", "NELLA PIKE",
     ["The card stays visible, and I can still lift it out. Leave the seam where my family can reach it.",
      "Thank you for making room for another account instead of deciding the search is finished."],
     "The Pass Card in a Reversible Frame", "The pass card now sits behind a removable fiber liner in the Lockhouse frame. The clear edge leaves its stamp and two notches visible while keeping the card from rubbing against the glass. The family review seam remains openable and is recorded in the custody receipt. Installation consumes one crafted Tag Sleeve, but does not consume or alter the original pass card. A later inspection can remove the liner, add a dated note or take the card back out of public display.", "document", (4.8, 1.7), []),
    ("chain", "A Gap between Chain Tags", "salt_lockhouse", "rowan_hale", "inspect", "salt_lockhouse_chain_tags",
     "Inspect the unmarked chain tags and trace the missing segment without assigning a blank tag to Nella's sibling.", "ROWAN HALE",
     ["The chain has a gap and two tags without names. The metal does not tell us which one, if either, belonged to Nella's family.",
      "I will draw the break and preserve both tags as unassigned objects."],
     "Unassigned Tags and a Broken Link", "Two chain tags in the Lockhouse case have no surviving name, and one link is broken. Salt and pressure have worn the edges; the break may be old, but the file has no dated inspection. Nella recognizes neither tag as her sibling's. Rowan photographs the arrangement, records the empty interval and leaves both objects unassigned. The chain may show that a group of tags was handled together, but it does not prove that all tags belonged to people on one cart or that the broken link marked a departure.", "", None, []),
    ("silas", "Silas's View Stops at the Gate", "salt_road", "silas_vane", "talk", "silas_vane",
     "Ask Silas whether the first signal let him see the lower road or only tell someone at the gate to act.", "SILAS VANE",
     ["From inside the weigh station I could see the gate and one cart. The bend hid everyone farther down the road.",
      "A signal may carry farther than my eyes. I cannot say who heard it or who was still behind the wall."],
     "Signal Reach Is Not Sight", "Silas places himself inside the weigh station when he fired his first signal. The wall and bend blocked his view of the lower road, though an audible or visible signal could travel beyond that obstruction. His statement can narrow where he stood; it cannot establish who heard him, how the order was interpreted or how many travelers remained out of sight. Rowan keeps his revised position beside the earlier ridge account, with both dates visible. Neither version identifies Nella's sibling or assigns a tag in the Lockhouse case.", "", None, []),
    ("sightline", "The Unseen Road on the Sketch", "salt_road", "rowan_hale", "inspect", "pike_signal_gap_sketch",
     "Mark the bend hidden from Silas's position and draw a separate signal radius that does not imply every traveler received it.", "ROWAN HALE",
     ["The road bends behind the wall. A signal radius marks possible reach, not a list of who heard it.",
      "I'll leave the unseen section uncounted rather than fill it with an invented group."],
     "Sightline and Signal Radius", "The sketch separates Silas's line of sight from an estimated signal radius. The lower bend falls outside the visible wedge, while sound or light may have traveled around the wall. The radius is not surveyed and does not prove that any particular person received the signal. Rowan marks the hidden road as uncounted, adds the station wall and gate for orientation, and labels the drawing as a field sketch rather than a measured map. The image can guide another search without turning the unseen section into an assumed empty road.", "waymarker", (-6.0, 4.0), []),
    ("nella", "Nella Sets the Copy Boundary", "salt_road", "nella_pike", "talk", "nella_pike",
     "Review the copied evidence with Nella and confirm which details can go public and which remain under family control.", "NELLA PIKE",
     ["The route method can be public. The pass card and my sibling's search stay ours unless we ask otherwise.",
      "I want the archive to say what it lacks, then leave space for a correction."],
     "Nella's Copy Boundary", "Nella consents to public release of the counting method and the locations of the damaged records, with identifying details removed. The pass card, private request slip and family search remain under her household's control unless the family asks for a copy to be opened. She requests that the archive state that no destination is known and that the person remains missing from this record. Her decision is a boundary for this file, not a general rule for every family or a declaration that the search has ended.", "", None, []),
    ("policy", "How Should the Archive Hold the Gap?", "salt_road", "nella_pike", "choice", "pike_archive_policy",
     "Choose a public method-only record or a family-controlled review copy for Nella's pass-card evidence.", "NELLA PIKE",
     ["One record can publish the way we counted and keep every household detail out. The other can reserve the card for a family request.",
      "Both leave my sibling's destination blank. Choose who may read the evidence, not what the evidence cannot say."],
     "Archive Access Decision", "The archive can publish the counting method and the measured locations while keeping all family details out of the public record. Alternatively, it can keep the pass-card copy behind a family-controlled review rule and publish only the fact that a private file exists. Both policies preserve the missing destination as unknown, retain a correction date and allow the family to withdraw its copy. The choice controls access and disclosure; it cannot determine whether the sibling crossed another route or what happened after the recorded checkpoint.", "noticeboard", (3.5, 0.5), []),
    ("public_margin", "Publish the Method, Keep the Name Blank", "salt_road", "rowan_hale", "inspect", "pike_public_margin",
     "Inspect the public copy and verify that it contains the count method, damaged wall map and no identifying household details.", "ROWAN HALE",
     ["The method and its uncertainty are here. The family name, card image and private request are not.",
      "A public record can show its blank without treating the blank as a person count."],
     "Public Method-Only Copy", "The public copy describes how Rowan recorded the nine empty hook positions, the transfer-docket mismatch and the wall damage. It contains no name, card image, household route or unverified destination. A note explains that the count applies to hooks and bundles, not people. This policy makes the method easier for other road communities to inspect, but prevents readers from following the family's private search through public documents. The record carries a correction date and a contact rule so that new evidence can amend the method without exposing the household.", "sealed_case", (-6.4, -1.1), []),
    ("family_copy", "Reserve the Copy for the Family", "salt_road", "nella_pike", "inspect", "pike_family_review_copy",
     "Inspect the sealed family copy and verify its named access rule, correction slip and withdrawal receipt.", "NELLA PIKE",
     ["The outside has no name. Our request is inside, and the receipt says we can change or withdraw it.",
      "Please file the method without opening this copy. We will ask when we are ready."],
     "Family-Controlled Review Copy", "The private copy holds the pass-card drawing, custody receipt and a request slip authored by Nella's family. Its outer cover contains no household name. The opening rule limits access to a family request and records who handled the copy; the correction slip allows a later statement to be attached without replacing the original. The withdrawal receipt gives the household a way to remove the copy from archive display. This protects privacy at the cost of public access to the card evidence, while leaving the search itself open to the people it concerns.", "sealed_case", (3.8, 0.0), []),
    ("afterword", "The Search Stays Open", "salt_road", "nella_pike", "talk", "nella_pike",
     "Speak with Nella after filing the selected policy and agree how a later witness can add or correct evidence.", "NELLA PIKE",
     ["The card is safe, the method has a date, and the empty place is still empty. That is an honest record for now.",
      "If someone brings a route or a name, let them speak before the archive decides what the blank means."],
     "Afterword: Leave a Place for a Witness", "The completed file preserves the pass card, the unassigned chain tags, the damaged shelter wall and the limits of Silas's view. Nella chose either a public method-only copy or a family-controlled review copy, and the save retains that policy. Neither version names the missing sibling or claims where they went. Ruth's dispatch remains a separate document with its own signed correction. The family search remains open: a future witness can provide a dated account, request a correction or ask for the private copy to be withdrawn without requiring Rowan to rewrite what the current evidence says.", "", None, []),
]
assert len(steps) == 21

quests, dialogues, codex, landmarks = [], [], [], []
previous = "side_ruth_recall_afterword"
for row in steps:
    (key, title, location, giver, kind, target, objective, speaker, lines,
     record_title, body, visual, position, reward_items) = row
    qid = "side_nella_" + key
    dialogue_id = "nella_missing_" + key
    quest = {
        "id": qid, "arcId": "the_salt_road", "stage": -1, "type": "side",
        "locationId": location, "giverId": giver, "title": title, "objective": objective,
        "prerequisiteIds": [previous],
        "objectives": [{"id": "resolve_" + key, "kind": kind, "targetId": target,
                        "requiredCount": 1, "description": objective, "dialogueId": dialogue_id}],
        "reward": {"gold": 7 if kind in ("talk", "choice") else 5, "items": reward_items}
    }
    if key == "return_mark":
        quest["reward"]["items"].append({"itemId": "windglass_reed_seed", "quantity": 1})
    if key == "open":
        quest["reward"]["items"] = [
            {"itemId": "windglass_reed_seed", "quantity": 1},
            {"itemId": "earthworm_bait", "quantity": 3}
        ]
    if key == "policy":
        quest["choiceFlag"] = "pike_archive_policy"
        quest["choiceSpeaker"] = "NELLA PIKE"
        quest["choicePrompt"] = "Who may read the pass-card evidence, and which parts of the method can be published?"
        quest["choices"] = [
            {"id": "method_public", "label": "Publish the count method and damaged-record locations, with no family details.",
             "flagValue": "method_public", "dialogueId": "nella_missing_choice_public",
             "reward": {"gold": 0, "items": [{"itemId": "pike_public_margin_compass", "quantity": 1}]}},
            {"id": "family_review", "label": "Keep the pass-card copy sealed for a family request and publish only the access rule.",
             "flagValue": "family_review", "dialogueId": "nella_missing_choice_family",
             "reward": {"gold": 0, "items": [{"itemId": "pike_family_review_knot", "quantity": 1}]}}
        ]
    if key == "public_margin":
        quest["prerequisiteIds"] = ["side_nella_policy"]
        quest["branchFlag"] = "pike_archive_policy"
        quest["branchValue"] = "method_public"
    if key == "family_copy":
        quest["prerequisiteIds"] = ["side_nella_policy"]
        quest["branchFlag"] = "pike_archive_policy"
        quest["branchValue"] = "family_review"
    if key == "afterword":
        quest.pop("prerequisiteIds")
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": ["side_nella_public_margin", "side_nella_family_copy"]}]
    quests.append(quest)
    dialogues.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex.append({"id": "nella_missing_" + key + "_record", "title": record_title,
                  "category": "The Blank Name", "writtenBy": speaker.title(),
                  "unlockQuestId": qid, "body": body})
    if visual:
        x, y = position
        landmarks.append({"id": "nella_missing_" + key + "_marker", "locationId": location,
                          "displayName": title[:58], "targetId": target, "visualId": visual,
                          "positionX": x, "positionY": y, "scale": 0.085})
    previous = qid

# This sleeve keeps the original pass card accessible and requires a real recipe.
items = [
    {"id": "pike_tag_sleeve", "name": "Removable Tag Sleeve",
     "description": "A narrow dryglass frame lined with Windglass fiber. It protects a pass card from abrasion while keeping the seam open for family review.",
     "category": "quest", "equipmentSlot": "", "maxStack": 1, "attackBonus": 0,
     "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "pike_public_margin_compass", "name": "Public Margin Compass",
     "description": "A small compass paired with a public count method. Its margin records uncertainty instead of assigning a name to an empty place.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 2,
     "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "pike_family_review_knot", "name": "Family Review Knot",
     "description": "A cord token for a sealed pass-card copy, tied with a dated correction and withdrawal rule held by Nella's family.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 0,
     "guardBonus": 2, "healAmount": 0, "sellValue": 0}
]
recipe = {
    "id": "craft_pike_tag_sleeve", "displayName": "Chế bao thẻ tháo được",
    "stationId": "cinderwell_assay_bench", "discipline": "alchemy",
    "outputItemId": "pike_tag_sleeve", "outputQuantity": 1,
    "ingredients": [
        {"itemId": "windglass_reed", "quantity": 1},
        {"itemId": "saltspool_skate", "quantity": 1},
        {"itemId": "dryglass_shard", "quantity": 1}
    ]
}
extra_dialogue = [
    {"id": "nella_missing_choice_public", "speakerName": "ROWAN HALE", "lines": [
        "We can publish the method and the map of damaged records without publishing the family's copy.",
        "The blank stays visible as a limit in our evidence, not as a name or a number." ]},
    {"id": "nella_missing_choice_family", "speakerName": "NELLA PIKE", "lines": [
        "Keep the card drawing sealed until my family asks for it. Publish only the rule that lets us review it.",
        "A private copy is not lost. It remains available to the people whose search it records." ]}
]

for filename, additions in [
    ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues + extra_dialogue),
    ("codex_catalog.json", codex), ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items), ("recipe_catalog.json", [recipe])
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} Nella Pike quests, {len(dialogues) + len(extra_dialogue)} dialogue scenes, "
      f"{len(codex)} records, {len(landmarks)} landmarks, {len(items)} items and one recipe.")
