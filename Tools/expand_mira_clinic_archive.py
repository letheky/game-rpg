#!/usr/bin/env python3
"""Add first-person and material-history notes to Mira Cole's Ashfall route records."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental room note —"

NOTES = {
    "mira_ash_house_open_record": """Supplemental room note — the first step back inside

Mira waits at the threshold until Rowan has finished moving the fallen herb jars. She remembers the room by the way it smelled when the old kettle was warm: dried mint, damp brick and the bitter trace of ash from the garden. The memory brings back the small sounds of apprenticeship, too — a chair leg scraping, a patient pausing before answering, her mentor setting a tool down instead of reaching across the table. The room had been quiet without being secret. That difference is the reason she wants it back.

The first walk through is not a promise to restore everything. Mira points out the cracked hearth, the loose cot hinge and the gap around the back door, then asks Rowan to help her make one safe change at a time. She has no list of everyone who once received care here and does not invent one to make the room feel full. Today it is empty. Tomorrow someone may choose to enter, and that choice is enough reason to clear the floor.""",
    "mira_ash_house_hearth_record": """Supplemental room note — heat without a hearth

The old hearth is cold, but the stone around it still carries soot in the fine cuts between blocks. Mira remembers how quickly a small crack can travel when a fire is lit against it. She does not want warmth to become the first thing the room offers if the wall cannot yet hold it. The alchemy table can heat water separately, under supervision, while the stone is examined. It is a temporary arrangement with a clear end: the hearth will stay unused until its seam is repaired.

When Rowan asks whether the workaround feels like giving up on the room, Mira says the opposite. A room can be useful before it is finished if its limits are visible. She writes the cold hearth on a card and hangs it where another worker will see it. No one should have to remember which part of the room is safe from a half-finished repair. The card is removed only after the masonry is checked again.""",
    "mira_ash_house_cot_record": """Supplemental room note — the view from the cot

Mira lies on the cot for a moment after Rowan braces its legs. From there the door is visible, the window gives a strip of pale light, and the shelf holding jars is not within easy reach. She asks Rowan not to place supplies above the resting space; a person should not have to trust a loose shelf while trying to sleep. The cot has one pillow and no strap. The room is for rest, not for keeping anyone in place.

Her mentor used to move the cot each morning to catch the sun, but Mira has never liked waking someone just to follow a rule about where a bed belongs. She will ask the next visitor whether the light or the shade is easier. For now, the cot can be moved by one person without blocking the door. Its hinge gets another chalk mark for later inspection, a practical reminder that a repaired frame still needs attention.""",
    "mira_ash_house_yard_warg_record": """Supplemental room note — the route the warg occupied

The Ash Warg chose the narrow space under the broken sill, where the wall gave it cover and the garden paths met. Mira used to cross there to collect drying cloths. Since the raid she had been sending people around the crowded front of the herb table, even when a short walk through the yard would have been easier. The detour made her feel that the room had become a trap for anyone who needed help getting in or out.

