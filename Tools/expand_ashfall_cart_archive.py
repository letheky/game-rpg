#!/usr/bin/env python3
"""Add post-repair field notes to Gideon Park's Ashfall cart codices."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "codex_catalog.json"
MARKER = "\n\nSupplemental Ashfall cart note —"

NOTES = {
    "ashfall_cart_offer_record": """Supplemental Ashfall cart note — a useful object can be offered back

Gideon wipes the dust from the cart handle before he asks Rowan to take it. The gesture is half habit and half apology: he has kept the broken frame under a tarp while the rest of the village decided what could be salvaged. Mira says the frame has value only if someone can safely use it, but she does not call that a reason to give it to the loudest household. Gideon wants the first repair decision recorded as a question put to the people who may depend on the road. Rowan writes that the cart is being assessed for shared use. No one signs away ownership of every tool they may later contribute.""",
    "ashfall_cart_wheel_record": """Supplemental Ashfall cart note — chalk the crack before the wheel turns

Tomas asks Gideon to mark both ends of the split hub with chalk while the wheel is still on its stand. After Rowan rotates it by hand, the line at the lower end looks wider, though the light has also shifted across the rim. They stop the wheel and make a second mark from the same angle. Gideon admits that he once heard a knock in this hub and kept using the cart because it was the only one near the shelter. The record preserves that recollection without assigning the crack to that day. The wheel stays off the road until the new pin is fitted and a separate inspection can begin.""",
    "ashfall_cart_medicine_record": """Supplemental Ashfall cart note — the medicine load is a route question

Mira arranges empty bottles inside a cloth wrap and asks Rowan to walk the proposed path before anyone loads medicine. The lower rut tilts the tray toward the wheel; a higher shelf keeps the bottles level but adds time and one tight turn. She asks the person carrying the kit which route they would choose, rather than deciding that speed matters most. The test uses empty glass, not a patient or a real dose. Mira writes down where the wrap was tied and which turn felt difficult to manage. A cart may carry a dry load along one path and still need a different arrangement for another trip.""",
    "ashfall_cart_rut_record": """Supplemental Ashfall cart note — keep the shallow turn visible on the map

The narrow track bends around a low stone where a footpath joins the road. Gideon used to cut the corner when the cart was empty. Now he walks the arc slowly with Rowan and notices that the outer wheel leaves the firm ground sooner than the inner one. They mark the shallow path and the wider detour separately. Mira asks them to keep the footpath clear for people moving between the well and shelter. The new map does not claim that every traveler can use either route in the rain. It records where a cart can turn today, so a future repair crew can ask who else needs room before widening the road.""",
    "ashfall_cart_clear_record": """Supplemental Ashfall cart note — clear the road after the fight as well

The Ash Goblin retreats beneath the cart shed, and Rowan draws it away before striking. Gideon stays beside the frame, ready to pull the tarp free if a loose board falls. After the fight, they find one bent strip of iron under the wheel and a smear of mud on the ground; neither shows whether the creature brought the strip there or moved it while hiding. Rowan stores the iron with the salvage but leaves the mud undisturbed until Gideon has checked the wheel stand. The encounter ends when the path is safe to approach, not when the last hit lands. The repair notes separate what the team recovered from what it only noticed.""",
    "ashfall_cart_salvage_record": """Supplemental Ashfall cart note — let the owner review the scrap pile

Gideon places the straight iron on a board beside the two cracked spokes and asks Rowan not to carry anything away yet. He recognizes the pale stripe on one piece as a mark he used when the cart was repaired years ago, but the stripe could have been copied from another workshop. Tomas takes measurements in Gideon's presence and gives each item back before deciding what can be used. The surviving pieces belong to the cart's repair history even if none is safe to install. They record which material was inspected and which was rejected. Salvage becomes a part only after someone checks its condition and the person who brought it in agrees to the proposed use.""",
    "ashfall_cart_measure_record": """Supplemental Ashfall cart note — repeat the turn after the road dries

