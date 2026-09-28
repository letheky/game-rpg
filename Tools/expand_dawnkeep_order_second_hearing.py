#!/usr/bin/env python3
"""Append a second, source-aware hearing to the Dawnkeep Order archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental archive leaf —"


LEAVES = {
    "dawnkeep_order_arrival_record": """Supplemental archive leaf — the fold Elara would not flatten

Elara set the map beneath a pane of glass but left the deep fold untouched. I offered to warm the paper over a lamp so the southern road would lie flat. She moved the lamp away before I could try. The ink had cracked along the crease, and heat might have lifted the faintest line from the page. Instead, she placed a narrow weight at either end and let the curl ease by itself while we copied the visible marks.

She did not tell me where the road ended. She asked which part of the route I could describe without naming its destination. I said there were two lock points, one service road, and a turn where the water narrowed. She added the height of the stone posts and the direction the water ran at that hour. Her map-making is not a habit of filling space. She gives an unknown a border and leaves it room to remain unknown.

By evening the page rested flat enough for a clean copy. We put the original back in its sleeve rather than pinning it beside the yard map. The line is legible now, but it still stops before Cinderwell. Elara says a map can guide an investigation without pretending that the journey has already happened. I had thought an unfinished route was a failed drawing. At Dawnkeep I learned to carry a question without drawing the answer for it.""",
    "dawnkeep_order_roster_rubbing_record": """Supplemental archive leaf — pressure from the chisel

The rubbing darkened where I pressed hardest. Elara saw the difference before I did: one of the short strokes looked like a name because the paper caught more graphite there. She asked me to lift the sheet and repeat the pass with a softer block. The second impression was lighter, but it kept the weathered groove and the shallow scrape separate.

We compared the two sheets with the stone in late afternoon light. A cut that seemed to run beneath another mark in the morning ended at its edge when the sun moved. That does not tell us which mark came first; the stone may have been turned, or the surface may have worn unevenly. Elara recorded the angle of the light, the distance of the paper from the eastern seam and which hand held the block. A future copyist can repeat those conditions and judge the impressions for themselves.

The first sheet remains attached to the field sketch. The second is filed as a repeat, not a correction. I wanted the darker sheet to be the better one because it made the roster easier to read. Elara reminded me that clarity can be manufactured by pressure. We can show the marks more plainly without making them say more than the stone does.""",
    "dawnkeep_order_disclosure_choice_record": """Supplemental archive leaf — the runner who carried both copies

I carried the rubbing from Elara's workroom to Captain Alden's table, then carried two sealed instructions back: one for the yard registrar and one for the archive drawer. The envelopes weighed almost nothing. I remember checking each seal twice because I was afraid of delivering the wrong choice to the wrong place.

Elara asked me what I thought should happen. I said the patrol should see the evidence. Alden asked what I would tell a family who read its name beside an empty space. I had no answer. My first response was a wish for speed; his question made me notice the people who would have to live with whatever speed did to the record.

