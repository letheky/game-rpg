#!/usr/bin/env python3
"""Append a later family hearing to Oren Bell's seed-tin archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets/Resources/Content/codex_catalog.json"
MARKER = "Third hearing —"

SCENES = {
    "oren_seed_tin_open_record": """Third hearing — opening the tin can stay ordinary

Oren opens the tin on a quiet afternoon to take out one packet label. He does not gather the kitchen crew or ask June to read the note. Rowan is nearby, but Oren says the small task does not need an audience. He lifts the lid, finds the label, and closes it again before the kettle boils. The act is neither a ceremony nor a measure of how much grief has passed.

Later, Oren tells June that keeping the tin in the workroom has made it easier to treat as an object he uses, rather than a relic he must protect from every hand. He still wants visitors to ask before looking beneath the lining. June adds this as his present preference, not a permanent rule for his family. The archive can record that he chose to open the tin on this date. It cannot infer that future openings will feel the same.""",
    "oren_seed_tin_hinge_record": """Third hearing — the hinge belongs to more than one repair

During a routine cleaning, Oren finds a small copper fleck caught under the hinge pin. It has the same color as the old solder but may have come from Tomas's repair bench. Oren asks Tomas to look without taking the tin away. They compare the fleck with the pin and find no clear way to identify its source, so Rowan records the observation as unresolved.

Tomas offers to replace the hinge before the fleck works loose. Oren asks him to wait until the lid begins to catch. The current hinge opens smoothly, and an unnecessary repair would remove material they have not yet understood. They agree on a simple check: Oren will notice whether the lid shifts sideways and ask for help if it does. The old solder remains visible. The archive shows that repair can mean watching carefully, then deciding together when a change is actually needed.""",
    "oren_seed_tin_paper_record": """Third hearing — copies have different readers

Oren considers making another copy of his mother's note for the family room. His first copy was made so he could tend the trial row without carrying the tin. A cousin who visits the room asks whether the words are intended for everyone to read. Oren says he has not decided. The packet instruction may help a gardener, while the rest of the note is still a family letter.

Rowan proposes a shortened label that names the planting instruction and leaves the personal sentence with Oren. Oren likes the option but wants to compare it with the original before choosing. June does not hurry the decision or call the shorter copy more public. They place both drafts beside the tin, clearly marked as drafts, and leave the wall sleeve empty. The page records who may see each copy only after Oren chooses. Until then, the blank sleeve is an honest state, not a missing task.""",
    "oren_seed_tin_date_marks_record": """Third hearing — a correction should preserve the wrong turn

The old pencil dates return when a visitor copies a photograph of the tin. Oren notices that the copied index leaves out the correction slip and asks Rowan to restore it. The first clerk had mistaken three cuts for three winters; Oren had said he used them to count packets. The correction explains how the error began, who challenged it and why the marks remain undated.

Oren does not want the public copy to turn the clerk into a villain. The question was reasonable until someone treated a guess as a fact. They keep the clerk's initials in the revision history because the person agreed to that credit, then separate the attribution from the family record. The tin's marks stay in the same order. A reader can follow the mistaken interpretation without repeating it. Rowan learns that a good correction does not erase the path that led to a false entry; it makes the path visible enough to avoid walking it again.""",
    "oren_seed_tin_june_memory_record": """Third hearing — June's memory is hers to tell

June remembers the first time she and Oren sorted the packets after the flood. She recalls that he held the tin while she dried the cloth, but she is unsure whether this happened before the convoy report or afterward. Oren remembers the room differently. Neither asks Rowan to decide which sequence is correct. June says she can keep her account in her own notebook, while Oren may keep his memory beside the tin.

They agree to place the two accounts on separate pages with their dates and authors. The pairing shows where the memories overlap without forcing them into a single family chronology. June wants her note read by cooks who may handle seed lots; Oren has not agreed to share the personal note outside the family room. A shared work problem has brought them together, but their permissions remain distinct. Rowan adds no summary that blends their voices. The archive makes room for two recollections and leaves the uncertain date open.""",
    "oren_seed_tin_first_row_record": """Third hearing — the first row was one person's trial

Oren visits the warm-wall bed after it has been replanted by another gardener. The new shoots are thinner than his first row, though the packet came from the same kitchen lot. The planter used a narrower spacing and watered after sunset. Oren asks permission to compare the two rows, then learns the gardener would rather keep their name off the archive. Rowan records the growing conditions without identifying them.

