#!/usr/bin/env python3
"""Extend Arc 8 codices about the final choice, consent records and watch rotations."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental Last Oath archive note —"

NOTES = {
    "aldens_unfinished_ledger": """Supplemental Last Oath archive note — leave both columns in the book

After Rowan reads the last page, Alden asks him to keep the ledger open on the table rather than carry it straight to the cairn. A clerk has penciled a short forecast beneath each column: how much seed might remain if the Crown is accepted, and how much labor the outer passage would need if Rowan leaves. The margins do not agree on their assumptions. Alden refuses to let Rowan choose between two tidy totals that hide different people behind them. He adds the source beside each estimate and leaves the rest of the line empty. The ledger can inform the decision, but it cannot sign the oath for its reader.""",
    "consent_call_dates": """Supplemental Last Oath archive note — send the question before the meeting

Rowan asks Alden whether a person who received the call sheet could answer before the council met. Alden searches the box for a reply slip and finds none. There may have been verbal answers that never entered the file, so he does not mark every recipient as silent. He adds a new blank receipt card to the copy room, with separate spaces for delivery, reading and answer. A person can return it privately or leave the answer field empty. The current archive cannot repair the sequence used in an earlier cycle. It can make the next call arrive with room for a response before the decision has already been scheduled.""",
    "consent_dispatch_dates": """Supplemental Last Oath archive note — the courier's route is not an answer

