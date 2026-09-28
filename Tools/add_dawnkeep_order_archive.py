import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS_PATH = ROOT / "Assets/Resources/Content/prologue_quests.json"
CODEX_PATH = ROOT / "Assets/Resources/Content/codex_catalog.json"

ENTRIES = [
    {
        "id": "dawnkeep_order_arrival_record",
        "title": "A Map with No Destination",
        "category": "Order Archive",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "order_arrival",
        "body": "Captain Alden sent me to Dawnkeep with a narrow map folded inside the dispatch. It showed the gate, the eastern yard and three paths down toward Cinderwell. No destination was marked at the end of those paths. I thought the missing label was a clerk's mistake. Elara Wren looked at the fold instead: the paper had been pressed flat so often that the road below the outpost had nearly vanished.\n\nShe asked me to speak with her before reporting what the map meant. That was the first order I received here, and the first one whose meaning I could not establish by carrying it out. I can say that Alden sent me, that the map was made for a journey south, and that Elara had been waiting for someone to ask about the old stone. I cannot yet say who traveled that road or why.\n\nI have copied the route without filling the empty destination. A blank on a map might hide a lost village, a discarded plan or a place its maker did not wish to name. I was taught to draw a line until it reached a border. At Dawnkeep, the border is the part we have to investigate."
    },
    {
        "id": "dawnkeep_order_roster_rubbing_record",
        "title": "An Impression of the Chiseled List",
        "category": "Order Archive",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "order_roster",
        "body": "The east face of the roster stone holds two kinds of marks. Names were cut deep enough to survive the weather; shorter strokes lie between them, where a chisel appears to have passed across the surface. Rowan pressed a sheet over the stone and made a rubbing. The impression keeps the gaps visible, though it flattens every cut into the same dark line.\n\nI recognize the arrangement from an older training copy. It was filed with the yard ledgers, not the muster rolls, and the heading is missing from both. One clerk may have copied the list into another book before anyone scraped it. The rubbing cannot tell us whether a name was removed for correction, privacy or some other reason. It cannot restore the names that no longer catch the paper.\n\nWe should keep the rubbing beside a sketch of the stone and note which marks are original. Do not trace the gaps into a new roster as if they were names. An impression preserves the shape of what remains; it does not recreate the person who might once have stood between the cuts."
    },
    {
        "id": "dawnkeep_order_disclosure_choice_record",
        "title": "Two Costs of a Copy",
        "category": "Order Archive",
        "writtenBy": "Captain Alden Vale",
        "unlockQuestId": "order_record_choice",
        "body": "The roster impression can be shown to the patrol or kept while we search the archive. Either course carries a cost. If the patrol sees it now, every empty space will become a question asked in the yard, and the living will have to answer questions the stone cannot settle. If it remains with the archive, those questions may wait while we find a second record. They may also wait because someone prefers the silence.\n\nI put the choice before Rowan as an officer's decision, then asked him to carry it. That is not the same as giving him a clean choice. The copy has already passed through my hands and the Order's rules have shaped what he can do with it. If I hide that, I make his decision look freer than it is.\n\nThe patrol deserves to know when an official record is incomplete. It also deserves to know that the marks are uncertain. I have no authority to make the uncertainty disappear for the sake of a simpler report. Whichever version is kept, let the written account name who received it, when it changed hands and which questions remain unanswered."
    },
    {
        "id": "dawnkeep_order_public_response_record",
        "title": "The Yard after the Rubbing Was Read",
        "category": "Order Archive",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "order_archive_public",
        "body": "The patrol gathered by the east wall when Rowan read the rubbing aloud. I expected anger first. Instead, the first person to speak asked whether the strokes between the names were old tally marks. Another cadet wanted to know why a training stone had been copied into the archive at all. No one had enough information to answer either question.\n\nI said what I knew: the stone has deep-cut names, shorter marks and a heading that is no longer attached to the record. I also said what I did not know: who made the cuts, whether the list was complete, or whether the people it once described were sent south. Several listeners had family names in the surviving lines. They deserved the plain account, not my confidence in a guess.\n\nThe rubbing now hangs beside a slate with room for corrections. Some will write to relatives; others may ask to have their name checked against the remaining rolls. Those requests will take time. Reading the record publicly changed who could question it, not what it proves. I will keep the first copy unmarked so a later correction does not erase what the patrol saw today."
    },
    {
        "id": "dawnkeep_order_private_response_record",
        "title": "The Drawer and the Missing Key",
        "category": "Order Archive",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "order_archive_private",
        "body": "Rowan kept the rubbing with the archive while I searched for its heading. I locked it in the shallow drawer beside the yard ledgers. The drawer has room for one copy and no separate compartment for the questions it carries. I have written the inventory on the outside: one rubbing, one sketch of the stone, no restored names, no proof of where the patrol went.\n\nI told the cadets we were checking the record before we spoke about it. Some accepted that explanation. Others asked who had chosen the delay. I said I had helped make it. That answer did not make the lock gentler, but it kept me from presenting privacy as something the archive had decided on its own.\n\nThe key stays with the registrar. If a family asks about a surviving name, they may request a supervised reading rather than wait for the entire investigation to finish. We have not found the old heading yet. Until we do, the drawer protects the fragile sheet from careless handling; it also limits who can see it. Put both effects in the catalogue. A locked record can prevent damage and postpone accountability at the same time."
    },
    {
        "id": "dawnkeep_order_empty_cots_record",
        "title": "Beds Put Away for Inspection",
        "category": "Order Archive",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "order_empty_cots",
        "body": "The old barracks hold an uneven row of cots. Some frames were dismantled cleanly and stacked against the wall. Others still carry the chalk numbers used to assign sleeping places. Dust covers the lower boards, but a narrow path runs between them, as if someone continued to enter the room after it was closed.\n\nI found a heel mark beside one frame and a pale strip where a blanket may have rested. Neither tells me how long ago a person slept there. A number on wood is an instruction for a place, not a name. The surviving roster has empty spaces, yet I cannot match those spaces to these beds. The room may have housed cadets whose records were kept elsewhere; it may have been used for more than one class.\n\nI drew every cot before moving the ones that blocked the passage. The sketch records which frames were whole, which were split and which chalk numbers remained. We did not find a personal letter, a weapon or anything that would identify an occupant. Until another source connects the room to the roster, the honest description is an empty barracks with numbered beds."
    },
    {
        "id": "dawnkeep_order_cadet_testimony_record",
        "title": "Nia's Correction in the Margin",
        "category": "Order Archive",
        "writtenBy": "Nia Porter",
        "unlockQuestId": "order_cadet_testimony",
        "body": "When I was a cadet, I copied the night assignments into the return ledger. A transfer order arrived with more beds counted than signatures at the gate. I added a mark in the margin and asked the clerk whether to change the total. The clerk said to leave the number as issued because a route order was not proof of arrival. I did. Later copies carried the total but not my question.\n\nI remember this because the question was mine, not because I know which people the number describes. I saw a sealed packet taken south. I did not see its passengers. I heard two versions of why the roster changed, each from someone who had read a different page. Neither version came from a person who could show me the receiving record.\n\nPlease file this as testimony about my work on the ledger. Do not use my account to fill the empty cots or restore the erased marks. I can point to the margin where I wrote the question if the old book is found. Until then, someone else's copy of what I remember should remain open to correction by the person who first made the mark."
    },
    {
        "id": "dawnkeep_order_transfer_ledger_record",
        "title": "A Dispatch with No Return Column",
        "category": "Order Archive",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "order_transfer_ledger",
        "body": "The transfer ledger places a set of cadet numbers beside an order for the southern road. A clerk has marked that the packet was sealed and issued. The column for a receiving signature is blank. A second page lists stores sent to Cinderwell, but the quantities do not map cleanly to the numbers on the first page. Someone may have joined two records when they copied the ledger.\n\nNia recognized the margin mark as the one she used when the return count did not match the order. Her mark proves she questioned the total. It does not prove which version was right. I have kept the first and second pages apart in the transcription, noting where the old binding placed them together. A neat table would make their relationship look more certain than it is.\n\nThere is no return column at all, only a space where a receiver might have signed. That space cannot tell us whether the party arrived, was redirected or was entered in a different book. The next search should follow the seal number and the supply trail through Cinderwell. Until a receiving document is found, this ledger establishes an order sent south and a record-keeping gap."
    },
    {
        "id": "dawnkeep_order_evidence_choice_record",
        "title": "The Limit of Naming Names",
        "category": "Order Archive",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "order_evidence_choice",
        "body": "The ledger gives us a count, a route and several names that survived the scraping. A few families have already asked whether their relatives were on the list. We cannot use the missing return signature to answer them. We can only show which marks remain, which copy they came from and which clerk last handled it.\n\nPublishing the verified names gives families a starting point for their own questions. Sealing the original and sending private copies gives them access without placing every surviving name on a public wall. Neither option tells a family what happened after the dispatch left Dawnkeep. Elara asked Rowan to decide which kind of access he could stand behind while the investigation continued.\n\nI would like to make the choice for him. That would be easier than seeing what the Order's old habits have taught us to call protection. The family copies must not become secret replacements for the public record, and a public list must not be mistaken for a complete roll. Record who can ask for a correction, who can see the source and how a copy can be withdrawn if a family requests it. A name belongs to the person first; the archive only keeps the marks we can justify."
    },
    {
        "id": "dawnkeep_order_open_testimony_record",
        "title": "A Noticeboard with a Correction Line",
        "category": "Order Archive",
        "writtenBy": "Nia Porter",
        "unlockQuestId": "order_open_testimony",
        "body": "We posted the verified copy at the yard noticeboard with the seal still visible and a blank line beneath every uncertain entry. The line is not a request for passersby to guess at the missing names. It lets someone who has a source leave a note about where the registrar can check it. I have put a small box beside the board for letters that should not be read aloud.\n\nSome cadets stopped to look, then left without writing. One asked whether an empty place beside a surviving name meant that a sibling was sent away. I told them the copy does not show that. It shows a name, a cut and the absence of a return signature in the ledger we have. The answer disappointed them. I would rather disappoint someone honestly than offer a story that becomes harder to correct.\n\nThe board will stay up for one week before the pages are reviewed for private details. If a family wants a name withheld, the request will be attached to the next copy rather than scraped off the current one without a trace. Public access needs a route for correction and a way to limit harm; otherwise the first posting only gives the loudest reader control of the next version."
    },
    {
        "id": "dawnkeep_order_sealed_record_record",
        "title": "Copies Beneath Family Seals",
        "category": "Order Archive",
        "writtenBy": "Elara Wren",
        "unlockQuestId": "order_sealed_record",
        "body": "We placed the original rubbing in the archive drawer and prepared one verified copy for each family who asked to receive one. The copy states how many marks remain legible, which pages were compared and where the receiving signature is missing. I sealed each envelope with the registrar's mark and recorded the recipient privately. A seal can show that the paper was handled through the archive; it cannot prove the contents are complete.\n\nThe families may keep their copy, return it or request a fresh one after the next comparison. They do not have to send a reason with a correction. I have also kept an unsealed transcription so that a later registrar can compare the public evidence without opening a family's letter. There are two records of distribution, but only one source rubbing. Neither should be treated as the original.\n\nI used to think a sealed record was a safer record. Now I think it is only safer for as long as people can find its keeper and ask what the seal means. The drawer will be catalogued by subject and date, not by the names whose families received copies. A person looking for a relative should not need to search through someone else's private correspondence."
    },
    {
        "id": "dawnkeep_order_cinderwell_dispatch_record",
        "title": "The Waterway Points South",
        "category": "Order Archive",
        "writtenBy": "Rowan Hale",
        "unlockQuestId": "order_cinderwell_dispatch",
        "body": "Elara spread the dispatch across the map of the waterway to Cinderwell. The route follows a service road above the channel, crossing two lock points before it reaches the lower basin. The inked arrow marks where the packet was meant to travel. It does not mark a boat, a camp or a group of cadets. I have written “planned route” beside it so a later reader will not mistake the line for a travel log.\n\nThe seals on the dispatch match the format Nia described. One clerk's mark appears beside the stores list, but the receiving space remains empty. At the second lock, the margin carries a note about a gate inspection. No names accompany it. These details give us places to visit and records to request. They do not yet show who passed through either lock.\n\nCinderwell can tell us whether the supply order was received, whether another ledger survives and whether the seal continued south. It cannot make the missing signature appear in the Dawnkeep book. We leave with better questions than we had when the map was folded: who accepted the packet, which copy they kept and whether the people counted in the roster traveled with it."
    },
    {
        "id": "dawnkeep_order_alden_reckoning_record",
        "title": "The Captain's Signature Does Not Answer",
        "category": "Order Archive",
        "writtenBy": "Captain Alden Vale",
        "unlockQuestId": "order_alden_reckoning",
        "body": "My signature appears at the bottom of the transfer order. It authorizes a dispatch of supplies and cadet numbers toward Cinderwell. I remember signing the page. I cannot claim that the memory tells me what happened after the packet left my desk, or why the return column in the surviving ledger was never completed.\n\nI once used the word routine when Rowan asked about the signature. Routine is useful when a hundred orders need to be checked; it is a poor answer to the people whose names no longer appear in the book. The seal is mine to explain, and the gap is mine to help investigate. That does not make me the witness to every journey listed beneath it.\n\nI have requested the original dispatch from the Cinderwell registrar and asked for the clerk's mark to be compared with the copy here. I will not alter the archive entry while we wait. If the comparison shows an error in the count, the correction should preserve this signed page beside the corrected one. My responsibility begins with admitting what I approved. It does not end until another record can show what the Order did with that authority."
    },
]


def main() -> None:
    quests = json.loads(QUESTS_PATH.read_text(encoding="utf-8"))["entries"]
    catalog = json.loads(CODEX_PATH.read_text(encoding="utf-8"))
    quest_by_id = {quest["id"]: quest for quest in quests}
    codex_by_id = {entry["id"]: entry for entry in catalog["entries"]}
    unlocks = {entry["unlockQuestId"] for entry in catalog["entries"]}
    added = 0

    for entry in ENTRIES:
        quest = quest_by_id.get(entry["unlockQuestId"])
        if quest is None or quest.get("arcId") != "the_order_of_the_dawn":
            raise SystemExit(f"Missing Arc 2 quest: {entry['unlockQuestId']}")
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
    print(f"Added {added} Dawnkeep Order Archive records to their matching Arc 2 quests.")


if __name__ == "__main__":
    main()