The comparison does not tell Oren that his method was better. Soil, shade and timing all changed, and the second gardener did not ask to repeat his exact steps. They write down both arrangements so someone may choose which to test next. Oren says his first row taught him how to watch the warm wall; it did not give him ownership over every packet derived from the tin. The entry now treats a seed line as shared material and a person's growing method as theirs to disclose or keep private.""",
    "oren_seed_tin_first_heads_record": """Third hearing — a harvest count needs its own purpose

When the first row is sorted again, June asks Oren to weigh the seed heads before they are carried indoors. He agrees for the kitchen trial, then declines to put the result beside the reserve totals. The row was planted in a small bed with unusual warmth; its number cannot describe how much grain the basin can expect from a season. They give the sample a separate tray and write the date and bed position on its tag.

Some heads are dry enough to keep, others are set aside for eating, and a few are too damp to store. Oren chooses the divisions after inspecting them. June does not decide how much must be saved for a later planting. The page records the portions from this harvest and the reason each was separated. It does not call the crop a success or failure for everyone. A count is useful when its purpose travels with it; without that note, a kitchen sample could be mistaken for a promise about winter.""",
    "oren_seed_tin_choice_record": """Third hearing — a choice can be revisited without being undone

At the family's request, Rowan reads back the two possible places for the final packet: the exchange shelf or Oren's winter box. Oren listens to each description and says the original choice was made for this packet, not for every harvest that follows. He still intends to use the box this winter. He does not want the archive to turn that decision into a family tradition before anyone has discussed it again.

June adds a review date after the next planting, leaving space for the family to move it if plans change. The date is an invitation to ask, not an automatic reopening of the box. Oren says he will bring the packet out only if he chooses. Rowan records the branch result because the game needs a stable quest outcome; the family record keeps a separate sentence about how that result may be reconsidered in life. The distinction lets the story resolve a step while the people in it remain free to change their minds.""",
    "oren_seed_tin_exchange_record": """Third hearing — an exchange shelf needs a way to say no

The exchange shelf is used for the first time when a neighbor brings a small packet of beans. Oren offers one measured amount of Cinderwell barley, but the neighbor says they would rather wait until the beans have been planted. No trade occurs. Rowan starts to write “declined,” then Oren asks him to use “no exchange today.” The first phrase could sound like a judgement about the visitor; the second describes only what happened.

They place a blank card beside the shelf explaining that no reason is required to pass. A person may take time, offer something later or leave with nothing. Oren keeps the tin packet behind the shelf rather than setting it out as a public reserve. The barley came from a family lot and is available only in the amount he chose to share. The archive notes that the shelf can host a voluntary offer, not that it guarantees supply or creates a debt between households.""",
    "oren_seed_tin_reserve_record": """Third hearing — winter storage is a plan with an end date

Oren checks the winter box and finds that the wrapping has stayed dry. He asks Rowan to note the inspection, then adds that the storage plan lasts through this season only. A later harvest may be larger, smaller or needed for another purpose. June helps choose a dry shelf but does not label the packet as untouchable. The decision belongs to Oren and the family members who agree to share custody.

Someone asks whether this means the reserve is secure. Oren answers that he can speak for one box in one room, not for every seed store in Cinderwell. He writes the lid condition and the next inspection date, leaving the amount of future planting open. The box protects a small packet from damp; it does not solve a basin-wide shortage. Rowan puts that limit in the public index so a reader cannot carry the family plan into the official supply book without context.""",
    "oren_seed_tin_custody_record": """Third hearing — custody names the task, not the owner

Oren asks his cousin to hold the tin while he moves the winter box to a higher shelf. Rowan offers to write down the handoff. Oren agrees, but asks that the note say the cousin carried the object for one minute, not that the cousin now has custody of the family record. The distinction sounds narrow until someone later sees the note without knowing the room.

They add three separate fields to the card: where the tin is stored, who may open it and who may carry it during a move. Oren keeps the right to change each field. June says the kitchen ledger uses a similar separation for food stock and serving tasks. Rowan notices that reliable records often begin by refusing to collapse several kinds of responsibility into one title. The family chooses to keep the detailed card private and share only the opening rule with the kitchen crew.""",
    "oren_seed_tin_perch_record": """Third hearing — the fish returned to a meal, not a survey

The next Emberscale Perch is caught on a cooler morning. Rowan records the spot and bait as before; June checks it for the kitchen and Oren asks whether it can be used in the cake trial. Talia wants to know whether the catch belongs in her separate water notes. Rowan shows her the time and location, and she decides to make a distinct observation page rather than copy the food record wholesale.

The fish is enough for one recipe test. Its size and condition tell the cooks how to prepare that meal, but they do not establish how many fish remain in the Warm Run. Oren knows the ingredients connect the cake to his mother's packet, yet the fish was gathered independently of the tin. June keeps the kitchen receipt with the recipe. Talia keeps her ecological note with its own limits. The same catch may support different work without one page claiming authority over the others.""",
    "oren_seed_tin_june_recipe_record": """Third hearing — June changes the recipe by asking first

June wants to grind one portion of barley more finely so the cake will hold together after cooling. Oren agrees to a small test but asks her not to change the family note under the tin. They create a kitchen revision card instead, naming the amount ground and the rack used. The first version stays beside it so a cook can repeat either method.

Oren tastes both pieces and prefers the one with the coarser grain. June likes the finer texture. They do not settle the disagreement by averaging the two recipes. June marks each version with the person who asked for it, after checking that both want their preference shared. A cook may make a third version later. The family note remains a planting instruction, while the kitchen recipe remains a working document. Their proximity gives the dish a history without making the mother's words answer every cooking question.""",
    "oren_seed_tin_cook_record": """Third hearing — the cake changes when the room is warm

On a warmer afternoon, the barley cake cools more slowly than it did during the first trial. The center stays soft after the outside has set, so June waits before cutting it. Oren turns the rack toward the open window, then moves it back when dust blows in. Rowan records both changes because the kitchen's position affected the cooling time more than the recipe card had allowed.

They use a clean covered shelf for the next batch and check it again before serving. June does not add a fixed number of minutes that would imply every room behaves the same way. Instead she writes the signs the cook should look for and asks another cook to review the wording. Oren appreciates that the recipe can improve without becoming an authoritative version of his mother's food. The cake is still an experiment in the shared kitchen, and a player may carry a serving without carrying the family story as an explanation.""",
    "oren_seed_tin_cooling_rack_record": """Third hearing — leave space around the rack

The cooling rack is moved twice in one week: once to clear a path for the sluice crew and once because a draft made the cloth cover flap against the cakes. June asks the next cook to leave a hand's width around the tray, but Oren points out that the room's furniture is likely to move again. They sketch the rack's current position and label it as temporary.

Rowan draws a small arrow showing the draft direction during the second test. It helps explain why the cloth shifted, though it does not predict every gust. A cook can move the rack if someone needs the walkway. June asks that the tray not block the water jar or the door. They agree that a clear path matters more than preserving the exact setup from the trial. The recipe archive records an arrangement that worked once and gives the next cook permission to adjust it.""",
    "oren_seed_tin_taste_record": """Third hearing — recognition is not a recovered recipe

Oren recognizes a faint toasted smell in the second cake and says his mother used to make something similar. He cannot tell whether she used barley from this tin or a different grain, and he does not want Rowan to write that she cooked this exact recipe. June asks what the smell brings back to him. He answers with a memory of waiting near a window, not a list of ingredients.

They keep the sensory memory in a personal note and the current method on the cooking card. The cake's warm taste may remind Oren of home, but another person may taste only barley and fish. He does not ask June to name the dish after his mother. She serves it under its practical recipe title and lets Oren decide when he wants to tell the story. A familiar sensation can be meaningful without functioning as proof of a lost formula.""",
    "oren_seed_tin_second_packet_record": """Third hearing — the second packet is not a promise of abundance

Oren opens a second packet after the first row's seed heads are sorted. The amount is small, enough for a comparison bed and no more. A visitor sees the number on the work card and asks whether the tin contains additional packets. Oren answers that the card records one packet taken out; it does not inventory the entire box. The question reminds him that a partial note can accidentally look like a complete count.

He changes the heading to “trial packet used” and keeps the winter-box list private. June helps make a separate kitchen tally for the amount that went into the cake. The pages now answer different questions: what was planted, what was cooked and what remains under family custody. Rowan refuses to add them together into a supply estimate. The two packets are connected by Oren's plan, but they do not create a dependable yield forecast for the basin.""",
    "oren_seed_tin_empty_tin_record": """Third hearing — an empty container may simply be empty

After the second packet is poured into its paper sleeve, Oren finds the tin empty for the first time since the route began. He turns it over and hears no loose seed inside. For a moment he feels relieved, then worries that the sound means the family story has reached its end. June says the tin can remain useful even when it carries no grain; it may protect a note, hold a tool or return to a shelf untouched.

Oren does not decide its next use that day. He folds the sleeve, places it beside the tin and asks Rowan to record that the container is empty at this inspection. No one calls it wasted or sacred. The fact can change when another packet is stored, but the family does not have to fill the space to make the object matter. Oren closes the lid gently and keeps the key. The archive leaves room for a future purpose he has not chosen yet.""",
    "oren_seed_tin_second_row_record": """Third hearing — comparison needs the same question twice

The second row grows in a sheltered tray rather than beside the warm wall. Rowan lays the two planting cards side by side. They differ in soil depth, light, watering time and the hands that tended them. Oren says the comparison may show what happened under two arrangements, but the rows do not isolate a single cause. June writes a new trial proposal that changes only the watering time next season, if the family wants to continue.

The gardeners who tended the tray ask for their names to stay off the public copy. Oren agrees. Their work can be useful without turning them into permanent subjects of a study. The public record shares the method and the limit; the private card keeps the names for anyone who needs to contact them. Rowan sees that a fair comparison depends not only on matching soil and light, but also on what the people involved agreed to share.""",
    "oren_seed_tin_new_shoots_record": """Third hearing — a pale shoot is a reason to observe

One of the new shoots emerges pale at the edge of the tray. Oren resists the urge to pull it up and inspect the root. June asks him to mark its position and check again after the next watering. The shoot may be shaded by the tray lip, or it may be developing differently for another reason. A single appearance cannot settle which explanation is right.

By the following morning, the color is still uneven. Rowan makes a second note rather than crossing out the first. The gardener who tends the tray chooses to move a loose board that casts the shadow, then agrees to take another look. Oren says the small change can be documented without calling the plant sick or rescued. If it grows, the sequence may help another gardener notice a similar pattern; if it does not, the note still describes what they saw. They keep the seed line intact and leave the cause open.""",
    "oren_seed_tin_june_aftertaste_record": """Third hearing — an aftertaste belongs to the person who noticed it

June says the cake leaves a bitter note after it cools. Oren tastes the same piece and notices mostly toasted grain. Neither tells the other that the difference is imagined. They ask whether the batch used the new tray harvest and discover that the ingredient card names the recipe lot but not the row. The cake cannot be traced to one growing condition, so they decline to use its taste as a verdict about either bed.

June adds a question to the next tasting card: “What changed for you after it cooled?” The answer can be left blank. Oren asks that the kitchen not turn the responses into a vote on which family memory is more accurate. The note will help the cook decide whether to serve the cake warm or wait. Taste can guide a recipe while remaining personal. Rowan keeps the growing records and the cooking feedback in linked, separate pages.""",
    "oren_seed_tin_note_return_record": """Third hearing — returning the note does not close its meaning

Oren slides the original note beneath the lining after the family visit. He has made one working copy for the planting table and decided not to pin a copy in the public room yet. June asks if the family discussion changed his reading of the sentence. Oren says it made one word feel different, but the paper itself has not changed. He wants to keep that new interpretation in his own notebook for now.

Rowan checks that the copy is dated and marked as a transcription. He does not press Oren to explain what the word now means. The family can return to the original when they choose, and another reader may hear the instruction differently. The note is not a puzzle with one answer hidden beneath the felt. Its place in the tin preserves the object; it does not require Oren to publish every thought it brings back. The working copy can guide a small bed without claiming to settle the letter's full meaning.""",
    "oren_seed_tin_next_season_record": """Third hearing — next season begins with a question, not an order

Before winter, Oren receives a request for seed from a neighbor who wants to test barley in a cooler courtyard. He says he may have a small amount after the family checks the tin, but he does not promise a packet before that conversation. The neighbor accepts the answer and leaves their own name on a private request card only after Oren offers that option.

June asks whether the kitchen should plan another cake around the same barley. Oren says he would like to wait until the family decides what remains for planting. The meal can change if the ingredient does. Rowan records the request, not a future allocation. The timing allows Oren to consult the people who share the tin without making their permission a public obstacle for the neighbor. No one is owed a harvest that has not happened. The route ends with an intention to ask again when the next season makes the choice real.""",
    "oren_seed_tin_afterword_record": """Third hearing — a family archive can keep changing its shelves

When the kitchen closes for the evening, Oren returns the tin to the upper shelf and leaves the working copy in its sleeve on the planting table. June places the recipe card beside it, with the old and new cooling notes still visible. The three records meet in one room, but each has a different keeper and purpose. Oren decides who may open the tin; June maintains the food instructions; Rowan preserves the field observations.

They agree to review the arrangement after the next planting, not because the current system has failed but because people and needs change. The review may result in the same shelf, another copy or no further public record. Oren says that would not erase what the kitchen and family already did. Rowan closes the archive without adding a final explanation for the mother's note. The box can hold seed again, stay empty or return home. Its next meaning remains with Oren and the family, beyond the quest's completed flag.""",
}


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in catalog["entries"]}
    missing = sorted(set(SCENES) - entries.keys())
    if missing:
        raise SystemExit("Missing Oren seed-tin codex records: " + ", ".join(missing))
    already_expanded = [record_id for record_id in SCENES if MARKER in entries[record_id]["body"]]
    if already_expanded:
        raise SystemExit("Third hearing already exists: " + ", ".join(already_expanded))

    before = sum(len(entry.get("body", "").split()) for entry in catalog["entries"])
    for record_id, scene in SCENES.items():
        entries[record_id]["body"] = entries[record_id]["body"].rstrip() + "\n\n" + scene
    after = sum(len(entry.get("body", "").split()) for entry in catalog["entries"])
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Appended {len(SCENES)} Oren Bell third-hearing scenes ({after - before:,} raw words).")


if __name__ == "__main__":
    main()
