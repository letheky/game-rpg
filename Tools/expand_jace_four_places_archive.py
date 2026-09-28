#!/usr/bin/env python3
"""Add laboratory notes to Jace Morrow's Four Places archive records."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental station archive note —"

NOTES = {
    "jace_four_places_open_record": """Supplemental station archive note — the case came back empty of names

Jace recognizes the brass corner guard and the shallow dent beside its latch. He cannot remember which surveyor carried the case on its final trip, and no cargo ledger names a keeper. The archive therefore records the person who returned it now, the desk that accepted it and the older origin as unknown. Jace adds his signature only to the present handoff.

He once thought the case should be displayed as proof that four people had left. Evelyn asks what connects an empty compartment to a person. Jace removes that sentence from the label and keeps the crossed-out draft with the revision slip. The case is evidence of a storage object and a gap in its paperwork; the gap remains open.""",
    "jace_four_places_case_record": """Supplemental station archive note — measure cavities before assigning cargo

The four hollows differ in depth by a few finger-widths. Jace numbers them from left to right as the case currently rests, then turns it around and confirms that the numbering follows the hinge rather than the room. A small liner shadow appears in the second hollow, but there is no matching piece of packing in the returned inventory.

Rowan records each interior measurement twice. Neither the dimensions nor the count of cavities tells them how many instruments were stored there. The labels stay as “space one” through “space four,” with no names attached. A later conservator can add a packing sample if one is found, without making the sample a roster.""",
    "jace_four_places_skyroot_record": """Supplemental station archive note — new fiber can test a new fit

The Skyroot sample was grown in Greenwake after the case returned. Jace writes the seed source, watering interval, harvest day and drying conditions on the bag before cutting a test strip. The current fiber bends without cracking against the metal lip. That gives Evelyn a safe material for checking the case's present edge; it does not show what the original packing looked like.

The sample is stored in a separate sleeve marked “modern comparison.” If later growth produces a different texture, that result receives a new card. Jace wants future crews to be able to repeat the fit check without mistaking a living plant from this season for an artifact from the missing survey.""",
    "jace_four_places_carp_record": """Supplemental station archive note — the pool had a sound that day

Jace holds the Farwake Carp's scale beside the receiver housing only after Rowan records where and when it was caught. The sample's moisture changes the sound when it taps the case; a dry table gives a sharper knock than the damp bank. Evelyn asks them to log the surface beneath the receiver too, so the fish sample does not become an unexplained “lake frequency.”

The test documents an ordinary environmental variation around the station. It cannot identify a past signal or prove that the carp heard one. Jace adds a line for water level and wind because the same pool may sound different on another visit.""",
    "jace_four_places_wind_record": """Supplemental station archive note — height changes the instrument reading

The ribbon is set at three heights beside the north window. It turns at the sill, rests against the middle peg and lifts above the roof edge; Jace repeats the sequence after Rowan moves to the other side of the post. Each observer stands on a chalk mark so the body does not block the airflow in a different way.

