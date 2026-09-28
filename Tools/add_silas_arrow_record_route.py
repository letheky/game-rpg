#!/usr/bin/env python3
"""Install Silas Vane's 38-quest Salt Road route, The Arrow Before the Answer."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"

def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))

def write(name, value):
    (CONTENT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def upsert(entries, additions):
    indexes = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)

def row(key, title, kind, target, objective, speaker, lines, record_title, record_body,
        visual="", position=None, giver="silas_vane", location="salt_road"):
    return {
        "key": key, "title": title, "kind": kind, "target": target,
        "objective": objective, "speaker": speaker, "lines": lines,
        "record_title": record_title, "record_body": record_body,
        "visual": visual, "position": position, "giver": giver, "location": location,
    }

common = [
row("open", "The Arrow Before the Answer", "talk", "silas_vane",
    "Meet Silas at the hunter's map. He wants to record where his first red arrow went without claiming whom it made turn back.",
    "SILAS VANE",
    ["I was eighteen when I loosed the first signal arrow. The order was mine to send, even if the road beyond the ridge was not mine to command.",
     "I have let other people carry the question of what happened next. I want my position and the limits of my sight in the record before I ask them for anything else."],
    "Silas Returns to the Hunter's Map",
    "After Nella files a rule for future witnesses, Silas brings his own account to the Salt Road map. He does not ask Rowan to decide whether the arrow changed the caravan's course. The map contains no view of every bend, and the people on the road were making decisions under pressure. Silas begins with what he can own: he fired, he chose the marked shaft, and he was standing at the western notch. Everything beyond those facts needs another source.",
    giver="silas_vane"),
row("map", "The Notch Above the Toll Road", "inspect", "salt_hunter_map",
    "Inspect the old hunter's map and mark the western notch, the crest and the blind bend as separate positions.",
    "ROWAN HALE",
    ["The map was drawn from the ridge after the road was empty.", "I'll keep the drawn line separate from the places the map cannot see."],
    "Three Positions on One Fold",
    "The old paper joins three places with a single red stroke: the notch where a signal could be loosed, the crest where a rider might first see it, and the bend hidden behind pale stone. A drawn stroke can suggest a path, but it cannot prove an uninterrupted view. Rowan adds a small index beside each place instead of extending the line through the blind bend.",
    "document", (7.2, -2.5)),
row("reed", "A Reed That Turns in Salt Wind", "harvest", "windglass_reed",
    "Harvest a fresh bundle of Windglass Reed. Keep the stalk direction and the dampness of the soil with the sample.",
    "SILAS VANE",
    ["I used to tie any pale stem to a shaft and call it steady.", "Take the field bundle too. Reed that stays straight in one gust may twist in the next."],
    "Windglass Reed Field Bundle",
    "The salt-bed plot yields two stems from a single cut. Both were grown in the same furrow, but one leaned toward the road and one toward the sea before harvest. Silas asks Rowan to preserve the cut end and note the afternoon gust. The reed can be a reference for a fletching trial; it is not a substitute for recording the bow angle or the weather at the time of a shot.",
    giver="rowan_hale"),
row("skate", "Scale from the Closed Pool", "catch", "saltspool_skate",
    "Catch one Saltspool Skate at Redpass Pool for a small light-scattering sample. Record the place and bait used.",
    "SILAS VANE",
    ["The old report says the arrow was bright. It does not say what every watcher could see.", "A scale is a material sample, not proof that the whole shaft shone the same way."],
    "A Saltspool Skate Scale",
    "A single Saltspool Skate scale scatters a narrow band of light when held wet beside the pool. The sample changes as it dries and turns in the hand. Rowan records the catch location, bait and time before passing it to Silas. The scale may help compare reflective surfaces in a controlled test, but it cannot recreate the arrow's brightness after years of dust, weather and altered memory.",
    giver="rowan_hale"),
row("sentinel", "A Sentinel at the Broken Range", "defeat", "roadglass_sentinel",
    "Defeat the Roadglass Sentinel prowling beside the old practice range. Recover any loose Roadglass Filament it leaves behind.",
    "SILAS VANE",
    ["It circles the stone where I once tested the red shafts.", "Clear the path before we set a new target. Do not treat the creature's trail as the arrow's trail."],
    "The Sentinel's Filament",
    "The Roadglass Sentinel has nested in the range rubble and dragged bright filament into its den. Rowan clears the path while Silas keeps beyond the marked test area. The recovered filament is a useful binding sample. Its position after the fight says where the creature carried it, not where the old arrow flew, so the field note keeps those observations on different pages.",
    giver="rowan_hale"),
row("forge", "A Loop That Holds Its Angle", "craft", "silas_windline_charm",
    "At Dawnkeep Forge, craft Silas's Windline Charm from Windglass Reed, one Saltspool Skate scale and Roadglass Filament.",
    "TOMAS REED",
    ["The reed keeps a heading, the scale catches a narrow glint, and the filament holds the notch in place.", "This charm can help you keep one test setup consistent. It cannot steady the wind itself."],
    "The Windline Charm",
    "Tomas Reed makes a small adjustable loop that fixes a sightline to a repeatable notch. Windglass Reed forms its backing, the skate scale provides a bright edge for comparison, and Roadglass Filament holds the two parts without hiding their join. The tool helps reproduce one setup. Silas writes that it does not make the user a better witness and cannot tell whether anyone saw an arrow on a different night.",
    "document", (4.9, 0.7), giver="tomas_reed", location="dawnkeep_outpost"),
row("crest", "The Crest Hides the Lower Mile", "inspect", "silas_arrow_crest_line",
    "Inspect the crest from the road side. Mark exactly where the lower mile disappears behind the stone rise.",
    "ROWAN HALE",
    ["From here the far tollhouse vanishes before the ridge itself does.", "I'll record the edge of the view, not extend it to the next bend."],
    "The Crest's Blind Edge",
    "The crest hides the lower mile from a person standing at the road. A second person two paces north sees farther between the rocks. The difference is small on the map and large enough to change an account of what was visible. Rowan marks both standing places and asks that any future witness give their position before describing the road.",
    "waymarker", (-4.8, 3.5), giver="rowan_hale"),
row("bend", "The Bend Behind the Salt Shelf", "inspect", "silas_arrow_blind_bend",
    "Inspect the blind bend from both ends of the trail. Note the portion that remains hidden from each side.",
    "SILAS VANE",
    ["The road is not a straight line after the shelf.", "I remember the red flare above me. I cannot say what the people below saw after this bend."],
    "Two Ends of the Same Bend",
    "The north approach hides the exit of the bend; the south approach hides a cart-sized space behind the salt shelf. Walking to both ends reveals no single position from which the whole curve is visible. Silas puts his remembered flash on a separate tracing instead of forcing it through the obscured section. The road's shape leaves room for several decisions without identifying which one any traveler made.",
    "waymarker", (-1.9, -3.8)),
row("backstop", "The Practice Stone Keeps a Scar", "inspect", "silas_arrow_backstop",
    "Inspect the old practice stone. Separate the shallow training scratches from the deeper impact mark.",
    "ROWAN HALE",
    ["Three small cuts share a height but not a depth.", "The deepest line may be old; without the shaft, it cannot date the strike."],
    "Marks Without a Date",
    "The stone contains three shallow horizontal cuts, one deep groove and a patch of newer mortar. The marks do not share a known date. Silas remembers practicing in the area but cannot identify this particular groove. Rowan measures each scar and labels the age as unknown. A mark is evidence that something touched stone; it is not proof of which person or event left it.",
    "signal_mark", (1.7, 3.1), giver="rowan_hale"),
row("range", "A Target for the Present Day", "inspect", "silas_arrow_test_target",
    "Inspect the new target after one practice shot. Record the shot's known shooter, position and wind before comparing its mark.",
    "SILAS VANE",
    ["That mark is mine. I fired from the chalk notch with Rowan watching.", "Now we have one example whose maker and conditions are known. Keep it apart from the old scar."],
    "A Known Shot Is a Better Comparison",
    "Silas fires one unmarked practice shaft at the new target while Rowan observes from the road. They record the shooter, release point, wind direction and time before measuring the impact. This gives them a known example to compare with the old stone. The test does not make the old mark identifiable; it shows which facts a future comparison would need before anyone makes that claim.",
    "signal_mark", (5.5, -1.4)),
row("silas", "The First Shot He Chose", "talk", "silas_vane",
    "Ask Silas to describe the signal order he received and the moment he chose to release the first arrow.",
    "SILAS VANE",
    ["The order said to send the red shaft if the western road was no longer passable.", "I saw dust above the lower mile. I chose to fire before I could see the caravan itself."],
    "A Decision Made at Eighteen",
    "Silas remembers the written order and the dust above the lower mile. He also remembers choosing to fire before he saw the caravan. That choice belongs to him even though the unseen road leaves its effect uncertain. The note does not turn obedience into innocence, and it does not turn an incomplete view into proof that the arrow caused a particular loss.",
    giver="silas_vane"),
row("ruth", "Ruth Reads the Order Beside the View", "talk", "ruth_calder",
    "Ask Ruth to place the hidden dispatch beside Silas's firing position and identify what the paper ordered, not what people later did.",
    "RUTH CALDER",
    ["I hid the page that sent him to watch the western road.", "Its words can explain the instruction. They cannot report what every person understood from the signal."],
    "An Order Is Not an Outcome",
    "Ruth confirms that the dispatch directed a watcher to signal if the western road became impassable. It contains no count of those who saw the arrow and no instruction that names a particular household. She puts her earlier concealment in the record beside the order. The page can establish what command Silas received; the consequences still need accounts from people who were there.",
    giver="ruth_calder"),
row("nella", "Nella Chooses What She Will Not Supply", "talk", "nella_pike",
    "Ask Nella whether she wants to add a family account. Accept her boundary if she declines to connect the arrow with her sibling's absence.",
    "NELLA PIKE",
    ["I know where my sibling's pass card was returned. I do not know who carried it back.", "You may record that I cannot connect the arrow to their absence. Leave the rest for my family to decide."],
    "A Witness May Decline the Question",
    "Nella does not give a statement about the arrow's effect. She confirms the returned card and refuses to infer who brought it or where her sibling went. Silas accepts the boundary without asking Rowan to persuade her. A record can include the limits of an interview without turning the refusal into evidence for either explanation.",
    giver="nella_pike"),
row("route_card", "Four Facts and Several Missing Views", "inspect", "silas_arrow_fact_card",
    "Inspect Silas's fact card. Keep his position, Ruth's order, Nella's boundary and the missing road view on separate lines.",
    "ROWAN HALE",
    ["The order, the shot, the view and the later absence are not one fact.", "A clean page must show where one account stops and another begins."],
    "The Fact Card Before the Choice",
    "The card lists four entries with different sources: Ruth's dispatch, Silas's remembered shot, Rowan's present-day view survey and Nella's choice not to connect the arrow to her sibling. The blank between them is visible rather than filled with a guess. Silas agrees that signing his own action does not give him ownership of another person's account.",
    "document", (3.8, 1.8), giver="rowan_hale"),
row("policy", "How Should Silas Carry His Account?", "choice", "silas_arrow_record_policy",
    "Choose how Silas will take responsibility for firing while preserving the limits of what the group can establish.",
    "SILAS VANE",
    ["I will sign what I did. I will not make another person sign for what I cannot see.", "Choose where the account goes next: on a public board with its limits, or in a sealed family-review copy."],
    "The Record Policy",
    "Silas accepts responsibility for sending the signal arrow and for waiting too long before documenting his own position. The group now has to choose how other people will encounter that account. A public first-person statement can make his action visible without exposing Nella's family. A sealed copy can preserve the same method while giving the family control over whether to review it. Neither route settles the arrow's effect.",
    "noticeboard", (0.0, 4.1), giver="silas_vane"),
]

public = [
row("public_open", "Silas Writes in the First Person", "talk", "silas_vane",
    "Hear Silas draft a first-person statement that names his own release of the arrow and leaves other people's choices unnamed.",
    "SILAS VANE",
    ["I fired the shaft. I had dust for a sign and no view of the caravan.", "That sentence is mine. The next sentence cannot say what the people below decided."],
    "A Statement with a Subject",
    "Silas chooses a sentence whose subject is himself. It records his action and the limited view he had at the time. He removes a later phrase that said the caravan turned because of him; nobody present can establish that from the surviving evidence. The correction makes the statement narrower and more accountable at once.",
    giver="silas_vane"),
row("public_board", "Leave the Family Names off the Board", "inspect", "silas_arrow_public_board",
    "Inspect the public notice draft. Confirm that no family name or unverified headcount appears beside Silas's account.",
    "ROWAN HALE",
    ["The board gives the reader Silas's position and the words he signed.", "The unfilled names are not an invitation to guess who stood on the road."],
    "A Public Copy Without a Roll Call",
    "The notice board carries Silas's signed account, a small drawing of his standing place and the weather notes. The page contains no list of travelers or households. It says the lower mile was out of sight and asks for corrections from witnesses who choose to speak. The public copy cannot be mistaken for a complete roster because it does not claim to be one.",
    "noticeboard", (-6.2, 2.2), giver="rowan_hale"),
row("public_method", "Show the Measurement Method", "inspect", "silas_arrow_public_method",
    "Inspect the method sheet and make sure another person could repeat the present-day line-of-sight check.",
    "TOMAS REED",
    ["I have added the distance from the notch to the target and the direction of the wind.", "A reader can repeat that trial. They still cannot repeat the night itself."],
    "A Repeatable Daylight Method",
    "The method sheet records the two standing places, the ridge height, the wind and the daylight conditions. It also labels the current target as a modern practice shot. Tomas checks that the gauge opens to the same notch when reset. Repeating these conditions can compare equipment in daylight; it cannot recreate what a distant traveler saw during the old signal.",
    "document", (6.5, 2.7), giver="tomas_reed"),
row("public_ruth", "Ruth Checks Her Own Line", "talk", "ruth_calder",
    "Ask Ruth to review the public wording and keep her responsibility for hiding the dispatch beside, not inside, Silas's account.",
    "RUTH CALDER",
    ["My concealment is part of this record. It does not tell us how each traveler read his arrow.", "Leave the two actions next to each other; do not make one cancel the other."],
    "Two Signatures Do Not Become One",
    "Ruth reviews the wording and signs a separate note about concealing the dispatch. The two statements share a folder but keep their authors, dates and actions distinct. The archive does not use Ruth's guilt to confirm Silas's memory or Silas's signature to erase Ruth's choice.",
    giver="ruth_calder"),
row("public_nella", "Nella Declines a Public Quote", "talk", "nella_pike",
    "Offer Nella a chance to review the notice. Respect her choice not to add a public quote about the missing sibling.",
    "NELLA PIKE",
    ["I will read the page. I will not put my family's empty place on the village board.", "You may record that I reviewed it and declined a quote. That is enough."],
    "Review Is Not Consent to Publish",
    "Nella reads the public notice and confirms that it contains no family name. She declines to add a quote. Her review is logged as a check of the page's boundary, not as approval of Silas's account or consent to publish her words. The difference remains written in the receipt.",
    giver="nella_pike"),
row("public_signature", "Silas Signs the Limits Too", "talk", "silas_vane",
    "Ask Silas to sign beneath both his statement and the line that says the arrow's effect is unknown.",
    "SILAS VANE",
    ["I used to think signing meant standing behind every sentence on the page.", "Now I will sign the limit as firmly as the action."],
    "The Uncertainty Has a Signature",
    "Silas signs his first-person account and the unresolved line below it. This does not weaken his admission; it prevents later readers from expanding it into a claim he cannot support. The date and witness to the signature are recorded so a later correction can be attached without quietly replacing his words.",
    giver="silas_vane"),
row("public_post", "The Account Goes Up at the Pass", "inspect", "silas_arrow_public_post",
    "Inspect the mounted public copy. Confirm the correction path and next review date are visible.",
    "ROWAN HALE",
    ["A small pocket below the sheet can hold a correction without tearing the original.", "The review date is a reminder, not a deadline for anyone to testify."],
    "A Public Copy with Room to Change",
    "The posted account has a dated correction pocket and a blank line for the next review. No one is required to speak by that date. The original statement remains legible if a correction is added, and the notice explains where a witness may leave a private request instead of a public name.",
    "noticeboard", (-3.0, -4.0), giver="rowan_hale"),
row("public_after", "The First-Person Account Is Filed", "talk", "silas_vane",
    "Speak with Silas after the account is posted. Confirm that the chosen copy names his action without assigning the missing decision to anyone else.",
    "SILAS VANE",
    ["The road is still incomplete in the record. At least my part no longer hides behind the blank.", "If a witness corrects me, the page has room for it."],
    "After Posting the Account",
    "Silas returns to the board after its first day in public. A passerby has left no name, only a request to keep the line that says the lower road could not be seen. Silas leaves the request attached without treating it as a new testimony. The public route has made his action visible and kept the unknown part open.",
    giver="silas_vane"),
]

sealed = [
row("sealed_open", "A Copy for the Family to Review", "talk", "nella_pike",
    "Ask Nella what kind of private review would be useful without asking her to confirm what happened on the road.",
    "NELLA PIKE",
    ["I want one copy I can take to my aunt. She can decide whether the account belongs in our papers.", "Do not write her silence as agreement. A family needs room to answer in its own time."],
    "Review Belongs to the Family",
    "Nella requests a private copy for her aunt and sets the limits herself. She does not speak for every household on the road, and the copy does not ask her to validate the arrow's effect. The receipt records who may open the case and how the family can return or correct the page later.",
    giver="nella_pike"),
row("sealed_case", "Build a Case with a Changeable Seal", "inspect", "silas_arrow_family_case",
    "Inspect the review case. Verify that the seal can be opened by the named family holder and resealed without replacing the record.",
    "ROWAN HALE",
    ["The wax can be lifted from this edge without scraping away the mark.", "The opening will show whether the paper was handled; it will not reveal why."],
    "A Seal That Shows Its Own Opening",
    "The case uses a paper hinge and a wax mark split across its flap. A named holder can open it, and the split mark will show whether it was resealed. The design is not a lock against every hand. Its purpose is to make access visible and give the family a way to notice handling, not to claim perfect secrecy.",
    "sealed_case", (4.4, -3.6), giver="rowan_hale"),
row("sealed_silas", "Silas Accepts a Limited Copy", "talk", "silas_vane",
    "Ask Silas to prepare a copy of his account that keeps his action and the uncertain interval together.",
    "SILAS VANE",
    ["I will not send the family a clean page that hides the missing road.", "They should be able to see where my memory ends before they decide what to do with it."],
    "The Interval Travels with the Account",
    "Silas refuses to separate his admission from the limits of his view. The copy carries his full account, the field method and a clear gap for what neither his memory nor the surviving map can establish. The family may read it, return it or keep it private without adding a conclusion.",
    giver="silas_vane"),
row("sealed_ruth", "Ruth Adds the Dispatch Reference", "talk", "ruth_calder",
    "Ask Ruth to add a reference to the dispatch without including the family's private names or details.",
    "RUTH CALDER",
    ["The order is relevant because it sent Silas to that notch.", "I will list where the original is kept and what I did to hide it. The copy need not carry a roll call."],
    "The Source Is Named Separately",
    "Ruth writes the dispatch's archive location and records her own concealment in a separate attachment. The family copy can be checked against the original if they request it. Ruth leaves household names out because the order did not contain a reliable list of who reached the road.",
    giver="ruth_calder"),
row("sealed_public_method", "Publish the Method, Not the Family Copy", "inspect", "silas_arrow_method_notice",
    "Inspect the public method notice. Check that the steps are visible while the signed family copy remains inside its case.",
    "ROWAN HALE",
    ["Anyone can repeat the daylight check without reading a family's private page.", "The notice says where a family may ask for a private review."],
    "Method Outside, Copy Inside",
    "The public notice shows the line-of-sight procedure, the target positions and the limits of the daylight test. It contains no facsimile of Silas's family copy. A small line explains how relatives may request access through Nella. Public readers get the method; the family retains control over the named account.",
    "noticeboard", (-0.9, 3.8), giver="rowan_hale"),
row("sealed_review", "The Named Holder Opens the Case", "inspect", "silas_arrow_family_receipt",
    "Inspect the access receipt after Nella's aunt reviews the copy. Keep the review date and her response private.",
    "NELLA PIKE",
    ["She has read it. She asked for the page that shows where the firing place was.", "I can tell you what to retrieve without telling the road what she said about it."],
    "A Private Review with a Narrow Receipt",
    "Nella records that the named holder opened the case and requested the position map. The receipt stores neither her aunt's reaction nor a public summary of it. A later request can add a family-approved correction, but the family is not required to provide one for the archive to accept their review.",
    "sealed_case", (6.6, -2.8), giver="nella_pike"),
row("sealed_sign", "Silas Signs the Case Copy", "talk", "silas_vane",
    "Ask Silas to sign the account and the access limits before the family copy is sealed.",
    "SILAS VANE",
    ["I am accountable for the shot whether the paper is public or sealed.", "The seal controls who reads this copy. It does not control who owns the memory."],
    "Accountability Does Not Depend on an Audience",
    "Silas signs the family copy before it is sealed. He writes the same admission as in the public route and the same limit on what he could see. Choosing privacy changes who receives the page, not whether he accepts his action.",
    giver="silas_vane"),
row("sealed_seal", "Record the Seal's First Mark", "inspect", "silas_arrow_seal_record",
    "Inspect the case after sealing. Record the split-wax mark, named holder and return path for a future correction.",
    "ROWAN HALE",
    ["The mark crosses the flap once, from paper to wax and back again.", "We record how to reopen it so the record does not pretend to be unreachable."],
    "The First Seal and Its Return Path",
    "The seal record notes the split mark, the family holder and the route back through Nella. It does not call the case inaccessible forever. If the family asks to reopen it, another receipt can record that visit and keep the older seal entry intact.",
    "sealed_case", (3.2, -1.3), giver="rowan_hale"),
row("sealed_after", "The Family Copy Is Filed", "talk", "silas_vane",
    "Speak with Silas after the case is sealed. Confirm that the method remains public and the family keeps control of the named copy.",
    "SILAS VANE",
    ["I wanted a public answer when I was eighteen. I had not earned the right to demand one from others.", "The method can travel farther than a family's page."],
    "After the Case Is Filed",
    "Silas checks that the public method notice can be repeated and the family copy remains under Nella's agreed access rule. He admits that he once mistook a signal for a command with a single meaning. The sealed route keeps a family's answer private while still leaving a path for a future witness to correct the record.",
    giver="silas_vane"),
]

shared = [
row("daylight_repeat", "Repeat the Sightline in Clear Weather", "inspect", "silas_arrow_daylight_repeat",
    "Repeat the present-day sightline when the wind is low. Add the weather and viewing position beside the first trial.",
    "ROWAN HALE",
    ["The ridge looks the same, but the air does not.", "This second view tells us how one condition changes the range today, not what the old night looked like."],
    "Two Daylight Conditions",
    "On a lower-wind morning, Rowan repeats the sightline from the same notch. The far marker stays visible slightly longer, but dust and cloud differ from the first trial. Both entries remain in the record with their conditions. A second measurement narrows a question about present visibility; it does not reconstruct the weather from the old account.",
    "signal_vane", (-6.1, -1.4), giver="rowan_hale"),
row("nella_addendum", "Nella Leaves a Door for Later Witnesses", "talk", "nella_pike",
    "Ask Nella how a future witness can add a correction without being made to inherit the current account.",
    "NELLA PIKE",
    ["A witness can bring a place, a date or a separate account.", "Let them choose their words before anyone files them beside my family's blank."],
    "A Doorway for Later Accounts",
    "Nella agrees to a return slip for future witnesses. They may request a private conversation, provide a location or submit an account in their own words. The slip does not name a likely witness and does not presume that anyone will come forward. It simply keeps the archive open to another source.",
    giver="nella_pike"),
row("repeat_target", "A Second Mark beside the First", "inspect", "silas_arrow_repeat_target",
    "Inspect the target after a second known practice shot from the same notch. Keep both impacts and both sets of conditions visible.",
    "SILAS VANE",
    ["I fired this one today. Rowan watched from the lower path.", "Two marks show variation between known shots. They do not identify the old one."],
    "Known Variation on the Practice Target",
    "Silas makes a second practice shot under the recorded morning conditions. It lands beside the first, not on top of it. The spread is measured, and neither mark is used to back-calculate the old groove. Known variation makes the current experiment more useful while reminding the team how little a single impact can tell them.",
    "signal_mark", (7.6, 0.0)),
row("reed_copy", "Replace the Test Bundle", "harvest", "windglass_reed",
    "Harvest a second Windglass Reed bundle for the next inspection cycle. Label it with this season's date.",
    "SILAS VANE",
    ["This bundle bent differently after last night's salt mist.", "Keep it as a new sample. Do not replace the first entry with it."],
    "The Second Reed Bundle",
    "The second harvest has a different bend after an overnight salt mist. Rowan records the date, plot and soil dampness before putting it beside, not over, the first bundle. Samples that differ across seasons are useful only if their origin stays attached. The next person can compare the change without mistaking it for a correction to the old measurement.",
    giver="rowan_hale"),
row("public_or_case", "Check the Chosen Copy's Return Path", "inspect", "silas_arrow_return_path",
    "Inspect the route's correction slip and confirm how a public witness or the named family holder can submit a new account.",
    "ROWAN HALE",
    ["There are two return paths, and neither asks for a conclusion.", "A new account can be attached before anyone decides what it means."],
    "A Correction Can Arrive Without a Verdict",
    "The return slip offers a public correction pocket and a private request through Nella. It accepts observations, locations and account corrections without asking for a verdict. The chosen policy changes who handles a copy, but both versions preserve authorship and dates. The archive can receive new evidence without promising that it will erase the uncertainty.",
    "document", (-5.4, 0.3), giver="rowan_hale"),
row("afterword", "The Arrow Stays in Its Own Record", "talk", "silas_vane",
    "Speak with Silas after the correction path is filed. Confirm what he owns, what remains unknown and who may add evidence later.",
    "SILAS VANE",
    ["I fired the arrow. I can say that without claiming what every person did next.", "If the road's account grows, let it grow by adding voices, not by widening mine."],
    "A Record That Does Not Borrow Another Voice",
    "Silas's final entry names his action, the order he received, the limits of his view and the people whose accounts remain their own. One branch posts his statement with a correction pocket; the other keeps the named copy under family review while publishing the method. Both leave the missing interval intact and provide a route for future evidence to arrive without being pre-written.",
    giver="silas_vane"),
]

def make_quest(entry, prior=None, branch=None, choice=False, any_prior=None, reward_items=None):
    qid = "side_silas_arrow_" + entry["key"]
    did = "silas_arrow_" + entry["key"] + "_dialogue"
    objective = {
        "id": "silas_arrow_" + entry["key"] + "_objective",
        "kind": entry["kind"],
        "targetId": entry["target"],
        "requiredCount": 1,
        "description": entry["objective"],
        "dialogueId": did,
    }
    q = {
        "id": qid,
        "arcId": "the_salt_road",
        "stage": -1,
        "type": "side",
        "locationId": entry["location"],
        "giverId": entry["giver"],
        "title": entry["title"],
        "objective": entry["objective"],
        "objectives": [objective],
        "reward": {"gold": 4 if entry["key"] in {"open", "afterword"} else 2, "items": reward_items or []},
    }
    if prior:
        q["prerequisiteIds"] = [prior]
    if any_prior:
        q["prerequisiteGroups"] = [{"anyOfQuestIds": any_prior}]
    if branch:
        q["branchFlag"], q["branchValue"] = "silas_first_arrow_record_policy", branch
    if choice:
        q.update({
            "choiceFlag": "silas_first_arrow_record_policy",
            "choiceSpeaker": "SILAS VANE",
            "choicePrompt": "Choose where Silas's signed account will be read. Both routes keep the missing interval unresolved.",
            "choices": [
                {
                    "id": "public_account",
                    "label": "Post Silas's first-person account and the sightline method; leave family names off the board.",
                    "flagValue": "public_account",
                    "dialogueId": "silas_arrow_choice_public",
                    "reward": {"gold": 0, "items": [{"itemId": "silas_open_range_charm", "quantity": 1}]},
                },
                {
                    "id": "family_copy",
                    "label": "Give one named family holder a sealed copy; publish the repeatable method without the private page.",
                    "flagValue": "family_copy",
                    "dialogueId": "silas_arrow_choice_family",
                    "reward": {"gold": 0, "items": [{"itemId": "silas_family_margin_charm", "quantity": 1}]},
                },
            ],
        })
    return q

quests = []
dialogues = []
records = []
landmarks = []
sequence = []
for entry in common:
    prior = sequence[-1] if sequence else "side_nella_afterword"
    is_choice = entry["key"] == "policy"
    quest = make_quest(entry, prior=prior, choice=is_choice,
                       reward_items=([{"itemId": "windglass_reed_seed", "quantity": 2},
                                      {"itemId": "earthworm_bait", "quantity": 6}]
                                     if entry["key"] == "open" else None))
    quests.append(quest)
    sequence.append(quest["id"])
    dialogues.append({"id": "silas_arrow_" + entry["key"] + "_dialogue",
                      "speakerName": entry["speaker"], "lines": entry["lines"]})
    records.append({"id": "silas_arrow_" + entry["key"] + "_record",
                    "title": entry["record_title"], "category": "The Arrow Before the Answer",
                    "writtenBy": "Rowan Hale", "unlockQuestId": quest["id"],
                    "body": entry["record_body"]})
    if entry["key"] == "policy":
        dialogues.extend([
            {"id": "silas_arrow_choice_public", "speakerName": "SILAS VANE",
             "lines": ["Put my signed action where anyone can read it, with the blind bend on the same page.",
                       "Nella's family names stay off the board. The gap stays visible."]},
            {"id": "silas_arrow_choice_family", "speakerName": "SILAS VANE",
             "lines": ["Let the family decide whether to read the named copy. I will not make their answer public for them.",
                       "Keep the daylight method available to everyone, and the private account with its holder."]},
        ])
    if entry["kind"] == "inspect" and entry["visual"] and entry["position"] and entry["target"] != "salt_hunter_map":
        x, y = entry["position"]
        landmarks.append({
            "id": "silas_arrow_" + entry["key"] + "_marker",
            "locationId": entry["location"],
            "displayName": entry["title"],
            "targetId": entry["target"],
            "visualId": entry["visual"],
            "positionX": x, "positionY": y, "scale": 0.085,
        })

branch_endings = []
for branch, entries in (("public_account", public), ("family_copy", sealed)):
    previous = None
    for entry in entries:
        quest = make_quest(entry, prior=previous or "side_silas_arrow_policy", branch=branch)
        quests.append(quest)
        previous = quest["id"]
        dialogues.append({"id": "silas_arrow_" + entry["key"] + "_dialogue",
                          "speakerName": entry["speaker"], "lines": entry["lines"]})
        records.append({"id": "silas_arrow_" + entry["key"] + "_record",
                        "title": entry["record_title"], "category": "The Arrow Before the Answer",
                        "writtenBy": "Rowan Hale", "unlockQuestId": quest["id"],
                        "body": entry["record_body"]})
        if entry["kind"] == "inspect" and entry["visual"] and entry["position"]:
            x, y = entry["position"]
            landmarks.append({
                "id": "silas_arrow_" + entry["key"] + "_marker",
                "locationId": entry["location"],
                "displayName": entry["title"],
                "targetId": entry["target"],
                "visualId": entry["visual"],
                "positionX": x, "positionY": y, "scale": 0.085,
            })
    branch_endings.append(previous)

previous = None
for entry in shared:
    quest = make_quest(entry, prior=previous, any_prior=branch_endings if previous is None else None)
    quests.append(quest)
    previous = quest["id"]
    dialogues.append({"id": "silas_arrow_" + entry["key"] + "_dialogue",
                      "speakerName": entry["speaker"], "lines": entry["lines"]})
    records.append({"id": "silas_arrow_" + entry["key"] + "_record",
                    "title": entry["record_title"], "category": "The Arrow Before the Answer",
                    "writtenBy": "Rowan Hale", "unlockQuestId": quest["id"],
                    "body": entry["record_body"]})
    if entry["kind"] == "inspect" and entry["visual"] and entry["position"]:
        x, y = entry["position"]
        landmarks.append({
            "id": "silas_arrow_" + entry["key"] + "_marker",
            "locationId": entry["location"],
            "displayName": entry["title"],
            "targetId": entry["target"],
            "visualId": entry["visual"],
            "positionX": x, "positionY": y, "scale": 0.085,
        })

items = [
    {"id": "silas_windline_charm", "name": "Windline Bow Loop",
     "description": "A field charm made from a reed, a Saltspool Skate scale and Roadglass Filament. It keeps one sighting setup repeatable; it cannot recreate another night. Increases Might and Guard by 1.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
    {"id": "silas_open_range_charm", "name": "Open Range Pin",
     "description": "Silas's pin marks an account that can be read and corrected in public. It carries his action, not another traveler's name. Increases Might by 2.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 2, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "silas_family_margin_charm", "name": "Family Margin Seal",
     "description": "A split-mark seal leaves room for a named family holder to open or correct a private copy. Increases Guard by 2.",
     "category": "equipment", "equipmentSlot": "charm", "maxStack": 1,
     "attackBonus": 0, "guardBonus": 2, "healAmount": 0, "sellValue": 0},
]
recipe = {
    "id": "forge_silas_windline_charm",
    "displayName": "Forge the Windline Bow Loop",
    "stationId": "dawnkeep_forge",
    "discipline": "smithing",
    "outputItemId": "silas_windline_charm",
    "outputQuantity": 1,
    "ingredients": [
        {"itemId": "windglass_reed", "quantity": 1},
        {"itemId": "saltspool_skate", "quantity": 1},
        {"itemId": "roadglass_filament", "quantity": 1},
    ],
}
encounter = {
    "id": "saltroad_silas_arrow_sentinel",
    "monsterId": "roadglass_sentinel",
    "locationId": "salt_road",
    "positionX": 1.1, "positionY": 4.0,
    "requiredQuestId": "side_silas_arrow_sentinel",
    "blockedQuestId": "", "blockedDialogueId": "",
    "contributesToQuest": True,
    "defeatObjectiveTargetId": "roadglass_sentinel",
    "defeatDialogueId": "silas_arrow_sentinel_victory",
    "downDialogueId": "rowan_field_retreat",
    "reward": {"gold": 3, "items": [{"itemId": "roadglass_filament", "quantity": 1}]},
}
dialogues.append({
    "id": "silas_arrow_sentinel_victory", "speakerName": "SILAS VANE",
    "lines": ["The path is clear. The filament is from this Sentinel's nest, not the old arrow.",
              "Mark the material sample as recovered today and keep the battle outside the sightline record."],
})

for filename, additions in [
    ("prologue_quests.json", quests),
    ("dialogue_catalog.json", dialogues),
    ("codex_catalog.json", records),
    ("quest_landmarks.json", landmarks),
    ("item_catalog.json", items),
    ("recipe_catalog.json", [recipe]),
    ("encounter_catalog.json", [encounter]),
]:
    catalog = read(filename)
    upsert(catalog["entries"], additions)
    write(filename, catalog)

print(f"Installed {len(quests)} quests, {len(dialogues)} dialogue entries, {len(records)} field records, "
      f"{len(landmarks)} landmarks, {len(items)} items, one recipe and one gated encounter.")
