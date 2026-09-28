#!/usr/bin/env python3
"""Expand Sister June and Oren Bell's Cinderwell kitchen codices."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental Cinderwell kitchen note —"

NOTES = {
    "june_stonepot_open_record": """Supplemental Cinderwell kitchen note — leave a place without asking why

June sets the ladle on the table before she calls anyone in. The first person to arrive can take a bowl and sit without telling her which crew they belong to. She keeps a separate pot for anyone who needs to leave quickly, but does not mark the bowl against a roster. The kitchen is a place to eat, not another checkpoint on the road.

Rowan asks how June will know whether the meal reached enough people. She says a list might count servings, but it cannot count hunger outside the room. She will ask whether the pot should stay open and what can be cooked next, then let people answer or keep walking.""",
    "june_stonepot_hearth_record": """Supplemental Cinderwell kitchen note — warmth does not repair stone

June traces the crack with a piece of charcoal and stops where it meets the drainage groove. The line looks unchanged after a small brazier test, but the hearth has not been inspected beneath its ring. She refuses to let Rowan call the mark stable after one short heating. A mason can check the structure when the lower path is safe.

Until then, the portable brazier sits on the dry platform with clear space on every side. The note lists the pot weight and the brief test so another cook can avoid repeating it. Cooking can resume at a smaller scale while the question of a permanent repair stays open.""",
    "june_stonepot_pantry_record": """Supplemental Cinderwell kitchen note — keep wet sacks away from the meal bed

June spreads the sacks on two shelves: dry seams above, softened seams below on a draining board. She does not open the dry sacks just because the Muck has been cleared; each one is checked when a portion is needed. Rowan draws the shelf positions, and June adds the damp line from the flood wall for the next cook.

