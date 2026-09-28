#!/usr/bin/env python3
"""Add a second, character-focused hearing layer to the First Oath codex route."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS_PATH = ROOT / "Assets/Resources/Content/prologue_quests.json"
CODEX_PATH = ROOT / "Assets/Resources/Content/codex_catalog.json"
MARKER = "\n\nSecond hearing —"

NOTES = {
    "warden_oath_open_record": """Second hearing — the man behind the witness

After the interview, the Warden waits beside the open doorway while Rowan returns the transcript to its sleeve. He asks what Rowan would have written if no one had called him a witness first. Rowan says he probably would have described a tired man refusing to guess. The Warden laughs once, then asks Lyra to preserve that answer as Rowan's impression, not as a new title for him.

He wants visitors to meet him before they decide what his age, memory or office should prove. Lyra adds a small note to the archive index: questions are welcome, but the Warden may end an interview without giving a reason. The invitation belongs to him; the archive cannot make him available on every visit.""",
    "warden_oath_bell_rim_record": """Second hearing — a bell does not keep the names of listeners

Lyra taps the bell once with a felt-covered mallet and asks the Warden which part of the sound he remembers. He says he remembers people becoming quiet before the strike, though he cannot tell whether the hush came from this room or from a later telling. Lyra puts the memory in his interview and leaves the bell's present tone on the measurement card.

