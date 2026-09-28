#!/usr/bin/env python3
"""Add Ruth Calder's playable missing-dispatch character arc to Ashen Oath."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"

def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def upsert(entries, additions):
    indexes = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)

# key, title, region, giver, kind, target, objective text, speaker, dialogue,
# codex title/body, visual icon, reward items
steps = [
("open","The Order Beneath the Axle","salt_road","ruth_calder","talk","ruth_calder",
 "Ruth Calder asks Rowan to examine the dispatch she hid before anyone turns it into a complete explanation for the caravan's retreat.","RUTH CALDER",
 ["I concealed an order in a wagon axle. I will not ask you to call that harmless, and I will not let one paper answer for every person who turned back.","Help me recover the whole dispatch. Nella and Silas remember different places; I want their accounts beside mine, not beneath it."],
 "Ruth's Admission","Ruth confirms that she hid a dispatch during the Salt Road retreat. She does not claim the hidden page explains every decision or every loss. The route begins with the sealed axle note, then compares it with Nella Pike's pass card and Silas Vane's signal sketch. The aim is to recover what the paper actually says, identify where each witness was standing and record what remains absent. Ruth accepts that concealment was her choice; the archive will not convert that admission into a verdict about the whole convoy.","",[{"itemId":"windglass_reed_seed","quantity":1},{"itemId":"earthworm_bait","quantity":3}]),
("margin","The Fold under the Axle Strap","salt_road","ruth_calder","inspect","ruth_axle_dispatch_margin",
 "Inspect the axle strap where Ruth folded the dispatch around a grease mark instead of placing it in the open route ledger.","ROWAN HALE",
 ["The fold runs through the date, not the destination. Someone opened the page after Ruth wrapped it, but the grease hides the order of those marks.","I can describe the crease and the smear. I cannot yet say who unfolded it or when."],
 "Dispatch Fold and Grease Mark","The dispatch was wrapped around the inner axle strap. A crease crosses the date line, while a dark grease mark covers part of the lower edge. The fold shows that the paper was carried inside the cart; it does not show who opened it later. Ruth recognizes the cord but cannot say whether another hand retied it. Rowan records the physical condition separately from her recollection. The date and destination remain partly legible, and neither has been compared with the other two witness records yet.","document",[]),
("nella","Nella's Pass Card","salt_road","nella_pike","talk","nella_pike",
 "Ask Nella Pike where she was when the caravan changed direction and what her pass card can establish.","NELLA PIKE",
 ["I was at the lower marker with the last walkers. The card proves I passed the checkpoint; it does not list everyone who was still behind me.","I will show you the edge where I wrote the bell count. Do not turn my route into a count of lives."],
 "Nella's Position at the Lower Marker","Nella places herself at the lower checkpoint when the caravan changed direction. Her pass card confirms her own passage and records a bell count in the margin. It does not list every traveler who remained on the road or prove what Ruth could see from the weigh station. Nella agrees to let Rowan copy the card's location and time while keeping her missing sister's name out of the public copy. Her testimony defines a boundary around what she witnessed rather than filling the blank for other people.","",[]),
("pass","The Card Edge with Two Notches","salt_road","rowan_hale","inspect","nella_pass_card_notches",
 "Read the two notches on Nella's pass card and compare their spacing with the posted toll-bell interval.","ROWAN HALE",
 ["The notches are close together, but the card has been trimmed and the toll clock was repaired afterward.","This can support Nella's remembered interval. It cannot synchronize her watch with Ruth's bell or Silas's arrow."],
 "Two Notches, No Shared Clock","Nella's card bears two shallow notches beside the checkpoint stamp. Their spacing resembles two quick bell strikes, but the card was trimmed and the toll clock was repaired decades later. No clock appears in the pass record. Rowan can compare the relative spacing with a known mark, not align it to an absolute time. The note preserves a useful local observation while refusing to turn an approximate rhythm into a precise sequence of events across the entire road.","waymarker",[]),
("skate","A Catch from the Sheltered Pool","salt_road","silas_vane","fish","saltspool_skate",
 "Catch a Saltspool Skate at the sheltered pool and keep its oily scale for the light test on Ruth's dispatch.","SILAS VANE",
 ["The scale leaves a thin sheen that can show which way a rubbed mark runs. It is a field aid, not a reagent that reveals hidden words by itself.","Catch one from the sheltered pool. We will test it on a spare strip before touching Ruth's page."],
 "Saltspool Scale for Directional Rubbing","A Saltspool Skate scale leaves a faint oily sheen when drawn across dry paper. Silas uses the sheen to compare stroke direction on a practice strip, not to make invisible writing appear. The scale cannot identify a writer, set a date or establish what the dispatch meant. Rowan records the pool and catch date so the sample is not confused with a scale kept from another trip. The test will be used only after a split-light plate has been prepared and checked on scrap material.","",[]),
("bell","The Toll Bell's Second Shell","salt_road","rowan_hale","inspect","ruth_toll_bell_shell",
 "Inspect the toll bell's inner shell and record which strike marks were made before the bracket was replaced.","ROWAN HALE",
 ["There are two sets of hammer marks. The newer bracket hid the lower set, but the rust crosses both rows.","The bell can preserve its own repair history. It cannot tell us whether a person heard it from the lower road."],
 "Repair Marks inside the Toll Bell","The toll bell's inner shell contains two rows of hammer marks. A replacement bracket covers part of the lower row, and rust crosses both groups. The marks show that the bell was repaired at least once; they do not establish the repair date or which strike could be heard from Nella's checkpoint. Rowan photographs the relative positions in the field log. The bell remains an object with a maintenance history, not a reliable clock shared by all three witnesses.","document",[]),
("guard","The Sentinel at the Cart Cut","salt_road","ruth_calder","defeat","roadglass_sentinel",
 "Defeat the Roadglass Sentinel guarding the cart cut so the team can recover the glass filament caught in its wheel casing.","RUTH CALDER",
 ["The Sentinel has dragged glass filament across the old wheel rut. Keep it away from the paper bundle; the edge can cut through a sleeve.","The cart cut is narrow. Wait for its marked rush to pass before crossing the rut."],
 "Roadglass Sentinel at the Cart Cut","The Roadglass Sentinel patrols the narrow cut below the toll station. Its marked rush follows the rut and can be evaded sideways when the warning line appears. A glass filament is lodged in its casing after the encounter. The material has a practical use in the assay lens, but the creature's presence does not explain why the old cart route was selected. Rowan keeps the combat note and the dispatch investigation as separate records.","",[]),
("filament","The Filament in the Casing","salt_road","ruth_calder","inspect","ruth_roadglass_filament",
 "Inspect the filament recovered from the Sentinel and check that it matches the fresh break on the practice lens frame.","ROWAN HALE",
 ["The filament's edge is fresh, but that only dates its contact with the Sentinel's casing relative to this break.","I will keep it with the encounter receipt, not use it to date a century-old page."],
 "Roadglass Filament Receipt","The recovered Roadglass filament has a clean break that fits a fracture on the practice frame. This confirms that it was caught there recently. It cannot date the older dispatch or show whether a glass tool was used to scrape the original ink. Talia's assay recipe uses a measured filament strand as part of the split-light plate. The receipt records where the material came from and prevents a new sample from being mistaken for a century-old trace.","sealed_case",[]),
("reed","Windglass Reed for the Plate","salt_road","rowan_hale","grow","windglass_reed",
 "Grow one Windglass Reed at the Salt Road plot to provide a measured fiber for the plate's frame.","RUTH CALDER",
 ["A single reed can brace the small test frame. The old dispatch will need a wider support so its fold does not carry the strain.","Record the planting and harvest. I will not call one plot proof that the ridge can supply every cart."],
 "Windglass Fiber and the Test Frame","One Windglass Reed was grown for the split-light plate's frame. The crop was harvested at the local Salt Road plot after its configured growth interval. A single reed can brace the test frame; it does not estimate how much material the ridge could supply to a caravan. Rowan records the seed, location and harvest together. Talia will compare this fiber with the Roadglass filament and the Saltspool scale before any part of the tool touches the dispatch.","",[]),
("lens","Talia's Split-Light Plate","cinderwell_basin","talia_mercer","craft","saltroad_beacon_lens",
 "Craft the Split-Light Plate at Cinderwell's assay bench using Windglass Reed, Saltspool scale and Roadglass filament.","TALIA MERCER",
 ["The plate divides one beam into two reference lines. It can expose a pressure difference on a test surface, but cannot authenticate the person who wrote it.","The ingredients have separate receipts. Use the assay bench and test the plate on scrap before you carry it back to Ruth."],
 "Split-Light Plate: Bench Test","Talia prepared the Split-Light Plate at the Cinderwell assay bench from one Windglass Reed, one Saltspool Skate and one Roadglass filament. Its two beams reveal small differences in raised ink when the paper is held at a fixed angle. A test on scrap shows that the plate works; it does not authenticate a writer or guarantee that every mark on an old page is original. The work order lists the ingredients and station so later reviewers can reproduce the same setup.","",[]),
("june","Sister June's Copy Rule","cinderwell_basin","sister_june","talk","sister_june",
 "Ask Sister June how she would preserve a corrected count without turning the correction into a new list of people owed an explanation.","SISTER JUNE",
 ["The correction should name the person who changed the record and keep the people named in the shipment from becoming cargo again.","I can witness the handoff, but I will not sign for the road or the decisions made there."],
 "Sister June's Copy Rule","Sister June recommends that a correction identify the person who changed the record while retaining the original page and its uncertainty. She will witness the transfer of copies but will not sign for events she did not see on the Salt Road. Her rule distinguishes custodianship from testimony. A corrected manifest can clarify the dispatch without claiming that every traveler was counted or that one signature explains why the caravan turned back.","",[]),
("lightbox","The Axle Copy under Split Light","salt_lockhouse","ruth_calder","interact","ruth_manifest_lightbox",
 "Fit the Split-Light Plate into the Lockhouse light box and illuminate the sealed axle copy without scraping the original.","RUTH CALDER",
 ["The raised line appears beside the route instruction. I can read the surviving words, but the last line breaks where the paper was torn.","Do not force the hinge. The plate must come out whole so a second keeper can repeat the exposure."],
 "Exposure without Scraping","The Split-Light Plate reveals a raised line beside the route instruction when mounted at the Lockhouse light box. The final line ends at a tear. No scraping or chemical wash was used, so the page remains available for another reading. Ruth recognizes the fold but does not claim to know when the raised mark was added. The exposure identifies a surviving physical feature; it does not determine who wrote the line, who read it or which witnesses saw the instruction before the retreat.","",[]),
("reverse","The Order's Torn Reverse","salt_lockhouse","rowan_hale","inspect","ruth_manifest_reverse",
 "Read the reverse of the exposed order and compare its torn edge with the separate toll receipt.","ROWAN HALE",
 ["The reverse carries a destination code and a request to return by third bell. The torn edge removes the initials and the reason.","That makes the order clearer and the chain of command less clear. We have to preserve both results."],
 "Reverse Text and Missing Initials","The reverse of the dispatch contains a destination code and a return instruction tied to the third bell. A tear removes the initials and the sentence explaining why the cart was to return. The toll receipt carries a matching code but no person or hour. The documents support a connection between the dispatch and the checkpoint; they do not show who authorized the instruction or whether it was issued before every traveler had arrived. Rowan records the strengthened link and the unresolved gap on the same page.","document",[]),
("silas","Silas Marks His Position","salt_road","silas_vane","talk","silas_vane",
 "Ask Silas Vane to mark the exact position from which he fired the first signal and what remained outside his view.","SILAS VANE",
 ["I fired from inside the weigh station, not the ridge. The ridge is where I said I stood because that sounded like a hunter's mistake instead of a choice.","I could see the gate and one cart. I could not see the lower road or the people beyond the bend."],
 "Silas's Revised Position","Silas places himself inside the weigh station when he fired the first signal. His earlier statement put him on the ridge. He explains that the first account felt easier to survive, but his present admission does not fill the views blocked by the station wall and road bend. Rowan keeps both statements with their dates. The revised position narrows what Silas could have observed; it does not prove that the signal caused the retreat or that he knew who remained out of sight.","",[]),
("signal","The Sighting Gap on the Sketch","salt_road","rowan_hale","inspect","silas_signal_sightline_gap",
 "Inspect Silas's sketch and mark the section of the lower road hidden behind the weigh station wall.","ROWAN HALE",
 ["The wall blocks the bend until someone reaches the gate. The signal could travel farther than Silas's view.","I am marking an absence in the sightline, not claiming the road was empty."],
 "Sightline Is Not a Headcount","The weigh station wall blocks Silas's view of the lower bend. A signal could travel farther than the person who fired it could see. The sketch marks the obstruction and the approximate gate position, but it is not a surveyed map. Rowan adds a note that the hidden stretch cannot be treated as empty merely because Silas did not see it. This correction limits the testimony without replacing it with an invented count of travelers.","waymarker",[]),
("ruth","Ruth Names Her Part","salt_road","ruth_calder","talk","ruth_calder",
 "Ask Ruth what she chose to do with the dispatch after she discovered its reverse-side instruction.","RUTH CALDER",
 ["I kept the paper from the common ledger. I told myself I was preserving the only readable copy, but I also kept the others from seeing it.","I accept that concealment. I still cannot tell you which people were past the bend when the order was followed."],
 "Ruth's Responsibility and Its Limit","Ruth acknowledges that she removed the dispatch from the common ledger and concealed it. She describes preservation as one reason, but admits that the choice also prevented others from examining the page. Her account does not establish how many travelers were beyond the bend or what each person knew. The archive keeps her responsibility beside its limit: she can answer for hiding the paper, while the missing initials, torn sentence and blocked sightline remain unresolved.","",[]),
("policy","Who Signs the Correction?","salt_road","ruth_calder","choice","ruth_manifest_account",
 "Choose who signs the correction first: Ruth, who hid the order, or Nella, who witnessed the lower checkpoint while Ruth signs only her own action.","RUTH CALDER",
 ["I can sign first and state plainly that I hid the dispatch. Or Nella can sign only the part she witnessed, while I sign the concealment separately.","Do not make her confirm the road from my window. The order needs more than one line because we did not stand in one place."],
 "Signing Scope Decision","The correction needs a signature for Ruth's concealment and a distinct boundary around Nella's checkpoint testimony. One policy places Ruth's acknowledgment first so readers meet the act before its explanation. The other lets Nella countersign only the location and bell interval she witnessed, while Ruth signs a separate statement about hiding the dispatch. Both options preserve the original, identify who changed the record and leave the torn reason and unseen road unresolved.","",[]),
("ruth_sign","Ruth Signs First","salt_road","ruth_calder","inspect","ruth_signed_addendum",
 "Inspect the addendum Ruth signed first, confirming that it names her concealment and leaves the missing route explanation unresolved.","RUTH CALDER",
 ["My name is on the first line, before the reason I kept the paper. I will not ask you to put the torn reason back with guesswork.","Keep the old dispatch attached. The correction is an addition, not a replacement for what I did."],
 "Ruth's Signed Addendum","The first line of the addendum records Ruth's choice to hide the dispatch from the shared ledger. A second line states that she cannot verify who was beyond the bend when the order was followed. The page remains attached to the original rather than overwriting it. This arrangement makes responsibility immediately visible, though readers may focus on Ruth before considering the limited evidence about the convoy. The addendum has a dated space for later correction and does not speak for Nella.","noticeboard",[]),
("joint_sign","Nella Countersigns Her View","salt_road","nella_pike","inspect","nella_joint_witness_copy",
 "Inspect the joint copy and confirm that Nella signs only her location and Ruth signs only the concealment she admitted.","NELLA PIKE",
 ["My signature stays beside the checkpoint and bell count. Ruth's belongs beside the page she hid.","The two signatures do not make one of us a witness to the other's view. Leave the spaces between them."],
 "Joint Copy with Bounded Witnesses","Nella's signature appears beside her checkpoint position and remembered bell interval. Ruth's signature appears beside her admission that she hid the page. The copy does not merge their testimony or imply that either witnessed the entire road. This format protects the difference between the two accounts, but readers may miss Ruth's responsibility if they skim the second section. Both sections point to the original dispatch and retain a date for review.","sealed_case",[]),
("afterword","A Ledger Can Hold Two Boundaries","salt_road","ruth_calder","talk","ruth_calder",
 "Speak with Ruth after the selected correction is filed and agree to keep the original, the signed account and the missing interval together.","RUTH CALDER",
 ["The page now shows what I did, what Nella saw and what neither of us can fill in. It does not make the road less painful.","If another witness is found, we can add their statement without asking them to inherit our words."],
 "Afterword: The Road Remains Open","The filed correction preserves Ruth's admission, Nella's bounded witness account and Silas's revised signal position. The papers now describe more than before, but they do not identify every traveler or settle the outcome of the retreat. Ellis Porter's name remains absent from the manifest; that absence cannot establish whether he reached the road by another route. Ruth keeps the ledger open for another witness and dates the next review. The two signing policies remain distinct in the codex so later readers can see who accepted responsibility and who described a place.","",[]),
]
assert len(steps)==20
quests=[]; dialogues=[]; codex=[]; landmarks=[]
position_by_location={"salt_road":0,"cinderwell_basin":0,"salt_lockhouse":0}
positions={
 "salt_road":[(-8.6,2.7),(-4.8,-3.7),(0.0,3.6),(8.6,-3.4),(4.1,2.9),(-7.0,-2.7),(5.7,3.2)],
 "cinderwell_basin":[(-5.6,2.2),(5.6,-2.4)],
 "salt_lockhouse":[(-4.6,2.8),(4.5,-2.9)]
}
for i,row in enumerate(steps):
 (key,title,location,giver,kind,target,objective,speaker,lines,record_title,body,visual,reward_items)=row
 qid="side_ruth_recall_"+key
 dialogue_id="ruth_recall_"+key
 prerequisite="salt_route_handoff" if i==0 else "side_ruth_recall_"+steps[i-1][0]
 quest={"id":qid,"arcId":"the_salt_road","stage":-1,"type":"side","locationId":location,
        "giverId":giver,"title":title,"objective":objective,"prerequisiteIds":[prerequisite],
        "objectives":[{"id":"resolve_"+key,"kind":kind,"targetId":target,"requiredCount":1,
                       "description":objective,"dialogueId":dialogue_id}],
        "reward":{"gold":7 if kind in ("talk","choice") else 5,"items":reward_items}}
 if key=="policy":
  quest["choiceFlag"]="ruth_manifest_account"
  quest["choiceSpeaker"]="RUTH CALDER"
  quest["choicePrompt"]="Who should sign first, and exactly which part of the account can each person attest to?"
  quest["choices"]=[
   {"id":"ruth_signs_first","label":"Ruth signs first and records her concealment before her explanation.",
    "flagValue":"ruth_signs_first","dialogueId":"ruth_recall_choice_ruth",
    "reward":{"gold":0,"items":[{"itemId":"ruth_signed_keel_charm","quantity":1}]}},
   {"id":"nella_countersigns","label":"Nella countersigns only her checkpoint account; Ruth signs the concealment separately.",
    "flagValue":"nella_countersigns","dialogueId":"ruth_recall_choice_joint",
    "reward":{"gold":0,"items":[{"itemId":"nella_boundary_knot","quantity":1}]}}
  ]
 if key=="ruth_sign":
  quest["branchFlag"]="ruth_manifest_account";quest["branchValue"]="ruth_signs_first"
  quest["prerequisiteIds"]=["side_ruth_recall_policy"]
 if key=="joint_sign":
  quest["branchFlag"]="ruth_manifest_account";quest["branchValue"]="nella_countersigns"
  quest["prerequisiteIds"]=["side_ruth_recall_policy"]
 if key=="afterword":
  quest.pop("prerequisiteIds")
  quest["prerequisiteGroups"]=[{"anyOfQuestIds":["side_ruth_recall_ruth_sign","side_ruth_recall_joint_sign"]}]
 quests.append(quest)
 dialogues.append({"id":dialogue_id,"speakerName":speaker,"lines":lines})
 codex.append({"id":"ruth_recall_"+key+"_record","title":record_title,
               "category":"The Recalled Order","writtenBy":speaker.title(),"unlockQuestId":qid,"body":body})
 if visual:
  idx=position_by_location[location];pos=positions[location][idx%len(positions[location])];position_by_location[location]+=1
  landmarks.append({"id":"ruth_recall_"+key+"_marker","locationId":location,"displayName":title[:58],
                    "targetId":target,"visualId":visual,"positionX":pos[0],"positionY":pos[1],"scale":0.085})

# This objective consumes the crafted plate, so it needs its own authored world actor.
landmarks.append({"id":"ruth_manifest_lightbox_marker","locationId":"salt_lockhouse",
                  "displayName":"Axle Copy Light Box","targetId":"ruth_manifest_lightbox",
                  "visualId":"document","positionX":2.1,"positionY":3.5,"scale":0.09})

dialogues.extend([
 {"id":"ruth_recall_choice_ruth","speakerName":"RUTH CALDER","lines":[
  "I sign first. Put the fact that I hid the dispatch before my reason for keeping it.",
  "The reason belongs in the record too, but it does not cancel the choice." ]},
 {"id":"ruth_recall_choice_joint","speakerName":"NELLA PIKE","lines":[
  "I countersign the checkpoint and bell interval that I witnessed. Ruth signs her own action on the facing page.",
  "Leave the gap between the statements. It shows where our knowledge stops." ]},
 {"id":"ruth_recall_guard_down","speakerName":"ROWAN HALE","lines":[
  "The Roadglass Sentinel is down. Its casing holds one fresh filament strand; I have logged the encounter separately from the dispatch evidence.",
  "The cart cut is open. We can recover the sample without treating the creature as an answer to the old route." ]},
 {"id":"ruth_recall_guard_player_down","speakerName":"ROWAN HALE","lines":[
  "That strike knocked us down before we could reach the casing. The Sentinel still guards the cut.",
  "Catch your breath and reset our footing. The dispatch evidence is safe, and we can attempt the crossing again." ]}
])
items=[
 {"id":"ruth_signed_keel_charm","name":"Signed Keel Charm","description":"A caravan-keel token paired with Ruth's first-line admission. It carries weight without replacing the original dispatch.","category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":0,"guardBonus":2,"healAmount":0,"sellValue":0},
 {"id":"nella_boundary_knot","name":"Witness Boundary Knot","description":"A route-knot tied only to the checkpoint and bell interval Nella witnessed. It keeps a witness account beside, not inside, another person's decision.","category":"equipment","equipmentSlot":"charm","maxStack":1,"attackBonus":1,"guardBonus":1,"healAmount":0,"sellValue":0}
]
encounters=[{"id":"saltroad_ruth_cart_guard","monsterId":"roadglass_sentinel","locationId":"salt_road","positionX":7.2,"positionY":-1.5,
 "requiredQuestId":"side_ruth_recall_guard","blockedQuestId":"","blockedDialogueId":"","contributesToQuest":True,
 "defeatObjectiveTargetId":"roadglass_sentinel","defeatDialogueId":"ruth_recall_guard_down","downDialogueId":"ruth_recall_guard_player_down",
 "reward":{"gold":0,"items":[{"itemId":"roadglass_filament","quantity":1}]}}]
for filename,additions in [("prologue_quests.json",quests),("dialogue_catalog.json",dialogues),
                           ("codex_catalog.json",codex),("quest_landmarks.json",landmarks),
                           ("item_catalog.json",items),("encounter_catalog.json",encounters)]:
 catalog=read(filename)
 if filename=="quest_landmarks.json":
  catalog["entries"]=[entry for entry in catalog["entries"]
                      if entry.get("id")!="ruth_recall_afterword_marker"]
 upsert(catalog["entries"],additions);write(filename,catalog)
print(f"Installed {len(quests)} Ruth Calder quests, {len(dialogues)} dialogue scenes, {len(codex)} records, {len(landmarks)} landmarks, {len(items)} charms and {len(encounters)} encounter.")
