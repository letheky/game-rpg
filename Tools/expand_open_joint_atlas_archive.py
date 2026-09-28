#!/usr/bin/env python3
"""Extend Tomas Reed's Regional Repair Atlas codices with field notes."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental atlas workshop note —"

NOTES = {
    "atlas_open_record": """Supplemental atlas workshop note — the margin belongs to the next repairer

Tomas finds a faint line beneath the first master's old pencil rule. It is not a measurement; it is the pressure mark left by a page that once covered the margin. He asks Rowan to hold the lamp while he compares the bound copy with a loose leaf from the same workshop. The leaf carries a note about a gate hinge after rain. That small addition explains why the original book left room beside each pattern. Tomas had thought the blank was a flaw in the copy. He now writes the two versions side by side and lets the reader see how a working page became a clean diagram.""",
    "atlas_master_gauge_record": """Supplemental atlas workshop note — a removed notch leaves a readable scar

Tomas rubs chalk across the gauge handle, then wipes only the raised surface. The fourth notch takes a thin white line that the other three do not. He does not deepen it to make the old mark easier to see. Rowan traces its current width on a separate card and records that the tool has been filed since the first pattern was drawn. The pins still move, but the scar cannot say who moved them or why. Tomas decides the atlas should show both the adjustable jaws and the fixed mark, with a reminder to check the tool against a known plate before using either as a reference.""",
    "atlas_cart_record": """Supplemental atlas workshop note — listen again after the cart returns

Gideon rolls the empty cart over the same dry strip and stops where the left wheel first caught a pebble. The new axle pin turns without a knock, but the repaired hub carries a faint wobble that Rowan had not noticed while the cart stood still. They mark the strip and repeat the pass once, then stop rather than adding cargo to a repair that has not been inspected under load. Gideon says the sound is different from the old crack. Tomas records that as the driver's observation, not as proof the hub is sound. The gauge describes one contact surface; the cart still needs its own repair check.""",
    "atlas_gideon_record": """Supplemental atlas workshop note — write the load before calling a brace tested

Gideon brings the old roof note to the stand and points to the phrase “strong enough.” He had written it after the brace held through an afternoon of light rain, but before the roof tiles were set back in place. He remembers the relief of seeing the beam stop moving. Rowan asks whether the phrase can remain if its conditions travel with it. Gideon adds the empty beam weight, the rain and the unfinished roof, then leaves the later load blank. The repairer's judgment is still part of the history. It simply cannot promise what was never tried.""",
    "atlas_reed_record": """Supplemental atlas workshop note — replace the reed before grit packs beneath it

A short length of Windglass Reed has flattened where the gauge jaw pressed against the wheel rim. Rowan loosens the pin and finds a few grains caught under the strip. Tomas replaces the packing, puts the used reed in a marked tray and checks the jaw on the clean bench plate again. The tool feels tighter, but the change might come from the new strip or the cleaning. He records both actions before the next measurement. Mara says the spent reed can return to the garden compost only after the metal dust is removed. A soft spacer has a useful life and a disposal path; neither belongs in the structural specification.""",
    "atlas_skate_record": """Supplemental atlas workshop note — the fish oil stays away from shared utensils

Tomas asks the cook for a clean cloth and a small covered dish before Rowan opens the Saltspool Skate sample. The oil is measured with a tool kept for workshop trials, not the kitchen ladle. After the scrap-iron test, the cloth and dish are labeled for disposal so no one mistakes a craft material for food. Rowan writes the bait, catch place and amount used, then seals the remainder. The procedure makes the trial easier to repeat without implying that oil from every catch behaves alike. If another sample is taken, its container starts clean and receives its own date.""",
    "atlas_talia_record": """Supplemental atlas workshop note — name the two scraps before the next watch

Talia asks Rowan to engrave a small A on the treated scrap and a B on its untreated mate. The labels are shallow enough not to change the exposed faces. At the end of the watch, both pieces are lifted with separate hooks and placed on their own dry tiles. One has darkened at the edge; the other carries a similar mark near its cut. Talia refuses to call the result a corrosion ranking until the pair has been checked under a second set of conditions. The trial's value is that the pieces can be found and compared tomorrow, not that the first reading settles a workshop rule.""",
    "atlas_cup_record": """Supplemental atlas workshop note — keep the cup's storage place in the comparison

The covered cup sat on a shelf above the upper channel, away from direct spray. Talia adds a sketch of that shelf because a cup drawn simply as “channel water” could be mistaken for a sample taken from the flowing stream. Rowan repeats the test with a fresh cup and leaves it uncovered for the same interval before the scraps are placed inside. The treated and untreated pieces now show less contrast. Neither run is discarded: the storage difference may matter. A small trial records how its sample reached the bench, since the condition of a container can travel with the water it holds.""",
    "atlas_forge_record": """Supplemental atlas workshop note — tool custody is part of calibration

When the gauge leaves Dawnkeep Forge, Tomas ties its calibration card to the case with a loop that can be opened without cutting it. He writes the current jaw setting, the bench plate used for the check and the name of the forge keeping the tool overnight. At return, another smith can verify whether the jaws shifted in transit. Rowan asks if every borrower must sign. Tomas says the handoff can be marked by a workshop stamp instead, as long as the next custodian is clear. The gauge is shared property for this trial; its care should not depend on guessing who last carried it.""",
    "atlas_fit_test_record": """Supplemental atlas workshop note — stop where the surface stops being stable

The jaw slides when it reaches the old crack, so Rowan paints a small boundary on the scrap board beside the hub rather than on Gideon's cart. Tomas examines the edge with a loupe and finds that the crack has lifted one side of the surface by a fraction. He refuses to force the gauge across it. The resulting reading would describe a tool slipping between two levels, not the fit of a replacement part. Gideon marks the cart for a separate repair inspection and keeps people clear of it until then. A measurement tool can reveal its own limit before it reveals a useful number.""",
    "atlas_mara_record": """Supplemental atlas workshop note — let the person tending the branch choose the check

Mara shows Rowan where last season's tie began to rub after the rain softened its fibers. The mark is shallow, but she does not want the graft tightened by someone who has not watched it grow. She chooses the next inspection day with the gardener who waters that bed and asks that a second person be available to hold the branch, not pull it. Tomas adds both roles to the local note without assigning names to every future shift. A removable brace protects a plant only when it is tended with care. The person with daily knowledge of the stem must be able to ask for a different method.""",
    "atlas_glassplum_record": """Supplemental atlas workshop note — collect a cutting with the grower's label attached

Mara cuts one Glassplum stem below the last healthy joint and leaves its companion in the bed. She marks the sample with the seed packet, row and harvest date before it reaches Tomas's bench. A pollinator net had covered the bed for part of the morning, so the growing conditions were not identical to the open rows. Rowan includes that detail rather than calling the stem a typical Greenwake sample. Mara asks that the cut end be sealed before transport so it does not dry out and change shape. The cutting is material for a fit demonstration, not a token that transfers the garden's seed rights to the forge.""",
    "atlas_stem_fit_record": """Supplemental atlas workshop note — a review date is not an expiry date

At the next watering turn, Mara checks whether the graft tie has begun to press into the stem. It has not, but one leaf has grown against the lower loop. She adjusts the tie by a finger's width and adds the change to the card. Tomas updates the diagram while keeping the first version visible. The review date prompted a look; it did not require the tie to be replaced automatically. Rowan asks whether the interval should be copied to the atlas. Mara says it belongs beside this plant's conditions, with a space for another gardener to choose a different interval after seeing the growth.""",
    "atlas_lyra_record": """Supplemental atlas workshop note — close the door without claiming the room is silent

Lyra shuts the Choir frame-room door after a worker leaves, then waits until the cart noise in the corridor passes. She hears water moving through the wall during the second ring and adds it to the log. The room is quieter, not silent. Rowan asks if she wants to keep the abandoned first recording. Lyra retains a note that it was discarded because it overlapped speech, but does not save the worker's voice or identify them. The atlas needs to say what condition changed between strikes. It does not need to turn an incidental speaker into part of a measurement they never agreed to join.""",
    "atlas_koi_record": """Supplemental atlas workshop note — a vivid catch is still one catch

After Lyra finishes her frame test, Rowan returns to the pool and records the Whisper Koi catch separately. He notes that its scales trembled while the net was lifted, then stops handling it once the observation is complete. The resonance card carries a different time, room and instrument. Tomas considers adding a diagram that links the marks, but Lyra asks what experiment could disprove the connection first. They leave the pages adjacent in the binder without drawing an arrow between them. Readers may compare two records; the archive should not supply a cause merely because the same crew saw both events.""",
    "atlas_sound_card_record": """Supplemental atlas workshop note — note the listener's position before the mallet falls

Lyra places a strip of blue tape where the observer stands and marks the frame's corner with a chalk dot. Rowan strikes from the opposite side on the next trial, keeping the mallet and force as close as he can. The ring seems shorter to him, although the card's timing differs by less than one beat. Lyra preserves the observer position as part of the setup. A later reader can repeat the frame test without treating a person's impression as an error. The instrument offers a comparison under stated conditions; it does not replace the craftsperson's hands, eyes or decision to inspect the joint.""",
    "atlas_ruth_record": """Supplemental atlas workshop note — the signal must remain readable during maintenance

Ruth refuses to take the milepost bracket down during the market day. Travelers rely on its arrow to find the dry road when the lower ford rises. Her crew puts a temporary marker on the opposite post and schedules the repair between wagon departures. Rowan records the temporary marker's position and when it will be removed. A maintenance plan that keeps a sign intact matters as much as the fastener schedule. The bracket's salt exposure still differs from an inland one, and the repair crew will review the schedule after winter. No one should mistake this local calendar for a universal interval.""",
    "atlas_bracket_record": """Supplemental atlas workshop note — preserve the scrape before tightening the pin

Before Ruth turns the lower fastener, Rowan makes a rubbing of the bright scrape and photographs the grit beneath the plate. They save the rubbing with a note that the pin was loose at the time. After tightening, the bracket no longer rocks under a light hand. Ruth declines to call it repaired until a second crew checks it after the next strong wind. The before-image will help them see whether the movement returns. Tightening changed the evidence, so the record keeps both the original condition and the current one instead of overwriting the first with a neat final mark.""",
    "atlas_evelyn_record": """Supplemental atlas workshop note — hide the first mark during the repeat

Evelyn covers her scale reading with a folded card before Rowan takes his turn with the gauge. He reads a slightly different angle and writes it down without seeing hers. They then exchange places and repeat once more. The second pair is closer, but not identical. Evelyn adds a note that the jaw may be held at a tilt and asks Tomas to make a guide for the operator's hand. She does not call one smith more accurate from two trials. Blinding the first mark reduces copying; it does not remove every difference in grip or judgment. The next change to the method remains visible in the record.""",
    "atlas_carp_record": """Supplemental atlas workshop note — one scale can test softness, not identity

Tomas trims a small loose scale from the Farwake Carp sample only after Rowan records how it was caught and handled. The sample flexes beneath the gauge's brass jaw, so Evelyn inserts a padded contact and repeats the pressure test on a bench strip. The scale's response helps them decide whether a softer jaw is worth prototyping. It does not identify a sound at the lake or stand in for the fish itself. Rowan labels the scale as a detached sample and returns the remaining fish through the ordinary kitchen process. The atlas keeps craft use separate from claims about the lake's living population.""",
    "atlas_margin_record": """Supplemental atlas workshop note — invite a third reader before choosing a number

Evelyn leaves the two disputed readings on the bench overnight and asks a smith from another shift to use the written setup without speaking to either of them first. The third reading falls between the two, but the observer notes that the outer rim is uneven. Tomas adds that condition to the margin and preserves all three values. The atlas does not gain certainty by voting among measurements. It gains another description of the surface and a reason to inspect the jaw design. Rowan keeps the word “outlier” crossed through but readable so the next editor can see how the first copy almost hid a real limitation.""",
    "atlas_nia_record": """Supplemental atlas workshop note — ask before a name travels with a correction

A smith brings Nia a corrected measurement and asks to sign it with a workshop mark instead of a personal name. Nia explains that the mark will identify where the method was checked but may still let neighbors guess who wrote it. They choose an edition number and a return date, leaving the author line blank. The correction remains traceable through its source page and review process. Nia keeps the signed original in the restricted cabinet and sends an approved copy to the atlas. A useful correction does not require the writer to surrender more identity than the readers need to verify the method.""",
    "atlas_policy_record": """Supplemental atlas workshop note — distribution comes with work after printing

Tomas asks Rowan who will answer a letter from a distant forge if the open foldout is copied without its newest correction. Nia offers to maintain a dated correction list, but only while the community continues to fund the paper and courier runs. Mara points out that local pages also need a keeper; a small workshop may close or lose its binder. The two options therefore carry different kinds of work, not one public and one private virtue. Rowan records who volunteered for the first review period and leaves the later periods open. People may revise the arrangement if maintaining either route becomes a burden they cannot carry.""",
    "atlas_field_copy_record": """Supplemental atlas workshop note — copy the warning in the same hand's reach

The foldout is printed on a larger sheet than the first trial copy so the warning box stays beside the jaw diagram when the page is folded. A maker should not have to unfold a separate appendix to learn that a fracture invalidates the reading. Gideon tests a copy in the cart kit and finds that rain smears the graphite revision strip. Nia changes the strip to ink and reserves a space for a later edition stamp. The open copy can travel widely, but only if its conditions survive the trip. Reproduction permission does not make a damaged or incomplete copy an approved repair.""",
    "atlas_teach_open_record": """Supplemental atlas workshop note — disagreement can be the first lesson

After the cadets find different readings on the hinge, one asks which of them should teach the gauge. Tomas gives each a clean plate and asks them to describe the surface before taking a measurement. Their methods converge on the flat side and separate again at the worn back. Neither cadet is dismissed. They write a short correction explaining that the tool needs a stable edge. The lesson goes into the next open edition with the original example. Tomas wants young smiths to learn that uncertainty can be a property of the object or method, rather than a failure they must hide from a master.""",
    "atlas_open_report_record": """Supplemental atlas workshop note — Gideon's kit needs a return path for old copies

Gideon takes the foldout with the repair kit and pins a card inside the cart shed naming the edition date. He asks that anyone who finds an older sheet return it to the shed or add its date to the correction envelope. The drawings may remain useful, but a superseded instruction should not circulate as if it were current. Rowan writes a simple notice that does not require a person's name. Gideon wants neighbors to challenge a bad fit without fearing they will be blamed for following the page. The public method is open to use and open to correction.""",
    "atlas_local_pages_record": """Supplemental atlas workshop note — return the local binder before leaving the forge

The local binder stays on the forge's dry shelf. A visiting maker may borrow a tracing, but the original page remains there so revisions do not split across copies. Tomas adds a checkout card for the tracing, not for the borrower's identity unless they choose to include it. At the end of the work, the sheet goes back into its numbered sleeve. The arrangement helps this forge keep a shared history; a neighboring shop may prefer to keep its own copy. Nia writes that local custody is a decision of the workshop, not a rule Tomas can impose on all of them.""",
    "atlas_teach_local_record": """Supplemental atlas workshop note — explain why the master changed the jaw

Tomas finds the old note folded beneath the altered gauge: the softer hinges had begun to show a crescent mark after the winter rain. His master changed the jaw to spread the contact, then kept the earlier version beside it for comparison. Tomas realizes that the notch was not an accusation but a record of material meeting weather. He copies the explanation into the local binder, including that the old jaw remains available for a controlled bench test. A later maker can decide whether the same change fits their metal. The story does not turn one master's fix into a rule for every shop.""",
    "atlas_local_report_record": """Supplemental atlas workshop note — review without turning the cover into a roster

When the review season arrives, Nia places a blank card by the forge door for comments about the gauge. Some makers mark the page number; others leave a question without signing it. Nia responds on a separate sheet and pins it beside the binder rather than filling the contributor list. The workshop can tell which instruction needs review without keeping a permanent record of who raised it. If a correction requires direct follow-up, the person may leave a private contact in a sealed envelope. The review date opens a chance to revise the method; it does not renew consent to publish anyone's name.""",
    "atlas_afterword_record": """Supplemental atlas workshop note — leave the last line for the next material

Tomas closes the book only long enough to tie the loose sheets together. On the cover he writes the six places where the gauge was tried and the limits recorded at each. He leaves the seventh line blank because no one has yet tested it against winter ice or a moving bridge. The blank is not a promised destination; a future craftsperson can use it for a question that matters to their work. Rowan asks if the atlas is finished. Tomas says the first edition is finished, while the practice of checking a repair belongs to whoever chooses to use it. The book can offer a method without owning the next decision.""",
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
    print(f"Expanded {changed} Regional Repair Atlas codices; added {added_words} authored words.")


if __name__ == "__main__":
    main()