When Rowan asks whether he wants the mallet placed at the old height, the Warden declines. He would rather hear today's test from where he stands now. The three of them listen without trying to recreate the past. Lyra writes that no person present spoke for the others who may once have gathered around the bell.""",
    "warden_oath_lyra_record": """Second hearing — Lyra names the work she inherited

Lyra shows Rowan how many times she has copied the Warden's page. The count is low enough to fit on one strip of paper, yet each copy changed the route by which a reader encountered the story. She used to feel proud when a title helped visitors remember the account. Seeing the attached heading beside the speaker's own sentence makes her wonder which version she taught first.

She does not ask the Warden to absolve her. He says the copies are part of the archive now, including the one she made before she understood the seam. Lyra records her responsibility in her own name. The Warden's memory stays his; the copy history belongs to the people who handled it.""",
    "warden_oath_kelp_record": """Second hearing — tending something that will outlive the visit

Rowan ties a loose Echo Kelp frond back to its support after the tone test. The Warden watches him work and asks whether the garden bed belongs to the Choir or to the people who tend it. Lyra says the bed is maintained by the current gardeners, and its schedule can change when they need it to. She cannot say who first put kelp in the water.

The Warden likes that answer. He has spent too long inside a record that keeps returning to its beginning. A living bed asks for a next day without requiring anyone to repeat an old promise. Rowan leaves the garden card with a blank date for the next gardener to choose.""",
    "warden_oath_koi_record": """Second hearing — a fish gives the crew something ordinary to share

After the sample is filed, Rowan and Lyra cook the catch at the small shore brazier. The Warden sits with them but does not join their discussion of the old phrase. He asks Rowan how the fish was prepared and whether the current had been kind to the line. Rowan explains that the catch took longer than expected because he had to move away from the bell's reflection.

Lyra writes nothing from their meal in the oath folio. It is not evidence, and the Warden asked for an evening without questions. She keeps the conversation in her own memory instead. The record needs room for him to be a guest at a table, not a source being harvested for another answer.""",
    "warden_oath_gate_record": """Second hearing — the passage was dangerous before it was a page

The Warden sees the pouch holding the Choir Mote and moves his chair farther from it. He does not call the creature a guardian or a punishment. He remembers that the lower passage was unsafe in one of his visits, but cannot tell whether the same nests were there. Rowan asks whether the old account mentioned the threat. The Warden says it mentioned leaving before the lamps failed.

Lyra adds the memory to his interview log, then walks Rowan through the path they cleared. She checks each marked exit and leaves the pouch in the materials chest. They do not carry the Mote into the hearing room. A safe route for today's crew and an account of an earlier journey are separate records.""",
    "warden_oath_craft_record": """Second hearing — Rowan is allowed to change the instrument

Tomas Reed checks the Listening Weight before the next session. Rowan asks to move its handle so it can be used from the lower step without leaning over the pool. Tomas agrees to draw a second grip and label it as a later alteration. The first version stays in the case rather than being treated as a failed design.

The Warden approves of the change because it lets the next listener choose a safer position. Lyra notes that he did not approve the historical account or the phrase attached to it; he approved a tool for present use. Rowan signs for the modification. The instrument can develop as long as its records show which measurements came from which form.""",
    "warden_oath_time_marks_record": """Second hearing — a broken line can remain readable

Rowan catches himself smoothing the copy where the repair bands interrupt the stone marks. He was trying to make a diagram another cadet could read quickly. Lyra asks him to draw the interruption back in. The cleaner version would save a reader a moment and cost them the chance to see what could not be measured.

The Warden says the first time he saw the marks, he thought they pointed toward an answer. He no longer remembers which mark made him think so. He does remember being pleased when the map was simple. Rowan leaves that admission in the conversation record, separate from the drawing. The archive now shows both the urge to make a clean diagram and the choice to leave its limits visible.""",
    "warden_oath_stairs_record": """Second hearing — they trade the place from which they listen

Lyra takes the upper stair while the Warden sits at the doorway. Rowan stands below and speaks the test phrase at a steady volume. The Warden hears it clearly; Lyra hears the water cover the last word. They trade places, and the result changes with the channel gate. No one chooses which listener was correct because each heard the room from a different position.

The Warden smiles when Rowan writes both accounts. For centuries, readers had asked him to describe the chamber as though his location never changed. This time the archive names where each person stood. Lyra asks whether he wants a third reading next season. He says anyone can do it, but he owes no one another demonstration.""",
    "warden_oath_first_promise_record": """Second hearing — the Warden resists becoming a lawgiver

Rowan asks what the Warden meant to protect when he made the first promise. The Warden answers with a person he can still picture carrying a wet cloak out of the bell room. He cannot remember the person's name, and he will not let Lyra place a guessed name beside the image. He says the promise felt narrow then: keep a particular confidence, for a particular person, in a particular room.

The later heading made it sound like he had accepted an office over generations. The Warden does not deny that he served the Choir afterward. He asks the archive to keep those two facts apart. Lyra lets the pause after his answer remain in the transcript, rather than replacing it with a summary of what she thinks he feels.""",
    "warden_oath_lyra_layers_record": """Second hearing — Lyra hears her own voice in the copies

Lyra reads three versions of the heading aloud. The first sounds like a clerk giving a shelf instruction; the second sounds like a rule; the newest sounds like a warning. She had once believed the later versions were simply more polished. Now she hears her own careful tone making the sentence firmer every time she repeated it.

The Warden says he understands why people want a short line to remember. He asks Lyra to keep the versions side by side, including the one she prefers. She worries that naming her influence will make the archive look less reliable. Rowan says a reader can judge the work only if the work is visible. She adds her initials to the copy history and leaves the original untouched.""",
    "warden_oath_light_test_record": """Second hearing — no lamp can illuminate an absent witness

The light test leaves a narrow band along the current waterline. Rowan moves the lamp, and the band follows it. Lyra asks whether the Warden remembers a lamp in the chamber during the promise. He remembers a warm glow but is uncertain whether it came from a lantern, a threshold or the later archive room. He asks that none of those sources be selected for him.

The team files three present-day sketches under their respective lamp positions. The Warden is invited to correct his interview later if a detail returns, but the page does not reserve a line for a confirmation he may never give. Light reveals the shape of the chamber today. It cannot illuminate the choice another person made centuries ago.""",
    "warden_oath_archive_copy_record": """Second hearing — the clerk who added a title is still unknown

Rowan asks if finding the clerk's name would settle the disagreement. The Warden says it might explain who joined the pages, but not whether the title helped, harmed or both. Lyra notes the question on a list of possible archive searches. She does not attach it to a suspected person or describe the unknown clerk as an enemy.

The Warden once wanted to know who made the change. Now he is more interested in letting readers see when it happened. He says a name could invite people to stop reading at the person's door. The copy history is a chain of choices, including choices made by later custodians. Rowan files the search request without promising it will find an answer.""",
    "warden_oath_private_memory_record": """Second hearing — choosing what not to remember aloud

The Warden declines one of Lyra's questions and looks toward the water instead. She closes her notebook and asks whether he wants the room cleared. He asks her to stay, but not to resume the interview. Rowan waits at the doorway. They sit together until the sluice's next cycle can be heard from the lower passage.

Later, Lyra writes that the interview stopped at the Warden's request. She does not add the subject he declined to discuss. A refusal may be recorded as a boundary without turning the hidden content into another mystery for visitors to solve. When they meet again, he may choose a different question; he is not required to explain this one.""",
    "warden_oath_measure_card_record": """Second hearing — three cards, three chances to correct

Lyra lays the measurement card, the interview page and the copy-history leaf on separate cloths. Rowan sees that he had written “first” in the margin of the measurement card, although it was the first test of the day rather than the first test ever made. He circles the word and adds a correction without erasing it.

The Warden asks that every replacement card list which older card it supersedes. He wants future readers to follow the sequence, including false starts. A clean desk can make all three sources look like one account. The new tray keeps them nearby but physically separate, so the next person can compare them without blending authorship.""",
    "warden_oath_policy_record": """Second hearing — the Warden asks to be told what the policy changes

Lyra reads the access policy to the Warden before filing it. He pauses at the paragraph explaining who can request a copy. He asks whether the policy also tells a custodian how long a request may sit unanswered. It does not. Rowan adds a response date and a contact point, then reads both lines back to him.

The Warden says he does not need the archive to promise that every request will be granted. He needs it to promise that a request will not disappear into a drawer without a reply. Lyra adds a way to contest a refusal. The policy has a custodian, but it also names the person affected by that custodian's decision.""",
    "warden_oath_public_open_record": """Second hearing — speaking in public is not the end of a choice

At the courtyard reading, the Warden asks Lyra to leave a clear space beside his statement so listeners can submit questions later. He speaks the account himself and waits through the first silence. One person asks where the copy was stored; another wants to know who may correct the heading. No one asks him to list every voice from the old room.

Lyra files the questions without attributing them until the listeners choose to sign. The Warden can answer a later question privately or decline it. Public access means people can hear him, not that they acquire a claim to all his memories. He leaves before the crowd has fully dispersed, and the archive notes the time without recording a reason.""",
    "warden_oath_public_folio_record": """Second hearing — an index can invite a reader without directing them

Lyra removes a decorative arrow from the first public folio layout. It pointed toward the Warden's signature as if his name were the correct ending of every page. She replaces it with an index of sources: his memory, the later heading and the present measurement. A reader can begin with any of them.

Rowan asks whether people will understand the folio without a guide. Lyra says they can ask for one, but a guide must identify when it is explaining and when it is interpreting. She adds a note beside the index asking readers to compare dates before drawing conclusions. The public version is complete enough to navigate and open enough to question.""",
    "warden_oath_public_method_record": """Second hearing — a visitor chooses not to repeat the test

During the demonstration, one visitor reads the method card and decides not to stand on the wet step. Rowan offers a dry position farther back. The visitor chooses to watch instead. Lyra had worried that the public method would be mistaken for an invitation to imitate every setup; she adds an optional observer role to the card.

The Warden appreciates the change. A method should explain how a reading was made, but it should not press a person to expose themselves to risk to prove they understand it. The visitor asks for a copy and leaves without touching the rig. Lyra writes down the request with permission, not the visitor's name. Participation remains available without becoming an obligation.""",
    "warden_oath_public_lyra_record": """Second hearing — Lyra lets someone else read the heading first

At the review, Lyra asks Rowan to read the heading before she does. He hears it as an instruction from a past custodian; she hears the sentence she has repeated for years. Their readings are not the same, though both can point to the same ink. The Warden listens and asks them to leave their interpretations signed beneath their names.

Lyra feels relief when Rowan gives a different reading. It means the archive can make room for disagreement without deciding which person has failed to understand. She adds a margin where future readers may describe their own first impression, then keeps the original heading unchanged.""",
    "warden_oath_public_margin_record": """Second hearing — the empty margin is not a missing witness

The question box stays empty through the first week. Lyra resists the urge to ask people to write something simply so the space will look used. The Warden jokes that he has spent enough of his life being surrounded by empty spaces that acquire meaning without him. Rowan asks if the joke belongs in the account. The Warden says it may stay as his present remark.

Lyra writes “no questions submitted during this period” on the review sheet, not “no objection.” The difference protects a reader who walked past the board or never saw it. A blank margin can record the state of the page without claiming to know the thoughts of everyone who saw it.""",
    "warden_oath_public_sign_record": """Second hearing — the Warden reads his signature in his own voice

He traces the signature on the public copy with one finger and tells Lyra which letters he still writes quickly. Rowan notices that his hand is steadier than it was during the first interview. Lyra records the observation only after asking him. The signature dates this copy and identifies its speaker; it does not confirm the later heading above it.

The Warden asks the archivist to stop calling the mark his approval. She agrees and changes the label before the next reading. A signature can authorize one act while leaving surrounding pages open to challenge. The revised caption names the act he chose: he signed the first-person copy for public reading.""",
    "warden_oath_public_board_record": """Second hearing — a correction box needs someone who checks it

Rowan volunteers to bring the public questions to Lyra each evening. She asks him to keep the sealed letters in a separate tray and to record the time he delivered the others. The Warden points out that a correction path without an assigned receiver is only a box with good intentions.

They add an alternate contact for the days Rowan is away and a note that says when the next review will occur. Lyra will acknowledge a correction even if the archive cannot accept it. The public board can now receive a disagreement without making the person who wrote it argue alone against a locked shelf.""",
    "warden_oath_public_after_record": """Second hearing — The Warden asks what the courtyard took from him

After the courtyard reading, Rowan asks whether the Warden feels exposed. He says he felt watched before the first word and tired by the last. He also heard people discuss the page with one another instead of asking him to settle every disagreement. Both parts matter. Lyra asks whether he wants the reading repeated. He says he will decide after resting.

She records his answer without turning it into a recommendation for future witnesses. A public account can create relief and fatigue at once. The next speaker will need their own terms, and the Warden's experience cannot serve as a template they must follow.""",
    "warden_oath_sealed_open_record": """Second hearing — privacy is still a relationship with a reader

The Warden asks who can tell him what happens to a private request after it enters the registry. Lyra describes the numbered receipt and the person responsible for replying. He asks whether he can change the custodian if they stop answering. The rule allows a review request, so she shows him where to file one.

He chooses to keep the folio sealed for now. Lyra notes that this decision leaves a relationship in place: a speaker trusts a custodian to respect a boundary, and the custodian owes the speaker a response. The public index explains that relationship without repeating the private words.""",
    "warden_oath_sealed_receipt_record": """Second hearing — the holder brings the receipt to the speaker

Lyra carries the blank receipt to the Warden before she signs as custodian. They read every field together. He asks that the line for a witness remain optional, because requiring someone else to observe his choice would disclose the request itself. She changes the form and gives him a copy to keep.

The receipt is no longer proof only for the shelf. The speaker can use it to ask what happened to his file, while the archive can use its own copy to track custody. Rowan writes the form number, then leaves the witness line empty. No one present treats the missing signature as evidence that the Warden did not consent.""",
    "warden_oath_sealed_lyra_record": """Second hearing — Lyra must be willing to say she cannot tell the story

A visitor asks Lyra what the restricted folio contains. She says she cannot summarize it and explains how the visitor may ask for access if the Warden permits it. The visitor is disappointed and asks whether Lyra could at least tell them the conclusion. She repeats the same boundary without adding a hint.

Afterward, Rowan asks if that felt like protecting the Warden or protecting herself. Lyra admits it was both; she is afraid of becoming the person who decides which parts of his story are useful. She writes the exchange in her custodian journal, not in the public index. A boundary can be kept for the right reason and still be difficult to hold.""",
    "warden_oath_sealed_method_record": """Second hearing — Rowan explains the method without offering the memory

Rowan teaches a new keeper to set the Listening Weight and read the waterline. The keeper asks whether the Warden will attend the trial. Rowan says the method works without him and that the Warden decides for himself whether to join. They complete the setup with the chair empty.

The result is easier to compare because no one tries to match it to a particular phrase. Lyra adds the empty-chair condition to the public procedure so future teams do not infer that a private witness must be present. The test can be repeated with ordinary consent and an appropriate safety check; the sealed folio remains closed.""",
    "warden_oath_sealed_copy_record": """Second hearing — the copyist's mark does not unlock the private case

Rowan asks whether the later heading's visible seam should give researchers a path to the sealed folio. Lyra says the seam belongs to the public copying history. It can be studied without opening the Warden's words. She moves the case farther from the display table and puts a separate request form by the index.

The Warden reviews the new arrangement and agrees that visitors may inspect the seam drawing. He does not authorize anyone to read the private copy. The boundary is written on the access card, not left for Lyra to enforce alone in each conversation. A public clue is not permission to open a private page.""",
    "warden_oath_sealed_sign_record": """Second hearing — the Warden keeps the review date in his own calendar

Lyra offers to remind him when the review window arrives. The Warden says he would rather put the date on his own card, because a reminder from the archive might feel like pressure to reopen the folio. He asks Rowan to note where the request form can be found, then keeps the date card in his pocket.

The registrar records that a review is available and how to request it. The archive will not send an invitation unless the Warden asks for one. A right to reconsider belongs to him even when he does not exercise it on the timetable another person would prefer.""",
    "warden_oath_sealed_mark_record": """Second hearing — a damaged seal starts a conversation, not an accusation

One edge of the wax appears crushed after the case is moved. Lyra stops the inspection, calls Rowan to witness and opens the handling ledger before touching the flap. The Warden waits in the room. They photograph the mark, compare the case number and find no sign the folio itself was opened.

Lyra records the damaged edge and replaces the seal under a new number. She does not write that someone tried to break in; they cannot establish how the wax was crushed. The Warden thanks Rowan for staying, then asks them to finish the inspection. A visible irregularity requires a process everyone can see, not an invented culprit.""",
    "warden_oath_sealed_after_record": """Second hearing — the Warden spends the afternoon outside the archive

The group finishes reviewing the public index, then Rowan asks whether the Warden wants to remain in the chamber. He asks where the upper garden path leads and walks there with Lyra. They talk about the sound of ordinary rain on the terrace, which does not echo like water inside the Choir.

Lyra does not turn the outing into a test of his memory. The Warden returns before dusk and chooses to leave the folio sealed. His day included both the archive and a place where no one asked him to reconstruct it. She writes no attendance count in the restricted record.""",
    "warden_oath_new_test_record": """Second hearing — Rowan learns to stop a trial before an answer

The new test begins with the tone drifting after the first reading. Rowan checks the gate and finds that a worker has started the next water cycle. He asks to pause rather than finish the set under a changed condition. Tomas marks the partial result and stores the weight until the chamber settles again.

The Warden says stopping is a choice he wishes he had recognized earlier in life. He does not connect that regret to the exact day of the first oath. Lyra records his words as a present reflection. Rowan waits for the next cycle and starts a fresh card instead of trying to rescue the interrupted sequence.""",
    "warden_oath_second_kelp_record": """Second hearing — the garden needs a keeper who can disagree

Lyra finds a new shoot bending toward a patch of light Rowan had not marked. She suggests moving the tray so the two samples receive the same conditions; the gardener says the difference is why they should leave them where they are. They talk through both options and decide to make a second pair rather than disturb the growing plant.

The Warden listens as they disagree without raising their voices. He asks who has the authority to decide where the new kelp goes. Lyra points to the people tending that bed. They add a second planting card and let the gardener choose the placement. The next measurement will depend on a decision openly made today.""",
    "warden_oath_second_koi_record": """Second hearing — the sample does not belong to the loudest account

Two fishers return from opposite sides of the pool with different descriptions of the current. One calls it still; the other says it pulled toward the gate. Rowan remembers fishing from the eastern step and admits he may have felt only the surface. Lyra asks them to mark their positions before they discuss the difference.

The Warden says a disagreement can tell the team where to look next, even when nobody is lying. They keep both statements attached to the locations and leave the shared conclusion blank. The sample's journey through the pool matters as much as its name on a page.""",
    "warden_oath_lyra_review_record": """Second hearing — Lyra gives the copyist a right of reply

Lyra drafts a review of the later heading and leaves space for the unknown copyist or their family to submit another source. She does not expect a reply and will not send anyone to locate them. Rowan asks whether a right of reply matters when no one knows whom to contact. Lyra says the space also reminds the archive that its account could be incomplete.

The Warden approves the blank but not the review's conclusion. He wants his own response printed beside it, while the copyist's space remains open. The folio now shows two present voices and one unanswered place without claiming they carry equal evidence.""",
    "warden_oath_copy_review_record": """Second hearing — people changed the heading for different reasons

Lyra brings a box of later indexes. One writer used the heading to shorten a catalogue; another placed it over a painting of the Warden; a third cited it as an instruction. Rowan notices that readers acted differently while looking at the same line. Lyra adds the uses to a chronology instead of assigning them to one shared motive.

The Warden watches the pages fill the table and asks whether the archive should keep every copy. Lyra says she will preserve the differences that explain how the heading traveled, and note when a copy is too damaged to read. One sentence did not have one effect. Its history is made of separate hands.""",
    "warden_oath_warden_walk_record": """Second hearing — the Warden sets the pace of a walk

Rowan starts ahead and then slows when the Warden stops to look at the water reflected under the arch. The Warden asks to walk without a route marker for a while. Lyra folds the map and follows behind. They take a side path that ends at a closed garden gate; no quest opens there and no hidden inscription appears.

The Warden says he wanted to see a place without being expected to remember it for someone else. Rowan leaves his sword sheathed and waits while Lyra asks whether he wants company on the return. He accepts, then chooses the path back himself. The archive records the walk because he asked, not because every movement must become evidence.""",
    "warden_oath_future_marker_record": """Second hearing — Rowan does not write a question for the next person

Rowan sits beside the blank card and tries several openings before he stops. He had planned to ask the next listener what they would do with the old promise. The Warden points out that the question already carries Rowan's expectations. Rowan turns the card over and leaves both sides blank.

Lyra files the card as an available space, not an unfinished assignment. The next visitor may use it, replace it or leave it untouched. For the first time, Rowan lets the archive end a page without telling another person where to begin.""",
    "warden_oath_afterword_record": """Second hearing — the archive closes for an ordinary reason

At the end of the route, Lyra closes the reading room because the lamps need replacing. No final speech is scheduled. The Warden asks Rowan whether they can meet outside the Choir another day, with no transcript between them. Rowan says yes, then asks Lyra to keep that promise outside the catalogue unless the Warden changes his mind.

The archive records which pages remain available, which folio stays sealed and where a correction can be sent. It does not call the story finished. Lyra returns the key to its hook and leaves the visitor's chair pulled out for whoever chooses to come next.""",
}


def main() -> None:
    quests = json.loads(QUESTS_PATH.read_text(encoding="utf-8"))["entries"]
    data = json.loads(CODEX_PATH.read_text(encoding="utf-8"))
    quest_by_id = {quest["id"]: quest for quest in quests}
    entry_by_id = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entry_by_id.keys())
    if missing:
        raise SystemExit(f"Missing First Warden records: {', '.join(missing)}")
    for record_id, note in NOTES.items():
        entry = entry_by_id[record_id]
        quest = quest_by_id.get(entry.get("unlockQuestId"))
        if quest is None or quest.get("arcId") != "the_choir_beneath_the_lake":
            raise SystemExit(f"First Warden record is not linked to Arc 5: {record_id}")
        if MARKER in entry.get("body", ""):
            raise SystemExit(f"Second-hearing section already exists: {record_id}")

    before = sum(len(entry_by_id[key]["body"].split()) for key in NOTES)
    for record_id, note in NOTES.items():
        entry_by_id[record_id]["body"] += MARKER + "\n" + note
    after = sum(len(entry_by_id[key]["body"].split()) for key in NOTES)
    CODEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(NOTES)} First Warden codices with {after - before} words of second-hearing narrative.")


if __name__ == "__main__":
    main()
