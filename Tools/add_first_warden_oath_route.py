#!/usr/bin/env python3
"""Install The First Oath's Missing Measure, a 40-quest Choir route for The First Warden."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"

def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))

def write(name, value):
    (CONTENT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def upsert(entries, additions):
    indexes = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)

def row(key, title, kind, target, objective, speaker, lines, record_title, record_body,
        visual="", position=None, giver="first_warden", location="choir_beneath_lake"):
    return {
        "key": key, "title": title, "kind": kind, "target": target,
        "objective": objective, "speaker": speaker, "lines": lines,
        "record_title": record_title, "record_body": record_body,
        "visual": visual, "position": position, "giver": giver, "location": location,
    }

common = [
row("open", "The First Oath's Missing Measure", "talk", "first_warden",
    "Meet The First Warden after the cycle report. He wants to write down the first oath as a memory with limits, not as a rule for every later century.",
    "THE FIRST WARDEN",
    ["The first oath began with a bell whose lower note no one could place. I remember my hand on the stone, but not every voice in the hall.",
     "I have allowed the archive to call my memory a beginning. Help me show what I remember, what the record repeats and where neither can speak."],
    "A Memory Is Not the Whole Beginning",
    "After the report on the ninety-ninth cycle, The First Warden asks to revisit the first oath. He remembers making a promise in a room beneath the lake, but no surviving witness list proves who else heard it. The archive later used his account as a starting point for its chronology. He wants to keep the memory while making its limits visible, so it cannot quietly become a forecast for every generation.",
    giver="first_warden"),
row("bell_rim", "The Bell's Lowest Rim", "inspect", "warden_oath_low_bell",
    "Inspect the lowest rim of the silent bell. Record the worn edge without assigning it to the first oath or a later repair.",
    "ROWAN HALE",
    ["The wear is real. Its date is not written here.", "I will label what my hand can measure and leave the rest open."],
    "Wear without a Date",
    "The lowest rim is polished along a narrow arc. The smooth surface may come from repeated handling, vibration or a repair made after the oath. Rowan records its width and position but does not assign the mark to the first night. The bell remains useful as a physical object; the date in the archive stays uncertain until another dated source can be found.",
    "noticeboard", (-2.4, 4.0), giver="rowan_hale"),
row("lyra", "Lyra Separates Memory from Notation", "talk", "lyra_moss",
    "Ask Lyra which line in the choir index is The First Warden's own memory and which lines were copied by later archivists.",
    "LYRA MOSS",
    ["His first account has a different ink and a different hand. Later copies make it look like a title page.", "I can show the layers without declaring which sentence should govern the rest."],
    "A First Hand and Many Copies",
    "Lyra finds the Warden's first account beneath three later index sheets. The oldest ink is faded, but its authorship mark remains. A later clerk added a heading that calls the account the beginning of every cycle. That heading is not in the Warden's hand. Lyra proposes preserving both layers with dates, rather than erasing the heading or treating it as a fact from the first night.",
    giver="lyra_moss"),
row("kelp", "A Fresh Echo Kelp Leaf", "harvest", "echo_kelp",
    "Harvest Echo Kelp from the choir garden for a fresh, dated sample. Keep the cut end and the living stem separate.",
    "THE FIRST WARDEN",
    ["I used to ask the gardeners to leave a leaf at the bell after each hearing.", "A fresh sample cannot reproduce the first sound, but it can tell us how this garden carries one now."],
    "One Leaf from the Present Garden",
    "The choir garden grows a new Echo Kelp leaf along its eastern bed. Rowan notes its depth and the date of harvest before bringing it to Lyra. The leaf carries a short vibration while wet and goes quiet as it dries. It is a sample of the present water and plant, not a preserved piece of the first oath.",
    giver="rowan_hale"),
row("koi", "Whisper Koi at the Listening Pool", "catch", "whisper_koi",
    "Catch one Whisper Koi at the Listening Pool. Note the pool, bait and time; the fish is a present-day comparison sample.",
    "LYRA MOSS",
    ["The old phrase says the second note arrived late. It does not say a fish carried it.", "We need a sample from this pool before we compare the phrase with a living sound."],
    "A Whisper Koi and Its Water",
    "Rowan catches a Whisper Koi where the archive's listening channel meets the pool. Lyra records the location, bait and catch time while the sample remains wet. The fish reacts to the current water and nearby activity. Its response cannot identify the source of a sound from the first oath, but it gives the team a repeatable present-day observation.",
    giver="rowan_hale"),
row("gate", "A Merrow in the Lower Passage", "defeat", "tiny_ch_choir_merrow",
    "Defeat the Choir Merrow disturbing the lower passage. Recover the Choir Mote from its nest for Lyra's non-vocal comparison rig.",
    "THE FIRST WARDEN",
    ["The creature has taken the loose glass from my old listening tray.", "Clear the passage, and keep the recovered mote separate from every human voice."],
    "A Mote from the Lower Passage",
    "A Choir Merrow has nested beside the lower listening passage and gathered bright fragments into its bed. Rowan clears the path while the Warden waits above. The recovered Choir Mote came from the creature's nest, not from a person or an oath recording. Lyra can use it to compare the hall's current resonance without playing a preserved voice.",
    giver="rowan_hale"),
row("craft", "Build a Non-Vocal Listening Weight", "craft", "first_oath_memory_charm",
    "At the Choir Harmonic Anvil, craft the First Oath Listening Weight from Echo Kelp, Whisper Koi and a Choir Mote.",
    "LYRA MOSS",
    ["This weight holds the listening rig at one depth; it does not retain a voice.", "If the hall changes its response, we can reset the position and try again."],
    "A Weight for a Repeatable Position",
    "Lyra and Tomas shape the Echo Kelp backing around a measured metal weight. A Whisper Koi scale marks the shallow side, and a Choir Mote helps the small edge catch the lamp. The item fixes the rig at a known depth without recording or storing any voice. If the hall's response changes, the same position can be restored and measured again.",
    "document", (5.5, 2.6), giver="lyra_moss"),
row("time_marks", "Three Marks Below the Surface", "inspect", "warden_oath_time_marks",
    "Inspect three tide marks beneath the bell. Measure the spacing and keep the first date label as unknown.",
    "ROWAN HALE",
    ["The marks are evenly spaced, but the wall has been repaired twice.", "I can measure the gaps without pretending the same hand cut each line."],
    "Three Lines, Two Repairs",
    "Three horizontal marks remain on the stone below the bell. Two repairs cross the same surface, and no dated plan shows whether the marks came before or after them. Rowan measures the distance between the grooves and records the repairs as visible interruptions. The spacing may help compare a later diagram, but it does not establish the order in which the first oath or any repair occurred.",
    "waymarker", (-5.1, 3.6), giver="rowan_hale"),
row("stairs", "The Stair That Changes the Note", "inspect", "warden_oath_stair",
    "Inspect the lower stair from two standing positions and mark where the bell's low note fades in today's hall.",
    "THE FIRST WARDEN",
    ["The note used to follow me down these steps. I cannot tell whether the stone changed or I learned to expect it.", "Write both standing places. Memory often keeps the destination and loses the path."],
    "A Note from Two Standing Places",
    "From the upper stair, the silent bell's test tone carries past the second landing. From the lower position, the same tone is masked by water moving through a side channel. The present-day difference depends on where Rowan stands. The Warden remembers a note following him down the stairs but cannot date the memory against the repairs. Both positions are recorded.",
    "waymarker", (-6.2, -2.4)),
row("first_promise", "The Promise Before the Heading", "talk", "first_warden",
    "Ask The First Warden to say the first promise in his own words before reading the archive heading aloud.",
    "THE FIRST WARDEN",
    ["I promised to keep the names I had been given from disappearing in the dark.", "The later heading says I promised every future generation would choose the same thing. That second sentence was not mine."],
    "Two Sentences with Different Authors",
    "The Warden remembers promising to keep the names entrusted to him. The archive heading expands this into a rule for every future generation. He does not remember making that broader promise. Lyra dates the heading to a later copy and keeps it visible as an editorial layer, so readers can see how a private commitment grew into a public doctrine.",
    giver="first_warden"),
row("lyra_layers", "A Drawer for the Copying Layers", "talk", "lyra_moss",
    "Ask Lyra how the archive can preserve a copyist's heading without mistaking it for The First Warden's testimony.",
    "LYRA MOSS",
    ["I can keep the heading, name the hand that added it and show the older page beside it.", "The archive can preserve the history of an error without repeating the error as its own voice."],
    "Preserving an Editorial Layer",
    "Lyra proposes a layered folio. The Warden's first-person memory remains in its original position. The later heading is copied on a separate leaf with the clerk's date and an editorial label. A reader can understand why generations used the heading while still seeing that it was added after the first account.",
    giver="lyra_moss"),
row("light_test", "A Lamp at the Same Depth", "inspect", "warden_oath_lamp_test",
    "Use the listening weight to repeat a low-note test with the lamp held at the marked depth. Record water height and distance.",
    "ROWAN HALE",
    ["The light breaks across the scale differently when the water rises.", "This trial compares today's depth and distance, not the first hall as I remember it."],
    "Light and Water Height",
    "Rowan fixes the non-vocal rig at the marked depth and tests the low note once with the waterline low and again after the sluice rises. The scale reflects different bands of light. The note remains a present-day test, and the conditions are written beside each reading. The result can help a later observer repeat the setup without borrowing the Warden's memory.",
    "document", (1.4, -3.9), giver="rowan_hale"),
row("archive_copy", "Find the Heading's Copy Date", "inspect", "warden_oath_heading_copy",
    "Inspect the copy dated after the Warden's first account. Record the hand, paper seam and the heading that was added.",
    "LYRA MOSS",
    ["The seam crosses the heading's lower stroke. It was attached after the older leaf was bound.", "A physical join gives us an order for the papers, not a reason for the later wording."],
    "The Heading Joined Later",
    "The paper seam crosses the lower part of the later heading. The leaf was attached after the older account had already been bound. This establishes a sequence for the pages, not the motive of the copyist. Lyra records the hand and seam beside the words so future readers can tell the addition from the source.",
    "document", (2.1, 1.4), giver="lyra_moss"),
row("private_memory", "What the Warden Cannot Date", "talk", "first_warden",
    "Ask The First Warden which part of the first oath he remembers as a feeling rather than a dated event.",
    "THE FIRST WARDEN",
    ["I remember the room was cold. I do not know if the season had turned or if the water had fallen.", "My body kept the feeling longer than the date. Do not file one as the other."],
    "A Feeling Has No Calendar",
    "The Warden remembers cold stone under his palm. He cannot say whether the season had changed or the water had dropped, and the current archive contains no instrument reading from that day. Rowan records the sensation as a personal memory with no date. It may help explain how the oath felt to him without becoming a measurement of the hall.",
    giver="first_warden"),
row("measure_card", "A Card with Space for Conditions", "inspect", "warden_oath_measure_card",
    "Inspect the draft comparison card. Make sure the memory, copied heading and current test occupy separate rows.",
    "ROWAN HALE",
    ["Three rows, three sources. Nothing in the margin turns them into one witness.", "The blank date stays visible until someone brings a dated source."],
    "Three Sources Kept Apart",
    "The card has separate rows for the Warden's first-person memory, the copyist's later heading and the present-day acoustic test. Each row names its source and limitations. A blank date remains rather than borrowing a date from the next page. The card is now readable without making one kind of evidence stand in for another.",
    "noticeboard", (-1.4, 2.0), giver="rowan_hale"),
row("policy", "Where Should the First Account Live?", "choice", "first_oath_record_policy",
    "Choose how The First Warden wants his first-person account to be kept after the copy layers are separated.",
    "THE FIRST WARDEN",
    ["I can let the account be read beneath my name, or I can keep the full memory for those I choose.", "Either way, the later heading must remain marked as a later hand."],
    "A Policy for the First Account",
    "The First Warden distinguishes ownership of his own memory from the archive's later use of it. A public folio can carry his first-person account, its date limits and the copyist's separate heading. A private folio can keep the memory available only through a review request while the method and copy history remain public. Both choices preserve the layers.",
    "noticeboard", (-0.4, 4.3)),
]

public = [
row("public_open", "The Warden Names His Own Hand", "talk", "first_warden",
    "Hear The First Warden draft the public opening under his name and mark which sentences are remembered rather than dated.",
    "THE FIRST WARDEN",
    ["I will speak in the first person. I will not make my memory the first voice of every generation.", "Keep the weather uncertain and my promise in the words I remember."],
    "A First-Person Opening",
    "The Warden drafts an opening that names himself as the speaker and labels the cold room as a remembered sensation. He refuses to state a season or a crowd size. The page does not ask readers to accept his account as a universal beginning; it gives them one witness's memory with its edges intact.",
    giver="first_warden"),
row("public_folio", "Set the Public Folio beside the Bell", "inspect", "warden_oath_public_folio",
    "Inspect the public folio. Confirm the Warden's name, the memory label and the later-heading note are visible.",
    "ROWAN HALE",
    ["The heading has a date and the account has a speaker.", "A reader should not need Lyra beside them to tell which is which."],
    "Public Folio Layout",
    "The public folio places the Warden's name above his words, a small label beside the undated memory and a separate note for the later heading. The layout makes the distinction readable without verbal assistance. A correction can be added beneath either layer with a date and author, leaving both earlier pages untouched.",
    "noticeboard", (0.6, -0.5), giver="rowan_hale"),
row("public_method", "Publish the Repeatable Hall Test", "inspect", "warden_oath_public_method",
    "Inspect the method sheet and verify that another reader can reset the lamp, waterline and listening weight.",
    "LYRA MOSS",
    ["The method belongs to anyone who wants to repeat it.", "The first-person memory belongs to the person who spoke it."],
    "A Method Anyone May Repeat",
    "The public method lists the bell location, weight depth, waterline and distance between two standing marks. It contains no voice sample. A visitor can repeat the low-note test and record a new result without listening to a stored human account. Lyra marks the method as current, so future readers will not mistake it for a first-cycle record.",
    "document", (7.0, -1.7), giver="lyra_moss"),
row("public_lyra", "Lyra Reviews the Layer Labels", "talk", "lyra_moss",
    "Ask Lyra to review the public labels. She must be able to distinguish the Warden's page from the copyist's heading.",
    "LYRA MOSS",
    ["I can read both layers without moving one beneath the other.", "Keep the copyist's name open for correction; this shelf has passed through many hands."],
    "A Review That Can Be Repeated",
    "Lyra reads the folio once from the speaker label and once from the copy-history label. The two passes produce the same separation of sources. She leaves the copyist field open because a later clerk may identify the hand more precisely. Her review confirms legibility, not the truth of the Warden's memory.",
    giver="lyra_moss"),
row("public_margin", "Leave the Undated Margin in Place", "inspect", "warden_oath_public_margin",
    "Inspect the public margin. Confirm that the cold-room memory has no borrowed date and the missing interval remains legible.",
    "ROWAN HALE",
    ["A blank line can show where the record stops.", "We need not write a guess into it just to make the page look finished."],
    "An Honest Blank in Public",
    "The public margin holds one blank for a date and another for a second witness. Neither is prefilled from the later heading. The page explains that the Warden's account is undated and that future evidence may be attached. The blank remains usable without being mistaken for an accidental printing gap.",
    "document", (-3.6, 0.9), giver="rowan_hale"),
row("public_sign", "The Warden Signs His Account", "talk", "first_warden",
    "Ask The First Warden to sign only his own account and its limits, not the copyist's later heading.",
    "THE FIRST WARDEN",
    ["I can sign what I remember and the fact that I cannot date it.", "The heading is another hand. I will not sign in its place."],
    "A Signature with a Boundary",
    "The Warden signs beneath his first-person account and the limits he has stated. He leaves the copyist's heading on its own sheet. The signature authenticates that he gave this memory; it does not certify every interpretation made from it across later centuries.",
    giver="first_warden"),
row("public_board", "Post the Folio with Its Copy History", "inspect", "warden_oath_public_board",
    "Inspect the posted folio and make sure its correction path is separate from the original words.",
    "ROWAN HALE",
    ["A later correction can join the file without scraping out the first page.", "The copy history is part of the reading, not a hidden note."],
    "A Public File with a Correction Path",
    "The posted folio has a pocket for dated corrections and a visible note about its copying history. The original page remains readable if new information arrives. No one is required to provide a correction, and the archive does not announce that one is expected. The Warden's account is public while the space beyond it remains open.",
    "noticeboard", (-7.1, 1.5), giver="rowan_hale"),
row("public_after", "The First Oath Is Read under His Name", "talk", "first_warden",
    "Speak with The First Warden after the public folio is posted and ask how it feels to see his memory without the later title.",
    "THE FIRST WARDEN",
    ["It is smaller on the wall than the rule it became.", "I can live with a smaller account. It leaves room for everyone else."],
    "After the Public Reading",
    "The Warden reads the folio from the beginning without the later title standing above it. He says his memory now feels smaller, and less heavy. The public route preserves his account and the fact that it was once used as a general rule. It does not require him to approve that old expansion.",
    giver="first_warden"),
]

sealed = [
row("sealed_open", "Keep the Full Memory in a Named Folio", "talk", "first_warden",
    "Hear The First Warden ask for one named private folio while leaving the copying method public.",
    "THE FIRST WARDEN",
    ["I would rather choose who reads the full memory. The later heading can still be studied in public.", "Do not call the closed folio lost. Write where a review request can reach it."],
    "A Requestable Private Folio",
    "The Warden chooses a private folio for his first-person memory. A public record will still show that the folio exists, who holds it and how a review request can be made. The route protects access to the memory without hiding the later copy history or pretending the archive never used the heading.",
    giver="first_warden"),
row("sealed_receipt", "Write the Access Receipt before Closing", "inspect", "warden_oath_access_receipt",
    "Inspect the access receipt. Name the holder, the review path and the fact that no one else may answer for the Warden.",
    "ROWAN HALE",
    ["The receipt describes who can open the folio, not what they must think after reading it.", "Access is a boundary; agreement is a different question."],
    "The Receipt Is Not an Endorsement",
    "The access receipt names the Warden as the memory's speaker and Lyra as the archive holder. It lets the Warden ask for a private reading and records any later opening. It does not say that a reader agrees with his account or that the account stands for the other first-cycle voices.",
    "sealed_case", (4.0, -3.1), giver="rowan_hale"),
row("sealed_lyra", "Lyra Holds the Key and the Correction Path", "talk", "lyra_moss",
    "Ask Lyra how she will protect the folio while still letting the Warden revise or withdraw it.",
    "LYRA MOSS",
    ["The access log will show each opening. The Warden can ask me to close the review path again.", "I will not copy his words into a public index just because I keep the key."],
    "The Holder's Duties",
    "Lyra accepts the role of holder with two duties: record each access and honor the speaker's request to close the review path. She will not summarize the private memory into a public index. The archive can publish its method and the copying history while leaving the account itself with its speaker.",
    giver="lyra_moss"),
row("sealed_method", "Keep the Measurement Method Public", "inspect", "warden_oath_sealed_method",
    "Inspect the public method sheet. Verify it includes no excerpt from the closed folio.",
    "ROWAN HALE",
    ["The test can be repeated without opening the case.", "A method does not need the private memory as its key."],
    "Public Method, Private Memory",
    "The public method sheet contains the bell's position, the rig depth, current water conditions and the reset steps. It includes no quotation from the Warden's folio. Anyone may repeat the acoustic test while the speaker retains control over the memory. The two records answer different questions and do not need to be published together.",
    "document", (6.6, 3.9), giver="rowan_hale"),
row("sealed_copy", "Set the Copyist's Heading on Its Own Shelf", "inspect", "warden_oath_heading_shelf",
    "Inspect the public copy-history note and make sure the later heading is attributed separately from the sealed memory.",
    "LYRA MOSS",
    ["The heading remains visible with its copy date.", "A sealed page cannot be used to claim that it agrees with an open title."],
    "A Separate Shelf for the Later Heading",
    "Lyra places the copyist's heading on a public shelf with its attachment date and a note that the source memory remains private. Readers can study how the later title shaped the archive without seeing the Warden's full account. The shelf entry does not paraphrase the private page.",
    "document", (3.2, 2.3), giver="lyra_moss"),
row("sealed_sign", "The Warden Signs the Access Rule", "talk", "first_warden",
    "Ask The First Warden to approve the access receipt and confirm he can reopen or withdraw the folio.",
    "THE FIRST WARDEN",
    ["I will place my name beside the rule that governs my own words.", "If I close the folio later, the fact that it existed can remain. The memory is mine to share."],
    "A Rule Signed by Its Speaker",
    "The Warden signs the access rule as speaker and holder of the memory. He can ask Lyra to open a review or close it again. The public history will retain the date of the change but not a copy of his words. This makes privacy reversible without making the archive's record of its own procedure disappear.",
    giver="first_warden"),
row("sealed_mark", "Seal the Folio with an Opening Mark", "inspect", "warden_oath_seal_mark",
    "Inspect the sealed case after closing it. Record the split mark and who may request a future opening.",
    "ROWAN HALE",
    ["The seal crosses paper and wax once; opening it will leave a visible change.", "The mark cannot stop every hand, but it makes the archive answer for access."],
    "A Seal That Records Its Own Change",
    "A split wax mark crosses the paper and case. Lyra records who may request an opening and where the key is kept. The seal is not described as unbreakable. Its purpose is to make handling visible and create a receipt if the folio is opened or resealed.",
    "sealed_case", (-0.7, -3.7), giver="rowan_hale"),
row("sealed_after", "The Private Memory Remains Requestable", "talk", "first_warden",
    "Speak with The First Warden after the folio is sealed and confirm that the method and copy history remain available.",
    "THE FIRST WARDEN",
    ["I have not hidden the archive's history. I have chosen when my memory is read.", "Those two things can be true at once."],
    "After the Private Folio Is Filed",
    "The Warden checks that the public method and later-heading history remain available while his account stays closed. The private route changes access, not the archive's claim that his account influenced later records. Lyra leaves the review path ready for a future request, and the Warden keeps the right to decide whether it opens.",
    giver="first_warden"),
]

shared = [
row("new_test", "A New Test without the Old Voice", "inspect", "warden_oath_second_test",
    "Repeat the non-vocal hall test with the listening weight at a second depth. Record the new waterline beside the first result.",
    "ROWAN HALE",
    ["The lower note weakens at a different point when the rig is raised.", "We have two current results now, not a reconstruction of the first night."],
    "Two Present-Day Readings",
    "Rowan repeats the test at a higher rig depth and writes down the new waterline. The low note weakens at a different point than it did at the first depth. Both results belong to the current hall. The Warden's memory remains in its own category whether the player selected a public or private folio.",
    "document", (-4.0, 2.4), giver="rowan_hale"),
row("second_kelp", "A Second Echo Kelp Harvest", "harvest", "echo_kelp",
    "Harvest another Echo Kelp leaf after resetting the garden plot. Label its age and water depth before Lyra compares it.",
    "LYRA MOSS",
    ["This leaf carries the note for less time than the first one.", "Its age may explain the difference; keep the dates attached to both samples."],
    "Two Leaves from Different Days",
    "Lyra compares two Echo Kelp leaves gathered on different days. The newer leaf carries the test vibration for less time, perhaps because it is younger or because the water changed. The team records both dates and depths rather than replacing the first sample. The difference belongs to the plants and conditions, not to a human voice.",
    giver="rowan_hale"),
row("second_koi", "Whisper Koi under a New Waterline", "catch", "whisper_koi",
    "Catch a second Whisper Koi after the pool level changes. Record the waterline and bait as separate conditions.",
    "THE FIRST WARDEN",
    ["I heard the second note arrive late in memory. This fish is not that note.", "Still, the pool has changed since our first sample, and the change belongs in the present record."],
    "A Second Fish, a Different Waterline",
    "The second fish comes from a pool whose waterline has risen. Rowan records the bait and level before Lyra places the sample beside the first. The catch helps compare present conditions. It cannot confirm the remembered delay in the first oath's second note, so the old phrase remains attributed to the Warden.",
    giver="rowan_hale"),
row("lyra_review", "Lyra Reads Both Policies Fairly", "talk", "lyra_moss",
    "Ask Lyra to explain the difference between the chosen policy and what it says about the Warden's memory.",
    "LYRA MOSS",
    ["Public or private changes who may read his words.", "Neither choice changes which page was written first or how much he can date."],
    "Access Does Not Change Chronology",
    "Lyra records the selected access policy but keeps the page order unchanged. The public route does not add certainty to the memory, and the private route does not make the later heading earlier. Both policies preserve the same source labels and leave the same date blank.",
    giver="lyra_moss"),
row("copy_review", "Review the History of the Heading", "inspect", "warden_oath_copy_review",
    "Inspect the heading's copy history one final time. Verify that its later date remains visible under either policy.",
    "ROWAN HALE",
    ["The title shaped how people read the account. That is part of its history.", "We can acknowledge the effect without treating the title as the original promise."],
    "A Heading with Consequences",
    "The archive records that the later heading influenced how readers understood the Warden's first promise. The note does not erase that effect, but it keeps the heading's date and author separate from the original memory. A future reader can study both the words and the way they were used.",
    "document", (0.8, -4.1), giver="rowan_hale"),
row("warden_walk", "The Warden Leaves the Bell Room", "talk", "first_warden",
    "Speak with The First Warden after the records are filed. Ask whether he wants to remain inside the archive for the next listening cycle.",
    "THE FIRST WARDEN",
    ["I can walk to the garden without carrying the page in my hand.", "Ask me again after the next cycle of visitors. I may give a different answer."],
    "A Walk Outside the Record",
    "The Warden steps beyond the bell room for a short walk to the garden entrance. He does not call this a new oath or a permanent departure. The action is small and current: the immortal witness chooses to stand somewhere other than the archive. The next visit may find him back at the bell or farther down the passage.",
    giver="first_warden"),
row("future_marker", "Leave a Space for the Next Listener", "inspect", "warden_oath_future_marker",
    "Inspect the open marker by the garden entrance. Confirm it can hold a new listener's own date and words.",
    "ROWAN HALE",
    ["No one has signed this space yet.", "The next visitor can write a different question instead of inheriting ours."],
    "A Space Not Assigned in Advance",
    "The marker contains no predicted name, title or answer. It has a line for a future listener's date and a blank area for the question they bring. It does not ask each generation to repeat the same test. The archive keeps the space available without suggesting that anyone is expected to use it.",
    "noticeboard", (7.1, -2.6), giver="rowan_hale"),
row("afterword", "The First Oath Keeps Its Missing Measure", "talk", "first_warden",
    "Speak with The First Warden after the new listener's marker is placed. Confirm what he remembers and what the archive must leave open.",
    "THE FIRST WARDEN",
    ["I remember the cold stone and the promise I made. I cannot date the cold or name every voice.", "Let the next listener add their own account. Do not make my beginning their ending."],
    "The First Oath Keeps Its Missing Measure",
    "The Warden's first-person memory remains beside, not above, the later copy history and present-day tests. If chosen, it is either publicly readable under his name or held in a requestable private folio. Both routes preserve the undated interval, the right to correct the file and a place for a new listener. The archive records a beginning without dictating how every cycle must end.",
    giver="first_warden"),
]

def make_quest(entry, prior=None, branch=None, choice=False, any_prior=None, reward_items=None):
    qid = "side_choir_first_oath_" + entry["key"]
    did = "warden_oath_" + entry["key"] + "_dialogue"
    objective = {
        "id": "warden_oath_" + entry["key"] + "_objective",
        "kind": entry["kind"], "targetId": entry["target"], "requiredCount": 1,
        "description": entry["objective"], "dialogueId": did,
    }
    q = {
        "id": qid, "arcId": "the_choir_beneath_the_lake", "stage": -1, "type": "side",
        "locationId": entry["location"], "giverId": entry["giver"], "title": entry["title"],
        "objective": entry["objective"], "objectives": [objective],
        "reward": {"gold": 4 if entry["key"] in {"open", "afterword"} else 2, "items": reward_items or []},
    }
    if prior:
        q["prerequisiteIds"] = [prior]
    if any_prior:
        q["prerequisiteGroups"] = [{"anyOfQuestIds": any_prior}]
    if branch:
        q["branchFlag"], q["branchValue"] = "first_oath_access_policy", branch
    if choice:
        q.update({
            "choiceFlag": "first_oath_access_policy",
            "choiceSpeaker": "THE FIRST WARDEN",
            "choicePrompt": "Choose how the Warden's account is kept. Both routes preserve the copy history and the undated limits.",
            "choices": [
                {
                    "id": "public_first_person",
                    "label": "Publish the Warden's signed first-person memory beside its limits and the later heading's date.",
                    "flagValue": "public_first_person",
                    "dialogueId": "warden_oath_choice_public",
                    "reward": {"gold": 0, "items": [{"itemId": "first_oath_public_pin", "quantity": 1}]},
                },
                {
                    "id": "private_folio",
                    "label": "Keep the full memory in a requestable private folio while publishing the method and copy history.",
                    "flagValue": "private_folio",
                    "dialogueId": "warden_oath_choice_private",
                    "reward": {"gold": 0, "items": [{"itemId": "first_oath_private_seal", "quantity": 1}]},
                },
            ],
        })
    return q

quests, dialogues, records, landmarks = [], [], [], []

def install_entry(entry, quest, choice=False, add_marker=False):
    quests.append(quest)
    dialogues.append({"id": "warden_oath_" + entry["key"] + "_dialogue",
                      "speakerName": entry["speaker"], "lines": entry["lines"]})
    records.append({
        "id": "warden_oath_" + entry["key"] + "_record",
        "title": entry["record_title"], "category": "The First Oath's Missing Measure",
        "writtenBy": "Lyra Moss", "unlockQuestId": quest["id"], "body": entry["record_body"],
    })
    if entry["kind"] == "inspect" or choice or add_marker:
        if entry["visual"] and entry["position"]:
            x, y = entry["position"]
            landmarks.append({
                "id": "warden_oath_" + entry["key"] + "_marker",
                "locationId": entry["location"], "displayName": entry["title"],
                "targetId": entry["target"], "visualId": entry["visual"],
                "positionX": x, "positionY": y, "scale": 0.085,
            })

prior = "choir_reckoning"
for entry in common:
    quest = make_quest(entry, prior=prior, choice=entry["key"] == "policy",
                       reward_items=([{"itemId": "echo_kelp_seed", "quantity": 2},
                                      {"itemId": "earthworm_bait", "quantity": 8}]
                                     if entry["key"] == "open" else None))
    install_entry(entry, quest, choice=entry["key"] == "policy")
    prior = quest["id"]

dialogues.extend([
    {"id": "warden_oath_choice_public", "speakerName": "THE FIRST WARDEN",
     "lines": ["Let the account be read under my name, with the date left open.",
               "The heading may remain beside it if the later hand is named."]},
    {"id": "warden_oath_choice_private", "speakerName": "THE FIRST WARDEN",
     "lines": ["Keep my full memory in the requestable folio. Publish the test method and the page history.",
               "I will decide when the private words are read."]},
])

branch_ends = []
for branch, entries in (("public_first_person", public), ("private_folio", sealed)):
    previous = "side_choir_first_oath_policy"
    for entry in entries:
        quest = make_quest(entry, prior=previous, branch=branch)
        install_entry(entry, quest)
        previous = quest["id"]
    branch_ends.append(previous)

previous = None
for entry in shared:
    quest = make_quest(entry, prior=previous, any_prior=branch_ends if previous is None else None)
    install_entry(entry, quest)
    previous = quest["id"]

items = [
    {"id": "first_oath_memory_charm", "name": "Listening Weight of the First Oath",
     "description": "A Choir field charm weighted for repeatable listening depth. It stores no voice and cannot reconstruct the first bell. Increases Might and Guard by 1.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
    {"id": "first_oath_public_pin", "name": "First-Hand Folio Pin",
     "description": "A pin marking a first-person account whose date and source remain visible. Increases Might by 2.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 2, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "first_oath_private_seal", "name": "Requestable Folio Seal",
     "description": "A seal that records openings while leaving the speaker in control of access. Increases Guard by 2.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 0, "guardBonus": 2, "healAmount": 0, "sellValue": 0},
]
recipe = {
    "id": "forge_first_oath_memory_charm",
    "displayName": "Forge the First Oath Listening Weight",
    "stationId": "choir_harmonic_anvil",
    "discipline": "smithing",
    "outputItemId": "first_oath_memory_charm",
    "outputQuantity": 1,
    "ingredients": [
        {"itemId": "echo_kelp", "quantity": 1},
        {"itemId": "whisper_koi", "quantity": 1},
        {"itemId": "choir_mote", "quantity": 1},
    ],
}
encounter = {
    "id": "choir_first_oath_merrow",
    "monsterId": "tiny_ch_choir_merrow",
    "locationId": "choir_beneath_lake",
    "positionX": -2.0, "positionY": 3.8,
    "requiredQuestId": "side_choir_first_oath_gate",
    "blockedQuestId": "", "blockedDialogueId": "",
    "contributesToQuest": True,
    "defeatObjectiveTargetId": "tiny_ch_choir_merrow",
    "defeatDialogueId": "warden_oath_merrow_down",
    "downDialogueId": "rowan_field_retreat",
    "reward": {"gold": 3, "items": [{"itemId": "choir_mote", "quantity": 1}]},
}
dialogues.append({
    "id": "warden_oath_merrow_down", "speakerName": "THE FIRST WARDEN",
    "lines": ["The passage is clear. The mote came from the Merrow's nest, not from a stored voice.",
              "Lyra can use it to fix the test depth without opening a human recording."],
})

for filename, additions in [
    ("prologue_quests.json", quests),
    ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", records),
    ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items),
    ("recipe_catalog.json", [recipe]),
    ("encounter_catalog.json", [encounter]),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} quests, {len(dialogues)} dialogue entries, {len(records)} field records, "
      f"{len(landmarks)} landmarks, {len(items)} items, one recipe and one gated encounter.")