Gideon remembers steering this frame through the eastern lane before the raid, when the path was covered in frost. Rowan's trial takes place on dry earth, so they mark a second pass for the next morning if the ground remains firm. The turning arc can change when mud softens the shoulder or when a wheel slips. They set a walking pace and keep the cart empty; a fast turn could hide the moment the hub shifts. Gideon watches the outer wheel while Rowan guides the handle, then they trade places. Their impressions differ at the tight corner. Both are written down so a later test can repeat the same roles or deliberately compare them.""",
    "ashfall_cart_tomas_record": """Supplemental Ashfall cart note — the shoulder pin follows the tested edge

Tomas sets the old pin beside the cracked hub and measures the shoulder twice before heating a new blank. He explains that adding another bore would remove wood from the narrowest part of the rim. Gideon wants the repair finished before the next supply run, but agrees to wait while Tomas cuts the pin to the recorded fit. The forge card names the iron source, jaw setting and bench used, then leaves a blank for the next inspection. Rowan watches Tomas reject one rough blank with a shallow seam. It could be straightened, but the seam would sit where the cart carries its turning force. Speed cannot make an uncertain piece part of the repair.""",
    "ashfall_cart_spokes_record": """Supplemental Ashfall cart note — the spoke measures distance, then goes back to storage

Rowan holds the cracked spoke against the metal rule while Tomas checks the gap at the hub. They mark the measurement on a card rather than carving it into the wood, which is already split near its head. The spoke returns to Gideon's salvage tray once the forge has its note. Mira asks that the tray stay apart from usable repair stock so someone searching for parts does not mistake the broken wood for a ready replacement. It remains a gauge sample, not a component. The card adds where the rule touched and which end of the spoke faced the rim. A future maker can use a new piece to repeat the measurement without forcing this one back into the cart.""",
    "ashfall_cart_forge_record": """Supplemental Ashfall cart note — record the pin's cooling place

Tomas lets the forged pin cool on a marked stone separate from the scraps waiting for inspection. He measures its shoulder after cooling and again after it has rested through one forge watch. The second mark is close, but he keeps both readings rather than calling the first an error. The pin is stamped with the date and a tiny workshop sign that identifies its maker, not the cart's owner. Gideon asks to keep the sign small enough that it will not catch the cloth wrap. The tool card travels with the part until installation. If the pin later needs removal, another smith can see what was fitted and how Tomas checked it.""",
    "ashfall_cart_return_record": """Supplemental Ashfall cart note — bring back the measuring rule too

Rowan returns the pin, the calibration card and Tomas's metal rule together. Gideon checks the card before touching the cart and notices that the spoke used as a gauge is not in the bundle. Rowan retrieves it from the forge tray and marks it “broken sample” so it cannot be mistaken for spare stock. Tomas asks for the rule back after installation, because the next inspection must use the same tool or record that a different one was used. The handoff includes more than the finished part: it preserves the path by which the part was measured. Gideon files the card with the cart papers instead of leaving it loose on the workbench.""",
    "ashfall_cart_install_record": """Supplemental Ashfall cart note — turn the wheel without a crowd around it

Before the wheel is lowered, Gideon asks the onlookers to step back from the stand. Rowan seats the pin, checks that the shoulder rests outside the iron ring and turns the wheel slowly by hand. It completes one circle without scraping. Tomas watches the mark on the hub, while Mira checks that no cloth has caught near the spokes. The test is quiet and brief. Gideon wants to celebrate by pushing the cart at once; Rowan points to the next inspection card. The repair is now installed, but a wheel that turns freely in the air has not yet carried anyone or anything on the road.""",
    "ashfall_cart_test_record": """Supplemental Ashfall cart note — stop at the marker, not at the rut

The empty cart rolls along the chalked strip and stops at the short marker Rowan placed before the deep rut. Gideon checks the pin, then walks back to the start to see whether the wheel left a new track. They find one shallow groove at the turn and no visible change at the hub. Mira asks that the cart remain empty until she has reviewed how a wrapped bottle sits in its tray. No one asks a villager to ride along as proof. The trial establishes that this frame moved across a short dry path under hand control. A different surface, a slope or a full load requires a different review.""",
    "ashfall_cart_load_record": """Supplemental Ashfall cart note — tie the marker where a carrier can reach it

Mira ties the cloth knot low on the inside rail, where a person standing beside the cart can loosen it without lifting the tray. The knot marks the test position for an empty medicine wrap; it does not reserve that place for a named patient. Rowan walks the cart over the short dry strip and the bottles remain still. They do not fill the bottles with water to imitate a dose, because a liquid load would shift differently and could spill. Mira adds a second position for a soft blanket bundle and leaves the choice of which arrangement to use to the carrier. The marker is an invitation to check, not a label for a person.""",
    "ashfall_cart_policy_record": """Supplemental Ashfall cart note — compare the upkeep each choice asks of people

At the shelter table, Gideon lays out a board for a shared parking bay and a small case for household repair kits. The shared cart needs a schedule, a clear return point and someone able to inspect the pin. The kits need a stock count, a place to ask questions and a rule for replacing parts that wear out. Mira asks who would be able to refuse each arrangement without losing access to the road. Rowan records the answers separately rather than ranking the two options as generous or selfish. The choice decides which upkeep the village will try first. It does not make every household responsible for pulling a cart or keeping a forge tool.""",
    "ashfall_cart_communal_bay_record": """Supplemental Ashfall cart note — leave a clear line from the bay to the well

Gideon marks the proposed bay outside the shelter door, then Mira asks him to move it away from the shortest path to the well. A cart parked there would force people carrying water to step into the wheel rut. Rowan walks the new route with an empty basket and checks that the handle can turn without striking the stone post. They keep a chalk space at the entrance for temporary unloading, but do not call it a permanent storage place. The shared bay works only if its use does not block another daily route. The map shows the bay, the well path and the turning arc on separate lines so later residents can revise the position.""",
    "ashfall_cart_communal_turn_record": """Supplemental Ashfall cart note — the chalk arc can be erased and drawn again

After the first turn, rain breaks the chalk line at the outer wheel. Rowan redraws it from the same starting mark and writes that the second trial followed a shower, while the ground still looked firm. Gideon notices the wheel has cut a little deeper near the gate. They do not average the first and second arcs; one was traced on dry soil and one on damp soil. A shared bay needs space for the cart as it turns, but its boundary should not claim more ground than the village can keep clear. The chalk can be moved after another trial. The record leaves a note for whoever has permission to change it.""",
    "ashfall_cart_communal_report_record": """Supplemental Ashfall cart note — a missed handoff does not name a culprit

The first shared schedule leaves a gap at dusk when the gate watch changes. The cart stands at the bay after the expected return time, so Gideon asks if anyone knows who last used it. Rowan adds an “unconfirmed return” mark and checks the wheel instead of copying a name from the duty board. The cart is intact, and a neighbor brings it back after the well path clears. They add a wider handoff window for the next week. The incident shows that the schedule needs room for delays; it does not prove anyone broke an agreement. Users can report a change of plan without defending themselves before taking the cart again.""",
    "ashfall_cart_household_kits_record": """Supplemental Ashfall cart note — count each kit before handing it over

Mira lays one repair kit on a dry cloth: a measuring gauge, a checked pin and a short instruction card. The kit cannot straighten a bent frame or replace Tomas's forge work. Gideon asks that the parts be counted at return, since a missing pin may mean it was used to keep a wheel from failing on the road. The card says where to bring a damaged tool and how to request a replacement without explaining a household's need in public. Mira tracks stock by item and condition, not by the names of people who borrowed it. A small case can make one repair easier, but it is not an emergency service for every broken cart.""",
    "ashfall_cart_household_test_record": """Supplemental Ashfall cart note — test the pin on the stand again after travel

The kit returns from the far lane with the pin still in its wrap. Mira places the matching wheel on the stand and asks Rowan to compare it with the original fit mark. The pin seats cleanly, but the stand holds the wheel at a different angle than the cart frame did. Gideon suggests adding that limitation to the instruction card. They run the check once more with the stand level and record both setups. The trial helps a household notice a loose pin before a trip; it cannot certify a repaired cart or teach every person to judge a cracked hub. People can bring the part back to the forge when the check raises a question.""",
    "ashfall_cart_household_report_record": """Supplemental Ashfall cart note — stock numbers can change without a borrower list

Gideon counts two pins in the case and writes the total on the shelf card. One kit is out for inspection, but Mira leaves its borrower field blank because the village only needs to know that the tool has not returned yet. When the kit comes back, the count changes and the shelf card is updated. A private request can be made at the medicine table if the person wants help finding a part. Nobody has to explain their route or cargo to receive a measuring tool. The stock record answers how many parts remain; it does not describe who owns a cart or who has asked for assistance.""",
    "ashfall_cart_afterword_record": """Supplemental Ashfall cart note — keep the road open to a different repair

At the end of the route, Gideon takes the cart down the lane without cargo and stops at the gate to listen for the old knock. It does not return on this pass. He leaves the pin card beside the tool case, not attached permanently to the frame, so a future repairer can replace it and keep the earlier record. Rowan writes that the village chose a shared bay or voluntary kits for the current season. Neither choice prevents residents from asking to try the other later. The road has one repaired cart, a tested short path and a way to request another inspection. Its next use belongs to the people who decide to travel it.""",
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    records = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(NOTES) - set(records))
    if missing:
        raise SystemExit(f"Missing codex records: {', '.join(missing)}")
    changed = 0
    added_words = 0
    for record_id, note in NOTES.items():
        record = records[record_id]
        if MARKER.strip() in record.get("body", ""):
            continue
        record["body"] = record.get("body", "").rstrip() + MARKER + note
        added_words += len(note.split())
        changed += 1
    if changed:
        CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {changed} Ashfall cart codices; added {added_words} authored words.")


if __name__ == "__main__":
    main()
