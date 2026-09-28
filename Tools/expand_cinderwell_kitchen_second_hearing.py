#!/usr/bin/env python3
"""Add character-led second-hearing scenes to the Cinderwell kitchen archive."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets/Resources/Content/codex_catalog.json"
MARKER = "\n\nSecond hearing —"

SCENES = {
    "june_stonepot_open_record": """Second hearing — the door is not a question

On the first morning the kitchen opens, June leaves the door unlatched even while she carries the stock book from the pantry. Rowan asks whether anyone might take supplies. June answers that a latch would make every hungry visitor explain why they came before she could explain what the kitchen can offer. She does not call the choice risk-free; she asks Oren to keep the dry shelf in sight while the pot is unattended.

Two people pass the threshold without sitting. One accepts a cup of water, then leaves it rinsed beside the basin. June does not add their initials to the day sheet. She records only the cup returned and the water used. For Rowan, the small entry becomes a lesson in what the ledger can honestly hold: a kitchen can count its own work without claiming to know the lives that touched it. The door stays open through the next shift, but the stock check remains a shared responsibility rather than a test of whether a visitor deserves to enter.""",
    "june_stonepot_hearth_record": """Second hearing — repair work has a stopping line

The mason arrives after the last bowl is washed and asks June to clear the hearth stones. June gives him the portable brazier card first. He studies the charcoal line and says the trial tells him where heat was used, not what the crack looks like beneath the ring. She appreciates the distinction and refuses to let the tired crew hurry him into a verdict before he has lifted a stone.

Rowan carries the cooking pot to the dry platform. Its iron bottom leaves a dark circle on the boards, exactly where June expected it. The mason marks that circle as a work position, not as proof that the platform can bear a full night of cooking. June asks for a second inspection after the lower stair is dry. The room can make small meals in the meantime, provided each shift checks the legs and clears the walking space. Her relief is visible when the fire is moved; her caution remains on the card. The hearth is still a question with a safer temporary answer.""",
    "june_stonepot_pantry_record": """Second hearing — the sack that was opened too late

Oren finds a softened seam at the back of the lower shelf and asks June if she wants him to discard the whole sack. She cuts only the wet corner away and checks the grain that stayed above the damp line. Some is sound enough for a small test; some has begun to clump. They put the portions on separate cloths and write the inspection time beside each one, so another cook can repeat the check instead of trusting the word usable without context.

