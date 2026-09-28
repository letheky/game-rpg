#!/usr/bin/env python3
"""Expand Nella Pike's Salt Road family-search records with custody context."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental family search note —"

NOTES = {
    "nella_missing_open_record": """Supplemental family search note — a file belongs to those it describes

Nella asks Rowan to place the pass card on a clean board while the family decides which parts may be copied. One relative wants the stamp drawn; another asks that the cord hole remain unphotographed because a household token once hung there. The two requests can coexist. Rowan records them on different slips so neither is treated as permission on behalf of the other.

The first catalogue entry names the objects and the current access rule. It does not ask the family to explain its worry or prove its connection before asking for privacy. Nella says the search can remain open while the copies stay limited. No public list is needed for the archive to remember where to look next.""",
    "nella_missing_card_record": """Supplemental family search note — measure the paper before reading the route

Rowan measures the trimmed edge from three corners and notes the spread between readings. The card bends near its cord hole; he supports the fold with a flat weight rather than forcing it level. A second drawing marks the stamp and notches at larger scale, with the card's outline kept beside them so a future reader can check that the details belong to this object.

Nella recognizes the shape of the punched hole but cannot date when it was made. The record distinguishes her recognition from the measurable crease. A later conservator can inspect the card without turning a family memory into an official date.""",
    "nella_missing_wall_record": """Supplemental family search note — the count depends on the wall's edge

Rowan photographs the plaster from straight on and from a shallow angle. The angled image shows a pale rectangle where a tenth hook may once have been, but there is no attachment left to count. They preserve both images and describe nine visible empty positions in the current frame. The damaged corner stays in the drawing as damage, not as a hidden name.

Nella remembers tags on the wall from several visits, not all at once. Her memory can direct a new search through stored labels, but it does not tell which hook held which tag. The public method card explains how the count was made without implying nine travelers or nine missing people.""",
    "nella_missing_ruth_record": """Supplemental family search note — Ruth's correction has a separate author

Ruth signs the date on which she disclosed the dispatch and the date on which she corrected its archive location. Those are two actions in the present investigation, not a reconstructed timeline for the old crossing. Nella reviews the reference number but does not countersign Ruth's statement. A family member should not have to certify a witness's account in order to retain control of a separate card.

