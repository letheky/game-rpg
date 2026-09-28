#!/usr/bin/env python3
"""Install Tomas Reed's regional field-repair atlas in the content catalogs."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"

def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))

def write(name, data):
    (CONTENT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def upsert(entries, additions):
    by_id = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in by_id:
            entries[by_id[entry["id"]]] = entry
        else:
            by_id[entry["id"]] = len(entries)
            entries.append(entry)

# key/title/kind/target/location/giver/speaker/objective/dialogue/record/body/marker/position
common = [
("open","The Open Joint Atlas","talk","tomas_reed","dawnkeep_outpost","tomas_reed","TOMAS REED",
"Meet Tomas Reed at Dawnkeep Forge and ask why one repair gauge needs more than one setting.",
["Gideon's axle pin fits his wheel because you measured that wheel. Good work should stay that specific.","I kept my first master's field book. Its margins leave room for a second measurement when the first one does not fit."],
"A Book with an Unfinished Margin","Tomas does not call the blank edge of the book an omission. His first master drew a narrow line beside each pattern, a place to record where the piece was used and what changed before the repair held. Later copies removed the line to make their diagrams easier to reproduce. The drawings became tidy; the weather, wear and local material disappeared. Tomas wants the margin restored without turning it into another rule that every maker must obey. Rowan agrees to carry the book through several regions, test an adjustable gauge and write down where that gauge itself falls short.","",(0,0)),
("master_gauge","The Rule on the Master Gauge","inspect","atlas_master_gauge","dawnkeep_outpost","tomas_reed","ROWAN HALE",
"Read the old forge gauge and find the fixed notch that replaced its adjustment marks.",
["The first three pins move. This fourth notch is filed into the handle; the book doesn't say when it was added.","I will keep the old spacing visible and write down who made the permanent mark."],
"Notches Removed from the Master Gauge","The brass gauge has three movable pins and a fourth notch cut directly into its handle. The cut is cleaner than the dents around it, so it was made later, but no date survives. A fixed notch is useful when many identical pieces are made under known conditions. It becomes risky when copied onto a wheel swollen by rain or a hinge forged from a different batch of iron. Rowan records the notch as a later alteration, not as proof that someone intended to force every repair into one size.","document",(3.4,1.9)),
("cart","Gideon's Wheel, Not Every Wheel","inspect","atlas_cart_comparison","ashfall_village","gideon_park","ROWAN HALE",
"Compare the repaired cart's axle pin with the older wheel sketch in Gideon's margin.",
["The pin turns without scraping, but the old drawing sits two fingers wider than this rim.","A drawing helps someone begin. It cannot tell them the load, the weather or how this wheel was repaired."],
"One Cart Is One Measurement","Gideon's cart uses the Ashfall Axle Pin forged for its cracked hub. The old drawing shows a wider rim and a straight beam where the repaired cart now carries a slight bend. The pin works for the current wheel under an empty-cart trial on dry ground. It is not a universal pattern for carts with swollen spokes or uneven loads. Gideon asks Rowan to preserve the successful measurement with its conditions. If someone copies only the pin's length, the copy may seem exact while leaving out why that length was chosen.","document",(-8.7,1.9)),
("gideon","Gideon's Repair Order","talk","gideon_park","ashfall_village","gideon_park","GIDEON PARK",
"Ask Gideon which repair notes helped during the evacuation and which were only guesses.",
["I used to write 'strong enough' when I meant 'it held while we watched.' Those aren't the same sentence.","Put the load and ground beside the mark. If either changes, the next person must measure again."],
"A Repair Note Should Name Its Conditions","Gideon's old notes use 'strong enough' beside several braces. He remembers one holding a roof beam for an afternoon but cannot say whether it stayed safe after rain softened the wall. The phrase records a judgment without its boundary. On Rowan's page he describes what was present: a dry cart, no cargo and two people watching the wheel during a short roll. He does not erase the earlier wording. A reader should see what Gideon knew then and what he would ask the next repairer to test now.","",(0,0)),
("reed","A Reed That Flexes Before It Splits","grow","windglass_reed","salt_road","tomas_reed","ROWAN HALE",
"Grow Windglass Reed at Salt Road and compare its flexible fibers with the forged gauge.",
["The reed bends along its length and tears across the grain. That may keep grit away; it cannot bear the cart's load.","Record how it was grown before we fit it into a tool. A wet-season stalk may behave differently."],
"Windglass Reed as Packing, Not Structure","The harvested reed can wrap around a loose metal jaw and keep grit from lodging between the gauge and a surface. Its fibers bend with the grain but split under crosswise pressure. Tomas refuses to call it a substitute for iron. Rowan records the bed, harvest day and stem condition, then keeps one stalk whole for another maker to compare. Packing can make a tool easier to use without making it stronger. The distinction prevents the word 'reinforced' from hiding which material bears the actual force.","",(0,0)),
("skate","A Catch from the Sheltered Pool","fish","saltspool_skate","salt_road","tomas_reed","ROWAN HALE",
"Catch a Saltspool Skate at the sheltered pool and record its oil as a possible hinge treatment.",
["This catch left a thin oil on the cloth. It might slow rust on one scrap, but it proves nothing about every tool.","Keep the catch site and date. Talia can compare the treated sample with an untreated one."],
"Saltspool Oil and a Narrow Claim","Rowan catches one Saltspool Skate at the sheltered pool. It leaves an oily trace on the cloth, and Tomas proposes testing a little on scrap iron. Neither observation establishes how the fish population changes through a season or whether the oil prevents corrosion in every climate. The catch record names the pool and day so the comparison can be repeated. Talia will test treated and untreated scraps side by side. Until then the oil is a candidate hinge treatment, not a recommendation for tools used near food or drinking water.","",(0,0)),
("talia","Talia's Comparison Cups","talk","talia_mercer","cinderwell_basin","talia_mercer","TALIA MERCER",
"Ask Talia how she separates a metal sample's condition from the water around it.",
["A stain on iron can tell us what touched that piece. It cannot tell us whether the whole channel is safe.","We will use the same cup and time window for both scraps, then list what we did not control."],
"Two Scraps, One Matched Trial","Talia compares a treated scrap with an untreated one using water from the same marked cup. She labels both before they enter the basin because a later observer must know which surface received fish oil. The test lasts one watch, not a season. Temperature, flow and the cup's source remain beside the result. If one scrap changes less, that difference may justify another test; it will not identify the chemistry of every channel or certify metal for food service. A useful trial is allowed to produce a small answer.","",(0,0)),
("cup","The Water Stayed beside the Test","inspect","atlas_matched_cup","cinderwell_basin","talia_mercer","ROWAN HALE",
"Read the sample card and confirm that both scraps came from the same cup at the same time.",
["The notes show one cup, one collection time and two scraps with different surface treatments.","Water may have changed before collection. This cup cannot rank the whole basin."],
"A Matched Pair Does Not Describe a Basin","Both scraps were submerged in water collected at the upper channel on the same morning. One was wiped with a little Saltspool oil; the other was untreated. The treated scrap darkened less during this brief observation, though the cup had been stored under a cover before Rowan arrived. The test supports another matched trial. It does not report the channel's safety, a contamination source or change after rain. Talia leaves the cup's location and storage time visible, refusing to let an orderly table become a wider claim.","document",(-2.8,-2.3)),
("forge","Forge the Adjustable Jaw Gauge","craft","regional_fit_gauge","dawnkeep_outpost","tomas_reed","TOMAS REED",
"Craft the field gauge from Tomas's steel blank, Windglass Reed and the Saltspool Skate catch.",
["The reed keeps grit from the sliding jaw; the brass pin still carries the measuring force.","Build a second movable jaw and leave room for the maker to write why it was adjusted."],
"Regional Fit Gauge: Build Record","The adjustable jaw gauge combines a steel blank, a reed packing strip and a little Saltspool oil on its hinge. The steel bears the force; the reed keeps grit away; the oil is used only on the hinge pin. Rowan forges one tool at Dawnkeep and stamps no single distance into its handle. Tomas asks him to scratch temporary marks during each field trial, then remove or relabel them when conditions change. The design carries a method for recording variation, not a final answer about every joint.","",(0,0)),
("fit_test","A Gauge Is Not a Verdict","interact","regional_jaw_test","ashfall_village","tomas_reed","ROWAN HALE",
"Use the adjustable gauge on Gideon's test stand and keep its reading separate from the repair decision.",
["The jaw meets the hub at two points, then slips when I measure across the old crack.","The tool shows where surfaces differ. Gideon still decides whether the cart is ready for the stated load."],
"The Gauge Found a Difference","At Gideon's stand the gauge holds against two clean surfaces of the hub, then slips across the old crack. That failure is useful: the instrument cannot measure a surface without a stable edge. Rowan leaves the mark beside the crack and writes 'do not infer fit across fracture.' The gauge does not decide whether the cart should carry a load. Gideon and Mira will test that question separately, with the axle pin installed and the cargo stated in advance.","document",(5.6,1.7)),
("mara","Mara's Living Packing","talk","mara_bell","greenwake_refuge","mara_bell","MARA BELL",
"Ask Mara whether plant fiber can protect a joint without hiding that it will change as it dries.",
["A grafting tie holds because it can be replaced. If it swells and stays forever, the support becomes a trap.","Date the fit and leave one side open. The next gardener should see whether it tightened."],
"A Brace That Can Be Removed","Mara shows Rowan a living graft tied with bark fiber. It loosens after rain and tightens as it dries, helpful only because the tie is checked and replaced. A permanent metal clip holds the same branch differently. She will not call either method safer everywhere. The record must name plant, moisture and inspection interval, then explain how to remove the brace without tearing the stem. Rowan sketches the open side of the tie rather than a closed loop that could cut into new growth.","",(0,0)),
("glassplum","One Glassplum Stem, One Season","grow","glassplum","greenwake_refuge","mara_bell","ROWAN HALE",
"Grow one Glassplum crop and compare stems from the watered and drier side of the bed.",
["Both stems came from the same seed packet, but one grew nearer the runoff line.","Record bed position and watering turn instead of calling the difference a property of the whole variety."],
"Glassplum Stem Notes","Mara's single bed has two stems that look alike at first glance. The one by the runoff line grew wider, though it also received water earlier in the rotation. Seed source, position and watering time are all recorded. Rowan cannot assign the difference to one factor from a single season. A stem can still serve as a fit sample when paired with a second piece cut at a known angle. Mara refuses to let the sample leave Greenwake without its label; an unlabeled piece would travel farther than its evidence.","glassplum_tree",(-4.6,2.6)),
("stem_fit","The Stem Must Keep Growing","inspect","atlas_graft_fit","greenwake_refuge","mara_bell","ROWAN HALE",
"Inspect Mara's removable graft tie and identify the gap that lets the stem expand after fitting.",
["The tie leaves an opening. It supports the branch today without guessing how thick it will grow.","Add a check date. A measurement can go stale while the living thing keeps changing."],
"An Adjustment with a Review Date","The tie supports the branch at two points and leaves a gap where the stem can thicken. Mara checks it at the next watering turn. A closed brace would be easier to draw, but its certainty could hide damage over time. Rowan records the fit as temporary and adds a review date rather than copying its width into a permanent template. The atlas needs an instruction for returning to a living object: the material may change after every measurement. The guide is not complete when a number is written; it is complete when someone knows when to measure again.","document",(-2.4,1.1)),
("lyra","Lyra's Resonance Check","talk","lyra_moss","choir_beneath_lake","lyra_moss","LYRA MOSS",
"Ask Lyra how she checks a loose joint by sound without preserving nearby private voices.",
["The frame rings after the fastener shifts. I log the note and place, not a voice caught in the same room.","A sound test can help repeat a repair. It doesn't grant permission to keep every sound around it."],
"Listening for a Shift, Not a Speaker","Lyra taps the test frame with a padded mallet, waits for the room to settle, then makes a second strike. The first sound overlaps a worker speaking outside; she discards that recording and retains only the marked interval after the doorway closes. Her log names the tool, frame and room, not the person whose voice crossed the sample. A longer ring may indicate looseness in this frame, but the room's stone and water also change resonance. Lyra records those conditions so future listeners can compare the setup without treating one pitch as a universal sign of failure.","",(0,0)),
("koi","A Whisper Koi beside the Frame","fish","whisper_koi","choir_beneath_lake","lyra_moss","ROWAN HALE",
"Catch a Whisper Koi at the Choir pool and record its location separately from Lyra's sound test.",
["The scales trembled when I lifted the net, but the frame test happened elsewhere and earlier.","I won't use the fish to explain a sound it never encountered."],
"Two Observations, Not One Cause","Rowan catches one Whisper Koi at the pool near the Choir frame. Its scales tremble briefly after the net is raised. Lyra's resonance test happened indoors before the catch, with a different tool and no shared recording. Both observations can stay in the atlas without being joined into a causal story. The entry names pool, date and handling, and notes that no population survey took place. A vivid detail makes a report easy to remember; it can also tempt a reader to supply a connection that the record does not contain.","",(0,0)),
("sound_card","The Quiet after the Strike","inspect","atlas_resonance_card","choir_beneath_lake","lyra_moss","ROWAN HALE",
"Read Lyra's resonance card and keep room size and strike distance beside the interval.",
["The same frame rang longer when the mallet struck closer to its corner.","We can repeat the position. We can't carry the number into another room without retesting."],
"Resonance Card with Its Room Attached","Lyra's card lists two strikes on one frame. The second began farther from the corner and produced a shorter ring. The interval can compare those trials, but the card also names room, water level and padded mallet. If any changes, the number may change. Lyra leaves a blank box for a new room instead of copying the first result everywhere. The field guide treats sound as a way to notice movement, not as a command that overrides a craftsperson's inspection.","document",(-2.8,-0.8)),
("ruth","Ruth's Bracket in Salt Air","talk","ruth_calder","salt_road","ruth_calder","RUTH CALDER",
"Ask Ruth Calder how often the milepost bracket is checked after salt wind loosens its fasteners.",
["The crew checks it before storm season and after any day the marker swings enough to strike stone.","That's a schedule built from this post and these winds, not a rule for every coast."],
"A Bracket Has a Weather Schedule","Ruth's crew checks the milepost bracket before storm season and after a visible swing. It is exposed to salt wind from the west; a sheltered inland bracket may not need the same schedule. Her predecessor copied a quarry's monthly check and found rust beneath the plate before the next inspection. The newer schedule is more frequent, but it is still local, not law. Rowan records wind direction, bracket material and the visible sign that triggers an extra check.","",(0,0)),
("bracket","The Fastener behind the Milepost","inspect","atlas_milepost_bracket","salt_road","ruth_calder","ROWAN HALE",
"Inspect the milepost bracket and note which fastener loosened without removing its marker.",
["The lower pin moves first because grit collects under the plate. I can see wear; I can't date its beginning.","Ruth wants a check that leaves the route sign readable during inspection."],
"Wear Does Not Carry a Date","The lower fastener has a brighter scrape than the upper pair. Fine grit gathered beneath its plate, where each gust allowed a small movement. Ruth cannot say when it began; the bracket may have loosened over many storms or during one impact. Rowan photographs both fasteners before tightening the lower pin, preserving their difference without inventing a timeline. The marker remains legible during inspection. A maintenance note should explain how to check a joint without removing the signal travelers rely on.","document",(-1.0,2.1)),
("evelyn","Evelyn's Second Calibration","talk","evelyn_hart","outerwake_archive","evelyn_hart","DR. EVELYN HART",
"Ask Evelyn Hart how to report a gauge that repeats on a table but changes when its holder changes.",
["The jaw returns to the same mark on my table. Rowan places it at a different angle against the same rim.","Keep both readings and write down each method before adjusting the tool."],
"Repeatability and the Hand Holding the Tool","Evelyn tests the gauge on a polished ring, then asks Rowan to repeat the fit without seeing her mark. The jaw returns to the same distance on the table, yet its angle differs between their hands. The tool may be sensitive to grip or to a small tilt in the surface. Evelyn refuses to average the numbers before they understand why. She records both operators and preserves the unadjusted scale. A repeated number is useful while the method still needs revision; removing the operator from the record would make disagreement impossible to reproduce.","",(0,0)),
("carp","A Catch with a Different Current","fish","farwake_carp","outerwake_archive","evelyn_hart","ROWAN HALE",
"Catch one Farwake Carp and record pool depth and current beside the measured scale plate.",
["The current changed while I waited for the bite. The scale plate isn't a ruler for the water.","Keep the fish and gauge in separate columns, with their shared time noted."],
"Farwake Sample and Moving Water","The Farwake Carp was caught near the outer shelf after the current shifted twice. Rowan records depth and bait, then measures a loose scale beside the gauge. The fish is a local sample, not a representative of every body in the lake. Its scale bends under different pressure than brass or wood, so the readings are not directly comparable to the milepost bracket. Evelyn retains the catch because it shows where the instrument may need a softer jaw, not because it answers a question about the whole population.","",(0,0)),
("margin","The Margin Must Hold Disagreement","inspect","atlas_calibration_margin","outerwake_archive","evelyn_hart","ROWAN HALE",
"Review the calibration sheet and keep Evelyn's and Rowan's readings visible as separate trials.",
["The table reading matches. The field angle does not. Neither row is a mistake until we know what changed.","Label the difference and keep both methods on the page."],
"A Difference Left in the Record","Evelyn's and Rowan's readings agree on the bench and differ at the outer pool rim. The first draft crossed out Rowan's result as an outlier. Evelyn restores it because the tool meets an uneven edge differently. Neither observation identifies the cause. The atlas records hand, angle and surface, then leaves room for a third trial. A guide preserving disagreement may look unfinished, but it gives another maker a path to test the instrument instead of inheriting false certainty.","document",(3.3,1.2)),
("nia","Nia's Copy Can Be Corrected","talk","nia_porter","dawnkeep_barracks","nia_porter","NIA PORTER",
"Ask Nia Porter how the guide can be copied without making its first version the only one allowed.",
["The family packets taught me to number copies, not people. A correction belongs to the page that needs it.","Leave the date, source and a place to reply. Don't make the keeper's name a condition of use."],
"Copy Number Is Not an Owner","Nia numbers each copy by edition and date while leaving contributors' names optional. Corrections attach to a page so readers can compare versions without losing the earlier reading. Nia does not erase obsolete guidance; she marks when and why it was replaced. This preserves accountability without forcing a craftsperson to publish a personal history beside a practical tool. She adds a return slot for corrections and a printed note that using the gauge does not mean endorsing every later change.","",(0,0)),
("policy","A Pattern or a Margin?","choice","atlas_policy_table","dawnkeep_outpost","tomas_reed","TOMAS REED",
"Choose whether the atlas begins as an open field pattern or locally held workshop pages.",
["A shared pattern makes a first repair easier to find. A local page lets its workshop change it without waiting for permission.","Either edition must say where its measurements were tried and what still needs checking."],
"The Atlas Decision","Tomas places two covers beside the gauge. One is a foldout for any workshop: measurements are starting points and a warning box travels beside the drawing. The other is a set of local pages held by each forge, so changes can be reviewed by people using that material and weather. The first may spread a method quickly, but a copied diagram can lose its conditions. The second allows close revision, but a traveler may not know where to request a copy. Rowan records that distribution and maintenance are separate questions. A pattern can be open while its assumptions remain visible; a local page can be shared without making contributors surrender control of their names.","noticeboard",(3.1,-3.0)),
]

branches = [
("field_copy","Foldout with Its Warnings Attached","inspect","atlas_field_copy","dawnkeep_outpost","tomas_reed","ROWAN HALE",
"Prepare a foldout pattern with its tested region and warning beside the drawing.",
["The warning can't be printed on the reverse where a hurried copyist might leave it behind.","The conditions stay inside the fold, next to the measurement that depends on them."],
"A Foldout that Carries Its Limits","The open edition puts warnings beside every measurement. Rowan includes the dry-ground Ashfall cart trial, Ruth's salt-wind schedule and Mara's removable graft tie as separate examples rather than one combined rule. Each page names its place and leaves a route for corrections. A copy may be made without Tomas's permission, but it must preserve the condition box and edition date. Nia adds a blank revision strip so another workshop can record a tested variation without pretending it existed in the first printing.","document",(-7.5,-3.4)),
("teach_open","Teach the First Fit, Then the Second","talk","tomas_reed","dawnkeep_outpost","tomas_reed","TOMAS REED",
"Ask Tomas to teach the gauge as a repeatable first fit followed by an independent second measurement.",
["I'll teach where to place the jaw and how to check it again. I won't teach that the first number ends the work.","Let a new smith explain what changed before anyone stamps a mark into the handle."],
"A Lesson with Two Readings","Tomas demonstrates the gauge to two cadets. The first places it against a flat hinge; the second repeats the fit after turning the hinge over. Their readings differ because the back plate is worn. The lesson is not that one cadet used the tool incorrectly. They document its orientation and ask whether the hinge should be replaced or watched. Tomas adds the method to the open foldout and invites the cadets to leave a dated correction when another part behaves differently.","",(0,0)),
("open_report","The Public Pattern Is Ready to Travel","talk","gideon_park","ashfall_village","gideon_park","GIDEON PARK",
"Give Gideon the field pattern and check that the dry-ground limits remain visible.",
["The diagram fits, and the warning fits beside it. I'll send a copy with the cart's repair kit.","If the wheel changes, the page gives the next person a way to measure again."],
"A Copy Sent with a Means to Revise","Gideon checks the public pattern against the cart. The conditions remain attached: empty load, dry ground, short test and named repair pin. He sends one copy with the kit and keeps another by the village tools. The guide does not certify the cart for a storm. It supplies a repeatable starting point and a visible place for new trials. Gideon asks copyists to keep the edition date and correction address so an old drawing can be challenged rather than silently treated as current.","",(0,0)),
("local_pages","Pages Kept beside the Workshop","inspect","atlas_local_pages","dawnkeep_outpost","tomas_reed","ROWAN HALE",
"Set up local pages where each forge can record its own material and inspection season.",
["The local copy has room for metal source, weather and who will check the joint next season.","It can leave the room, but no maker has to send their name with it."],
"A Margin for Local Practice","The local edition binds blank pages after each tested pattern. A workshop may note iron source, wood age, wind exposure and the next inspection date. Names are optional; method and revision date are not. Nia numbers each page so corrections can be matched without attaching a household to the repair. The format encourages useful sharing while leaving room for local materials. It does not promise every forge has the same supply or the same person available to maintain the tool.","sealed_case",(7.3,-2.4)),
("teach_local","Let the Next Smith Change It","talk","tomas_reed","dawnkeep_outpost","tomas_reed","TOMAS REED",
"Ask Tomas to leave the gauge adjustable so the next smith can record a local fit.",
["The last smith changed my first jaw. I thought that meant he'd ruined my work.","His note showed why. It kept me from repeating the same mistake. Leave the screw free."],
"The Maker Who Changes the Pattern","Tomas remembers finding a jaw gauge altered by his first master. He believed the change criticized his measurements until he found the attached note: the original jaw had scored a softer hinge after a wet winter. The master left Tomas a reason, not only a different notch. Tomas keeps the screw free and asks future smiths to record their material and conditions. The local edition treats revision as part of the craft, not proof that the first maker failed.","",(0,0)),
("local_report","A Local Page with a Review Date","talk","nia_porter","dawnkeep_barracks","nia_porter","NIA PORTER",
"Ask Nia to add an optional review date without requiring contributors to disclose their names.",
["The copy says when it should be checked. It doesn't demand a name from the person who wrote the measurement.","That is enough to invite a correction without turning the page into a roll of people who approved it."],
"Review Date without a Roll of Names","Nia writes the next review season on the cover and puts a correction envelope beside the pages. A maker can add a name, a workshop mark or no attribution. The method remains traceable because each entry names material and place; the person decides whether their identity travels with it. Nia refuses to create another roll that might be mistaken for consent to every future use. The local copy records an invitation to review, not permanent approval on behalf of its contributors.","",(0,0)),
]

items = [
{"id":"regional_atlas_scrap","name":"Mẩu Thép Bìa Sổ","description":"Thép sạch Tomas giữ lại làm trục thử cho thước hàm điều chỉnh.","category":"material","equipmentSlot":"","maxStack":99,"attackBonus":0,"guardBonus":0,"healAmount":0,"sellValue":1},
{"id":"regional_fit_gauge","name":"Adjustable Field Jaw Gauge","description":"Thước hàm trượt có thể chỉnh và ghi lại nhiều kích thước; không phải khuôn cố định.","category":"quest","equipmentSlot":"","maxStack":1,"attackBonus":0,"guardBonus":0,"healAmount":0,"sellValue":0},
{"id":"regional_open_pattern_charm","name":"Bùa Bản Vẽ Có Lề","description":"Mảnh đồng giữ cảnh báo cạnh hình đo; +1 Giáp.","category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":0,"guardBonus":1,"healAmount":0,"sellValue":0},
{"id":"regional_local_margin_charm","name":"Bùa Vạch Chỉnh Địa Phương","description":"Thước gỗ có vạch xóa được để nhắc người dùng đo lại; +1 Công.","category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":1,"guardBonus":0,"healAmount":0,"sellValue":0},
]
recipe = [{"id":"forge_regional_fit_gauge","displayName":"Forge Adjustable Field Jaw Gauge","stationId":"dawnkeep_forge","discipline":"smithing","outputItemId":"regional_fit_gauge","outputQuantity":1,"ingredients":[{"itemId":"regional_atlas_scrap","quantity":1},{"itemId":"windglass_reed","quantity":1},{"itemId":"saltspool_skate","quantity":1}]}]
choice_dialogues = [
{"id":"atlas_choice_field_copy","speakerName":"TOMAS REED","lines":["The foldout will travel farther than I can. It needs to carry its limits with it.","Anyone may copy it, and anyone who finds a better fit can send a dated correction."]},
{"id":"atlas_choice_local_margin","speakerName":"TOMAS REED","lines":["Local pages give each forge room to write what its own material asks of the tool.","I will leave them easy to lend and easy to correct. No one owns the only copy."]},
]

quests, dialogues, codex, landmarks = [], [], [], []
previous = None
for key,title,kind,target,location,giver,speaker,objective,lines,record_title,body,visual,point in common:
    quest_id = "side_atlas_" + key
    dialogue_id = "atlas_" + key
    quest = {"id":quest_id,"arcId":"the_order_of_the_dawn","stage":-1,"type":"side","locationId":location,
             "giverId":giver,"title":title,"objective":objective,
             "objectives":[{"id":"resolve_"+key,"kind":kind,"targetId":target,"requiredCount":1,
                            "description":objective,"dialogueId":dialogue_id}],
             "reward":{"gold":8 if kind in ("talk","choice") else 6,"items":[]}}
    if previous is None:
        quest["prerequisiteIds"] = ["side_ashfall_cart_afterword","order_cadet_oath"]
        quest["reward"]["items"] = [{"itemId":"regional_atlas_scrap","quantity":1},
                                      {"itemId":"windglass_reed_seed","quantity":2},
                                      {"itemId":"glassplum_seed","quantity":1},
                                      {"itemId":"earthworm_bait","quantity":6}]
    else:
        quest["prerequisiteIds"] = ["side_atlas_" + previous]
    if key in ("skate","glassplum","koi","carp"):
        quest["reward"]["items"] = [{"itemId":"earthworm_bait","quantity":4 if key == "skate" else 3}]
    if key == "policy":
        quest.update({"choiceFlag":"atlas_distribution","choiceSpeaker":"TOMAS REED",
                      "choicePrompt":"The repair atlas needs a first edition. How should it travel?",
                      "choices":[
                        {"id":"field_copy","label":"Publish a foldout with every test limit attached","flagValue":"field_copy","dialogueId":"atlas_choice_field_copy","reward":{"gold":0,"items":[{"itemId":"regional_open_pattern_charm","quantity":1}]}},
                        {"id":"local_margin","label":"Keep adjustable pages with local workshop stewards","flagValue":"local_margin","dialogueId":"atlas_choice_local_margin","reward":{"gold":0,"items":[{"itemId":"regional_local_margin_charm","quantity":1}]}}
                      ]})
    quests.append(quest)
    dialogues.append({"id":dialogue_id,"speakerName":speaker,"lines":lines})
    codex.append({"id":"atlas_"+key+"_record","title":record_title,"category":"Regional Repair Atlas","writtenBy":"Rowan Hale","unlockQuestId":quest_id,"body":body})
    if visual:
        landmarks.append({"id":"atlas_"+key+"_marker","locationId":location,"displayName":record_title,"targetId":target,
                          "visualId":visual,"positionX":point[0],"positionY":point[1],"scale":0.085})
    previous = key

for index,(key,title,kind,target,location,giver,speaker,objective,lines,record_title,body,visual,point) in enumerate(branches):
    value = "field_copy" if index < 3 else "local_margin"
    prerequisite = "side_atlas_policy" if index in (0,3) else "side_atlas_" + branches[index-1][0]
    quest_id, dialogue_id = "side_atlas_"+key, "atlas_"+key
    quests.append({"id":quest_id,"arcId":"the_order_of_the_dawn","stage":-1,"type":"side","locationId":location,
                   "giverId":giver,"title":title,"objective":objective,"branchFlag":"atlas_distribution","branchValue":value,
                   "prerequisiteIds":[prerequisite],"objectives":[{"id":"resolve_"+key,"kind":kind,"targetId":target,
                   "requiredCount":1,"description":objective,"dialogueId":dialogue_id}],"reward":{"gold":8,"items":[]}})
    dialogues.append({"id":dialogue_id,"speakerName":speaker,"lines":lines})
    codex.append({"id":"atlas_"+key+"_record","title":record_title,"category":"Regional Repair Atlas","writtenBy":"Rowan Hale","unlockQuestId":quest_id,"body":body})
    if visual:
        landmarks.append({"id":"atlas_"+key+"_marker","locationId":location,"displayName":record_title,"targetId":target,
                          "visualId":visual,"positionX":point[0],"positionY":point[1],"scale":0.085})

dialogues.extend(choice_dialogues)
quests.append({"id":"side_atlas_afterword","arcId":"the_order_of_the_dawn","stage":-1,"type":"side",
               "locationId":"dawnkeep_outpost","giverId":"tomas_reed","title":"The Measure That Leaves Room",
               "objective":"Return to Tomas and record what the atlas can test and what it cannot decide for a maker.",
               "prerequisiteGroups":[{"anyOfQuestIds":["side_atlas_open_report","side_atlas_local_report"]}],
               "objectives":[{"id":"resolve_afterword","kind":"talk","targetId":"tomas_reed","requiredCount":1,
                              "description":"Give Tomas the final field notes.","dialogueId":"atlas_afterword"}],
               "reward":{"gold":18,"items":[]}})
dialogues.append({"id":"atlas_afterword","speakerName":"TOMAS REED","lines":["The gauge still has room to move, and the book has room for another maker's note.","That's a better ending than a perfect pattern. We can repair the tool when the world changes."]})
codex.append({"id":"atlas_afterword_record","title":"The Measure That Leaves Room","category":"Regional Repair Atlas","writtenBy":"Rowan Hale","unlockQuestId":"side_atlas_afterword",
              "body":"Tomas reads the final pages without closing the book over its margin. The notes carry examples from Ashfall's dry road, Salt Road's grit, Cinderwell's water, Greenwake's living stems, the Choir's resonant rooms and Outer-Wake's uneven surfaces. None is declared the best. Each page names its object, tool, conditions and a route for another measurement. The atlas works because a reader may begin without pretending the first mark settles every future repair.\n\nThe open foldout keeps warnings beside diagrams and leaves a return address for corrections. The local pages give each forge room to record materials and review dates; contributors' names remain optional. Either edition can be copied, challenged and replaced. The records preserve what was tried, not a permanent claim over the hands that will use the tool.\n\nRowan leaves the last line empty. It is not waiting for a final standard. It is a place for the next repairer to say what changed: a storm, a new material, a different load, or a surface that no longer holds still. Tomas adds one sentence beneath it: 'Measure again before you promise.'"})

for name, additions in [("prologue_quests.json",quests),("dialogue_catalog.json",dialogues),("codex_catalog.json",codex),
                        ("quest_landmarks.json",landmarks),("item_catalog.json",items),("recipe_catalog.json",recipe)]:
    data = read(name)
    upsert(data["entries"], additions)
    write(name,data)

print(f"Upserted {len(quests)} quests, {len(dialogues)} dialogue records, {len(codex)} codex records, "
      f"{len(landmarks)} landmarks, {len(items)} items and one smithing recipe.")
