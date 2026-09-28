#!/usr/bin/env python3
"""Expand the first-cycle archive with source-aware Warden and Lyra notes."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental first-oath archive note —"

NOTES = {
    "warden_oath_open_record": """Supplemental first-oath archive note — what a witness can still say

When Lyra asks whether he heard the promise alone, the Warden says he remembers voices around him but cannot separate them now. He will not turn that impression into a witness list. The room beneath the lake has been repaired, flooded and copied into maps across many lifetimes; each change gives memory a new frame to borrow. He can keep the feeling of making a promise while admitting he cannot count who stood nearby.

His request is not to weaken the archive. It is to stop a later reader from treating his survival as proof that he remembers every detail. Lyra writes the limit beside the account, not above it, so the memory remains his own and the missing names remain missing.""",
    "warden_oath_bell_rim_record": """Supplemental first-oath archive note — a polished edge holds repeated contact

Tomas checks the bell rim with a cloth and finds no loose scale at the polished arc. He does not scrape the surface to look for an earlier layer. Rowan measures from the same notch on three visits, using the bell's current mounting rather than a drawing whose date is uncertain. The values describe the object now and can be compared if the mounting changes again.

The Warden says the rim was already smooth the last time he remembers the room clearly, but he cannot place that memory before or after the first promise. Lyra records his statement as a recollection, not a date for the metal. The bell's wear and the Warden's memory remain neighboring sources with separate limits.""",
    "warden_oath_lyra_record": """Supplemental first-oath archive note — the hand beneath the heading

Lyra lays the oldest surviving leaf on a dark support so the faded strokes show without adding chalk. She traces the authorship mark on a transparent overlay, then lifts the three index sheets one at a time. The later heading appears only on the top sheet. Its placement made it look like part of the account when the archive was read from the shelf.

The new catalogue entry describes the physical order of the papers and the order of their copying. It does not claim to know why the clerk chose that heading. Lyra says the title helped later generations remember the promise, but it also gave them a sentence the Warden never wrote. Both consequences belong in the record.""",
    "warden_oath_kelp_record": """Supplemental first-oath archive note — living samples change while they teach

The harvested leaf is placed in a shallow tray lined with damp cloth. Lyra records its length, water depth and time before Rowan carries it through the test tone. Its edge curls as it dries, changing how long the vibration seems to linger. A second observer hears the leaf after a short pause and writes a shorter duration.

