#!/usr/bin/env python3
"""Install the Outer-Wake carrying-capacity evidence line into the authored catalogs."""
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

# id, title, location, giver, kind, target, objective, speaker, dialogue lines,
# codex title, codex body, landmark visual (empty for non-landmark objectives), reward items
steps = [
("open", "The Measure of a Living World", "outerwake_archive", "evelyn_hart", "talk", "evelyn_hart",
 "Dr. Evelyn Hart wants Rowan to review the resource model before its projected limits are carried into the final hearing.",
 "DR. EVELYN HART", ["The Archive report shows the signal can be measured. It does not tell us who gets to choose what the measurement means.", "I want you to trace one resource model from its assumptions to the people living beneath it. Bring back the gaps as carefully as the totals."],
 "A Question Before the Figure", "The Outer-Wake model predicts how long stored resources might last under several patterns of use. Its first sheet treats each person as a constant demand, though the margin notes describe seasonal care, illness, travel and voluntary sharing. None of those notes has a scale on the main chart. The model can help compare scenarios, but its neat curve is not a verdict about how many lives the world can sustain. Rowan records the question that must stay beside every projection: who selected the assumptions, and who can challenge them?", "", [{"itemId":"skyroot_seed","quantity":1},{"itemId":"earthworm_bait","quantity":4}]),
("projection", "Three Curves, One Missing Column", "outerwake_archive", "evelyn_hart", "inspect", "capacity_projection_board",
 "Read the three resource curves and find the blank column where local choices should have been recorded.",
 "ROWAN HALE", ["The three curves begin with different rainfall and harvest assumptions, but they all use the same demand column.", "The blank heading is not zero demand. It is a question the people who made the chart never asked."],
 "Projection Board: Assumptions", "The board overlays three estimates: a wet cycle, a dry cycle and a cycle with one failed harvest. The lines diverge, then converge because the same fixed demand value is reused in every case. A handwritten margin proposes recording care work and stored seed, but no one added either to the calculation. The chart does not prove that the world has abundant resources; it shows that this particular projection cannot compare all the ways people share them. The blank column must remain visible until a method for recording it is agreed upon.", "document", []),
("gauge", "Jace's Wind Gauge", "outerwake_archive", "jace_morrow", "talk", "jace_morrow",
 "Ask Jace which readings his passive receiver actually captured while the model was being assembled.",
 "JACE MORROW", ["The receiver logged pressure changes and the time they arrived. It did not identify a sender or measure what anyone intended.", "One clock drifted after the storm. I kept both readings so a later reviewer can see the uncertainty instead of inheriting my correction."],
 "Receiver Log and Clock Drift", "Jace's passive receiver captured three pressure pulses on separate nights. The device stores arrival time and signal strength, not the identity of a sender. Its clock ran slow after a storm, so Jace preserved the uncorrected entries beside a second estimate. The resource projection imported only the corrected times and omitted the drift note. That omission may alter a plotted interval, but it cannot establish why the pulses occurred. The raw values remain available for review, while the identity of the source stays unresolved.", "", []),
("skyroot", "A Sample from the Stone Bed", "outerwake_archive", "evelyn_hart", "grow", "skyroot",
 "Grow Skyroot in the Outer-Wake plot so the model can distinguish a living reserve from a counted harvest.",
 "DR. EVELYN HART", ["The old estimate counted every seed as food before the plant had taken root. This sample lets us record the time between planting and usable sap.", "One plot cannot predict a valley. It can show whether the model keeps seed, growing time and harvest in separate columns."],
 "Skyroot: Reserve or Yield", "The Skyroot sample began as one seed and produced sap only after a full growing interval. A portion of the harvest must remain available for the next planting if the plot is to continue. The projection spreadsheet counted the entire first yield as immediate supply and did not subtract replacement seed. This trial does not estimate the productivity of all Outer-Wake land; it identifies a bookkeeping choice that can make a repeating harvest appear larger than it is. Future runs should record planting stock, time, losses and gathered sap separately.", "", []),
("farwake", "A Fish with a Place and a Date", "outerwake_archive", "jace_morrow", "fish", "farwake_carp",
 "Catch a Farwake Carp at the Celestial Pool and record the catch location and date without turning one catch into a stock estimate.",
 "ROWAN HALE", ["The ledger says one Farwake Carp came from the Celestial Pool today. That is a catch record, not a count of every fish in the lake.", "I will keep the date and spot attached to the sample. We do not know how many fish were missed or how often this result repeats."],
 "Celestial Pool Catch Record", "The Celestial Pool register contains one Farwake Carp catch recorded during the model review. The entry includes the pool, bait used and date, but no survey of fish that were not caught. It can confirm that this species was present at that place and time. It cannot measure the lake population, a breeding rate or the share of water used by other species. The resource model copied the catch into a general food column without the sampling limit. Rowan restores the missing context rather than inflating a single observation into a stock estimate.", "", []),
("clock", "The Uncorrected Interval", "outerwake_archive", "jace_morrow", "inspect", "capacity_clock_register",
 "Compare Jace's raw time marks with the corrected chart and keep the clock drift attached to each sample.",
 "JACE MORROW", ["The corrected line looks cleaner, but the correction assumes the clock slowed at a steady rate.", "I cannot show that from two checks. Keep the raw marks beside the estimate and let the next survey decide whether the drift was steady."],
 "Two Clocks, Two Records", "The register stores the receiver's printed time beside Jace's manual clock checks. Between checks, the devices disagree by several minutes. A straight-line correction is convenient, but the clock may have lost time unevenly during the storm. The board showed only the adjusted interval, which made the signal appear more regular than the source data warranted. Rowan leaves the original sequence and the proposed correction side by side. Another observer can repeat the comparison without accepting Jace's estimate as certain.", "document", []),
("review", "An Assumption Is Not a Witness", "outerwake_archive", "evelyn_hart", "talk", "evelyn_hart",
 "Return to Evelyn and ask why the chart described its demand column as if it were testimony.",
 "DR. EVELYN HART", ["I called the column a witness because it came from a ledger. I had forgotten that the ledger was written for a different purpose.", "A record can be accurate about what it counts and still be the wrong evidence for the question we ask of it."],
 "A Ledger Can Answer the Wrong Question", "The demand column was copied from an inventory ledger used to schedule shipments. It records sacks dispatched, not meals eaten, people served or food shared between households. The number may be accurate within the shipping ledger while failing to represent actual need. Evelyn had treated the source's precision as proof that it measured the correct thing. The review now names the ledger's original purpose and warns later readers against substituting a precise shipment count for a measure of hunger or population.", "", []),
("garden", "A Seed Ledger at Greenwake", "greenwake_refuge", "mara_bell", "talk", "mara_bell",
 "Ask Mara Bell how the seed exchange ledger separates a reserve from food already distributed.",
 "MARA BELL", ["Our ledger marks seed saved for another season in a different color from fruit offered at the tables.", "The colors do not tell us whether every household had enough. They tell the next keeper what was set aside and what was given away."],
 "Greenwake Seed Exchange Rules", "The Greenwake exchange separates three entries: seed retained for planting, fruit distributed for eating and stock held for an agreed trial. The totals change after a poor season, but the ledger does not list household names beside public counts. Mara says families may correct their own entries or withdraw a sample from the trial. The record therefore describes a process rather than a universal yield. A carrying-capacity model that treats all seed as immediate food would erase the reserve that makes the next season possible.", "", [{"itemId":"glassplum_seed","quantity":1},{"itemId":"earthworm_bait","quantity":3}]),
("seedledger", "The Reserve in the Margin", "greenwake_refuge", "mara_bell", "inspect", "capacity_seed_exchange_ledger",
 "Inspect the seed exchange ledger and identify which reserve entries were excluded from the public crop total.",
 "ROWAN HALE", ["The public total lists fruit gathered, while the margin holds seed kept for the next planting.", "If I combine them, I count the same season twice: once as food and again as the beginning of another harvest."],
 "Seed Reserves Are Not Surplus", "The public Greenwake sheet reports the fruit distributed during one harvest. A narrow margin lists seed retained for the following planting, but that amount is absent from the chart reproduced at Outer-Wake. The margin does not prove that the reserve was sufficient; it shows that it was reserved for a different purpose. Counting it as current food would make the public supply appear larger and leave the next cycle unaccounted for. The correct report must show both quantities and say who is allowed to revise them.", "seed_cradle", []),
("glassplum", "One Glassplum Trial", "greenwake_refuge", "mara_bell", "grow", "glassplum",
 "Grow one Glassplum crop and record planting stock, elapsed time and usable harvest as separate measurements.",
 "MARA BELL", ["The graft came from a branch that has not been tested through winter. It may fruit well in this bed and fail somewhere else.", "Write down the one plot we actually observed. Leave the promise of a regional yield for a trial that has not happened."],
 "Glassplum Trial: One Bed", "The trial began with one grafted seed in the Greenwake bed. The crop matured after the configured interval and produced two fruit in this run. No second bed was planted, and the graft has not been tested through winter. These observations are useful for repeating the same trial, not for promising a valley-wide yield. Mara keeps the seed source, planting date and harvest together so another gardener can compare conditions. The model must distinguish a measured plot from an assumed regional rate.", "", []),
("wellmarks", "The Well Marks Do Not Agree", "greenwake_refuge", "mara_bell", "inspect", "capacity_greenwake_well_marks",
 "Read the two marks on the well wall and record that they were taken on different days under different weather.",
 "ROWAN HALE", ["The higher line followed a storm; the lower scratch was present before it. Neither one alone shows how much water the garden used.", "I am recording their dates and conditions instead of drawing one smooth line through two unequal observations."],
 "Greenwake Well Marks", "Two marks remain on the Greenwake well wall. The upper mark was noted after rain; the lower scratch predates the storm and may belong to an older gauge. The notes give no controlled reading of water entering or leaving the well. Joining the marks into a single trend would conceal their different conditions. Rowan records both heights and leaves room for a later measurement made with the same reference point. This evidence describes the wall, not the total groundwater reserve of Greenwake.", "stone_rill", []),
("choir", "Lyra's Listening Window", "choir_beneath_lake", "lyra_moss", "talk", "lyra_moss",
 "Ask Lyra Moss how a listening sample can be kept without turning a private voice into a public statistic.",
 "LYRA MOSS", ["A recording can preserve a pitch and still remove the moment when someone chose to sing. I log the room and the invitation separately.", "You may use the interval in the model, but do not copy a person's voice into a chart unless they agreed to that use."],
 "Listening without Naming", "Lyra's Choir ledger separates the measured interval from any voice heard during it. A participant may agree to a timing test without granting permission to preserve or publish a recording. The model needs the interval and the conditions of measurement; it does not need a private name to calculate that interval. Lyra's practice records consent scope beside each sample and permits withdrawal before the report is issued. A count that omits those limits may be mathematically tidy while taking more from a participant than the test required.", "", [{"itemId":"echo_kelp_seed","quantity":1},{"itemId":"choir_mote","quantity":2},{"itemId":"earthworm_bait","quantity":2}]),
("whisper", "A Whisper Koi at the Listening Pool", "choir_beneath_lake", "lyra_moss", "fish", "whisper_koi",
 "Catch one Whisper Koi and add the pool and date to Lyra's non-identifying listening register.",
 "LYRA MOSS", ["The koi carried a faint vibration in its scales today. We can note the sample and the pool without assigning it a meaning.", "One catch cannot tell us whether the vibration is common, seasonal or connected to the signal we heard."],
 "Whisper Koi: Local Sample", "One Whisper Koi was caught at the Choir pool for this review. The entry records the pool, time and physical condition of the specimen. The fish's faint vibration is an observation made by the keeper, not a decoded message or evidence of population size. Other species and uncaught fish were not surveyed. Lyra files the sample separately from the listening test so that a memorable catch cannot be used to explain an unrelated sound without further evidence.", "", []),
("kelp", "Echo Kelp in a Single Plot", "choir_beneath_lake", "lyra_moss", "grow", "echo_kelp",
 "Grow one Echo Kelp crop and keep its plot result separate from the wild samples in Lyra's register.",
 "LYRA MOSS", ["The cultivated kelp held a steady vibration after harvest, but the wild sample came from deeper water and another season.", "They are two observations. Do not use one to stand in for the other just because the same species name appears on both labels."],
 "Cultivated and Wild Echo Kelp", "The Choir bed produced cultivated Echo Kelp after one measured growth interval. The earlier field samples were collected from deeper water under unknown seasonal conditions. Both entries share a species label, but their growing environments differ. Lyra keeps the cultivation result out of the wild abundance column. This prevents a garden harvest from being mistaken for a naturally replenishing lake stock. A later study could compare the two environments, provided it records the location, season and number of samples.", "", []),
("balm", "A Balm for the Long Listening Shift", "choir_beneath_lake", "lyra_moss", "craft", "echo_balm",
 "Brew Echo Balm from the cultivated kelp and choir motes at the Archive Loom before reviewing the long listening interval.",
 "LYRA MOSS", ["The balm eases the strain after a long listening shift. It does not improve the accuracy of the receiver or restore a missing sample.", "Use the loom recipe, then note that the tool supported the observer rather than changing the evidence."],
 "Echo Balm and Observer Fatigue", "The Echo Balm was prepared from one cultivated kelp harvest and two choir motes using the Archive Loom. It eased fatigue during the review, but it did not alter the receiver's recorded interval. The original worksheet mixed the observer's late shift with the signal strength measurement; Rowan separates them. Human fatigue may affect when a keeper notices a sound, so the condition belongs in the procedure notes. A remedy can support the observer without serving as proof that the measurement itself is correct.", "", []),
("listening", "A Pause in the Score", "choir_beneath_lake", "lyra_moss", "inspect", "capacity_choir_score_margin",
 "Inspect the score margin where Lyra marked a pause and an invitation that could be refused.",
 "ROWAN HALE", ["The pause changes the timing but does not erase it. Lyra asked the singers whether it could be included before she wrote it down.", "A measurement of shared work still needs a boundary around what participants agreed to contribute."],
 "A Pause Is Part of the Record", "The Choir score includes a measured pause that was initially removed from the aggregate interval. Lyra restored it after the singers approved using timing data, while leaving their names out of the public copy. The pause changes the total, but its inclusion is not a license to preserve every voice. The record distinguishes consent to a timing measurement from consent to audio publication. Future comparisons should use the same inclusion rule and document when the rule changes.", "document", []),
("cinder", "Talia's Sample Standard", "cinderwell_basin", "talia_mercer", "talk", "talia_mercer",
 "Ask Talia Mercer how Cinderwell distinguishes a salt indicator from a measurement of the full water supply.",
 "TALIA MERCER", ["The wick changes color with the salt concentration in one sample. It cannot tell you the depth of the reservoir or where the salt came from.", "Take two samples from named points, label the conditions and keep the wick away from the distribution ledger."],
 "A Wick Is Not a Water Survey", "Talia uses a prepared wick to compare salt concentration between individual Cinderwell samples. Its color cannot estimate reservoir volume, identify a contamination source or describe all water delivered to households. The wick is a small test with a narrow purpose. Talia separates sample location and time from the allocation ledger so an indicator result cannot be used to assign responsibility for a shortage. The carrying-capacity report should identify the test's scope and make clear which larger questions remain unanswered.", "", [{"itemId":"salt_saffron_seed","quantity":1},{"itemId":"dryglass_shard","quantity":1}]),
("saffron", "Salt Saffron under Two Measures", "cinderwell_basin", "talia_mercer", "grow", "salt_saffron",
 "Grow Salt Saffron and record the bloom separately from the seed and the time the plot occupied water.",
 "TALIA MERCER", ["This bed used one seed and two watering turns. The blooms can be counted, but the water and growing time are part of the cost.", "If the model reports only the harvest, it makes the crop look free and hides what another plot could not use."],
 "Salt Saffron: Yield and Inputs", "One Salt Saffron bed grew from a saved seed and required the configured watering interval. The harvest produced two blooms in this run. The crop sheet had listed the blooms without the seed retained for another planting or the water used during growth. Talia adds those inputs beside the output. This does not decide whether Salt Saffron is an efficient crop; it supplies the information needed for someone else to compare it with alternatives under a stated set of conditions.", "", []),
("wick", "Prepare the Brine Wick", "cinderwell_basin", "talia_mercer", "craft", "cinderwell_brine_wick",
 "Craft a Brine Wick from one Salt Saffron bloom and the Dryglass shard Talia supplied at the assay bench.",
 "TALIA MERCER", ["The wick takes its dye from Salt Saffron and its edge from Dryglass. We will test one marked sample, not every channel in the basin.", "The tool is ready when its ingredients and location are written beside it. A color alone is not a conclusion."],
 "Brine Wick Preparation Card", "The Brine Wick uses one Salt Saffron bloom and a Dryglass shard. Talia prepares it at the assay bench and labels the sample cup before the color test. The wick responds to salt concentration in that cup; it does not report a water level, household access or the source of the salt. Rowan records the recipe so another worker can reproduce the tool. The prepared wick is an instrument with a limited range, not a shortcut around a basin-wide survey.", "", []),
("color", "The Color inside the Cup", "cinderwell_basin", "talia_mercer", "inspect", "capacity_brine_sample_card",
 "Read the sample card and compare the wick color only with samples taken at the same marked points.",
 "ROWAN HALE", ["The two cups changed by different shades, but they were filled on different days and after different rainfall.", "We can report the colors and conditions. We cannot rank the whole basin from these two cups."],
 "Two Samples, Unequal Conditions", "The first cup was collected before rain at the upper channel; the second came from the lower bend after a storm. Their wick colors differ, but both the location and timing changed. Without a matched collection schedule, the difference cannot be assigned to distance along the channel or to household use. Talia retains the separate readings and adds the weather note. The result motivates a controlled repeat; it does not prove that one district received worse water than another.", "document", []),
("dawnkeep", "Nia's Distribution Ledger", "dawnkeep_outpost", "nia_porter", "talk", "nia_porter",
 "Ask Nia Porter what a distribution ledger can reveal about access and what it leaves out about household need.",
 "NIA PORTER", ["The ledger records what crossed the gate and who signed for a delivery. It does not prove who drank, who shared or who had to leave early.", "You can publish delivery totals, but label them as deliveries. A household can correct its own receipt without exposing its neighbors."],
 "Deliveries Are Not Needs", "Nia's gate ledger records sacks delivered, the person who signed and the hour of arrival. It does not record how food was shared after the gate or which household members were absent. A shipment total can help plan transport, but it cannot serve as a direct measure of hunger or demand. Nia allows a household to correct its own receipt and keeps neighboring names private. Rowan copies the ledger's scope into the final report so readers do not mistake a precise count of deliveries for a complete census of need.", "", []),
("blackreed", "A Catch Below the Weir", "dawnkeep_outpost", "nia_porter", "fish", "blackreed_trout",
 "Catch one Blackreed Trout at Dawnkeep Lakeshore and log only the catch site and the waterline observed that day.",
 "ROWAN HALE", ["The trout came from the lakeshore pool below the weir. Nia's delivery log is a different record and should stay separate.", "I will note the waterline beside the catch date without claiming the fish tells us how many households the water can support."],
 "Blackreed Trout and Waterline", "One Blackreed Trout was caught below the Dawnkeep weir during this review. The note includes the location and same-day waterline, but no repeated catch survey or flow reading. Fish presence and a visible mark do not establish the volume available to homes, gardens or downstream species. Rowan keeps the catch log beside, not inside, the distribution ledger. The two records can be compared later when collection dates and methods align, but neither can replace a measurement it was not designed to make.", "", []),
("waterline", "The Line under the Barracks Step", "dawnkeep_outpost", "nia_porter", "inspect", "capacity_dawnkeep_waterline",
 "Inspect the waterline note and check whether the mark was recorded before or after the gate's scheduled release.",
 "NIA PORTER", ["The note gives a height but not the gate state. I can find the release time in another book, though the two pages were not signed together.", "Keep the uncertainty. If a later keeper matches the time, they can update the comparison without erasing this first note."],
 "Waterline without Gate State", "The stone mark was measured to the lower step, but the observer did not record whether the weir gate was open. A separate schedule lists a release that afternoon; its clock was not checked against the observer's watch. The two documents may refer to the same event, but their connection has not been verified. Nia keeps the original note and appends a cross-reference rather than merging them. The waterline remains a valid observation with an incomplete operating context.", "stone_rill", []),
("return", "Carry the Limits Back to Evelyn", "outerwake_archive", "evelyn_hart", "talk", "evelyn_hart",
 "Return the crop, catch, listening, sample and delivery notes to Evelyn without treating them as a single population count.",
 "DR. EVELYN HART", ["We have several careful observations and no common survey that makes them interchangeable.", "The report can still improve. It should name what was measured, who may correct it and which conclusions remain beyond the evidence."],
 "A Packet of Non-Equivalent Measures", "The review packet contains crop yields, fish catches, listening intervals, sample colors, shipment totals and waterline marks. Each entry has a different unit and collection method. Combining them into one score would require assumptions that have not been tested. Evelyn drafts a report that keeps the measures in separate sections and identifies the observer, date and known limits. The evidence can challenge an overconfident projection without pretending to solve the world's resource crisis or determine what every community should choose.", "", []),
("compare", "The Curve with Its Margins Restored", "outerwake_archive", "evelyn_hart", "inspect", "capacity_model_final_board",
 "Review the revised chart with seed, water, timing, consent and delivery limits visible beside every projection.",
 "ROWAN HALE", ["The range is wider now because we restored omitted inputs and clock uncertainty. A wider range is not proof that the world is safe.", "It is a more honest account of what these records can support and what must be checked again."],
 "Revised Projection: Open Uncertainty", "The revised chart keeps seed reserved for future planting, notes water used during crop trials and shows receiver clock uncertainty. It places consent limits next to Choir timing data and labels Nia's figures as deliveries rather than needs. The resulting range is wider and less decisive than the original curve. That change is not evidence that the world has escaped collapse. It means the available measurements support fewer precise claims than the earlier presentation suggested. A future review can narrow the range only by collecting comparable evidence under disclosed rules.", "document", []),
("policy", "What Should the Report Carry?", "outerwake_archive", "evelyn_hart", "choice", "capacity_publication_policy",
 "Choose how the report will present uncertainty while keeping household names and private voices out of the public copy.",
 "DR. EVELYN HART", ["We can publish a bounded range now, with assumptions and a review date, or publish the method while asking each region to revisit its figures first.", "Neither route makes the projection a law. Decide what readers need to check the work without turning a forecast into permission to sacrifice anyone."],
 "Publication Policy Decision", "The report is ready for a decision about publication, not a decision about whose life matters. One route releases bounded ranges, assumptions and an explicit review date while keeping personal records private. The other releases the calculation method immediately and delays regional totals until local stewards have checked whether the source records can be compared. Both routes preserve corrections and identify missing evidence. Neither route proves the World Will's forecast correct or false; the choice concerns how uncertainty and accountability are presented to readers.", "", []),
("publish", "Publish the Bounded Range", "outerwake_archive", "evelyn_hart", "inspect", "capacity_public_noticeboard",
 "Inspect the public summary and verify that its range, assumptions, correction path and next review date are visible.",
 "ROWAN HALE", ["The board shows the range, the assumptions beneath it and a date when anyone may request a correction.", "Household names and private recordings are absent. Readers can challenge the method without being given another person's ledger."],
 "Public Range and Review Date", "The public sheet shows the projection range, the rainfall and harvest scenarios, the seed-reserve adjustment and the receiver's timing uncertainty. It names no household and includes no private recording. A review date is printed at the bottom, along with a route for submitting corrections. This version offers more immediate public scrutiny, though readers may still mistake a bounded estimate for a promise. Evelyn adds a note that the range describes current records and must not be used as an eligibility rule for aid.", "noticeboard", []),
("restricted", "Publish the Method, Hold the Totals", "outerwake_archive", "evelyn_hart", "inspect", "capacity_method_review_case",
 "Inspect the sealed review receipt and confirm that the method is public while regional totals await local correction.",
 "ROWAN HALE", ["The method is available to everyone. The regional totals remain in the review case until the stewards check dates and definitions.", "The delay has a cost: people cannot compare the numbers yet. The receipt names when that delay will be reviewed."],
 "Method Released, Totals Under Review", "The review receipt confirms that the calculation method has been released while regional totals remain under review. Local stewards may correct dates, definitions and source references before publication. This protects communities from having unmatched delivery and harvest records presented as comparable measures, but it delays public comparison. The receipt includes a review date and a way to challenge the delay. The sealed case does not make evidence private forever; it sets a short accountability window before the totals must be reconsidered.", "sealed_case", []),
("afterword", "A Measure That Can Be Challenged", "outerwake_archive", "evelyn_hart", "talk", "evelyn_hart",
 "Speak with Evelyn after the selected report is filed and agree which measurements must be repeated before the next hearing.",
 "DR. EVELYN HART", ["The report can be corrected without pretending the earlier chart never mattered. We have documented its source and the choices it left out.", "At the next hearing, we can show what changed, what stayed unknown and who had a chance to challenge the measurements."],
 "Afterword: Review Before Judgment", "Evelyn files the selected report with its method, scope and review date. The team has not settled whether the world can endure without the recurring sacrifice. It has established that resource projections must be open to correction and that a measurement cannot consent on behalf of the people it counts. The next hearing will compare repeated crop, water and delivery records under shared definitions. The archive preserves both the earlier chart and the revision so later readers can see why the estimate changed rather than inheriting a claim without its history.", "", []),
]

