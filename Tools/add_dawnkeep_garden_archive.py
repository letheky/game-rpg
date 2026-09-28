import json
from pathlib import Path


QUESTS_PATH = Path("Assets/Resources/Content/prologue_quests.json")
CODEX_PATH = Path("Assets/Resources/Content/codex_catalog.json")

ENTRIES = [
    {
        "id": "dawnkeep_garden_open_slate",
        "title": "The Slate Was Never a Roster",
        "category": "Garden Practice",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "side_elara_garden_open",
        "body": "I reopened the east bed because the slate had been copied into three separate training binders, each with the same blank interval after heavy rain. I thought the empty line meant someone had failed to report. The stone beside the gutter made me doubt that reading: its lower scratch was older than the newer roof hinge, and water could not have followed both marks at once.\n\nRowan asked why I had not simply corrected the slate years ago. I had no satisfying answer. I preserved the wording because I feared changing a record without understanding it. Then I began treating preservation as if it were the same thing as care. The mint seed in the step crack survived without a schedule, while the garden remained closed because I would not teach an incomplete one.\n\nThe bed is not proof that the old rotation worked. It is a place to learn what its writer could not leave in the margin: how the channel behaves now, what a small crop needs, and who wants to tend it. Keep the original slate with this note. Anyone reopening the bed should be allowed to replace our lesson with a better one.",
    },
    {
        "id": "dawnkeep_garden_blank_turn",
        "title": "The Space Left by the Rain",
        "category": "Garden Practice",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "side_elara_garden_shift_notes",
        "body": "The slate places the blank interval between an evening watering turn and the next morning's check. Rain is recorded in the margin, but not in the square where a cadet's name would usually go. The stone below the gutter holds a lower waterline, while a second scratch lies closer to the drain frame. They do not line up well enough to be one measurement.\n\nElara first read the space as a missing person. The tools tell a smaller story: the watering can stayed beneath the awning, the soil did not need another pour, and the runoff channel had filled with grit. Someone may have paused the rota to avoid adding water. We cannot identify who made that decision, or whether one person made it at all.\n\nI have marked the blank with a weather note rather than a name. That does not settle the old record; it only gives the next reader another possibility to compare. The garden's slate should never be copied into the cadet roll as evidence of attendance. A pause in work and a missing cadet are different claims, even when the same empty square tempts us to join them.",
    },
    {
        "id": "dawnkeep_garden_waiting_years",
        "title": "Years Preserved, No Water Given",
        "category": "Garden Practice",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "side_elara_garden_shift_talk",
        "body": "I kept the old rotation beside my desk long after the bed closed. When new cadets asked about the blank interval, I repeated the explanation I had inherited: the slate was incomplete, so no one should act on it. That sounded careful. It also meant I never had to find out whether the runoff could be measured again.\n\nThe garden remained clean on paper. No one watered a dry plot, no one signed a turn they had not taken, and no one could be blamed for a bad crop. But the mint pushed through a crack at the east step, a stubborn plant outside the record's reach. Rowan brought me one of its leaves, and for the first time I saw that my perfect copy had described a garden no one was tending.\n\nI am not ashamed of keeping the slate. I am ashamed that I let the copy stand in for teaching. The new lesson begins with what we can touch: soil, water, the bent hinge and a seed that may not sprout twice. A cadet can decline a turn. A record can say the bed was idle. Neither statement erases the work of the people who kept the old pages dry.",
    },
    {
        "id": "dawnkeep_garden_hinge_pass",
        "title": "A Hinge That Lets the Channel Breathe",
        "category": "Garden Practice",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "side_elara_garden_drain",
        "body": "The lower hinge carries two grooves where a clip could rest, one above the gutter and one level with the catch pocket. The lower groove is easy to reach but fills with grit. The upper groove stays cleaner, though a person standing at the bed cannot read a water mark there without leaning over the stones.\n\nElara asked me to sketch both positions without choosing for the next keeper. We checked the old frame first. It bends when pressed near the channel, so no fitting should be used to brace it or stop its movement. The runoff has to pass through the gutter whether the garden is planted or not. Blocking it would turn an observation tool into a dam.\n\nThe useful quality of a marker is not that it never moves. It is that someone can remove it, clean around it and see the channel underneath. I left room in the sketch for a hand to reach the fastener. The frame is still damaged and needs a carpenter's inspection before heavy rain. This note covers placement for a small trial only; it is not a repair order for the roof gutter.",
    },
    {
        "id": "dawnkeep_garden_mint_saved_seed",
        "title": "Mint from the Step Crack",
        "category": "Garden Practice",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "side_elara_garden_mint",
        "body": "The first Dawnmeadow Mint did not grow in a prepared row. It appeared in the narrow crack where the step meets the wall, fed by spray from the gutter and warmed by the stone after midday. I saved a seed when the plant flowered, but I did not label it as the last living seed or the strongest one. Several pods were still closed when I gathered this sample.\n\nRowan planted one seed in the reopened bed. It needed a full crop cycle before we could cut a leaf without pulling the root. The mint smell was strongest after the leaves dried on the table; the fresh ones carried more water than scent. The difference matters to a healer, but we have not tested either batch as medicine. Mira asked us to keep the harvest separate from her remedy stock until she can inspect it.\n\nA seed saved from one crack can restart one small row under these conditions. It does not promise that the plant will take in another bed, nor that the gutter will keep the soil wet. I have placed the remaining seed packets beside this note so a future gardener may compare the two crops. If none are planted next season, record that too. Quiet ground is not a failed lesson.",
    },
    {
        "id": "dawnkeep_garden_scale_gauge",
        "title": "A Trout Scale beside a Ruler",
        "category": "Garden Practice",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "side_elara_garden_fish",
        "body": "Elara needed a thin mark that would not split in the gutter's damp air. The Blackreed Trout scale was flexible when wet and stiffened as it dried; that gave us a way to set a short edge against the bronze clip. It is an odd ruler, but it was available at the lakeshore and easy to replace with another sample.\n\nI wrote down the catch location and the time before trimming the scale. Its dark rim faded after it dried, and the pale center curled when left near the forge. We adjusted the clip while the scale was still damp, then let the material dry away from the flame. It now marks a height. It does not measure the safety of the lake, the age of the fish or the level of water in every gutter.\n\nThe fish returned to the food basket after the scale was taken. No part of the catch was kept as a permanent standard. A later sample may be a different size; whoever makes a new clip should record that difference rather than forcing it to match this piece. Elara wants the garden tool to be replaceable, not rare. The measure belongs to the trial and its conditions, not to a species name.",
    },
    {
        "id": "dawnkeep_garden_two_marks",
        "title": "Two Scratches on the Gutter Stone",
        "category": "Garden Practice",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "side_elara_garden_waterline",
        "body": "The pale lower scratch crosses a patch of moss that now grows only on one side of the gutter. The higher mark is sharper, nearer the bent frame. It may be a second waterline, or it may be a tool scrape left when the roof hinge was handled. The stone does not tell us who made either mark.\n\nNia suggested measuring the distance from each scratch to the fixed corner rather than comparing one to the other. That makes the notes easier to repeat: a reader can find the corner even if the moss grows over the old line. I took two readings after the mint had been watered and a third after the catch pocket was emptied. The lower mark stayed damp; the upper one did not.\n\nThese readings are not a history of the storm. They are three present-day observations with different conditions. A future student may find that the moss has moved, the hinge has been repaired or the stones have settled. Keep the measurements beside the date and weather, and start a new column rather than overwriting ours. If no one can tell which mark is which, the correct entry is “uncertain,” not a blended average.",
    },
    {
        "id": "dawnkeep_garden_flexible_handoff",
        "title": "Handing over a Turn without a Name",
        "category": "Garden Practice",
        "writtenBy": "Nia Porter",
        "unlockQuestId": "side_elara_garden_nia",
        "body": "The old handoff slate gives every turn a fixed name before the person has a chance to see the weather or the bed. That works only when the schedule survives the week unchanged. At Dawnkeep, drill times move, rain closes the yard and a cadet may be sent to a different hall. The record then treats a changed duty like a missing one.\n\nElara asked how I would write a garden turn without handing someone a permanent place in the rota. I suggested recording what needs attention first: inspect the drain, water the mint if the soil is dry, clear grit after rain. A person can choose one task, ask someone else to take it or leave the slate untouched until conditions change. The next keeper writes what actually happened, not what a prior copy expected.\n\nA handoff is useful when the person receiving it can see the state of the work and decline to inherit the schedule. The roster I keep for cadets has its own corrections and missing replies; I will not copy it into a garden list. The bed has no attendance requirement. I left a blank line for whoever volunteers to note a task, and another for a later reader to revise the instructions.",
    },
    {
        "id": "dawnkeep_garden_clip_fitting",
        "title": "Bronze Clip, Mint Fiber, Fish Scale",
        "category": "Garden Practice",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "side_elara_garden_brace",
        "body": "The clip is made from a narrow bronze strip, a twist of Dawnmeadow Mint fiber and one Blackreed Trout scale. The fiber stops the metal edge from scraping the old frame; the scale provides a short reference mark. None of these parts makes the gutter stronger. Tomas checked the fastener and asked us to leave the cracked hinge visible for a carpenter.\n\nAt the forge we bent the bronze over a cold block rather than heating it until the color changed. A hotter strip held its shape, but it also crushed the scale when we fitted the padding. The softer piece can be opened with a hand tool. It is less impressive than a permanent brace and easier to remove after the test.\n\nThe clip's mark is readable only when the scale is clean and the bed's edge is not hidden by leaves. Elara will keep spare fiber in a dry envelope. If the scale curls, the fiber loosens or the metal bites into the frame, the clip should come down. The object records a water level during a short trial. It is not a structural part, a roof repair or a guarantee that the channel will stay clear.",
    },
    {
        "id": "dawnkeep_garden_install_note",
        "title": "A Mark That Can Be Taken Down",
        "category": "Garden Practice",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "side_elara_garden_install",
        "body": "We placed the clip in the upper groove, where a keeper can read it from the stone path and remove it without reaching into the runoff. The catch pocket remains open. After Rowan fitted the fastener, I ran one cup of water through the gutter to see whether the mark touched the stream. It did not. The test was short and took place in dry weather.\n\nI asked Rowan to leave the clip in place for one observation, then take it down before cleaning the frame. A tool that can be removed invites its owner to inspect what lies behind it. A permanent mark would be easier to copy into a diagram, but it might hide damage or gather grit at the hinge. The old frame still needs a proper repair; the clip does not change that.\n\nWe will not ask cadets to climb the roof or handle a fast stream to repeat this check. The garden path is enough for the next reading. If the waterline passes the mark, if metal begins to press against the wood, or if the pocket fills, remove the clip and write the condition beside the date. The lesson is the removable measure and the way to question it, not a claim that the gutter has been made safe.",
    },
]


