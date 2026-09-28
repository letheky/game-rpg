#!/usr/bin/env python3
"""Add character-centered source notes to The Table beside the Forecast."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental table note —"

NOTES = {
    "crownfall_shared_table_open_record": """Supplemental table note — the first tray

The first tray came back with one heel of bread on it. No one could say whether it had been set aside for a late worker, carried from another room, or simply missed when the table was cleared. Ada wrote down where she found it and asked the kitchen to keep returned food separate until its condition could be checked. A surplus was not automatically safe to serve again.

The supper was quieter than the forecast meeting. People asked where the beans came from, whether the portion would change tomorrow, and who had decided that the table closed at dusk. No answer belonged in the grain estimate. Rowan records those questions beside the serving sheet because a meal can be counted without its recipients becoming a survey. The first shift establishes that the proposed table can open. It says nothing yet about who could reach it, who chose not to, or whether the same amount would remain available after a harder day.""",
    "crownfall_shared_table_bowls_record": """Supplemental table note — a bowl with a name beneath it

The chipped bowl has a name scratched under its foot, too faint to read without turning it in the light. Ada does not rub the mark clean to make a better measurement. The kitchen keeper says the bowl was used by several generations of the same household, then lent to the table when the storehouse lost its plain dishes. Neither account identifies the person who made the capacity marks.