The courier's route map shows that the sealed notices reached the east gate before the council session. It does not show which person carried each envelope after the gate, or whether the intended reader opened it. Rowan copies the delivery marks onto a separate sheet and keeps the recipient field unresolved where the seal obscures it. Alden recognizes a stamp from the old dispatch office but cannot identify the clerk who used it. The dates help reconstruct the order of events; they do not reveal what a recipient understood. A future letter may fill one gap without filling every one. The archive holds the map beside the call sheet, not in place of it.""",
    "first_refusal_record": """Supplemental Last Oath archive note — remember the question before the legend

The Warden returns to the council chamber with Rowan and stops beside the stone lip where the champion once set his folded map. The map is gone; a shallow dust line remains beneath the later supply ledger. He can still point to where the champion asked if the people might live without selecting a vessel. He cannot supply the answer the council gave. Rowan asks whether the Warden could have insisted that the question be copied into the record. The Warden says he remembers making room for the convoy list instead. His regret belongs to this witness. It does not tell Rowan what the first champion would choose today.""",
    "emberroot_trial": """Supplemental Last Oath archive note — leave the planting note with the seed

Mara asks Rowan to return the unused Emberroot seed to the keeper who loaned it, rather than seal it inside the public trial file. The keeper agrees to let one seed remain in the archive packet until the next review, with a note that it is borrowed and may be reclaimed. Rowan writes the germination conditions on a separate card so the sample can be replanted without treating its current owner as a permanent supplier. The harvest supplies one narrow trial. The seed could fail in another patch, and a future grower may decline to lend more. Evidence of a possible crop is not permission to requisition it.""",
    "starlit_sample": """Supplemental Last Oath archive note — the pool has no duty to answer twice

Evelyn checks the observation card against the passive receiver's time marks. The clock drift leaves a window rather than an exact moment, and the minnow's return to the shadow overlaps that window only within the margin of error. She asks Rowan to retain both timings and to avoid drawing a line from the fish to the signal. The animal was returned to the pool; no one has permission to capture it repeatedly just to make the chart look convincing. A future observation can use another method or another day. The current result is worth keeping because it shows what the team saw and where the timing remains uncertain.""",
    "signature_compare": """Supplemental Last Oath archive note — a mark can authenticate a handoff

Tomas checks the sword tracing beside an ordinary work-order signature. The cuts on the blade were made with a narrow tool at different depths; the ink signature follows a separate pressure pattern. He can compare the physical marks, but he cannot infer how many people agreed with the order from the way Alden signed his name. Nia labels the sheet as a comparison of objects, not of consent. Rowan keeps the roster's return marks on another page so a reader will not mistake a weapon for a list of witnesses. Each source proves a different act. Neither completes the record of the people who never returned.""",
    "consent_archive_draft": """Supplemental Last Oath archive note — review the key rule before a name is requested

The two custodians read the draft procedure aloud before any family asks to open a sealed page. They notice that the first version says who may request access but not who must answer if both custodians are away. Nia adds an alternate contact outside the office that stores the packet and writes a maximum response date beside the appeal route. A late answer will be logged as late, not treated as permission to publish. Alden asks to sign the cover as commander; the reviewers tell him his role does not give him authority over another person's record. He signs only the receipt showing the procedure was reviewed.""",
    "consent_named_archive": """Supplemental Last Oath archive note — publication does not end the correction period

A person named in the public copy returns with a different spelling on a letter written by their own hand. The page has already been read aloud at Crownfall, so Nia cannot make the first copy disappear. She adds a correction slip that preserves the earlier version and asks the person which spelling should appear in the next printing. The contributor chooses the corrected spelling and asks that the old one remain visible only in the revision history. The request changes that record alone. It does not authorize the archive to rename other people or describe every champion as willing. The public edition remains open to correction after release.""",
    "consent_sealed_archive": """Supplemental Last Oath archive note — inspect the seal without opening it

The seal arrives with one edge softened by damp. The custodians photograph the packet from four sides, compare the cord with the closure mark and log the condition before deciding whether it must be opened for preservation. The family receives the condition report and can choose whether to attend a supervised inspection. The packet stays closed while they decide. Nia adds a line for the reason if the seal is broken, so a necessary repair cannot be mistaken for unauthorized access. A locked file still requires care, review and a route to challenge the custodian. Privacy lasts only while those duties are visible.""",
    "alden_watch_arrival": """Supplemental Last Oath archive note — leave the blank hour unresolved

Mara compares the shift book with the small fuel tally kept beside the floodgate. The tally shows that someone added kindling during the missing hour, but it does not identify who rested or whether the watch changed hands. Alden first wants to copy the mark into the rest column. Nia asks him to preserve it as a separate observation with its own source. The blank remains on the original page, while the fuel note is indexed next to it. A person may have tended the gate without signing the roster; the book does not settle that question. The new copy makes the gap easier to see, not easier to fill.""",
    "alden_watch_interview": """Supplemental Last Oath archive note — commander, take the first unassigned shift

During the test rotation, the hour before dawn has no volunteer. Alden offers to take it himself, then asks the people already present whether his doing so would prevent anyone from requesting a later change. They agree to try the shift once, with a rest period afterward and no penalty if the hour proves difficult. Alden records himself as the person on duty, not as the person who assigned it. The distinction matters to him because he has spent years using an order as a substitute for asking. One night of a different practice cannot rewrite the old ledger, but it gives the next keeper a procedure to review.""",
    "alden_emberroot_rest": """Supplemental Last Oath archive note — keep the frost line beside the watering time

The gardener returns to the bed before sunrise and finds a white line of frost on the outside stone, but none on the soil under the roof edge. Rowan compares the mark with the watering card and sees that the bed was watered earlier than the exposed plot. They record both facts without claiming that the shelter alone protected the plant. The gardener asks to keep one living root in the soil until the next shift can inspect it. Alden writes the request beside the harvest date and removes the root from his supply estimate. The crop trial can continue only if the person tending it chooses to continue.""",
    "alden_starlit_interval": """Supplemental Last Oath archive note — schedule the rest even when no fish is caught

On the next cast, Rowan waits through the same quiet interval and brings back no Minnow. Alden notices that the shift book has a field for catch and no field for the time spent beside the water. He adds a separate observation for an empty hook and a line for the fisher's rest period. No one has to cast again to earn a break. The lake may offer no food, and the quiet hour still belongs to the person who stood watch. Alden crosses out a note suggesting that the catch could supply a night meal. A single successful cast never made the schedule dependable.""",
    "alden_watch_spindle_record": """Supplemental Last Oath archive note — release the page before filing a correction

Nia demonstrates the spindle by turning its two grips until the watch sheet lifts free without tearing. She marks the original page number on its sleeve, then places a correction beside it rather than stitching the new page into the old one. Alden asks whether a loose page could be lost. Nia adds a return slot and a receipt so the person who takes it can bring it back or request a copy. The tool protects paper, not the truth of every line. Its value is that a reader can remove a record for review without destroying the revision trail or the original's custody history.""",
    "alden_sword_wear_context": """Supplemental Last Oath archive note — stop counting nights with the blade

Alden puts the sword away after the tracing is made. He used to touch the grooves whenever he believed he had stayed longer than the other guards. The marks became a private way of proving that he had carried the duty alone. When Rowan shows him the missing hour in the ledger, he sees how the blade's count left no room for anyone else's unrecorded work. He does not cut new grooves to represent them; that would turn his guess into their evidence. The tracing remains labeled with Alden's name and explanation. The other workers may submit their own account or leave the page untouched.""",
    "alden_roll_watch_comparison": """Supplemental Last Oath archive note — store the roll beside the watch book, not over it

The archive shelf has enough room for both volumes when they are laid flat. Lyra draws a small shelf map so a future clerk will not bind them under one title again. The cycle roll answers who was remembered at the Crown; the watch book answers what shift was written down at the gate. Their index cards carry separate date ranges and separate gaps. Rowan asks whether a name from the roll can be used to request the watch book. Nia says the archive can accept a request, but the name alone does not establish that the person stood a particular hour. Cross-reference is a path to search, not a proof of service.""",
    "alden_refusal_rule": """Supplemental Last Oath archive note — leave the reason field optional

The newest roster draft has a box labeled “reason for declining.” Alden catches it before the page is printed and asks who needs that answer. The gate only needs to know that the person will not take the shift; the private reason may involve illness, travel, family or nothing they want to explain. He removes the required mark and leaves a separate optional note that can be sealed if the person requests support. A refusal still requires the crew to find another plan. It does not require the person who refused to defend their character in the public ledger.""",
    "alden_named_optin_record": """Supplemental Last Oath archive note — a visible name belongs to one chosen line

Before the public roll is copied, each volunteer reads the description of where the page will be posted and how long it will remain there. One person agrees to show a name beside a single shift and declines to have it copied into the longer campaign record. Nia makes those permissions separate checkboxes. The name appears only on the shift line, and the review date applies to that copy. Alden wanted the public list to show a complete team. He accepts an empty place where someone chose not to publish. A roster may identify a volunteer without turning that choice into consent for every later use.""",
    "alden_household_copy_record": """Supplemental Last Oath archive note — household custody needs a way to travel

A household asks for its schedule to remain private but worries that the person carrying the copy may be away when a shift changes. Nia offers a sealed duplicate with the same revision number and a receipt showing which one is current. If the household changes its hours, it can return either copy for updating without listing members on the public board. The office keeps only the number of uncovered posts and the time they need another person. Alden asks whether the total could reveal a household's routine. Nia moves the public notice to a broader time block. Privacy is a practice that can be revised when a detail becomes too revealing.""",
    "alden_watch_afterword_record": """Supplemental Last Oath archive note — leave the next name to the next keeper

At the first review, the morning guard returns the spindle and chooses a different hour for the following week. Alden does not enter the choice for them. He marks that the schedule changed, removes the old public line at the volunteer's request and recalculates the open hours. The page records a working arrangement, not a promise that every gate will be covered. When Rowan carries the record toward the Oath Cairn, he leaves the next review box blank. The next keeper may use the same method, propose another one or close the roster. The final oath cannot make that future choice on their behalf.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - set(records))
    if missing:
        raise SystemExit(f"Missing codex records: {', '.join(missing)}")
    changed = 0
    added_words = 0
    for record_id, note in NOTES.items():
        record = records[record_id]
        if MARKER.strip() in record.get("body", ""):
            continue
        record["body"] = record.get("body", "").rstrip() + MARKER + note
        added_words += len(note.split())
        changed += 1
    if changed:
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {changed} Last Oath agency codices; added {added_words} authored words.")


if __name__ == "__main__":
    main()
