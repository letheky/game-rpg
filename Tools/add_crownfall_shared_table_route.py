#!/usr/bin/env python3
"""Install Ada Sloane's pre-ending ration trial into the content catalogs."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, value):
    (CONTENT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, kind, target, objective, giver, speaker, two dialogue lines,
# codex title, codex body, visual, position
steps = [
    ("open", "The Table Beside the Forecast", "talk", "ada_sloane",
     "Ask Ada why her last ration forecast still has a blank column for who was served.",
     "ada_sloane", "ADA SLOANE",
     ["The forecast predicts what the storehouse can release. It does not say who stood in the queue when the door opened.",
      "Alden calls the blank column a nuisance. I think it is where the people disappear from his arithmetic. Help me measure one actual shift."],
     "A Forecast Meets Its First Supper",
     "Ada pins the release forecast beside a list of meals expected at the Crownfall table. The two sheets use the same grain store but different units: one counts sacks issued, the other records bowls offered. At first the totals appear to match. Then Ada points to a blank column where the clerk was meant to note how many people were turned away, asked to return later, or chose not to give a household name. The page records none of these events. Captain Alden says a clean ledger is easier to defend than a complicated one. Ada answers that a clean total can still leave a person hungry. She asks Rowan to follow one serving shift, from the sealed store to the table, without turning a small sample into a promise about the whole settlement.", "", None),
    ("bowls", "Two Bowls, Three Marks", "inspect", "crownfall_table_bowls",
     "Inspect the two serving bowls and the marks scratched beneath their handles.",
     "rowan_hale", "ROWAN HALE",
     ["One bowl has a shallow rim and one has a chipped base. The marks are not measurements unless someone tells us what they mean.",
      "I will record their shape and ask the kitchen who uses them. I will not treat a scratch as a person's name."],
     "The Bowls at the Crownfall Table",
     "The table keeps two bowls for measuring a portion. One is wider and shallow; the other is narrower, with a chip under its base. Three scratched marks may indicate a serving size, a repair count, or a child's attempt to keep a place. The kitchen has no key that explains them. Rowan measures the bowls with the same grain scoop used for the store release and photographs the scratches before anyone cleans them. The two vessels are tools in a service routine, not proof of who was fed. Ada asks to list capacity and condition separately from attendance, so a future worker can repeat the comparison without inventing a roster from the marks.",
     "document", (-9.7, 4.5)),
    ("portion", "The Scoop That Sets the Portion", "inspect", "crownfall_portion_scoop",
     "Inspect the storehouse scoop and compare its rim with the two serving bowls.",
     "rowan_hale", "ROWAN HALE",
     ["The scoop is measured in volume, but the ration board describes its issue as a weight. Grain settles differently after it is shaken.",
      "I can test the same grain in both bowls. The result will describe this scoop and this batch, not every store in Asterra."],
     "A Scoop Is Not a Weight",
     "The storehouse scoop has a bent rim and an old notch cut into its handle. Ada's forecast counts each level scoop as a fixed quantity, while the release board calls it a weight. Rowan fills the scoop with the grain currently held for the evening meal, then fills each bowl without packing it down. The amounts differ because the bowls have different shapes and the grain shifts as it settles. A second fill gives a slightly different result. The record therefore names the tool, batch, fill method and date. It does not convert this one comparison into a universal serving size. A later cook may choose a different portion; the ledger should say so rather than silently rewriting the forecast.",
     "sealed_case", (-6.5, 4.45)),
    ("alden", "Alden's Rule for the Store Door", "talk", "captain_alden_final",
     "Ask Captain Alden why he requires the same storehouse issue before every serving shift.",
     "captain_alden_final", "CAPTAIN ALDEN VALE",
     ["I set one issue per shift because the last keeper was accused of giving the second key to friends. A fixed amount kept the doors open.",
      "If you change the rule, show me how the next keeper can catch a mistake before it becomes a rumor that the store was stolen."],
     "Why Alden Keeps One Measure",
     "Alden does not defend the forecast as perfect. He remembers two storekeepers arguing over how much had been released after a flood. Their accounts used different scoops and neither had signed the other's page. The accusation spread before the missing grain was found in a dry loft. Alden's fixed issue reduced one kind of dispute: every shift began with the same number of scoops and ended with a lock check. It also made the routine slow to adapt when the queue changed. A family arriving late could be sent away even if grain remained, because the next issue was already assigned to another shift. Alden asks for a replacement rule that can be inspected by the person who inherits it. He fears both waste and favoritism, and he does not accept that good intentions alone protect a shared store.", "", None),
    ("rota", "The Shift Rota Has No Empty Place", "inspect", "crownfall_shift_rota",
     "Inspect the rota and locate the line where a worker could record a delayed or refused serving.",
     "rowan_hale", "ROWAN HALE",
     ["The rota counts open shifts and sealed keys. It has no place for a second queue or a serving carried out of the room.",
      "Alden's lock check is still useful. We can add a return column without asking every person to sign for food."],
     "A Shift Rota with One Queue",
     "The rota records who unlocked the store, how many scoops left it and which keeper returned the key. It does not record the time people arrived at the table or whether a serving went to someone outside the hall. Alden says adding names would make the document harder to protect; Ada agrees that a meal should not depend on surrendering a name. Rowan draws two alternative columns: one for a missed or delayed serving, and one for grain returned unused. Neither column identifies a household. The original lock check remains intact. The proposed rota is meant to show where an issue went, not to make the people receiving it easier to monitor.",
     "noticeboard", (-2.7, 4.45)),
    ("emberroot", "A Harvest Reserved for Another Planting", "grow", "emberroot",
     "Grow one Emberroot at the Crownfall garden and set aside seed before counting the harvest as food.",
     "ada_sloane", "ADA SLOANE",
     ["The old model counts every root as a meal. This bed needs seed for the next cycle, and the first harvest cannot serve both columns.",
      "Mark what we plant, what we keep and what we actually carry to the table. Let the time between those marks stay visible."],
     "A Root, a Seed, and an Available Meal",
     "Ada asks Rowan to plant Emberroot in the Crownfall bed and write down the seed source before watering. When the crop is ready, they separate a small portion for another planting before weighing the roots offered to the kitchen. The forecast spreadsheet treated all gathered weight as immediately available food. It contained no replacement-seed column and no growing interval, so a repeating harvest looked larger on paper than it was in the bed. The current crop corrects one assumption but cannot estimate the entire region's yield. Some roots are damaged, some are saved, and a later season may fail. Ada puts all three categories beside the date rather than collapsing them into one total. Alden agrees that a reserve exists only if the ledger shows what was actually kept aside.", "", None),
    ("bed", "The Bed Needs Water Tomorrow Too", "inspect", "crownfall_emberroot_bed",
     "Inspect the Emberroot bed after harvest and mark which soil stayed damp enough for another planting.",
     "rowan_hale", "ROWAN HALE",
     ["The west edge held water; the east edge dried before the leaves opened. One harvest hides that difference if I write only the total.",
      "I will leave a note for the next grower. They can decide whether the same bed is worth planting again."],
     "One Bed Cannot Stand for the Reach",
     "The Crownfall bed is small and close to the stone wall. Its western half stayed damp after the morning watering, while the eastern edge dried sooner. Rowan marks both edges and records the Emberroot harvest separately by row. That split helps a future gardener decide whether to repeat the test, but it does not tell Ada how much food the reach could produce. The bed's shelter, soil depth, water source and tending time are all local conditions. The old forecast used the word 'average' without naming any of them. Ada removes the word from the trial sheet and replaces it with the actual observations. The result is less convenient for a speech, but more useful to a person who will plant here next week.",
     "seed_cradle", (1.0, 4.45)),
    ("minnow", "A Minnow beneath the Lanterns", "fish", "starlit_minnow",
     "Catch one Starlit Minnow at Starlit Lake and record the bait and water level with the catch.",
     "rowan_hale", "ROWAN HALE",
     ["The model places fish in the food column as if a net brings back the same number every night.",
      "I caught one fish at this place and time. The next cast may miss, and a person who cannot fish still needs a meal."],
     "A Catch Is Not a Nightly Supply",
     "Rowan catches a Starlit Minnow at the lake and writes down the bait, water level and time. The fish goes to the kitchen as a single meal ingredient. The forecast's food column had converted fish from the lake into a dependable nightly supply, though the catch record contained no count of failed casts or days the shore was inaccessible. One successful catch shows that the species was available at this place and time. It does not establish a population, a daily catch rate or an equitable way to distribute food. Ada asks that the meal trial keep the catch attached to its conditions. If the model later uses a fishing estimate, its author will have to explain how many attempts went uncounted.",
     "", None),
    ("waterline", "The Water Mark beneath the Landing", "inspect", "crownfall_lake_waterline",
     "Inspect the Starlit Lake water mark and compare it with the landing used by the serving boat.",
     "rowan_hale", "ROWAN HALE",
     ["The old chalk mark sits above today's water. That tells us the level changed; it does not tell us when or why.",
      "The landing cannot carry a basket at every level. Add access to the forecast beside yield."],
     "The Lake Is Not an Open Pantry",
     "A pale line on the landing stone sits above the current water. It may mark a seasonal height, a storm or an earlier measuring point; there is no date beside it. The route from the boat to the Crownfall table is passable today, but the last stretch becomes slippery when the lake falls below the carved step. Ada's projection counted a fish at the lake as available food without including the time it takes to bring a catch to the people waiting. Rowan records the path condition with the catch rather than subtracting a guessed amount from the total. Access can change independently of supply. The note invites a later trial at another water level and does not claim that the old mark belongs to the same season as the forecast.",
     "document", (3.3, 4.45)),
    ("cook", "Cook One Trial Portion", "craft", "crownfall_starlit_pottage",
     "Cook one Emberroot and one Starlit Minnow into a single trial portion at the Crownfall field stove.",
     "ada_sloane", "ADA SLOANE",
     ["The forecast calls both ingredients available, but that is not yet a meal. Cook one portion and write down what it cost.",
      "This recipe tests one shift at one table. Keep the harvest, the seed reserve and the prepared food in separate columns."],
     "Emberroot and Minnow: One Trial Portion",
     "Ada asks Rowan to bring one harvested Emberroot and the Starlit Minnow caught for the trial to the field stove. The cookpot yields one portion of pottage. They record the two ingredients, the time spent preparing them and the fact that the seed reserve remains untouched. Neither ingredient is treated as an unlimited supply: the root came from one small bed, and the fish from one baited cast. The prepared portion can test whether the open table serves food without a household roll. It cannot establish how often either ingredient can be gathered or whether the meal meets every need. Ada asks that the recipe remain attached to the trial record so the next watch can repeat the same preparation or explain why it changed.",
     "", None),
    ("warden", "The Warden Names His Portion", "talk", "first_warden_final",
     "Ask The First Warden how the first oath treated people whose needs changed between scheduled issues.",
     "first_warden_final", "THE FIRST WARDEN",
     ["The first oath named a reserve, but I remember no rule for a person who could not reach the line on its appointed day.",
      "My memory covers one measure and one winter. Do not turn it into a law for every hundredth year."],
     "A Memory with a Small Boundary",
     "The First Warden remembers a storekeeper dividing grain into fixed portions at the beginning of a winter. He does not remember whether people could return for more or whether the rule changed when a road closed. His memory was carried through many retellings; he cannot separate every sentence he heard from words added later. The story shows that a reserve was part of the oath's practice, not that every cycle used the same serving rule. Ada keeps it beside the current trial as a question about continuity. Alden listens carefully: he had treated the remembered measure as authority for his own rule. The Warden says he can testify to the measure he saw, but not to every person it served. His limit does not make the memory useless. It keeps it from deciding the meal before anyone at the table speaks.",
     "", None),
    ("reserve", "A Shelf for What Must Be Replanted", "inspect", "crownfall_seed_shelf",
     "Inspect the seed shelf and compare its reserve with the Emberroot saved from the trial bed.",
     "rowan_hale", "ROWAN HALE",
     ["The reserve shelf holds two sealed jars, but neither label says when the next planting is due.",
      "I will add a date and a keeper's mark. A reserve that no one can open in time is only a number behind a lock."],
     "The Reserve Needs a Return Date",
     "Two seed jars remain on the shelf. Their seals are unbroken, yet both labels describe the jars as 'for later' without saying which planting they are meant to support. A reserve protects a future meal only if a keeper knows when to release it. Rowan adds a planting window and leaves a second field for the next keeper's mark. He does not assign a permanent guardian; the rotation changes with the watch. Alden admits that his lock schedule was designed to prevent unrecorded withdrawals, not to preserve germination quality. Ada asks for both conditions on the card. Storage and access belong in the model alongside food yield, because one cannot replace the other.",
     "sealed_case", (6.5, 4.45)),
    ("choice", "Choose the Rule for Tomorrow's Table", "choice", "crownfall_meal_policy",
     "Choose whether the provisional rule is posted for correction or tried at an open table without a household roster.",
     "ada_sloane", "ADA SLOANE",
     ["A public rota lets people correct the count, but a posted list can make a late arrival feel watched. An open table avoids that list, but the storekeeper still needs a clear limit.",
      "Choose the risk we can review tomorrow. This trial is one evening, not a decree for the Reach."],
     "Two Ways to Keep the Table Accountable",
     "The trial has shown two risks that cannot be removed by making the page neater. A posted rota makes a serving rule visible and correctable, but names can turn a meal into surveillance. An open table protects privacy, yet a storekeeper still needs to know when the reserved grain must remain untouched. Ada offers two temporary procedures. Rowan may post the portion rule with blank spaces for people who choose not to be counted, then invite corrections before the next shift. Or the team may serve one open meal, record only the amount used and leave household totals out of the book. Alden prefers the first because it gives the watch a handoff. Ada prefers the second because it asks less of the people in the queue. Neither option changes the final allocation or settles the cycle. The choice belongs to this trial and must be reviewed after it is used.",
     "noticeboard", (-9.7, -4.35)),
    ("public_board", "Post the Portion Rule, Leave Names Blank", "inspect", "crownfall_public_meal_board",
     "Inspect the provisional board and verify that the portion method is visible while household names remain optional.",
     "rowan_hale", "ROWAN HALE",
     ["The rule is in large letters; the correction date is beside it. A blank line stays blank unless someone asks to add a name.",
      "The board says one shift only. The next keeper can change it after hearing from the people who use it."],
     "A Posted Rule with a Review Date",
     "The public board gives the trial portion, the amount held for replanting and the time when the next shift may review the rule. Household names are not required. People can add a correction anonymously or ask Ada to read it aloud at the next meeting. Alden checks that the reserve shelf and store key still have separate entries; posting the serving rule does not open the seed jars. A red line marks the page as a one-shift trial, not a standing order. The board gives people a way to challenge the method, though Ada knows some may still avoid a public place. She leaves a covered box beneath it for written comments. The record says what the procedure offers and where its blind spots remain.",
     "noticeboard", (9.6, 4.35)),
    ("public_forum", "Alden Answers the First Correction", "talk", "captain_alden_final",
     "Ask Alden to hear a correction that the late shift arrived after the posted serving window.",
     "captain_alden_final", "CAPTAIN ALDEN VALE",
     ["The rota says the line opened at dusk. It does not say the road gate was closed while the cart crossed the bridge.",
      "I will widen the window for one trial. Mark what delayed the people; do not mark them as late."],
     "The Queue Arrived after the Page",
     "A correction arrives from the late shift: several people reached the table after dusk because the road gate had been held for a cart crossing. The board had treated dusk as a reliable start time and described anyone arriving later as a late arrival. Alden first wants to keep the old label; he worries that changing the window will make tomorrow's lock check harder. He reads the road log and sees the delay was recorded by the watch, not by the people waiting. Rowan changes the rota wording to 'serving window' and adds the reason for the first delay. No names are added. Alden agrees that a rule can be firm without accusing the person it failed to reach. The correction stays attached to the old version so the next keeper can see why the time changed.",
     "witness", (-7.4, 0.8)),
    ("public_receipt", "Attach the Correction to the Old Rota", "inspect", "crownfall_public_correction",
     "Inspect the corrected rota and verify that its first time window remains visible beside the revision.",
     "ada_sloane", "ADA SLOANE",
     ["We have not erased the old time. We have marked who changed it, what evidence they used and when to review it again.",
      "If the road delay repeats, the next shift can challenge the rule without accusing the people who arrived."],
     "Correction History beside the Serving Rule",
     "The corrected rota keeps the first serving window, the road delay and the new review time on one page. Ada signs the change as editor; Alden initials the store transfer, not the count of people served. This separation lets a future keeper distinguish a policy edit from a food tally. The trial remains temporary until the next shift reviews it. A person who disagrees may submit another correction without signing for a meal. The board does not show whether everyone felt safe using it, and Ada records that as a question for the review rather than claiming that the new procedure solved it. She asks Rowan to leave the earlier version legible, since a correction without its history could look like an unexplained change to the store's rule.",
     "sealed_case", (9.7, 2.4)),
    ("public_posting", "The Next Keeper Receives the Rule", "talk", "captain_alden_final",
     "Hand Alden the revised rota and ask him to read the review date before accepting the watch key.",
     "captain_alden_final", "CAPTAIN ALDEN VALE",
     ["The board tells me what to do and when to question it. I can hand over the key without pretending the first rule was perfect.",
      "Keep the correction box where the queue can reach it. I will not ask the next keeper for a list of names."],
     "A Rule Passed Forward with a Question",
     "Alden takes the revised rota and reads the review date aloud before accepting the watch key. He repeats the portion method, the seed reserve and the wider serving window in his own words. If he had missed one, Ada would have corrected the page before the next shift began. The handoff does not prove the rule will work for every person. It gives the next keeper a procedure that can be checked and a time when it must be reconsidered. Alden leaves the correction box at the edge of the table rather than beside the locked store. A person can question the schedule without approaching the key. Rowan notes that the board will remain through one evening and that a longer policy requires another decision.",
     "", None),
    ("quiet_room", "Set One Meal without a Roll Call", "inspect", "crownfall_open_table_notice",
     "Inspect the open-table notice and confirm that it lists the serving time without asking for names or household totals.",
     "rowan_hale", "ROWAN HALE",
     ["The notice names the hour and the serving limit. There is no line to write down who came through the door.",
      "Alden still needs to check the store after the meal. We can count what left the shelf without counting the people who took it."],
     "An Open Table with a Store Limit",
     "The open-table notice gives a time, a serving limit and a request that people take only what they can use before the close. It does not ask for names, household size or a reason for arriving. Alden worries that someone may take an extra portion. Ada says the store transfer can still be checked by weighing the returned grain and comparing it with what was issued. Neither method will show exactly who ate. The notice makes privacy part of the trial while keeping the reserve separate. Rowan places it where people can read it before joining the queue, then confirms the storekeeper can close the table at the posted time without taking a name list.",
     "document", (-6.7, -4.35)),
    ("quiet_service", "Serve What the Table Can Safely Release", "interact", "crownfall_open_meal_table",
     "Serve the cooked Emberroot and Minnow portion at the open table and keep the seed reserve sealed.",
     "rowan_hale", "ROWAN HALE",
     ["The Emberroot and Starlit Minnow became one portion at the field stove. We can open the table now; the reserve stays sealed.",
      "The bowl is offered without a sign-in. Anyone who needs to leave before eating can take a wrapped portion."],
     "One Open Meal, No Household Count",
     "Rowan lays out the cooked pottage and a small number of bowls. The seed reserve remains sealed, and the table closes at the time printed on the notice. People can eat in the room or take a wrapped portion for someone who could not come. No clerk asks them to name that person. At closing, Ada and Alden count the food left and compare it with the store transfer. They know how much was offered and how much returned; they do not know how many people ate or whether the serving met every need. Ada resists writing an attendance estimate from the empty bowls. The meal is a test of a privacy-preserving procedure, not a survey of hunger across Crownfall Reach.",
     "sealed_case", (-3.5, -4.35)),
    ("quiet_return", "Return the Grain That Stayed on the Tray", "inspect", "crownfall_returned_grain_tray",
     "Inspect the returned grain and compare its weight with the amount issued for the open meal.",
     "rowan_hale", "ROWAN HALE",
     ["Some grain came back dry and untouched. The count tells us what returned, not why anyone left it.",
      "We can return it to storage after the kitchen checks it. Do not subtract a person from the meal because a scoop remains."],
     "A Return Count Is Not a Refusal Count",
     "The tray holds grain that stayed dry through the serving. Rowan weighs it before the kitchen decides whether it can be stored again. The difference between the amount issued and the amount returned describes what left the tray; it cannot say whether a person refused food, took a wrapped portion or never arrived. Ada writes the returned quantity beside the transfer and refuses to call the difference 'consumed.' The open table kept names out of the ledger, as intended, but it also leaves some questions unanswered. The next trial could ask people for voluntary comments, yet the comment must never become a condition for receiving a meal. Alden accepts the narrower count because it is still enough to close the store safely.",
     "sealed_case", (0.0, -4.35)),
    ("quiet_review", "Alden Counts the Store, Not the Queue", "talk", "captain_alden_final",
     "Review the store transfer with Alden and agree that the remaining grain is evidence about the stock, not attendance.",
     "captain_alden_final", "CAPTAIN ALDEN VALE",
     ["I can account for what left the store and what came back. I cannot account for every person who may have eaten elsewhere.",
      "That is still enough for my key check. If I want a count of people, I will have to ask for one with consent instead of pretending the grain gives it to me."],
     "A Store Check without a People Count",
     "Alden checks the lock, the issued grain and the returned portion. The store balances within the scale's margin. He says that this closes the key check, not the question of how many meals Crownfall needs. In the old rota he would have written a household total beside the transfer and treated the difference as an attendance estimate. The open-table trial gives him no such number. He is uncomfortable with that gap but no longer claims that the grain can fill it. Ada suggests a voluntary conversation at a later meal. Alden agrees only if the serving does not depend on a response. He will keep the store method and retire the assumption that a balanced shelf proves a complete ration.",
     "", None),
    ("shared_record", "Keep the Harvest beside the Serving", "inspect", "crownfall_meal_record",
     "Inspect the shared meal record and confirm it separates food grown, food reserved and food actually served.",
     "rowan_hale", "ROWAN HALE",
     ["The page now has three columns: harvested, held for seed and offered at the table.",
      "It does not estimate need. That question belongs to the people who choose to tell us, not to a crop total."],
     "Three Food Columns, No Demand Guess",
     "The final meal record has three columns: what was harvested, what was kept for the next planting and what was offered at the table. A fourth field names the tools and conditions used to measure each amount. There is no column for 'total need' because no one in the trial measured it. Ada keeps that question open for a later conversation with the people who use the table. The record can support a store check and help a gardener repeat the crop trial. It cannot decide how much food every household requires or whether one serving rule is fair in every season. Alden asks that the sheet stay with the store key. Ada asks that a copy stay by the table. Rowan makes both copies and marks them with the same review date.",
     "document", (0.0, -2.45)),
    ("warden_review", "The Warden Refuses to Call It a Law", "talk", "first_warden_final",
     "Ask The First Warden whether one successful serving trial can settle the ration rule of the old oath.",
     "first_warden_final", "THE FIRST WARDEN",
     ["I remember a store door and a measured cup. I cannot tell you that every person received what they needed.",
      "A practice repeated for a century is not made just by surviving a century. Keep the question with those who will live under the next rule."],
     "The Measure Did Not End the Argument",
     "The First Warden studies the two copies and recognizes the notch on the store scoop. He remembers a keeper tapping the handle against the stone before every issue. He cannot remember whether that gesture was a measurement check or simply a habit. He will not call the current trial the original rule, nor will he use its successful lock check to settle the ethics of the ration. The meal answered a smaller question: the store can record a transfer without requiring every person to give a name. The Warden says a law kept for a hundred years may still deserve review by the people asked to live under it. Ada writes that sentence in the margin, not as a verdict against Alden but as a warning against confusing endurance with consent.",
     "", None),
    ("alden_review", "Alden Signs the Review Date", "talk", "captain_alden_final",
     "Ask Alden to sign a date when the next watch will review the meal rule with Ada.",
     "captain_alden_final", "CAPTAIN ALDEN VALE",
     ["I used one rule because I thought any exception would bring back the old accusation. The trial held without asking for a roll of names.",
      "I will sign the review date. If the next shift finds a gap, I want them to tell me before the rumor does."],
     "Alden Accepts a Date for Review",
     "Alden signs a review date rather than a permanent order. He explains that the fixed scoop was his answer to an earlier theft accusation, and that he feared any change would look like favor. The trial did not prove that favoritism has disappeared. It did show that a store transfer can be checked while leaving the meal queue uncounted. Alden is willing to test the procedure again with the next watch. He asks to hear about an empty place, a delay or a damaged measure before someone turns it into a rumor. Ada records that request alongside the date but does not call it a guarantee. A promise can guide the next shift; only the shift can show whether the promise was kept.",
     "", None),
    ("afterword", "Leave Tomorrow's Table Open to Change", "talk", "ada_sloane",
     "Speak with Ada after the trial and confirm that neither the forecast nor the meal record decides who deserves a serving.",
     "ada_sloane", "ADA SLOANE",
     ["The forecast is still useful when it says what it assumes. The table record is useful when it says what happened here and stops there.",
      "Tomorrow's keeper has a method, a reserve and a date to ask again. That is not a final answer, but it is a choice the people at the table can challenge."],
     "The Table beside the Forecast",
     "Ada files the forecast and meal record together without merging their numbers. The forecast estimates what the store may hold under stated conditions. The meal record describes one shift, one crop, one catch and one serving procedure. Alden will carry the store key into the next watch; Ada will return after the posted review date. Neither result decides which ending Rowan should choose or whether the world has enough resources to remain unchanged forever. The trial gives the people at Crownfall a small, revisable rule for tomorrow and leaves them free to change it when the conditions change. Rowan looks at the blank column that began the route. It is no longer mislabeled as zero. It says what the team did not count, and leaves the decision to count it later with the people who would be counted.",
     "", None),
]

quest_entries, dialogue_entries, codex_entries, landmark_entries = [], [], [], []
choice_id = "crownfall_shared_table_policy"
previous = None
public_branch = {"public_board", "public_forum", "public_receipt", "public_posting"}
quiet_branch = {"quiet_room", "quiet_service", "quiet_return", "quiet_review"}

for key, title, kind, target, objective, giver, speaker, lines, codex_title, body, visual, position in steps:
    quest_id = "side_crownfall_shared_table_" + key
    dialogue_id = "crownfall_shared_table_" + key
    objective_id = dialogue_id + "_objective"
    quest = {
        "id": quest_id,
        "arcId": "two_last_oaths",
        "stage": -1,
        "type": "side",
        "locationId": "last_oath_reach",
        "giverId": giver,
        "title": title,
        "objective": objective,
        "objectives": [{
            "id": objective_id,
            "kind": kind,
            "targetId": target,
            "requiredCount": 1,
            "description": objective,
            "dialogueId": dialogue_id,
        }],
        "reward": {"gold": 6, "items": []},
    }
    if key == "open":
        quest["reward"]["items"] = [
            {"itemId": "emberroot_seed", "quantity": 1},
            {"itemId": "earthworm_bait", "quantity": 6},
        ]
    if previous is not None:
        quest["prerequisiteIds"] = ["side_crownfall_shared_table_" + previous]
    if key in {"public_board", "quiet_room"}:
        quest["prerequisiteIds"] = ["side_crownfall_shared_table_choice"]
    if key == "choice":
        quest.update({
            "choiceFlag": choice_id,
            "choiceSpeaker": "ADA SLOANE",
            "choicePrompt": "Choose a temporary ration procedure for one shift. Both choices keep the seed reserve sealed and set a review date.",
            "choices": [
                {
                    "id": "posted_rule",
                    "label": "Post the portion method with optional names, a correction box and a date to review it.",
                    "flagValue": "posted_rule",
                    "dialogueId": "crownfall_shared_table_choice_posted",
                    "reward": {"gold": 0, "items": []},
                },
                {
                    "id": "open_table",
                    "label": "Serve one open meal without a household roll and record only the store transfer.",
                    "flagValue": "open_table",
                    "dialogueId": "crownfall_shared_table_choice_open",
                    "reward": {"gold": 0, "items": []},
                },
            ],
        })
    elif key in public_branch:
        quest.update({"branchFlag": choice_id, "branchValue": "posted_rule"})
    elif key in quiet_branch:
        quest.update({"branchFlag": choice_id, "branchValue": "open_table"})
    elif key == "shared_record":
        quest.pop("prerequisiteIds", None)
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": [
            "side_crownfall_shared_table_public_posting",
            "side_crownfall_shared_table_quiet_review",
        ]}]
    if key == "public_posting":
        quest["reward"]["items"] = [{"itemId": "open_hand_store_charm", "quantity": 1}]
    if key == "quiet_review":
        quest["reward"]["items"] = [{"itemId": "quiet_table_charm", "quantity": 1}]

    quest_entries.append(quest)
    dialogue_entries.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex_entries.append({
        "id": "crownfall_shared_table_" + key + "_record",
        "title": codex_title,
        "category": "The Table beside the Forecast",
        "writtenBy": "Ada Sloane",
        "unlockQuestId": quest_id,
        "body": body,
    })
    if visual and position:
        x, y = position
        landmark_entries.append({
            "id": "crownfall_shared_table_marker_" + key,
            "locationId": "last_oath_reach",
            "displayName": title,
            "targetId": target,
            "visualId": visual,
            "positionX": x,
            "positionY": y,
            "scale": 0.085,
        })
    previous = key

dialogue_entries.extend([
    {"id": "crownfall_shared_table_choice_posted", "speakerName": "ADA SLOANE", "lines": [
        "Post the rule, then. I will put the correction box at the table rather than beside the store key.",
        "If people choose not to add their names, the line stays blank. We will still review the portion and the reserve tomorrow."
    ]},
    {"id": "crownfall_shared_table_choice_open", "speakerName": "ADA SLOANE", "lines": [
        "One open meal, with no household roll. The store transfer gives Alden enough to close the key check.",
        "If anyone wants to tell us how the service went, we will listen. The meal will not depend on an answer."
    ]},
])

for filename, additions in [
    ("prologue_quests.json", quest_entries),
    ("dialogue_catalog.json", dialogue_entries),
    ("codex_catalog.json", codex_entries),
    ("quest_landmarks.json", landmark_entries),
]:
    catalog = read(filename)
    if filename == "quest_landmarks.json":
        catalog["entries"] = [entry for entry in catalog["entries"]
                              if entry.get("id") != "crownfall_shared_table_marker_public_posting"]
    upsert(catalog["entries"], additions)
    write(filename, catalog)

items = read("item_catalog.json")
upsert(items["entries"], [
    {
        "id": "open_hand_store_charm",
        "name": "Open-Hand Store Charm",
        "description": "A small iron measure with a review date stamped beside the handle. Increases defense by 3.",
        "category": "equipment",
        "equipmentSlot": "charm",
        "maxStack": 1,
        "attackBonus": 0,
        "guardBonus": 3,
        "healAmount": 0,
        "sellValue": 42,
    },
    {
        "id": "quiet_table_charm",
        "name": "Quiet Table Charm",
        "description": "A folded brass token that protects a private meal without asking who received it. Increases attack by 3.",
        "category": "equipment",
        "equipmentSlot": "charm",
        "maxStack": 1,
        "attackBonus": 3,
        "guardBonus": 0,
        "healAmount": 0,
        "sellValue": 42,
    },
    {
        "id": "crownfall_starlit_pottage",
        "name": "Crownfall Emberroot Pottage",
        "description": "One field-kitchen portion cooked from Emberroot and Starlit Minnow for Ada Sloane's ration trial. Restores 20 health when used.",
        "category": "consumable",
        "equipmentSlot": "",
        "maxStack": 10,
        "attackBonus": 0,
        "guardBonus": 0,
        "healAmount": 20,
        "sellValue": 0,
    },
])
write("item_catalog.json", items)

recipes = read("recipe_catalog.json")
upsert(recipes["entries"], [
    {
        "id": "cook_crownfall_starlit_pottage",
        "displayName": "Cook Crownfall Emberroot Pottage",
        "stationId": "last_oath_kitchen",
        "discipline": "cooking",
        "outputItemId": "crownfall_starlit_pottage",
        "outputQuantity": 1,
        "ingredients": [
            {"itemId": "emberroot", "quantity": 1},
            {"itemId": "starlit_minnow", "quantity": 1},
        ],
    },
])
write("recipe_catalog.json", recipes)

print(f"Installed {len(quest_entries)} quests, {len(dialogue_entries)} dialogue entries, "
      f"{len(codex_entries)} codex records, {len(landmark_entries)} markers, 2 branch charms and a cooking recipe.")
