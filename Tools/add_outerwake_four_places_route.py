#!/usr/bin/env python3
"""Install Jace Morrow's post-report Outer-Wake route and its authored field archive."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, data):
    (CONTENT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


records = [
    {
        "key": "open", "title": "Four Places Left Unassigned", "kind": "talk", "target": "jace_morrow",
        "objective": "Meet Jace beside the returned survey case. Ask him to separate the equipment record from the names he cannot verify.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "A Case Returned without a Roster",
        "lines": [
            "The case came back with four fitted sleeves and no index card. I wrote 'four places' because that is what the rack holds, not because I know four people left in it.",
            "I am not going to fill the gaps with a story that makes my report feel finished. Help me describe the case, the tests we can repeat and the names I still cannot supply."
        ],
        "body": "After Evelyn accepted the Outer-Wake report, a sealed instrument case arrived from the receiving desk. Jace recognizes the brass catches and the padded frame, but the index card that should link each sleeve to a surveyor is missing. Four long spaces remain inside. The first copy of his old report called them crew slots; a later copy shortened the phrase to crew. Neither wording proves who carried the instruments, whether the sleeves travelled together or whether every place was occupied during the final departure.\n\nJace asks Rowan to begin with the object itself. He is careful about the distinction because he has already seen how a plausible summary can become a fact after two or three rounds of copying. The case can be measured. Its hinges can be tested. The missing card can be recorded as missing. None of those observations supplies the absent names.\n\nThe case also brings Jace back to a choice he has avoided since writing his first report. He wants another person to check the instruments, but he does not want a new reader to mistake the empty sleeves for proof that their owners died, escaped, or reached a known refuge. He asks Rowan to help him make a record that admits the limit in its first paragraph. If the old expedition remains unresolved at the end, the new page must be allowed to say so plainly."
    },
    {
        "key": "case", "title": "The Four Padded Sleeves", "kind": "inspect", "target": "jace_four_places_case",
        "objective": "Inspect each fitted sleeve, hinge and empty label window. Record the case's present condition without assigning an owner.",
        "speaker": "ROWAN HALE", "giver": "rowan_hale", "codex_title": "Four Compartments, No Four Names",
        "visual": "sealed_case", "position": (-9.4, 4.35), "display": "Returned Survey Case",
        "lines": [
            "The lining was cut to hold four instruments, but the label windows are empty and the foam has been replaced at different times.",
            "I can draw the sleeves as they are now. I cannot draw a person into a space just because the case was built for one."
        ],
        "body": "The returned case contains four padded sleeves, two sizes of retaining strap and a narrow channel where a paper index card could have been kept. The foam in the first sleeve is darkened at the edge; the third has a newer patch stitched with pale thread. Rowan notes both details and turns the case under the lamp to find a date stamp. The stamp is a maker's mark from a repair shop, not a survey date.\n\nThere are no initials in the label windows. One blank has a faint rectangle where a paper tag may once have rested. The rectangle could be the mark of a removed label, but the case has been handled by several archive keepers since it returned. Jace remembers the old report listing four instruments. He does not remember who had each one, and the report copy does not name a keeper beside the list.\n\nThe case is evidence of capacity: four tools could be carried in it at once. It is not a census of the people who travelled. The archive entry therefore lists the dimensions of the sleeves, the state of the straps and the repair marks, then leaves the owner column empty. This makes the case useful for a later physical comparison without turning an empty label into a missing-person conclusion."
    },
    {
        "key": "skyroot", "title": "Skyroot at the Same Mark", "kind": "grow", "target": "skyroot",
        "objective": "Grow one Skyroot at the Outer-Wake garden bed. Mark its water depth before comparing the new root with the old packing fiber.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "A Living Fiber Is Not an Old Packing",
        "lines": [
            "The packing fiber has been stored dry for years. A living Skyroot will bend differently, so we need a present sample before judging the old sleeve lining.",
            "Write down how deep the bed was watered. The comparison only means something if the growing conditions stay beside it."
        ],
        "body": "A strand caught beneath the case hinge resembles Skyroot fiber, but its color has faded and its surface is flattened. Jace will not call it packing from the old expedition until Rowan has a living sample for comparison. The Outer-Wake bed can grow Skyroot again, so the team records the planting date, seed source and water depth. When the plant reaches harvest, they compare flexibility, split lines and the way each strand holds dust.\n\nThe live stem springs back after a shallow bend. The old fiber stays folded. That difference may result from age, dryness, pressure inside the case or a different material. The sample cannot tell the team which explanation is right. It gives them a repeatable comparison under one present-day condition. If a later keeper repeats the test with a different water depth, both outcomes can be kept rather than averaged into a single answer.\n\nJace admits that he once wrote 'Skyroot packing' in a margin without collecting a second sample. The phrase entered a copied inventory, where it lost the question mark he had pencilled beside it. Rowan records the earlier wording as an unverified label and keeps the new growth separate from the archived strand. The garden has supplied a reference, not a time machine. Nothing in the root identifies a person, proves how long the case travelled or tells the team what happened after the survey stopped."
    },
    {
        "key": "carp", "title": "A Carp from the Pool Below", "kind": "fish", "target": "farwake_carp",
        "objective": "Catch one Farwake Carp at Celestial Pool. Record the waterline, bait and catch time as present-day conditions for the listening rig.",
        "speaker": "LYRA MOSS", "giver": "lyra_moss", "codex_title": "The Pool's Present Noise",
        "lines": [
            "The old report calls the pool quiet. That word leaves out the water height, the wind and where the listener stood.",
            "Catch a current sample and give me the conditions with it. I can test the hall today without pretending today's fish remembers the old expedition."
        ],
        "body": "Celestial Pool sits beneath the receiver platform, where the water touches the archive foundation. A Farwake Carp caught there is not a witness to the expedition. It is a living sample from the pool as it exists now. Lyra asks Rowan to record the bait, catch time and visible waterline before moving the fish to the comparison basin. A note that only says 'quiet' cannot be repeated; a note with conditions gives another listener a chance to try the same setup.\n\nThe pool carries a low vibration when the wind comes through the west aperture. On the afternoon of the catch, the note grows rougher after a maintenance gate is opened. The fish turns toward the deeper wall, though nobody claims to know whether the sound, shadow or current caused the turn. Lyra keeps the observation beside the measurement instead of choosing one cause.\n\nJace's old report says the surveyors heard a low interval before the receiver went silent. It does not say that a fish made the sound or that the pool was at the same level. The current catch helps the team isolate one local condition. It cannot verify the old sound or identify the source of any message. The record's narrow claim is enough: a present-day observer can repeat the catch and listen again at a marked waterline."
    },
    {
        "key": "wind", "title": "Three Heights on the Wind Mast", "kind": "inspect", "target": "jace_four_places_wind",
        "objective": "Inspect the wind mast at ground, platform and upper rail height. Keep all three readings instead of choosing one as the expedition's weather.",
        "speaker": "ROWAN HALE", "giver": "rowan_hale", "codex_title": "The Wind Changed with the Listener",
        "visual": "pressure_gauge", "position": (-6.8, 4.5), "display": "Three-Height Wind Card",
        "lines": [
            "The vane turns a little farther above the platform. The gauge at ground level hardly moves.",
            "I will keep all three readings with their heights. One number would hide the difference we came here to measure."
        ],
        "body": "The mast has three sockets where a hand gauge can be fixed: ground level, the observation platform and the upper rail. Rowan reads each one within a minute, using the same instrument and noting the direction of the vane. The upper reading is stronger. A second pass after the sun drops is weaker at all three heights, but the gap between them remains. The instruments were not available to Jace's old team in exactly this arrangement, so the new card is a repeatable test of the archive, not a reconstruction of their night.\n\nOne copied report gives a single wind direction. Another gives a direction and the word 'violent.' Their dates are close but not identical, and neither copy says where the gauge was mounted. The three current readings show why height matters. A vane beside a wall can turn differently from one exposed above it; neither has to be false.\n\nRowan writes the mast position, height, time and instrument ID beside every number. He leaves the old report's column unchanged and adds a note that the mounting height is unknown. Jace wants the discrepancy visible because it affects how a receiver could have shifted, but he does not claim that wind caused the missing signal. The measurements can bound a new test. They cannot identify an old sender, determine who stood at the mast or fill the empty roster."
    },
    {
        "key": "interval", "title": "The Interval Card with No Hour", "kind": "inspect", "target": "jace_four_places_interval",
        "objective": "Inspect the interval card and its paper seam. Record the order of the marks while leaving its calendar date unresolved.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "Sequence without a Calendar Date",
        "visual": "document", "position": (-1.2, -4.45), "display": "Unnumbered Interval Card",
        "lines": [
            "Someone marked three short intervals, then added a longer one in darker ink. The paper seam tells us which edge was folded first, not what day it was.",
            "Do not give the card a date because the report needs one. Write 'undated' and show why."
        ],
        "body": "The card holds four vertical marks in a sequence that may represent pauses in a test. A crease crosses the third mark, and darker ink extends the final interval. The marks can be ordered by where the pen overlaps the fold. No calendar date appears on the paper, and the storage envelope has a catalogue number written by a later clerk. The archive cannot infer the hour from the shape of the marks.\n\nJace used to place the card beside the night the survey receiver stopped sending. He believed the overlap suggested that the interval came from the same test. After reviewing the box, he says the card might belong to another calibration session; its edge was folded to fit a different sleeve. The sequence and the session are separate questions. The first has an answer from the ink and paper. The second remains open.\n\nRowan draws the marks at scale, photographs the crease in the field record and writes 'undated' where the old inventory left a blank. This is not an attempt to make uncertainty sound precise. The note explains exactly which part can be checked: a reader can compare the line order, fold and ink. A reader cannot use the card to place four people at the receiver, say when it failed or prove that the signal was sent from beyond the Veil."
    },
    {
        "key": "receiver", "title": "A Receiver Set to Listen Only", "kind": "inspect", "target": "jace_four_places_receiver",
        "objective": "Inspect the passive receiver and verify that its outgoing lead is physically disconnected during the comparison.",
        "speaker": "DR. EVELYN HART", "giver": "evelyn_hart", "codex_title": "A Silent Receiver Can Still Be Misread",
        "visual": "document", "position": (6.2, 4.55), "display": "Passive Receiver Plate",
        "lines": [
            "A receiver can be passive at the sensor and still share a circuit with a transmitter farther down the line.",
            "We will trace the outgoing lead, label every connection and write down the limit before anyone calls this a listening-only test."
        ],
        "body": "Evelyn opens the service panel and follows the receiver cable by hand. The first switch cuts power to the speaker, not to the signal relay. A second lead continues behind the wall, where a junction box connects the old line to the archive's maintenance network. Rowan disconnects it at the junction and places a dated seal across the open terminal. Only then do they run the passive comparison.\n\nThe receiver records three low intervals. The final one may be a vibration from the foundation; the instrument cannot separate it from the pool's movement without another sensor. The team notes the reading and resets the receiver. No outgoing message is prepared or sent. Evelyn asks Jace to write that sentence in the first page, because the word 'passive' can otherwise sound safer or more absolute than the wiring permits.\n\nThe survey's original diagram shows a receiver and a separate transmission mark, but the line between them is incomplete. The new test proves how the present archive can isolate one receiver. It does not prove that the old equipment used the same junction, that a signal came from another world or that no one altered the earlier setup. Those are questions for evidence that is not in this case."
    },
    {
        "key": "evelyn", "title": "Evelyn Counts the Unknowns", "kind": "talk", "target": "evelyn_hart",
        "objective": "Ask Dr. Evelyn Hart to review the measurements and distinguish the number of equipment spaces from the number of people on the survey.",
        "speaker": "DR. EVELYN HART", "giver": "evelyn_hart", "codex_title": "Two Ledgers and One Unfinished Join",
        "lines": [
            "The equipment ledger lists four sleeves. The personnel ledger has an empty field. Those two records cannot be joined by arithmetic.",
            "Jace is right to preserve the question, but the report also needs a method another archivist can challenge. Keep the readings, the labels and the missing link on separate pages."
        ],
        "body": "Evelyn places the equipment ledger beside the personnel sheet. One contains four fitted sleeves; the other has a blank field where a team list might have been copied. She refuses to write four names, four deaths or four departures into that gap. The ledgers answer different questions, and their matching shelf number may only mean that a clerk stored them together.\n\nShe reviews Rowan's three mast readings, the Farwake Carp sample and the receiver test. Each result has conditions that another person can repeat. The old report does not. Evelyn wants to add a method sheet that tells a future observer where to place the gauge, when to read the pool and how to disconnect the outgoing lead. A second reader could then dispute the results without needing to accept Jace's memory.\n\nJace says the careful procedure feels like a way to make the lost survey less important. Evelyn answers that a method is not a replacement for a person. It can preserve what they were trying to learn while leaving their identities and choices unclaimed. The team decides that the archive will keep the two ledgers side by side but not merge them. A later discovery may connect them; the current record has no authority to do so."
    },
    {
        "key": "draft", "title": "Jace Revises the Sentence He Wrote", "kind": "inspect", "target": "jace_four_places_draft",
        "objective": "Inspect Jace's draft and identify the sentence that turns an empty equipment index into a statement about the surveyors.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "The Sentence That Went Further than the Case",
        "visual": "document", "position": (10.2, 2.25), "display": "Jace's Unsent Draft",
        "lines": [
            "I wrote that the four places were lost with the crew. The case does not say that. I joined two blanks because I wanted the report to have an ending.",
            "Cross out my sentence, not the uncertainty. I will sign the correction with my own name."
        ],
        "body": "Jace's draft says, 'The four places were lost with the crew.' The sentence began as a note to himself, then appeared in a typed summary without its crossed-out ending. The case does not establish that the four spaces were occupied during the last test, and the personnel ledger does not show what happened to anyone who travelled. Jace has spent years treating the sentence as a confession that he failed to bring the team home. He now recognizes that the sentence claims more than he knows.\n\nHe does not erase the old copy. Rowan makes a correction slip that quotes the original wording, dates the review and identifies Jace as the person withdrawing its factual status. The revised note explains why the statement is unsupported and keeps it available for study as part of the archive's history. The error mattered: readers used it as a summary. Removing every trace would hide the way it changed the record.\n\nJace asks for a decision about the personal pages in the same box. The pages include his own field impressions and loose writing from an unknown hand. Some passages may be private, and no known author has given permission for publication. The measurement method can be public without those pages. The next choice will decide where each record belongs and who can review it. It will not decide whether the absent surveyors are dead, alive, lost or safely returned."
    },
    {
        "key": "policy", "title": "Choose How the Personal Pages Are Kept", "kind": "choice", "target": "jace_four_places_policy",
        "objective": "Choose how the archive will handle personal pages whose authorship and permission cannot yet be verified.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "The Policy before the Copy",
        "visual": "noticeboard", "position": (-10.15, -2.45), "display": "Archive Access Policy Board",
        "lines": [
            "The public method can be checked by anyone. The loose pages are different: the hand is unknown, and no family has asked us to publish them.",
            "I want a policy I can explain later, even if the choice makes the archive less complete."
        ],
        "body": "The box contains a public method sheet, the equipment ledger and loose personal pages. The method describes instruments and settings. The loose pages contain impressions that may belong to Jace, another surveyor or a later keeper. No page states that its author wished to publish it. Jace asks Rowan to choose a storage policy rather than guess the writer's wishes.\n\nOne route publishes the measurements, correction history and empty-roster warning, while withholding the loose pages. The public reader can repeat the test and challenge the old summary without seeing words whose author and permission are unresolved. The other route places the personal pages in a requestable folio. The access receipt names Jace as custodian, gives him a correction and withdrawal process, and lets a family request a review without promising access automatically.\n\nNeither policy adds names to the personnel ledger. Neither seals the public method. The choice is about the boundary between an instrument record and personal writing, not about whether the old expedition reached a safe destination. The archive will record who chose the policy and when, so a later custodian can reopen the decision if the missing authorship is established."
    },
    {
        "key": "public_method", "title": "Publish the Repeatable Test", "kind": "inspect", "target": "jace_four_places_public_method",
        "objective": "Review the public procedure. Confirm that it lists mast height, pool waterline, receiver wiring and the limits of each reading.",
        "speaker": "ROWAN HALE", "giver": "rowan_hale", "codex_title": "Instructions Anyone May Correct",
        "visual": "document", "position": (-6.4, -2.05), "display": "Public Test Procedure",
        "lines": [
            "The page gives another reader enough detail to repeat the setup and enough blank space to disagree with our result.",
            "It also says what the test cannot prove. That limit belongs beside the numbers, not in a locked appendix."
        ],
        "body": "The public procedure begins with the receiver disconnected from the outgoing relay. It lists the wind mast heights, the time between readings, the visible waterline and the position where a listener stands. A reader can use the same instruments or write down why a replacement was needed. The page includes a correction box with space for date, source and the name of the person making a change.\n\nJace insists that the limitations be printed in the same type size as the instructions. A low interval in the present hall cannot identify the old signal. A wind reading from one mast cannot reconstruct weather at an unknown date. Four instrument sleeves do not prove four people. The method is still worth sharing because it tells another observer what evidence could improve the record.\n\nRowan tries to repeat the steps from the page without help. He finds the receiver switch, traces the outgoing lead and writes the same three mast heights. One instruction assumes a tool is stored in the blue drawer; the blue drawer has since been removed. Jace adds a note that the tool's name matters more than the drawer's color. A public procedure stays open to correction, and the first correction comes before the page is posted."
    },
    {
        "key": "public_index", "title": "Post the Index with Its Empty Field", "kind": "inspect", "target": "jace_four_places_public_index",
        "objective": "Inspect the public index after posting. Keep the personnel field visibly blank and attach the correction history to Jace's old sentence.",
        "speaker": "LYRA MOSS", "giver": "lyra_moss", "codex_title": "A Blank Field Kept in Public View",
        "visual": "noticeboard", "position": (10.4, -2.35), "display": "Public Expedition Index",
        "lines": [
            "The blank is now labeled 'unverified roster,' not 'four lost people.' That is a smaller sentence and a more honest one.",
            "Keep the correction beside the old copy, so readers can see how the phrase changed."
        ],
        "body": "The public index lists the case, the four sleeves, the receiver test and the date the archive received the box. The personnel field remains blank, with a note explaining that no verified roster was found in the returned materials. The phrase does not imply that the sleeves were empty during the expedition, nor that their users disappeared. It tells the reader only what the archive has not identified.\n\nLyra attaches Jace's correction slip beside the older summary. She does not remove the sentence he wrote, because its history explains why the archive once treated the equipment count as a crew count. A small index tab directs readers from the old wording to the correction and then to the repeatable method. That arrangement makes the record less clean, but it also makes the process visible.\n\nA visitor can now challenge the way the case was interpreted, submit a new document or request that an error be corrected. The public sheet does not contain personal pages from the box. Jace signs as the keeper of the correction, not as the person who can speak for the unknown writers. The record ends with a question for future evidence rather than a prediction about the absent surveyors."
    },
    {
        "key": "private_receipt", "title": "Write the Receipt for the Requestable Folio", "kind": "inspect", "target": "jace_four_places_private_receipt",
        "objective": "Inspect the access receipt. Confirm that it names the custodian, review path, correction right and conditions for a future request.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "A Receipt with an Exit Path",
        "visual": "sealed_case", "position": (5.7, -4.65), "display": "Folio Access Receipt",
        "lines": [
            "The receipt must say how to ask, how to correct a mistake and how to close the folio again.",
            "A seal without an exit path would only transfer control from the unknown writer to the archive."
        ],
        "body": "Jace lists himself as custodian of the requestable folio. The receipt explains where a future request can be filed, who will review it and how the decision can be appealed. A request does not guarantee access. It begins a conversation about authorship, family interest and the safety of sharing a personal page. If the writer is identified, that person may ask for a correction or withdrawal.\n\nThe receipt also records the limits of the archive's authority. Jace cannot consent on behalf of the unknown writer, and Rowan cannot infer consent from the fact that the page was stored with survey equipment. If no author can be found, the method remains public while the personal text stays closed. A dated review may reopen the question when new evidence appears.\n\nThe document includes a visible opening mark on the folio, but it does not describe the case as unbreakable. Its purpose is to leave evidence of handling and require the custodian to record a change. Jace signs as a person accepting a duty, not as an owner of the words. The archive will be able to show who held the key, who asked for a review and whether the folio was opened, while continuing to admit that it cannot name every writer."
    },
    {
        "key": "private_folio", "title": "Place the Pages under a Requestable Seal", "kind": "inspect", "target": "jace_four_places_private_folio",
        "objective": "Inspect the closed folio. Verify that the method remains public, the personal pages are unquoted and the seal can be reviewed by request.",
        "speaker": "DR. EVELYN HART", "giver": "evelyn_hart", "codex_title": "What the Seal Protects and What It Cannot",
        "visual": "sealed_case", "position": (0.75, 4.45), "display": "Requestable Personal Folio",
        "lines": [
            "The public procedure stays on the table. Only the pages whose author is uncertain are under seal.",
            "A seal can limit access; it cannot tell us who wrote the page or what they would have wanted."
        ],
        "body": "The folio holds the loose personal pages and a copy of the access receipt. It does not hold the public method, equipment measurements or correction history. Evelyn checks the separation before the case is closed. A future reader can reproduce the receiver test without seeing a private sentence, and a family can ask the archive to review access without being promised an answer on someone else's behalf.\n\nThe seal is dated and split across the paper edge. If it is opened, the break will be visible and a new receipt must be added. The mark offers accountability, not physical protection from every hand. Jace keeps the key in the archive office and records which two staff members may witness a review. Neither witness can substitute their consent for the writer's.\n\nEvelyn asks Rowan to read the public index once more. It says the folio exists, describes how a request may be made and does not quote its contents. The private route therefore leaves a public trail without exposing the words. The unknown hand stays unknown; the family has a path to ask; the method remains available to everyone. Those boundaries may change if the author is identified, so the seal is requestable rather than permanent."
    },
    {
        "key": "afterword", "title": "Leave Four Places Open to Evidence", "kind": "talk", "target": "jace_morrow",
        "objective": "Speak with Jace after the chosen record is filed. Confirm that the method can be challenged and that no one has been declared lost or safe without evidence.",
        "speaker": "JACE MORROW", "giver": "jace_morrow", "codex_title": "Four Places Left for a Future Record",
        "lines": [
            "The case has a public description now. The pages have a boundary. I still do not know who used each sleeve or where the survey ended.",
            "For once the report can remain unfinished without pretending I have stopped looking."
        ],
        "body": "The route ends with the same four empty sleeves that opened it. Their shape is now measured, the repair marks are dated where possible, and the unknowns are written beside the claims they limit. Skyroot fiber has a present-day comparison. Farwake Carp has a catch record from Celestial Pool. The receiver has been tested after its outgoing lead was disconnected. None of those steps places a name in the personnel field.\n\nJace reads the filed version in both forms. If Rowan chose the public index, the method and correction history can be examined directly. If Rowan chose the requestable folio, the public method still stands beside an access receipt that gives personal pages a review path. In either route, Jace no longer asks the archive to turn the four sleeves into a count of people.\n\nHe says the correction has not repaired the survey or resolved its ending. It has changed what a reader is allowed to assume. A later letter, instrument log or verified family account could connect one of the sleeves to a person. Until such evidence exists, the archive leaves the spaces unassigned. Jace asks Rowan to keep the empty field visible at the next review. The record can be incomplete and still be more accurate than the finished sentence he once wrote."
    },
]

quests, dialogues, codex, landmarks = [], [], [], []
previous = "side_outerwake_jace_afterword"
policy_flag = "jace_four_places_policy"

for entry in records:
    quest_id = "side_outerwake_four_places_" + entry["key"]
    dialogue_id = "jace_four_places_" + entry["key"]
    objective_id = "jace_four_places_" + entry["key"] + "_objective"
    prior = previous
    if entry["key"] == "private_receipt":
        prior = "side_outerwake_four_places_policy"
    quest = {
        "id": quest_id,
        "arcId": "archive_beyond_veil",
        "stage": -1,
        "type": "side",
        "locationId": "outerwake_archive",
        "giverId": entry["giver"],
        "title": entry["title"],
        "objective": entry["objective"],
        "prerequisiteIds": [prior] if prior else [],
        "objectives": [{
            "id": objective_id,
            "kind": entry["kind"],
            "targetId": entry["target"],
            "requiredCount": 1,
            "description": entry["objective"],
            "dialogueId": dialogue_id,
        }],
        "reward": {"gold": 5, "items": []},
    }
    if entry["key"] in {"public_method", "public_index"}:
        quest["branchFlag"] = policy_flag
        quest["branchValue"] = "public_method"
    elif entry["key"] in {"private_receipt", "private_folio"}:
        quest["branchFlag"] = policy_flag
        quest["branchValue"] = "requestable_folio"
    elif entry["key"] == "policy":
        quest.update({
            "choiceFlag": policy_flag,
            "choiceSpeaker": "JACE MORROW",
            "choicePrompt": "Choose how the unknown personal pages are held. The equipment method and correction history remain available in both routes.",
            "choices": [
                {
                    "id": "publish_method",
                    "label": "Publish the repeatable method and correction history; keep the unverified personal pages out of the public index.",
                    "flagValue": "public_method",
                    "dialogueId": "jace_four_places_choice_public",
                    "reward": {"gold": 0, "items": []},
                },
                {
                    "id": "requestable_folio",
                    "label": "Keep the personal pages in a requestable folio with a custodian, review path and correction right.",
                    "flagValue": "requestable_folio",
                    "dialogueId": "jace_four_places_choice_folio",
                    "reward": {"gold": 0, "items": []},
                },
            ],
        })
    elif entry["key"] == "afterword":
        quest.pop("prerequisiteIds", None)
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": [
            "side_outerwake_four_places_public_index",
            "side_outerwake_four_places_private_folio",
        ]}]
    quests.append(quest)
    dialogues.append({"id": dialogue_id, "speakerName": entry["speaker"], "lines": entry["lines"]})
    codex.append({
        "id": "jace_four_places_" + entry["key"] + "_record",
        "title": entry["codex_title"],
        "category": "Four Places Left Unassigned",
        "writtenBy": "Jace Morrow",
        "unlockQuestId": quest_id,
        "body": entry["body"],
    })
    if entry.get("visual"):
        x, y = entry["position"]
        landmarks.append({
            "id": "jace_four_places_marker_" + entry["key"],
            "locationId": "outerwake_archive",
            "displayName": entry["display"],
            "targetId": entry["target"],
            "visualId": entry["visual"],
            "positionX": x,
            "positionY": y,
            "scale": 0.085,
        })
    previous = quest_id

# Branch choice outcomes are separate interactions and unlock their branch-only definitions.
dialogues.extend([
    {"id": "jace_four_places_choice_public", "speakerName": "JACE MORROW", "lines": [
        "Then the measurements and my correction stay open to review. The loose pages will not be quoted or indexed as testimony.",
        "If someone identifies the writer, we can revisit the boundary with evidence instead of guessing."
    ]},
    {"id": "jace_four_places_choice_folio", "speakerName": "JACE MORROW", "lines": [
        "Keep the original pages together and leave a request path on the public index. A family can ask us to review them, but the request does not decide what the writer wanted.",
        "I will sign as custodian and accept the duty to reopen the case."
    ]},
])

for filename, additions in [
    ("prologue_quests.json", quests),
    ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", codex),
    ("quest_landmarks.json", landmarks),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} quests, {len(dialogues)} dialogue entries, "
      f"{len(codex)} field records and {len(landmarks)} interactive markers.")