Some grain is fit for a small meal and some needs Oren's review before it is moved. The new arrangement protects what is usable without turning the pantry into an official reserve. June writes “inspect before serving” on the work card, not “all clear.”""",
    "june_stonepot_draft_record": """Supplemental Cinderwell kitchen note — a safe flame belongs to a shift

Talia and June test the portable brazier once with the sluice wheel idle, then again after a gate worker turns it. The airflow changes when the lower opening is partly covered by a moving cart. They mark the gap and the brazier's uphill position for this shift, with a reminder to check the draft whenever the gate changes.

June asks Rowan not to leave a fixed diagram over the stove as if the room's air never moved. The note is kept near the fire tools where a cook can see it and update it. The meal can be repeated; the exact flame path still depends on who is working nearby.""",
    "june_stonepot_oren_record": """Supplemental Cinderwell kitchen note — kitchen grain and seed grain

Oren counts the trial packet into a small bowl and labels it with the kitchen bed, not the basin reserve. June sets one measure aside for cooking and returns the intact seed heads to him after harvest. The two portions cannot do the same job: a cooked kernel cannot be planted, and a planting seed is not a promised meal.

June asks Oren to write the packet's origin on both containers. If the next crop is poor, the kitchen will know what it used and the reserve ledger will still show no change. The trial creates a choice for this meal without pretending to solve the basin's food supply.""",
    "june_stonepot_grow_record": """Supplemental Cinderwell kitchen note — one harvest teaches one bed

The kitchen bed received morning water from a small can while the outer basin plots waited on the sluice schedule. June records each watering instead of calling the warm wall a reliable advantage. The plants matured, but the crop occupied only one short row and grew under one wall's shade pattern.

After harvest, June and Oren sort the heads on separate cloths. Barley with intact kernels goes back for seed review; cracked grain goes to the meal bowl. Rowan notes the distinction so later cooks do not copy the cooking portion into the garden ledger. The harvest is useful and local, not a forecast for every field in Cinderwell.""",
    "june_stonepot_fish_record": """Supplemental Cinderwell kitchen note — bring the catch to the cook, not the ledger

June meets Rowan at the kitchen door with a clean board and asks where the fish was caught, when and with which bait. She records one Emberscale Perch from the Warm Run and sends the water question to Talia's separate notebook. The kitchen needs a food-handling note, while the sluice team needs observations about the outlet; one page should not claim both.

The fish is cleaned for the meal, and the catch record stays with the recipe ingredients. A single perch does not tell them how many fish remain or whether the water is safe to drink. It gives June one ingredient she can cook today.""",
    "june_stonepot_grindstone_record": """Supplemental Cinderwell kitchen note — the small mill has a small batch limit

June catches the ground barley in a shallow tray and checks it for grit with her fingertips. The lower lip is brushed before each use, then the hand mill is wrapped so dust from the pantry cannot fall into it. A single kitchen portion takes only a few turns; a full reserve sack would need more space, time and a different cleaning plan.

Oren asks whether the mill's steady turn means it is ready for a public work line. June says it is ready for this batch. She logs the cleaning and amount used so the kitchen can decide later whether the same tool can serve more people.""",
    "june_stonepot_cook_record": """Supplemental Cinderwell kitchen note — repeat the pot, adapt the serving

The first pot yields two bowls from two measures of barley and one perch. June writes down when the barley enters the water and how long the pot stays over the brazier, but she leaves the seasoning line blank for whoever cooks next. Rowan keeps one bowl for travel recovery; the other goes to the table or into the road crate according to the choice made in the route.

The recipe describes how to make this batch, not how every person should eat. June asks cooks to offer a smaller serving when requested and to let the person decide whether to take more. The in-game restorative value belongs to Rowan's item; it does not measure the meal's value to the whole kitchen.""",
    "june_stonepot_sample_record": """Supplemental Cinderwell kitchen note — feedback is not a vote tally

June sets three blank slips beside the pot. Anyone can write a note about salt, texture or serving size and leave without signing; the slips are kept apart from the workers' duty board. The first comment asks for a softer barley, while another says the perch should stay in larger pieces. June pins both beside the recipe as suggestions, not as the basin's decision.

Rowan records that one pot was tasted and that its maker was June. A clean bowl and a repeatable method make the next batch easier, but the recipe remains changeable. Nobody needs to praise the meal in exchange for eating it.""",
    "june_stonepot_choice_record": """Supplemental Cinderwell kitchen note — choose where the first bowl goes

June gives Rowan the bowl and lets him carry it either to the people still at the cistern table or to the road crew preparing before dawn. She does not rank the two groups. The kitchen shift faces another sluice check; the road crew faces a longer walk with uncertain stops. Both needs are real, and one bowl cannot settle what anyone should receive tomorrow.

The saved choice records the handoff and opens a different keepsake for Rowan. His second bowl stays in inventory as usable food. June leaves the serving dish by the brazier so either group can return if the next pot is ready.""",
    "june_stonepot_table_record": """Supplemental Cinderwell kitchen note — keep the ladle within reach

The workers who remain for the meal serve themselves while June checks the next water schedule. She does not collect names or ask for a signature beside each bowl. One late-shift worker leaves half a serving covered for later; another takes a second spoonful after the first table has finished.

The record counts one bowl placed at the table, not the number of people who ate from it. June prefers a simple line that can be checked against the pot rather than a list that might follow people between shifts. The meal is available to the group present; the note does not claim to know everyone's need.""",
    "june_stonepot_departure_record": """Supplemental Cinderwell kitchen note — pack food without packing a person into the tally

The bowl is left uncovered until steam stops rising, then sealed in the crew's crate beside a clean cup. June writes “one serving packed” on the food slip and keeps it separate from the traveler count. A later handoff can change who carries it without changing the amount that left the kitchen.

The road crew decides among themselves where the meal should sit. Rowan does not write a recipient's name on the lid. If the crew shares it, carries it onward or gives it to someone they meet, that choice remains theirs and is not reported back as a completed quest objective.""",
    "june_stonepot_table_report_record": """Supplemental Cinderwell kitchen note — one comment belongs to one meal

The late-gate worker's request for less salt is written beside the batch number. Another person asks for more barley next time but gives no name, and June leaves the author field blank. The comments can guide the next pot without being described as a survey of the basin or a vote on the recipe.

June keeps the right to adjust the meal and the right to leave it alone if ingredients run short. Anyone may ask for water, a smaller portion or no bowl at all. The kitchen's welcome does not depend on leaving feedback.""",
    "june_stonepot_departure_report_record": """Supplemental Cinderwell kitchen note — the crew owns the handoff after departure

The crew chooses a carrier and checks that the crate latch opens from both sides. June records the serving's departure time because a warm bowl should not sit sealed for hours. She does not ask the carrier to report who eventually ate it. The handoff ends at the gate; after that, the travelers decide how to share the food.

Rowan's page describes the container and the portion, not a person. A future count of meals can compare what left the kitchen with what remained in the pot, but it cannot infer the crew's route or destination. The road stays open beyond this little supply record.""",
    "june_stonepot_afterword_record": """Supplemental Cinderwell kitchen note — the kitchen waits for its next cook

June stores the brazier where the next shift can inspect its legs before lighting it. The recipe hangs inside a clean sleeve, with the hearth crack and current draft card beside it. She asks Oren to tell her when another kitchen packet is ready, but does not reserve grain without his agreement.

The first service made two bowls and gave Rowan one usable item. It did not rebuild the permanent hearth, produce a stable yield or answer how many people need food each day. June will reopen the table when someone chooses to cook and the pantry can spare ingredients.""",
    "oren_seed_tin_open_record": """Supplemental Cinderwell kitchen note — opening a keepsake is its own choice

Oren carries the tin to the kitchen in both hands and leaves it on the scale's wooden platform without weighing it. He asks Rowan to wait while he decides whether to lift the lid himself. June stays nearby but turns to the brazier, giving him room to open it without an audience. The pause is not an objective to complete; it is part of Oren's first visit back to the object.

He finds one packet and a folded note. The seed is small enough for one row, not a promise to supply the basin. Oren wants to know what his mother meant by a visible planting before choosing where the packet will go next.""",
    "oren_seed_tin_hinge_record": """Supplemental Cinderwell kitchen note — both repairs kept the tin useful

Oren rubs a thumb over the first solder bead and remembers his mother's steady hand at the little stove. The raised ridge beside it is his own repair, made with a borrowed iron after water entered the store. He had kept the tin shut because opening it might expose the packet to damp, but also because he was afraid of losing the memory attached to it.

Rowan sketches the two repairs from the same side of the hinge. The drawing records order only as Oren remembers it; it does not assign a year. The lid now opens with care, showing that a family object can be used and still remain recognizable.""",
    "oren_seed_tin_paper_record": """Supplemental Cinderwell kitchen note — the note speaks to a row

June reads the sentence about planting where someone can see it and asks Oren whether his mother used to leave the garden gate open. He remembers her setting a stool beside the row so a child could watch the shoots. The memory helps him understand why the note says “visible,” but it is still Oren's recollection rather than an explanation written by its author.

They return the note beneath the tin lining after copying its words for the family. Rowan does not place the copy in the basin allocation ledger. One row can be shared in daylight without being turned into a promise to feed everyone.""",
    "oren_seed_tin_date_marks_record": """Supplemental Cinderwell kitchen note — a cut counts an opening for one keeper

Oren sets the tin beside the warehouse shelf card. Three cuts inside the lid match how many packets his mother told him she had used; the shelf card has a different symbol for a season's full inventory. The marks are close enough that a clerk once copied one into the other record. Oren asks Lyra to correct the index while leaving both originals visible.

The correction names the source and the person who requested it. It does not claim that the tin's count was official storage data. Keeping the household object separate protects its meaning and prevents a small family mark from altering the basin's reserve ledger.""",
    "oren_seed_tin_june_memory_record": """Supplemental Cinderwell kitchen note — June remembers a kitchen, not a quantity

June remembers Oren's mother turning the thin cake with the side of a flat spoon. When the public kitchen closed, she made one small portion on a stove near the wall so Oren could have the crisp edge. June recalls the smell of barley and the quiet after the last shift, but cannot say how much grain the household stored.

She offers the kitchen because the seed should meet good soil if it is still viable. Oren accepts the offer after asking that the trial lot be kept away from the protected reserve. The memory gives them a meal to make together, not evidence about the basin's old inventory.""",
    "oren_seed_tin_first_row_record": """Supplemental Cinderwell kitchen note — watch this row before naming it a yield

Oren checks the shoots each morning, while June records which part of the bed dries first. He wants to count the plants as soon as they emerge. Rowan suggests waiting until the grain heads can be separated, then recording what survived rather than predicting a harvest from green stalks.

The row matures and produces enough for a recipe trial plus a small packet to review. Oren smiles at the color of the heads, then asks June to leave the drying cloth in the kitchen so he can help sort them. The experience matters to him as a return to gardening with someone else; the count remains a single result from one bed.""",
    "oren_seed_tin_first_heads_record": """Supplemental Cinderwell kitchen note — decide each kernel's use before milling

June places the intact heads in a shallow tray and the loose grain in a bowl. Oren chooses not to grind everything at once. Some barley will become a cake; some will stay whole until a gardener decides whether it can be planted. That split leaves less food for today's meal and more possibility for another row.

Rowan records the amounts after Oren has chosen, not before. The family packet supplies the material for both uses, but does not make either one compulsory. The kitchen trial and the future planting are entered on separate cards so their totals do not blur.""",
    "oren_seed_tin_choice_record": """Supplemental Cinderwell kitchen note — a packet can move without becoming a rule

Oren asks Rowan to choose between an unlocked exchange shelf and a dry winter case, but first asks June to confirm that the packet is not part of the strategic reserve. She checks the label and signs only for the kitchen trial lot. The decision concerns where one family packet sleeps this season, not how every grower must share seed.

Oren keeps the tin and its note either way. He wants the next keeper to know why the packet was placed there and how to revisit the choice. A location can be changed when the garden changes; the old arrangement need not become an inherited command.""",
    "oren_seed_tin_exchange_record": """Supplemental Cinderwell kitchen note — a shelf invite can be accepted or passed

The exchange shelf has two trays: one for packets offered and one for notes about growing conditions. Oren places a single packet in the upper tray and leaves the lower tray empty until a gardener chooses to write. No names or return promises are required. The shelf opens to the kitchen growers, not to the reserve ledger.

Oren comes back at the end of the shift and sees that the packet is still there. He does not call the quiet shelf a failure; the seed may be planted later, or remain available for someone who is ready. The tin stays with his household, and the packet's future remains a choice.""",
    "oren_seed_tin_reserve_record": """Supplemental Cinderwell kitchen note — a winter case needs a review date

Oren folds the packet in dry paper and places it beside his household lot, separate from the tin's lining. He writes the origin, the room's current dry shelf and the date for checking moisture again. The case protects a small amount, but the kitchen will still need to inspect it before planting; the label is not a guarantee that every kernel will sprout.

June asks to be told if the case moves so she can update the kitchen index. Oren agrees to a note, not an open-ended transfer of ownership. The winter decision can be reviewed after the cold season without being treated as permanent.""",
    "oren_seed_tin_custody_record": """Supplemental Cinderwell kitchen note — write a reason that can be reconsidered

Oren adds a short line explaining that his mother asked for a visible row and that he chose a storage place for the next packet. He marks the first part as a quotation from the note and the second as his present decision. A future reader can tell which sentence came from his mother and which belongs to him.

He had hidden the tin long enough for its location to feel like an instruction. Now the packet's destination is written where it can be questioned. Oren keeps the right to change it if the next season brings different needs.""",
    "oren_seed_tin_perch_record": """Supplemental Cinderwell kitchen note — carry a fresh catch through one kitchen door

Rowan records the Warm Run location, Earthworm Bait and catch time, then brings the Emberscale Perch to the kitchen board. June checks the fish before adding it to the trial; the catch sheet stays with the meal materials rather than the water safety file. The outlet and the fish's presence are noted separately because neither answers every question about the other.

Oren watches June scale the fish and asks how the filling might fit the thin cake shape he remembers. The cooking decision belongs to the present kitchen. A single catch does not establish the pool's population or future supply.""",
    "oren_seed_tin_june_recipe_record": """Supplemental Cinderwell kitchen note — adaptation can carry memory forward

June makes the first filling in a small bowl and leaves the seasoning unmeasured until Oren tastes it. The shape comes from his family memory; the perch comes from the Warm Run; the method uses the Cinderwell brazier. She writes each source next to its part of the recipe so nobody has to pretend this is the exact cake his mother made.

Oren likes the combination but asks to keep the original note beside the new recipe. The adaptation can be repeated by the kitchen and changed by future cooks. Inheriting a shape does not require freezing every ingredient.""",
    "oren_seed_tin_cook_record": """Supplemental Cinderwell kitchen note — the cake belongs to whoever cooks it

June measures two portions of barley and one perch, then records the pan heat from the brazier mark rather than an assumed stove setting. The first cake is prepared for Rowan's inventory, while Oren and June share a smaller taste to check the filling. The recipe yields one restorative item in the game; the in-world note describes a single cooked trial.

Oren asks that his mother's name remain on the tin note, not on the recipe title as its sole owner. The dish now carries a family memory and a present-day adaptation. Anyone at the kitchen can cook it and leave a different suggestion.""",
    "oren_seed_tin_cooling_rack_record": """Supplemental Cinderwell kitchen note — keep the correction beside the first attempt

The first cake browns at its rim while the center is still soft. June lowers the brazier and turns the next one once more. She writes the first timing on the left and the correction on the right, without scraping out the earlier value. Oren keeps the piece that browned too quickly; it reminds him that a recipe changes when its shape changes.

The correction applies to this filled cake on this portable brazier. It does not rewrite his mother's thinner version. A cook can compare both methods and choose which one to make.""",
    "oren_seed_tin_taste_record": """Supplemental Cinderwell kitchen note — recognition can include difference

Oren recognizes the crisp edge before he tastes the filling. For a moment he expects the old pan and his mother's hand to be beside him; then he notices June's seasoning and the perch. He says the taste is not the same, but that it can belong beside the memory rather than replacing it.

Rowan records Oren's words with his permission and does not label the new recipe “authentic.” The tin note and the kitchen method remain separate pages. Their connection is the family story Oren chooses to tell, not an archive's claim that it can reproduce the past.""",
    "oren_seed_tin_second_packet_record": """Supplemental Cinderwell kitchen note — repeat the planting with a new source label

The second kitchen packet comes from the trial lot, not from the final family packet or Oren's winter case. He offers it after watching the first row mature and seeing that the kitchen can keep cooking grain separate from seed grain. June labels the new row before Rowan plants so the two harvests can be compared without blending their origins.

Oren still asks to see the bed himself. He is not promising to share every future packet; this one is offered for a specific planting under a known set of conditions. The seed's success depends on care, water and the next season.""",
    "oren_seed_tin_empty_tin_record": """Supplemental Cinderwell kitchen note — empty does not mean forgotten

Oren removes the folded note and leaves the tin open on the shelf. The empty space feels unfamiliar, so June places a small cloth beneath the lid to keep it from scratching the wood. They do not fill the tin with the next packet immediately. Oren wants to decide after the garden's review, not because an empty container appears to require a new seed.

The tin can be used again or kept as a family object. Its value no longer depends on keeping the last packet hidden inside it. The recipe sits nearby, but no one seals the two together.""",
    "oren_seed_tin_second_row_record": """Supplemental Cinderwell kitchen note — this time the row has company

Oren and June take turns watering the second row. June leaves a small can beside the bed so the next person knows where to find it, and Oren writes the amount on a reusable slate rather than carving it into the plot marker. Rowan counts the seed heads at harvest and records how many remain suitable for cooking or another planting.

The second row gives Oren a new memory of growing alongside someone else. It does not prove every household can get the same result from the crop. The kitchen can choose to repeat the practice if water and seed are available.""",
    "oren_seed_tin_new_shoots_record": """Supplemental Cinderwell kitchen note — a dry patch asks for a local adjustment

June checks the seam in the warm wall at midday and again after the shade returns. The soil there dries sooner, so she waters that strip rather than giving the whole bed another full can. Oren compares the shoot color on each side and asks Rowan to keep the two observations on the same dated sheet.

The patch is a small feature of this garden, not a permanent map of Cinderwell soil. If the wall is repaired or the sluice schedule changes, the difference may change too. Their note tells the next gardener where to look, not what every bed will do.""",
    "oren_seed_tin_june_aftertaste_record": """Supplemental Cinderwell kitchen note — a guest need not bring a story

June proposes three places at the next table for people who choose to come: someone who remembers Oren's mother, a late-gate worker and a traveler returning from the road. None must explain why they are hungry or prove that they knew the family. Oren likes that the invitation can include his mother's recipe without making it an entry fee.

The kitchen will cook only what its pantry can spare. If fewer people arrive, June will save the remaining grain for another batch. The guest list is never written into the seed ledger.""",
    "oren_seed_tin_note_return_record": """Supplemental Cinderwell kitchen note — put the words where they can be read

Oren smooths the folded note and lays it beside the tin. He asks June not to add a date or signature for his mother; the paper has no such mark, and the family does not know when she wrote it. The original remains in the tin's custody while a readable copy can stay by the kitchen bed.

Daylight changes how Oren sees the instruction. It feels less like a command he must fulfill alone and more like an invitation he can answer with other growers. Both readings are his current understanding, not a claim about what his mother intended in every circumstance.""",
    "oren_seed_tin_next_season_record": """Supplemental Cinderwell kitchen note — review before carrying seed forward

Oren, June and the growers agree to inspect the bed before deciding whether another packet can be spared. The review will check the seed heads, pantry stock and water schedule, then let the people tending the plot make a proposal. Oren will not treat one successful row as a standing allocation.

He plans to keep the tin open, the note visible and the recipe adjustable. A later season may need more seed for planting or more grain for meals. The decision can change while the family story remains intact.""",
    "oren_seed_tin_afterword_record": """Supplemental Cinderwell kitchen note — keep the story and the seed in different hands

Oren remains the person who tells the story of the tin and his mother's note. June keeps the kitchen recipe where any cook can amend its seasoning. The growers decide, season by season, where a trial packet can be planted. No one needs ownership of every part for the memory to survive.

The two rows provided one family keepsake, a recipe trial and a shared afternoon in the garden. They did not replace the basin reserve or prove a dependable harvest. The tin stays open on the shelf, ready for a future choice rather than preserving a rule that no one remembers agreeing to.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Cinderwell kitchen records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Cinderwell kitchen records; added {after - before} words.")


if __name__ == "__main__":
    main()
