#!/usr/bin/env python3
"""Add family-centered context to Nia Porter's Dawnkeep return-desk archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental family archive note —"

NOTES = {
    "dawnkeep_household_mail": """Supplemental family archive note — two requests at one desk

The two households arrived with questions about the same bundle, but each began by asking what the other could see. One wanted a receipt proving that a private copy had been handed over. The other wanted its address removed from the wall index before anyone discussed the envelopes. Neither request answered the question of where the mail had gone. Nia wrote them on separate slips so a clerk could not later read their presence at one meeting as shared permission.

The return desk used to keep one visitor book for every matter. Nia now sees how a convenient book can create a new list of families connected to a missing cadet. She leaves the visitor page unused and gives each household its own code. The codes describe custody of a paper, not the people who brought it. If a family returns, it can bring its receipt without having to prove that it once stood in this room.""",
    "dawnkeep_envelope_inventory": """Supplemental family archive note — paper is not a travel diary

Nia lays the five envelopes beside the inspection card and turns each one only by its edges. The three torn seals have different folds; the two closed ones are not opened to compare what is inside. A gray smudge occurs on all five, but the east desk is dusty and the mail pouch was stored near a stone stair. The mark can be described without pretending it names a route.

One visitor recognizes the twine around an envelope but cannot say whether the bundle was carried home or brought back unopened. Nia records the observation in the private review copy, not the public catalogue. The distinction matters because memory can help identify an object while still leaving its journey uncertain. A photograph of an exterior can show a crease, a seal or a stain. It cannot tell the archive who read the words inside.""",
    "dawnkeep_unclaimed_badges": """Supplemental family archive note — a badge is a tool, not a body

The pouch containing three cadet badges was found after the morning roll had closed. Two serials can still be read. The third has a broken hook and a face worn nearly smooth. Nia remembers cadets trading straps and lending cloak pins before drill; a serial belonged to an issued object, not always to the person who carried it on a particular day.

One damaged badge sits close to an envelope with a similar gray mark. Their proximity is the only link between them. Nia asks that they remain in separate containers so a future clerk will not slide the badge under the nearest roster line. She knows the temptation: the pouch appears in the same drawer as papers about Ellis, and a matching number would feel like a clue. A feeling of fit is not a chain of custody. The inventory therefore marks the badge as unassigned until someone brings evidence that can be checked.""",
    "dawnkeep_address_redaction": """Supplemental family archive note — a name should not open a front door

The public roster needs to show which unit was sent to which destination and on what date. A home address answers a different question. Nia removes it from the wall copy after a relative points out that the board faces the road where carts stop. The address had been added years earlier to help return lost property; no one had reviewed whether that purpose still justified leaving it visible.

