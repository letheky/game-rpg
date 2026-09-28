#!/usr/bin/env python3
"""Add source-aware long-form leaves to the first twenty Hundredth Roll records."""
import json
from pathlib import Path


CONTENT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"
MARKER = "\n\nSupplemental archive leaf —"


SUPPLEMENTS = {
    "hero_legacy_001_record": """Supplemental archive leaf — the west pier tally

The bridge ledger has a second sheet folded behind the toll column. Its top edge is dark with river mud, and the lowest lines were entered with a reed that split as it dried. The names are mostly missing. What remains are three work marks: a square beside the upper arch, two short strokes beside the eastern stair, and a hook beside the sandbag landing. Abel's measurements put each crew at a different span. The monument's claim that one champion restored the entire bridge cannot be reconciled with that division of work.

A later keeper pencilled a note beside the returned toll: some households had carried stones before their labor was counted. Abel did not charge them again when the winter levy came due. He also did not cancel the levy for those who had not worked; the ledger gives no such instruction. He corrected the amount for each household and left the reason beside it. That small distinction matters. Relief given because someone stood in a crew is not the same as a general order that everyone else owed nothing.

Rowan's reading: Abel's figures can guide a repair crew and a clerk checking a duplicate charge. They do not explain the missing contract page. The blank space between his final bridge entry and the next morning's departure remains a blank space. A returned toll proves a decision about payment. It does not prove a bargain with the World Will, a refusal of one, or the private thoughts behind Abel's choice to leave.""",
    "hero_legacy_002_record": """Supplemental archive leaf — the stones that stayed dry

Beatrice's map case contained a set of narrow paper slips marked with the day and the height of the river. They do not form a second map. Each slip records one place where the water crossed a path, one stone that stayed exposed, or one marker that could no longer be found. The western bank was surveyed after a dry week; the eastern bank was measured after the flood. The two drawings were never meant to meet at the center of the page.

The neat copy joined their lines and removed the dates. It gave travelers a crossing that looked convenient in every season, but the survey notes describe three different channels. Beatrice's method was slower: walk from a known marker, record the next visible stone, and stop when the water hides the reference point. She preferred a broken map with a date to a perfect line without one. A traveler could report the missing stone without being asked to guess where the river had moved.

The surviving slips include no account of a successful permanent crossing. Rowan cannot tell whether Beatrice returned to the river after the campaign or whether someone else filed the later notes under her name. What he can preserve is the distinction between two observations made under different conditions. The map offers a way to find out when the crossing fails. It is not a promise that the route will remain open.""",
    "hero_legacy_003_record": """Supplemental archive leaf — the night shift beside the cooling yard

One of Cato's cooling sheets records a mold splitting after the last workers had gone home. The royal tally entered no ingot for that attempt, so the official copy lists the furnace as idle. Cato's page instead records the heat already spent, the water carried to the yard, and the hours required to clear the broken clay. No one is named as responsible for the crack. A margin notes that the mold had been used twice beyond the maker's mark, but the handwriting does not match Cato's.

The workers' meal marks on the reverse are easy to mistake for finished-goods counts. Cato crossed out that interpretation and wrote the names of two carriers who delivered food after the second bell. Their visits do not prove that the shift continued; the cooling yard still needed water after the furnace went dark. A later portrait shows Cato holding a sword with an uneven spine, but no receipt ties that blade to this failed mold. The weapon may have been made from the recovered metal, yet the ledger does not say so.

Rowan's copy keeps production, repair and care in separate columns. A workshop's output cannot be measured fairly by counting only the pieces that survived casting. At the same time, a record of wasted heat is not proof that the royal copy was deliberately altered by a particular clerk. Cato left evidence of what the short count omitted and no name for the person who made it short.""",
    "hero_legacy_004_record": """Supplemental archive leaf — a hinge counted from both sides

The two reopened doors left different marks. The lower hinge carries fresh scrapes on its courtyard side; the upper one has a worn line on the interior pin. They were not forced in the same way, and the marks do not establish which door opened first. Delia's list places a family beside each courtyard turn, but several entries are only household signs: a blue pot, a three-pronged rake, a length of red cord. The list was useful to the gate crew. It was never a roster of everyone who lived in the district.

At the foot of the page, an unsigned hand added that the bell sounded before the last cart crossed. Delia wrote beneath it that the lower door had been reopened afterward. The note does not say who ordered it. A disciplinary report focuses on the seconds between signal and latch; Delia's page tracks the line of people still moving. Both papers describe the same gate from different jobs. Neither records the final crossing count.

Rowan leaves the reopened hinge in the entry because it confirms that the written order did not describe the entire evacuation. He does not call Delia a rule-breaker or a savior. The people who needed the door may have been inside the courtyard, outside it, or still on the road beyond the bell. Her record preserves a choice made under pressure without pretending that a later clerk could count every person who passed.""",
    "hero_legacy_005_record": """Supplemental archive leaf — rope, rain and the unfinished repair

The watchtower repair request is attached to the diary by a copper staple added long after Eamon's notes. Its date falls between two storms, but the page does not say whether the roof was fixed during that interval. A patch of clean paper above the signal schedule suggests that the leak stopped for a time. A later stain begins several inches below it. The rope's fibers swell in the same direction as the ink runs, although the stain alone cannot identify its cause.

Eamon recorded a test at the bell rope before the rain began. After an eastern wind, the line dragged against the tower's stone lip and returned slowly. He asked the next keeper to repeat the test with the rope dry and wet, using the same hand and the same pull. The instruction is practical: a missed call cannot be assigned to carelessness until the equipment and weather are checked. The signal book gave no place to record either condition, so Eamon wrote them in his travel diary where a later reader might still find them.

Rowan copies the repair request beside the measurements rather than marking the roof as repaired. The different handwriting on the added date proves that someone later changed the file, not why they did it. Eamon's pages let the next tower crew reproduce the test. They do not establish whether the three missed calls were caused by the rope, a keeper, a damaged bell, or more than one thing at once.""",
    "hero_legacy_006_record": """Supplemental archive leaf — two harvests with different purposes

The tin under the feast plot contains paper wraps with two planting dates. One batch was dry at the time it was sealed; the other already carried a pale ring of moisture. Faye kept both rather than mixing them, and wrote the bed number on every packet that could still be read. The public ledger counts the feast row as a single planting, which makes the garden appear larger and more reliable than the seed stock actually was. Faye's notes show where that impression came from without proving that anyone meant to create it.

The later gardener planted the reserve on lower ground, where water remained after the first morning. That bed yielded less in the first week. It also produced seedlings after the upper row had failed in a dry spell. The account has no complete harvest weight; several baskets were given to households whose names were not entered. A child marked the empty seed holes with small stones so no one would plant over the damaged wraps. Faye saved the stones in a saucer, an odd but useful reminder that a missing shoot had been noticed rather than forgotten.

The tin did not feed the town by itself. It kept one next attempt possible. Rowan preserves the dates and bed conditions along with the yield because seed that survives storage is not the same as food already on a table. Faye chose continuity over one impressive feast row, but her notes do not tell us what she personally thought of the officers the plot was meant to welcome.""",
    "hero_legacy_007_record": """Supplemental archive leaf — the unlabeled key and its copy

Gideon's drawing has a faint grease mark where someone pressed the key against the paper. The mark shows the bow's shape but not the teeth well enough to cut a replacement. His card gives the order of the tumblers and marks the brittle spring pin in red. A mechanic could use it to inspect the old lock; the page cannot open the archive by itself. Gideon noted that the pin should be removed from the rear, because pushing from the front could split the housing.

The inventory calls the key lost on the same night the lower hall was cleared. Gideon's note says he handed it to a keeper whose name he could not record. Those statements may refer to the same key and the same night, but the card does not mention a receipt or a witness. The later copy of the inventory uses the word stolen in a margin. No signature accompanies that accusation. Rowan leaves the word outside the transcription and records it only as an addition made by a later hand.

Gideon refused to put his name on the key tag. That could have been caution, courtesy to the keeper, or a way to stop his name from being mistaken for a claim of ownership. The evidence does not choose among those readings. The usable instruction is more modest: repair the lock without forcing the spring, and keep the custodian's identity blank until a reliable record supplies it.""",
    "hero_legacy_008_record": """Supplemental archive leaf — the stopping mark on the cliff lift

Hesta's first trial sheet includes a chalk line on the platform deck where the pulley was supposed to stop. The line sits close to the handrail, leaving less room for cargo than the storehouse plan allows. In the margin she drew two figures carrying a long crate between them. The figures have no faces and no names. A later copy removed them, labeling the space unused capacity. Hesta restored both the handrail and the chalk mark on her own copy before sending the plan back to the cliff crew.

The cracked brace was not replaced on the same day as the first failed lift. One note describes a temporary timber support; another says the wind had turned across the cliff face, so the platform was left at the lower landing until morning. The cargo register records no delivery in that interval. Hesta wrote that a stopped lift was still a working system if people could return by the stair. Her slower pulley ratio reduced the number of sacks carried per hour and kept the platform from striking the wall in crosswind.

Rowan cannot establish that the lift saved anyone during the campaign. The drawing does show that Hesta designed for people who had to ride back down after setting a load. The next keeper should test the wind, inspect the brace and leave the stopping point visible. Raising capacity is not the same as improving a route if the people who load the lift have no safe way down.""",
    "hero_legacy_009_record": """Supplemental archive leaf — two pages that answer different questions

Idris's oath page and his well-repair notebook have matching holes where they were once stitched into one booklet. The binding thread is different: the oath sheet was sewn with a dark cord, the work notes with linen. A clerk later joined the sheets through the same holes and copied both onto a single roll. The result reads as though every person named in the repair list stood behind Idris's vow. None of the work notes says that. Idris specifically wrote that the mason, the child with the chalk and the neighbor carrying rope were not present when the oath was spoken.

The well entry describes a cracked lip that dropped grit into the bucket. Idris waited for a mason to replace the upper stone before the village used the lower draw. The child marked the safe side of the path with chalk, then left before the repair was complete. The neighbor tested the rope twice and tied a different knot on the second attempt. These details are ordinary. They show why the well record matters: it lists work that continued after the formal campaign without turning that work into proof of allegiance.

Rowan keeps the praise for Idris and the repair list on adjacent pages, with a note that they were written for different purposes. The repair does not diminish his oath, and the oath does not absorb the labor of everyone nearby. The joined roll is a later editorial choice, not a statement Idris signed.""",
    "hero_legacy_010_record": """Supplemental archive leaf — a meeting with a visible pause

June's first room plan placed the honored chair on a low platform and the only door behind the speaker. In the revised drawing she moved the exit beside the table, left a clear strip of floor to it and added an unmarked chair at the end where the light was dimmer. No attendance sheet survives. Her minutes instead record pauses: the meeting stopped when someone asked, began again after water was brought in, and ended before the final motion was copied. The person who called for each pause is not named.

One fragment says that the blank chair was used once to hold a lamp while the council moved nearer the window. A second fragment says it remained empty. Both may describe different meetings. June did not fill the space on the seating chart afterward. She wrote that a place offered for listening should not become an obligation to speak. The room was small enough for a person to hear without sitting in the center of the group.

The council later called the layout a courtesy. June's note ties it to the way decisions were recorded: a person could stop the discussion before a vote, and a clerk had to mark that pause rather than erase it. Rowan cannot tell whether that rule changed the council's outcome. He can see the door beside the speaking chair and the blank place preserved on the plan. The drawing gives a later meeting a chance to make refusal visible before the minutes call silence agreement.""",
    "hero_legacy_011_record": """Supplemental archive leaf — the pause between the cases

The drill inventory lists a shortage of sharp points on the day Kellan halted practice. His private note explains that the case opened by the child held hunting shafts, not blunt practice arrows. He moved both racks indoors after noticing that the labels faced the wall when the lid was raised. The change did not add arrows to the supply count. It changed which arrows could be reached during a lesson and how easily a person could mistake one set for another.

The child is not named in the surviving sheet. A second hand added a small mark beside the phrase wrong case, then removed it from the clean copy. That might have been a correction or an attempt to identify who opened it; nothing else on the page supports either. Kellan records that no one was injured. Rowan does not use that line to argue the drill was safe: a precaution that prevents an injury does not become pointless because the injury did not occur.

On the next lesson, Kellan asked each archer to name the cap shape and check the rack before taking a shaft. The record does not show that every student remembered. It does show that the new storage rule was paired with a practice step rather than a warning posted too high to see. The ridge remained a dangerous place to miss. Kellan changed the arrangement of the work before asking the students to become more careful.""",
    "hero_legacy_012_record": """Supplemental archive leaf — the aperture in mist

Liora's original chart preserves three kinds of night: a covered window, an open window and the nights when condensation blurred the aperture. She marked the cloud cover beside each reading and copied the temperature from a separate wall gauge. The regular cycle in the published chart appears only after the uncertain nights are removed. Liora's margin does not say that the pattern was false; it says the clean copy cannot demonstrate how often the signal failed to appear.

A strip of paper taped to the aperture frame carries a drawing of the shutter edge. Liora asked a second watcher to check whether the bright interval came from beyond the ridge or from light passing along the inside of the frame. Their marks do not agree on one night. On two others they do. Neither watcher signed a statement identifying a sender. The test helped distinguish the tower's own hardware from a repeated light, but it did not answer what lay outside the view.

Rowan leaves both the disagreeing measurement and the two matching ones in the record. He does not call disagreement a flaw to be averaged away. The source remains unknown, and the chart covers only the aperture's small field of view. Liora's work matters because a future watcher can repeat it with the shutter open or closed and report which conditions were present. The page preserves a question that was measured carefully without pretending that the measurement solved it.""",
    "hero_legacy_013_record": """Supplemental archive leaf — the water between the two marks

Merek's brass weight has a flat side where it struck a stair tread. The rope used after the pump stopped carries a green stain below its fourth knot; the later line has a pale mineral ring at a higher point. The marks are not interchangeable. One was made while the flooded stair held still enough for a reading. The other came after the bell rope moved and the water shifted beneath the landing. A rescue clerk averaged the lengths, perhaps to produce one figure for the report. Merek wrote both values on separate sleeves for a reason.

The margin also records three sounds: a pump wheel slowing, a rope scraping stone and a bell moving once without a hand at the clapper. No time is written beside them. Rowan cannot turn the order of those sounds into a precise account of what happened below the landing. The water could carry vibration from a neighboring passage, and the report does not show where the listener stood. He records the sounds as observations with no assigned speaker.

The stairwell plan shows the last dry step, but no mark identifies the depth on the night of the rescue. Merek's two readings give a future crew a way to test the same landing under different flow conditions. They do not tell Rowan who reached the lower room or why the pump stopped. Keeping both lengths separate preserves the change in the water instead of inventing a single stable depth.""",
    "hero_legacy_014_record": """Supplemental archive leaf — a bell test is not a duty roster

Nessa's three bell positions were chosen by how the harbor carried sound, not by where a watch could be stationed. She noted the listener's location, the direction of the wind and whether a boat was moving between the tower and the east path. The lowest bracket reached the path nearest the village. The upper positions carried over open water but could be masked by rope noise near the quay. Her blank line for the next testing hour was left blank on purpose; a schedule needed people who had agreed to stand watch.

An officer's schedule was attached over the blank, assigning night calls to one family for an entire month. The pin holes overlap Nessa's test marks. She drew a box around the new schedule and wrote that no sound trial had been held at that hour. She did not cross out the family's name. The archive does not show whether she had authority to remove the assignment or whether the family later took the shifts.

Rowan transcribes the schedule as a later attachment, not as part of Nessa's experiment. A bell that can be heard from one place may be inaudible from another, and a sound test does not appoint the people who must repeat it. If the village wants another trial, it should record the position and conditions and ask who will take part. Nessa's page leaves that choice for the next group.""",
    "hero_legacy_015_record": """Supplemental archive leaf — the cart across the lamp

The third daylight reading was made while a loaded cart passed between Orin and the watcher. The lamp was not hidden by fog or cloud; its flash disappeared behind the cart's high canvas frame. The clean report called the attempt a failure and recommended testing only after sunset. Orin drew the cart's position on his copy and asked that the same signal be repeated at noon once the road cleared. The received plan omitted the sketch, so later keepers tested the lamp at night and never learned what the daylight trial had actually shown.

Orin moved the bracket lower on the tower to keep the lamp clear of the stone cornice. Two later readings remained visible to the watcher, but their timings differ by a few breaths. The note does not identify whether the difference came from the shutter, the person counting or the lamp's wick. A spare wick was found in the box, sealed and unburned. That is evidence about the storage kit, not proof that the original light failed.

Rowan keeps the blocked observation beside the two successful ones. It is not an excuse for a signal that could not be seen; it is a condition the next trial must reproduce or avoid. Orin tested in daylight because the ridge had repeatedly closed at noon. His record can help another keeper choose a bracket and a clear line. It does not identify who received the flash or what the receiver understood.""",
    "hero_legacy_016_record": """Supplemental archive leaf — the margin left unassigned

Petra's ration card uses the width of a scoop as its unit, but she wrote the grain weight on the back whenever the storehouse scale was available. Three portions remain in the margin without a household mark. A later officer assigned them to names already on the list, turning unclaimed food into a surplus that had never existed. Petra crossed through that calculation with one line and wrote the arrival date of three travelers. Their names are absent because no one asked them before the count closed.

The storehouse door could not shut during that week. The hinge had sagged and sacks were stacked where the latch should turn. Petra recorded every time she moved the last basket away from the threshold. She also noted that one traveler took no grain, another accepted a half scoop and the third asked for water instead. No reason is recorded. The card does not label any of them as hungry, sick or transient; it preserves what was offered and taken.

Rowan leaves the three portions unassigned. A complete page may still be incomplete if the people arriving after a tally are never asked what they need. But he does not distribute the remainder on their behalf, either. Petra's margin shows where a later clerk should return and ask, not how to calculate an answer for people whose names are unknown.""",
    "hero_legacy_017_record": """Supplemental archive leaf — a bridge that held through one rain

Quen's inspection sheet places the west pin and the stone seat on separate drawings. The crew that replaced the pin signed a measurement from the upper rail; the crew that reset the seat recorded a level from the lower bank. The two figures use different reference points. A later report compared them as if they were the same dimension, then blamed one crew for leaving the joint out of line. Quen circled the mismatch in units before he asked either group to inspect the other's work.

One crew accepted the invitation and wrote a note about the seat settling after rain. The other left the page unsigned. Their disagreement was not symmetrical: one had provided a measurement, the other had refused to certify a shared inspection. Quen did not erase either fact. The bridge held through the next storm, which tells us that the repair remained in place for at least that passage. It does not prove that either method was sufficient for every load or season.

Rowan preserves the unsigned space as well as the signatures. A blank signature line should not be mistaken for agreement, and a successful crossing should not settle an argument about which repair carried the load. The next bridge keeper can compare the two reference points and inspect the joint again. Quen's record leaves a way to continue the work without asking the archive to issue a verdict it cannot support.""",
    "hero_legacy_018_record": """Supplemental archive leaf — the inward face of the largest block

The quarry slips show six village marks on the shared cut. Rilla's family sign is present on the largest block, but the mason's drawing places that face against the wall where visitors could not see it. A later portrait was painted from the public side and makes the block look as if Rilla stood beside a family donation. Her note asks the painter to turn the mark inward in the next version. The painter did not change the portrait; a second copy of Rilla's note survived folded inside the lift ledger.

Each village supplied a different part of the work: one crew cut the stone, another cleared the path, two carried rope, and the remaining groups hauled the blocks when the cart axle failed. The memorial list records the dimensions and the lift crews, but not the quarry owners. Rilla asked for that choice because several households had shared the ridge for generations without agreeing that one sign represented it. The page names a common cut and leaves the exact first fracture unknown.

Rowan cannot reconstruct who struck the first wedge. He can preserve the distinction between ownership, labor and the public act of raising a wall. The stone's size does not make its source a family claim. Rilla's memorial gave the six villages a place to gather without putting the largest mark where everyone would assume it belonged to one person.""",
    "hero_legacy_019_record": """Supplemental archive leaf — three jars and a leaking roof

Soren's storage diagram numbers the shelves from the floor upward. The lower jars were filled first, before the roof began to leak. The upper trays caught soot from the workshop across the street, but a loose shelf brace let some of it fall into the samples below. Soren drew a dotted line where he believed the mixture began. His label lists three possible sources and gives a range for each; it does not claim that every fleck came from the same building.

The wind notes are in another hand and describe a turn across the lane during the fire. They do not have a matching date, though the paper fibers align with the jar tags. The sketch shows smoke drawn in two directions at different times. A later catalog shortened Soren's careful label to the nearest burned workshop, likely because that was the only name present on the city map. The archive cannot determine whether that simplification was made for speed, certainty or blame.

Rowan records the shelf damage as part of the sample's history. A jar can preserve ash and still collect contamination after it is closed. The material may narrow the broad area of the fire; it cannot identify a single doorway or person. Soren's three possibilities remain attached so that a familiar workshop name does not become more certain each time someone copies it.""",
    "hero_legacy_020_record": """Supplemental archive leaf — the shelter between blue and charcoal

The pass map folds along the ridge that closed during the storm. Blue marks lead outward from the last confirmed cairn. Charcoal begins after the party had waited inside a shelter whose roof sloped toward the western wall. Tovah wrote two nights beside the shelter sketch and drew a short line where the snow crossed the threshold. The official map connected the blue and charcoal marks into one route. That smooth line hides the pause, but the shelter note survives on the inside of the fold.

The rescued traveler's recollection describes a second path through the pine cut. The account was spoken after the party returned, not drawn while they were in the pass. Tovah left space for the witness to mark the path but never filled it in herself. A later surveyor added a dotted branch from the shelter to the north slope; the ink is different, and no explanation accompanies it. The branch may reflect the traveler's account, but the archive does not link the hand to a name.

Rowan keeps the blue and charcoal marks separate and notes the shelter as a known point. A future survey can walk from the cairn to the doorway and compare the two trails in different weather. It cannot reconstruct which path every member took, or whether the second route belonged to the same day. Tovah's map helps someone find the place where certainty stopped.""",
    "hero_legacy_021_record": """Supplemental archive leaf — the turning strip

Una's separate notebook records three answers from the households beside the strip. One family used the ground to turn a handcart; another carried water across it when the ditch dried; the third asked that the trial rows stop short of the shallow well cover. The answers were written beside a sketch of the boundary stakes, not transferred into the Crown crop ledger. A later clerk attached Una's yield tally to that ledger anyway. The numbers can describe what grew in the plot, but they cannot grant the Crown a right to the path or to the well approach.

The plants were removed before the public-bin harvest. The record does not say whether the vegetables were returned to the households, eaten by the garden crew or lost during storage. A tiny cart wheel drawn at the edge of the page may mark where the turning space was kept clear, but the drawing is not to scale. Rowan places it beside the measured row length and labels the relationship uncertain.

Una's choice was modest and specific: ask before moving a stake. She did not write a judgment about legal title, and no signed boundary agreement survives. The field succeeded as a trial crop, yet the ground remained shared by use. A future gardener can reproduce the crop arrangement; a future clerk must still ask the people who rely on the path before changing it.""",
    "hero_legacy_022_record": """Supplemental archive leaf — when to remove the brace

Vance's mast sketch contains two brace lengths and a small cut-out showing the sail's sweep. The long brace tore cloth because it crossed that path during a gust. The shorter strut cleared the sail but did not hold the mast at the same angle in calm air. Vance wrote separate measurements for each condition rather than offer a single replacement dimension. The harbor copy kept the calm measurement, which made the repair appear simpler and hid the instruction to remove the strut before the wind turned.

The crew made two repairs to the seam during the year. The first patch is square; the second follows the tear at a slant. That difference may indicate a new split or a larger patch on the same place. The record does not connect either repair to the short brace. No watch roster assigns the removal task, and Vance did not supply a name to fill the gap. Rowan leaves the responsibility field empty instead of placing it on whoever stood nearest the mast.

The drawing offers a procedure to inspect: check the sail path, compare the windward angle and remove the temporary brace before a crosswind. It cannot prove the second tear would not have happened with a different design. The lesson is not that removable parts solve every failure; it is that a repair must retain the conditions under which its measurements apply.""",
    "hero_legacy_023_record": """Supplemental archive leaf — the broken seal and the waiting shelf

Willa's custody slip begins after the seal was already broken. She counted the tools without recording their exact condition, then placed the crate on a shared-store shelf where a claimant could inspect it. The receipt says the contents were intended for a public well; it does not name the person who packed them or confirm that every tool arrived. Willa crossed out the absent family's mark because the family had left the district. She did not replace it with a neighbor's name merely because that household lived closest to the store.

The word donated appears in a later inventory, written below Willa's dated correction. It may describe what happened after the waiting period, but no handoff receipt accompanies it. A chisel returned to the crate has a different handle from the one drawn on the receipt. That could be a repair, an exchange or an error in the drawing. The tools were useful to the well crew; their usefulness does not establish who owned them.

Rowan records three steps separately: a crate arrived, Willa kept it in common custody, and an inventory later called it a donation. No document joins those steps with a confirmed decision by the absent family. A shared shelf protects tools from disappearing while a claimant is sought. It should not quietly turn into proof that no claimant existed.""",
    "hero_legacy_024_record": """Supplemental archive leaf — the lower course beneath the root

Xander's two survey marks sit on opposite sides of a root that lifted the measuring line each spring. The first stake followed the stone plan; the second measured the wall from a point where the tree's roots did not disturb the cord. Xander drew the distance between them and marked the finished wall lower by one stone course. The mason's note says the foundation was reset before the frost, but gives no reason for choosing that day. The wall survived the season without another repair ticket.

The tree was not cut down, though the file contains a request to prune two branches that covered the courtyard window. Xander did not sign the pruning order. Another hand marked the work as deferred. No dated account shows who made that decision or whether the branches were later trimmed. The record therefore cannot support the claim that Xander personally saved the tree. It can show that his measurements allowed the wall to be built around the root without hiding the change from the final plan.

Rowan keeps both distances on the copy. The lower course may have helped the wall settle, but the page does not isolate it from the new footing or that year's mild frost. A living root is a condition in the site, not an explanation by itself. Xander's work is repeatable because he wrote where the original line failed and where the replacement line began.""",
    "hero_legacy_025_record": """Supplemental archive leaf — the pot near the wall

Yara's row sheet contains a small pot mark beside the earliest shoot. That pot stood against a south-facing wall and was carried indoors on the frost warning night. The field-bed seeds were planted later, after the rain, and exposed to two nights when the soil crusted. The published note lifted the first shoot from the pot and placed it at the head of the field row, then called the seed frost-proof. Yara's private page separates the protected plant from the trial bed and shows why the comparison did not support that label.

She recorded every seed, including the ones that never opened. For three entries, the soil condition is written beside an empty mark. One plant emerged after the second thaw but died before its first leaf spread. The harvest register left those lines out because there was no fruit to count. Yara kept them to explain how many seeds had been planted and why the reported yield seemed higher than the bed's actual return.

No surviving test identifies a stronger variety. Rowan writes down the shelter, dates and failed shoots so another gardener can set a pot and field row under matching conditions. One protected plant can begin a question. It cannot stand in for a whole crop, especially when the field failed twice.""",
    "hero_legacy_026_record": """Supplemental archive leaf — the last complete pour

Zev's cracked cup is stored beside the public table where a reader can compare its rim with the neighboring vessel. The cup was made by a different potter and has a slightly wider base. Zev stopped the cistern test when the hairline reached the lip, then recorded the last full pour he could finish without spilling. The estimate added later came from a cup that held a different volume. It may be a reasonable planning guess, but it is not a measurement taken from Zev's vessel.

The test card includes the draw time and the bucket position, but the cistern level mark is missing from that date. A second reader can repeat the pour only if they know which cup, which line and which level were used. Zev left space for those details on the public table. The clerk filled the blank with a neighboring vessel's total instead. The change made the series look complete and made the original failure harder to find.

Rowan preserves the crack as part of the evidence, not as a dramatic symbol. A broken instrument can tell a later worker when to stop trusting a run. He refuses to infer the unmeasured remainder from the shape of the neighboring cup. The next table can start again with matched vessels and a marked level; this one should remain incomplete where Zev stopped.""",
    "hero_legacy_027_record": """Supplemental archive leaf — the shutter test before dawn

Alwen's notebook pairs readings from three surfaces: the west soil bed, a stone ledge above it and the water in a covered jar. The soil was warmest before dawn after a clear day. On mornings following rain, the difference narrowed. When the greenhouse shutter stayed closed, the stone and bed cooled more slowly than the jar. Alwen proposed that stored warmth in the wall could explain part of the pattern, but did not remove the possibility of a warm spring beneath the floor. No instrument reached the water below the greenhouse.

The first keeper had called the warm row proof that the spring heated the soil. Alwen did not cross out that sentence. She set a second column beside it for the readings taken after the shutter opened, showing how the gap changed with air movement. A later summary copied the first observation and left out the repeat. It may have been shortened for the planting guide; the page does not identify who edited it.

Rowan keeps the measurements attached to their surfaces and times. Soil warmth can affect a crop even if its source remains unknown. A new gardener can repeat Alwen's test by measuring before sunrise and comparing the shutter conditions. The archive does not authorize anyone to dig into the greenhouse floor or name the spring as the cause without a separate measurement.""",
    "hero_legacy_028_record": """Supplemental archive leaf — the path along the shared centerline

Briar's chart places a centerline between two garden plots, but the hedge itself leans from one side to the other as its branches thicken. The straight-wall gardener wanted a clean division. The other household pointed out that the low path needed wind cover while seedlings were small. Briar measured the hedge from both beds and marked the branch that sheltered the tray. The measurements do not grant either household a greater share of the boundary; they show what would change if the thick limb were removed.

The two signatures on the chart appear below the path sketch, not below the hedge dimensions. Both households accepted keeping the footpath open. Neither signed the proposed cut. A later garden plan shows the hedge trimmed at the top, but the date is uncertain and the initials are too faint to identify who did the work. The disagreement about the shape may have continued after the path was agreed upon.

Rowan leaves the path agreement distinct from the pruning question. A practical compromise can settle one immediate use without settling every claim around it. Briar's shared centerline gives the gardeners a place to begin another conversation. It should not be copied as a permanent property boundary without asking whether the same families still use the path or whether the hedge has grown differently.""",
    "hero_legacy_029_record": """Supplemental archive leaf — the basket columns

Cress's original tally has three columns beneath the basket count: sold, exchanged and left at the gate. A fourth line beneath them records produce spoiled before the stand opened. The supervisor's tax copy preserved the sale column and omitted the other three. It therefore made the stand look half-empty and the tax due look smaller. Cress wrote that the missing vegetables were shared or spoiled, but no receipt confirms the weight assigned to either group. The records do not permit Rowan to rebuild the exact loss.

The gate note lists a traveler who arrived after the produce had been set out. The entry has no name, only the hour and a mark for one bundle carried away. It could refer to one of the shared portions or to a barter that was never copied into the sale book. The next morning, Cress added a note that rain had softened the lower baskets and that some leaves could not be sold. These entries make generosity and waste part of the same week without reducing one to the other.

Rowan transcribes the columns separately. He will not use the tax copy to calculate the stand's total harvest, and he will not claim every missing vegetable fed a traveler. Cress's count is incomplete, but it is honest about the different ways a basket can leave a stall.""",
    "hero_legacy_030_record": """Supplemental archive leaf — the rung and the low branch

Dara's ladder drawing puts the first rung close to the ground so a picker can test the feet before climbing. The widened base reduced how much the ladder shifted on the orchard slope. A second adult signed the weight test, but the note says only that they climbed halfway and returned. The page does not describe a test at the top with a full basket. Rowan keeps that limitation beside the repair rather than calling the ladder proven safe for every load.

The branch within reach of children is shown with an arrow to a cluster of fruit. The caretaker's objection was about next year's yield, not the children's safety. Dara marked the fruit in its own row so the next harvest could show whether leaving the branch changed the total. No harvest record survives for that season. The caretaker and Dara may have disagreed about the risk; the archive only preserves the proposed test and the missing result.

Dara wrote that the ladder served the people who picked fruit. That includes experienced adults and anyone asked to carry a basket, but it does not answer how much risk was acceptable or who could decide. Rowan leaves the trial open. The repair is a useful design to inspect, not permission to send a child up the branch or to treat one halfway test as a guarantee.""",
    "hero_legacy_031_record": """Supplemental archive leaf — the week without a planting mark

Elowen's calendar places a blank week after a storm that soaked the upper beds. The official plan assigned a crop to every row of the schedule, so the gardeners who did not plant appeared behind. Elowen wrote the soil condition in the margin and left the dates where they were. When the ground drained, the second gardener followed the same calendar and added the actual planting day beside the planned one. Their yield was smaller than the first year's estimate, but the beds can be compared without moving every later date to conceal the delay.

The blank interval is not a forecast. It does not say every future storm will require the same pause. A note from the gardener marks one bed where water remained under a board even after the surface looked dry. Another bed drained more quickly because its furrow had been cleared. Elowen did not merge them into a single soil condition. The schedule that came later did, perhaps to make the fields easier to manage from the office.

Rowan keeps the empty week visible and attaches the weather note. A calendar with a blank may still record work accurately when no planting took place. A later gardener can use Elowen's dates to decide what to check before sowing, but should not copy the pause as a rule independent of soil, drainage and the people tending each bed.""",
    "hero_legacy_032_record": """Supplemental archive leaf — carrying weight on wet ground

Fenwick's two basket samples are still marked with the waterline they were tested under. The rigid basket carried more seed in dry weather. When its handle stayed wet, the stiff weave pressed a narrow ridge into the carrier's palm. The mixed weave held less, but its joined short reeds flexed when the path tilted. Fenwick demonstrated the difference with the same sack and wrote down which handle each carrier used. The market copy called the mixed basket inferior after comparing weight alone.

The workshop note records a repair to the double knot after a strand loosened. Fenwick shortened the loose end and tucked it under the crossing reeds rather than add a metal fastener that would snag clothing. The repair did not make the basket stronger than the rigid sample; it made the handle easier to replace with marsh reeds on the path. A later carrier added a cloth wrap for a long walk. That addition is in a different hand and was never included in the pattern's standard version.

Rowan keeps both basket designs and the conditions beside them. The larger basket remains useful for a dry, level road. The flexible one carries less and fits the marsh route better. Neither is simply the better tool. Fenwick's record survives because it names the person carrying the load as part of the design.""",
    "hero_legacy_033_record": """Supplemental archive leaf — waiting through the next winter

Garrick's graft tag records the day the branch first flowered and the night a late frost browned its fruit. The rootstock field is blank, and the donor field says traveler, with no mark for a name or home. Garrick asked another gardener to wait through one more winter before naming the cross. A market seller later called the fruit Crown Sweet and credited it to Garrick, but the surviving tag does not show whether Garrick saw that label. The name may have helped people recognize a basket without describing the tree's lineage.

The tree survived the frost, though several branches did not flower the following spring. Garrick drew each living limb and numbered the graft points. The drawing uses the direction of the branch rather than its height so another gardener could find the same place on the trunk. A later sketch traces a line through the graft as if it were a single crown. Rowan keeps the earlier numbering beside it; the two drawings record different ways of describing the plant.

No evidence identifies who supplied the rootstock or whether the traveler was the graft's only source. The tree could be propagated, but a seller's name does not settle its ancestry. Garrick's patience leaves the question open until another season can be observed. The archive preserves that waiting as part of the work, not as a failure to finish naming.""",
    "hero_legacy_034_record": """Supplemental archive leaf — condensation on the stair pipe

Hester's two stone jars occupied different places in the cellar. The dry shelf stood above the stairs, where air moved freely. The damp jar sat near a pipe that leaked only before sunrise, leaving a film inside the stone. Hester noted when the wall felt wet and when the seeds darkened. The clerk emptied that jar before she could weigh the damaged lot. A second jar lost seeds to insects, though its inner wall stayed dry. Hester refused to call either storage method reliable after one season.

The humidity card includes a line of charcoal beside each date. It marks the pipe's drip, not the amount of water inside the jar. A later reader copied the line into a seed-loss column, making it appear that the wet jar had lost more seeds than the dry one. The original does not give a complete count for either. Rowan records the charcoal as a condition marker and leaves the missing quantities missing.

The better-germinating lot came from the shelf, but it also began with a different seed packet. The comparison cannot isolate the jar from the starting stock or insect damage. Hester's record supports a new trial with matched seeds and clean vessels. It does not certify stone jars, and it does not tell a future gardener to discard every packet that has touched a damp wall.""",
    "hero_legacy_035_record": """Supplemental archive leaf — move the bench before the tray

Isolde's first trial moved the trays between benches, but the roots had already grown toward the light. She restarted the comparison with empty trays and marked where the morning shadow ended. On a cloudy day, the eastern bench's advantage shrank but did not disappear. The window pane also held a faint amber tint that the room plan does not mention. Isolde wrote that the test needed matching seed lots and the same water before anyone could attribute stronger growth to the seed.

The later summary compares the yield of the eastern tray with the western one and calls the seed stronger. It does not say that the eastern bench had more hours of direct light. Isolde drew the shadow line beside the summary, then added a note asking the reader to repeat the trial after cleaning the panes. No receipt says whether the panes were cleaned. The plants were later moved out of the room during roof repairs, ending the comparison.

Rowan keeps the bench position as an observed condition, not a proof of cause. A future grower can place empty trays, track light and water, then compare matched seeds. The experiment has no final answer because the repair interrupted it. That interruption belongs in the archive; removing it would make an unfinished trial look like a settled judgment about the seed.""",
    "hero_legacy_036_record": """Supplemental archive leaf — the dotted line beneath the trench

Jory's map begins at the exposed trench face. He drew roots he could see as solid lines and extended them with dots where the soil remained closed. The older map connected those dotted sections into a continuous underground channel. It also left out that the upper bed had been watered twice as often. Jory wrote the watering schedule beside the root sketch, but the copyist placed the note on the next page. Without that context, the green bed looked like evidence of one hidden water source.

The trench was not widened after Jory drew the map. No excavation tested whether the roots met or whether moisture traveled along the same layer of soil. A gardener's note from the lower bed says its leaves dried before noon, then recovered after the afternoon watering. That note describes the plants; it does not locate every root below them. Rowan places it beside the map so the reader can see another difference between the beds.

Jory's dotted lines are a method for showing where observation ends. They are not a decorative version of the roots. The archive keeps the boundary between visible ground and unseen soil. A future gardener can reopen a small section and revise the map, but should not dig along the entire dotted route on the strength of a drawing that clearly marks itself incomplete.""",
    "hero_legacy_037_record": """Supplemental archive leaf — the wake between the rings

Kestrel's first bell test coincided with a boat crossing the lake. Its wake reached the lower bank before the sound did, and the listener wrote that the first ring had not arrived. The second ring, made after the boat passed, was heard across the water. The report later included only that successful reading and recommended the bell as a reliable warning. Kestrel kept the failed trial with a sketch of the boat's route and a request for another signal near the docks.

The far-bank listener and the dock keeper stood in different places. Their notes use the same word, heard, but one describes the bell's rhythm and the other says only that a sound reached the post. No one recorded how loud the wake was, and the boat's speed is unknown. The two accounts cannot be averaged into one distance. They can help a later tester choose separate listening points and repeat the ring with and without boat traffic.

Rowan preserves both trials without declaring the bell unusable. A signal may work across open water and fail beside a busy dock. Kestrel did not finish the design of a second method; the page only asks that one be considered. The next group must decide whether another trial is worthwhile and who will stand at each location.""",
    "hero_legacy_038_record": """Supplemental archive leaf — the shoveled alley

Larkin's drift chart includes two measurements at the warming-room door. Before the workers cleared the path, snow covered the lower latch. Afterward the line was lower, but the crew had piled the snow along one wall and narrowed the alley. A later chart plotted both heights as natural accumulation, attributing the sudden change to wind. Larkin drew a shovel beside the second date and wrote that the crew had moved the drift. The handwriting is small but matches the maintenance notes elsewhere in the book.

The crew cleared the door because an older resident needed the room's warmth before nightfall. The note gives no name and does not describe the resident's condition. A tally records one trip through the doorway and two bundles of wood carried inside. Rowan keeps those entries separate; they do not prove that the person stayed overnight or that the room warmed adequately. They do show why the door was cleared while measurements were still underway.

The wind gauge for that evening is missing. Larkin's snow marks remain useful if the shovel work and alley shape are included as part of the site. A future keeper can measure a natural drift only after noting what was cleared and where it was moved. The chart cannot tell whether the wind shifted during the same hour.""",
    "hero_legacy_039_record": """Supplemental archive leaf — the listener's blank field

Maris wrote the rhythm as groups of short and long marks separated by a pause. The second listener arrived after the first had stepped away from the stones. Both heard the pattern return; neither saw a person near the vent. Their notes do not agree on which beat came first, and the stones were wet on one side of the passage. A rehearsal copy added the name of a choir singer who was recorded in another village that night. Maris's page leaves the source field blank.

The southern stones sit above a channel that carries water after rain. A maintenance plan also shows a bell cable running behind the wall, though no note confirms that the cable moved during the listening. Water, a bell or an unseen chamber could have shaped the rhythm. Rowan will not select one explanation because it best fits the archive's larger story. The singer's absence corrects one mistaken attribution; it does not identify what made the sound.

Maris transcribed what could be repeated: the pause, the number of beats and the place where each listener stood. She did not claim to have met the speaker. That distinction protects the record from becoming a message assigned to the nearest person in a roster. A future listener can test the stones under dry and wet conditions, with the cable still and moving, and add observations without filling the blank for Maris.""",
    "hero_legacy_040_record": """Supplemental archive leaf — two bends, one reed

Niall's temporary marker was a reed tied beside a repaired stone gauge. The stem has two pale bends: a lower one facing upstream and a higher crease facing the bank. A branch caught in the channel appears in his sketch above the second crease. The first bend may have come from the current, a line pulled against the stem or the weight of the marker itself. Niall wrote those possibilities in a margin rather than choose one. The rushed report later turned both marks into a single high-water event.

The reed was replaced the next morning, before another observer could inspect it in place. Niall brought the stem to the repair table and drew its direction against a north mark, but did not note how long it had been drying. The scars preserve an order only if the sketch's orientation is accurate. A later hand added a date that may refer to the gauge repair, not to the flood. Rowan keeps that distinction visible.

The record can guide a repeat test using a firm marker and a second witness during rising water. It cannot reconstruct a complete flood level from a removed reed. The two bends are evidence that the stem changed shape twice; their causes and timing remain open. Niall's page is valuable because it leaves enough uncertainty for the next measurement to be honest.""",
    "hero_legacy_041_record": """Supplemental archive leaf — the line before the names

Odelia's transcript has a divider drawn in blue ink where the measured bell interval ends and the neighbor's private account begins. The public copy keeps the timing, the listener's position and the direction of the wind. Beyond the divider, the page is folded inward and sealed with a mark that Odelia describes as the witness's own. The binder that lost the divider pressed both halves flat and copied the private words into the index. No surviving authorization allows that copy to be read aloud.

The sealed portion remains in the archive, but this record does not reproduce it. Rowan can see where its edge begins and can verify that the consent slip is signed only for the interval. He cannot infer the neighbor's name from a public schedule or use the private pages as evidence of who was present. The witness may have discussed a person, a sound or something unrelated to the bell. Odelia's boundary protects the testimony from being made to answer questions it was never given for.

The public timing can be compared with other bell tests without opening the sealed section. If a later reader asks for the rest, the file says to ask the witness or the person the witness designated. Silence is not a release of permission. Odelia's most important contribution is a divider that survives the act of copying.""",
    "hero_legacy_042_record": """Supplemental archive leaf — position before instrument

Perrin's listening rope carried two knots: one for the depth at which a bell became distinct and another where water noise covered it. At the second well, the listener stood higher and closer to the stone fork than in the first trial. The summary blamed the fork after the results differed. Perrin moved the listener to the first position before replacing the fork, then repeated the hearing. The gap narrowed. That repeat did not explain what lay under the stone floor, but it showed that the comparison had changed two conditions at once.

The rope itself stretched when wet. Perrin measured its length on the quay before lowering it and again after hanging it dry overnight. The first knot shifted by less than a finger's width; the second mark was harder to read because the rope had twisted. A later copy drew the knots as perfect circles. Rowan keeps Perrin's uneven marks and the warning that depth estimates are approximate.

The old well's sound remains unexplained. A future test can match the listener's distance, depth and rope condition before changing the fork. It should not treat a clearer sound as proof of a hidden chamber. Perrin's method narrows one source of variation so the next question can be asked without pretending the first experiment answered everything.""",
    "hero_legacy_043_record": """Supplemental archive leaf — inspect the hinge first

Quilla's crescent cut sits on a stone plate near the southern window, but the plate's fastening holes are wider than the iron pegs. It could have shifted when the archive wall was repaired. Quilla compared the cut's direction with the shutter schedule and found that a wooden panel covered the window for half the month. Her note asks the next surveyor to inspect the hinge and record whether the shutter stands open before comparing the mark with the moon.

The later guide calls the cut a calendar. A second copy calls it a warning. Neither title appears on Quilla's sheet. Her measured drawing preserves the shape, the noon direction and the plate's relation to the sill. A note in the guide's binding says that the plate may have been moved before the archive was sealed, but it is unsigned. Rowan records the titles as later interpretations, not as evidence of Quilla's intent.

The mark may have been decorative, practical or astronomical. The archive supports none of those explanations by itself. A modern observation can check the plate's position and the shutter's movement, then report the conditions. It should not use a striking shape to fill the gap left by the missing fastening receipt. Quilla left a question for a surveyor to inspect, not a prophecy to inherit.""",
    "hero_legacy_044_record": """Supplemental archive leaf — the change in mesh

Rook's net was sewn from two patterns because the dock served both a narrow creek and a mixed current near the outer wall. One panel held small fish when dry but tightened after soaking. The other stretched under wet weight and let some of the smaller catch escape. Rook joined them with a visible seam and marked which section had been used in each test. The buyer's word defective appears on a receipt for the net, not on Rook's repair sheet.

After the storm, the net was mended again. The second repair used a different knot, and the catch log ends before any weight is written beside it. We cannot compare the net's yield before and after that repair. A dock child drew three fish beside the torn seam; the drawing is not an inventory, but it may show where the net had snagged. Rook did not copy it into the buyer's record.

Rowan keeps the seam, the two knot patterns and the limits of the catch count in one entry. A net with different openings can be appropriate for separate jobs if its use is named. It is still necessary to inspect damage and record the conditions. Rook's pages cannot tell us whether the mixed design fed the dock through the winter, only how someone tried to repair it without making its differences invisible.""",
    "hero_legacy_045_record": """Supplemental archive leaf — what the resonator changed

Sable marked the pier stone with a chalk grid before fastening the metal resonator. The first pulse moved dust from one square into the next. When the plate was removed, the pulse remained in the stone, but the interval was harder to count. As a barge passed behind the wall, the rhythm shifted. The resonator had made the movement visible and helped Sable mark time; it had not produced the vibration or named its source.

The public report calls the device a discovery tool. Sable's own page uses a smaller phrase: counting aid. A later keeper underlined discovery and attached a list of possible chambers, but the list has no measurements. Rowan leaves it in the file as an interpretation. The pier plan shows a drainage channel near the north stones and a mooring ring close to the resonator. Either could affect vibration, and neither was tested while the barge passed.

A repeat should compare the plate fixed, removed and placed on another section of stone, with boat traffic noted each time. That would help separate what the instrument reveals from what the structure carries. Sable's observation remains valuable without giving the pulse a speaker. The archive has a rhythm and an unknown source, not a message waiting to be assigned.""",
    "hero_legacy_046_record": """Supplemental archive leaf — the dark nights in the tally

Tamsin's lamp sheet marks five nights without a flash. Two entries cite mist thick enough to obscure the ridge's direction. One records a damaged shutter; another notes that a traveler asked for the path to remain unmarked while they moved through the pass. The fifth line is torn away. The public tally counted each blank as a missed shift because it had columns for flash and failure but none for a deliberate pause.

Tamsin's copy does not prove every blank night was a choice. The missing line could have described a breakdown, weather, a change of keeper or another request. A repair receipt exists for the shutter but carries no date. Rowan leaves the torn place open instead of choosing whichever explanation suits the account of a careful night watch. The weather entries show why a lamp might be withheld; they do not establish what happened each time it was dark.

The path marker would have helped some travelers and exposed others. Tamsin recorded the request without naming the person who made it. A later signal plan should include a way to write why a signal was held, who made that decision and whether it was repeated under safer conditions. Absence from a tally is not automatically failure. It is also not automatic proof of protection.""",
    "hero_legacy_047_record": """Supplemental archive leaf — low water and rainwater

Ulric's two bell intervals were measured from the same stone ledge but under different water levels. At low water, the sound reached the listener after a longer pause. After rain, it arrived sooner. The copied report averaged those numbers into one travel time and removed the water marks. Ulric's original card warns that the stone channel may have narrowed or widened as the lake rose, but he never measured the channel itself.

The bell was tested once with the shoreline rope tied and once while the rope hung loose. The record does not say which interval belongs to which rope condition. A sketch of the knots was added later in another ink. Rowan preserves the sketch as a clue to an unrecorded variable, not as a correction he can make with certainty. The channel may carry sound, but the tests do not locate its source beneath the wall.

Future readings can be taken at both water levels with the rope secured the same way and the listener standing at the marked ledge. The result could help keep the warning schedule from assuming one travel time through every season. It cannot identify a chamber or prove that the bell and the water pulse share a source. Ulric's page suggests a comparison, not a conclusion.""",
    "hero_legacy_048_record": """Supplemental archive leaf — the line of dots

Veda's original transcript carries a tear through the middle of a sentence. She copied the readable words on either side and drew a line of dots where the paper was gone. The witness had asked to review the page before it entered the archive, then never returned. Veda's private margin remembers a pause but not the words. A later copy joins the fragments into a fluent account, changing the point where the speaker stopped and making the sentence appear complete.

The archive does not say why the witness failed to return. They may have changed their mind, moved away or been unable to come back. Veda did not write that the account was withdrawn; she wrote that she could not verify the missing line. Rowan keeps the readable portions but marks the reconstruction as an editorial addition. He will not use the later smooth sentence as direct testimony.

If the witness or their chosen representative returns, they can review the surviving copy and decide whether the fragments should remain public. Until then, the dots are part of the record. A fluent sentence is easier to repeat, but ease of repetition does not make it accurate. Veda's transcript allows the archive to preserve what survived without claiming ownership of what did not.""",
    "hero_legacy_049_record": """Supplemental archive leaf — distance and effort

Weston's milepost has two carved faces. One measures outward from the gate; the other measures the return from the sheltered well. The road descends on the way out and climbs on the way back, so the same marked distance costs different effort. A route book copied only the gate face and described the road as level. Weston's sketch shows the grade and a stopping place where the axle could cool before the climb.

Two cart marks are scratched into the post base: one broad and one narrow. They may represent loaded and empty wagons, but Weston did not label them and no test log connects either mark to a weight. The post's distance is a measurement between points, not a promise about travel time. Rain, load and wheel condition could change the journey even if the mile count did not.

Rowan copies both faces and the slope. He leaves the two cart marks unattributed. A future traveler can record the load, weather and rest stop while following the route. That information would explain why one return took longer than another without changing the measured distance. Weston built a marker that answered where the road turns; he did not claim every cart would travel it at the same pace.""",
    "hero_legacy_050_record": """Supplemental archive leaf — the last reliable weight

Yvonne found the salt jar's seal loose after a dry week. She marked the crystals caught in the thread, wrapped the remaining sample in waxed paper and wrote the last reliable weight on the outer label. The official stock count still called the jar full because no one weighed it after the leak. The inventory therefore records what was expected to be present, not what Yvonne found on that day.

The jar's clay came from the basin named on the receipt, but the receipt describes the delivery rather than the contents at the time of storage. Yvonne did not say who opened it or whether anyone used salt during the week. A pinch may have fallen through the loose seal; the record does not quantify it. A later tally attributes the missing amount to the road crew, though no issue slip is attached.

Rowan keeps the basin label and the last weight separate. The crystals can still identify the sample's broad origin even if the quantity is uncertain. The stock total cannot be corrected by guessing how much leaked or who handled the jar. A future keeper should weigh the container, replace the seal and record the change before it enters another inventory.""",
    "hero_legacy_051_record": """Supplemental archive leaf — the fourth bowl

Bram's rota lists three scheduled watches. The kitchen sheet records four bowls used on two nights, and a later clerk interpreted the difference as stolen food. Bram wrote that one guard asked to stay unnamed after taking an unplanned watch. The person may have been the same on both nights; the sheets do not prove that. The bowls were washed and returned to the shelf, so there is no mark that would identify who used them.

The road post had a rule that the last traveler could take a warm meal if weather closed the crossing. That rule was written on the kitchen door, not in the ration ledger. Bram's bowl may have been used under that rule or by the unnamed guard. Rowan cannot connect the two without a receipt, and the post's closing page is missing. He leaves the kitchen count as four and the rota count as three.

Those numbers answer different questions. The rota says how many watches were scheduled. The bowl count says how many portions were taken from the kitchen. Neither can be used alone to infer who was present or whether food went missing. Bram's blank name protects the guard from being added to a list they declined, while still allowing the extra meal to be accounted for.""",
    "hero_legacy_052_record": """Supplemental archive leaf — the signal above the turn

Corra's target board stood above the stones where the road narrowed. One caravan saw the mark before the bend and slowed; another arrived in rain and passed without seeing it. The first team traveled in a dry hour and the second after the light had fallen. Corra recorded the order of arrival and the weather, but the report does not name every driver or describe how fast each cart moved.

The proposed alternative was to widen the road and remove the trees that framed the turn. Corra tested a high board first, then asked both teams to slow at the stone marker. The road was not widened that season. The file does not say whether the trees were protected, whether the budget ran out or whether the test was judged sufficient. Rowan keeps the outcome separate from its unknown cause.

The high mark helped one team and failed another. A future signal plan should be tested in rain and fading light, with a second observer at the approach. Widening might improve sightlines but would change the road and the trees around it. Corra's trial offers a lower-cost comparison; it does not settle which option the caravans should choose or who would maintain a new board.""",
    "hero_legacy_053_record": """Supplemental archive leaf — the spare kept near the gate

Dain's chain inspection shows two hammer marks on one link and a replacement pin made from a different alloy. The guard's report calls the link sabotaged. Dain's measurement card says the marks could come from a repair hammer and gives no test that would distinguish repair from deliberate weakening. He ordered a spare chain kept near the gate while the old one remained in service. The chain later failed at another joint, away from the marked link.

The failure does not prove the first link was harmless. It also does not show that the marked link caused the later break. A workshop note lists a shortage of matching pins, which may explain the different alloy. The note is unsigned and may concern another gate. Rowan attaches it as a possible context rather than a definitive explanation.

The spare chain is recorded in the next inventory, but no handoff receipt says who placed it at the gate. Dain's page helped the crew prepare for a failure without naming a culprit. A later reader can inspect the old link and repeat the measurements. The record should not be used as the sole proof of sabotage or as proof that no one tried to weaken the crossing.""",
    "hero_legacy_054_record": """Supplemental archive leaf — destination without a person

Elsie's desk could record where a parcel was going without requiring a traveler to leave a name. She returned one tag blank and attached a separate tally for weight and destination. The next clerk copied that weight into the nearest household account because the destination was a village. A village name describes a place, not the person who accepted a package there. The parcel may have reached the village; the delivery receipt never returned to Elsie's desk.

The tag was later fastened to a cargo crate with a different color of thread. It is possible the string was replaced after the original broke. The cargo log lists the crate as one parcel, while the gate book contains two weight marks that do not match. Elsie never saw who carried it onward, and Rowan cannot tell whether the discrepancy came from a changed load, a second parcel or a copying error.

The useful part of the record is the route through the gate and the parcel's measured weight at one point. The blank name remains blank. A clerk can ask for a delivery receipt from the destination, but should not infer a recipient from the closest household or turn an anonymous tag into evidence that a particular traveler carried the crate.""",
    "hero_legacy_055_record": """Supplemental archive leaf — samples kept apart

Fenn's three dust samples came from different parts of the same damaged wagon. Pale grit collected against the outer wall, darker sand sat inside the axle cap, and a thin salt line remained on the sheltered scale. The caravan had crossed quarry road and tidal flats, so mixing the samples would have erased a possible difference between the route's surfaces. A trader combined them later to show a buyer that the sacks had been damaged. Fenn's separate papers survived in a tool roll.

No chemical test identified the grains. Fenn compared color, weight and how the dust settled on a wet cloth. The quarry sample clumped; the road sand ran through the weave; the salt left a bright edge after drying. Those observations may help a new survey choose what to test, but they do not date the wagon's passage or tell which wheel crossed each surface first. A route map lists both roads without a signed dispatch.

Rowan restores the sample labels and notes the trader's combined bag as a later display. It may have been honest shorthand for a sale, not an attempt to conceal the route. The evidence can narrow where the wagon traveled. It cannot identify who loaded the sacks or assign every grain to a specific axle.""",
    "hero_legacy_056_record": """Supplemental archive leaf — a waiver under a closure notice

Greer's ledger lists the bridge closure beside the removed crossing fees. One support rope had frayed, so wagons were sent along the ridge road for a week. The complaint that followed called the waiver a gift to one favored caravan, but the ledger shows that every wagon using the ridge had its crossing fee removed. It also lists a foot toll paid by a family carrying goods by hand. The policy treated carts and pedestrians differently, though Greer's margin does not explain why.

The repair request was issued before the fees were waived. A receipt for rope appears two days later, but the bridge reopening date is written in another hand and may refer to a footpath rather than the full wagon span. No complete traffic count survives for the closure. Rowan cannot verify whether every caravan received the same notice or whether anyone paid after the ledger was copied.

Greer's record explains the condition attached to the waiver without settling whether its terms were fair. A later road keeper should compare who received the closure notice, which routes remained open and how the fees were changed. The ledger is evidence of a policy made during rain, not proof that every traveler experienced it equally.""",
    "hero_legacy_057_record": """Supplemental archive leaf — load before measurement

Harlan's wheel changed width between the loaded reading and the one taken after the cart was unloaded and cooled. The road grade and temperature were written beside the figures, but the repair order copied only the smaller value. A replacement rim was requested to fit that number. The wagon did not return for a final test, so the shop cannot show whether the new part matched the cracked wheel under load.

The full salt load was not weighed. A supply sheet estimates it from the number of sacks, but two sack sizes were used during that trip. Harlan marked the larger bags with a charcoal slash; the loading clerk used a different mark. The two records cannot establish the cart's exact weight. Rowan leaves the measurement conditions attached instead of using a guessed load to calculate stress on the rim.

The crack may have grown during the climb, while the cart cooled, or before Harlan inspected it. His note says the crack was visible at the rim; it does not date its first appearance. A future mechanic should measure the wheel at the same temperature, with the load known, then confirm the replacement after a return journey. Until that test exists, the repair remains proposed rather than verified.""",
    "hero_legacy_058_record": """Supplemental archive leaf — the groove under the plank

Iona traced the groove from the tollhouse hatch toward a storage wall before the floor was swept. It narrowed near the wall and ended where a plank later covered the stone. The first clerk thought a handcart made it. Iona measured both ends and marked the route with chalk, but the next work crew found no object beneath the plank. The groove could match a dragged crate, a cart wheel or repeated movement of another kind. Its shape cannot reveal what it carried.

The tollhouse inventory lists two storage boxes moved that month, neither with a measured weight. A delivery receipt records a crate but gives no drawing of its base. Rowan does not join either entry to the floor groove. The timing overlaps, yet overlap is not a chain of custody. The plank may have been placed to protect the stone, hide a trip hazard or cover the mark after the room was repaired.

Iona's chalk marks let another inspector compare the groove's width and direction while it remains visible in the copy. The original floor is now covered. No recovered object or named mover exists in the file. The record can support a question about traffic through the tollhouse; it cannot establish a secret cargo or accusation against a particular clerk.""",
    "hero_legacy_059_record": """Supplemental archive leaf — an escort is not a deadline

Jessa's rota shows the departure party complete before the traveler asked to remain at the wayhouse. She crossed out her own departure time and wrote a wait beside a blank chair in the room plan. The official log later counted her arrival as late. Her note gives no reason for the request, and she did not name the traveler. A second page shows that the wayhouse stove was lit until morning, but it does not say who used the room.

The route steward marked the escort task as unfinished because the party had not moved. Jessa's own ledger describes it as covered: she stayed at the post, kept the road clear and left a message for the next watch. The two records use different definitions of completion. A later clerk copied the late mark from the rota and omitted the wayhouse entry, leaving Jessa's choice to look like a missed duty.

Rowan preserves both pages. An escort may have responsibility for a safe departure and still need to wait when the person being escorted asks for time. The record cannot tell us why the traveler stayed or what they decided by morning. It does show that arrival on schedule was not the only measure of Jessa's work.""",
    "hero_legacy_060_record": """Supplemental archive leaf — the lower listener's place

Kade fitted one bell above the back road after two carts met on a blind descent. He tested it from the road, where the signal arrived clearly, and from the drainage ditch below the bank, where a foot traveler might wait. The second listener heard the ring late. A later survey measured only the road and described the bell as audible across the descent. Kade asked for a lower bell, but no purchase or installation appears in the next inventory.

The drainage ditch carries water after rain and can swallow quiet sounds. Kade's test date was dry, though the slope remained shaded. A footpath map shows a place where someone could step out of the ditch, but the bell's reach was not checked there. Rowan will not assume that another bell would solve the delay; a different location or a visual signal might be more useful, depending on who uses the road.

Kade's first test identifies a blind spot and gives a listener's position. A new trial can compare the ditch, the road and the upper path, then ask carts and pedestrians which warning they can notice. The missing second bell is not evidence that the proposal was rejected. It is a design question left open in the inventory.""",
    "hero_legacy_061_record": """Supplemental archive leaf — volume beside the grip

Lyle's winter comparison used one cup with a cracked rim and a new vessel ordered by the storehouse. The new cup held more water, but its handle was narrower and harder to grasp with stiff fingers. Lyle wrote a volume column and a handling column on separate sides of the page. The order clerk copied the larger capacity and left the handle note on the reverse. The storehouse gained a cup that held more while making it harder for some workers to carry.

The cracked cup was kept, cleaned and marked with a shallow groove at the handle. Lyle's note says it could still be used for comparison, not for drawing drinking water. He never measured whether the cistern level changed between the two tests; the cup comparison tells us about the vessels only. A later report used the difference between cup volumes as an estimate of water loss, though the page does not support that conclusion.

Rowan leaves both measurements with their purpose. The cracked cup is not a standard vessel, and the new one is not automatically the better tool. A future inventory should record capacity and who can use the handle. Lyle's winter record remains a comparison of cups, not a measure of the cistern or the worker's strength.""",
    "hero_legacy_062_record": """Supplemental archive leaf — the jar beneath the hopper

Mina swept kernels that fell through the gap under the grain scale into a separate jar. Some remained whole; others had been crushed under cart wheels and mixed with fine dust. She recorded the jar's weight beside the issued amount, then wrote that the remainder needed inspection before it returned to stock. A later store report added the whole jar to usable grain, making the inventory appear larger without counting what could still be eaten.

The gap was repaired after the next delivery. The repair ticket records a new floor board, but no follow-up weight says how much grain had been recovered. A bird left tracks near the jar, though no note confirms that it ate from it. Rowan does not subtract an invented amount or count the whole jar as food. The record identifies a loss path and a separated remainder; it does not supply a final number.

Mina's scale card shows the grain issued and the material left beneath the hopper as two entries. They should stay separate until someone inspects the kernels. Dust can still add weight while contributing little food. Her page gives a future storekeeper a practical task before pouring anything back into the bins.""",
    "hero_legacy_063_record": """Supplemental archive leaf — two water sources changed

Nolan measured the channel while the upper gate was closed, then repeated the reading after it opened. The line fell over six minutes in the first trial and rose in the second. At the same time, a side ditch carried water into the channel. The public notice described the opened gate as restoring full flow, but the two readings cannot isolate the gate from the ditch. Nolan asked for a separate mark at the ditch mouth before anyone used the result as a single-cause explanation.

The gate's position was marked by chalk on the stone, but rain blurred the lower line before it could be copied. A repair sheet lists the gate as open; it does not state how far the handle turned. Rowan cannot convert the timing into a volume because the channel width is missing. He records when the levels changed and what else was changing at the same time.

Another test can hold the side ditch steady, mark the gate position and measure the channel at the same point before and after. It would still be one trial in one condition. Nolan's account is useful because it shows why the notice exceeds the evidence: several things changed together, so the measured rise cannot prove which one restored the flow.""",
    "hero_legacy_064_record": """Supplemental archive leaf — wait before drawing the sample

Orla placed two jars on the settling-basin ledge, one from each side. The first looked clear from above. When she set it against a strip of dark glass, fine silt remained in motion near the bottom. She waited before pouring either jar into the filter test and wrote the settling time on a separate card. The public sheet preserved only the clearer-looking sample and omitted how long it had stood.

The second jar held larger particles that settled quickly. That did not make the sample cleaner; it only made the change easier to see. Orla's notes describe appearance and movement, not the safety of the water. The filter test itself was not completed because the paper seal tore. A later summary still calls the first jar clean. Rowan attaches the torn seal note beside the settling times so the record does not claim a completed test.

The samples show that water can look different after waiting. They do not certify quality, identify a source of contamination or establish which side of the basin is safe. A repeat would require matched jars, a recorded wait and a working filter test. Orla's main observation is about timing: a first glance and a later reading are not interchangeable.""",
    "hero_legacy_065_record": """Supplemental archive leaf — halfway was a mark, not a setting

Piers cut a shallow notch between the valve's open and closed stops after the handle jumped under pressure. The mark let an operator notice where the valve had slipped during a repair test. The maintenance sheet called it an obstruction and ordered it filed smooth. Piers's sketch instead points to a worn bolt beneath the handle. No one tested the valve after replacing that bolt, so the half-position was never confirmed as a safe or useful flow setting.

The handle carries a scratch at the open stop that may be older than Piers's repair. It is not aligned with the new notch. A later copy uses the notch as though it were an approved measure, even though Piers called it a reference mark. Rowan records the difference between a temporary indicator and an operational instruction. There is no flow reading beside the halfway point.

The next engineer should inspect the bolt, repair the handle and measure the channel at each known setting. Piers's mark can help find where the mechanism failed; it should not tell a farmer how far to open the valve. The archive holds a clue to a slipping handle, not a prescription for the basin's water schedule.""",
    "hero_legacy_066_record": """Supplemental archive leaf — notes beneath the forecast heading

Rhea's cloud page records wind, color and time so the planting group could decide whether to cover its trays. She made no prediction about the following day. A public board copied the observations beneath the heading Tomorrow's Weather, and several gardeners treated that heading as a forecast. The plants were not counted afterward, so Rowan cannot measure what effect the decision had. Rhea's correction says the page described the sky as it was, not as it would be.

One board copy retains the old heading beneath a strip of pasted paper. The strip is dated after the planting group acted, but the person who changed the title did not sign it. The correction may have been made by Rhea or by another keeper following her note. Rowan records the layers of paper and leaves the editor unnamed.

Observations and predictions can share the same weather words while doing different jobs. A gardener may use a cloud reading to choose whether to cover a tray, but should know how uncertain the next day remains. Rhea's page can train someone to look at wind and sky. It cannot tell them that rain will arrive because similar clouds once appeared before it.""",
    "hero_legacy_067_record": """Supplemental archive leaf — frost below the dry step

Stellan marked the first patch of ice above a pipe running from the west wall. After insulation was installed, the frost began lower on the stairs but remained along the wall seam. The nearest step stayed dry, so the maintenance report declared the pipe fixed. Stellan's second drawing shows that the cold had moved rather than disappeared. He asked for the plaster to be opened, but the cellar was closed before that work began.

The pipe carried water; the frost might have come from a leak, a cold bridge in the stone or moisture left by the cellar air. No flow test was made. A repair receipt lists insulation and a replaced joint, yet its date falls between Stellan's two observations. Rowan cannot tell which measure came first from the receipt alone. He notes the sequence as written and leaves the source of the cold unresolved.

The dry step was a useful improvement for people using the stairs, but it did not prove the wall was dry. A future inspection could compare the seam, pipe joint and air temperature before opening the plaster. Stellan's record holds evidence of change after repair; it does not certify the hidden section of wall or establish that the water source was found.""",
    "hero_legacy_068_record": """Supplemental archive leaf — the dotted trench beyond the stone

Talia traced the second outlet from a wet patch near the seed store to a flat stone. Beyond that point, she used a dashed line because the trench was hidden. On a dry day, no water appeared. On a rainy day, the patch returned. A later map extended the dashed line straight to the river, drawing a route nobody had excavated. The direct line is possible, but so are runoff across the courtyard, a blocked pipe or a shallow channel under the store wall.

The building plan marks an old drain near the flat stone, but its outlet is not shown. A mason's note says the drain was filled during a floor repair; the note has no completion signature. Rowan keeps it beside Talia's two weather observations without treating it as confirmation. The rain may have entered through the drain, through soil or through a damaged roof nearby.

The next survey can begin at the flat stone and inspect the old drain before tracing farther. A dry-day reading and a rain-day reading should remain separate. Talia's map is useful because it shows the last place she saw water and the first place she did not. The dotted section means the route is not yet observed.""",
    "hero_legacy_069_record": """Supplemental archive leaf — a bucket without a fill mark

Ulna's receipt records who carried water to the upper bed and where it was delivered. The volume field is blank because the bucket had no fill line. A supervisor wrote in the household's usual amount and treated it as measured. Ulna crossed the estimate out and returned the paper unsigned. The crop survived the dry week, but no one recorded how many trips the carrier made or how full the bucket was each time.

The bucket itself has a dark ring near the handle, but the mark may be wear rather than a waterline. A kitchen vessel with the same shape holds a different amount because its base is thicker. Rowan refuses to use that cup as a substitute standard. A later ledger copied the supervisor's figure into the ration total, spreading an estimate through several pages without preserving where it began.

The missing volume cannot be recovered from the surviving receipt. A future carrier can use a marked vessel and record each trip, while leaving the old field blank. Ulna's correction does not deny that water reached the bed. It prevents a familiar household estimate from being presented as a measured quantity.""",
    "hero_legacy_070_record": """Supplemental archive leaf — equal measures, equal cooling

Vesper tested grain from two cooling pans, but the first portions were not weighed equally. One pan came off the kiln while its rim still glowed; the other waited until it had cooled. The grain from the second trial cracked less, though it may also have been a smaller sample. Vesper asked for a repeat with matched measures and the same grain lot. A later recipe retained the cooling interval while dropping the request for equal weight.

The two pans were made from different clay. One was thicker at the base and could hold heat longer after leaving the fire. Vesper noted the difference on a workshop sketch, but the recipe copy records only the pan shape. Rowan cannot isolate the effect of cooling time from the material, thickness or sample size. The method may still be promising, but the first comparison is not enough to call it proven.

The next test should weigh both portions, use the same grain lot and record the pan material. It should also count cracked kernels after the same cooling period. Vesper's note is valuable because it asks for conditions that the recipe later omits. The archive keeps the question open so a useful technique does not harden into a rule before it has been compared fairly.""",
    "hero_legacy_071_record": """Supplemental archive leaf — the barrel that no longer fit

Wynn's counterweight balanced the storehouse door when it moved freely. A sack placed against the frame stopped the door from returning to the same point, so Wynn measured the collision mark and shortened the pull rope. The new limit reduced the swing and kept the iron weight from striking the wall. It also narrowed the opening so the widest barrel could no longer pass through without being turned sideways.

The later plan lists the door as repaired and omits the barrel restriction. A store list records that one barrel was moved through the south entrance, but does not say whether that was a direct consequence of Wynn's change. Rowan preserves the tradeoff beside the repair: a safer stopping point and a narrower passage. There is no second measurement showing whether a lighter counterweight could have kept the full opening.

Wynn's repair addressed one hazard. It did not solve every use of the door. A future builder can test a different counterweight and inspect the frame under load, but should keep the old collision mark as a reference. Calling the system fully repaired hides the cost of its new limit; calling it a failure ignores the reduced swing. The record describes both.""",
    "hero_legacy_072_record": """Supplemental archive leaf — the faded upper lime

Xena marked the damp wall with two lime lines before the masons painted it. The upper line faded first, while the lower remained visible. A repair ticket blamed poor paint. Xena's note records that the upper stones received more sun and that the room was aired each afternoon. She did not open the wall to search for a pipe, and the next rain arrived before she could repeat the test under the same conditions.

The masons replaced the paint before the rain and sealed one crack near the sill. A receipt confirms the work but does not identify which repair was intended to address moisture. The wall stayed pale for several days. That outcome may reflect paint, sunlight, airflow or a change in dampness. Rowan keeps the receipt and the lime marks together without calling the wall dry.

The useful next step is to repeat the markings after the paint has set, note sunlight and airflow, and inspect for new moisture after rain. Xena's page locates the difference between two heights. It cannot say where water entered or whether the crack carried it. The faded mark is an observation that invites another check, not a diagnosis of the hidden wall.""",
    "hero_legacy_073_record": """Supplemental archive leaf — the pencil list before the ink

Yestin's pencil roster was made while the night drill was still being proposed. Three spaces beside the shifts remained blank, and the margin says the cadets had not chosen a schedule. The later ink copy includes three names on a second page signed after the drill took place. The names could record who attended, who was assigned afterward or whose signature was gathered later. The two documents do not explain the transition.

The drill was completed, but the shift report names only the instructor and the gate. No roll call survives for every turn. Rowan cannot say whether the cadets volunteered, were ordered or traded shifts among themselves. He leaves the pencil blanks visible next to the later signatures so the date of each decision can be reconsidered if another roster appears.

Yestin's page does not prove that the ink signatures were false. It shows that the schedule remained open when the first list was written. A blank box may mean undecided, unfilled or simply not recorded. Without a later statement from each cadet, it cannot be turned into consent or refusal. The roster preserves the change between proposal and practice without assigning intent to the people named.""",
    "hero_legacy_074_record": """Supplemental archive leaf — the cloak returned to common laundry

Zola found the cloak on an empty cot with a repair tag but no owner's name. The tag gives the date a torn sleeve was mended. A clerk added the initials of the nearest cadet, then removed them after Zola asked who had authorized the change. The initials remain faintly visible beneath the erasure. They are not a reliable identification, but they show how quickly proximity became a claim of ownership.

The cloak went to the common laundry. A laundry list notes one dark wool garment and a missing brass button, but no mark matches it to the cot. No reclaim receipt survives. Rowan cannot tell whether the owner returned, moved to another barracks or chose to leave the cloak behind. The empty cot and the unclaimed garment are separate facts; joining them does not identify the person who slept there.

Zola's inventory protects the record of the object without inventing a name. The repair date may help someone recognize the cloak if a family later asks about it. Until then, the common store can hold it for a fixed period and document what happens next. A blank name field should stay blank when the evidence is only a nearby bed.""",
    "hero_legacy_075_record": """Supplemental archive leaf — the route drawn below the bench

Ansel's map lesson took place in a hall where a reader had to stand on a bench to reach the top board. He drew a second route at seated height and marked the turn in chalk beneath the bench. A cadet with a sprained ankle followed those marks without climbing. Ansel did not give the student's name; the class note says only that the low route was used during the lesson. The instructor's copy later preserved the raised board alone.

The chalk line was washed away before the next class. Ansel's sketch records where it turned, but not its exact length. A maintenance note says the bench moved to the north wall, so a future teacher could not simply repeat the same placement. Rowan keeps the map's height and the room arrangement together. The low route can be redrawn, though its old marks cannot be restored exactly.

The adapted lesson became part of the official curriculum without the alternate route. Ansel's page proves the second method existed before that copy; it does not show why it was left out or whether later classes still used it. A map can be legible from more than one height. Ansel recorded that practical fact before the training office had a category for it.""",
    "hero_legacy_076_record": """Supplemental archive leaf — two return stamps

Blythe kept the envelope after it came back the first time without a reason marked. The second return added a routing stamp and a clearer address. The final address is legible, but no receipt shows that the recipient saw the letter. The office log records the last return only and dates the failure to the sender. Blythe's copy contains both stamps, which show that the envelope traveled through at least two desks before being called undeliverable.

The envelope's seal is unbroken in the archive. That does not prove it was never opened; the flap may have been resealed before Blythe received it. A small notch on the side could be a filing cut or damage from a packet string. Rowan records the condition but does not call it evidence of tampering. The routing stamps identify office movement, not the reason the recipient did not answer.

A later clerk could ask the recipient or their family whether the address was correct, if contact remains welcome. The archive does not authorize a conclusion about refusal or delivery. Blythe's pages help identify which offices handled the letter and where the route changed. They cannot speak for the person waiting at the final address.""",
    "hero_legacy_077_record": """Supplemental archive leaf — a training bend and a campaign portrait

Caris replaced one rivet on the cadet buckler and returned it to the practice rack. Her note identifies a wooden blade and a supervised sparring exercise as the source of the bend. The armour ledger calls the shield battle-damaged. Years later, a portrait places a shield with the same repair beside a campaign banner. Its rim and rivet appear similar, but no inventory ties the portrait's object to Caris's practice buckler.

The rivet size is recorded clearly enough for another armourer to make a matching repair. The shield was not discarded after it bent, and the practice rack entry says it could be used again. The portrait may show the same buckler later carried into battle, or a different shield repaired in the same way. Rowan leaves both possibilities open rather than turn a resemblance into a personal history.

The difference between the training note and the campaign label matters because it changes how the damage is understood. Caris's record preserves the event she witnessed and the work she performed. It does not settle the later item's journey. If the shield returns to the archive, its marks can be compared with the repair record before anyone assigns it a battle.""",
    "hero_legacy_078_record": """Supplemental archive leaf — the latch in glare

Doran's gate drill moved from the southern latch to the shaded wall after the first group opened the gate correctly and the second waited for a lantern in full daylight. The practice mark had been painted on the sun-facing stone, where its outline disappeared at noon. Doran moved the marker and asked cadets to repeat the steps without a spoken cue. The roster says the drill was completed, but it does not say which observers watched or whether each recruit could see the latch from the approach.

A later gate plan restores the mark to the southern wall, probably because the new paint matched the older diagram. The plan gives no light condition. Rowan cannot say whether the cadets trained there again or whether the change was reversed for another reason. The drill demonstrates that the sign was hard to see in glare; it does not show that moving it permanently improved every approach.

An accessible route should be checked at the hour people use it, from their side of the door. Doran's note also shows that a practice can be completed on paper while leaving some observers unknown. A future officer can repeat the no-cue drill and record who saw the mark. The old roster should not be used as proof that every recruit understood the gate.""",
    "hero_legacy_079_record": """Supplemental archive leaf — the vacant bed and the open docket

Eira's morning count found one empty cot. The first roster marked its occupant absent; Eira left the status box blank because a transfer docket had been issued without a return date. The destination is clear in the docket, but the receiving office has no arrival receipt. A later copy marks the cadet missing. That status may reflect a separate search, yet no search notice is attached to the page.

The cot was stripped after the next inspection. A blanket ticket lists a repair, not a transfer of the blanket to another bed. The clothing inventory has no name beside it. Rowan keeps the physical count of one vacant space distinct from the unresolved status of the person. A bed can be empty because its occupant is away, transferred, hospitalized, on leave or missing; this file does not decide among those possibilities.

The docket gives the family a destination to ask about. It does not prove that the cadet arrived there. Eira's blank field preserves an interval between dispatch and receipt. A future clerk can add a confirmed response without erasing the earlier uncertainty. The empty cot is a fact about the barracks on one morning, not a verdict on someone's fate.""",
    "hero_legacy_080_record": """Supplemental archive leaf — pale thread at the break

Ferris repaired the transfer register with pale thread across the torn list and dark thread around the missing corner. The different colors show where the paper survived and where its edge was gone. Two lines meet near the tear but do not align. A clerk copied them as one sentence, making a destination appear attached to a name that may have belonged to the next line. Ferris's repair allows the sheet to flatten without hiding the gap.

The thread is waxed on one side and rough on the other. Ferris wrote that the page should be turned slowly so the stitching did not catch. A later binder mounted it behind glass, preventing another reader from checking the reverse. Rowan records the visible text and the conservation note but does not infer the missing words from the order of nearby transfers.

The original wording may never return. Ferris's repair preserves the shape of the evidence instead of restoring a sentence that reads more smoothly. The register can still show that two lines were present and that the paper tore between them. That is enough to request a corrected copy from another office, if one survives. It is not enough to identify which cadet went to which destination.""",
    "hero_legacy_081_record": """Supplemental archive leaf — restore the caller's place

Harlan's whistle card lists two tones and two caller positions. The first tone carried past the north wall but faded by the barracks door. The second sounded louder near the caller and disappeared from the same doorway. Harlan moved to the open arch and repeated both signals before changing the whistle. At the arch, the second tone carried farther. The official recommendation kept the higher pitch but omitted the relocation, making the instrument seem responsible for a difference the caller's position may have caused.

The courtyard plan shows the arch was open during the later test. It does not describe whether the barracks door remained open. A note written beside the signal says that a passing cart interrupted one reading. Rowan leaves that entry as an obstruction, not as proof the tone failed. The card does not identify which cadets were within hearing range or whether the drill was meant for everyone in the yard.

The test can be repeated only if the caller and listener return to the marked places. Harlan wrote both on the same line as the pitch. A future signal plan should preserve the location instead of copying only the preferred tone. The drill card measures a sound in a courtyard; it is not a permanent order for every gate or weather condition.""",
    "hero_legacy_082_record": """Supplemental archive leaf — the hinge beside magnetic iron

Ina's compass held steady outside the eastern gate, then pulled toward the hinge once she crossed the threshold. She traced two iron plates around the doorway and marked their position on the map. A later copy used the second bearing as true north and rotated the practice route. Ina's note says to check the compass outside before drawing the line. The plate may have affected the needle, but the gate was never dismantled and no second instrument tested the same direction.

The old map includes one route through the gate and another along the outer wall. Their distances were paced by different cadets. Ina's measurements do not show that the inner path is shorter; they show only how the needle behaved at each point. Rowan keeps the practice route separate from the compass readings so that the drawn line does not inherit an unverified direction.

A future survey could compare two compasses at the threshold and inspect the iron plates without removing them. If the needle still pulls, the map should note the local deviation rather than redraw the whole world around it. Ina's page helps a cadet know where the instrument becomes unreliable. It cannot identify which part of the gate caused the change or establish a universal north line.""",
    "hero_legacy_083_record": """Supplemental archive leaf — the number on the brass back

Joryn found the badge beneath an unused bunk. The paper face had been scraped clean, but the brass back carried a cadet number. A transfer list had two people with similar initials, and Joryn declined to choose between them. The badge was returned to the quartermaster with a receipt for one tag, no name. A later inventory copied the closest initials into the description. Rowan leaves that addition out of the transcription and notes that it was made after the object was returned.

The scrape marks run in two directions. They could come from a tool, a rough surface or repeated handling. No name survives under the paper face, and the badge's number does not match a complete year of rosters. The cadet number may have been reused, or the record may be incomplete. The archive cannot tell which.

Joryn's blank field is not an invitation to guess. If a family later brings another badge or transfer receipt, the number can be compared. Until then, the brass object remains a returned tag with an unknown wearer. A nearby bunk and similar initials do not combine into an identity.""",
    "hero_legacy_084_record": """Supplemental archive leaf — a lower rack within view

Kira moved one section of the training rack lower after a cadet with an injured wrist struggled to return a practice blade. The quartermaster worried that the low shelf would be mistaken for the public store. Kira painted a border around the training section and checked whether it was visible from the door. The audit records one practice blade in that rack but does not identify the user who needed it. The change improved access without requiring the person to ask the quartermaster each time.

The border was painted in pale red, which matched a stripe on the public store boxes. A later inventory described the low rack as a reserve. It is unclear whether the writer saw the border or followed an older shelving plan. Rowan keeps Kira's door-view sketch attached to the rack note, so a future keeper can inspect the distinction before moving the blades.

Lower storage changes who can reach a tool and how much floor space remains clear. Kira did not claim the arrangement was best for every weapon. Her record asks the next armorer to test it from the doorway and ensure training gear is not confused with issued steel. The user's name stays private, while the design problem remains visible.""",
    "hero_legacy_085_record": """Supplemental archive leaf — the beat that could stop

Lorne's first note sheet marks the drum pattern as a practice cue. It helps cadets keep a shared pace across the inner yard, but his copy gives the drummer permission to stop if the group loses rhythm. A later night schedule uses the same beats to order formation and removes the stopping line. The rhythm may have been convenient for both purposes; the documents do not show who authorized the change from cue to order.

The yard stones make one beat ring longer near the eastern wall. Lorne marked that echo and advised the drummer to stand near the open center, where the pace was easier to hear. The field-march report lists the cadence but gives no location or weather. No record confirms that the pattern was used beyond the practice yard.

Rowan preserves the line that lets the drummer stop. A tool for coordination and an order with no pause are different uses, even when the sound is identical. A future instructor can test the cadence with the group and ask whether it remains useful. The sheet does not prove the march went well or badly; it shows a boundary the schedule later omitted.""",
    "hero_legacy_086_record": """Supplemental archive leaf — two counts at two hours

Maelin's slate shows the first total below the words east stair and the second below dawn. The first counted people who had reached the stair. The later count recorded those still present after the night had passed. Maelin left the earlier chalk visible beneath a pale wash instead of erasing it. A town summary chose the larger number and described everyone as accounted for, though Maelin's margin says the stair was not checked after the last bell.

The slate has a third line for people carrying water, but no count beside it. Some may have crossed twice. The gate record lists trips, while the shelter record lists people staying; neither is a direct list of unique residents. Rowan cannot combine these sources into a final survivor total without a list of names or a method for removing repeat crossings.

Maelin's two numbers are not rival answers to the same question. One records arrivals at a point, the other presence at a later hour. The chalk beneath the wash makes the time difference visible. The archive keeps both and leaves the final total open, so a larger number is not mistaken for a more complete account.""",
    "hero_legacy_087_record": """Supplemental archive leaf — scrape height and force direction

Oren measured the scrape on both faces of the shelter door bar because the first report did not say which side had been pushed. The marks differ by less than a finger. One could have come from lifting the bar from inside, the other from a strike outside, or both could be parts of the same movement. Oren's note refuses to choose a direction from two nearly matching scratches.

A witness remembered a sound from the shelter but could not say whether it was the bar, the hinge or something falling within the room. The witness did not sign the report. A later clerk attached a name from the night roster, though the roster contains no note that the person was present at the door. Rowan keeps the testimony and the roster separate.

The shelter was found open. That is the confirmed condition. Oren's measurements help another inspector compare both sides of the bar, but they cannot identify who moved it, when it was lifted or why. The report can support a repair and a new closure test. It cannot make a scrape into an accusation.""",
    "hero_legacy_088_record": """Supplemental archive leaf — the missing evening handoff

Piper's blanket carries two dated repairs: a lower-edge patch and a strip sewn over the seam that pulled away from a cot frame. Between them, the shelter handoff list is missing one evening. The inventory calls the blanket usable, but that description does not show who slept beneath it or whether the second tear appeared during use. Piper returned the cloth to the shelter after each repair and did not mark a household name on the hem.

The blanket was washed at least once between repairs. A laundry ticket lists one wool cover but not its color. A later story says it passed among three families. The repair dates allow that to be possible, yet no handoff page confirms the sequence. Rowan does not use the number of patches to count the people who used it.

Piper's work records an object shared through a cold week, not a roster of the shelter. A future quartermaster could add a sign-out card if users want one and if their privacy is protected. The missing evening should remain visible until another receipt turns up. A blanket can be in usable condition while its history remains incomplete.""",
    "hero_legacy_089_record": """Supplemental archive leaf — the lower room in rain

Quinley's bell test reached the well-shelter entrance while rain struck the roof. A listener in the lower stone room heard nothing at that time. After the rain passed, one person on the stairs heard a ring. The door position and listener's place are recorded, but the roof's condition is not. A later report calls the test a clear success, using the stair reading and leaving out the first trial.

The bell may serve people near the entrance and fail in the lower room during heavy rain. Quinley asked for a second method near the bottom of the stair, but no plan shows that one was installed. The shelter's stone walls could carry sound differently when damp; the archive contains no test of that possibility. Rowan leaves the two results beside the weather note.

A future signal test can repeat the ring in rain and in dry weather from the entrance, stairs and lower room. It should include a visual cue or another way to call for help if sound does not reach the shelter. Quinley's record does not prove the bell useless. It prevents the word success from concealing where the sound was not heard.""",
    "hero_legacy_090_record": """Supplemental archive leaf — count the boots, not the travelers

Riven found three pairs by the hearth after a group left through the west path. One pair was small; another had a repaired heel that matched no mark in the shelter ledger. The third pair was wet inside. Riven counted the footwear and left the number of travelers blank. A later tale says three villagers escaped because three pairs remained. That statement assumes one pair per person and that no one returned for them.

The west-path gate record shows movement during the night but does not identify how many people crossed. A shelter list includes visitors who were not local, though it may have been copied from a meal count. The boots could belong to people who shared a pair, to travelers or to anyone who had gone barefoot during the fire. Rowan keeps these records adjacent without joining them.

Riven's note preserves three objects that survived the fire and the fact that they were left by the hearth. It cannot tell who wore them or whether their owners escaped. A family searching for footwear could compare repair marks, but the archive will not turn a count of objects into a count of lives.""",
    "hero_legacy_091_record": """Supplemental archive leaf — rope length is not water depth

Sybil shortened the well rope after a frayed section was removed. She measured the water depth before tying the new knot and recorded where the bucket stopped afterward. The public card kept the new rope length but not the depth. A later reader used the shorter rope to claim the well had fallen. Sybil warned that the bucket might touch bottom when water was low, but no second depth reading followed the repair.

The old rope had stretched near its wet end. Sybil marked the worn fibers and kept a short piece beside the measurement. The bucket's stop point depended on the knot and how much slack was let out; the card does not record the operator's hand position. Rowan therefore keeps the rope length, knot and depth as separate observations.

A future keeper can lower a marked line and measure the water directly, then compare the bucket stop with the same knot and method. Sybil's record helps choose a safe test. It cannot establish whether the well rose or fell between two dates, because the second depth was never taken.""",
    "hero_legacy_092_record": """Supplemental archive leaf — the two sides of the sill

Tavian gathered ash from both sides of a shelter window after the fire. The inner ledge held pale gray dust from a roof collapse; the outer ledge carried darker flecks blown from the south. He stored them in separate paper folds and drew the wind direction on the frame backing. A public report lists one sample from the house and says the roof fell after the fire began. Tavian's note says the roof had already dropped before the second sweep.

The report does not show which sample was tested or whether the folds were kept sealed. The inner ash may have come from the roof, but no timber fragment is attached. The outer flecks could have blown in from another building. Rowan preserves the two deposits without naming a starting point for the fire.

The samples can tell a future investigator that material reached both sides of the sill under different conditions. They cannot establish where ignition occurred, what burned first or who was present. Tavian's wind arrow helps interpret the deposits but does not replace a complete timeline. The archive's useful result is two samples instead of one mixed handful.""",
    "hero_legacy_093_record": """Supplemental archive leaf — room for a correction plate

Ulla's first memorial design used a fixed number of stones. She left a gap at each turn so families could add a correction plate after confirming a spelling. The mason worried that the empty spaces would make the path look unfinished. Ulla answered that a wrong name cut into stone would be harder to repair than a blank. Several plates were added over time, but the request slips do not identify who asked for each one.

The path contains one plate whose letters were recut. The older grooves remain visible beneath the new strokes. No receipt shows who approved the change, and the family file is sealed. Rowan lists the plate as revised without copying the earlier spelling into a public index. A correction can serve the people connected to the name without turning the mistake into another permanent display.

Ulla's layout allows a verified name to be added later. It cannot recover the spelling of someone whose family or records are missing. The blank spaces are not proof that a person was forgotten or that no one searched. They preserve room for a future correction while refusing to carve a guess into the memorial.""",
    "hero_legacy_094_record": """Supplemental archive leaf — arrivals, crossings and repeats

Virgil's first tally was taken before sunrise and included people sleeping near the east gate. The second followed the warning bell and included travelers arriving after the road reopened. Some people crossed twice to carry water. Virgil wrote the hour beside each number but took no names, so a single person could appear in both counts and several crossings could appear as separate marks.

The town summary merged the columns into one large crowd. Its total may be useful for estimating how busy the gate was, but it does not count unique people. A water carrier's note lists trips and buckets, not names. Rowan refuses to remove an assumed number of repeats because the documents do not show which entries belong to the same person.

Virgil's record can be repeated with separate columns for people present, arrivals and crossings. A future count might ask for names only when needed and with permission, or use another method to avoid duplicate entries. His two totals remain valid for their different hours. The summary's single number answers no clear question about population.""",
    "hero_legacy_095_record": """Supplemental archive leaf — pages moved by the wind

Wren found the paper roll after a roof repair let wind into the shelter desk. One sheet landed in the courtyard; another caught beneath a beam. Wren pinned them down and asked two witnesses to confirm their order before reading. A clerk later filed the sheets as one list. The ink on the underside is faint, and some names are uncertain, so page order alone cannot establish the sequence in which entries were written.

The witnesses agreed that both sheets came from the same roll but disagreed about which had been on top. One remembered the corner torn before the wind; the other saw the pages after they landed. Neither signed the final copy. Rowan keeps their statements separate and does not use the physical position of the papers as a tie-breaker.

The list may still help families search if the uncertain letters remain marked. Wren's instruction is to compare the page with another source, not to infer order from where the wind left it. The event moved the papers before any person did; that does not mean the papers are meaningless, only that their arrangement is not a reliable chronology.""",
    "hero_legacy_096_record": """Supplemental archive leaf — chalk composition beside the water line

Xavia's wall has three marks. The lowest came from a damp boot; the middle was traced beside a bucket carried through the room; the highest remained after the floor had dried. A later report called them three flood levels. Xavia's card labels only one as water and asks the next keeper to check the chalk composition before treating the rest as a stain. No sample was taken for a laboratory test.

The bucket line may be a drip, a smear or a mark left when the pail turned. The boot impression may have come from water tracked in after the cellar flooded. Xavia drew the wall's position relative to the stair and noted which marks could be touched by hand. These observations narrow where to inspect; they do not provide a historical water depth.

Rowan preserves each mark with its source field as written. A future test can apply the same chalk to dry and damp stone and compare how it fades. It cannot retroactively assign all three lines to the flood. The wall remembers where marks were made, but it does not remember their causes for us.""",
    "hero_legacy_097_record": """Supplemental archive leaf — the unnamed chair near the door

Ysra moved one chair from the center of the meeting plan to a place close to the exit. The official layout put the speaker in the middle and left the door behind them. Ysra's version kept the speaker visible while allowing someone at the end to leave without crossing the room. The minutes record one early departure but do not say whether that person sat in the unnamed chair or why they left.

The door was kept unlatched during the meeting. A clerk's note says the draft minutes were paused while a guest stepped outside, then resumed when they returned. It does not name the guest or state whether the discussion changed. Rowan keeps the chair plan and the pause together without claiming that the room felt safe to everyone present.

Ysra's design makes leaving physically possible and does not demand an explanation. It cannot tell a later reader what each family thought or whether anyone felt able to speak. The minutes that follow should record a pause as a pause, not translate it into agreement. The unnamed seat remains part of the plan because a room can offer choice without identifying who used it.""",
    "hero_legacy_098_record": """Supplemental archive leaf — first repair, then the mural

Zander returned his sword to the repair rack after the duel. Its guard needed a new rivet and the wet grip had begun to slip. The feast plan had a place for the blade, but Zander's card lists a smith and the materials needed to make it usable again. A painter copied the sword's shape into the victory mural before that repair was complete. The image may have helped people remember the duel; it does not show the condition of the weapon or the work required to carry it.

The smith's receipt records a replacement guard and a new wrap that could be tightened after rain. No battle report says whether Zander carried the repaired blade again. Rowan leaves the portrait and the maintenance card as separate records. A victory image can preserve a public story while a repair sheet preserves the labor that followed it.

The sword became a symbol after the mural was painted, but the archive begins with a loose grip and a missing rivet. Zander did not place the weapon on the feast table that night. That choice does not prove he rejected the celebration or disliked the title given to him. It shows where he sent the blade when it needed care.""",
    "hero_legacy_099_record": """Supplemental archive leaf — answer before the first morning ring

Zadie's note tied to the bell rope asks the next keeper to answer before ringing. The night roster gives her the final hour but leaves the first morning shift unnamed. The dawn log records one bell at first light and a second response several minutes later. It does not say whether Zadie rang both, whether the morning keeper arrived between them or whether one sound came from another tower.

The response interval was not entered in the public schedule. A later copy calls the two rings a sequence, though the original log uses separate lines. The tower repair sheet mentions that the eastern rope had been temporarily joined, which may have affected how quickly it returned. Rowan does not use that detail to attribute either ring to a particular person.

The bell's note remains a request for a handoff. A future watch can record who received the rope and when, if the keepers agree to be named. The interval between the rings can be measured without guessing who made them. Zadie preserved the gap so a new shift would not begin as an order without an answer.""",
}


def main():
    path = CONTENT / "codex_catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    for record_id, supplemental in SUPPLEMENTS.items():
        record = entries.get(record_id)
        if record is None:
            raise KeyError(f"Missing Hundredth Roll record: {record_id}")
        if MARKER not in record["body"]:
            record["body"] += "\n\n" + supplemental
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(SUPPLEMENTS)} already-unlocked Hundredth Roll records.")


if __name__ == "__main__":
    main()