def main():
    quests = json.loads(QUESTS_PATH.read_text(encoding="utf-8"))["entries"]
    catalog = json.loads(CODEX_PATH.read_text(encoding="utf-8"))
    quest_by_id = {quest["id"]: quest for quest in quests}
    codex_by_id = {entry["id"]: entry for entry in catalog["entries"]}
    unlocks = {entry["unlockQuestId"] for entry in catalog["entries"]}
    added = 0

    for entry in ENTRIES:
        quest = quest_by_id.get(entry["unlockQuestId"])
        if quest is None or quest.get("arcId") != "the_order_of_the_dawn":
            raise SystemExit(f"Missing Arc 2 garden quest: {entry['unlockQuestId']}")
        if entry["unlockQuestId"] in unlocks and entry["id"] not in codex_by_id:
            raise SystemExit(f"Quest already unlocks another codex: {entry['unlockQuestId']}")
        existing = codex_by_id.get(entry["id"])
        if existing is not None:
            if existing != entry:
                raise SystemExit(f"Codex ID already exists with different content: {entry['id']}")
            continue
        catalog["entries"].append(entry)
        codex_by_id[entry["id"]] = entry
        unlocks.add(entry["unlockQuestId"])
        added += 1

    CODEX_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} Dawnkeep garden codex records, each unlocked by its matching Arc 2 quest.")


if __name__ == "__main__":
    main()
