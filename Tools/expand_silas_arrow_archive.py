#!/usr/bin/env python3
"""Add scene-specific field and custody notes to Silas Vane's arrow archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental arrow archive note —"

NOTES = {
    "silas_arrow_open_record": """Supplemental arrow archive note — the fold that will not close

Nella's return slip was clipped to the lower edge of the map, not placed over the empty bend. Silas notices that the map was folded through the western notch for years; each crease carries dust from a different shelf. He and Rowan flatten it under two clean weights, then leave the old fold visible instead of pressing it away. A new drawing can make the road easier to read, but it cannot repair a missing viewpoint by making the paper look continuous.

Silas asks that his own account be kept beside the map without being used as its caption. A reader may compare the two sources, but the map is not proof of the remembered flash and the memory is not a key for every mark on the road. The folder's contents list names each object on its own line.""",
    "silas_arrow_map_record": """Supplemental arrow archive note — a route line is a proposal

Rowan adds three numbered circles and a fourth mark for the section no one can see from either road approach. The circles record where a person stood; they do not imply that the person moved from one to another. Silas had first drawn an arrowhead along the red stroke, which made the line look like a travel direction. He removes it after Rowan asks which source supports the direction rather than the locations.

The replacement legend uses an open bracket for a surveyed edge and a dotted edge for an unobserved interval. Future mapmakers can extend the survey by adding a dated layer. They should not erase the bracket simply because a later observer gets a longer view from different weather or a different height.""",
    "silas_arrow_reed_record": """Supplemental arrow archive note — the cut belongs to the sample

Rowan ties a loose paper tag to each stem rather than carving a mark into the reed. The tag records the furrow, date cut, direction of lean and whether the stem came from the road-facing or sea-facing side. Silas asks Tomas to keep the sample intact until another fletcher can inspect the grain. Removing the bark now would change the surface they are trying to compare.

The bundle is stored away from the test bow so a future reader will not assume it was the shaft material. It can help describe local plant variation or a possible fletching source. No surviving arrow is attached to it, and the archive does not state that either stem resembles the one Silas used years ago.""",
    "silas_arrow_skate_record": """Supplemental arrow archive note — brightness needs conditions

Lyra puts the scale on a dark cloth and then on pale stone. The reflection looks broader against the cloth; the sample is unchanged, but the background is not. She records the surface, angle, dampness and observer position beside Rowan's drawing. Silas watches from the road and sees a different glint from the one he sees at the table.

They keep the two observations because disagreement can reveal which conditions matter. Neither is a reconstruction of the old signal. The sample came from a fish caught now, and the scale's sheen changes as it dries. A later experiment can compare present materials under named conditions without assigning this scale to an arrow that no one recovered.""",
    "silas_arrow_sentinel_record": """Supplemental arrow archive note — a recovered strand has a short history

The filament is collected only after Rowan marks the Sentinel's den and Silas records that he did not enter it. A clean paper sleeve keeps the strand from catching on the map case. The label states who removed it, where it lay after the fight and which parts of the den were disturbed during the encounter. That is enough to preserve a useful binding sample without pretending the creature left it there on the night of the old signal.

Tomas uses a short offcut for a repair demonstration and returns the unused length to the sleeve. The remaining sample shows how the thread behaves under present tension. Its strength may inform a craft choice; its color cannot identify an old shaft.""",
    "silas_arrow_forge_record": """Supplemental arrow archive note — calibration is not testimony

Tomas stamps the gauge's maker mark on the inside edge, where it can be checked without hiding the adjustable notch. Rowan records the starting position and the amount of movement before the loop settles. They repeat the reset three times, once with Silas watching and twice with him turned away, to see whether expectation changes the reading. It does not turn the tool into a witness; it makes one part of a present-day comparison repeatable.

Silas keeps the charm because it reminds him how carefully a setup must be described. He refuses to call it an arrow finder. It cannot locate a missing shaft or infer what a traveler saw from a distant road.""",
    "silas_arrow_crest_record": """Supplemental arrow archive note — a standing place is part of a view

Rowan writes the eye height beside each crest mark and uses the same shoulder-width stance on both visits. A short person sees more of the lower road from the northern position because the rock shelf blocks less of the line, while a taller observer at the southern mark catches a strip of sky instead. The variation is not a flaw to average away; it describes why a witness's position belongs with the claim.

Silas adds the place where he remembers standing but leaves its exact distance from the old milestone uncertain. The account can be revisited if another person recognizes the ground. Until then, the archive preserves a remembered position separately from Rowan's current measurements.""",
    "silas_arrow_bend_record": """Supplemental arrow archive note — movement changes the question

Walking the bend makes the hidden space change shape. From the north, the salt shelf covers a loaded cart; from the south, a person can see the wheel tracks but not the road beyond the pale stone. A moving rider might pass through both views, but the route does not show when the rider arrived or what they noticed. Rowan draws each view as a small frame instead of merging them into one panorama.

Silas looks at the frames and says the old account had made the bend sound like a single window. He revises the description to name where his sight stopped. That correction narrows his claim without removing the fact that he chose to fire.""",
    "silas_arrow_backstop_record": """Supplemental arrow archive note — absence of a date is a field value

Rowan assigns temporary labels A through D to the cuts and photographs their edges beside a ruler. The mortar patch crosses the shallowest mark, but there is no dated repair ledger for this stretch of wall. That overlap gives an order between two traces, not a calendar year. Silas keeps his practice memory in a separate column so it cannot silently become a date for mark C.

When the group rechecks the stone after rain, a wet edge looks deeper. The earlier dry measurement remains in the folder; the new value is added with its weather note. The record can grow through comparison without replacing an older observation that was made under different conditions.""",
    "silas_arrow_range_record": """Supplemental arrow archive note — the control shot is a control

Before releasing the practice shaft, Rowan places a paper witness card at the target and signs the back. Silas then names his bow, draw length and release point while Tomas checks the wind ribbon. They use a fresh target face so an earlier impact cannot be mistaken for this one. The impact location is measured twice by separate readers before they compare numbers.

The control shot demonstrates how present conditions can be documented. It does not estimate the trajectory of a missing arrow, because the old bow, shaft, wind and release are not available as a matched set. Silas accepts the smaller use of the trial: it can show what a future account should include.""",
    "silas_arrow_silas_record": """Supplemental arrow archive note — the moment before release

Silas writes that he heard the command, reached for the marked shaft and made the choice to draw. He cannot tell whether a different choice would have kept the road safe. He can tell that no one put the bow in his hands or released it for him. This distinction gives him a responsibility he can name without pretending to control every consequence that followed.

The page is dated from his present interview, not backdated to the night itself. He reads the statement once aloud and changes a phrase that made the order sound like an excuse. Rowan keeps the first draft with the correction attached so later readers can see how the account was narrowed.""",
    "silas_arrow_ruth_record": """Supplemental arrow archive note — the dispatch has its own chain

Ruth identifies the dispatch drawer, the docket number and the place where she hid a copy when the inquiry began. She writes the concealment in her own hand, apart from Silas's recollection of the signal. The original is not moved into the public notice folder; Rowan makes a reference card that lets a custodian request it under the same archive rules as the other dispatches.

The order describes a condition for signaling. It does not list every traveler, say who heard a sound or say what happened after the road became difficult to see. Ruth is willing to correct her earlier omission. She does not claim that her new statement fills every gap left by the dispatch.""",
    "silas_arrow_nella_record": """Supplemental arrow archive note — refusal remains private

Nella asks Rowan not to record why she declines the question. The interview note therefore states only that the question was offered, the witness declined and no further prompt was made. It does not use a mark for “uncooperative,” and the blank space after the entry is left empty rather than filled with the clerk's interpretation.

Silas thanks her without asking for another conversation. He understands that a family can help set the boundaries around its own papers without becoming responsible for finishing his account. If Nella chooses to speak later, her words can be added with their own date and permission. Silence does not become a vote for either side of the arrow's uncertain effect.""",
    "silas_arrow_route_card_record": """Supplemental arrow archive note — four sources, four permissions

The card is printed on thick paper and divided into four columns: dispatch, remembered action, present survey and witness boundary. Ruth may correct the dispatch reference, Silas may revise his account, Rowan may add a dated measurement, and Nella controls whether she contributes anything. No one has permission to edit another column merely because the entries appear together.

The card lists the blank interval as unresolved and carries a revision date. A later source can be attached to the relevant column without changing the rest. Silas signs beside his own action and leaves the space beside Nella's boundary unmarked. The card's layout makes the limits legible before a reader reaches the interpretation.""",
    "silas_arrow_policy_record": """Supplemental arrow archive note — policy governs copies

The choice is discussed after Silas's admission has been written in full. The wording of that admission, its date and the description of his limited view travel into either filing route. Only the handling of the named copy changes: one policy places a first-person statement where any passerby can read it; the other gives the family a private copy and publishes the method without names.

Silas says he will not call privacy a way to avoid blame, and Nella says she will not be required to stand beside a board to prove that she was consulted. Their conditions are recorded separately. The policy card leaves room for a later witness to choose another route.""",
    "silas_arrow_public_open_record": """Supplemental arrow archive note — first person keeps its boundary

The final sentence begins with “I fired,” not with “the road turned.” Silas reads the subject and verb together to check that the statement names the action he owns. A separate sentence says the lower mile was outside his view. The removed phrase is retained on a dated draft sheet with a note explaining that the surviving evidence did not support it.

That revision does not soften his responsibility. It prevents an admission about an action from expanding into a claim about every person's response. The public statement is short enough to be read at the board, with a reference to the longer method card for anyone who wants the measurements.""",
    "silas_arrow_public_board_record": """Supplemental arrow archive note — a notice is not a roll call

Rowan positions the board away from the barracks door so readers do not have to pass a clerk or declare why they stopped. The account includes Silas's name because he chose to sign it, but it omits the names of travelers and households. A small index directs corrections to a box that can be opened without gathering a crowd around the page.

Nella checks the layout and confirms that her family does not appear. She does not endorse the account by checking this boundary. The receipt says only that she inspected the page's scope. The posted notice can be public while keeping the act of reading, commenting or walking away private.""",
    "silas_arrow_public_method_record": """Supplemental arrow archive note — the setup travels with the measurement

Each daylight trial has a small card listing the ridge marker, observer height, target surface, wind ribbon and start time. If one condition changes, the new sheet gets a fresh identifier rather than being called a failed repeat. Tomas marks the gauge position in pencil so it can be checked against the tool itself. The method tells another craftsperson how the present comparison was made.

The sheet is deliberately separated from Silas's account. Someone can repeat the sightline test without agreeing with his memory or reading the family copy. A method can be open to correction while personal statements remain under their author's control.""",
    "silas_arrow_public_ruth_record": """Supplemental arrow archive note — adjacent pages remain separate

Ruth dates her note by the day she disclosed the hidden dispatch, not by the night it was issued. She describes when she found the copy, why she kept it and when she returned it to the archive. These facts concern her custody of the order. They do not rewrite the terms of the order or provide a second witness to Silas's release of the arrow.

The binder uses two tabs and a shared index number. A reader can follow the related material without mistaking two signatures for one account. If either person later makes a correction, it attaches to that person's page and leaves the other page unchanged.""",
    "silas_arrow_public_nella_record": """Supplemental arrow archive note — scope check, not endorsement

Nella points out that an earlier copy used “the families” as if all households had sent a shared request. The board text is changed to say that one relative asked to inspect the page. The correction avoids turning a single person's action into a group position. Nella chooses not to supply a sentence for the public account, and her choice is not printed on the board.

The archive receipt records the narrow edit and the date she reviewed it. It does not contain her reaction, her family history or a statement about Silas. A reader can see that she checked one privacy boundary without learning anything else she did not choose to share.""",
    "silas_arrow_public_signature_record": """Supplemental arrow archive note — a signature can own a sentence

Silas signs below the account rather than beside the route card. A custodian witnesses the signing and gives him a duplicate that shows the same page number. He can later challenge the wording or add a correction, but neither action silently replaces the first signed copy. The correction pocket records what changed and who requested the change.

The unresolved line is signed too. Silas wants it to be clear that the limit is part of his statement, not an editor's attempt to protect him. A reader may question his memory, but cannot fairly extend his signature to a conclusion the signed page expressly leaves open.""",
    "silas_arrow_public_post_record": """Supplemental arrow archive note — a correction should not demand a crowd

The board's pocket accepts a public correction card, while the side box accepts a private request addressed to Nella. A person can use either route without announcing a household connection at the notice board. The pocket is checked at the end of each watch by two clerks; both write their initials even when it is empty, so an uncollected silence is distinguishable from a box nobody opened.

The review date marks when the page should be checked, not a deadline for a witness to speak. If nobody responds, the account remains unchanged and is not marked confirmed.""",
    "silas_arrow_public_after_record": """Supplemental arrow archive note — an unsigned request is not testimony

The paper left by the passerby asks to preserve the blind-road sentence and contains no description of an event. Silas does not attach it to the evidence column. He logs it as an anonymous request about the notice's wording and keeps the request with the board maintenance record. The public copy remains unchanged except for the note that a wording request was received.

Silas had expected a signed reply to make the account feel complete. Instead, the first response reminds him that people may want the record to stay narrow without adding their names to it. The page now has a visible route for further corrections, but no invented witness.""",
    "silas_arrow_sealed_open_record": """Supplemental arrow archive note — the family sets the table

Nella asks for one copy for her aunt and another for the archive, with different access rules. The aunt's copy includes Silas's admission and the field method; the archive copy keeps the sealed packet's access history. Nella does not request a copy for every household on the road and is not asked to explain that limit.

Before the packet is closed, Rowan reads the return instructions aloud and Nella corrects the contact route. She may ask for another review or return the page without writing a response. The receipt names the permitted holder and the copy number, not the contents of a private conversation.""",
    "silas_arrow_sealed_case_record": """Supplemental arrow archive note — visible handling has limits

The split wax mark gives the family a way to notice a broken seal. It cannot identify every person who touched the case, and paper can be replaced. Nella asks for a second measure: each transfer is written on the sleeve, with the sender, receiver and date. If a mark is damaged in ordinary handling, the custodian adds an explanation instead of resealing the case in silence.

The archive describes the protection honestly. The case can show that an opening may have occurred and preserve a chain of recorded custody. It cannot guarantee that no one could ever open it.""",
    "silas_arrow_sealed_silas_record": """Supplemental arrow archive note — privacy does not cut away context

The family copy keeps the order reference and Silas's signed account together so his admission cannot be detached from the limit on his view. It also contains the map index, which shows the blind interval without exposing unrelated household records. Nella may return the page with a question attached; she is not required to keep a copy simply because it was offered.

The access card records whether the packet left the desk and returned. It does not report what anyone thought after reading it. The family may keep its response outside the archive, where an official need not turn private grief into a catalog entry.""",
    "silas_arrow_sealed_ruth_record": """Supplemental arrow archive note — the source can be checked

Ruth includes a location code for the original dispatch and signs a separate account of how she withheld a copy. The family's custodian can ask to compare the packet's reference with the original under supervised access. No household names are written on the request card; the archive needs the code and the permitted holder, not a public explanation for wanting to verify the source.

If the dispatch differs from Ruth's description, the copy can receive a dated correction. The family may choose whether that correction travels with the private account. Ruth's note still does not identify who saw the signal or what happened at the bend.""",
    "silas_arrow_sealed_public_method_record": """Supplemental arrow archive note — two routes can share one method

The public method sheet contains the numbered positions, present-day readings and instructions for requesting another survey. It does not reveal the aunt's name or duplicate her copy. A private holder can compare the method with the account at home, while any craftsperson can repeat the daylight setup in the field.

Nella approves this split because it lets others check the measurement without turning access to Silas's named statement into a public condition. The index explains that the method is independent of the private packet. A public result may be corrected by a new measurement; it cannot be used to infer that the family approved the account.""",
    "silas_arrow_sealed_review_record": """Supplemental arrow archive note — the receipt records the handoff

The narrow receipt has four fields: copy number, named holder, handoff date and return option. It contains no box for a family member's reaction. Nella asks to have the inspection witnessed by a clerk from another desk, so a relative does not have to describe the visit to Silas. The clerk confirms the handoff, then leaves before the reading begins.

If the holder wants to correct the account, the receipt points to the return channel. If they want to keep their response private, the empty comment field stays empty. Review is an opportunity, not a demand for testimony.""",
    "silas_arrow_sealed_sign_record": """Supplemental arrow archive note — the same admission under either policy

Silas signs before the copy is placed in the case and asks the custodian to read the page number back to him. He compares it with the public method index to catch a mismatch, then initials the custody line. These small checks establish which page he approved; they do not ask the family to certify the truth of his memory.

He writes one sentence on the inside flap: “My choice is mine; the result is not mine to invent.” Nella leaves it in the packet because it describes the boundary of the account without requiring her to agree with the statement.""",
    "silas_arrow_sealed_seal_record": """Supplemental arrow archive note — reopening adds a page

If the family returns the case, the custodian breaks the seal in front of the named holder and records the split mark. A new seal receives a new number; the old entry remains in the ledger. The archive never scrapes wax away and pretends the first opening did not occur. The holder can take the packet again, leave it with the desk or ask for an updated copy.

This route preserves choices over time. A later relative may be granted access only if the family changes the instruction. The first holder's permission does not automatically become permission for every person with the same surname.""",
    "silas_arrow_sealed_after_record": """Supplemental arrow archive note — a quiet route can still be accountable

The public method notice receives its regular check, and the case sleeve receives a separate custody entry. Silas does not inspect the family's private copy. He asks Nella whether the published method still avoids naming the holder; she confirms only that boundary and gives no report of her aunt's response.

The filing is complete as a procedure, not as an explanation of the old night. Silas accepts that accountability may be read by a small number of people and still be real. The archive will keep the route open if the family later changes who may see the account.""",
    "silas_arrow_daylight_repeat_record": """Supplemental arrow archive note — compare conditions before values

The two daylight sheets are laid side by side with their weather cards. Wind speed differs by one ribbon-width, the far marker is damp on the second visit and the observer wore a thicker coat that changed the recorded shoulder height. The team circles these differences before comparing the final visible interval. A larger number would mean little if readers could not see which conditions changed.

Rowan keeps both trials. They show that a present view can vary within a named setup, not that either view recreates an earlier season. A third visit can add a new condition card, never erase the first two.""",
    "silas_arrow_nella_addendum_record": """Supplemental arrow archive note — another account begins on its own terms

The return slip offers three ways to respond: ask for a private meeting, submit a written account or request a new survey. It does not contain a box marked “agree” or “disagree.” A witness can name a place without explaining a family relationship, and can ask for the note to be held while its use is discussed.

Nella chooses the slip's wording but not a likely future witness. She refuses to set a date by which someone must come forward. The archive can remain ready without treating the empty box as evidence that everyone has spoken.""",
    "silas_arrow_repeat_target_record": """Supplemental arrow archive note — spread is part of the comparison

The second shaft is checked against the bow and target before it is released. It lands beside the first mark, and Rowan measures from the center of each cut rather than from the edge that looks cleanest. Tomas records the difference as a range for this bow and setup. If another craftsperson repeats the exercise, their values will be entered on a new sheet.

The pair of marks shows ordinary variation in a known practice. Neither mark is matched to the old groove, because the old shaft, bow and weather are missing. The experiment helps explain uncertainty; it does not turn uncertainty into a calculable answer.""",
    "silas_arrow_reed_copy_record": """Supplemental arrow archive note — a second season is not a replacement

The overnight salt mist curls one reed bundle toward the coast. Rowan records moisture in the soil and the time of harvest; Tomas labels the cut height so the next bundle can be taken at a similar point. The two sets are stored in separate paper sleeves with their season tags facing outward.

Silas asks whether the newer bundle is closer to the old shaft he remembers. No surviving material can answer that comparison, so the note declines to rank them. A new sample can teach the team how local plants vary across weather. It cannot become an unmarked substitute for lost evidence.""",
    "silas_arrow_public_or_case_record": """Supplemental arrow archive note — new evidence gets a date and an owner

The correction form asks for the source, the part of the record it concerns and permission for the requested copy. It does not ask the submitter to decide whether the arrow caused a loss. A location sketch can be shared without a name if the witness chooses that option; a first-person account can stay with its author until they approve a wider copy.

Both the board and the private route keep the earlier page legible. If a new fact changes the interpretation, the archive can explain the change and preserve the older wording. Evidence should alter the record through a visible addition, not an anonymous rewrite.""",
    "silas_arrow_afterword_record": """Supplemental arrow archive note — what Silas can leave for the next reader

Silas adds an inventory of what the archive holds: his dated account, Ruth's dispatch reference, Rowan's present-day surveys and the record of Nella's chosen boundary. It lists no recovered arrow and no statement from a traveler who saw the signal. That absence is not a puzzle the page promises to solve later; it is the limit of this file today.

The next custodian can open a place for new evidence without borrowing Nella's voice, guessing at a household's route or deleting Silas's admission. The folder's last line gives the return address and review procedure. It does not write a verdict for whoever comes next.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Silas arrow records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Silas arrow records; added {after - before} words.")


if __name__ == "__main__":
    main()
