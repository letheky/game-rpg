#!/usr/bin/env python3
"""Append a second, route-aware hearing to Gideon's Ashfall cart archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets/Resources/Content/codex_catalog.json"
MARKER = "Second road hearing —"

SCENES = {
    "ashfall_cart_offer_record": """Second road hearing — the offer is not ownership

After the repaired cart returns from its first trip, Mira asks Gideon whether the people who accepted the offer still consider it his. Gideon says he brought the old frame into the square, but that does not give him a claim over every journey it may carry. Mira remembers who first used it for medicine; another neighbor remembers the blankets tied along its side. The recollections do not agree about which trip came first, so Rowan keeps both beside the date of the repair.

They leave the cart where visitors can see it and let the next person choose whether to use it. Gideon refuses to turn the offer into a sign-up list. A person may ask for a ride without explaining why, and a person may decline to lend the cart without being called selfish. The archive records how the object became available, not who now deserves it. Its earlier use remains part of the history, while the next trip belongs to whoever agrees to make it.""",
    "ashfall_cart_wheel_record": """Second road hearing — the crack gets a new inspection date

Tomas checks the wheel after the second rain. The iron ring still sits evenly against the rim, but a wet stain has made the old split difficult to see. He dries the wood with a cloth and asks Rowan to mark the crack's end again from the same side. It has not visibly advanced. Tomas writes that as one comparison under damp conditions, not as a guarantee that the wheel will stay unchanged.

Gideon wants to roll the cart immediately and is disappointed when Tomas asks him to wait until the wood is fully dry. Their disagreement is small but useful: urgency has not made the damaged section easier to judge. The new card gives the wheel another inspection date and says to stop if the ring shifts or the split lengthens. No one calls the cart unsafe forever or safe without limit. They have a repair that can be watched and a clear reason to return it to the stand.""",
    "ashfall_cart_medicine_record": """Second road hearing — the medicine stays within reach

Mira tests the cloth knot with a glass bottle filled to the same level as a tonic jar. On the first run, the knot loosens where the cart bounces over the village stones. She moves the tie point farther inside the rail and asks Rowan to walk beside the wheel while she watches the load. The second run holds, though they have tested only a light parcel over a short path.