The family keeps its own correspondence and can correct its own contact details. Another household cannot authorize publication on its behalf, even if both families have asked about the same mail sack. Nia records the redaction as a change to the copy's scope and preserves the old version in restricted custody. She does not erase the fact that an address once appeared; she stops the public page from making that information available to every passerby.""",
    "dawnkeep_return_window_hours": """Supplemental family archive note — the hours nobody signed for

The third watch ended before the fifth began, leaving an interval where the return desk had no named clerk. Two envelopes bear marks from that interval. Nia compares the ink with the guard's gate stamp; the colors are close, but the paper absorbed them differently. No one can say whether a guard began the handoff or a clerk finished it after the shift changed.

She used to treat a blank schedule as an invitation to write “routine transfer.” A routine can explain what staff expected to happen, not what happened to a particular piece of mail. The new form shows the gap as a band and asks the next clerk to add a signature only when they can identify their own action. The missing mark remains visible. It does not accuse the guard or clear the desk; it gives the family a more honest limit than an invented continuous timeline.""",
    "dawnkeep_courier_handoff": """Supplemental family archive note — placed beside the door

The courier note says a pouch was left beside the east door. A desk stamp from later that day carries another bag code. Nia cannot tell whether the second stamp belongs to the pouch, a replacement bag or a separate delivery. The written note never says a clerk signed for the first one, and the pouch itself is not among the returned objects.

The courier is willing to repeat what they remember but asks not to be quoted beyond the delivery wording. Nia copies the statement as a dated note, keeps the speaker's permission beside it and does not add a name to the public index. The account narrows one step of the journey: someone recalls placing a pouch near the door. It does not bridge the distance between the doorstep, the return desk and a household. A later page must not use the word “delivered” to smooth over that missing distance.""",
    "dawnkeep_private_review_rules": """Supplemental family archive note — a meeting that can stop

The first private review lasted less than a watch. One relative read the outside of an envelope, closed the copy and asked for the rest to be held. Another wanted time alone with a version that contained only their own household's papers. Nia records which version was offered and whether it left the room. She writes no attendance tally and does not ask what the visitors felt when they read.

The keeper's role is to explain the copy, point out what is missing and stop when asked. Rank does not change that rule. Nia has to follow it too; she is not entitled to keep reading because she works at the desk or because the papers concern her brother. A request to pause is entered as a procedural event, not as a reaction or a refusal to cooperate. The family can return later, request another version or decide not to read further.""",
    "dawnkeep_copy_scope_decision": """Supplemental family archive note — what a public count cannot say

The aggregate option would let anyone check how many envelopes were inspected, when the desk was staffed and which seals looked similar. It would not show which household had received a letter. The sealed option would let each family review a private copy before deciding whether any summary could be shared. It would take longer, and an unanswered invitation could leave the public without a count.

Nia asks the player to choose a procedure for this bundle, not a theory about Ellis. A number of inspected envelopes cannot tell whether one person waited at a gate or received a message somewhere else. A sealed packet cannot prove that the archive has been complete. She marks the choice with its limitations on the same page. If the households later ask to change the scope, the record can be reopened without rewriting their earlier request as agreement.""",
    "dawnkeep_aggregate_mail_sheet": """Supplemental family archive note — five objects on the public page

The aggregate sheet lists five inspected envelopes, two unsigned time windows and three seals with similar wear. The number five describes the items found in one barracks bundle. It is not a count of families, letters sent, letters delivered or cadets who received news. Nia prints that warning beside the total in the same type size so it cannot be separated from the number when the page is copied.

An officer asks whether the unsigned marks should be excluded to make the table simpler. Nia leaves them in and labels them “unassigned time,” because hiding an awkward part would make the total look more certain than the papers allow. The public copy can be corrected by anyone who can point to a specific version and field. Private source pages remain available only under their access rules. A transparent count is useful only while readers can see exactly what was counted.""",
    "dawnkeep_sealed_family_packet": """Supplemental family archive note — a packet remains pending

Each sealed packet has a code on the outside and a version number beneath the fold. The outer index names the custodian who holds the key, but it does not list the contents or say that a household has read them. An invitation with no reply stays pending. Nia rejects a proposed deadline that would convert silence into approval once the watch changed.

The keyholder has to log every opening, including a session stopped midway. A family can use the receipt code to request a copy, narrow the permitted audience or withdraw it from the review table. The procedure may delay a public summary, but it protects a choice the family has not made yet. Keeping the packet closed neither confirms nor denies where a letter went. It simply describes what the archive is authorized to show today.""",
    "dawnkeep_scope_label": """Supplemental family archive note — permission in words a clerk can follow

Nia rewrites the scope label after a new clerk mistakes “family copy” for permission to show the packet to every relative. The revised label names the allowed readers, the version they may see, the reason the copy can be used and the route for changing that permission. It says who supplied the scope and when it was last checked. No field asks the family to defend a narrower request.

The label is short enough to travel with the copy but specific enough to stop a custodian from guessing. If the author of a letter is unknown, permission from its recipient does not automatically speak for the sender. If the sender cannot be found, the register says so rather than making the nearest available person the owner of every question. A clerk can follow the label without deciding whose privacy matters more.""",
    "dawnkeep_key_access_log": """Supplemental family archive note — the drawer records its keepers

The access log begins with the shift supervisor who opened the drawer to check its lock. It records the stated purpose, the page version viewed and the time the key was returned. The next line records Nia's own access while she copied the public summary. She includes herself because an audit that lists everyone except its author would be decoration.

One failed attempt to open the drawer remains in the log. The key did not turn, and no paper was removed. Nia keeps the entry so a future review can distinguish an unsuccessful attempt from an unrecorded visit. The log contains no family responses or letter contents. It makes the custody process visible without making the people who request privacy easier to identify. The keyholder is part of the history of a record, not an invisible space outside it.""",
    "dawnkeep_correction_without_name": """Supplemental family archive note — the address changed on one copy

The correction slip identifies the public page, line and address field without naming its sender. Nia compares the request with the restricted contact card, updates the public copy and leaves a reason code rather than a family name. The private packet keeps its own version unless the requester asks for it to change as well. A correction to one copy does not silently rewrite every document in the archive.

At first, Nia worries that an unsigned request will be dismissed as unreliable. The page can be corrected without authenticating the sender's identity because the error is visible on the public copy itself. If the request concerns private information, the custodian can ask for a receipt code through a private channel. The public change log shows only that an edit occurred and which version was replaced. It does not expose who asked for the door to be hidden.""",
    "dawnkeep_copy_receipt": """Supplemental family archive note — receipt B-04

Receipt B-04 confirms that a copy was handed to one person on a stated date. It does not say that the person read it, believed it, approved the archive or confirmed the events described inside. Nia separates those boxes on the new form. The old sheet used one checkmark beside “received” and let later clerks infer the rest.

The new receipt records the version number and explains how to request a correction or withdraw that copy. A household can keep the receipt without placing its address on the public board. If a replacement is issued, its version refers back to the earlier copy so the archive can tell which page may still be circulating. Delivery, reading and agreement remain separate actions. A small set of boxes cannot explain a whole family's response, but it can stop the desk from claiming more than it observed.""",
    "dawnkeep_open_margin_registry": """Supplemental family archive note — the margin stays open

Nia leaves one margin wide enough for a later custodian to write what changed and which copies must be reviewed again. The board has a public correction mark; the restricted packet has a separate access note; neither asks a family to repeat its private reason in front of the barracks. The register can be narrowed or reopened using the receipt code, even after Nia is no longer assigned to the desk.

She still does not know where Ellis is. The bundle of returned mail, the badges and the unsigned watch interval do not combine into proof that he died or proof that he reached home. Nia resists making her own fear into a conclusion, even when the blank space belongs to someone she loves. The desk can serve the families who need a record and protect those who do not want their names posted. It cannot answer the question she carries beyond the end of this route.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Nia family records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Nia family records; added {after - before} words.")


if __name__ == "__main__":
    main()