The captain's note did not choose for me, though it shaped the choice by naming consequences I had not considered. I keep both instructions in this archive because a later reader might otherwise imagine that I decided alone. My decision was real, and so were the limits around it: I did not make the rubbing, set its custody rule, or know the missing destination. The branch we followed changed who could read the page first. It did not change what the page proves.""",
    "dawnkeep_order_public_response_record": """Supplemental archive leaf — the question after the reading

When the noticeboard reading ended, a cadet stayed behind to ask whether the list had been used to decide who was allowed to leave. Elara answered that the record before us could not settle that. The cadet looked at the surviving names and said that an incomplete answer was still an answer the Order had chosen to give. Elara did not correct them. She wrote the question on a separate card, with the time and the page the cadet had seen.

Nia asked whether the card should carry the cadet's name. The cadet said no. We filed the question without one and added a note that the speaker had requested anonymity. The public copy still shows its source seal, but the question is not evidence that any particular person was transferred. It is evidence that a reader asked how the roster had been used.

Elara read the card back before placing it in the review box. She has started doing this whenever a visitor asks for a correction; a person should be able to hear the words the archive intends to keep. The yard grew quiet after the exchange. We did not count who stayed. We recorded one question we could answer only by finding another source.""",
    "dawnkeep_order_private_response_record": """Supplemental archive leaf — the key's daily route

The shallow drawer key is not kept in the registrar's office overnight. At closing, the registrar signs it over to the watch captain, who carries it while the hall is unlocked. In the morning the captain returns it before reading the access log. Elara discovered the routine when she asked to inspect the rubbing after the clerk had gone home; the ledger named a custodian, but not where the key would be.

She added a location column and a line for an emergency handoff. Alden objected that a lost key could reveal the archive's weakness. Elara replied that a location hidden from the person who needed access was not security; it was uncertainty with a lock around it. They settled on a sealed daily log kept in the watch office, with the public index naming the responsible role but not the room where the key rested.

No one opened the drawer that night. The new procedure did not make its contents public, and the sealed sheet did not identify the family names inside. It made custody easier to question if the key went missing. Elara says that privacy needs a keeper whose actions can be checked, even when the protected page cannot be read by everyone.""",
    "dawnkeep_order_empty_cots_record": """Supplemental archive leaf — the board beneath the third bed

While we lifted the split cot from the passage, a loose board shifted under its rear leg. There was no paper beneath it, only a line of pale grit and a small copper washer. Elara recognized the washer as the kind used on the barracks window latches. We found one latch with a newer screw and another still bound by a strip of leather. Neither repair could be dated from the metal alone.

The floor marks changed when the cot moved. A dark rectangle that looked like the footprint of a trunk vanished under the dust we had disturbed. I sketched both conditions before sweeping: first the room as we found it, then the exposed board and washer. The first drawing preserves the evidence before our work; the second shows what the inspection uncovered. We marked the cot as moved so nobody will mistake the after-sketch for the original arrangement.

The washer tells us that someone maintained a window latch. It does not identify a sleeper or prove that a particular bed was occupied when the roster changed. I wanted the empty room to yield a name. It yielded a repair detail, which is smaller but still useful: a future inspection can compare the other latches without inventing a person to fit the space.""",
    "dawnkeep_order_cadet_testimony_record": """Supplemental archive leaf — Nia's second look at the margin

Nia returned to the ledger with the original question she had written as a cadet. She had remembered a hooked mark at the end of the line. The page we found contains a short diagonal stroke instead. She ran one finger above the ink without touching it, then asked me to read the sentence aloud exactly as it stood. The words were hers; the mark might have been hers, a later correction, or a copyist's shorthand.

She declined to replace her earlier account. Instead she wrote a new note: the remembered shape and the visible shape differ, and she cannot now say when the change occurred. That costs her the confidence of a clean recollection. She said she would rather lose a detail than pretend her memory had not shifted while she spent years retelling the event.

Elara asked whether Nia wanted the two accounts displayed together. Nia chose the archive copy, accessible by request, and asked that the public summary mention the disagreement without printing her old work schedule. She remembers an error in a total and a sealed packet leaving the desk. She still does not know who traveled south. The margin remains a question she can help us examine, not a key to other people's identities.""",
    "dawnkeep_order_transfer_ledger_record": """Supplemental archive leaf — a scale checked against an empty pan

The store quantities in the transfer ledger did not match the weights on the duplicate dispatch. Before we treated that as a discrepancy, Rowan asked the quartermaster to test the scale with an empty pan and a standard stone. The beam returned to its mark. Then we learned that one sheet counted sacks and the other recorded the weight of grain after two torn bags had been repacked.

The totals still differ, but their units differ too. A later clerk had copied the figures into one column and drawn a line between them, making them look like competing counts of the same goods. We made a comparison sheet that keeps sack count, estimated weight and repacked amount separate. The torn-bag note has a different hand from the dispatch signature, so we left authorship blank.

This check narrows the question. The supplies may have continued south in more than one form; the ledger does not yet tell us who accepted them or whether they traveled with the listed cadets. Alden recognized the quartermaster's mark but did not use it to identify a recipient. We can reconcile a measurement without reconciling the journey. The blank return column remains the record we most need to find.""",
    "dawnkeep_order_evidence_choice_record": """Supplemental archive leaf — the family that asked for the method

A family came to the archive carrying no claim about the roster. They asked how we decided which marks were legible and whether they could have the method card without receiving a copy of the names. Elara showed them the graphite rubbing, the stone sketch and the two lighting conditions used in the comparison. They checked the method card and said it was enough for now.

Their request changed the choice we had framed as public names or sealed copies. Access to a method is not the same as access to a person's record. We added an option to request the comparison procedure by itself, and a separate form for families who want a verified copy of the evidence. The new form does not ask why someone needs it. It asks what material they are requesting and where the registrar should send it.

The family did not ask us to withhold or publish any name. We will not describe their visit as support for either branch. Alden said the Order should learn to offer a useful answer before a person has to reveal why they came. Elara added that a method card can still carry errors, so it includes the date and the observer who prepared it. The roster question remains open; our way of asking it has become more precise.""",
    "dawnkeep_order_open_testimony_record": """Supplemental archive leaf — reading the correction line aloud

Nia took the first evening shift beside the noticeboard. A visitor could not see the small print from the walkway, so Nia read the instructions aloud when asked. One person wanted to correct a spelling but had no source with them. Another brought a letter and did not want its contents read in public. Nia gave them an envelope and showed where it would be stored until the registrar could review it.

The board's open line had been intended for references to other records. It looked like an invitation for anyone to write a missing name. Nia covered that line with a short instruction: “Tell us where to check; do not guess here.” She dated the change and kept a copy of the earlier board in the archive. The amendment makes the process clearer without hiding that the first version could mislead.

No one left a correction that night. We recorded the two requests by subject and marked the second as private correspondence. Nia asked me not to call the shift quiet; a lack of written entries cannot tell us how many people read the board or decided not to approach it. She chose to sit there again the next evening, after the amended notice was copied in larger letters.""",
    "dawnkeep_order_sealed_record_record": """Supplemental archive leaf — the envelope returned unopened

One family brought its sealed copy back to the registrar with the wax intact. They had received the packet but had not opened it. The person delivering it asked for a receipt that said only that the envelope had been returned. They did not explain why. Elara checked the seal number, recorded the date, and asked whether the packet should go back into the drawer or be held for pickup.

The family requested that it be kept for one month, then destroyed if nobody returned. That instruction was written on a separate custody card and signed by the person who delivered the envelope. We did not add a reason or a household description. The roster copy itself remains sealed, so the return tells us nothing about whether the family read or accepted its contents.

Elara marked the packet as temporarily held and set a reminder for the named date. She says a copy belongs to its recipient even when it comes back to us; the archive cannot infer that silence means consent to keep it forever. The sealed-copy route now has a clear end point for an unwanted document. The record we retain is limited to the custody request the family chose to make.""",
    "dawnkeep_order_cinderwell_dispatch_record": """Supplemental archive leaf — the lockkeeper's torn corner

At the first lock below Dawnkeep, the keeper showed us a ledger with a missing lower corner. The remaining paper carried the dispatch seal number and a note that a packet had been passed to the southbound store boat. The entry did not list passengers. Its water stain had spread through the receiving column, so no signature could be recovered from the surviving fibers.

The lockkeeper remembered that the boat stopped again at the lower basin to take on an empty barrel. She could not remember its crew or whether the sealed packet stayed aboard. We recorded her recollection separately from the ledger and asked her to review the wording before it was filed. She corrected “delivered to Cinderwell” to “passed toward the southbound boat.” The distinction is hers, and it keeps our copy from claiming the packet reached its destination.

Rowan traced the torn corner and made a protective sleeve so the page can be handled without losing more fibers. We have a point on the route and a transfer to a boat, not a receiving record. Elara thanked the keeper without asking her to guess who might have carried the dispatch. The next search follows the boat's store account and the barrel's return mark.""",
    "dawnkeep_order_alden_reckoning_record": """Supplemental archive leaf — the signature Alden keeps beside the question

Alden returned to the signed dispatch after the lockkeeper's ledger was copied. He placed his signature beside the new transfer note, then asked that we not draw a line connecting them. The documents are related by the seal number and route, but he did not witness the handoff at the lock. A line on a page could make the chain look unbroken when it is not.

He told Rowan that he once signed orders in batches at the end of a watch. The seal had to be checked, the numbers read back and the destination verified; the person who carried each packet was entered elsewhere. Alden recalls the procedure more clearly than this dispatch. That may be because the procedure happened hundreds of times. He will not use repetition as proof that every step was followed here.

Before leaving, he added his own request to the open questions: find the page that records who took the packet from the boat. He did not ask the archive to clear his name or assign blame to the clerk whose mark appears on the copy. His signature remains evidence of authorization. The gap after it is still a gap, and his responsibility is to help trace the authority he gave.""",
}


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in catalog["entries"]}
    missing = sorted(set(LEAVES) - set(entries))
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")

    changed = 0
    for codex_id, leaf in LEAVES.items():
        entry = entries[codex_id]
        marker = MARKER + " "
        title = leaf.split("\n", 1)[0]
        if marker + title in entry["body"]:
            continue
        entry["body"] += MARKER + " " + leaf
        changed += 1

    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Appended second-hearing leaves to {changed} Dawnkeep Order records.")


if __name__ == "__main__":
    main()
