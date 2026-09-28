#!/usr/bin/env python3
"""Import the CC0 Basic Green monster set as the Verdant Memory field arc."""

import hashlib
import json
import re
import zipfile
from pathlib import Path

from import_tiny_creatures_fieldbook import ART, CONTENT, REGIONS, ROOT, read_catalog, write_catalog

ARCHIVES = {
    "early": ROOT / "Docs/AssetArchives/basic-green-monsters-batch-1-3.zip",
    "middle": ROOT / "Docs/AssetArchives/basic-green-monsters-batch-4-6.zip",
    "late": ROOT / "Docs/AssetArchives/basic-green-monsters-batch-7-9.zip",
}

# (archive, path prefix, filename, singular field signature)
CREATURES = [
    ("early", "Basic Green Monster Colection/", "Bat.png", "A thin membrane catches the warm air above the well."),
    ("early", "Basic Green Monster Colection/", "Bee.png", "Pollen clings to the legs in colors absent from Ashfall's flowers."),
    ("early", "Basic Green Monster Colection/", "Centaur.png", "Four hoof marks circle the same patch without crossing it."),
    ("early", "Basic Green Monster Colection/", "Death Mage Elf.png", "A blue flame dims when the old drill bell rings."),
    ("early", "Basic Green Monster Colection/", "Death-Cob.png", "The web is stitched between stones with no anchor thread."),
    ("early", "Basic Green Monster Colection/", "Dragoon.png", "A split pennant bears colors missing from every Order banner."),
    ("early", "Basic Green Monster Colection/", "Ghost.png", "Dust falls through the silhouette but collects at its feet."),
    ("early", "Basic Green Monster Colection/", "Goblin.png", "Small boot-shaped impressions stop neatly before the well rim."),
    ("early", "Basic Green Monster Colection/", "Hell Knight.png", "The soot on its armor stays cool after the charge."),
    ("early", "Basic Green Monster Colection/", "Naga Mage.png", "A waterline curls upward along the stone beside it."),
    ("early", "Basic Green Monster Colection/", "Naga.png", "Its track leaves a dry spiral across recently wetted clay."),
    ("early", "Basic Green Monster Colection/", "Shadow.png", "The shadow points away from the lantern that casts it."),
    ("early", "Basic Green Monster Colection/", "Soul-Eater.png", "A ring of seed husks remains untouched around the site."),
    ("early", "Basic Green Monster Colection/", "Spectral-Warrior.png", "Its stance matches a drill diagram no cadet recognizes."),
    ("early", "Basic Green Monster Colection/", "Vault Guard.png", "A square print appears where the floor has no dust."),
    ("early", "Basic Green Monster Colection/", "Worm.png", "The soil tunnel bends away from every visible root."),
    ("early", "Basic Green Monster Colection/", "Wraith.png", "A cold patch holds its outline for three measured breaths."),
    ("early", "Basic Green Monster Colection/", "Yaktaur.png", "A broken shaft is wedged through a fence from outside."),
    ("middle", "Batch 4-6/PNG/", "Anaconda.png", "Two crossing coils press furrows into otherwise dry silt."),
    ("middle", "Batch 4-6/PNG/", "Big Fish.png", "Its gills pulse in air but the scales stay damp."),
    ("middle", "Batch 4-6/PNG/", "Dragon.png", "A soot spiral on the wing repeats at measured intervals."),
    ("middle", "Batch 4-6/PNG/", "Earth Worm.png", "A line of fresh earth ends at unbroken cistern stone."),
    ("middle", "Batch 4-6/PNG/", "Frog.png", "Its toe marks circle the shallow basin clockwise."),
    ("middle", "Batch 4-6/PNG/", "Giant Bat.png", "The membrane folds along a pattern like a folded map."),
    ("middle", "Batch 4-6/PNG/", "Giant Beetle.png", "A glassy scrape runs across the shell but not the floor."),
    ("middle", "Batch 4-6/PNG/", "Gold Fish.png", "Bright scales reflect a ceiling lamp that is not present."),
    ("middle", "Batch 4-6/PNG/", "Griffin.png", "Feathers and fur lie together without a visible molt."),
    ("middle", "Batch 4-6/PNG/", "High Priest Elf.png", "A pale mark on its robe resembles no local chapel seal."),
    ("middle", "Batch 4-6/PNG/", "Jelly Fish.png", "A clear bell shape leaves a salt ring above water level."),
    ("middle", "Batch 4-6/PNG/", "Killer Bee.png", "One dark pollen grain stays fixed inside a translucent wing."),
    ("middle", "Batch 4-6/PNG/", "Killer Klown.png", "Paint flakes settle in alternating bands around its footprints."),
    ("middle", "Batch 4-6/PNG/", "Manticore.png", "A loose spine is cleanly snapped rather than torn away."),
    ("middle", "Batch 4-6/PNG/", "Mosquito.png", "A needle-thin shadow reaches farther than the body."),
    ("middle", "Batch 4-6/PNG/", "Turtle.png", "The shell carries parallel grooves with no matching rock."),
    ("middle", "Batch 4-6/PNG/", "Wizard Orc.png", "Chalk dust collects inside its sleeves, away from the wall."),
    ("middle", "Batch 4-6/PNG/", "Wolf Spider.png", "Eight fine lines converge under a stone nobody moved."),
    ("late", "Batch 7-9/PNG/", "Abomination 1.png", "Its outline changes between the two lantern positions."),
    ("late", "Batch 7-9/PNG/", "Abomination 2.png", "A second shadow trails the body by half a heartbeat."),
    ("late", "Batch 7-9/PNG/", "Abomination 3.png", "Three incompatible tracks share one narrow patch of dust."),
    ("late", "Batch 7-9/PNG/", "Acid Blob.png", "A green bead eats no metal but clouds clean water."),
    ("late", "Batch 7-9/PNG/", "Apis.png", "The wingbeat repeats exactly when the cistern bell is struck."),
    ("late", "Batch 7-9/PNG/", "Chaos Spawn.png", "Its resting shape differs in each charcoal sketch."),
    ("late", "Batch 7-9/PNG/", "Chinese Dragon.png", "Clouded scales hold a faint stripe after the light moves."),
    ("late", "Batch 7-9/PNG/", "Hellwing.png", "The wing shadow crosses the ground before the wing does."),
    ("late", "Batch 7-9/PNG/", "Lorocyproca.png", "A narrow trail turns sharply where no doorway exists."),
    ("late", "Batch 7-9/PNG/", "Maurice.png", "Its hand leaves a dry print on the wet glass."),
    ("late", "Batch 7-9/PNG/", "Orphan.png", "A small empty nest remains warm beside its path."),
    ("late", "Batch 7-9/PNG/", "Reaper.png", "The floor keeps a straight scratch where no blade fell."),
    ("late", "Batch 7-9/PNG/", "Rotting Devil.png", "The scent fades at the threshold rather than at the body."),
    ("late", "Batch 7-9/PNG/", "Sigmund.png", "Its sleeve has a paper crease but no surviving page."),
    ("late", "Batch 7-9/PNG/", "Slime.png", "A clean gap divides the residue into two tide marks."),
    ("late", "Batch 7-9/PNG/", "Snorg.png", "Coarse hair catches on both sides of an open gate."),
    ("late", "Batch 7-9/PNG/", "Sun Demon.png", "Its bright edge stays visible through a shuttered lantern."),
    ("late", "Batch 7-9/PNG/", "Tormentor.png", "The nearby bell rope sways after the air has gone still."),
]