assert len(steps) == 29
quests, dialogues, codex, landmarks = [], [], [], []
for i, row in enumerate(steps):
    (key,title,location,giver,kind,target,objective,speaker,lines,codex_title,body,visual,reward_items) = row
    qid = "side_capacity_" + key
    did = "capacity_" + key
    target_id = target
    prereq = "archive_return_report" if i == 0 else "side_capacity_" + steps[i-1][0]
    entry = {
        "id": qid, "arcId": "archive_beyond_veil", "stage": -1, "type": "side",
        "locationId": location, "giverId": giver, "title": title, "objective": objective,
        "prerequisiteIds": [prereq],
        "objectives": [{"id": "complete_" + key, "kind": kind, "targetId": target_id,
                        "requiredCount": 1, "description": objective,
                        "dialogueId": did}],
        "reward": {"gold": 6 if kind in ("talk", "choice") else 4, "items": reward_items}
    }
    if key == "policy":
        entry["choiceFlag"] = "capacity_publication_policy"
        entry["choiceSpeaker"] = "DR. EVELYN HART"
        entry["choicePrompt"] = "Choose a review policy. Both options keep names and private recordings out of the report."
        entry["choices"] = [
            {"id":"publish_range","label":"Publish the bounded range, assumptions and next review date; invite corrections.",
             "flagValue":"publish_ranges","dialogueId":"capacity_choice_publish",
             "reward":{"gold":0,"items":[{"itemId":"outerwake_margin_compass","quantity":1}]}},
            {"id":"regional_review","label":"Publish the method now; hold regional totals until local records are checked.",
             "flagValue":"regional_review","dialogueId":"capacity_choice_review",
             "reward":{"gold":0,"items":[{"itemId":"outerwake_review_locket","quantity":1}]}}
        ]
    if key == "publish":
        entry["branchFlag"] = "capacity_publication_policy"
        entry["branchValue"] = "publish_ranges"
        entry["prerequisiteIds"] = ["side_capacity_policy"]
    if key == "restricted":
        entry["branchFlag"] = "capacity_publication_policy"
        entry["branchValue"] = "regional_review"
        entry["prerequisiteIds"] = ["side_capacity_policy"]
    if key == "afterword":
        entry.pop("prerequisiteIds")
        entry["prerequisiteGroups"] = [{"anyOfQuestIds":["side_capacity_publish","side_capacity_restricted"]}]
    quests.append(entry)
    dialogues.append({"id":did,"speakerName":speaker,"lines":lines})
    codex.append({"id":"capacity_"+key+"_record","title":codex_title,
                  "category":"Carrying Capacity Review","writtenBy":speaker.title(),
                  "unlockQuestId":qid,"body":body})
    if visual:
        landmarks.append({"id":"capacity_"+key+"_marker","locationId":location,
                          "displayName":title[:58],"targetId":target_id,"visualId":visual,
                          "positionX":[-7.0,-2.4,2.4,7.0][sum(1 for m in landmarks if m["locationId"]==location)%4],
                          "positionY":[2.2,-1.0,-3.4][sum(1 for m in landmarks if m["locationId"]==location)%3],
                          "scale":0.085})