The sheet preserves the disagreements rather than averaging them. The wind reading describes this station, this hour and these positions. It does not fill the date column in the old survey ledger. Jace adds the observer's initials beside each height, since a later reader should know whose hands placed the ribbon.""",
    "jace_four_places_interval_record": """Supplemental station archive note — order is not a calendar

The recovered notes show that one receiver check came before a change to the case lining, and that a second check came afterward. The page corners are missing, so Jace cannot assign either check to a season. Evelyn draws arrows only where a physical cross-reference supports the order; she leaves the date line blank.

Jace initially writes “winter test” in the margin because he remembers cold air at the station. He replaces it with “temperature not recorded” and attaches the first draft. A memory can suggest a question for the archive. It cannot make a lost date reappear. The sequence remains useful even while its calendar position is unknown.""",
    "jace_four_places_receiver_record": """Supplemental station archive note — silence has several possible causes

The receiver was disconnected from the archive relay when Rowan found it. During the bench check it produces no signal, but the battery contact is corroded and the antenna joint moves under light pressure. Jace lists those conditions before anyone calls the instrument silent. After Tomas cleans the contact, the unit still records no incoming transmission during the short observation window.

That result is a bounded test, not a proof that no signal ever arrived. The log names the duration, power state and antenna position. Jace asks that another technician repeat it with a calibrated source before comparing the device with an older account.""",
    "jace_four_places_evelyn_record": """Supplemental station archive note — two ledgers use different clocks

Evelyn sets the field book beside the station clock ledger and circles the places where their readings can be compared. One clock ran slow during a cold night; the other was reset after maintenance without an entry for the correction. A timestamp written in the first book may therefore fall within a range when translated into the second.

Jace confirms which pages he signed, but he does not fill the uncovered intervals from memory. Evelyn adds a join table with source, correction and uncertainty for each conversion. The table makes the records easier to compare without making them one continuous timeline.""",
    "jace_four_places_draft_record": """Supplemental station archive note — the sentence outran the measurements

The draft says the four empty compartments belonged to the people who never returned. Jace wants the sentence to express what he feared when he saw the case, but the case has no roster or baggage tags to support that claim. Evelyn underlines the verb “belonged” and asks him to name the object that proves ownership.

Jace changes the line to say that four spaces remain unassigned in the current inventory. The earlier wording stays on a dated draft page so a later editor can see why it was removed. The correction does not make his fear false as a feeling; it keeps that feeling from being used as evidence about four unknown people.""",
    "jace_four_places_policy_record": """Supplemental station archive note — decide who may read before copying

Jace and Evelyn separate the method sheet, the equipment account and any personal recollection before they choose a release policy. The public route gives readers the calibration steps and the conditions needed to repeat them. The folio route carries the named recollections under a request rule. Both copies retain the same empty identity fields and correction path.

The archive records the policy choice after the case inventory is complete. It does not let a desire to publish override the people named in a private account. Jace signs his own section in either route; the choice governs its audience, not whether he accepts his earlier signature.""",
    "jace_four_places_public_method_record": """Supplemental station archive note — publish enough to repeat the setup

The open method card includes the window position, three ribbon heights, receiver power state, case measurements and the duration of the listening interval. It omits household messages and the names of anyone who has not agreed to be quoted. A second reader checks the diagram against the station before the card is posted.

At the bottom, an unprinted margin provides room for a corrected value. Anyone repeating the method can add the date and their equipment serial, then request a revision if the instructions are unclear. Jace wants the procedure to outlive his memory without pretending the method explains the old survey's missing roster.""",
    "jace_four_places_public_index_record": """Supplemental station archive note — a visible blank is a deliberate result

The public index has four ruled fields for former case users. Each remains blank and is labeled “not identified in the returned records.” The phrase is longer than a dash, but Jace prefers it because a dash might look like a printing error or an invitation to guess a name.

The index links to a correction channel that accepts a source document, date and permission to quote. It does not ask a visitor to submit a likely identity. The empty fields can change if checked evidence arrives; until then, the public page makes the limit visible instead of hiding it in a footnote.""",
    "jace_four_places_private_receipt_record": """Supplemental station archive note — a receipt can have an exit path

The folio receipt identifies which copy left the archive, who may request its return and how a correction can be attached. It leaves the comment field empty unless the holder chooses to write something. Jace asks that each handoff record the copy number without repeating private names on the outer wrapper.

If the holder returns the page unread, the receipt records the handoff back, not a judgment about its contents. The family can ask for a replacement under a new rule later. A document can leave the archive without the archive claiming that its reader agreed with the account.""",
    "jace_four_places_private_folio_record": """Supplemental station archive note — the seal does not solve the inventory

The private folio contains Jace's signed recollection and a drawing of the case. It does not contain a roster because no verified roster was found. A restricted holder may inspect the material and request a correction, but access itself does not assign the four hollows to four people.

Evelyn keeps the calibration method outside the folio so the public can repeat a test without seeing personal pages. The folio's cover carries a copy number and review date, not a family name. Its seal protects access under the agreed rule; it cannot authenticate an unsupported sentence or make missing equipment records complete.""",
    "jace_four_places_afterword_record": """Supplemental station archive note — leave the case usable to the next crew

Jace leaves a maintenance card beside the public method and a request route beside the private folio. The card says when to inspect the hinge, how to replace the Skyroot liner and where to enter a new receiver test. It also tells the next crew not to mark a space with a person's name unless a source can be checked and permission is clear.

The four compartments remain four spaces in a returned case. The signal source, the former users and the survey crew's final route are still unassigned. Jace signs the afterword as the person who prepared this index today, leaving future evidence room to arrive under its own date.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Four Places records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Jace station records; added {after - before} words.")


if __name__ == "__main__":
    main()