# Two multi-target field cases per location, written as separate investigation briefs.
CASES = {
    "af": [
        ("The Well's Second Shadow", "Mira Cole finds two different silhouettes appearing on the well stones after dusk. Clear both sites, then compare the ash at the rim before the water carriers return. She wants the time and wind recorded beside each trace, because the village has been treating every dark shape as part of the same attack."),
        ("A Margin Left in the Ledger", "A dry page in Mira's well ledger has a damp outline but no writing. Rowan is to clear the creatures gathered along the path; Mira will preserve each impression separately and ask the water carriers what they saw, without filling the blank with a guess."),
    ],
    "do": [
        ("Cadet Yard, Unmatched Steps", "Nia Porter discovers a formation scratched into the packed earth beside the drill yard. Remove the things repeating its turns and leave the chalk lines intact. She will compare the pattern with cadet exercises before anyone calls it an Order maneuver."),
        ("The Banner with No Unit", "A weathered strip of blue cloth has appeared on the eastern fence. Nia asks Rowan to make the fence safe while she checks old stores and watch rosters. The creatures' marks may share a color with an old banner; color alone will not name its unit."),
    ],
    "db": [
        ("Letters Returned Unopened", "Elara Wren finds envelopes stacked outside a room that was sealed during the barracks evacuation. Clear the room's living hazards and keep the envelopes in their current order. Elara will match folds and dispatch marks before deciding whether any letter was ever sent."),
        ("A Drill Not in the Manual", "Several marks on the barracks wall reproduce a movement absent from the current cadet manual. Rowan must remove the creatures that block the lower gallery. Elara will make two copies of the marks and leave the original wall untouched for the Order's archivist."),
    ],
    "cw": [
        ("The Seed Store Has a Visitor", "Talia Mercer finds new tracks between the seed store and the low-water channel. Drive the visitors off the work path, then note which sacks were already open. The harvest ledger will keep spoilage, missing grain and animal traces in separate columns."),
        ("Water Marks Above the Gauge", "A stain appears above the basin's highest recorded waterline. Clear the ledge so Talia can reach the gauge; do not scrub the mark. She will compare its color with the silt sample from the lower channel and record the readings that fail to match."),
    ],
    "cc": [
        ("Three Samples, Three Labels", "Talia's cistern samples were placed on one bench and their tags have shifted. Clear the passage so she can restore the order from the wax seals and dry rings. Rowan must record the chalk mark on each container before anyone moves it again."),
        ("The Bell Between Currents", "A low note comes from the dry side of the cistern just before the current turns. Remove the threats near the measuring points. Talia will time the bell and water separately, including the intervals when neither changes."),
    ],
    "sr": [
        ("Tracks on Both Sides of the Milepost", "Ruth Calder finds prints approaching the third milepost from opposite directions. Rowan clears the exposed route; Ruth will measure each set from the outer edge and mark damaged sections with a dotted line rather than joining them."),
        ("The Cart That Left No Wheel Marks", "A supply cart was reported near the pass, but the salt crust holds no clear wheel rut. Remove the creatures along the ridge so Ruth can inspect the slope. She will compare the report with axle grease, broken grass and the caravan's signed crossing list."),
    ],
    "sl": [
        ("A Voice Outside the Seal", "The lockhouse watch hears a familiar voice from behind an unopened drain door. Clear both stretches of corridor, but do not break the seal. Ruth Calder will schedule a two-person listening watch and compare the chalk line after every turn."),
        ("The Counterweight's Missing Mark", "A counterweight stops at a height absent from the maintenance chart. Rowan removes the hazards around the winch; Ruth records the rope, rust and mark on the door before anyone resets it. The mechanism can be safe without explaining who last operated it."),
    ],
    "ch": [
        ("A Note Heard Twice", "Lyra Moss hears one bell note arrive twice beneath the lake. Clear the ledges around the sounding posts so she can place two listeners at once. Each will record their own timing, including any echo too faint to identify."),
        ("Light Without a Lamp", "A pale stripe crosses the water even after the lamps are covered. Remove the creatures blocking the still pool. Lyra will sketch the light from two fixed positions and keep the sketches apart until their angles can be compared."),
    ],
    "gw": [
        ("The Garden's Unclaimed Rows", "The First Warden finds new tracks between the seed beds but no broken fence. Rowan clears a path wide enough for the harvest crew. The Warden will note where the plants bend back upright and leave the crooked rows for a later season's comparison."),
        ("A Keeper Without a Name", "Something has been sleeping beside the garden cistern, leaving the water clean and the stepping stones warm. Clear the approaches; do not call the visitor a guardian. The First Warden will ask the gardeners which paths they choose when no one is watching."),
    ],
    "ow": [
        ("The Index Repeats a Local Shape", "Dr. Evelyn Hart finds the same unlabelled silhouette in two archive plates from different centuries. Rowan secures both gallery approaches. Evelyn will compare image edges and pigment decay, preserving the chance that the match comes from the copying process rather than a living ancestor."),
        ("A Creature Drawn Before Its Track", "A sealed plate depicts a creature whose trace now crosses the Outer-Wake floor. Clear the route so Evelyn can document the print without touching it. She will keep the old plate, new trace and Rowan's account as three sources that may disagree."),
    ],
    "lo": [
        ("The Last Margin in the Green Index", "Captain Alden Vale finds four silhouettes pressed into the Cycle Heart's outer record. Rowan clears the final approach while the oath chamber remains closed. Alden will enter each encounter by location and time, never as a tally of lives the Crown claims to have counted."),
        ("What the World Kept", "The First Warden asks Rowan to clear a quiet court where the green record has begun to move. Alden records the route and the Warden compares it with the old garden index. Neither will call the creatures proof of what the World Will remembers until another witness can read the same page."),
    ],
}