dialogues.extend([
    {"id":"capacity_choice_publish","speakerName":"DR. EVELYN HART","lines":[
        "I will publish the current range with every assumption visible, and put a review date where readers can find it.",
        "Household names stay private. The open margin is for corrections to the model, not permission to sort people by its estimate."]},
    {"id":"capacity_choice_review","speakerName":"DR. EVELYN HART","lines":[
        "I will release the method now and ask each region to check whether its records share dates and definitions.",
        "The totals will wait for that review. I will also publish when the wait itself must be reconsidered."]}
])
# The afterword may follow either mutually exclusive branch.
items = [
    {"id":"outerwake_margin_compass","name":"Open Margin Compass",
     "description":"A charm awarded for publishing a bounded resource range with its assumptions and review date. Its open rim leaves room for corrections.",
     "category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":0,"guardBonus":2,"healAmount":0,"sellValue":0},
    {"id":"outerwake_review_locket","name":"Local Review Locket",
     "description":"A charm awarded for releasing the method while regional totals await local correction. It protects the review date from being lost with the papers.",
     "category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":1,"guardBonus":1,"healAmount":0,"sellValue":0},
]
for filename, additions in [
    ("prologue_quests.json",quests),("dialogue_catalog.json",dialogues),
    ("codex_catalog.json",codex),("quest_landmarks.json",landmarks),
    ("item_catalog.json",items)
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename,catalog)
print(f"Installed {len(quests)} resource-model quests, {len(dialogues)} scenes, {len(codex)} evidence records, {len(landmarks)} landmarks and {len(items)} charms.")
