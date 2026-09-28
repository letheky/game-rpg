#!/usr/bin/env python3
"""Add field and maintenance notes to Pella Quinn's Greenwake wall codices."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental Greenwake rootwall note —"

NOTES = {
    "greenwake_rootwall_open_record": """Supplemental Greenwake rootwall note — return to the line she left behind

Pella reads her old sentence beside the repaired patch and recognizes the quick, square letters she used before leaving. She does not cross out “the stone failed.” Instead, she adds the date of her return, the position of the loose block, and a note that the old page was written before anyone measured the footing. Her father taught her to set a wall by eye, but he also taught her to leave a mark another mason could check. She remembers the lesson clearly; she cannot make it a measurement after the fact. Rowan places a fresh blank sheet next to the old entry, so the repair can begin without pretending the earlier record said more than it did.""",
    "greenwake_rootwall_sill_record": """Supplemental Greenwake rootwall note — renew the chalk datum

The original chalk mark has weathered down to a grey fleck. Pella chooses the corner of a fixed stone that remains above the soil line and asks Rowan to photograph it beside the ruler before drawing a new mark. They write the old reference and the new one on separate cards. If the stone shifts, the next crew will know that their measurements no longer share a starting point. The two gaps are not averaged into a cleaner number. One belongs to an earlier survey with an uncertain ruler position; the other belongs to this visit. Pella says that a careful difference can be more useful than a smooth-looking answer.""",
    "greenwake_rootwall_mortar_record": """Supplemental Greenwake rootwall note — keep the moved stone's position visible

The block has already been lifted from the damp earth, so a sketch made now cannot restore its exact place before the garden was cleared. Rowan draws the face that was down and the side that held the loose mortar, then notes which edge was handled first. Pella asks the crew to keep the stone on a timber rest rather than set it upright for a better view. The rest prevents fresh scuffing but does not recover the missing scene. When the block returns to the wall, its new position will be recorded as a repair choice, distinct from whatever position it occupied when it fell.""",
    "greenwake_rootwall_mara_record": """Supplemental Greenwake rootwall note — the blank seasons stay blank

Mara lays the watering book open across two seasons where the ink stops. She remembers that the garden crew was short-handed, but she will not fill the empty dates from a memory that could belong to a neighboring bed. Pella asks whether they should mark those pages as missing. Mara prefers “no surviving entry,” because the book may have been stored elsewhere rather than never written. Rowan adds the phrase to the index without squeezing it into the watering table. They can start a complete schedule now, but it will describe a new period. A full present record cannot tell them what happened during the absent seasons.""",
    "greenwake_rootwall_first_bed_record": """Supplemental Greenwake rootwall note — leave room beside the east bed

The first row sits close enough to the stones that its gardener has to turn sideways to reach the inner plants. Mara shows Pella where a wide basket catches on the wall and where a smaller hand tray passes without brushing the new shoots. They mark both paths on the plot card, then ask the next shift which route is comfortable to use. The test bed keeps its position for comparison, while access to it can still be improved. Pella does not count a harvest as a success if tending the row requires someone to hurt their shoulder or tread on the neighboring plants. That concern belongs to the garden plan, even though it cannot explain the older crack.""",
    "greenwake_rootwall_ring_record": """Supplemental Greenwake rootwall note — check the cutting tool before comparing rings