CODEX = {
    "af": ("Mira Cole", "Ashfall: The Green Copy in the Well Ledger", "Mira Cole added this sheet after Rowan's second trip around the village well. The creatures were real enough to block a path, leave residue and force the water carriers to change their hours. The notes do not make them responsible for the raid. Mira keeps the ash, warmth and footprints on separate lines because the village has already learned how quickly fear turns a nearby mark into a name.\n\nThe green pigment appears in the creatures and in a rubbing from a page that predates the first Ashfall registry. That resemblance could be the World Will copying a useful shape, or a pigment shared by two unrelated records. Mira keeps both rubbings, including the portion that fails to match. The people who draw water need a route they can trust; they do not need an origin story invented for them."),
    "do": ("Nia Porter", "Dawnkeep: A Formation Without a Regiment", "Nia Porter compares the new silhouettes with cadet drills and finds a few turns that look familiar. A resemblance is not a record of service. The creatures leave no names, unit badges or signed oath; even the old blue cloth on the fence may have been cut from a market awning. She has entered the watch times beside each observation so later patrols can repeat the route.\n\nThe archive plates carry a green border, but the border is not part of the creature. Nia preserves a copy with the margin and another without it. If the Order still exists in a form able to inherit the outpost, its recruits should be taught to say what the evidence supports, and to leave a space where it does not. A safe drill yard can be returned to cadets without turning every print into a fallen soldier."),
    "db": ("Elara Wren", "Barracks Annex: Letters Beside the Green Plates", "Elara Wren sorted the returned envelopes by fold, seal and dispatch mark. None can yet be tied to the creatures in the gallery, and she will not infer a sender from a matching shade of green ink. The letters belonged to people who once expected a reply; their unfinished paths through the barracks matter even if the archive has no way to deliver them now.\n\nA plate found behind the cabinet shows a silhouette close to one Rowan met in the corridor. The plate's paper fibers are older than the room's plaster, but the drawing could have been copied from an earlier book. Elara stores a rubbing with a scale reference and leaves the original envelope stack intact. The Order may inherit the shelves, not the right to complete somebody else's letter."),
    "cw": ("Talia Mercer", "Cinderwell: A Living Shape Is Not a Water Reading", "Talia Mercer refuses to put the visitors' tracks in the same ledger as the reservoir level. The green marks recur near damp earth, yet several appear on stone above the highest waterline. She has kept measurements from before, during and after Rowan cleared the seed-store path, including days when the stain did not return. An empty result is still a result that can constrain the next test.\n\nThe archive calls the shapes a verdant index. That title may describe pigment, a copyist's category or a set of forms the World Will uses when it records life. Talia cannot tell whether these creatures grew in Asterra, were recalled from another place or were made as a working model. She asks the next surveyor to preserve the water samples and ask the gardeners separately. Hunger, mold and unsafe channels remain local problems whichever explanation proves true."),
    "cc": ("Talia Mercer", "Lower Cistern: The Bell and the Green Trace", "Talia Mercer entered the low bell and the cistern creatures on separate diagrams. Their timing sometimes overlaps, but not reliably. The water turns when a gate seal relaxes, when the upper channel overfills and on two occasions when no one saw the wheel move. She records each cause as a possibility, not a conclusion, and keeps the failed intervals in the book.\n\nGreen pigment survives on stone that has been submerged and on stone no water has reached. That pattern makes the index difficult to read as a simple reflection of local habitat. It might instead be a record that can appear wherever the World Will's memory touches the present. The cistern crew need clean, labeled samples more than a settled theory. Talia leaves the bell schedule beside the measurements so anyone can repeat both observations without relying on Rowan's recollection."),
    "sr": ("Ruth Calder", "Salt Road: A Record with Two Directions", "Ruth Calder filed each footprint set according to its direction, depth and the state of the salt crust. A pair of tracks crossing near the milepost does not show that their owners met; the wind can expose an older trail after a newer traveler has passed. The creatures on the route were dangerous, so Rowan's intervention allowed people to cross. Their presence does not establish who caused the missing-cart report.\n\nOne green plate from the archive seems to show the pass before the road was cut. Ruth marks the uncertain edge with a dotted line and has refused to align it with the current map. She keeps the crossing list sealed until families can decide whether their names should be copied into the public index. The record is useful when it helps someone travel safely; it is harmful if a resemblance is treated as proof against a living neighbor."),
    "sl": ("Ruth Calder", "Lockhouse: Voices, Seals and Moving Forms", "Ruth Calder wrote down the state of each drain seal before and after the watch. The familiar voice came from behind the same door on one night and from farther down the passage on another. No one opened the hatch. She records the listener, time and position because a sound that travels through a lockhouse cannot be assigned to a speaker by tone alone.\n\nThe green silhouettes gathered close to old counterweights, but none touched the rope in a way that explains its missing mark. The archive plate may be an illustration of this very building, or a pattern used to train a clerk's hand. Ruth will not enter absent people into a prisoner list based on a voice or a shape. Keeping the corridor safe is urgent; deciding whose voice the World remembers requires evidence from a second source."),
    "ch": ("Lyra Moss", "Choir: Two Listeners and One Green Reflection", "Lyra Moss asked two listeners to stand on opposite sides of the still pool. Their recorded bell times differed by less than a breath when the green visitors were nearby and by more when the lanterns were covered. She kept the raw notes, including the listener whose first reading was wrong. A corrected measurement should not erase the path by which it was corrected.\n\nThe figures on the old plates have no matching names in the Choir's missing-person register. Their light can be described; their origin cannot. Lyra believes the World Will may retain patterns of living things as it retains the sound of a bell, but a repeated echo is not the bell itself. She leaves a blank column for observations made after the lake has changed again. The people who return to this chamber should be able to challenge her account with their own measurements."),
    "gw": ("The First Warden", "Greenwake: A Garden and Its Temporary Keepers", "The First Warden marked the plants bent by passing bodies and left them in place. Several recovered by morning; several did not. A creature's warm resting hollow beside the cistern could be shelter, accident or a trace copied from another ecology. The gardeners were asked which paths they use when the court is empty. Their answer matters more than a title bestowed by the Crown.\n\nThe green index contains forms that resemble visitors now living in Greenwake, but the gardeners have never met these exact creatures before Rowan's patrol. The First Warden will not call them ancestors or guardians. If the World Will preserved an image of life, that image does not own the lives that grew from it. He writes down what was touched, what was left alone and which seed beds still need water before the next argument about the archive begins."),
    "ow": ("Dr. Evelyn Hart", "Outer-Wake: Comparing the Index to Its Imprint", "Dr. Evelyn Hart treats each encounter as a comparison problem. She has set the archive plates beside photographs of tracks, measured pigment under two lamps and asked a second reader to trace the edges without seeing the creature's name. The matches are suggestive but incomplete. Some details repeat; others look like damage in the paper. She saves the plates that do not support her first reading.\n\nThe World Will's archive may be holding a memory of living forms, a model for rebuilding them, or a catalog copied from somewhere beyond the Veil. None of these pages shows a person returning from death. Evelyn therefore calls the creatures imprints until a better word is earned. She also refuses to make Rowan's battle report the only witness. The archive should help the living ask what kind of world they want, not quietly decide that an image is equal to a life."),
    "lo": ("Captain Alden Vale", "Crownfall: What the World Kept, and What It Did Not", "Captain Alden Vale entered the four final encounters by place and hour. He did not call them four lives or four omens. The green index has no count of those it depicts, no signatures from the creatures and no way to ask whether an image remembers being alive. These gaps are written on the same page as the route because a record should show the limits of its maker.\n\nThe First Warden compared the last silhouettes with the garden ledger and found both resemblance and difference. Alden believes the World Will can preserve a pattern without preserving the people who once carried it. If Rowan chooses to end the cycle, the archive may become a witness to a world that refused the Crown's arithmetic. If Rowan renews it, the same pages may be used to justify another sacrifice. Alden leaves the index open, not as a verdict, but for the next reader to answer for themselves."),
}

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def atomic_write(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    if len(CREATURES) != 54 or len({row[2] for row in CREATURES}) != 54:
        raise SystemExit("The source list must define 54 distinct creature files.")
    if len(CASES) != len(REGIONS) or len(CODEX) != len(REGIONS):
        raise SystemExit("Every authored region needs two cases and one field record.")

    file_names = ["monster_catalog.json", "encounter_catalog.json", "prologue_quests.json",
                  "item_catalog.json", "dialogue_catalog.json", "codex_catalog.json"]
    paths, catalogs = {}, {}
    for file_name in file_names:
        paths[file_name], catalogs[file_name] = read_catalog(file_name)

    known = {entry.get("id", "") for data in catalogs.values() for entry in data["entries"]}
    expected_ids = []
    for index, (_, _, filename, _) in enumerate(CREATURES):
        region_code = list(REGIONS)[min(index // 5, 10)]
        slug = slugify(Path(filename).stem)
        expected_ids.extend([f"verdant_{slug}", f"verdant_{slug}_site", f"rowan_verdant_{slug}_record",
                             f"fieldgear_verdant_{slug}"])
    expected_ids.extend(f"side_verdant_{code}_{number}" for code in REGIONS for number in (1, 2))
    expected_ids.extend(f"verdant_codex_{code}" for code in REGIONS)
    found = [entry_id for entry_id in expected_ids if entry_id in known]
    existing_art = [ART / f"verdant_{slugify(Path(filename).stem)}.png"
                    for _, _, filename, _ in CREATURES]
    if found:
        if len(found) == len(expected_ids) and all(path.is_file() for path in existing_art):
            print("Verdant Memory is already imported; no changes made.")
            return
        raise SystemExit("Partial Verdant Memory import detected; inspect catalogs and sprites before retrying.")

    source_archives = {key: zipfile.ZipFile(path) for key, path in ARCHIVES.items()}
    sprites = []
    try:
        for archive_key, prefix, filename, _ in CREATURES:
            source_name = prefix + filename
            archive = source_archives[archive_key]
            if source_name not in archive.namelist():
                raise SystemExit(f"Missing source sprite {source_name} in {archive.filename}.")
            pixels = archive.read(source_name)
            if not pixels.startswith(b"\x89PNG\r\n\x1a\n"):
                raise SystemExit(f"Source is not PNG: {source_name}")
            sprites.append((source_name, filename, pixels))
    finally:
        for archive in source_archives.values():
            archive.close()

    # Region difficulty rises with the campaign. The final four are all elite.
    common_per_region = {"af": 3, "do": 3, "db": 3, "cw": 3, "cc": 3,
                         "sr": 3, "sl": 3, "ch": 2, "gw": 2, "ow": 1, "lo": 0}
    moves = ["shockwave", "siphon", "hook", "line_charge", "ranged_bolt", "marked_strike"]
    slots = ["weapon", "armor", "charm"]
    themes = {"af": "well", "do": "drill yard", "db": "returned letters", "cw": "seed store",
              "cc": "cistern bell", "sr": "milepost", "sl": "lockhouse", "ch": "still pool",
              "gw": "garden court", "ow": "archive gallery", "lo": "Cycle Heart"}

    additions = {name: [] for name in file_names}
    sprite_paths = []
    contract_last_by_region = {}
    final_quest_by_region = {}
    creature_by_region = {code: [] for code in REGIONS}
    index = 0
    for code in REGIONS:
        count = 4 if code == "lo" else 5
        regional = CREATURES[index:index + count]
        if len(regional) != count:
            raise SystemExit("Region distribution is incomplete.")
        index += count
        group_ranges = [(0, 2), (2, count)]
        if count == 4:
            group_ranges = [(0, 2), (2, 4)]
        region = REGIONS[code]
        common_count = common_per_region[code]
        last_elite = [entry["id"] for entry in catalogs["prologue_quests.json"]["entries"]
                      if entry.get("type") == "side" and entry.get("id", "").startswith(f"side_elite_{code}_")]
        prerequisite = last_elite[-1] if last_elite else region["root"]
        if code == "ow":
            prerequisite = "archive_return_report"
        if code == "lo":
            prerequisite = "last_oath_choice"

        for group_number, (start, end) in enumerate(group_ranges, 1):
            quest_id = f"side_verdant_{code}_{group_number}"
            predecessor = final_quest_by_region.get(code, prerequisite)
            case_title, brief = CASES[code][group_number - 1]
            objectives, rewards = [], []
            member_count = end - start
            positions = region["positions"]
            for local_index in range(start, end):
                archive_key, prefix, filename, signature = regional[local_index]
                name = Path(filename).stem
                slug = slugify(name)
                global_index = index - count + local_index
                common = local_index < common_count
                rank = "common" if common else "elite"
                monster_id = f"verdant_{slug}"
                encounter_id = f"verdant_{slug}_site"
                dialogue_id = f"rowan_verdant_{slug}_record"
                item_id = f"fieldgear_verdant_{slug}"
                level = region["level"]
                elite = not common
                slot = slots[global_index % len(slots)]
                attack_bonus = (level + (2 if elite else 0)) if slot == "weapon" else (max(1, level // 2) + (1 if elite else 0) if slot == "charm" else 0)
                guard_bonus = 0 if slot == "weapon" else (max(1, (level * 3 + 2) // 4) + (1 if elite else 0) if slot == "armor" else max(1, level // 3))
                appearance = signature.split(". ", 1)[-1].rstrip(".")
                item_name = f"Verdant {name} { {'weapon': 'Edge', 'armor': 'Mantle', 'charm': 'Keepsake'}[slot] }"
                item_description = (f"A field tool made after the {name}'s trace at the {themes[code]}. "
                                    f"Its {appearance}; useful when Rowan must return to the same mark and compare it.")
                item_description += f" Tăng {attack_bonus} Công và {guard_bonus} Giáp."

                additions["monster_catalog.json"].append({
                    "id": monster_id, "displayName": name.replace("-", " "), "rank": rank,
                    "maxHealth": 32 + level * 7 + (42 if elite else 0),
                    "attackDamage": 4 + level + (4 if elite else 0), "attackReach": 1.25,
                    "approachSpeed": round(0.88 + min(level, 10) * 0.028 + (0.06 if elite else 0), 3),
                    "lungeDistance": 1.65 if not elite else 1.9, "lungeSeconds": 0.34,
                    "lungeStopDistance": 0.68, "openingDelay": round(1.3 - min(level, 8) * 0.035, 3),
                    "closingSeconds": 1.12 if not elite else 1.2,
                    "telegraphSeconds": 0.82 if not elite else 1.08,
                    "recoverySeconds": 0.95 if not elite else 1.08,
                    "counterBonusDamage": 12 if not elite else 20,
                    "hitCooldown": round(0.7 - min(level, 5) * 0.025, 3),
                    "spriteResource": f"verdant_{slug}", "lungeSpriteResource": "",
                    "spriteScale": 2.55 if not elite else 2.7, "spritePixelsPerUnit": 32,
                    "specialMoveId": moves[global_index % len(moves)] if elite else "",
                    "specialMoveReach": round(3.2 + level * 0.24 + (0.5 if elite else 0), 2) if elite else 0.0,
                })
                position = positions[(local_index - start) % len(positions)]
                additions["encounter_catalog.json"].append({
                    "id": encounter_id, "monsterId": monster_id, "locationId": region["location"],
                    "positionX": position[0], "positionY": position[1], "requiredQuestId": quest_id,
                    "blockedQuestId": "", "blockedDialogueId": "", "contributesToQuest": True,
                    "defeatObjectiveTargetId": monster_id, "defeatDialogueId": dialogue_id,
                    "downDialogueId": "rowan_field_retreat",
                    "reward": {"gold": 8 + level * 3, "items": []},
                })
                additions["item_catalog.json"].append({
                    "id": item_id, "name": item_name, "description": item_description,
                    "category": "equipment", "equipmentSlot": slot, "maxStack": 1,
                    "attackBonus": attack_bonus, "guardBonus": guard_bonus, "healAmount": 0,
                    "sellValue": 48 + level * 10,
                })
                objectives.append({"id": f"defeat_{slug}", "kind": "defeat", "targetId": monster_id,
                                   "requiredCount": 1,
                                   "description": f"Đánh bại {name.replace('-', ' ')} và ghi lại dấu vết tại hiện trường."})
                rewards.append({"itemId": item_id, "quantity": 1})
                evidence = signature[:-1] if signature.endswith(".") else signature
                additions["dialogue_catalog.json"].append({
                    "id": dialogue_id, "speakerName": "ROWAN HALE", "lines": [
                        f"Mẫu trong bản ghi được nhận dạng là {name.replace('-', ' ')}. {evidence} "
                        f"Tôi đo khoảng cách tới {themes[code]} và đánh dấu vị trí trước khi đội dọn đường đi qua.",
                        f"{region['author']} giữ bản vẽ này riêng khỏi hồ sơ người mất tích. Dấu xanh lặp lại, "
                        f"nhưng nó chưa nói sinh vật đến từ đâu; lần đo kế tiếp phải có người khác đối chiếu.",
                    ]
                })
                creature_by_region[code].append((name, rank, signature))
                sprite_paths.append((f"verdant_{slug}.png", sprites[global_index][2]))

            additions["prologue_quests.json"].append({
                "id": quest_id, "arcId": region["arc"], "stage": -1,
                "type": "side", "locationId": region["location"], "giverId": region["giver"],
                "title": case_title, "objective": brief,
                "prerequisiteIds": [predecessor], "objectives": objectives,
                "reward": {"gold": 24 + region["level"] * 4, "items": rewards},
            })
            final_quest_by_region[code] = quest_id
        contract_last_by_region[code] = final_quest_by_region[code]

    for code, region in REGIONS.items():
        author, title, body = CODEX[code]
        additions["codex_catalog.json"].append({
            "id": f"verdant_codex_{code}", "title": title, "category": "World Memory",
            "writtenBy": author, "unlockQuestId": contract_last_by_region[code], "body": body,
        })

    # Validate all catalog IDs before touching files, then write sprites and catalogs atomically.
    for name, data in catalogs.items():
        old_ids = {entry.get("id", "") for entry in data["entries"]}
        new_ids = [entry["id"] for entry in additions[name]]
        if len(new_ids) != len(set(new_ids)) or old_ids.intersection(new_ids):
            raise SystemExit(f"Duplicate catalog ID while preparing {name}.")
    if len(sprite_paths) != 54 or len({path for path, _ in sprite_paths}) != 54:
        raise SystemExit("Each of the 54 species must receive one distinct sprite.")
    for file_name, catalog in catalogs.items():
        catalog["entries"].extend(additions[file_name])
    for relative, payload in sprite_paths:
        destination = ART / relative
        if destination.exists():
            raise SystemExit(f"Sprite already exists: {destination}")
        destination.write_bytes(payload)
    try:
        for file_name, catalog in catalogs.items():
            atomic_write(paths[file_name], catalog)
    except Exception:
        for relative, _ in sprite_paths:
            (ART / relative).unlink(missing_ok=True)
        raise

    mapping = ROOT / "Docs/AssetArchives/verdant-memory-species-map.tsv"
    with mapping.open("w", encoding="utf-8") as stream:
        stream.write("resource\tsource_archive\tsource_path\tmonster_id\trank\tlocation\n")
        at = 0
        for code in REGIONS:
            count = 4 if code == "lo" else 5
            for archive_key, prefix, filename, _ in CREATURES[at:at + count]:
                slug = slugify(Path(filename).stem)
                local_index = at % 5
                rank = "common" if local_index < common_per_region[code] else "elite"
                source = f"{prefix}{filename}"
                stream.write(f"verdant_{slug}\t{ARCHIVES[archive_key].name}\t{source}\tverdant_{slug}\t{rank}\t{REGIONS[code]['location']}\n")
            at += count

    print("Imported 54 CC0 Verdant Memory sprites, 22 multi-objective side contracts, "
          "54 species records, encounters, authored field dialogues and unique equipment rewards, "
          "and eleven location-specific codex records.")


if __name__ == "__main__":
    main()