Mira leaves one small space open beside the bottle. A traveler should be able to take the medicine without unpacking the blankets or asking Gideon to move the whole load. She does not label the space with a patient's name. The card says what can be reached and how the knot was tied; it does not say who needs the jar. Gideon offers to carry the first parcel, then asks whether someone else wants the handle. Mira lets the crew decide. A practical handoff can keep help available without making the recipient visible to everyone in the square.""",
    "ashfall_cart_rut_record": """Second road hearing — one rut changes after the storm

The east rut is shallower than it was on the day Rowan measured it. Rain filled the low point, and a neighbor packed the edge with broken brick before the cart came back. Gideon recognizes the curve but not the exact patch of ground. Rowan repeats the test with the empty cart and draws a new chalk line beside the old one. The wheel follows a slightly wider turn.

Tomas asks them to keep the earlier mark instead of replacing it. The first line belongs to dry ground; the second belongs to a patched lane after rain. Both can help another driver understand why the cart was guided around the stone step. Neither line is a permanent road instruction. A child points out that the turning space narrows when a water barrel is left near the wall. Gideon moves the barrel for this test and records its temporary location. The page now describes a route with weather, patching and nearby objects attached, not a universal radius for every cart in Ashfall.""",
    "ashfall_cart_clear_record": """Second road hearing — the goblin left, and the road remains

Rowan returns to the cart after the Ash Goblin has fled from beneath it. The axle is exposed, and no new mark crosses the wheel's cracked section. Gideon asks whether the creature had been trying to steal the iron. Rowan cannot tell. A few loose scraps have moved, but the fight and the earlier salvage work happened in the same small space. He records where the goblin appeared and what remained visible after the encounter, then keeps motive out of the note.

Mira finds a clean path to the medicine parcel and moves it before the repair begins. The cleared area makes the next inspection possible; it does not explain why the creature chose that hiding place. Gideon says the lane feels less threatening now that the cart can move, but he does not ask Rowan to turn that feeling into a report about everyone else's safety. The archive preserves one resolved encounter beside several unanswered questions. Clearing the immediate obstacle lets the group resume their work without pretending the whole road has been understood.""",
    "ashfall_cart_salvage_record": """Second road hearing — keep the iron separate from the inventory

The two salvaged pieces are placed beside Tomas's bench after the axle pin is installed. One length has a bright edge where the smith cut it; the other still carries soot from the old cart. Gideon asks if both should be entered as replacement parts. Tomas says only the fitted pin has been tried under the wheel. The remaining length has not passed a matching check, and the old spoke was used as a gauge rather than installed as timber.

Rowan makes three labels: fitted pin, untested iron and measuring spoke. The labels look fussy until a volunteer reaches for the wrong length to repair a handcart. Tomas shows them the difference and lets the volunteer decide whether to keep the material for a later job. No one marks the untested iron as wasted, but no one promises it will fit another axle. Salvage can remain useful without being counted as a functioning part. Gideon keeps the box at the workshop, where another repairer can ask before taking anything.""",
    "ashfall_cart_measure_record": """Second road hearing — the turning line needs its load condition

Rowan repeats the turning test with a cloth bundle weighing roughly as much as the medicine crate. The outer wheel reaches farther than it did with the empty frame. A heavier load shifts the cart's balance before the handle reaches the painted stone. Gideon remembers that the old cart once turned in the lane while full of firewood, but he cannot remember which bundles were aboard or how the ground had dried.

They draw two arcs: one from the empty trial and one from the light parcel. The second line is not a prediction for a full cart. Tomas asks that the card state the load and surface beside each mark, since a future worker could otherwise mistake the pair for an allowance. Gideon wants one easy circle that anyone can follow; Rowan explains that a circle without conditions would hide the part they actually learned. They keep the test simple enough to repeat and leave the larger-load question open for a day when the road crew can choose to try it safely.""",
    "ashfall_cart_tomas_record": """Second road hearing — the shoulder is a stop, not decoration

Tomas lays the axle pin against the wheel and lets Rowan feel the raised shoulder with one finger. The shoulder prevents the pin from sliding inward when the wheel turns, while the outside end remains accessible for inspection. A hurried repair could make the rod look secure from the front and still leave it free to travel through the hub. Tomas draws the section twice because the first sketch hid the lip beneath the iron ring.

Gideon asks whether the shape can be copied for a different cart. Tomas says the drawing gives another smith a place to start, but the hub width, wood condition and load must be checked first. He writes down the material and the dimensions of this pin, then leaves blank space for any later replacement. Rowan understands why Tomas avoids calling the sketch a pattern. The part's safety comes from its fit and its inspection, not from being named after the person who made it. Gideon adds the date he received the pin so its custody can be followed without implying that he owns every future repair.""",
    "ashfall_cart_spokes_record": """Second road hearing — a gauge can fail in a useful way

The straight spoke rests across the wheel rim while Tomas checks the gap at three points. At the top, it touches both edges. Near the lower nail, a warped section leaves a thin line of daylight. Rowan had first thought the spoke was straight enough to use as a replacement; Tomas asks him to turn it end for end and repeat the comparison. The gap changes sides, revealing a bend too slight to notice by eye.

Gideon keeps the spoke on the bench rather than throwing it away. It still shows where the rim narrows, provided the card mentions its bend and the direction used during measurement. They do not use it to support the cart. Mira says the test gave them a better question for the next board, not a perfect measuring tool. Rowan records the result as a rejected part that remains a rough reference. The note will help another worker avoid mistaking a convenient straight edge for a verified standard.""",
    "ashfall_cart_forge_record": """Second road hearing — the forge is not where the trial ends

The pin leaves the forge cool enough to handle, and Tomas checks its shoulder against the drawing. He finds no visible burr, but he does not ask Gideon to install it while the metal is still warm. The cart has been waiting outside; the crew would like to finish before dark. Tomas closes the tongs and says the bench check has one purpose: confirm that the part resembles its dimensions before it meets a wooden hub.

After the pin cools, the shoulder slips into the gauge without scraping. Tomas signs for the forging step only. Rowan adds a separate line for installation, which will be checked under the wheel. The distinction matters because a clean part can still be wrong for a damaged hub. Gideon accepts the delay when Mira offers to carry the medicine parcel by hand. The cart will move later, after the fit is known. No one treats the completed craft action as proof that the vehicle is ready for the road.""",
    "ashfall_cart_return_record": """Second road hearing — return the sample before lending the tool

Gideon brings the measuring spoke back to Tomas after the turn test. A strip of chalk on the wood shows which edge was placed against the rim, so Tomas can repeat the check without guessing. He wipes the mark away only after Rowan copies its orientation into the ledger. The spoken explanation would probably survive between the two of them; the note is for the next repairer, who may arrive after both have left.

Mira asks whether she can borrow the gauge for the shelter cart. Tomas agrees, then writes down when it leaves the bench and leaves an empty line for its return. He does not ask her to provide a reason or a household name. The tool is useful because it travels, but its measurement is only as clear as the conditions carried with it. Rowan adds that the spoke remains a reference and must not be installed. The handoff gives Mira access without erasing Tomas's responsibility to explain what the instrument can and cannot show.""",
    "ashfall_cart_install_record": """Second road hearing — installation leaves the old hole visible

Once the pin is fitted, Tomas shines a small lantern through the hub to inspect its path. The new shoulder rests outside the iron ring, while a dark stain marks the older place where the wood was split. Gideon wants a fresh coat of paint to make the repair look finished. Mira asks them to wait until the wheel has turned through its hand test; paint could cover a new scrape before anyone notices it.

They rotate the empty wheel slowly. The pin stays in place, and the ring does not catch. Rowan marks the test complete beside the date, then adds a reminder to inspect the same point after the cart travels over the repaired lane. Gideon decides to leave the old hole visible under a clear coat. It helps distinguish the new fitting from the damage that came before. A repair can be neat without hiding its history, and a visible mark can guide future inspection without being treated as evidence of who caused the break.""",
    "ashfall_cart_test_record": """Second road hearing — the empty run has a clear boundary

The first full turn takes place on a dry, flat stretch. Rowan walks beside the right wheel and calls out when the iron ring passes the painted line. The cart rolls without wobbling, but the test stops before the lane's shallow rut. Gideon says it felt steady. Tomas writes that the wheel remained aligned during one empty run on level ground, which is more precise and less impressive than declaring the repair complete under every condition.

They place a low cone at the end of the trial so no one mistakes the boundary for a marker to cross. Mira asks that the medicine stay off the cart until the next test, since she wants a separate note for a carried load. The crew can now decide whether to repeat the run or wait for a second pair of hands. No one is required to volunteer for the next attempt. Rowan records the people who agreed to assist but leaves the public copy without names. The lane is ready for another chosen trial, not yet cleared for every kind of trip.""",
    "ashfall_cart_load_record": """Second road hearing — a knot is part of the route

Mira asks a neighbor who has never tied a cart parcel to try the cloth knot from the illustrated card. The neighbor places the jar near the outer rail, where it knocks against a spoke when the cart starts. They stop before the glass breaks. Rowan moves the strap inward and lets the neighbor try again without taking over the work. This time, the jar stays still through the small turn.

The card gains a picture of the knot from the hand that made it, with a note that the parcel should sit inside the wheel line. Mira asks whether the neighbor wants their name shown. They decline, so the public record says only that a first-time user found the drawing unclear. The change improves the instruction without making a person into an example against their wishes. Gideon suggests adding a second knot for heavier cargo. Tomas says that would need another test with a load chosen by the people who will carry it. They keep the current card narrow enough to remain true.""",
    "ashfall_cart_policy_record": """Second road hearing — a shared cart and a home kit solve different waits

The village holds a short meeting at the bay. One household prefers a cart they can borrow without buying a replacement wheel; another already has a small handcart and would rather keep a pin and gauge at home. Gideon lays out both proposals without asking either family to defend its budget. The shared option needs a visible return time and room to turn. The household option needs clear instructions and a way to request help when the repair exceeds a person's tools.

Rowan writes the practical obligations beside each choice, not above it as a ranking. A cart schedule can fail if nobody wants the next shift; a kit can sit unused if its parts are difficult to identify. Mira offers to keep the drawing at the medicine table, where people may read it without taking a kit. Gideon agrees that the next arrangement should be reviewed after it has been used. The choice flag records what Rowan helped organize today. It does not decide which method every Ashfall household must prefer.""",
    "ashfall_cart_communal_bay_record": """Second road hearing — keep the turning space empty for a reason

The bay stays clear for most of the morning, then a sack of kindling appears beside the wall. Its owner set it there to keep the doorway open and did not know the cart needed a wider turn. Gideon moves the sack with permission and asks whether another storage spot is available. The owner chooses one near the shelter steps. They make the change together rather than writing the name on a warning card.

Rowan measures the empty arc once more, this time with the new stack of crates near the lane. The cart still turns, but its handle passes close to the wall. They shift the crates half a pace and draw a chalk boundary that can be rubbed away if the bay changes. A permanent painted box would look official even after the route changed. The shared space works today because neighbors can ask about stored objects and move them by agreement. The ledger records the clearance and the conditions around it, not a claim that the village has reserved this ground forever.""",
    "ashfall_cart_communal_turn_record": """Second road hearing — count the turns that stop early

The cart makes one complete turn before lunch. On the second attempt, a loose stone rolls beneath the outer wheel and Gideon stops before the handle reaches the chalk arc. Rowan asks whether to record that as a failed turn. Tomas says it is a stop caused by the surface; it is useful to keep because future users should know why the trial ended. They remove the stone and do not repeat the attempt until someone checks the wheel again.

The report now includes one completed turn and one interrupted run, with different marks beside them. The difference prevents a neat total from hiding the caution that changed the work. A visitor offers to smooth the whole lane, but the group has not agreed on how much ground belongs to the bay. Gideon thanks them and asks for a smaller patch near the wheel track instead. The shared cart remains available under the posted conditions. The space for an early stop stays part of the instructions, because safety work is also the ability to end a trial before a small warning becomes a larger repair.""",
    "ashfall_cart_communal_report_record": """Second road hearing — the return board records an object, not a person

The first cart user writes “back at the bay” on the slate and wipes the chalk away after unloading. Another resident asks whether the schedule should include the borrower's name so the next user can ask questions. Gideon says the cart can carry a contact token if someone volunteers to be reached, but a name is not a condition of borrowing. They leave a small blank for a return time and an optional note about the lane.

Mira adds a line for damage or a changed strap. She does not add “reason for trip.” The next person can check the wheel, read the load card and decide whether the cart meets their own needs. Rowan records that the schedule was used twice and does not estimate how many households now depend on it. A shared object needs a reliable handoff, not a census. If the bay becomes inconvenient, its users can request a change. Gideon agrees to ask again after several trips instead of treating the first week as a final policy.""",
    "ashfall_cart_household_kits_record": """Second road hearing — a kit should explain what is missing

The repair kits arrive with one shoulder pin, a measuring card and a cloth envelope for loose fasteners. Mira notices that the first envelope has no label for an empty compartment. A missing piece might mean it was used, lost or never included. She and Tomas add three check boxes on the card and ask each household which format is easier to read. One person wants words; another circles small drawings.

Gideon offers to deliver the kits, but two neighbors prefer to collect theirs when they visit the square. Nobody has to sign for receiving one. The inventory can track how many kits were assembled without naming who took them. Rowan suggests adding an optional way to ask for another pin. Tomas writes the forge location beside it, so the instructions do not promise that a replacement is always on hand. The kit is an invitation to try a small repair, not a transfer of responsibility for every broken cart onto each household. Help remains part of the plan.""",
    "ashfall_cart_household_test_record": """Second road hearing — two stands reveal two different problems

Mira tests a loose wheel on the wooden stand, while Tomas repeats the same hand turn on the iron stand at the forge. The wood frame flexes slightly when the pin is pushed sideways; the iron frame holds still. Neither result means that one stand is useless. The household kit is meant to help someone notice a loose fitting before a cart is loaded, not to imitate every force it may meet on the road.

They add a warning to stop if the stand itself shifts. One household asks to keep the kit near the door; another puts it above a dry shelf. The archive does not choose a storage place for them. Rowan records which stand was used in each trial so a later reader can compare results without treating them as identical. Tomas asks for a road test only if the cart owner agrees and a second person can walk beside the wheel. A repair instruction should make stopping ordinary, not embarrassing.""",
    "ashfall_cart_household_report_record": """Second road hearing — asking for help is part of the kit

Mira finds a note tucked beside the measuring card: “I can fit the pin, but I cannot tell if the hub is splitting.” She recognizes the question as a reason to stop and asks the writer whether it may be copied into the public instructions. The writer agrees without signing their name. Tomas adds a simple check: if a crack continues past the iron ring, do not load the wheel; bring the cart to the forge or ask a repairer to inspect it.

Gideon wants to know which household wrote the note so he can check on them. Mira explains that the cart owner can contact him directly if they want help. The public record can answer the repair question without exposing the person who asked it. Rowan leaves the name field blank and adds the date the instruction changed. The household kit now has a route back to skilled support, rather than a promise that everyone must become their own mechanic. A tool is useful when it also shows where its limits begin.""",
    "ashfall_cart_afterword_record": """Second road hearing — leave a place for the next repairer

At the end of the month, the shared cart has made several short trips and spent one week under cover while a new scrape was inspected. The home kits have been borrowed for two loose pins; one came back with a note asking for a smaller measuring card. Gideon expected the village to settle on one arrangement. Instead, both are still being used in different places, and each has acquired a small revision.

Rowan makes two copies of the archive: one stays with Tomas's workshop, the other with the bay schedule. They include the conditions of the trials, the names of those who chose to sign, and blank space for someone to disagree or add a date. Mira says a record should be easy to correct before it becomes a rule. Gideon puts the cart key back on its hook without locking the shed. The road remains open for another journey, but nobody claims that a repaired wheel can promise the future will be smooth. The next repairer will have a place to begin and permission to change the page.""",
}


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in catalog["entries"]}
    missing = sorted(set(SCENES) - entries.keys())
    if missing:
        raise SystemExit("Missing route codex records: " + ", ".join(missing))
    already_expanded = [record_id for record_id in SCENES if MARKER in entries[record_id]["body"]]
    if already_expanded:
        raise SystemExit("Second hearing already exists: " + ", ".join(already_expanded))

    before = sum(len(body.split()) for entry in catalog["entries"] for body in [entry.get("body", "")])
    for record_id, scene in SCENES.items():
        entries[record_id]["body"] = entries[record_id]["body"].rstrip() + "\n\n" + scene
    after = sum(len(entry.get("body", "").split()) for entry in catalog["entries"])
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Appended {len(SCENES)} Ashfall cart second-hearing scenes ({after - before:,} raw words).")


if __name__ == "__main__":
    main()