One branch was trimmed with Mara's narrow pruning knife and the other with an older saw. The cut edges differ, and a shallow nick makes the outer ring harder to follow on the second sample. Pella marks the uncertain arc instead of tracing through it. Rowan measures the same visible radius twice and records which tool made each cut. The growth bands may help choose where to inspect a living root next, but they do not supply dates for the wall. Before another comparison, Mara wants both branches cut with the same cleaned tool and laid in the same orientation. A similar-looking ring is not a calendar unless the method gives it one.""",
    "greenwake_rootwall_mite_record": """Supplemental Greenwake rootwall note — draw the passage before closing it

After the Vine Stalker is gone, loose earth begins to slide into the narrow passage. Rowan places a board beneath the edge so Pella can finish the sketch without leaning against the wall. They draw the creature's route through the soil as it looks now, not as it might have looked before the fight. Mara asks that the opening stay visible until a gardener checks whether small animals still use it. The repair crew can protect the footing without sealing every living gap. Pella writes that the encounter changed the site before their final inspection. The note prevents a later reader from mistaking this cleared tunnel for an untouched view of the old crack.""",
    "greenwake_rootwall_fiber_record": """Supplemental Greenwake rootwall note — two sleeves for two kinds of dirt

The clean fiber and the soil-stained fiber travel in separate sleeves, each with the finder, place and collection time. Rowan notices that a few strands from the clean sample have caught on the outside of the second sleeve. Talia tells him not to brush them back inside; once the packages touch, the second sleeve is relabeled as a handling sample. Pella accepts that the usable piece has become smaller. A tiny material test with a known source is more useful than a larger sample whose path is uncertain. The fiber may inform the removable resin trial. It cannot establish when the wall opened or which living thing first passed through it.""",
    "greenwake_rootwall_talia_record": """Supplemental Greenwake rootwall note — wash one face and preserve the other

Talia draws a line through the middle of the comparison stone, then washes only one side with clean water from a labeled vessel. The other side stays as found. She weighs the stone before and after drying both faces and records how long it sat under the same roof. Pella can compare adhesion on two surfaces without calling either one representative of the entire garden. Talia keeps the rinse water in a jar because the test has added material to it. Nothing from that jar returns to the basin. The small procedure answers a question about this stone and this resin mixture; it does not replace a water inspection by the people responsible for the channel.""",
    "greenwake_rootwall_cinderstone_record": """Supplemental Greenwake rootwall note — a useful example can still be the wrong size

The Cinderwell step demonstrates a clean way to cut a drainage lip, but Pella notices that its underside would concentrate weight on Greenwake's softer soil. Tomas shows her the chisel angle without recommending the same block dimensions. They sketch the cutting line separately from the garden wall plan so a later mason can borrow the craft detail and leave the load estimate open. The step's dark lower edge records repeated wetting at its own site; it does not show how water moves through the Greenwake footing. Pella labels the drawing “method reference.” A good example can transfer a technique while the structure around it still needs its own measurements.""",
    "greenwake_rootwall_moss_record": """Supplemental Greenwake rootwall note — return the remaining moss to its plot

After the resin trial, Mara carries the unused Brineglass Moss back to the Lower Cistern gardener who tended it. The gardener asks for the plot number to stay on the tag because another bed was planted later with a different watering rhythm. Rowan weighs the returned clump and writes down what the trial consumed. Pella had first planned to list the moss as a wall repair ingredient; she changes the page to call it a small experimental additive. The distinction keeps future builders from assuming there is a steady supply. The material came from one cultivated plot and can be requested again only if its grower agrees and the crop allows it.""",
    "greenwake_rootwall_survey_record": """Supplemental Greenwake rootwall note — support the paper before opening it flat

The survey sheet tears at one fold when the corner is pressed against the table. Lyra places a thin backing beneath the page and records which fold was already split before they handle it. Pella holds a light at an angle so the marks on the reverse can be read without rubbing the graphite. They make one tracing and store the original between boards with its front and back identified. No one adds a unit to the old measurements based on what the modern channel uses. The paper can guide a search for a related ledger, while its exact instrument and author remain uncertain. Careful handling preserves questions as well as marks.""",
    "greenwake_rootwall_fish_record": """Supplemental Greenwake rootwall note — the jar has a keeper and an end date

The oil sample stays in a stoppered jar on a shaded shelf, away from the food prep bench. Mara writes the catch location on one side of its card; Pella writes the resin batch number on the other. They agree on a date to discard the remainder unless a second test is planned before then. Rowan records the fish used for the sample as an ingredient in the trial, not as a promise that another catch will be available. The carp was taken with bait and returned through the ordinary kitchen route before its oil was separated. Any future collection must follow the fishing spot's own rules. A wall fitting does not create a right to harvest from the lake.""",
    "greenwake_rootwall_evelyn_record": """Supplemental Greenwake rootwall note — let the instruments share the same shade

For the paired reading, Evelyn moves both stones beneath the same awning and lets the thermometer settle before either value is written. Rowan reads first; Pella repeats without seeing his number. Their results differ by a small amount, so Evelyn records both and checks the instrument against its reference mark. She does not alter the earlier sunlit reading. A paired trial may explain how heat affects the drying sample under the awning, but it cannot convert every previous observation into a controlled experiment. The wall's season-long behavior still needs checks at other times. Evelyn leaves the setup diagram with the tool box so whoever takes the next shift can repeat the placement.""",
    "greenwake_rootwall_workorder_record": """Supplemental Greenwake rootwall note — a blank handoff is a task, not a name to guess

Pella unfolds the work order under the original seal and uses a loose paper guard where the lower edge has worn thin. The repair quantities are legible, but a dark patch covers part of the receiving-shift line. She remembers carrying timber for her father and cannot say who signed the paper after she left. Rowan makes a new handoff sheet that starts with today's date and a clean receiver field. The historical blank remains unchanged. The crew can document who holds the current key and the next inspection without assigning that responsibility to an unknown worker from the past.""",
    "greenwake_rootwall_second_bed_record": """Supplemental Greenwake rootwall note — give the slower row its full place in the book

The inner bed grows more slowly, and one stalk bends where a watering can brushed it. Mara wants the damaged stalk kept in the harvest count but marked as damaged, so the garden can see both what grew and what handling changed. Pella leaves the row tag in place until the next visit instead of moving it beside the more vigorous plants. The seed came from the same packet as the east bed, but soil depth, light and access were different. These paired beds can help plan a new local trial. They cannot tell the crew which condition caused the wall to move, because they were not measuring the wall under matched conditions.""",
    "greenwake_rootwall_measure_record": """Supplemental Greenwake rootwall note — mark where the ruler could not lie flat

At the inner bed, a small stone pushes the ruler away from the root by the width of a nail. Rowan adds a dotted offset line showing where the tool rested. Pella repeats the reading from the opposite side and gets a slightly different range. They keep both ranges on the page and place the tool in a labeled wrap so its worn edge can be checked later. Mara says the useful question for the next visit is whether the same visible root has changed, not whether this one measurement matches an expected number. The wall fitting uses its own mechanical marks. A plant measurement should not quietly become the threshold for moving masonry.""",
    "greenwake_rootwall_craft_resin_record": """Supplemental Greenwake rootwall note — clean the pan before changing the recipe

Mara washes the Still House pan twice and lets it dry before she weighs the next resin batch. A dark trace from the first mixture stays in the corner, so she records the second batch as a continuation with possible carryover rather than a fresh independent test. Pella asks for a new pan if the workshop can spare one. The crew has enough material for the existing sample, not for a larger wall repair. They keep the uncoated control stone under the same roof and put a date beside both pieces. Before any broader use, a mason must test the mixture against the wall's load, weather and removal needs. This recipe is only a bench trial.""",
    "greenwake_rootwall_choice_record": """Supplemental Greenwake rootwall note — ask who can realistically inspect each option

At the garden table, Mara explains that a hinge needs someone to check its gap, while the removable slot needs someone to find and use the service key. A volunteer who lives far from the wall asks whether a missed week would make the slot unsafe. Pella adds a line for the inspection interval and names no one until the caretakers choose their shifts. The crew chooses with those duties visible, rather than comparing the two samples as if they were maintenance-free. A branch of the decision belongs to the people who will tend the wall. The record captures their selected method and leaves room to change it if the schedule proves unworkable.""",
    "greenwake_rootwall_hinge_install_record": """Supplemental Greenwake rootwall note — the hinge's first mark belongs to this morning

Before fitting the hinge, Pella scratches one copper reference line across the two stones and draws a matching line on the plan. After installation, Rowan checks whether the marks still align, then photographs the gap with a scale in view. The copper shows the position on this day; it is not a forecast of where the stones should remain. Mara keeps the fitting key in a labeled box that can be reached without disturbing the bed. If the seam needs to be opened, the gardener can request the key and record why. The reversible joint makes inspection easier. It does not make an unfinished wall safe for every use.""",
    "greenwake_rootwall_hinge_gap_record": """Supplemental Greenwake rootwall note — record the side from which each point was read

Rowan approaches the upper gap from the path, while Pella reads the two lower points from inside the garden. The rough stone edge catches the ruler differently from either side. They repeat the measurements after exchanging positions and mark the reader beside each result. The readings converge at the middle but not at the top. Pella leaves the upper range visible and asks that future checks use the same approach where possible. A different reading angle may explain part of the difference. The crew will not pack the gap merely to make the three figures agree; preserving the mismatch helps the next inspection decide whether it is a surface issue or a change in the joint.""",
    "greenwake_rootwall_hinge_bed_record": """Supplemental Greenwake rootwall note — a leaf can show exposure without showing a cause

At dawn, the wall-facing leaves stay in shade longer than those at the inner edge. By midday the shadow has moved, and the two samples look closer in color. Mara marks both observation times instead of using the first difference to label one plant unhealthy. She asks the gardener to keep the same two tags for another week and to water from the established can marks. Pella's wall check remains on a separate card, since leaf color does not measure stone movement. If the roots are to be compared later, the team will need to note the soil and light as well as the visible growth. The garden remains a living place, not a static gauge.""",
    "greenwake_rootwall_hinge_mara_record": """Supplemental Greenwake rootwall note — do not tie the new root to the old repair

The young root curves toward a damp patch below the hinge. Mara refuses to tie it to the copper mark, even temporarily, because the tie could steer the growth and make the next survey answer a question the gardeners created. She places a loose marker in the soil instead, far enough away that rain will not drive it into the root. Pella schedules another look after the next pruning, when the gardener can see the root without lifting the stones. The clipped sample remains labeled separately from the living branch. Both can teach them something, but only one is still responding to the bed as it grows.""",
    "greenwake_rootwall_hinge_flow_record": """Supplemental Greenwake rootwall note — swap the trays before naming the better slope

The first run-off test put the hinged stone on the lower side of the board. Pella swaps the two stone trays and repeats the same pour from a marked height. This time the unhinged piece sheds less mud. Rowan records the reversed result, then checks that the board did not rock during the second pour. The test suggests the tray position mattered; it says little about a wall anchored in living soil. Mara asks them to repeat with both orientations on another day before the comparison is used in a meeting. The fitting can still be inspected for mud retention, but no single pour establishes drainage performance across Greenwake.""",
    "greenwake_rootwall_hinge_talia_record": """Supplemental Greenwake rootwall note — label what the rinse has touched

Talia writes the order of contact on the sample jar: test stone, collection tray, rinse vessel. The tray had been used earlier for a garden sample, so she moves the sediment to a second container labeled “possible carryover.” Pella asks if they can still use the first jar; Talia says it is suitable for comparing visible particles, not for claiming where every grain began. She does not test the basin water from this material. The working card now says “sediment from a bench rinse” rather than “water residue.” A smaller claim gives the crew a reliable way to repeat the adhesion test without attaching an unsupported water conclusion to it.""",
    "greenwake_rootwall_hinge_review_record": """Supplemental Greenwake rootwall note — make the early check possible to request

Mara adds a box to the schedule for an unscheduled visit after heavy rain or fresh soil loss. She does not define “heavy” by a single number because the hillside drains differently after the garden paths are cleared. Instead, the caretakers can write what they saw and ask for Pella or a mason to look sooner. The next routine date remains on the page, but it can move if no one is available. Pella keeps the box wide enough to include a reason and the person who accepted the request. A flexible review is only useful if someone can call for it and the record shows whether the request reached a worker.""",
    "greenwake_rootwall_hinge_report_record": """Supplemental Greenwake rootwall note — a report can separate observation from repair approval

The first copy describes the gap and living roots but leaves the work order unsigned. Pella makes a second page for the mason to approve any change to the load-bearing stones. Mara can confirm garden conditions without being asked to certify construction. Rowan labels the two pages “field observation” and “repair authorization” and ties them with a removable thread. If a later shift sees a new crack, they can amend the observation without silently rewriting the approval. The wall has a chosen maintenance plan and a named key holder; it has not received an inspection of every stretch. Pella wants the next crew to know exactly which page they are allowed to change.""",
    "greenwake_rootwall_slot_install_record": """Supplemental Greenwake rootwall note — keep the key within the garden's reach

The removable wedge works only if the service tool can be found before the gap closes. Mara asks to keep the key box beneath the covered bench, not in the distant workshop where a caretaker might need to cross a flooded path. Pella checks that the box is reachable from a seated position and adds a large mark to its lid. The tool's location is written on the garden map and the shift board. A person can still decline the service task or pass it to another caretaker. Making the fitting removable is a design property; making its upkeep accessible requires a separate, revisable arrangement.""",
    "greenwake_rootwall_slot_ticks_record": """Supplemental Greenwake rootwall note — explain the tick marks to the next gardener

Mara asks Rowan to demonstrate the center mark without using the words “good” or “bad.” He points to the position where the wedge sat during installation and reads the number from the ruler. Pella adds a small sketch showing how to hold the tool so a new caretaker does not measure from the rounded edge. The two outer ticks still describe the sample's mechanical travel, not a safe growth limit. A caretaker who sees the marker near either edge should request a review rather than push the wedge back by force. The instruction is short enough to post beside the fitting and leaves the final decision with the trained repairer.""",
    "greenwake_rootwall_slot_owen_record": """Supplemental Greenwake rootwall note — keep the sky calendar out of the repair trigger

Owen notices that the planting notes and his wind calendar both turn a page near the same new moon. He could connect their marks with a thin line, but first asks Pella what observation that line would predict. They have no paired series long enough to test whether a sky event changes the root gap. He instead clips the two calendars side by side under separate headings, with their units and observers named. A gardener can still use the wind sheet to choose a sheltered time for work. It does not determine when the wedge should be moved. That trigger remains tied to the visible root and the measured stone gap.""",

    "greenwake_rootwall_slot_fish_record": """Supplemental Greenwake rootwall note — two samples still share one lake

The second Farwake Carp goes into its own jar with a new label and a clean tool. The first jar is still sealed nearby, but the two oils are not pooled. Pella applies each to separate small hinge pins and lets both rest under the same roof. One turns more easily at first; after an hour, the difference is smaller. Rowan writes the elapsed time rather than calling either oil the better choice. Two catches can show that the preparation is repeatable enough for another bench check. They do not show how often carp can be caught or whether the oil will behave the same in wet stone, winter air or a load-bearing joint.""",
    "greenwake_rootwall_slot_calendar_record": """Supplemental Greenwake rootwall note — a missed visit should produce a new date

The week marked for the first wedge check passes while Mara is away caring for the upper beds. No one moves the fitting. When she returns, she records the missed visit and chooses the next available afternoon with Pella, rather than drawing a false checkmark in the old square. Rowan adds a place to note which observations were made after the gap in the schedule. The wall may have changed during that time; the page cannot say whether it did. The calendar now makes a missed shift visible and allows the caretakers to reschedule. A maintenance plan should help people resume the work without pretending they were there.""",
    "greenwake_rootwall_slot_moss_record": """Supplemental Greenwake rootwall note — count the plot before requesting another batch

The Lower Cistern gardener asks the repair crew to bring back an empty sack with the moss tag still tied to it. That lets them see how much was used and whether the requested amount matched the trial. Rowan records the amount returned, the amount left in the plot and the next harvest date supplied by the gardener. Pella changes the materials list from “available” to “grown under agreement.” The distinction matters if another repair crew arrives during a slow season. They may need a different fitting or a later date. The wall plan should not silently turn someone else's crop into a guaranteed supply.""",
    "greenwake_rootwall_slot_service_record": """Supplemental Greenwake rootwall note — record a return even when no repair was needed

At dusk, Tomas signs out the box and walks the path with Mara, who knows where the lower step holds rain. They inspect the wedge, find no reason to adjust it and return the tools before the gate closes. The service card records “checked, unchanged” with both the outgoing and returning times. Pella says the no-change visit matters: otherwise a later reader cannot tell whether the wedge was inspected or simply forgotten. The key box remains available to the next shift and the caretakers can decline future visits if the route is unsafe. A blank service page is not proof that nothing needed attention.""",
    "greenwake_rootwall_slot_report_record": """Supplemental Greenwake rootwall note — keep a copy where the caretaker works

Pella makes one small map for the garden bench and one full drawing for the repair archive. The bench copy includes the wedge position, service box and request path, but leaves out the family details in the older work order. Mara asks that a damp-weather note be added by hand if the path changes again. Rowan numbers both copies and writes where the other one is kept. If a correction is made to either, the caretaker can ask for both to be updated without handing over the original record. The report now travels with the tool people need, while the longer history remains available to anyone responsible for the wall.""",
    "greenwake_rootwall_afterword_record": """Supplemental Greenwake rootwall note — leave the next inspection's author line empty

Pella closes the binder after adding the repair plan, but leaves the next inspector's line untouched. Mara says she can take the first visit; she does not promise every visit after it. The current key holder is named on the shift board and can pass the task along when needed. A spare resin sample is stored with its recipe and discard date, not sealed into the wall as if it could never change. Beyond this repaired stretch, the garden still has stones that have not been measured. The final page gives a new crew the map, tool location and right to revise the method. It does not require them to repeat Pella's choice if the conditions differ.""",
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
    print(f"Expanded {changed} Greenwake rootwall codices; added {added_words} authored words.")


if __name__ == "__main__":
    main()
