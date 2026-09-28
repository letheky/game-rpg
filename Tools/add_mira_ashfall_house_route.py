#!/usr/bin/env python3
"""Add Mira Cole's 40-definition Ashfall clinic story and its alchemy/farming loop."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"
PREFIX = "side_mira_ash_house_"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, catalog):
    (CONTENT / name).write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    positions = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in positions:
            entries[positions[entry["id"]]] = entry
        else:
            positions[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, kind, target, objective, speaker, lines, codex title/body, landmark (visual,x,y)
before_choice = [
    ("open", "The Door Beyond the Herb Table", "talk", "mira_cole",
     "Ask Mira why she keeps a second Ashfall room shuttered behind her herb table.", "MIRA COLE",
     ["The herb table is for recipes. The room behind it used to be where I learned to treat people without a crowd around them.",
      "I have kept the door shut since the raid. If it opens again, I want to know what kind of help it is meant to offer."],
     "Mira's Shuttered Room", "Mira asks Rowan to help reopen the small treatment room behind her Ashfall herb table. She trained there before the raid, but stopped using it after its hearth and door frame cracked. The room was never a ward for keeping people under watch; her mentor used it to speak with a patient away from a crowd. Mira wants to recover that quiet purpose before choosing how the room should serve the village now.", None),
    ("hearth", "A Crack Above the Hearth", "inspect", "mira_house_hearth_crack",
     "Inspect the line in the stone above the room's old warming hearth.", "ROWAN HALE",
     ["The crack follows the mortar seam and stops before the flue. The wall is stable, but a hot fire could widen it.",
      "We can warm water on the herb table until a mason has time to reset this stone."],
     "The Hearth Seam", "A narrow crack follows the mortar above the room's small hearth and stops before the flue. The wall is holding, but Mira does not want to light a full fire until its stone can be reset. She remembers her mentor boiling water on the alchemy table during a repair and decides to use that same safe workaround. The room can begin serving people before every old fixture is restored.", ("document", -8.4, 2.8)),
    ("cot", "The Cot That Folds Inward", "inspect", "mira_house_folded_cot",
     "Unfold the cot and check whether its hinge can still take a patient's weight.", "ROWAN HALE",
     ["The hinge is loose, not broken. The cot will hold if its legs are opened fully and braced against the wall.",
      "The room can take one resting patient at a time. Mira does not want to promise more than it can hold."],
     "One Cot, Clearly Stated", "The folding cot's hinge is loose, but its frame is sound once both legs are fully opened and braced. Mira plans for one resting patient at a time rather than filling the room with more beds than its doorway can serve. Her mentor used to move the cot close to the window for morning light. Mira is not ready to copy the whole old arrangement, but she wants the room to remain easy to leave.", ("sealed_case", 7.8, 2.7)),
    ("yard_warg", "The Warg at the Back Door", "defeat", "ash_warg",
     "Drive the Ash Warg away from the room's back door so the garden path can be cleared.", "MIRA COLE",
     ["It has been sleeping beneath the broken window ledge and snapping at anyone who crosses the yard.",
      "Keep it away from the doorway. I can clear the path once it stops guarding the room."],
     "The Back Door Cleared", "An Ash Warg had settled under the treatment room's broken window ledge and guarded the path through the yard. Rowan drove it away, leaving Mira a route to the garden bed and the back door. The wall still needs repair, and the room is not ready for a patient yet. Mira is glad the route is clear; she disliked having to send people back around the crowded front of the herb table.", None),
    ("seed_pocket", "A Seed in the Mortar", "inspect", "mira_house_seed_pocket",
     "Remove the seed packet wedged behind the garden bed's loose brick.", "ROWAN HALE",
     ["The packet stayed dry inside waxed cloth. The label says Emberlily, but the planting instructions have faded.",
      "Mira remembers the leaf shape. The bed is sheltered enough for a small trial."],
     "The Emberlily Packet", "A waxed packet of Emberlily seeds was hidden behind the garden bed's loose brick. The label survives, while the directions for planting have faded. Mira recognizes the broad, dark leaves from her training days. She offers two seeds for a small trial and asks Rowan to grow them where they can be watched from the open door. The packet does not belong to the strategic seed store or to any official reserve.", ("sealed_case", -4.1, -4.2)),
    ("first_bed", "The First Emberlily Bed", "grow", "emberlily",
     "Plant and harvest Emberlily in the sheltered treatment-room bed.", "MIRA COLE",
     ["Press the seed into the cool ash layer and leave room for the roots to spread under the brick lip.",
      "The flower opens late. Wait for its ember-colored center before taking the petals."],
     "The First Emberlily Bed", "The Emberlily grew in the sheltered strip beside the treatment room. Its roots held in the cool ash layer under the brick lip, and its ember-red center opened near dusk. Mira recognizes the same plant from her mentor's garden but has not used this patch for medicine before. She sets the harvested petals aside for a cautious trial and leaves the next plant to flower rather than strip every stem.", None),
    ("first_bloom", "A Flower That Opens at Dusk", "inspect", "mira_house_first_bloom",
     "Inspect the Emberlily bloom after sunset and separate the petals without crushing the center.", "ROWAN HALE",
     ["The center is warm from the evening light, not from any flame. The outer petals release cleanly when lifted from the base.",
      "Mira says her mentor dried them on cloth, never over the cracked hearth."],
     "The Dusk Petals", "Emberlily opens its bright center late in the day, when the stone around the garden bed has started to cool. The petals release cleanly if they are lifted from the base instead of pulled across the central cup. Mira remembers drying them on cloth away from direct heat. Her mentor used the flower to prepare a simple skin balm, not to cure every injury, and Mira wants to keep that limit with the recipe.", ("herb_ledger", -8.0, -0.2)),
    ("moonwort", "Moonwort for the Wash Cloth", "grow", "moonwort",
     "Harvest Moonwort for a clean wash cloth and the first Emberlily balm trial.", "MIRA COLE",
     ["Use the outer leaves for washing and keep one clean leaf for the balm. The inner stem bruises too easily.",
      "A plant can serve two small needs when we decide how much to take."],
     "Moonwort for Care", "Mira grows Moonwort for a clean wash cloth and reserves one sound leaf for the balm trial. She shows Rowan how to take the outer leaves without pulling up the plant. Her mentor taught this as a way to keep an herb bed alive through repeated small treatments. The crop is used for care and washing here; the harvest does not turn Moonwort into a universal cure or a substitute for clean water.", None),
    ("brook_trout", "Water from the Village Brook", "fish", "blackreed_trout",
     "Catch one Blackreed Trout from the Ashfall brook for Mira's warming bowl.", "ROWAN HALE",
     ["The brook is moving quickly after the ash run-off. I will take one fish from the clear bend upstream of the footbridge.",
      "It can make a warm bowl for someone resting. One catch tells us nothing about the whole stream."],
     "A Bowl from the Upstream Bend", "Rowan caught one Blackreed Trout from the Ashfall brook above the footbridge. Mira wants the fish for a warming bowl for someone who chooses to rest in the treatment room. She does not ask him to use it as medicine or to treat one catch as a count of the fish population. The brook has moved ash since the raid, so the clean bend is chosen by sight and current flow rather than by an old map.", None),
    ("mortar", "The Bowl with the Worn Rim", "inspect", "mira_house_mortar_bowl",
     "Inspect the clay mortar bowl and find the chip that keeps it from sitting flat.", "ROWAN HALE",
     ["A small chip rocks the bowl when it is pressed on the table. The inside is smooth enough to grind petals without cutting them.",
      "A folded cloth under its base will keep it level until Mira finds a potter."],
     "Mira's Mortar Bowl", "The clay mortar has a chip at its base, but the inside remains smooth and unbroken. A folded cloth steadies it on the herb table so Mira can grind petals without cutting them on a rough edge. The bowl belonged to her first training room. She had kept it in the back of a drawer after the room closed, unable to decide whether it was a useful tool or a reminder of a lesson that had ended badly.", ("document", 5.2, -4.1)),
    ("first_balm", "A Balm Made Two at a Time", "craft", "mira_emberlily_balm",
     "Brew two Emberlily Balm portions at Mira's herb table from one petal and one Moonwort leaf.", "MIRA COLE",
     ["Grind the petals gently, fold in the leaf, then warm the mixture only until it binds.",
      "This is a skin balm for a small burn or split. It cannot close a deep wound."],
     "Emberlily Balm Recipe", "Mira's Emberlily Balm uses one Emberlily petal and one Moonwort leaf per portion. Rowan makes a small pair at the herb table, following the old mortar-and-cloth method rather than heating the mixture over the cracked hearth. Mira describes it as a soothing balm for a small burn or split. It cannot close a deep wound, stop heavy bleeding or replace examination by a healer. The recipe produces two portions so the first service can be shared and still leave Rowan a usable item.", None),
    ("first_jar", "A Jar on the Open Shelf", "inspect", "mira_house_balm_jar",
     "Read the balm label and place the first jar where a patient can ask about it before use.", "ROWAN HALE",
     ["Mira writes what the balm does, what it cannot do and how often it should be applied.",
      "The label sits beside the jar instead of underneath it."],
     "The Balm Label", "Mira writes the balm's intended use and limits on a label facing the patient. The jar sits on an open shelf, not hidden inside a locked drawer. She includes an instruction to ask before applying it and a direction to stop if the skin reacts badly. This label does not make the balm suitable for every injury; it gives the person receiving it a chance to decide after hearing what Mira knows.", ("remedy_shelf", 8.0, -2.2)),
]

branch_steps = [
    ("clinic_wall", "A Window for the Fixed Room", "inspect", "mira_house_clinic_window",
     "Inspect the old window frame and measure how much light the fixed treatment room can admit.", "MIRA COLE",
     ["The frame can open halfway without catching on the cracked stone. Morning light will reach the cot, but the room will still be private.",
      "If we keep a fixed room, I want it to feel like a place someone can leave as easily as they entered."],
     "The Fixed Room's Window", "The old window opens halfway without striking the cracked stone. Morning light can reach the cot while the frame still gives a resting patient some privacy. Mira is drawn to the fixed room because it keeps the mortar, wash cloth and herb shelves together. She asks Rowan to help restore that space as a local place to rest, with the door and window easy to open from inside.", ("clinic_house", 8.1, 3.4), "open_room"),
    ("clinic_latch", "The Door Opens from Inside", "interact", "mira_house_clinic_latch",
     "Set the inside latch so a resting patient can open the clinic door without assistance.", "ROWAN HALE",
     ["The latch now turns from both sides. It holds the door against the wind but never traps the room's occupant.",
      "Mira checks it from inside before she lets anyone use the cot."],
     "An Inside-Opening Latch", "Rowan and Mira fit the old latch so the room stays closed against a gust but opens from either side. Mira tries it while inside before considering the fixed room ready. Her mentor had insisted that a patient should be able to leave without asking the person who offered care. The new latch keeps the door useful without turning a treatment space into a locked ward.", ("door_brace", 6.2, 2.9), "open_room"),
    ("clinic_basin", "A Basin within Reach", "inspect", "mira_house_clinic_basin",
     "Place the wash basin where it can be reached from the cot and refilled from the open door.", "ROWAN HALE",
     ["The basin fits beside the cot. No one has to step past the hearth to reach the door or wash their hands.",
      "Mira wants the path clear even when the room is in use."],
     "The Clinic's Clear Path", "The wash basin fits beside the cot, within reach of someone resting. The route to the door remains open, and Mira can refill the bowl without stepping across the warming hearth. She prefers a room where a patient can see the exit from the cot. The fixed clinic plan now has a clean path from door to basin to bed, with enough space for one caregiver and one guest.", ("noticeboard", 4.8, 3.6), "open_room"),
    ("clinic_choice", "Mira Chooses a Place to Return To", "talk", "mira_cole",
     "Ask Mira whether she wants the treatment room to stay open as a fixed Ashfall clinic.", "MIRA COLE",
     ["I want a room where a person can sit down and decide what kind of help they want without being hurried away.",
      "Keep the shelf low and the door easy to open. This can be a place to return to, not a place someone is kept."],
     "Mira Chooses the Fixed Clinic", "Mira chooses to reopen the fixed treatment room as a small Ashfall clinic. The room's cot, basin and herb shelf stay together, and its inside-opening latch lets a patient leave on their own. She knows a fixed place cannot reach someone who is already on the road, so she plans to keep a small supply for travelers too. Her choice gives the village one stable point of care without claiming it can answer every need.", None, "open_room"),
    ("clinic_sign", "The Red Leaf at the Door", "inspect", "mira_house_open_sign",
     "Hang the red-leaf sign outside the fixed clinic so visitors can find its door.", "MIRA COLE",
     ["The sign says 'Ashfall Clinic' in plain letters and shows the Emberlily leaf below it.",
      "No one has to knock to ask whether they are allowed inside."],
     "Ashfall Clinic Sign", "Mira hangs a red-leaf sign above the treatment room's door. It names the place simply and leaves the latch free to turn from either side. A traveler can recognize the clinic without having to find a particular healer first. The Emberlily leaf recalls the small garden that supplied the first balm. It does not promise that the room is staffed at every hour or that every injury can be treated there.", ("clinic_house", 8.6, 1.8), "open_room"),
    ("kit_straps", "A Bag That Leaves Room for Hands", "inspect", "mira_house_satchel_straps",
     "Inspect the shoulder straps on Mira's field satchel and test whether they stay clear of both hands.", "ROWAN HALE",
     ["The straps cross behind the shoulder instead of over the chest, leaving both hands free to carry a patient or a lantern.",
      "The satchel is light enough to bring medicine to the road without becoming another burden."],
     "The Field Satchel's Straps", "The field satchel's straps cross behind the shoulder and leave both hands free. Mira used an older bag during her apprenticeship, but its front buckle caught on her sleeve when she tried to lift someone. This design keeps the weight close and lets her carry a lantern or steady a patient. A traveling kit can bring care to a road crew, though its small supply cannot replace a stocked room.", ("sealed_case", -8.3, 3.2), "field_kit"),
    ("kit_roll", "The Balm Roll Stays Dry", "interact", "mira_house_balm_roll",
     "Fit a waxed cloth roll inside the field satchel to keep the balm jars from rubbing together.", "ROWAN HALE",
     ["The waxed cloth keeps dust off the jars and lets Mira open one without unpacking the whole bag.",
      "She marks the roll with the same red leaf as the garden bed."],
     "A Dry Roll for the Field Kit", "Rowan fits a waxed cloth roll inside the field satchel. It separates the small jars and keeps dust away from their lids. Mira can remove one jar without emptying every pocket onto the road. She marks the roll with the Emberlily leaf so another healer can recognize its purpose. The field kit is easier to carry now, but it holds fewer supplies than a fixed shelf.", ("document", -6.1, 2.8), "field_kit"),
    ("kit_map", "The Road Fold on the Map", "inspect", "mira_house_road_fold",
     "Inspect Mira's folded Ashfall map and mark the quickest path from the herb table to the east road.", "ROWAN HALE",
     ["The eastern path is short, but it narrows by the fallen lintel. The south gate takes longer and allows a stretcher through.",
      "Mira chooses the wider path, even if the map makes it look less direct."],
     "A Route Wide Enough for Help", "The folded Ashfall map shows two ways from the herb table to the east road. The eastern path is shorter but narrows beside a fallen lintel. The south gate takes longer and leaves enough room for a stretcher. Mira marks the wider route for the field kit. She would rather arrive a little later with space to help than follow the shortest line on the map and discover it cannot serve the person who needs her.", ("waymarker", -4.0, 0.3), "field_kit"),
    ("kit_choice", "Mira Chooses the Road", "talk", "mira_cole",
     "Ask Mira whether she wants to carry treatment supplies to the roads in a field satchel.", "MIRA COLE",
     ["I want to meet people where they are, especially if walking back here would hurt them more.",
      "The kit will be small, and I will tell anyone what it contains before offering it."],
     "Mira Chooses the Field Kit", "Mira chooses a field satchel that can reach the east road and the wider south gate. She wants to offer care where a person is already resting rather than make a sick traveler walk back to Ashfall. The kit is deliberately small and each jar will be explained before it is offered. Mira understands that a mobile supply runs out sooner than a stocked room, so she will still return to the herb table between trips.", None, "field_kit"),
    ("kit_mark", "The Leaf on the Traveling Bag", "inspect", "mira_field_satchel_station",
     "Attach Mira's red-leaf mark to the field satchel so other villagers can recognize it.", "MIRA COLE",
     ["The leaf sits beside the buckle where it can be seen before the bag is opened.",
      "If another healer carries it, the mark tells them where to bring it back."],
     "The Field Satchel Mark", "Mira attaches the Emberlily leaf beside the satchel's buckle. A villager can recognize the field kit before it is opened and can return it to the herb table after a journey. She wants the mark to identify a shared tool, not to imply that its carrier owns or controls the people who ask for help. The satchel is ready to travel with a healer who has chosen to carry it.", ("field_satchel", -7.6, 1.8), "field_kit"),
]

after_choice = [
    ("first_shift", "A Shift Without a Roll Call", "talk", "mira_cole",
     "Speak with Mira after the room or satchel is prepared and ask how she wants to begin the first shift.", "MIRA COLE",
     ["We begin by asking who wants help and what they can manage on their own. There is no list to fill before someone can rest.",
      "My mentor called that good medicine: start with the person in front of you."],
     "The First Treatment Shift", "Mira begins the first shift by asking each person whether they want help and what they are able to do themselves. She does not require a name or a written reason before offering a place to rest. The chosen setup, whether a fixed clinic or a traveling kit, changes how she carries supplies; it does not change the patient's right to hear an offer and decline it. The room is ready for its first visitor.", None),
    ("mentor_token", "The Button in the Mortar Drawer", "inspect", "mira_house_mentor_button",
     "Find the brass button Mira kept from her mentor's old work apron.", "ROWAN HALE",
     ["The button has a pressed leaf on one side and a worn edge where a thumb turned it during a long conversation.",
      "Mira says her mentor held it while listening, never while deciding for someone else."],
     "A Button Kept from Training", "A small brass button sits in the mortar drawer. It carries a pressed leaf and a smooth edge rubbed by a thumb. Mira's mentor held it during long conversations, turning it slowly while the patient spoke. Mira kept the button after the treatment room closed, though she could not look at it without remembering her unfinished training. She takes it now as a reminder to listen before deciding which tool to reach for.", ("sealed_case", 5.7, -1.4)),
    ("mentor_lesson", "What the First Lesson Was", "talk", "mira_cole",
     "Ask Mira what her mentor taught her before letting her treat anyone alone.", "MIRA COLE",
     ["She made me ask the patient to describe the pain in their own words. I wanted a faster answer; she wanted me to wait.",
      "I thought that was a lesson about manners. It was a lesson about sharing the decision."],
     "Mira's First Lesson", "Mira's first mentor asked her to let a patient describe pain in their own words before she offered treatment. Mira once thought this was a lesson in politeness that slowed down a busy room. Her mentor explained that the person receiving care knows what they feel, while the healer knows what a remedy can do. A good decision needs both kinds of knowledge. Mira wants to keep the lesson even when the room fills again.", None),
    ("second_seed", "Seeds for Another Dusk", "talk", "mira_cole",
     "Ask Mira for one more Emberlily packet to replenish the treatment-room garden.", "MIRA COLE",
     ["The first flowers were enough for a trial. Here are three seeds from the packet I saved; leave one flower standing at harvest.",
      "I want the bed to make medicine next season without emptying itself this evening."],
     "A Second Emberlily Packet", "Mira supplies three Emberlily seeds from the portion she saved for the garden. She asks Rowan to leave at least one flower standing at harvest, so the bed can renew itself rather than supply every jar at once. The seeds are a small household lot and will not change the region's food or medicine reserve. Mira is beginning to think of the treatment room as a place with another season ahead of it.", None),
    ("second_bed", "The Garden's Second Flowering", "grow", "emberlily",
     "Plant and harvest Emberlily again, leaving one mature flower on the bed for next season.", "MIRA COLE",
     ["The first bed showed where the roots hold. This one should leave enough room for a mature flower to seed itself.",
      "We can use a smaller harvest now and still keep the garden alive."],
     "Emberlily for a Later Season", "The second Emberlily bed produces another small harvest while leaving a mature flower for the next season. Mira prefers a modest yield that keeps the garden alive over stripping every open bloom for immediate use. She has seen medicinal beds disappear when all of their flowers were treated as stock. This patch gives the clinic petals for another balm batch and a visible sign that its medicine depends on care over time.", None),
    ("garden_shade", "A Patch of Shade at Noon", "inspect", "mira_house_garden_shade",
     "Inspect the garden's shadow at midday and move the cloth shade off the returning flower.", "ROWAN HALE",
     ["The cloth covers the flower longer than the leaves. Pull it back one brick so light reaches the open center.",
      "The old bed was built for a different wall; this room needs its own garden rhythm."],
     "The Emberlily's Noon Shade", "At midday, the treatment room's cloth shade covers the open Emberlily flower instead of the bed's hotter edge. Rowan moves it back one brick so the center receives more light. Mira recognizes that her mentor's old garden plan was made for a different wall and will not fit every room unchanged. The new placement lets the flower finish opening without putting the rest of the bed in direct afternoon heat.", ("waymarker", -1.4, -4.1)),
    ("second_balm", "A Second Pair of Balm Jars", "craft", "mira_emberlily_balm",
     "Brew two more Emberlily Balm portions from the second harvest at Mira's herb table.", "MIRA COLE",
     ["This batch smells brighter because the petals opened in the warm bed. Keep the cloth over the bowl while it binds.",
      "Two jars are enough for tonight's round. We can make more when the next flower opens."],
     "The Second Balm Batch", "The second batch uses Emberlily from a new flowering and a fresh Moonwort leaf. The petals opened later in the warmer patch, so the balm has a brighter scent than the first pair. Mira covers the bowl with clean cloth while it binds. The recipe remains the same, but the harvest conditions have changed. Each batch contains two portions, allowing one to be offered during the evening round while the other remains available to Rowan.", None),
    ("cooling_cloth", "Cool Cloth, Warm Jar", "inspect", "mira_house_cooling_cloth",
     "Check the balm jar after cooling and make sure its lid seals without trapping steam.", "ROWAN HALE",
     ["The rim is dry now. Close it only after the steam leaves, or the cloth will gather moisture underneath.",
      "Mira marks the jar with the opening date so another healer knows when it was prepared."],
     "The Cooling Jar", "The second balm jar cools with its lid set aside so steam can escape. Mira closes it only after the rim is dry and marks the preparation day on a removable tag. She does not treat the tag as a guarantee of shelf life; it tells another healer when the jar was made so they can decide whether it is still suitable. The first jar remains open on the clinic shelf for the evening round.", ("document", 1.9, -2.9)),
    ("night_service", "An Offer at the Evening Cot", "interact", "mira_emberlily_handoff",
     "Offer one portion of Emberlily Balm to the patient resting at the treatment cot.", "MIRA COLE",
     ["Tell them what the balm is for, then wait for their answer. The jar is theirs to accept or leave on the shelf.",
      "They accept one portion and ask to keep the label beside it."],
     "An Evening Balm Offer", "Mira explains the balm's limited use and asks the resting patient whether they want one portion. They accept it and keep the label beside the jar. The treatment uses one of the two portions made from the second harvest. The patient can decide how to apply it and may stop if it irritates the skin. Mira stays nearby to answer questions rather than treating the offer as permission to act without asking again.", ("remedy_shelf", 7.2, -3.9)),
    ("well_imp", "An Imp in the Wash Passage", "defeat", "tiny_af_well_imp",
     "Drive the Ash Well Imp away from the wash passage before it reaches the open treatment room.", "MIRA COLE",
     ["The little imp is drawn to water and keeps tipping the wash basin. Please clear it from the passage.",
      "That gives us the basin back. I will move it beside the cot once the floor is dry."],
     "The Wash Passage Cleared", "An Ash Well Imp had been tipping the wash basin in the passage behind the treatment room. Rowan drove it away before it reached the open cot. Mira dries the floor and moves the basin back within reach of the bed. The imp's presence explains the fresh marks around the drain, but not every disturbance in the old house. The passage is clear for the evening; Mira will keep checking it when the garden draws creatures toward the water.", None),
    ("well_lip", "The Drain's New Scratches", "inspect", "mira_house_well_scratches",
     "Inspect the fresh scratches around the wash drain and clear the grit from its rim.", "ROWAN HALE",
     ["The scratches run outward from the grate. They match the imp's small claws, not the older cracks in the hearth.",
      "The drain is clear now, and Mira can hear if the water starts to back up."],
     "Scratches around the Drain", "The new scratches around the drain begin at the grate and run outward, matching the Ash Well Imp's small claws. Older cracks in the treatment room follow different seams. Rowan clears grit from the rim so Mira can hear if water starts backing up. Separating the fresh marks from old damage helps her repair the right thing, but it does not identify every cause of wear in a room that stood closed for so long.", ("sealed_case", 5.8, -3.5)),
    ("mira_boundary", "A Healer's Answer Can Be No", "talk", "mira_cole",
     "Ask Mira what she will do when a patient declines the treatment she offers.", "MIRA COLE",
     ["I will explain what I know, make room for another choice, and stay available if they change their mind.",
      "My mentor said care offered without a way to refuse is another kind of pressure."],
     "The Right to Decline", "Mira says she will explain what she knows, make room for another choice and stay available if a patient changes their mind. Her mentor taught that care without a way to refuse becomes another kind of pressure. Mira once struggled to hear a refusal as anything but a judgment of her skill. The reopened room gives her a chance to practice listening without treating acceptance as proof that she was right or refusal as a failure.", None),
    ("mentor_thread", "The Apron Thread", "inspect", "mira_house_apron_thread",
     "Inspect the brass button's loose thread and decide how it can be attached without hiding its pressed leaf.", "ROWAN HALE",
     ["The old cloth is too brittle to mend, but the button's shank can take a new dark thread.",
      "Mira wants it visible on the room's curtain, where it can be seen without being worn as a badge."],
     "A Button on the Curtain", "The cloth from Mira's mentor's apron has become too brittle to hold a repair. The brass button's shank remains sound, so Mira attaches it with a new dark thread to the treatment room's curtain. She does not wear it as a badge or claim the old apron as her own uniform. The pressed leaf stays visible beside the door, where it can remind her of her training without standing in for the person who taught her.", ("document", -6.8, 4.0)),
    ("quiet_bell", "The Bell That Does Not Call a Crowd", "interact", "mira_house_quiet_bell",
     "Hang a small hand bell inside the room so the resting patient can call Mira without alerting the street.", "MIRA COLE",
     ["A single tap will reach the herb table through the open door. It will not announce anyone's name to the whole village.",
      "Mira tests it once, then leaves the choice to the person using the cot."],
     "A Quiet Bell beside the Cot", "Mira hangs a small hand bell within reach of the cot. One tap can reach the herb table through the open door, but the sound does not carry into the street. A patient can call for help without announcing their name or condition to everyone outside. Mira tests the bell once and leaves it where its user can decide whether to ring. The room becomes easier to use without asking anyone to perform their need in public.", ("noticeboard", 0.2, 4.1)),
    ("door_sign", "The Sign Read from the Road", "inspect", "mira_house_sign_sightline",
     "Check that a traveler can read the chosen clinic or field-kit sign from the path into Ashfall.", "ROWAN HALE",
     ["The marker is visible from the road without pointing toward the cot itself.",
      "A person can find the healer and still choose whether to come closer."],
     "A Sign with Room to Choose", "The red-leaf marker can be seen from the path into Ashfall without revealing the cot or the person resting there. Whether the village chose a fixed room or a traveling kit, the mark points toward help while leaving the visitor free to decide how close to come. Mira wants the sign to make care easier to find, not to make anyone's need visible to the whole road.", ("waymarker", 8.4, -0.7)),
    ("bench", "The Empty Place beside Mira", "inspect", "mira_house_empty_bench",
     "Place the spare stool beside Mira's work surface without blocking the room's clear path.", "ROWAN HALE",
     ["The stool gives another person somewhere to sit and talk without being placed between Mira and the door.",
      "There is room for a conversation and room for someone to leave it."],
     "A Stool beside the Work Surface", "A small stool fits beside Mira's work surface without blocking the clear path to the door. Someone can sit while they speak with her, rather than being asked to stand over the cot or wait outside. The stool is light enough to move when the room needs more space. Mira likes that the room can hold a conversation without forcing a person to stay in the same place once it has ended.", ("noticeboard", -0.2, -2.6)),
    ("afterword", "A Room for the Living", "talk", "mira_cole",
     "Speak with Mira after the first evening shift and agree to keep the clinic or field kit available on the village's terms.", "MIRA COLE",
     ["The room is open, and the satchel is ready to travel when I can carry it. People can ask, wait, or leave.",
      "That is enough for tonight. Tomorrow the village can tell me what it needs next."],
     "Afterword: Care without a Locked Door", "Mira keeps the treatment room open and the field satchel ready under the policy Rowan chose. The first Emberlily harvest supplied balm for an evening patient, while the second flowering began a garden that can renew itself. The Ashfall clinic does not promise a remedy for every wound or a healer at every hour. Mira's former training room has returned as a place where a person can ask for care, accept it, decline it or leave without being trapped by the offer.", None),
]


def quest_objective(key, kind, target, description, dialogue_id):
    return {"id": "resolve_" + key, "kind": kind, "targetId": target,
            "requiredCount": 1, "description": description, "dialogueId": dialogue_id}


def make_quest(key, title, kind, target, description, dialogue_id, previous,
               branch=None, branch_prereq=None, any_of=None):
    quest = {
        "id": PREFIX + key, "arcId": "ashes_of_ashfall", "stage": -1, "type": "side",
        "locationId": "ashfall_village", "giverId": "mira_cole", "title": title,
        "objective": description,
        "objectives": [quest_objective(key, kind, target, description, dialogue_id)],
        "reward": {"gold": 8 if kind in ("talk", "choice") else 6, "items": []},
    }
    if previous:
        quest["prerequisiteIds"] = [previous]
    if branch:
        quest["branchFlag"], quest["branchValue"] = branch
    if branch_prereq:
        quest["prerequisiteIds"] = [branch_prereq]
    if any_of:
        quest.pop("prerequisiteIds", None)
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": any_of}]
    return quest


quests, dialogues, codex, landmarks = [], [], [], []
previous = "side_ashfall_remedy_shelf"


def add_step(step, previous_id):
    key, title, kind, target, description, speaker, lines, record_title, body, marker = step
    quest_id = PREFIX + key
    dialogue_id = "mira_ash_house_" + key
    quests.append(make_quest(key, title, kind, target, description, dialogue_id, previous_id))
    dialogues.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex.append({"id": "mira_ash_house_" + key + "_record", "title": record_title,
                  "category": "Ashfall Clinic", "writtenBy": speaker.title(),
                  "unlockQuestId": quest_id, "body": body})
    if marker:
        visual, x, y = marker
        landmarks.append({"id": "mira_ash_house_" + key + "_marker", "locationId": "ashfall_village",
                          "displayName": title[:58], "targetId": target, "visualId": visual,
                          "positionX": x, "positionY": y, "scale": 0.085})
    return quest_id


for step in before_choice:
    quest_id = add_step(step, previous)
    if step[0] == "open":
        quests[-1]["reward"]["items"] = [
            {"itemId": "emberlily_seed", "quantity": 2},
            {"itemId": "moonwort_seed", "quantity": 1},
        ]
    previous = quest_id

choice_key = "policy_choice"
choice_id = PREFIX + choice_key
choice_dialogue = "mira_ash_house_policy_choice"
choice = make_quest(choice_key, "A Room that Stays or a Kit that Travels", "choice",
                    "mira_clinic_policy_choice",
                    "Choose whether Mira's first treatment service will use the fixed room or a portable field kit.",
                    choice_dialogue, previous)
choice["choiceFlag"] = "mira_clinic_policy"
choice["choiceSpeaker"] = "MIRA COLE"
choice["choicePrompt"] = "Where should Mira place her first reliable supply of care?"
choice["choices"] = [
    {"id": "open_room", "label": "Reopen the fixed Ashfall room with a cot, wash basin and open door.",
     "flagValue": "open_room", "dialogueId": "mira_ash_house_choice_clinic",
     "reward": {"gold": 0, "items": [{"itemId": "emberlily_window_charm", "quantity": 1}]}},
    {"id": "field_kit", "label": "Prepare a light satchel Mira can carry to the road and gate.",
     "flagValue": "field_kit", "dialogueId": "mira_ash_house_choice_kit",
     "reward": {"gold": 0, "items": [{"itemId": "mira_runner_knot_charm", "quantity": 1}]}},
]
quests.append(choice)
dialogues.append({"id": choice_dialogue, "speakerName": "MIRA COLE", "lines": [
    "Both plans can offer care, but they put the first supply in different places.",
    "Should I keep a room ready in Ashfall, or carry the first kit out to the road?" ]})
codex.append({"id": "mira_ash_house_policy_choice_record", "title": "A Room that Stays or a Kit that Travels",
              "category": "Ashfall Clinic", "writtenBy": "Mira Cole", "unlockQuestId": choice_id,
              "body": "Mira asks Rowan to choose where the treatment room's first dependable supply should go. A fixed clinic keeps its cot, basin and herbs together in Ashfall. A field kit can reach the road and gate, but carries fewer supplies and must return for refills. Both plans leave the patient free to accept or decline treatment. The choice sets the first service arrangement without claiming that one can replace the other forever."})
landmarks.append({"id": "mira_ash_house_policy_choice_marker", "locationId": "ashfall_village",
                  "displayName": "Ashfall Treatment Plan", "targetId": "mira_clinic_policy_choice",
                  "visualId": "noticeboard", "positionX": -0.5, "positionY": -4.2, "scale": 0.085})
previous = choice_id

branch_ids = []
for key, title, kind, target, description, speaker, lines, record_title, body, marker, branch_value in branch_steps:
    dialogue_id = "mira_ash_house_" + key
    quest_id = PREFIX + key
    quests.append(make_quest(key, title, kind, target, description, dialogue_id, None,
                             branch=("mira_clinic_policy", branch_value), branch_prereq=previous))
    dialogues.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex.append({"id": "mira_ash_house_" + key + "_record", "title": record_title,
                  "category": "Ashfall Clinic", "writtenBy": speaker.title(),
                  "unlockQuestId": quest_id, "body": body})
    if marker:
        visual, x, y = marker
        landmarks.append({"id": "mira_ash_house_" + key + "_marker", "locationId": "ashfall_village",
                          "displayName": title[:58], "targetId": target, "visualId": visual,
                          "positionX": x, "positionY": y, "scale": 0.085})
    branch_ids.append(quest_id)

previous = None
for index, step in enumerate(after_choice):
    quest_id = add_step(step, None if index == 0 else previous)
    if index == 0:
        quests[-1]["prerequisiteGroups"] = [{"anyOfQuestIds": branch_ids}]
    if step[0] == "second_seed":
        quests[-1]["reward"]["items"] = [{"itemId": "emberlily_seed", "quantity": 1}]
    previous = quest_id

dialogues.extend([
    {"id": "mira_ash_house_choice_clinic", "speakerName": "MIRA COLE", "lines": [
        "The room stays. I will keep the cot, basin and balm shelf ready for someone who wants to rest here.",
        "The sign will tell the road where the door is; it will not tell the room who should come in." ]},
    {"id": "mira_ash_house_choice_kit", "speakerName": "MIRA COLE", "lines": [
        "The first kit travels. I can carry it through the south gate without making a patient walk back here.",
        "The herb table stays open for refills, and the satchel can come back when its jars are empty." ]},
])

items = [
    {"id": "emberlily_seed", "name": "Emberlily Seed", "description": "A small medicinal flower seed saved for the Ashfall treatment-room bed.",
     "category": "material", "equipmentSlot": "", "maxStack": 30, "attackBonus": 0,
     "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "emberlily_petals", "name": "Emberlily Petals", "description": "Dusk-opened petals used in Mira Cole's limited skin balm. They are soothing care, not a cure for deep wounds.",
     "category": "material", "equipmentSlot": "", "maxStack": 30, "attackBonus": 0,
     "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "mira_emberlily_balm", "name": "Emberlily Balm", "description": "A two-portion soothing balm made from Emberlily and Moonwort. Restores 52 health when used.",
     "category": "consumable", "equipmentSlot": "", "maxStack": 10, "attackBonus": 0,
     "guardBonus": 0, "healAmount": 52, "sellValue": 0},
    {"id": "emberlily_window_charm", "name": "Emberlily Window Charm", "description": "A small red-leaf charm from the fixed clinic window, warmed by the room where Mira chose to listen.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 0,
     "guardBonus": 3, "healAmount": 0, "sellValue": 0},
    {"id": "mira_runner_knot_charm", "name": "Runner's Balm Knot", "description": "A quick-release knot from Mira's field satchel, tied so one jar can be reached while both hands stay free.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1,
     "guardBonus": 1, "healAmount": 0, "sellValue": 0},
]
recipe = {
    "id": "brew_emberlily_balm", "displayName": "Brew Emberlily Balm",
    "stationId": "ashfall_herb_table", "discipline": "alchemy",
    "outputItemId": "mira_emberlily_balm", "outputQuantity": 2,
    "ingredients": [{"itemId": "emberlily_petals", "quantity": 1},
                    {"itemId": "moonwort_leaf", "quantity": 1}],
}
farm = {
    "id": "ashfall_emberlily_bed", "locationId": "ashfall_village",
    "positionX": -2.6, "positionY": -1.0, "cropId": "emberlily",
    "cropDisplayName": "Emberlily", "seedItemId": "emberlily_seed",
    "harvestItemId": "emberlily_petals", "harvestQuantity": 2, "growSeconds": 100,
}
encounters = [
    {"id": "mira_house_yard_warg", "monsterId": "ash_warg", "locationId": "ashfall_village",
     "positionX": 5.4, "positionY": -0.2, "requiredQuestId": PREFIX + "yard_warg",
     "blockedQuestId": "", "blockedDialogueId": "", "contributesToQuest": True,
     "defeatObjectiveTargetId": "ash_warg", "defeatDialogueId": "mira_ash_house_yard_warg",
     "downDialogueId": "rowan_field_retreat", "reward": {"gold": 0, "items": []}},
    {"id": "mira_house_well_imp", "monsterId": "tiny_af_well_imp", "locationId": "ashfall_village",
     "positionX": 1.0, "positionY": 3.7, "requiredQuestId": PREFIX + "well_imp",
     "blockedQuestId": "", "blockedDialogueId": "", "contributesToQuest": True,
     "defeatObjectiveTargetId": "tiny_af_well_imp", "defeatDialogueId": "mira_ash_house_well_imp",
     "downDialogueId": "rowan_field_retreat", "reward": {"gold": 0, "items": []}},
]

for filename, additions in [
    ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", codex), ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items), ("recipe_catalog.json", [recipe]),
    ("farm_catalog.json", [farm]), ("encounter_catalog.json", encounters),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} Mira quests, {len(codex)} codex records, {len(dialogues)} dialogues, "
      f"{len(landmarks)} landmarks, one farm plot, one alchemy recipe and {len(encounters)} encounters.")