June remembers a previous kitchen where throwing out one damaged sack had left the next crew with no supper. She also remembers that serving spoiled food would have harmed the people she wanted to protect. She does not tell Rowan that either memory settles today's decision. They keep the tested grain for the current pot and ask Oren to inspect the remaining stock. The Muck's defeat cleared a route to the shelf. It did not certify everything stored behind it. On the work card, June writes the next checker's name only after asking whether that person has agreed to take the task.""",
    "june_stonepot_draft_record": """Second hearing — hear the room when the gate turns

Talia visits during a quiet hour and asks June to repeat the brazier test while the sluice worker turns the lower gate. The flame leans for a moment, then settles. A cart rolls past the opening and changes the draft again. No one is in danger, but the movement is enough to make the old diagram incomplete. June takes it down from the wall and carries it to the tool shelf, where it can be read as a record of one arrangement rather than an instruction carved into the room.

Rowan notices that Talia waits for the worker to finish before asking for another turn of the wheel. June says the cook must be able to see who is changing the air around the flame. A fixed number cannot replace a glance at the door, the cart and the people beside the stove. The new note has three small sketches and room for another. Each cook may add a condition that changes the flame path. The recipe stays repeatable because it says when to stop and look again, not because it pretends the room never changes.""",
    "june_stonepot_oren_record": """Second hearing — a measure can carry two histories

Oren holds the kitchen packet in one hand and the basin reserve card in the other. Both use the same weight mark, yet he says he would never want a clerk to combine them. The first belongs to an experimental row and can be spent on a meal; the second is guarded against a season when the water schedule fails. June writes each source on its own label, then asks Oren to check her spelling of the old bed name.

The shared measure reminds Oren of his mother's tin, but the packet is not taken from it. He says this matters because a familiar size can make two stores look interchangeable. Rowan copies the measure without copying the ownership. In the evening, June uses the trial portion and returns the unground kernels to Oren. No one treats the small cooking decision as permission to draw on the reserve. Oren keeps the kitchen receipt beside his own notes, not inside the tin. The two histories now sit next to one another where they can be compared without being merged.""",
    "june_stonepot_grow_record": """Second hearing — the row that could not be hurried

June remembers arriving at the bed before dawn and finding Oren there with his sleeves rolled past his elbows. He wanted to pull one shoot to see whether the roots had taken. She gave him the watering can instead. A crop can look unchanged while it is doing work below the soil; pulling it early would answer a question by destroying the chance to observe the next day.

Oren laughs at himself when Rowan mentions this in the ledger. Later, he measures the same row at noon and finds the wall-side soil drying first. The difference is useful for this bed, in this stretch of weather. June adjusts one small watering, not the whole basin schedule. When harvest comes, they keep the food grain and seed heads separate. Oren takes pride in the few intact heads, but he asks not to have the bed called a success for every grower. His row taught him how to wait and which patch to watch; it did not promise the same result everywhere. June keeps his observation with the date and shade conditions so another gardener can test it again.""",
    "june_stonepot_fish_record": """Second hearing — a fish has more than one destination

The Warm Run is quiet when Rowan brings the catch back, and June asks him not to lay it beside the seed cloth. She clears a different board and rinses the knife before touching the perch. Talia arrives with a water jar but waits until June has finished the food check. They agree to write two notes: June's records how the fish was handled for the kitchen, while Talia records the outlet and the time of collection for her separate inquiry.

Neither woman wants the other's page to become a broad claim. June cannot use one fish to describe the whole run. Talia cannot infer drinking safety from its condition. Rowan records the bait and the exact spot so a later catch can be compared fairly. The perch is cooked that evening, and its cleaned bones go into a small covered bowl rather than back toward the water. June says a meal and an ecological survey may share an afternoon without becoming the same task. The record gives each purpose enough detail to be useful and leaves the rest open.""",
    "june_stonepot_grindstone_record": """Second hearing — one turn belongs to the person at the mill

Oren offers to keep the hand mill turning while June checks the recipe. She lets him begin, but stops him when he starts matching the speed of the sluice wheel outside. The grain shifts under the stone when the handle is rushed. He slows down, feels the resistance and finds a small grit fleck caught under the lip. The cleaned tray catches the rest of the flour before it can mix with the dust left from the pantry shelf.

June tells Rowan she once treated a quiet worker as proof that the mill was easy to use. She now asks each person who wants to grind to try the handle with an empty bowl first. Nobody is assigned the job because they are the strongest or because they already know the kitchen. The card records the batch size and cleaning steps; it does not set a pace. After the test, Oren wraps the handle to keep dust out. He is pleased to have found the grit, though June credits the pause rather than the force he used. The next shift will begin with a clean stone and the chance to learn the turn.""",
    "june_stonepot_cook_record": """Second hearing — the recipe leaves room for a cook

The first batch tastes thinner than June expected. She reaches for salt, then pauses so Rowan can write down the original seasoning before anyone changes it. One worker wants more broth; another prefers the grain firm. June makes a small adjustment in a second bowl instead of rewriting the whole recipe. Both portions come from the same pot, but they do not have to be served as though every person asked for the same texture.

Rowan's restorative meal is set aside before the kitchen table begins. June wants the player's inventory item to have a clear use, while the kitchen recipe has a different question: can the people eating it ask for a change without being treated as a problem? She records two versions and the amounts used. The page is longer, but no version becomes the official taste of Cinderwell. June signs only for the batch she cooked and invites the next cook to make a new note. Her method preserves what can be repeated and keeps preference where it belongs, with the person holding the spoon.""",
    "june_stonepot_sample_record": """Second hearing — leave the blank slips blank

After the first pot, one person returns a slip with three words about salt. Another leaves a smudge where a name could have been. June does not ask whose mark it is. She pins both to the underside of the recipe sleeve, where a cook can see the comments before starting but a visitor cannot read them from the door. Rowan asks whether she will need to count the slips to decide which seasoning wins. June says a handful of anonymous remarks is useful guidance, not a vote that speaks for everyone who never wrote.

Oren reads the note about salt and suggests offering a small portion before the next pot is served. June agrees, then asks him to record the suggestion as his rather than attributing it to the table. He does. The cook may still choose the seasoning according to what ingredients remain, and diners can refuse without explaining themselves. The sample check records how the meal was received by the people who chose to comment. It cannot tell the kitchen how many people came hungry or what they would want tomorrow. The empty slips stay beside the full ones for whoever prefers to write later.""",
    "june_stonepot_choice_record": """Second hearing — there is no clean arithmetic for a bowl

June does not follow Rowan when he carries the first bowl away. She watches the doorway, then asks Talia how long the next gate inspection can wait. The cistern crew needs someone to write the measurement; the road crew needs food before the walk. June knows what the route choice sent today and what remains on the counter, but she refuses to turn that count into a rule about who should receive tomorrow's first serving.

When Rowan returns, she asks whether the bowl arrived warm. He can answer that much. He cannot know whether it met every need at either destination. June accepts this smaller report and puts the next portion where he can take it if he chooses. The two keepsakes remember different acts of care, not different rankings of people. She asks him to come back after the next shift and listen before the pot is divided again. No story flag can replace the voices of those present at the kitchen table on another day.""",
    "june_stonepot_table_record": """Second hearing — people decide when a meal is enough

The late shift gathers at different times. One worker eats standing by the door because the wheel alarm has not been cleared; another stays to wash cups. June starts to write that three people shared the pot, then crosses out the number when one of them says a traveler took a bowl after she turned to the sink. The pot count is still accurate, but the number of diners is not.

She changes the entry to say how many servings left the pot for the common table. Rowan asks why that difference matters if the food is gone either way. June answers that the count may later be used to plan another meal. A false headcount could make someone believe everyone had eaten or that an extra bowl is always available. She does not need to know who took the serving. She needs the next cook to know what was cooked, what remains and when the shelf should be checked. The table can be open without becoming a roll call, and a small reliable count is kinder than a confident guess.""",
    "june_stonepot_departure_record": """Second hearing — keep the crate easy to open

The road crew asks to carry the meal in a crate that has a stiff latch. June tries it herself with damp hands and cannot open it. She calls the crew back before they leave and asks them to choose a container that any member can open without asking one person to return the key. They select a basket and wrap the covered bowl inside it. Rowan notes the change as a practical choice made by the people carrying the food.

June's earlier slip said one serving was packed; it said nothing about who had authority to distribute it. She adds no recipient name and no delivery promise. At the gate, a crew member offers to bring the basket back after the next supply run. June declines the promise because their route may change. She only asks that the empty bowl not be left in the rain. Once the group is on the road, the kitchen's responsibility is to keep enough food for its own next service, not to supervise every handoff beyond the wall.""",
    "june_stonepot_table_report_record": """Second hearing — feedback belongs beside its circumstances

The request for less salt came from a person who had been working beside the sluice for most of the day. June writes that context beside the comment only after asking whether the person is comfortable being described. They say a role is enough and decline to give a name. The note will remind the next cook that heavy work can change what a person wants, without turning one worker into a spokesperson for the entire crew.

Someone else asks to keep the recipe as it is because they liked the first bowl. June leaves both comments where the cook can see them. Rowan suggests tallying each preference, but June points out that the people who had to leave before supper never had a chance to reply. The record describes who spoke, in broad terms, and when the meal was served. It remains a small sample. June will offer the recipe again and accept new notes without requiring anyone to defend an earlier choice. Feedback can alter the next pot; it cannot close the conversation.""",
    "june_stonepot_departure_report_record": """Second hearing — a handoff ends where the road begins

The crew returns with the basket after two days, scraped along one side and still usable. They say the bowl reached the first camp, but they do not know who ate from it after their own watch changed. June asks whether the latch worked and whether the wrapping kept the container steady. They answer those questions and leave the rest untold. She thanks them without asking for a route map or a list of names.

Rowan adds that the handoff is confirmed to the gate and that a later camp was reported by the carrier. He does not write that the meal reached every traveler. June approves the narrower note. In the kitchen, a report can end at the limit of what the reporter saw without being called incomplete or unhelpful. The returned basket lets them plan another serving; the uncertain journey remains with the people who made it. June hangs the receipt beside the packing card so the next crew can choose a lighter wrap, not so the kitchen can follow them farther than they agreed.""",
    "june_stonepot_afterword_record": """Second hearing — a place for the person who opens tomorrow

At the end of the week, June leaves the kitchen key on its peg and writes the name of the next cook only after that person agrees to take it. The recipe sleeve is clean. The hearth still needs its full inspection, and the pantry card still calls for another check. Nothing on the board declares the room finished. June finds this comforting: a completed quest can mark one good handoff without pretending the community has stopped changing.

Rowan asks whether she is disappointed that the kitchen is smaller than the old public hall. June looks at the benches and says size is not the same as welcome. A room can feed people well and still need more hands; the next shift may decide to expand, pause or cook something else. She wants the archive to leave that decision open. The current pot became a practice others can revisit, not a fixed program that every future resident must obey. The hearth is ready for another cook when one chooses to return.""",
    "oren_seed_tin_open_record": """Second hearing — Oren chooses the pace of the lid

The next day, Oren asks June to open the tin again with him. This time he keeps one hand on the lid and gives Rowan permission to read the note. It takes only a few seconds, but he is no longer surprised by the handwriting beneath the felt. He says he thought the first opening would either preserve everything or make the memory smaller. Instead he has learned that he can put the note back and open it again when he is ready.

June does not congratulate him for being brave. She asks if the tin should stay on the kitchen table while they work or return to his home afterward. Oren chooses the table until the planting is complete, then the shelf beside his tools. Rowan records the location for this part of the story but does not treat it as permanent custody. The object is not a test of whether Oren can share his grief. It is still his family's container, and he controls when another person sees inside.""",
    "oren_seed_tin_hinge_record": """Second hearing — a repair does not erase the earlier hand

Oren turns the hinge in morning light and recognizes the line his mother left with the old solder. He remembers holding the tin while she repaired it, but cannot say whether she had already planted from that packet or intended to do so later. His memory has sharpened around the gesture of her thumb; the order of the seasons has not. He asks Rowan to preserve that difference in the record.

When Oren made his own ridge repair after the flood, he was embarrassed that it looked rough. June points out that both patches held the lid shut through different kinds of wear. The comparison makes him smile, then grow quiet. He does not want the new story to turn the tin into an emblem of a perfect family or a perfect repair. Rowan draws the hinge from above and underneath, leaving the solder colors distinct. A future keeper can learn where to press when opening it. No one needs to polish away the marks to make the object worthy of being shown.""",
    "oren_seed_tin_paper_record": """Second hearing — a sentence can be shared without being solved

June reads the note aloud once, then asks Oren if he wants her to read it a second time. He shakes his head and repeats the sentence himself. His mother's words are short enough to fit in one breath; the new questions around them take longer. Did she want neighbors to see the row, or did she want Oren himself to watch it grow? Oren cannot know, and he does not want Rowan to fill the paper's margin with a guess.

Instead they place a copy beside the seed bed, where anyone tending the trial can read it. The original returns beneath the tin lining. Oren says this arrangement lets the note be public while the family object remains private. June asks whether he wants to explain the choice to visitors. He says the label is enough for now. The archive keeps the sentence intact and adds the present-day context in a different hand. Readers may understand the instruction differently without claiming that one interpretation belongs to his mother.""",
    "oren_seed_tin_date_marks_record": """Second hearing — do not turn openings into anniversaries

Oren sees the three cuts on the tin after a clerk asks whether they mark three winters. The question has already appeared on a copy of the warehouse register, where someone added dates in pencil. Oren studies the marks and says he was taught to count packets, not years. He is certain about how his mother showed him the cuts; he is not certain when the teaching happened. Rowan notes both parts of that answer instead of treating uncertainty as a reason to discard the family count.

The clerk removes the pencilled years but keeps a dated correction slip in the public index. Oren agrees to the correction because it names who made the inference and who challenged it. The small cuts can guide the family while the inventory uses its own marks. June places the tin on a shelf away from the reserve ledger, so a later keeper is less likely to copy the numbers into a different system. A notation is useful when its purpose travels with it.""",
    "oren_seed_tin_june_memory_record": """Second hearing — June remembers what her hands did

When Oren asks June for more about his mother's cooking, she can recall how the woman held the pan and how she waited for the edge to crisp. She cannot remember the exact year, the amount of barley or whether the little stove was used every night. Oren says those limits feel fairer than a polished story that fills every gap. June is relieved; she had feared he wanted details she could no longer supply.

They make a cake with no fish filling, using the remembered thin shape as a test. Oren turns the first one and drops a small edge back onto the pan. He laughs at the same crisp sound that he remembers from childhood, though the smell differs because the flour is new. June writes that they prepared a version inspired by the memory. The old meal remains Oren's recollection. The present cake belongs to the two people who made it today. Rowan keeps the entries adjacent so one can lead to the other without making them identical.""",
    "oren_seed_tin_first_row_record": """Second hearing — the morning he almost counted every shoot

Oren comes to the bed with a slate and begins marking each green tip. After the first dozen, he realizes that he is trying to remember the whole row while bent over one end of it. June shows him how to divide the bed by the existing stones instead. He can count one section, rest, then check it again from the opposite edge. The method is slower than he wanted but gives him a result another grower can reproduce.

He is disappointed that the number is smaller than his guess. Rowan asks whether the crop feels unsuccessful. Oren shakes his head: the row has done what they asked of it. The first count was a hope; the second is a measurement. June writes down the shade and water conditions as well as the total. Oren chooses to keep the slate instead of letting the kitchen copy it into the reserve book. His plants matter to the shared trial, but his first attempt belongs in the kitchen record where its small scale remains clear.""",
    "oren_seed_tin_first_heads_record": """Second hearing — sorting takes longer than harvesting

The handful of barley heads fits on one cloth, yet sorting them takes most of the afternoon. Oren finds a kernel with a dark spot and asks whether it should be ground or saved. June says the kitchen can inspect a sample but should not put a questionable grain into the next packet without checking. They place it in a third dish marked for review. The two obvious piles are not the only choices available.

Oren had imagined the harvest as the end of the work. He now sees why growers keep notes after the plants are cut: the next decision depends on what stayed intact, what dried properly and what needs another look. He and June prepare the meal portion separately. Rowan records the three dishes and their destinations without turning the sorting into a judgment of Oren's skill. The second packet will be considered when the grain has rested. Until then, the careful part of the harvest is not a pause in the story. It is where the next season begins.""",
    "oren_seed_tin_choice_record": """Second hearing — Oren does not owe an explanation to the shelf

After he chooses where to keep the packet, Oren writes a note for the next season and sets it beside the tin. He first drafts three paragraphs about his mother, then crosses them out. The shelf needs to say whose packet this is, how it should be kept and when to inspect it. The family story can remain in the field archive without being attached to a seed anyone might borrow.

June reads the short label and asks if he wants her signature. Oren declines; the placement is his decision, and she has signed only to confirm the trial lot is separate from the reserve. The distinction makes him feel lighter. The two storage choices are both ordinary enough to change if a dry room becomes damp or a grower asks for a packet. Rowan does not write that Oren has overcome his reluctance. He writes where the packet went, what he agreed to share and which details he kept at home.""",
    "oren_seed_tin_exchange_record": """Second hearing — no one takes the packet during this shift

At closing, the exchange packet is still on the open shelf. Oren had expected a neighbor to take it as soon as he put it there. June asks if he wants to bring it back to the winter case, but he chooses to leave it for one more day. He adds a card describing the warm bed and the patch that dried first. If a grower does take the packet, that information can help them plan; if no one does, the seed remains available without a name attached.

The shelf is not an auction, and silence is not a rejection of Oren's mother's wishes. It may mean that the planting season is wrong or that people need to ask their households first. Rowan records the packet's current location and leaves the invitation open. Oren visits later and sees a question written on the conditions card, not a claim on the seed itself. He decides to answer it tomorrow. Sharing begins here as a reversible offer, not a transfer that asks the giver to stop caring.""",
    "oren_seed_tin_reserve_record": """Second hearing — winter storage has a date on it

Oren returns a month later to check the winter case with June. The paper is dry, the packet label is readable, and no kernels have been taken. He is pleased, but June reminds him that one inspection cannot promise the packet will remain sound until spring. They schedule another check before the first warm week and place the date on the outside of the case where the next keeper can see it.

Oren adds that the seed came from the kitchen trial, not from his mother's original tin. He wants the family object to stay at home, while the new packet may eventually travel. Rowan copies this source note into the field record. If a future grower opens the case, they will know which story the seed carries and which one it does not. The decision to keep a packet is care, not proof that its owner lacks generosity. The next review belongs to Oren and the gardeners who may ask for seed, after they have compared the winter conditions.""",
    "oren_seed_tin_custody_record": """Second hearing — ownership and care need separate lines

Oren reads the draft custody label and points to the sentence that says June will check the tin. He wants her to check the kitchen packet, not take responsibility for the tin itself. They rewrite the label together. The family object remains Oren's; the trial seed has a shared record; the winter case has a review date. Three small statements are clearer than one broad promise about who is in charge.

June appreciates being asked to correct the line before it is copied. She is willing to help inspect moisture and measure the bed, but she cannot be present whenever Oren opens the tin. Rowan leaves a blank space for future caretakers to sign only if Oren names them. The current decision does not create an office or a permanent duty. Oren says that when he can see the boundaries written down, sharing feels less like handing away the whole memory. He keeps the label with the packet, not tied to the tin's hinge.""",
    "oren_seed_tin_perch_record": """Second hearing — the catch is weighed after it is cleaned

June asks Rowan to note whether the Emberscale Perch was weighed before or after cleaning. Rowan has not written a weight because the recipe uses one fish and the water study tracks another set of observations. Together they add the preparation stage so a later cook will not compare a cleaned portion with a whole catch and think the size changed.

Oren watches from the doorway and says his mother rarely measured fish for the thin cakes. She cooked by the pan's sound. June does not add that memory as a recipe instruction; the present kitchen needs a repeatable amount while it learns the filling. They prepare one test piece and leave the remaining fish sealed for the pot. Talia's water sample stays on its own shelf. The food note now tells another cook what was brought in and what entered the dish, but it does not pretend to predict future catches. Rowan keeps the modest measure because it answers the kitchen question without taking over Talia's.""",
    "oren_seed_tin_june_recipe_record": """Second hearing — write down the change from the remembered cake

June places her version beside a drawing Oren made from memory. The old cake is thinner and has no filling; the new one carries barley and perch. They both taste a corner, and Oren says the crisp edge is familiar while the center belongs to this kitchen. June asks him which name should go on the recipe. He chooses one that refers to today's shared test rather than claiming the old family version back.

Rowan adds an editor's note that the recipe is adapted from Oren's description and does not reproduce an original card, because none survives. June likes the phrasing: it gives credit without promising exactness. Oren says he can imagine his mother trying the filling and disagreeing about the salt. The thought makes him laugh instead of making the meal feel like a memorial. The kitchen can keep changing the recipe as supplies and cooks change. A copied method honors a memory best when it also admits what was invented this afternoon.""",
    "oren_seed_tin_cook_record": """Second hearing — the cake cools before Oren speaks

Oren reaches for the first cake while steam still rises from its center. June sets a board between his hand and the pan and asks him to wait one minute so the filling can hold together. He waits, listening to the crackle fade. When he bites, he closes his eyes briefly, then looks at the plate. Rowan does not ask what he saw in his memory; Oren chooses to say that the texture reminds him of a winter evening when a lamp had burned low.

The image is private enough that Rowan asks before writing it down. Oren agrees to keep it in the family margin, visible only when he opens the tin. The public recipe records the cooling time and the pan turn. It does not require a family story from anyone who wants to cook. June serves a second piece without asking Oren whether it tasted like his mother's. He can enjoy it as a meal made with friends, even if its shape came from an old memory. The archive now distinguishes a repeatable method from a personal association.""",
    "oren_seed_tin_cooling_rack_record": """Second hearing — the scorched edge is still a useful test

The first cake leaves a dark crescent on the pan. Oren is ready to call the batch a failure, but June turns the piece over and shows that the center has cooked safely while the edge browned too fast. They lower the heat, rotate the pan and set the next cake on a rack where the steam can escape. The change takes longer than either expected.

Rowan keeps the spoiled crescent in the kitchen's compost bowl and the adjustment on the recipe card. There is no reason to hide the imperfect trial; without it, another cook might begin at the same heat and burn a larger batch. Oren asks whether the card will make people think June does not know her stove. She says a kitchen trusted only when its meals are perfect cannot teach anyone. The rack note becomes an invitation to revise, not a mark against the cook. The surviving cake rests beside it, ready to be tested rather than praised.""",
    "oren_seed_tin_taste_record": """Second hearing — recognition is not a measurement

Oren asks June to make one cake without the filling and another with it. He tries each in turn. The plain one brings back the crisp edge from childhood; the filled one is a new food that he wants to share at the next meal. He can recognize a sensation without naming the exact day it came from. June does not ask him to reconstruct his mother's kitchen. She asks which present version he would like to cook again.

Rowan offers separate lines on the tasting card: one for Oren's memory and one for today's preference. Oren chooses to sign the second and leave the first within the family note. The separation lets him talk about his mother without making his memory the standard by which every cook's work is judged. June asks if the recipe title still feels right. He says yes, because it carries both the old shape and their new attempt. The distinction is small, yet it gives him room to return to the pan without having to repeat the past exactly.""",
    "oren_seed_tin_second_packet_record": """Second hearing — another packet is a new offer

Oren brings the second kitchen packet himself instead of asking Rowan to collect it. He explains that it came from the trial lot after June checked the heads and that he has kept it apart from the family tin. He is not ready to lend the tin, but he is willing to let the shared crop continue. June thanks him without treating this as a larger act than the first one.

At the bed, he marks where the packet enters the soil and watches June cover it. Rowan records the source, the amount and the current weather. The planting belongs to a new round, not to the original note alone. If the row grows, the next decision will still depend on how much survives. Oren asks to help sort the harvest when the time comes, but he does not promise to manage the bed every day. That boundary lets him participate without inheriting a job he never chose. The packet travels from one willing hand to another while the tin remains at home.""",
    "oren_seed_tin_empty_tin_record": """Second hearing — empty does not mean finished

With the last original packet out of the tin, the metal sounds different when Oren taps it. He once thought an empty container would only remind him that the seed was gone. Now he can hear the loose clasp and tell that the inside will need cleaning before he stores anything in it again. He takes the felt lining out and finds a little soil caught in one seam, which he brushes into a dish instead of throwing it away.

June asks whether the tin should stay open on the shelf. Oren closes it, then opens it again to check the hinge. He decides it may be used for seed after he chooses what belongs inside. Rowan writes the object is empty at the time of inspection, not that it has no future use. The note remains under the lining at home in its copy sleeve. Oren says the tin can hold something new without proving he has forgotten what it held before. The game records a personal object changing hands and purpose at its owner's pace.""",
    "oren_seed_tin_second_row_record": """Second hearing — three gardeners work at three speeds

During the second planting, Oren wants each row covered at the same pace. June moves faster at the edge of the bed; Rowan stops to clear a stone from the shallow groove. Oren notices that rushing to match one another would leave one patch too high and another too compacted. They agree to finish each short section before beginning the next, then compare the soil by touch.

The shared work takes longer, and no one is assigned the slowest task as a punishment. Oren says that when he planted the first row alone, he measured progress by how quickly the bed disappeared behind him. Now he measures it by whether everyone can explain what they did. June marks the sections in the ledger, while Rowan leaves the stone in place as a boundary marker. The seed came from a small trial packet, so the two rows remain small trials. The new memory is larger: Oren knows what it feels like to tend the bed with people who can disagree about pace and still finish together.""",
    "oren_seed_tin_new_shoots_record": """Second hearing — the dry seam changes the route

June finds the warm wall seam on her first watering round. Oren reaches for the whole can, but she asks him to test the soil on each side. The seam is dry; the next patch is still damp. He gives only the dry strip a little water and returns at midday to see whether the boundary moved. It has, though not as far as he expected.

They chalk the two observations with different times rather than drawing one permanent border. Rowan reminds them that the wall will hold heat differently as the weather changes. Oren likes seeing the bed answer a careful question, but he does not want the chalk to become a rule for the next grower. June erases the mark after the soil has been checked and leaves the dates in the ledger. The plant's needs can be observed again without declaring the wall always dry. A living row gives the kitchen a new task each day; its map should stay easy to revise.""",
    "oren_seed_tin_june_aftertaste_record": """Second hearing — three plates, three different silences

Oren invites three people to try the later batch: June, a worker just off shift and a traveler who has returned to the kitchen. June says the filling is balanced. The worker eats slowly and asks for plain barley next time. The traveler finishes a small piece and declines another. Nobody explains their appetite, and Oren does not ask them to prove they knew his mother.

At first he looks to June for a single verdict. She hands him the empty plates instead. Each has a different amount left, but the shapes do not tell them whether anyone disliked the meal or simply needed to go. Rowan records that three people were offered a taste, with two comments and one refusal of more. He does not convert those responses into a satisfaction score. Oren says he is glad the recipe can meet people without asking them to meet his story first. The next gathering will be a meal, not an audience for the family's memories.""",
    "oren_seed_tin_note_return_record": """Second hearing — let Oren decide which words travel

Oren copies the sentence from the note onto a card and reads both versions side by side. He prefers the original on the inside cover, where the exact handwriting remains private, and his copy beside the bed, where gardeners can see it. The card also says that he chose this placement. June asks if the public copy should explain why he has not dated it. He says the missing date is part of what they know, not something to apologize for.

Rowan makes a clean index note that points readers to the family-owned original only with Oren's permission. The words can travel without the object being moved from his home. This gives the growers enough context to plant and keeps the paper from becoming an artifact everyone expects to handle. Oren does not call this the one correct interpretation of his mother's wish. He says it is the arrangement he can live with today. If that changes, the card can be replaced and the archive can record when.""",
    "oren_seed_tin_next_season_record": """Second hearing — the review begins with the people who tend

Before the weather turns, June posts a reminder to inspect the seed beds. Oren adds a second line: ask the growers what they want to try before opening the packet. A clerk suggests setting an automatic amount aside for the reserve. Oren replies that the kitchen trial is small and cannot make that promise on behalf of the basin. June invites the clerk to join the review, but gives no one authority to decide alone.

Rowan records the questions they will bring: which heads survived, how the water schedule changed and whether the kitchen can spare grain. The review date matters because the first choice was made under different conditions. Oren still wants visible rows, but he no longer thinks every row must carry his family's name. The next season may use a different bed, different gardeners or no packet at all. His intention is to open a conversation before opening the tin. That is more durable than a quantity written down before anyone knows what the year will require.""",
    "oren_seed_tin_afterword_record": """Second hearing — invite the next cook without assigning a successor

On the evening the archive entry is filed, Oren asks to keep the recipe sleeve and leave a copy in June's kitchen. He is not giving the place to someone who will take over his mother's memory. He is giving a working recipe to anyone who wants to cook the present cake. June accepts the copy and writes where it came from, then leaves the seasoning line open for future changes.

The tin, the packet, and the cake now have different keepers. Oren can tell the family story; growers can choose whether to plant; cooks can decide how to serve. None of those roles has to become permanent. Rowan checks that the afterword says the trial happened twice in one bed and under one set of local conditions. Oren asks him to include the afternoon they spent sorting kernels, because that was the part he wants to remember next. The archive closes with an invitation to return, not an order to continue. The next person may begin a new story without inheriting an old obligation.""",
}


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(SCENES) - entries.keys())
    if missing:
        raise SystemExit(f"Missing kitchen records: {', '.join(missing)}")
    marked = [key for key, entry in entries.items() if key in SCENES and MARKER in entry["body"]]
    if marked:
        raise SystemExit(f"Second-hearing scenes already present: {', '.join(sorted(marked))}")
    before = sum(len(entries[key]["body"].split()) for key in SCENES)
    for key, scene in SCENES.items():
        entries[key]["body"] += "\n\n" + scene
    after = sum(len(entries[key]["body"].split()) for key in SCENES)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {len(SCENES)} character scenes to June/Oren archive records: +{after - before:,} raw words.")


if __name__ == "__main__":
    main()