Rowan's fight clears the path, but it does not repair the sill or prove that no other creature will return. Mira asks for the yard to be checked before each shift until the wall is fixed. She knows a guard cannot be stationed at every door in Ashfall. A clear route is a useful beginning; a reliable room also needs someone to notice when the route has changed. The chalk line on the stones marks where the next inspection should start.""",
    "mira_ash_house_seed_pocket_record": """Supplemental room note — a packet outside the store

The packet of Emberlily seeds was hidden close enough to the old room that Mira wonders whether her mentor put it there. She cannot say so with certainty. The label carries a plant name and a season, but no signature. In the training days, seed was often divided into small envelopes and left where a student could find it when the garden needed attention. Those packets were not an official reserve, and Mira does not want this one counted as if the whole village had agreed to lend it.

She chooses a tiny trial bed because it can be watched from the open door. If the seeds fail, the loss stays small and the packet can be kept as a record of what did not grow. Rowan is asked to write down the position of the bed and the condition of the soil rather than guess at the faded directions. The first responsibility of the new garden is to leave a better note for the next pair of hands.""",
    "mira_ash_house_first_bed_record": """Supplemental room note — the strip that stayed cool

The first Emberlily bed fits between the brick lip and the garden wall. Its ash layer is shallow enough for the roots to reach packed earth, and the wall keeps the soil cool after midday. Mira checks the bed at different times rather than treating one morning inspection as a description of the whole day. The plant is small, but the red center can be seen from inside the room when the door stands open.

She asks Rowan to leave the weakest stem alone. The trial is not a contest for the largest harvest. Mira wants to learn whether the bed can renew itself before she relies on it for a recipe. A flower left standing may produce seed, or it may not; the season will decide. The garden card therefore has two boxes, one for the petals used now and one for what remains at the end of the week. The second box is allowed to stay blank.""",
    "mira_ash_house_first_bloom_record": """Supplemental room note — a petal left on the cloth

Mira lays the Emberlily petals on cloth and waits until the cup has cooled enough to handle. She does not hurry them toward the mortar. Her mentor used to say that a careful harvest begins when the person collecting it notices what will be left behind. Mira had thought the phrase was about thrift. Now she sees that it is also about not turning a living bed into a shelf of supplies just because a room has reopened.

One petal falls beside the drying cloth and is kept separate. It has a torn edge and is not used in the trial batch. Rowan records the reason instead of writing only the final count. A later healer can tell that the smaller amount was a deliberate choice, not a missing ingredient. The note gives the recipe a place in the garden's history: this first balm came from a cautious harvest, not from stripping every flower the bed could offer.""",
    "mira_ash_house_moonwort_record": """Supplemental room note — leaves for washing

The Moonwort leaf is set aside for the wash cloth before the balm is made. Mira knows the plant from training, but she does not treat that familiarity as proof that every leaf is clean. Rowan rinses the sound one with water from the covered bowl, and Mira checks it for grit before it touches the cloth. The rest of the plant stays rooted. Its next growth is more useful than one larger harvest that leaves the bed bare.

The wash basin sits beside the cot, so a person resting there can see how it is prepared. Mira wants the work to be visible enough for a guest to ask questions, while keeping the guest's own story private. She writes the plant's name and use on the garden card, not on a patient record. Moonwort helps them prepare this room's materials; it does not make water plentiful or turn a leaf into a substitute for clean water.""",
    "mira_ash_house_brook_trout_record": """Supplemental room note — the bowl brought from the brook

Mira cooks the Blackreed Trout in the open kitchen rather than at the damaged hearth. The fish is a meal for a person who has chosen to rest, not an ingredient in the balm. The distinction sounds obvious until people start adding every helpful thing to one supply list. A bowl of food belongs in a kitchen record; a medicine jar belongs on a shelf with its ingredients and limits written down.

The upstream bend looks clear today, but the brook carried ash after the raid. Mira will not use one bright stretch of water to certify the whole stream. Rowan marks where he fished and the direction of the current. They have one catch, one meal and one afternoon's observation. Mira tastes the broth before it is offered and asks the guest whether warm food would be welcome. No one is required to eat because the fish was difficult to catch.""",
    "mira_ash_house_mortar_record": """Supplemental room note — why the mortar stayed in the drawer

Mira takes the mortar from the drawer and notices that she has been holding its base too tightly. The chipped edge is not the reason she put it away. During training she once rushed a practice mixture, read the mentor's brief instruction as permission to finish alone, and had the batch stopped before anyone used it. No one was harmed, but Mira carried the shame as if the room itself had rejected her. The mortar became easier to hide than the memory of needing correction.

She checks the inner surface with a clean cloth, then lays another folded cloth beneath the bowl so it cannot rock on the table. The repair is ordinary and visible. Mira tells Rowan that a tool can be safe to use while still reminding its owner of a mistake. The room does not ask her to forget the lesson; it gives her a way to use the same tool more carefully and to ask for a second opinion before a batch is offered.""",
    "mira_ash_house_first_balm_record": """Supplemental room note — the first two portions

Mira keeps the first balm batch deliberately small. She checks the Emberlily petal and Moonwort leaf against the written recipe, grinds them with the cloth beneath the mortar, and refuses Rowan's suggestion to use the cracked hearth to speed the work. The formula is an in-game treatment for a minor burn or split. Its limits are part of the label: it cannot settle a deep wound or replace a healer's examination. The game item restores a small amount of health, but that number is a combat rule, not a claim about every injury.

Two jars come from the batch. Mira asks that the first be offered to a visitor only after they hear what it is and what it is not. The second stays with Rowan so he can use the item during travel if he chooses. Neither jar is treated as proof that the garden can meet every future need. This first preparation shows that the old recipe can be followed in a safer workspace, not that Mira has solved medicine for Ashfall.""",
    "mira_ash_house_first_jar_record": """Supplemental room note — the label faces outward

The jar's label faces the person who might use it rather than the healer who stored it. Mira adds the batch date, the two plant names and a brief description of the balm's intended use. She leaves enough room to write a correction if the contents change or the jar is set aside. A neat label is not permission to apply something to another person's skin; the jar still has to be offered and explained.

The room's old shelves were arranged so that the healer could reach everything from the work surface. Mira changes that arrangement. Jars are grouped by use, and the label faces outward so the person receiving care can read along. Rowan notices that she has not written the guest's name anywhere. Mira says the recipe needs its own history; the guest does not have to become part of it. If the balm causes discomfort, the offer ends and the jar goes back to the shelf.""",
    "mira_ash_house_policy_choice_record": """Supplemental room note — choosing where the weight belongs

The fixed clinic places more weight on the room: shelves, a cot, a basin and supplies kept together. The field kit places more weight on Mira: a satchel on her shoulder, a route across broken streets and fewer jars to offer when she arrives. Rowan's choice decides which arrangement is prepared first. Mira does not ask him to choose the one that will always be best; she asks which limitation Ashfall can manage today.

She describes the fixed room as a promise to stay within reach of the village, then immediately adds that staying in one place can leave the road unattended. The kit can travel, but travel spends time and supplies and may separate the healer from the people who know the town. The record keeps both costs on the same page. A policy is useful when it says who carries the weight and where the missing help might be. The patient's ability to accept or decline care applies under either arrangement.""",
    "mira_ash_house_clinic_wall_record": """Supplemental room note — morning through a narrow window

The window is narrow, but morning light reaches the cot without landing directly on the shelf of jars. Mira tries it at two different heights before leaving the frame as it is. The room once had heavier curtains; the remaining hooks are uneven, and she does not want to hang cloth that could block the exit path. For now, the window gives a patient a view of the garden and lets the healer see the red Emberlily flower from inside.

Mira keeps the glass partly shaded from the lane. The person resting can see out, while a passerby cannot easily see the cot. She is not trying to hide that the clinic exists. She is making a small distinction between finding help and being displayed while receiving it. Rowan marks the safe opening angle on the frame. If the stone shifts, the window should be checked again before it is used at full width.""",
    "mira_ash_house_clinic_latch_record": """Supplemental room note — the test from inside

Mira closes the door, sits on the cot and works the latch with one hand. The lever opens without catching her sleeve, and the door swings clear of the basin. She repeats the movement slowly, then asks Rowan to try it from outside without pulling on the frame. Neither test proves that the repair will last through every season, so the hinge is added to the monthly inspection card.

Her mentor's old rule was short: a patient must not need a keeper to leave. Mira had treated it as a principle she already understood, until the first time she found herself standing between a frightened visitor and the door because she wanted to finish explaining. Now she has arranged the room so the latch and exit are visible before anyone sits down. The door can still be closed against a gust. It cannot be used as a lock.""",
    "mira_ash_house_clinic_basin_record": """Supplemental room note — carrying water without crossing the room

The basin fits beside the cot, but the first placement makes the refill path cross the visitor's feet. Mira moves it closer to the wall and tries carrying a covered bowl from the water station with one hand. There is enough room to pass without brushing the cot. Rowan marks the floor where the basin should stand after the room is cleaned, then wipes the chalk away so it will not become a permanent boundary.

The route is designed for one caregiver and one guest, not a crowd. If a second healer is needed, the stool can move and the door can remain open. Mira likes being able to see the exit from the work surface; the person on the cot can see it too. The placement does not prove that every visitor will find the room comfortable. It makes a few choices visible and leaves enough space to move furniture when the next visitor asks for a different arrangement.""",
    "mira_ash_house_clinic_choice_record": """Supplemental room note — a fixed place, with a return path

Mira chooses the clinic because the room lets her keep the basin, cot and herb shelf within a few steps of one another. After the raid, she has spent too much time moving supplies from one place to another and too little time hearing what people actually ask for. A stable work surface helps her prepare the balm carefully and rest between visits. It is a choice about how she wants to practice, not an order that every injured traveler must come to her door.

She makes a small traveling pouch for the road even though the fixed room is the main plan. The pouch carries less and has to be restocked from the clinic, but it preserves a way to reach someone who cannot walk to Ashfall. Rowan's help has made a room available; it has not made every road passable. Mira writes the clinic's hours on the sign and leaves one contact bell within reach of the cot. A fixed address can be dependable without pretending to be everywhere.""",
    "mira_ash_house_clinic_sign_record": """Supplemental room note — the sign's missing promise

Mira hangs the red-leaf sign high enough to be found from the path, then asks Rowan to stand at the far gate and read it. The words are plain. They name the clinic and state when Mira expects to be present. She declines to add “all care, all hours,” because the room has one healer and a limited supply. A sign that promises more than the clinic can provide could turn a difficult absence into a betrayal.

The leaf mark comes from the plant that supplied the first balm. It lets a traveler find the door without asking someone in the busy square to explain why they came. Mira leaves no list of patients or illnesses on the wall. The clinic can be visible while the person who enters remains private. When the sign is not current, Mira wants the hours crossed out and rewritten rather than left to fade into a statement that used to be true.""",
    "mira_ash_house_kit_straps_record": """Supplemental room note — the satchel during a long walk

Mira loads the satchel with jars, cloth and a lantern, then walks the lane twice before deciding where the straps should cross. The older bag used to swing forward when she knelt; its buckle caught her sleeve at exactly the moment she needed both hands. This one sits close to her back and opens from the side. Rowan watches her squat, rise and lift the lantern without loosening the straps.

The bag still has a limit. Mira removes one spare jar when the weight presses too hard on her shoulder and writes that choice on the packing card. A traveling healer who carries everything may arrive too tired to help. She does not want the satchel to look like a heroic burden. It is equipment that should be rearranged when the carrier's body says the load is wrong. The person wearing it decides what is comfortable enough to take onto the road.""",
    "mira_ash_house_kit_roll_record": """Supplemental room note — a pocket for each small thing

The waxed cloth roll has separate folds for jars and clean cloth. Mira ties each pocket with a different knot she can recognize in low light. She leaves one fold empty, not because it is waiting for a particular medicine but because an unexpected request should not require unpacking the whole satchel. Rowan asks whether the empty pocket makes the kit incomplete. Mira says an empty place can be part of a plan if it is labeled honestly.

Dust stays off the lids, and the roll can be removed from the satchel for a quick inventory. Mira writes a short list inside the fold rather than on the outside, where a passerby could read it. The kit identifies a healer's work, not the conditions of the people she has visited. At the end of each journey, the jars return to the herb table and are counted again. No one should discover that a supply is missing only when someone asks for it.""",
    "mira_ash_house_kit_map_record": """Supplemental room note — the route wide enough for a stretcher

The eastern path is shorter on the map, but a fallen lintel narrows it until two people cannot walk side by side. The southern gate adds several minutes and gives enough width for a stretcher or two helpers carrying a heavy load. Mira circles the wider route, then draws a second line to the east road in case the southern gate is blocked. The map is a working copy, not a guarantee that either path will stay open after rain or debris.

She asks Rowan to walk the route with the satchel and return by the same way. The time is written beside the weather and the condition of the gate. Mira does not want a single travel estimate turned into a rule for everyone; a person who moves more slowly may need another path or a pause. The note helps her prepare. It does not tell the person receiving help how quickly they must be found.""",
    "mira_ash_house_kit_choice_record": """Supplemental room note — meeting people where they already are

Mira chooses the field kit because some people resting on the road will not be able to cross town to reach the clinic. She remembers how the village square filled after the raid and how a person could be surrounded by help and still have no clear route out. A mobile offer gives her a way to meet someone at a quieter place. It also means every supply has to travel with her and every trip requires a return for refills.

She does not call the kit freedom from the clinic. The satchel depends on the herb table for clean cloth, a work surface and replenishment. She plans to return after each route and leave the bag with Mira's own notes, not with a list of who accepted care. The choice lets her carry help outward while keeping a stable point where materials can be checked. If the road becomes unsafe, she can pause the trip; the choice does not demand that she go everywhere.""",
    "mira_ash_house_kit_mark_record": """Supplemental room note — the leaf beside the buckle

The Emberlily mark sits next to the satchel's buckle, where another healer can recognize it without opening the bag. Mira chooses a leaf instead of a name. The satchel belongs to the treatment work and can be returned if its carrier cannot finish a route. It does not belong to the people who ask for help, and no one should read the mark as proof that its owner has authority over them.

The red thread is bright enough to find in a dim room. Mira tests that by turning the satchel over and asking Rowan to point to its opening without touching the straps. He finds it quickly. A clear mark saves time during a handoff, while the blank inside pocket keeps private notes out of view. When the kit returns, the next healer can check the seals and supply card. The plant symbol tells them what tool they found; it does not tell them whose story to ask for.""",
    "mira_ash_house_first_shift_record": """Supplemental room note — how the first offer begins

Mira begins each conversation with a question rather than a direction. “How would you like me to help?” leaves room for someone to describe a need she had not anticipated, ask only for a place to sit, or say that they want to be left alone. She listens before taking a jar from the shelf. Rowan sees that the room's first shift is not a test of how quickly the healer can use her supplies.

The record counts two people who visited, but does not list their names, injuries or choices. Mira will not turn the shift into proof that the clinic model works for everyone. One visitor used the cot; another only asked where the southern gate led. Both had a reason to enter, and neither has to become a case study. The supply total is written on one page and the visitors' private words stay outside the archive. The next shift begins from the same question.""",
    "mira_ash_house_mentor_token_record": """Supplemental room note — a button turned in the hand

The button from Mira's training years is brass with a small pressed leaf. Its edge is smooth where her mentor's thumb turned it during long pauses. Mira had once mistaken those pauses for uncertainty. Later she learned that her mentor was giving a patient time to find their own words. The button brings back that lesson more clearly than any of the old written instructions in the drawer.

Mira keeps it beside the mortar rather than wearing it as a badge. She is not her mentor, and the button does not certify her skill. Its place at the work surface reminds her to stop before reaching for the next tool. Rowan notices that she turns it once when a visitor declines the balm. She puts it down, listens, and asks whether the person wants anything else. The object has not changed; the way Mira uses the pause has.""",
    "mira_ash_house_mentor_lesson_record": """Supplemental room note — knowledge held on both sides

Mira's first mentor asked a student to hear a patient's description before proposing a remedy. At the time, Mira thought the sequence was inefficient. She wanted to show that she had learned the names of plants and could prepare a jar without help. Her mentor pointed out that a healer knows the limits of a remedy, while the person receiving care knows what they feel and what they are willing to try. A sound choice needs both kinds of knowledge.

The lesson had been written on a card, but the card is gone. Mira reconstructs it in her own words and leaves a space for someone to disagree. She says she can still ask the wrong question or misunderstand an answer. What matters is whether she leaves room to correct herself. Rowan watches her rewrite “patient report” as “what the visitor chose to tell us.” The new wording is longer because it admits that the archive does not own the other person's account.""",
    "mira_ash_house_second_seed_record": """Supplemental room note — returning seed to the bed

Mira divides a few Emberlily seeds from the flower left at the first harvest. She keeps one packet for the room and gives another to the neighbor who lent the original seed. The note calls the first seed a loan and the second a return; neither is entered into the village reserve. A small garden can keep its own promise without becoming a strategic store.

The neighbor has not promised to keep growing the plant, and Mira does not ask them to. The seed can be planted, shared again or kept through the winter according to the owner's choice. Rowan labels both packets by source and date, leaving the expected harvest field blank. A new season is possible, not guaranteed. Mira likes that the bed carries something forward, but she refuses to write “future supply” where only a handful of seeds have been counted.""",
    "mira_ash_house_second_bed_record": """Supplemental room note — a harvest that leaves a flower

The second bed produces enough petals for another pair of balm portions while one mature flower remains on the plant. Mira chose the harvest line after comparing the stems, not because she expected a fixed yield. If the flower fails to seed, the garden will need another packet. If it succeeds, the next person who tends the bed can decide whether to plant or share. Rowan marks the living flower with a short stake so no one mistakes it for an unharvested accident.

The clinic uses what it needs and leaves the rest outside the jar count. Mira has seen a useful plant disappear when every bloom became inventory. This time the garden continues to belong to the season as well as to the room. She writes down the number of petals used and the number left, then folds the card so rain will not wash either line away.""",
    "mira_ash_house_garden_shade_record": """Supplemental room note — the cloth shade moves at noon

The shade cloth was hung according to her mentor's old sketch, but the wall now blocks afternoon light differently. At noon, the cloth covers the Emberlily's open center while the eastern edge of the bed grows hot. Mira slides the cloth one brick back. Rowan makes a temporary mark on the wall, then checks the flower again after the shade moves with the sun.

The garden plan is not a rule that can be copied without looking at the site. Mira had once believed that respecting a teacher meant repeating every arrangement exactly. She now thinks it can mean keeping the purpose — protecting a flowering plant from excess heat — while changing the method to suit the room they have. The mark is dated and can be erased. If the wall, season or plant changes, the next gardener should test the shade again rather than follow the old line by habit.""",
    "mira_ash_house_second_balm_record": """Supplemental room note — comparing the second batch

The second Emberlily opened in warmer air than the first. Its scent is stronger, but Mira does not change the recipe by guesswork. She prepares the same small batch and writes down the harvest time, the petal condition and the Moonwort leaf used. A different smell may be worth noticing; it is not by itself proof that the balm is stronger or safer.

The bowl remains covered with clean cloth while the mixture binds. Rowan offers to label the jars, and Mira asks him to copy the source plants before writing the intended use. This order keeps the name of a remedy from hiding where it came from. Two portions are made again. One will be offered during the evening service; the other stays available for the player's inventory. The preparation record describes this batch only, so a future healer can compare without treating either one as a universal standard.""",
    "mira_ash_house_cooling_cloth_record": """Supplemental room note — when the lid goes on

Mira leaves the second jar uncovered until its rim feels dry. She does not seal warmth and moisture inside just to make the shelf look tidy. The removable tag carries the date, the ingredients and the phrase “check before use.” She deliberately leaves out an expiry claim she cannot support. A later healer can inspect the jar and decide whether it is still suitable, or discard it if anything has changed.

The old cabinet had a permanent label nailed to each shelf. Mira replaces those labels with cards that can be changed when the stock changes. A fixed inscription can make an empty shelf look as if a supply ought to be there. The new cards show the amount actually present and the day it was checked. Rowan copies that practice onto the field kit's packing sheet. The goal is not a perfect archive; it is to make the next decision possible without pretending someone already made it.""",
    "mira_ash_house_night_service_record": """Supplemental room note — an offer after the lamps are lit

The evening visitor does not ask for the balm at first. Mira explains what is in the jar, describes the small kind of injury it is meant for and points out the label. She asks whether they want a portion. The visitor accepts, then asks if it can wait until morning. Mira agrees and leaves the jar within reach, unopened. The next choice remains theirs.

One portion is still available from the second batch, and Mira writes that amount on the shelf card. She does not write who took the first offer or what they applied it to. Rowan sees how easily a care record could become a story about the healer's success instead of the visitor's decision. The evening shift closes with supplies counted and no claim that everyone who entered was treated. Mira stays by the door until the visitor has chosen whether to leave now or rest a little longer.""",
    "mira_ash_house_well_imp_record": """Supplemental room note — the wash passage after the fight

The Ash Well Imp had been tipping the basin and scattering grit into the passage. Rowan drives it away, but Mira checks the floor before carrying clean water through. The fight left new dust along the drain, while the older cracks remain where they were. She sweeps from the cot toward the doorway so the path stays clear rather than pushing debris back under the bed.

The encounter explains the fresh claw marks; it does not explain why the older stone shifted or whether the drain has a deeper problem. Mira puts a temporary cover over the basin when no one is using it. The room can reopen for the evening because the immediate path is clear, but she adds the passage to each shift's opening check. A healer should not have to spend the first part of every visit discovering that a creature has moved into the same corner again.""",
    "mira_ash_house_well_lip_record": """Supplemental room note — separating new scratches from old seams

The small claws left marks from the drain outward. The older cracks run along the brick seam and do not have the same shape. Rowan sketches each pattern on a separate corner of the inspection card, while Mira keeps grit from falling back into the basin. The sketch helps a mason see what was present after the imp was driven away. It cannot show how the damage began before anyone looked closely.

Mira had once tried to explain the whole room's wear with a single cause because a simple answer seemed easier to repair. Now she prefers to leave two questions open: what did the imp do, and what had the closed room been doing to itself over time? The drain is clear for the moment. The next heavy rain may reveal something different, so the inspection card carries a date and a line for later comparison rather than a final verdict.""",
    "mira_ash_house_mira_boundary_record": """Supplemental room note — when an offer ends

Mira says that an offer of care has to stop being an offer the moment the other person says no. Her first instinct used to be to list every reason a treatment might help. She thought persistence would show that she cared. Her mentor told her that the patient should not need to win an argument to refuse. Mira still finds the silence after a refusal difficult, especially when she believes she has prepared something useful.

The room's arrangement now supports the boundary: the door opens from inside, the bell can be reached from the cot and the jar is not already in someone's hands. Mira can stay nearby if asked, or step away if that is what the visitor wants. She writes the principle on a small card for herself rather than posting it as a rule over patients. Rowan sees her put the card beside the button from her mentor. It is a reminder to practice, not a claim that she will never get it wrong.""",
    "mira_ash_house_mentor_thread_record": """Supplemental room note — mending the curtain without keeping the apron

The old apron cloth tears when Mira tries to sew the button back into it. She stops, folds the brittle piece and stores it separately instead of cutting it into strips for the room. The thread of its history matters to her even if the fabric can no longer be used. A new curtain receives the button with dark thread, and the original apron stays in the drawer as something she does not have to turn into equipment.

Mira chooses a place near the doorway where the button can be seen when the curtain is drawn. It marks a pause before entering, not ownership of the person inside. Rowan asks whether the curtain is meant to block every sound. Mira says no: it softens the view while leaving the hand bell and open exit available. The cloth can be moved aside at the visitor's request. A piece of training follows Mira into the room, but it does not get to decide how the room is used.""",
    "mira_ash_house_quiet_bell_record": """Supplemental room note — a signal small enough to choose

The hand bell sits on a low hook beside the cot. Mira tests it from the stool and hears one clear tap at the herb table. From the street, the sound disappears under the wind. She does not want a patient to have to shout through an open door to get her attention, and she does not want a private need broadcast across the square. The bell offers one small way to call, but no one is required to use it.

The visitor can move the bell closer, leave it alone or ask Mira to take it down. Rowan writes the location on the room plan, not on a record of who rang. If the bell is out of reach for a particular person, the arrangement needs to change. Mira keeps the cord long enough to move and short enough not to tangle around the cot. It is a tool for communication, not a signal that the healer owns the room's next response.""",
    "mira_ash_house_door_sign_record": """Supplemental room note — a mark visible from the path

The red-leaf sign is tested from the gate at dusk and again in the morning. It can be seen without showing the cot through the window. A passerby can identify where help may be offered without learning who has entered or why. Mira keeps the wording spare. A sign that lists conditions or expected patients would turn the entrance into a public record of private needs.

In the fixed-clinic route, the sign points toward the open room and its posted hours. In the field-kit route, the same mark tells a traveler where Mira can be found between journeys. It is not a promise that she is present at every moment. Rowan makes a small space for Mira to change the time card when her route changes. The sign helps people find her work; it does not decide whether they should come closer.""",
    "mira_ash_house_bench_record": """Supplemental room note — the stool does not belong to the healer

The stool stands beside the work surface, but Mira asks Rowan to carry it to the other side of the room and try the layout again. A visitor may want to sit near the door, look toward the garden or have no seat at all. The stool is light enough to move without turning every preference into a request for permission. When someone is speaking, the healer can sit too; the room does not require one person to stand as the authority.

Mira remembers her mentor working through long shifts without resting. She once copied that posture as if exhaustion were proof of commitment. The empty stool is a quiet correction to that habit. If Mira sits between visitors, she may be more able to listen through the next conversation. Rowan notes where the stool can be placed without blocking the basin path. The mark is a guide, not a fixed position. The room should be rearranged around the people using it.""",
    "mira_ash_house_afterword_record": """Supplemental room note — a practice that can change

At the end of the first run of shifts, Mira reviews the supply card, the door inspection and her own notes. She does not write a total for “people healed.” That column would turn different needs and private choices into one claim she cannot support. She writes what is available, what was offered, what remains to be checked and when she plans to return. The field kit route adds distance and rest stops; the fixed clinic route adds a posted hour and a room to maintain. Each needs a different daily routine.

Mira leaves the clinic sign and satchel mark in place, but neither becomes permanent law. If the room becomes unsafe or the road changes, she can revise the arrangement. The Emberlily garden may renew its seeds, or it may fail in the next season. Rowan's help gave her a place to begin, not a finished answer about care. The afterword leaves a space for the next healer to disagree with Mira and for the next visitor to choose differently.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing codex entries: {', '.join(missing)}")
    remaining = [key for key in NOTES if MARKER not in entries[key]["body"]]
    if not remaining:
        print("All Mira clinic records already contain their supplemental notes.")
        return
    before = sum(len(entries[key]["body"].split()) for key in NOTES)
    for key, note in NOTES.items():
        if key in remaining:
            entries[key]["body"] += "\n\n" + note
    after = sum(len(entries[key]["body"].split()) for key in NOTES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(remaining)} Mira clinic records; added {after - before} words.")


if __name__ == "__main__":
    main()