The sample is returned to the present garden ledger after the trial rather than kept as an imitation of an ancient relic. Its value is that another gardener can grow a leaf and repeat the observation. It cannot retain the first oath's sound, and neither a strong vibration nor a quiet one can confirm which words were spoken in that room.""",
    "warden_oath_koi_record": """Supplemental first-oath archive note — a catch is also a water record

Rowan writes the pool's depth against the stone step and records the sluice state before wetting the scale. Lyra watches from the channel entrance, where moving water adds a faint sound not heard at the bank. The two notes are kept together because the sample's response depends on the place in which it is observed, not just on the fish.

The Warden remembers a second note after his promise. He does not ask the team to reproduce that memory with a fish or a test tone. A present catch can show how living material responds to today's water and nearby movement. The old phrase remains attached to its speaker and is not presented as a recovered recording.""",
    "warden_oath_gate_record": """Supplemental first-oath archive note — the recovered mote came from a nest

After the Choir Merrow leaves the lower passage, Rowan photographs the nest before moving any bright fragments. Tomas collects the Choir Mote from loose material nearest the entrance and labels the exact spot. Lyra confirms that none of the preserved folio leaves were disturbed during the encounter. The Mote is a resource from the creature's present shelter, not an object that came from the first oath.

The team carries it to the anvil in a closed pouch and records when it is used in the resonance rig. The distinction matters because the lower passage contains old stone, current water and newly gathered monster material side by side. Their proximity does not make them parts of one historical event.""",
    "warden_oath_craft_record": """Supplemental first-oath archive note — the rig has no place to store a voice

Tomas adds a plain stop to the weight so Rowan can lower it to the same marked depth without relying on a spoken count. Lyra tests the rig with an empty backing before the Echo Kelp strip is attached. Its small lamp edge shows where the instrument sits, but the device has no reed, horn or memory plate capable of keeping a voice.

The Warden asks that the inventory say this plainly. He does not want a later keeper to describe the charm as a key to his memory. It is a positioning tool for repeatable measurements. If the hall answers differently next season, the team can compare the current response without playing or extracting any remembered words.""",
    "warden_oath_time_marks_record": """Supplemental first-oath archive note — repairs interrupt the pattern

Rowan overlays a transparent grid on the three stone marks and draws the two repairs as bands that cover their edges. The distances between visible grooves can be measured, but the covered portions cannot be reconstructed from symmetry alone. Tomas suggests extending the lines across the repair to make a cleaner diagram; Lyra declines and keeps the break visible.

The Warden recognizes one mark from a later visit but is unsure which repair was present then. His statement is dated to the current interview, not placed into the gap between the marks. The archive can preserve what he recognizes without allowing that recognition to date the stone.""",
    "warden_oath_stairs_record": """Supplemental first-oath archive note — an echo changes with the listener

Rowan repeats the test tone from the upper step after Lyra moves the water gate by one notch. The sound carries farther, but the side channel masks its tail from the lower mark. When Rowan trades places with the Warden, both describe a different point at which the note becomes difficult to hear. The group records positions before comparing impressions.

The Warden's memory of following a note down the stairs remains his account, not a measurement made by the present crew. The experiment shows why a remembered echo may feel continuous to one person and interrupted to another. It does not identify the note's source or prove that everyone in the room heard it.""",
    "warden_oath_first_promise_record": """Supplemental first-oath archive note — the promise had a speaker

The Warden repeats the sentence slowly while Lyra writes down each clause. He remembers promising to keep the names entrusted to him; he does not remember pledging authority over the choices of people not yet born. The later heading joined those ideas by using “every generation” as its subject. The change seems small on a shelf label and large in the rule built around it.

Lyra preserves the two sentences in separate columns. The Warden does not ask her to destroy the expanded heading because generations have acted under it. He asks that readers see how the wording widened, and that his own promise not be used as consent supplied by future people.""",
    "warden_oath_lyra_layers_record": """Supplemental first-oath archive note — layers can be read in both directions

Lyra makes a new folio where the oldest account appears first, followed by the later heading and a note about when the pages were joined. A reader can start with the memory and see how it became doctrine, or start with the doctrine and trace the phrase back to the narrower source. Neither path hides the other leaf.

The Warden asks Lyra to leave the editorial label large enough to see without a guide. She worries that the archive will look accusatory toward the copyist. He answers that recording a change is not the same as accusing its maker. The layer describes what the page did across time; motive remains outside the record unless another source supplies it.""",
    "warden_oath_light_test_record": """Supplemental first-oath archive note — a difference belongs beside its conditions

At the lower waterline, the shallow mark on the scale catches a narrow reflection. After the sluice rises, the same mark appears broader, while the test tone weakens at the deeper rig setting. Rowan leaves the lamp at a fixed angle and writes down the gap between trials. Lyra checks that the second reading was not copied from the first card.

They retain both results even though neither supports a simple rule about the hall. A future listener can repeat the setup at either water height and compare new readings. The Warden's memory is not used as a baseline. This experiment shows how today's space responds to today's water, light and equipment.""",
    "warden_oath_archive_copy_record": """Supplemental first-oath archive note — the seam gives an order, not a reason

Lyra inspects the thread holes and finds that the lower heading leaf was stitched into the folio after the older account had already been bound. Rowan sketches the seam and marks the holes that do not line up. The repair dates the physical joining relative to the surviving binding, but the archive has no dated work order for the stitch.

The copyist's choice may have followed a shelf convention, a request from a later keeper or a reason now lost. Lyra records each as a possible question rather than filling the field with a likely answer. Readers can see when the heading entered the folio without being told why the person who added it did so.""",
    "warden_oath_private_memory_record": """Supplemental first-oath archive note — a feeling belongs in first person

The Warden remembers pressing his palm against cold stone, then pulling it away when another voice began to speak. He cannot say whether that voice came from the upper stair, the chamber entrance or someone beside him. He is certain the stone felt cold to him; he is not certain what the sensation meant or what season produced it.

Lyra keeps the description in his first-person account and declines to translate it into a water temperature. The room's present measurements cannot travel backward into a night with no instrument record. The memory helps a reader understand how the oath stayed with him without becoming evidence of a dated climate or a complete room plan.""",
    "warden_oath_measure_card_record": """Supplemental first-oath archive note — the card joins references, not conclusions

The Warden asks Lyra to read the three rows back in a different order. The present-day test remains intelligible when separated from the copyist's heading, and the memory remains readable when the measurement is covered. Rowan adds a source mark beside every date so the empty calendar field cannot borrow the date of the paper below it.

The card's purpose is to make the archive navigable for someone arriving centuries later. It does not reduce the three sources to a single score. If a new test disagrees with Rowan's readings, the card can accept a fourth row without changing the remembered sentence or the history of its heading.""",
    "warden_oath_policy_record": """Supplemental first-oath archive note — access belongs to the speaker

The First Warden wants the archive to name its own use of his account. He agrees that the later heading should remain available for study, since it shaped the council's decisions, but he does not agree that his private memory must be public forever. Lyra writes both permissions on the policy card: the heading and copy history may be inspected; the first-person account follows the Warden's selected route.

The choice does not alter which pages came first or which words he remembers. It changes who can read the personal account now and how a future request may be made. The method for testing the hall remains open under either policy.""",
    "warden_oath_public_open_record": """Supplemental first-oath archive note — an account can begin without declaring a rule

The Warden removes the phrase “from the beginning” from his opening sentence. It implies that his memory contains a full chronology, when what he remembers most clearly is the promise and the cold surface beneath his hand. He leaves that detail in the first person and marks the date as undetermined.

Lyra asks whether the narrower opening will make readers think the archive is uncertain about everything. The Warden says the archive should be precise about the parts it can check and honest about the part it cannot. The public page gives one witness's account, with enough context to read it and no claim that every listener shared it.""",
    "warden_oath_public_folio_record": """Supplemental first-oath archive note — the labels need no interpreter

Rowan moves the copy-history label below the account, where a reader can see that it belongs to another page. The Warden's name appears beside the first-person text; the copyist's field remains open pending a stronger identification. A reader should not need Lyra standing nearby to know which words belong to which layer.

The correction margin is attached to the sheet it concerns. If someone dates the copyist later, the added date will not look like part of the Warden's memory. The folio's layout treats authorship as part of the evidence rather than a detail hidden in a catalogue screen.""",
    "warden_oath_public_method_record": """Supplemental first-oath archive note — the low note is a chosen control

Lyra explains that the rig uses a low test tone because it can be produced at the same setting without retaining a human voice. The method card records the bell's position, weight depth, waterline, two listener marks and the length of each interval. Visitors are asked to note any change to the equipment rather than silently copying the prior setting.

The Warden approves the method but asks that no one call it a reconstruction. It is a present-day comparison chosen to protect the private quality of a memory. A repeatable procedure can test whether the hall's current response changes; it cannot recover a lost audience or authenticate a sentence from the first cycle.""",
    "warden_oath_public_lyra_record": """Supplemental first-oath archive note — a review can test the page's clarity

Lyra reads the public copy once as a visitor who knows the Warden and once as a visitor who has never met him. The headings let both readers distinguish the memory from the later title. She does not certify that the memory is factually complete; there is no independent witness list against which to check it.

Her review card names the sentences that may be quoted and the parts that remain undated. A later keeper can perform the same legibility check after a copy is moved or repaired. The review is repeatable because it asks a narrow question about the page, not because every reader must reach the same opinion.""",
    "warden_oath_public_margin_record": """Supplemental first-oath archive note — blank fields need labels too

Rowan adds the words “date not preserved” above the first blank. Without that note, a visitor could assume a clerk forgot to finish the form. The second blank is marked “additional witness, if one is identified”; it does not ask the Warden to name someone from an uncertain memory.

The public sheet says who may attach new evidence and how the addition will be dated. It does not promise that a witness exists or will appear. The Warden asks Lyra to keep the margin visible rather than decorating it with a symbol of completion. An unfinished field is part of the archive's current state.""",
    "warden_oath_public_sign_record": """Supplemental first-oath archive note — signing authenticates the present account

The Warden reads the boundary statement before signing it. He confirms that the page records his memory as he gave it today, including the missing date and unknown audience. Lyra witnesses the act and writes her own name on a separate line to show she handled the folio; her signature does not become a second witness to the first oath.

The later heading stays on its own sheet with its own author field. A reader can trace who signed what without treating the signatures as a vote on the account's meaning. If a correction is requested, it will be attached as a dated page rather than written over either signature.""",
    "warden_oath_public_board_record": """Supplemental first-oath archive note — posting does not summon a response

The notice is placed where a visitor can read it without entering the private stack. It explains how to request a correction and where to repeat the present-day test. No announcement asks former listeners to come forward, and no name appears as a suspected witness. Lyra wants the invitation to remain available without turning it into a demand.

After the first review, the page stays unchanged because no new source has arrived. The archive does not add a mark reading “confirmed by silence.” The Warden accepts that public access can make a memory visible while leaving the room's other voices uncounted.""",
    "warden_oath_public_after_record": """Supplemental first-oath archive note — a smaller memory can be carried

The Warden reads his account without the later heading printed above it. He pauses at the line about keeping entrusted names and does not add a list. The old title once made the promise feel like a command he had renewed for every person who followed him. Read by itself, it is the promise he remembers making in one room.

He says the page feels lighter, not because he has forgotten the generations shaped by the heading, but because he no longer has to claim they all consented through him. Lyra records this reaction as his current response to the layout, not as a conclusion about what every generation believed.""",
    "warden_oath_sealed_open_record": """Supplemental first-oath archive note — the public record names the boundary

The public index states that a private folio exists, identifies its custodian and gives the route for requesting a review. It does not summarize the Warden's private wording. Lyra asks him to choose a review interval, and he leaves the date open until he wants to revisit it. The procedure permits a request; it does not schedule one on his behalf.

The later heading remains public with its attachment history. This lets readers study the archive's influence while the Warden controls the access to his own memory. The two facts are deliberately held together: privacy for the speaker does not erase the institution's record of what it did with his account.""",
    "warden_oath_sealed_receipt_record": """Supplemental first-oath archive note — the receipt names the action

Lyra writes the folio's copy number, the date it enters restricted custody and the person authorized to request an opening. She leaves the reaction field empty because no reading has occurred. When the Warden requests access later, that action receives another line rather than being described as approval of the account.

The receipt distinguishes speaker, holder and reader. Lyra may keep the case secure without becoming the author of its memory; the Warden may be its speaker without controlling the public copy history. Those roles can overlap in the archive but should never be collapsed into a single signature.""",
    "warden_oath_sealed_lyra_record": """Supplemental first-oath archive note — a custodian can refuse to paraphrase

Lyra declines to write a short public summary of the restricted account. Even a careful paraphrase could make the Warden's private words appear to speak for the first cycle. The index instead states only the folio's subject, its access rule and the date of the most recent custody check.

She keeps a sealed note explaining how to process a future request. It does not contain the memory itself. If Lyra is no longer the archivist, the next keeper can honor the Warden's rule without inheriting permission to retell his words.""",
    "warden_oath_sealed_method_record": """Supplemental first-oath archive note — an open method does not expose a private page

The public method card includes a drawing of the current rig, the waterline mark and a reset instruction for the weight. It contains no quotation from the Warden, no image of the sealed folio and no clue that would let a visitor infer its sentences. A craftsman can repeat the test without requesting access to the memory.

Lyra tests the method using the same blank folio case that carries the equipment, to confirm that no audio is stored by the rig. The check is logged separately from the historical account. Publishing a procedure gives the public a way to inspect present conditions while leaving the speaker's access boundary intact.""",
    "warden_oath_sealed_copy_record": """Supplemental first-oath archive note — a later title can be studied without the memory

The public shelf holds a copy of the later heading with the paper seam drawn beside it. The label says that the underlying first-person memory is restricted and does not paraphrase its contents. Scholars may compare how the heading was copied across later indexes without seeing the private folio.

The Warden worries that keeping the heading public may preserve its influence. Lyra replies that removing it would hide the way a phrase shaped the archive. They leave the heading in view with its date and editorial status attached, so readers can study the expansion without mistaking it for his original sentence.""",
    "warden_oath_sealed_sign_record": """Supplemental first-oath archive note — access can change without erasing the change

The Warden signs the rule as speaker and asks Lyra to write the date in words as well as numbers. If he later closes the review path, the ledger will record the date of closure but will not copy or summarize the private memory. If he reopens it, the new authorization receives its own line.

The rule gives him a continuing choice about access. It does not give him the power to erase the archive's account of how later clerks used the heading. The signed page applies to his own words; the public copy history remains a separate record with its own author and custodian.""",
    "warden_oath_sealed_mark_record": """Supplemental first-oath archive note — the seal is an event marker

Lyra divides the wax mark across the folio flap and its case. She records the wax batch, the custodian and the person who may request an opening. If the mark is broken during routine inspection, the case is not resealed quietly; a witness signs a handling receipt and a new mark is given a new number.

The Warden asks that the archive avoid words such as “untouchable.” A seal can show that a particular handling event occurred, but it cannot prove that no one ever approached the case. The procedure makes custody visible without pretending that material controls are perfect.""",
    "warden_oath_sealed_after_record": """Supplemental first-oath archive note — the public layers remain available

The Warden checks that the shelf still contains the later heading, its seam drawing and the current test method. His own memory remains closed under the rule he selected. He does not ask Lyra to remove the public pages simply because he chose a private route for the first-person account.

This distinction matters to him: the archive may need to examine its own history even when a witness limits access to personal words. The case remains ready for a request, but Lyra will not announce that an opening is expected. Both the decision to read and the decision to leave the folio closed belong to the speaker.""",
    "warden_oath_new_test_record": """Supplemental first-oath archive note — a new depth adds a new condition

The higher rig position places the weight nearer the water's surface and changes how quickly the low tone fades. Rowan measures from the marked stair rather than from the railing, which shifts slightly when the sluice fills. Lyra writes that shift beside the result so a future repeat can use the same reference.

The Warden listens from the doorway but does not report whether the new tone resembles his memory. The test card remains valid without his comparison. It records what the hall does now under a named setup, leaving the historical recollection where it belongs: in the account of one witness.""",
    "warden_oath_second_kelp_record": """Supplemental first-oath archive note — two leaves have two growth histories

Lyra lays the samples on separate damp cloths and checks their harvest labels before comparing them. The older leaf came from the eastern bed after a week of still water; the newer one grew near the channel after the sluice was used. The short vibration may reflect age, water movement or a difference in the plant itself.

Rowan does not crush the leaves to force a stronger reading. Both are returned to their own storage sleeves after the observation. A future gardener can repeat the comparison with another pair. The result belongs to current plant growth and cannot establish how Echo Kelp behaved during the first oath.""",
    "warden_oath_second_koi_record": """Supplemental first-oath archive note — the waterline belongs beside the catch

The first fish was caught below the lower step; the second was caught after the pool rose to the pale mark. Rowan uses the same bait and the same small tray, but Lyra records that the wind has changed. They compare how long the sample responds without claiming the two catches are identical trials.

The Warden remembers a delay between one note and another. He leaves that wording untouched while the team records the two present catches. A current sample can help the archive describe the pool's variation and improve a later test. It cannot verify that a remembered delay happened in the same way centuries ago.""",
    "warden_oath_lyra_review_record": """Supplemental first-oath archive note — an access policy cannot move a page in time

Lyra checks the folio index after the Warden selects his route. The public copy still names the heading's attachment date, and the restricted receipt still names the current holder. She confirms that neither page has been moved to make the memory appear older or newer than the evidence permits.

Her review has two checks: can a reader tell which words are the Warden's, and can a custodian tell who may open the private copy? It does not decide whether the memory is complete. Repeating the review after a policy change can verify the labels again without changing the order of the sources.""",
    "warden_oath_copy_review_record": """Supplemental first-oath archive note — consequences need a source too

Lyra interviews a later archivist who remembers being taught the heading as a universal rule. She records the lesson as that archivist's memory, with its own date, rather than using it to claim every generation learned the same thing. The heading's wide use can be documented through surviving copies; its effect on every listener cannot.

The note sits beside the copy history because readers need to understand that an editorial title may shape behavior. It does not blame one unknown copyist for the entire cycle. The Warden agrees that the archive should preserve both the heading's consequences and the limits of evidence about its author.""",
    "warden_oath_warden_walk_record": """Supplemental first-oath archive note — leaving the room is not leaving the promise

The Warden walks as far as the garden doorway and stops where the damp stone changes to dry tile. Rowan offers to accompany him back, but he asks for a moment alone. No quest log calls the walk a departure and no farewell is written on the folio. The record says only that he chose to stand beyond the bell chamber during this visit.

Lyra does not turn the gesture into a sign of what he will choose at the end of the story. The Warden can question the archive's old use of his promise without withdrawing every act of care that followed. For now, he has taken one short step outside a room that held him for centuries.""",
    "warden_oath_future_marker_record": """Supplemental first-oath archive note — do not prewrite the listener's question

The marker's lower half has room for a date, the listener's chosen question and the source of any observation. Lyra rejects a preprinted line that said “the next cycle,” because it assumed someone would inherit the same assignment. The blank should be available to a person who chooses to use it, not presented as an appointment already made.

The Warden asks that the marker stay unsealed and replaceable. If a future listener brings a different question, the archive can attach a new card rather than bending the old one to fit. The available space promises no answer and imposes no duty.""",
    "warden_oath_afterword_record": """Supplemental first-oath archive note — the first page cannot choose the last

Lyra's index closes with the current state of each source: a memory with no reliable date, a later heading with a visible attachment history, and several measurements from the hall as it stands today. The public route exposes the Warden's account under his name; the private route leaves it requestable under his rule. Neither arrangement declares which ending Rowan must choose.

The Warden asks the next reader to begin with the page they are permitted to read and to leave room for another source. His promise to keep entrusted names remains in the archive. The heading that expanded it remains there too. Their difference is now visible, so no one must inherit the same interpretation without seeing how it was made.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All First Warden oath records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} First Warden records; added {after - before} words.")


if __name__ == "__main__":
    main()