The bowl's history matters to the serving trial only as a limit: a familiar household dish is not neutral equipment, and the person who lends it can ask for it back. Rowan compares its volume with the plain bowl using dry barley, empties both, then records the chip and the order of the pours. The result can help a cook choose a bowl that will not tip. It cannot authorize anyone to take this one, assign it to a family, or infer the size of a serving from its scratches.""",
    "crownfall_shared_table_portion_record": """Supplemental table note — the cook's hand

The cook fills the scoop differently when the grain is damp. A level rim is still visible, but a small shake settles the kernels and leaves room for more. She has learned this by making bread through several wet seasons, not by using the scoop as a scale. Ada asks her to demonstrate the gesture twice so the record can distinguish a level measure from a packed one.

The cook agrees to describe the method but refuses to have her hand called a standard. Her wrist is sore after long shifts, and another worker may not be able to make the same motion. Rowan writes both facts beside the comparison. A repeatable tool helps a storekeeper close a balance; a repeatable instruction also has to say what happens when the person following it cannot perform the demonstration. The trial keeps the scoop for inventory and lets each kitchen state its serving method in plain language.""",
    "crownfall_shared_table_alden_record": """Supplemental table note — why the accusation stayed

Alden remembers the flood store because its dispute never reached a clean ending. Two keepers brought different totals to a council hearing. One had issued grain before the water reached the lower stair; the other had counted what remained after the sacks were moved. A clerk copied both pages into one column, and the mismatch was treated as proof that someone had taken food. The missing issue slips were found years later in a crate that had been used to brace the door.

He keeps a single measure because it gives the next watch something they can check without trusting his memory. The flood taught him that a bad ledger can injure an honest worker and leave a real loss unexplained. He accepts that one measure cannot tell the kitchen how much a hungry person needs. His request is narrower: record what leaves the store and allow the rule for eating to be discussed in the open.""",
    "crownfall_shared_table_rota_record": """Supplemental table note — carrying the key

The keeper scheduled to carry the key asks that the rota name the duty, not the household. They are willing to sign for the lock because a missing key affects the whole store; they do not want a public list that turns every late arrival into a question about who they know. Alden checks the returned key in front of Rowan and lets the keeper sign before him.

That order is copied onto the draft. It does not prove that the store was never opened outside the recorded shift. It makes the next handoff visible enough for someone else to ask. The page also notes that a second person can witness the lock without becoming responsible for counting meals. The rota concerns custody of supplies. Attendance remains unrecorded unless a separate, voluntary process is proposed by the people who would be counted.""",
    "crownfall_shared_table_emberroot_record": """Supplemental table note — keeping tomorrow's seed

The gardener who lent the Emberroot seed asks Rowan to keep one root from the harvest only if it is still sound enough to replant. The original packet was not a gift to the storehouse; it was a loan for this bed, with the expectation that a good harvest would return seed to its owner. Ada checks the root before separating it and records the packet as returned rather than adding it to the meal total.

The distinction changes the ledger without changing the crop. One portion was eaten, one was held for a possible next planting, and one was returned under the seed agreement. If the root fails to sprout, the bed cannot promise a second harvest. The record keeps the gardener's claim visible so a future keeper will not mistake a reserve for food that belongs to everyone. Shared work still needs clear terms for what is borrowed and what is offered.""",
    "crownfall_shared_table_bed_record": """Supplemental table note — the bed behind the wall

The western shade is not the only difference between the two halves of the bed. A loose stone channels water from the wall into one corner, and the gardener has set a flat shard there to slow the runoff. Rowan records the shard because moving it would change the next trial. He does not recommend the same arrangement for a bed with a different slope.

Two neighbors help turn the soil, but only one can stay for the harvest. Ada lists labor separately from yield and asks whether the absent worker wants their name on the copy. They choose to leave it out. The page therefore keeps the number of hands as an observation and the personal credit line blank. One small bed can teach the Reach how this patch behaves; it cannot predict every plot or decide how much effort each household owes a common table.""",
    "crownfall_shared_table_minnow_record": """Supplemental table note — the empty hook

Another fisher tries the same bait after Rowan's catch and brings back an empty hook. A third leaves when the lake begins to cloud near the landing. None of these attempts proves that fish have vanished; each describes a different effort under a different condition. The kitchen accepts the single Starlit Minnow, but does not write it into a nightly ration plan.

The fisher asks that the archive not call a failed attempt waste. Time at the lake was spent watching the water and avoiding the storm edge, even though no food came back. Ada adds a place to record attempts only if later estimates include the hours, weather and bait used. A catch is useful to the meal in front of them. A repeated survey would need permission from the fishers and a method that does not make one successful evening stand in for every night.""",
    "crownfall_shared_table_waterline_record": """Supplemental table note — who can cross the landing

When the lake rises, the shortest path to the table crosses the landing stones. A traveler using a cane says the uneven lower step becomes difficult before the water reaches the pale mark. They ask for a second route to remain open along the upper path. The mark records water height; it does not record who can safely approach it.

Rowan walks both paths with the traveler and notes that the upper route takes longer but stays above the wet stone. He does not write the traveler into the public copy. Ada adds the route condition to the serving notice so a cook cannot mistake an empty place at the table for a lack of need. The forecast's water estimate and the meal record remain separate, but access links them in practice: food can be available and still be unreachable.""",
    "crownfall_shared_table_warden_record": """Supplemental table note — the name he cannot recover

The First Warden pauses after describing the keeper with the tapping scoop. He can picture the motion and the dark sleeve, but not the keeper's face. He recalls a child waiting near the door and a second bowl being filled after the rule was explained. He cannot tell whether the child was allowed another portion or whether someone else spoke for them.

The Warden asks that the missing name remain missing. He has seen later copies attach a familiar official's name to an old store rule because a page looked incomplete without one. Rowan preserves the account as an imperfect memory rather than a witness list. It supports the narrow claim that a keeper used a repeated serving motion during one winter. It cannot tell the table what the child needed, what answer they received, or whether an old practice was fair.""",
    "crownfall_shared_table_reserve_record": """Supplemental table note — the borrowed jar

One jar was placed on the reserve shelf by a seed keeper who expects it back after the next planting. The seal is unbroken, but the cord around its neck is the keeper's own, not the storehouse tie. Ada adds a custody note and a date for the keeper to return. Alden first worries that a separate label will make the shelf harder to count, then agrees that an honest total must distinguish common stock from borrowed stock.

The second jar belongs to the storehouse and can be opened if the first planting fails. Its label needs a germination check before it is treated as a reliable reserve. Rowan records the two jars in different columns. Neither is available for the current supper without a new decision from its owner or custodian. The page makes the next action visible; it does not promise that either jar will produce a meal.""",
    "crownfall_shared_table_choice_record": """Supplemental table note — what the trial can decide

Ada asks Rowan to describe the choice without calling either procedure a solution. Under the posted rota, a guest can read who holds the key, how much food was released and when the rule will be reviewed. Under the open table, a guest can eat without giving a name, while the storekeeper sees only what was issued and returned. Both procedures leave questions unanswered.

The team does not use attendance as a score for the player's choice. A larger crowd would not prove that one group is more deserving, and a quiet room would not prove that privacy had succeeded for everyone. The decision sets how this particular trial will be run and what its record can show. Ada leaves a space for comments from people who use the table, including a way to decline the survey. The next review may change the procedure.""",
    "crownfall_shared_table_public_board_record": """Supplemental table note — reading the board aloud

The board is placed where the lower road meets the hall, out of the rain and below the eye line of a seated reader. A volunteer offers to read the rule aloud during the first shift. They ask whether the review date can be repeated at closing, since a notice can be visible and still be missed by someone arriving late or unable to read the lettering.

Ada adds an oral reading to the procedure but does not list who listened. The volunteer's name appears only on the work rota with their permission. A covered box receives notes, and the board explains that a person may speak to Ada instead of writing. These options make the trial easier to approach; they do not guarantee that every concern will reach the archive. Rowan records the placement and the reading time so another group can decide whether the notice was accessible in their own hall.""",
    "crownfall_shared_table_public_forum_record": """Supplemental table note — the cart at dusk

The road gate was held so a cart could pass while its wheel was steadied. People who had been told the serving window began at dusk arrived after the board was read. The correction names the delay but not the cart driver. There is no reason to make one person answer for a schedule that failed to include traffic on the road.

The kitchen keeper proposes a wider window on days when the gate is in use. Ada asks what would happen if the cart were delayed longer than expected. The group adds a second serving period only when food remains safe to hold, and writes that condition plainly. Rowan attaches the correction to the earlier page. The original time is preserved as the rule that was tried, not as a promise the late group ignored.""",
    "crownfall_shared_table_public_receipt_record": """Supplemental table note — a correction with two signatures

The receipt carries two marks that answer different questions. Ada signs that the public record was edited and gives the reason for the change. Alden initials that the store transfer was checked against the scoop and scale. Neither mark certifies the number of people who ate, since no attendance count was gathered.

A later copyist might compress the signatures into one approval line. Rowan adds a margin key explaining why that would be inaccurate. The page also carries the earlier version number and a note that the serving window was extended after the cart delay. Anyone comparing copies can see that the change was deliberate. The signatures make responsibility traceable; they do not turn a limited trial into a final rule for Crownfall Reach.""",
    "crownfall_shared_table_public_posting_record": """Supplemental table note — the handoff at closing

At closing, Alden gives the watch key to the next keeper and reads the review date once more. The new keeper asks whether the posted portion applies when the Emberroot reserve is low. Alden answers that the trial only covers the food counted on this sheet. Ada writes the question in the margin so it can be answered before a shortage, not during one.

The board stays up through a single evening. The group agrees to remove it before turning the trial into a standing schedule, then return with observations from the next shift. Rowan records the handoff as a handoff, not a vote by everyone who ate. Accepting a key commits the keeper to a task for that shift. It does not give them authority to speak for the people who were not present.""",
    "crownfall_shared_table_quiet_room_record": """Supplemental table note — the door that stays open

The room has a door, but the notice says it need not be closed. One guest prefers to sit near the exit and leave as soon as they finish. Another asks whether a wrapped portion can be carried outside for someone who cannot come in. The kitchen sets a clear limit on what can be taken, then leaves the path unobstructed.

Alden checks that the store has enough stock to honor the notice before the room opens. Ada keeps the limit in the public copy so privacy does not become an unlimited promise the kitchen cannot meet. Rowan writes down the room layout and the serving time, not the guests' appearance or reason for attending. A quiet table needs boundaries around supplies and space; it does not need a roll call.""",
    "crownfall_shared_table_quiet_service_record": """Supplemental table note — the covered portion

One guest asks the cook to cover a second bowl and leave it beside the door. They do not give a name. The request can be filled within the trial limit, so the bowl is placed on a clean tray with the meal ingredients listed for anyone who needs to check them. Rowan sees it carried away but does not record who carried it.

Ada asks the kitchen to note that a portion left the table for another person, without treating that as proof that two people were fed. The second person may not receive it, and the guest may have taken it for another reason. The record can safely say that the procedure allowed food to leave the room without an attendance entry. That small privacy choice matters to the trial, even though it cannot measure the meal's final destination.""",
    "crownfall_shared_table_quiet_return_record": """Supplemental table note — the food left on the tray

The returned grain is dry enough to store, but the cook will not reuse a spoonful that touched a wet serving cloth. The amounts are weighed separately. Alden asks whether that means the kitchen wasted food; the cook answers that keeping a store safe is part of serving it, even when a portion must be discarded.

Rowan notes the amount returned, the amount retained and the small quantity that cannot be stored. The totals explain the movement of grain for this shift. They do not show how many people wanted another serving or chose to leave. Ada keeps an anonymous comment box beside the tray but makes clear that a comment is not required to receive a meal. A balance sheet can be complete about its stock while remaining silent about its guests.""",
    "crownfall_shared_table_quiet_review_record": """Supplemental table note — enough for the lock check

The store balances within the scale's margin, and the key is back on its hook. Alden calls this a successful closing procedure. The cook agrees that the stock was handled safely but says nothing about whether the meal was enough. Those statements can both be true because they describe different parts of the evening.

Ada adds a separate line for food safety and keeps the question of portions open for review with the people who use the table. Rowan watches Alden remove the word complete from a draft heading. The page now says the lock check is complete, a distinction the next keeper can verify. A balanced shelf cannot answer a question it was not designed to measure.""",
    "crownfall_shared_table_shared_record_record": """Supplemental table note — copies on opposite sides

The store copy is tied to the key ring; the table copy is kept under the board. Neither copy holds the only version. Ada and Alden compare the review date, instrument note and correction number before separating them. If one page is damaged, the surviving copy can show that an earlier version existed, though it cannot restore every detail.

The gardeners ask that the seed return agreement remain with the table copy because that is where the food decision is discussed. Alden asks for the scoop condition to stay with the store copy. The group places a short reference on both sheets pointing to the other. Rowan records who took custody of each page, but the pages remain available for correction. A common meal does not require a single office to own every part of its history.""",
    "crownfall_shared_table_warden_review_record": """Supplemental table note — the sound of the handle

The scoop makes a small wooden tap when Alden sets it down. The sound brings back the Warden's image of a keeper at the old store, but the Warden cannot say whether the keeper was tapping to settle the grain or simply to hear that the handle remained firm. The gesture has survived in his memory longer than the reason for it.

Ada leaves the sound out of the measure instructions. It can prompt an inspection of the handle, but it cannot calibrate a portion. The Warden agrees that memory should sit beside the present test rather than govern it. The archive keeps the remembered gesture as a clue about how people worked, not as a command to repeat it. Their disagreement remains attached to the record because both the caution and the uncertainty belong to its history.""",
    "crownfall_shared_table_alden_review_record": """Supplemental table note — the mark he chooses to sign

Alden signs the date and key transfer, then leaves the serving recommendation to Ada and the kitchen. He says he once signed a rule that outlived the store conditions that made it useful. A flood had closed one road, grain had come from an emergency cache, and the rule was copied as if it had always applied. He will not make a permanent order from this single shift.

His signature accepts a duty to return for review. It does not certify that every future keeper will arrive or that the rule will remain fair. Ada writes the missed review date as a possible failure state and includes an instruction to suspend the trial if food safety or the reserve is uncertain. The promise has a boundary the next watch can inspect. Alden is still responsible for his part of the rota, but he no longer asks one signature to carry the whole table.""",
    "crownfall_shared_table_afterword_record": """Supplemental table note — an empty space left open

The last sheet has room for a question from the next shift. No one fills it in before the archive closes. Ada asks Rowan not to treat the blank as agreement with the trial; it only means that nobody added a question on this copy before it was stored. The board's box remains available at the table for the next evening.

The two routes leave different kinds of record. One lets the public inspect a serving method while keeping household names out of view. The other keeps the meal open without making attendance a condition, while limiting what can be learned about demand. Neither route settles the world's shortage or cancels Rowan's final oath. They give the Reach a small procedure that can be repeated, questioned and stopped. The empty line leaves room for the people who will live with it to answer in their own time.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Crownfall table records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(NOTES)} Crownfall table records; added {after - before} words.")


if __name__ == "__main__":
    main()