Rowan adds a reference tab that lets the two documents be found together while keeping their custody histories apart. Ruth's responsibility for hiding the order can be recorded plainly without allowing the order to supply a name or destination it never contained.""",
    "nella_missing_docket_record": """Supplemental family search note — an overwritten tally remains visible

The Lockhouse clerk copies the docket on a sheet with a transparent window aligned over the overwritten row. A second copy shows the surrounding shelf numbers so later readers can locate the entry without handling the older ledger. They mark the two tallies as incompatible and preserve each version with its own source label.

Nella asks whether the larger number could include her sibling. No unit in the ledger says person, passenger or cadet; the written headings describe bundles. Rowan declines to convert one unit into another. The mismatch may help locate where a container record changed, but it cannot become an estimate of who passed through the Lockhouse.""",
    "nella_missing_return_mark_record": """Supplemental family search note — orientation is part of a trace

The rail chip is placed in a paper cradle so its salt crust is not scraped off by a glass vial. Rowan sketches which side faced the road and which side faced the return desk; Talia adds the height above the floor. A similar width on another surface is only a resemblance until the two objects' histories can be linked.

The pass card is compared in its sleeve and again on the flat board. Its edge has softened since the family first brought it in. The archive adds the new observation without changing the earlier measurement, preserving both dates and the handling conditions that may explain the difference.""",
    "nella_missing_skate_record": """Supplemental family search note — consumption is written on the receipt

The practice strip receives a small amount of scale film at one end, leaving the other end untouched for comparison. Talia records how much was used, who applied it and when the test was finished. The rest of the catch is not saved as an unexplained souvenir; the recipe consumes it for the preservation trial and records that use.

Nella reads the receipt before the sample is prepared. She can ask for a different method or stop the activity without losing the card from her family's custody. The fish's catch record belongs with the sample test, not with the old crossing, and the index keeps those categories apart.""",
    "nella_missing_reed_record": """Supplemental family search note — a protective material needs its own label

The fiber is stored with a crop label until Talia prepares the sleeve. Rowan notes the seed source, plot, watering interval and harvest day; a replacement liner should be traceable to its material without being mistaken for part of the original card. The family can request a new sample if the first becomes worn.

Nella touches the practice strip through a clean cloth and approves the softness, not an authentication claim. The fiber cushions an edge and makes the drawing easier to inspect. It does not repair the trimmed corner or reveal whether a mark was added before or after the card left the checkpoint.""",
    "nella_missing_fiber_check_record": """Supplemental family search note — one removal is a small trial

Talia lifts the liner once, checks for residue under angled light and lays it back without pressing the card. Rowan writes “one removal observed” rather than “reversible in all conditions.” Dust, moisture and repeated handling may change how the fiber behaves; the archive does not have years of aging tests to support a stronger claim.

Nella asks for an open edge wide enough to grip with a cloth. She should not need a tool or a clerk's permission to take the card out if the family changes its mind. The construction note explains how to open it and records who may do so under the current policy.""",
    "nella_missing_craft_record": """Supplemental family search note — the original is not an ingredient

The bench recipe consumes one Windglass fiber and one practice sample, not the pass card. Talia lays out the parts on a diagram before Rowan begins crafting so the family can see what will be spent. The resulting sleeve is inspected with a blank card first; the original remains on Nella's cloth until the frame is ready.

After assembly, the openable seam is tested by hand and the replacement steps are written beside the ingredient list. A future craftsperson can make another sleeve without using any part of the family's evidence. The copy of the recipe stays public only to the extent that it contains no household identifier.""",
    "nella_missing_june_record": """Supplemental family search note — method and search are different records

June separates the public method card from the family's search sheet by color, category and storage location. She points out that a public explanation of hook counting does not authorize a public image of the pass card. A person can learn how Rowan documented the wall and docket while remaining unable to identify which household has a private file.

The rule applies to this case because Nella requests it. June does not turn the request into a universal practice that overrides another family's choice. The record lists who approved each copy and when that approval can be reviewed again.""",
    "nella_missing_seal_record": """Supplemental family search note — access instructions must travel with the seal

The outer pouch has a plain face; its numbered receipt is stored in the restricted ledger. The opening rule names the family contact route and explains how to request correction, renewed review or withdrawal. Nella asks Rowan to read the rule aloud before the pouch is sealed so a future holder will not have to guess what the number means.

The seal indicates handling, not truth. If it breaks, the keeper records what happened and contacts the family through the approved route. A damaged mark alone cannot say who opened the pouch or why.""",
    "nella_missing_install_record": """Supplemental family search note — display can be undone

The frame ledger records the sleeve's item number and the date it was fitted. No adhesive touches the pass card. A visitor can see the checkpoint stamp and notches through the clear edge, while the family can request removal through the same counter where it was installed. The display card says that the drawing shows the present object, not every stage of its journey.

Nella checks that the frame can be opened with gloved fingers. Installation consumes the crafted sleeve, but the original card and the family's permission remain separate from that gameplay object. A later change of policy can return the card to private storage without rewriting the installation record.""",
    "nella_missing_chain_record": """Supplemental family search note — the broken link has no owner

Rowan photographs the chain tags from above and from the side, placing a scale at the same distance in both images. One link has a bright interior under the dark surface, but no conservator can tell whether that came from a recent break or repeated motion. The storage case is recorded as the location where the tags were found, not as proof they traveled together.

Nella declines to choose either tag as her sibling's. The archive uses “unassigned” rather than “unknown traveler,” because even the connection to a traveler is not established. If a later mark can be compared, it receives its own date and source.""",
    "nella_missing_silas_record": """Supplemental family search note — a signal can travel farther than a witness sees

Silas draws the weigh-station wall on his statement and marks his remembered standing position with a distinct symbol. The word “inside” is kept as his present description; it is not converted to a measured coordinate. Rowan places a second mark for the modern survey and labels its date so a reader cannot mistake the two positions for one observation.

Nella does not use the statement to assign the chain tags. Silas's account can establish what he remembers doing and where his view was blocked. It cannot identify who received a signal or which road a missing person took.""",
    "nella_missing_sightline_record": """Supplemental family search note — the shaded area is not an empty area

The sketch uses a hatched wedge for the section blocked from Silas's recorded position. Rowan adds the station wall, gate and two known markers for orientation, then labels the estimated signal radius with a question mark. That line is an untested guide for a future survey, not a circle that contains everyone who might have heard or seen the signal.

The lower bend remains uncounted in this sheet. Nella requests that later copies keep that label even if a new map has more detail. A clearer view can improve the field record; it cannot make the present uncertainty retroactively disappear.""",
    "nella_missing_nella_record": """Supplemental family search note — consent has a narrow subject

Nella reads the public copy line by line. She approves the method, the damaged-record locations and the statement that no destination is established. She does not approve publication of the card image, the household's request slip or anyone else's account. Rowan records that scope rather than checking a single broad box marked “family consent.”

Her signature confirms the copy boundary on this date. It does not mean that she accepts every interpretation in the archive or that she gives up the right to change the boundary later. Nella can speak for this file and this request only.""",
    "nella_missing_policy_record": """Supplemental family search note — either policy preserves the same open question

Before Rowan records the choice, he reads both descriptions back to Nella: a public method-only card, or a public notice that a restricted family file exists. Neither option publishes the card or names the sibling. Both retain a correction date, a withdrawal path and the same warning that no destination is known.

The decision changes the audience for records, not the events the records can prove. Nella is allowed to choose without predicting what every other family would want. The selected policy is saved so a later custodian does not quietly substitute the path they find more convenient.""",
    "nella_missing_public_margin_record": """Supplemental family search note — the correction date is not a deadline

The public card includes a date for the next archive review. That date prompts Rowan to recheck the method and the contact route; it does not require Nella to report a result by then. The wall count may change if plaster is repaired or a lost tag is found, and such a change can be added without turning the new count into a count of people.

The card uses a blank space for future corrections rather than leaving room for household names. Anyone who finds a new record can send its source and date through the listed channel. The archive can respond without displaying the family's private search.""",
    "nella_missing_family_copy_record": """Supplemental family search note — withdrawal returns the copy, not the evidence

If Nella asks to withdraw the family copy, the archive returns that copy to the named holder and records the handoff. The public method card and the original docket remain in their own custody because they are different objects under different permissions. The withdrawal entry says what was returned, not why the family asked.

The family may later request a new copy under a revised rule. The earlier receipt stays in the ledger so custodians can account for the history without keeping a version the family asked them to return. Privacy is maintained through an explicit procedure rather than a promise that no record of handling exists.""",
    "nella_missing_afterword_record": """Supplemental family search note — leave room without promising an answer

The file's final index lists where a witness may send an account, how the family may reopen the private copy and how an older statement can be corrected. It does not set a deadline for an answer or a required final status for the search. Nella wants the archive to stay useful if someone remembers a date, a place or a paper mark years later.

Rowan leaves the destination field blank. That blank records the limit of today's file, not a conclusion about the sibling's life. If a future witness arrives, their account will begin with its own source, date and permission, not with a verdict written in advance.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Nella family-search records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Nella family-search records; added {after - before} words.")


if __name__ == "__main__":
    main()
