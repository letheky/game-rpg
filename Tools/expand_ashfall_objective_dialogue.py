import json
from pathlib import Path


QUESTS_PATH = Path("Assets/Resources/Content/prologue_quests.json")
DIALOGUE_PATH = Path("Assets/Resources/Content/dialogue_catalog.json")

# Quest ID, objective ID, dialogue ID, speaker, lines.
OBJECTIVES = [
    ("ashfall_survivors", "meet_mira", "mira_af_first_list", "MIRA COLE", [
        "Đừng vội viết tên vào bảng, Rowan. Người vừa chạy khỏi con hẻm chưa chắc biết ai còn mắc kẹt sau cánh cửa.",
        "Đánh dấu điều mình nhìn thấy, để khoảng trống vẫn mở. Khi có tin từ phía đông, ta sửa danh sách bằng chứng mới.",
    ]),
    ("ashfall_warg", "defeat_ash_warg", "rowan_af_warg_trace", "ROWAN HALE", [
        "Ash Warg ngã xuống, nhưng chiếc vòng đồng mắc trong tro không mang dấu Order. Mình sẽ giữ nguyên vết khắc và hỏi thêm nguồn khác.",
        "Trận này chấm dứt nguy hiểm trước mặt. Nó chưa giải thích ai mở cổng, hay vì sao con thú vào sân.",
    ]),
    ("ashfall_shelter_witness", "talk_gideon", "gideon_af_shelter_witness", "GIDEON PARK", [
        "Tôi đưa ba người tới mái hiên: hai người cho biết tên, người cuối chưa muốn nói. Tôi không biết cô ấy đã đi cùng ai.",
        "Ghi số ghế tôi có thể kê và chỗ còn để trống. Đừng cho cái ghế ấy một cái tên chỉ vì hình dáng của nó quen.",
    ]),
    ("ashfall_trail_evidence", "inspect_burned_seal", "rowan_af_burned_seal", "ROWAN HALE", [
        "Vết sáp lõm ở mặt trong; dấu có thể được ép khi giấy còn nóng hoặc sau khi lửa đã bén. Tro không cho mình chọn một giả thuyết.",
        "Ghi vị trí và bọc phần còn lại. Ta sẽ so nó với khuôn lưu ở Dawnkeep trước khi nói ai từng cầm con dấu.",
    ]),
    ("ashfall_shelter_report", "report_to_alden", "alden_af_shelter_report", "CAPTAIN ALDEN VALE", [
        "Em đã đưa người tới chỗ trú và giữ lại những gì họ nói. Tôi sẽ ghi hai việc ấy riêng; một việc không chứng minh nguyên nhân của việc kia.",
        "Số người được cứu không thể thay cho lời khai về ai ra lệnh. Ta giữ cả hai câu hỏi cho tới khi có chứng cứ.",
    ]),
    ("ashfall_trail_report", "compare_seal_with_alden", "alden_af_seal_comparison", "CAPTAIN ALDEN VALE", [
        "Vết sáp gần với khuôn dự phòng của Order, nhưng bản lề dấu đã nứt trước khi bị đốt. Tôi không biết ai cầm nó lần cuối.",
        "Đây là một mối liên hệ, chưa phải nhận dạng người mang dấu. Ghi phần chắc chắn cạnh phần còn thiếu.",
    ]),
    ("side_ashfall_moonwort", "harvest_moonwort_for_mira", "rowan_af_moonwort_first_crop", "ROWAN HALE", [
        "Moonwort mở hai nụ ở luống ấm, còn mép đất chưa đâm chồi. Mira muốn cả lá khuyết được ghi vào mẫu.",
        "Một canh tưới trễ có thể đã ảnh hưởng. Vụ nhỏ này chưa hứa đủ thuốc cho mọi người đang ở mái hiên.",
    ]),
    ("side_ashfall_embermaw", "defeat_embermaw_matriarch", "rowan_af_matriarch_well", "ROWAN HALE", [
        "Matriarch rời giếng sau khi bị thương. Gió vẫn kéo tro lên dốc, nên vệt bụi quanh ổ có thể đã có từ hôm qua.",
        "Ta sẽ ghi dấu móng, hướng gió và giờ quay lại. Chúng không cho mình biết con thú tới đây vì lý do gì.",
    ]),
    ("side_field_af_ashbound_zombie", "defeat_ashbound_zombie", "rowan_af_ashbound_trace", "ROWAN HALE", [
        "Tro còn ấm trên chân Ashbound Zombie, nhưng thành giếng đã nguội. Dấu trên đất xác nhận nó đi qua đây, không chỉ ra nơi nó xuất hiện.",
        "Ghi lại lớp mưa phủ trên vệt chân để người sau biết thứ tự tương đối của hai dấu.",
    ]),
    ("side_field_af_grave_skeleton", "defeat_grave_skeleton", "rowan_af_grave_skeleton_trace", "ROWAN HALE", [
        "Một đốt xương văng tới hàng rào, các đốt khác nằm thành vệt ngắn cạnh mộ. Trận đánh làm xáo dấu cũ; ta đánh dấu chỗ nào đã bị tác động.",
        "Hàng rào không có vết phá mới. Ta chưa thể nói bộ xương đã đi qua cổng nào.",
    ]),
    ("side_field_af_ash_goblin", "defeat_ash_goblin", "rowan_af_goblin_footprints", "ROWAN HALE", [
        "Dấu chân Ash Goblin hướng về những thùng lương rỗng. Thùng đã được chuyển trước đó, nên đường đi không chứng minh nó lấy thức ăn.",
        "Tách dấu chân khỏi biên nhận kho. Hai hồ sơ có thể gặp nhau sau này mà không cần giả làm một câu trả lời.",
    ]),
    ("side_field_af_well_imp", "defeat_well_imp", "rowan_af_cinder_sparks", "ROWAN HALE", [
        "Tia sáng của Cinder Imp tắt trước khi chạm nền. Mình thấy vệt nóng trên ba viên đá, nhưng không tìm được điểm phát ra chúng.",
        "Ghi thời tiết và mặt đá; lần sau ta có thể so lại, thay vì gọi chớp lóe là dấu vết của ma thuật cổ.",
    ]),
    ("side_elite_af_ashvault_flameskull", "defeat_ashvault_flameskull", "rowan_af_flameskull_echo", "ROWAN HALE", [
        "Tiếng lửa trong Ashvault còn dội lại sau khi đốm sáng biến mất. Tường phía bắc trả âm chậm hơn vòm nứt.",
        "Đừng gộp tiếng vọng với tiếng gọi. Ta ghi vị trí từng lần nghe để người khác có thể thử lại khi gió lặng.",
    ]),
    ("side_verdant_af_1", "defeat_bat", "rowan_af_well_bat", "ROWAN HALE", [
        "Đàn dơi lướt sát mái giếng khi bóng râm dài thêm một viên gạch. Ta không thể đếm số con từ tiếng cánh; vài con có thể quay lại cùng đường bay.",
        "Ghi giờ và độ cao tương đối. Chuyển động này thuộc lượt quan sát hiện tại, không phải lịch cố định của cả đàn.",
    ]),
    ("side_verdant_af_1", "defeat_bee", "rowan_af_well_bees", "ROWAN HALE", [
        "Ong quay về chiếc máng vỡ, không phải hàng hoa phía nam. Đường bay khác đường của dơi dù cả hai băng qua cùng dải bóng râm.",
        "Ta không nối hai dấu thành một tổ. Gió đã đổi hướng giữa hai lượt ghi.",
    ]),
    ("side_verdant_af_2", "defeat_centaur", "rowan_af_centaur_tracks", "ROWAN HALE", [
        "Dấu móng của Centaur dừng trước hàng rào ngoài. Ba vết in có độ sâu khác nhau; mưa đêm qua có thể đã làm một dấu lún thêm.",
        "Chưa có vết móng phía bên kia. Ta chỉ ghi được tới đây, chưa phải một lộ trình trọn vẹn.",
    ]),
    ("side_verdant_af_2", "defeat_death_mage_elf", "rowan_af_mage_page", "ROWAN HALE", [
        "Mảnh giấy bạc mắc trên cọc chống có một câu bị cắt mất đầu. Mực và nét chữ không cho biết người chép có mặt ở trận nào.",
        "Ta kẹp tờ giấy giữa hai phiến phẳng. Nội dung chưa đủ để biến nó thành tuyên bố của cả đội.",
    ]),
    ("side_verdant_af_2", "defeat_death_cob", "rowan_af_death_cob_spores", "ROWAN HALE", [
        "Vệt bào tử dày ở chỗ nước đọng, thưa trên gờ khô. Sau khi trận đấu khuấy bùn, ranh giới đã nhòe đi một phần.",
        "Mẫu hôm nay chỉ cho thấy nơi ta nhặt được nó. Muốn biết mùa khác ra sao, phải quay lại bằng cùng cách đo.",
    ]),
    ("side_crawl_af_1", "defeat_black_bear", "rowan_af_bear_well_lane", "ROWAN HALE", [
        "Gấu đen chọn lối thấp dọc bờ giếng; vết cào trên rào cũ đã bạc màu, không trùng với dấu mới trên cỏ.",
        "Ta dọn lối đi để người qua lại, nhưng không ghi con thú là mối đe dọa cho cả mùa chỉ từ cuộc chạm trán này.",
    ]),
    ("side_crawl_af_1", "defeat_bog_body", "rowan_af_bog_body_reeds", "ROWAN HALE", [
        "Cọng sậy bám vào vai Bog Body có bùn mới ở đầu gãy và cặn khô gần rễ. Nó cho biết hai lớp đất đã chạm nhau, không cho biết cơ thể nằm ở đó bao lâu.",
        "Giữ mẫu riêng trước khi nước dâng và kéo phần còn lại đi.",
    ]),
    ("side_crawl_af_1", "defeat_ghoul", "rowan_af_ghoul_well_lane", "ROWAN HALE", [
        "Ghoul lao qua lối có hạt giống rơi, nhưng bao tải vẫn buộc kín. Ta không thấy dấu cắn trên từng hạt.",
        "Gideon sẽ kiểm lại niêm kho; còn trang field note này chỉ ghi dấu chân và nơi túi vải bị kéo lê.",
    ]),
    ("side_crawl_af_2", "defeat_anubis_guard", "rowan_af_anubis_mask", "ROWAN HALE", [
        "Mặt nạ của Anubis Guard nằm úp cạnh bếp tắt. Một bên phủ muội, bên kia có vết xước thẳng như bị kéo trên nền gạch.",
        "Ta ghi cả hai mặt và giữ khoảng cách với tro nóng; hiện vật không nói ai đã đặt nó xuống.",
    ]),
    ("side_crawl_af_2", "defeat_salamander", "rowan_af_salamander_stove", "ROWAN HALE", [
        "Lò nguội khi ta tới, còn dấu bò của Salamander dừng trước chân bệ. Nhiệt còn trong tro không cho biết ai đã đốt lửa trước đó.",
        "Ta để riêng mẫu than và vệt vảy. Hai dấu được tìm cạnh nhau, nhưng có thể có thời điểm khác nhau.",
    ]),
    ("side_ashfall_replant_moonwort", "harvest_second_moonwort", "rowan_af_moonwort_second_crop", "ROWAN HALE", [
        "Lứa thứ hai có lá dài hơn vì luống được che gió. Ta giữ lại một nhánh cùng ghi chú, để vụ sau Mira có thể thay cách che.",
        "Hai lần thu hoạch chưa đủ chứng minh khí hậu đã đổi; chúng chỉ cho thấy chăm sóc khác nhau tạo kết quả khác.",
    ]),
    ("side_ashfall_blackreed_record", "catch_blackreed_for_recipe", "rowan_af_blackreed_sample", "ROWAN HALE", [
        "Blackreed Trout cắn mồi ở mép nước có bóng mái cầu. Vảy ướt giữ một dải sáng xanh, còn mực nước đã thấp hơn vạch đá hôm qua.",
        "Ta ghi nơi và giờ bắt; một con cá không cho ta biết cả đàn đã chuyển đi đâu.",
    ]),
    ("side_ashfall_brew_moonlight", "brew_recorded_moonlight_tonic", "mira_af_moonlight_batch", "MIRA COLE", [
        "Mẻ này dịu hơn hôm qua vì Rowan để nước nguội trước khi thả lá. Viết cả nhiệt độ tương đối, không chỉ tên thuốc.",
        "Ai uống cũng có thể nói vị quá đắng hoặc quá ngọt; ta sẽ sửa công thức theo người thử, không theo một lời khen duy nhất.",
    ]),
    ("side_ashfall_two_bells_grow", "grow_signal_moonwort", "rowan_af_signal_moonwort", "ROWAN HALE", [
        "Moonwort ở luống sát tường giữ được phấn trên lá, còn luống ngoài hiên đọng nước mưa. Harper cần biết vị trí trước khi thử tín hiệu.",
        "Ta gửi cả lá đạt và lá dập; một phép thử công khai phải ghi phần nó không dùng được.",
    ]),
    ("side_ashfall_two_bells_mix", "craft_rainmark_chalk", "rowan_af_rainmark_mix", "ROWAN HALE", [
        "Mẻ Phấn Dấu Mưa bám rõ trên đá nhám nhưng mờ trên gỗ ướt. Harper có thể chọn vật liệu thử ở hai điểm, không lấy màu phấn làm lời hứa tín hiệu luôn nhìn thấy.",
        "Ghi lượng Moonwort và đồng tro đã dùng để lần sau pha lại được.",
    ]),
    ("side_ashfall_muster_open", "ask_mira", "mira_af_muster_roster", "MIRA COLE", [
        "Có người muốn đánh dấu mình đã tới; người khác chỉ cần chỗ ngủ mà không muốn tên lưu trong bảng. Tôi sẽ phát chăn trước rồi hỏi từng người.",
        "Một ô trống là thông tin chưa được trao, không phải một người còn thiếu mà chúng ta có quyền đi tìm.",
    ]),
    ("side_ashfall_blank_rows", "ask_gideon", "gideon_af_blank_rows", "GIDEON PARK", [
        "Ba hàng này để dành cho số chăn chưa kiểm lại, không phải ba người biến mất. Khi nhận thêm đồ, tôi ghi giờ và người giao.",
        "Nếu ai muốn tự ghi tên, tôi sẽ để họ cầm bút. Bảng này giúp chia việc; nó không phải cổng vào nơi trú.",
    ]),
]

CHOICES = {
    "ashfall_choice": {
        "shelter": ("rowan_af_choose_shelter", "ROWAN HALE", [
            "Mình chọn dựng chỗ trú trước. Mira đã gom người về giếng, còn Gideon cần thêm tay nâng khung mái; dấu chân phía đông có thể chờ một lượt.",
            "Không phải mình quên vết tích. Người đang đứng ngoài sân cần mái che ngay bây giờ.",
        ]),
        "trail": ("rowan_af_choose_trail", "ROWAN HALE", [
            "Mình theo dấu về phía đông trước khi gió phủ mất đường. Gideon có thể đưa mọi người tới mái hiên; mình sẽ quay lại với điều đã tìm thấy.",
            "Đây là thứ tự việc làm, không phải câu trả lời ai gây ra cuộc đột kích.",
        ]),
    }
}


def main():
    quests = json.loads(QUESTS_PATH.read_text(encoding="utf-8"))
    dialogue = json.loads(DIALOGUE_PATH.read_text(encoding="utf-8"))
    quests_by_id = {entry["id"]: entry for entry in quests["entries"]}
    dialogues_by_id = {entry["id"]: entry for entry in dialogue["entries"]}
    additions = {}
    linked = 0

    for quest_id, objective_id, dialogue_id, speaker, lines in OBJECTIVES:
        quest = quests_by_id.get(quest_id)
        if quest is None or quest.get("arcId") != "ashes_of_ashfall":
            raise SystemExit(f"Missing Ashfall quest: {quest_id}")
        found = [obj for obj in quest.get("objectives", []) if obj.get("id") == objective_id]
        if len(found) != 1:
            raise SystemExit(f"Expected one objective {quest_id}/{objective_id}, found {len(found)}")
        objective = found[0]
        if objective.get("dialogueId") not in (None, "", dialogue_id):
            raise SystemExit(f"Objective already points to another dialogue: {quest_id}/{objective_id}")
        objective["dialogueId"] = dialogue_id
        linked += 1
        additions[dialogue_id] = {"id": dialogue_id, "speakerName": speaker, "lines": lines}

    for quest_id, choice_ids in CHOICES.items():
        quest = quests_by_id.get(quest_id)
        if quest is None:
            raise SystemExit(f"Missing choice quest: {quest_id}")
        choices_by_id = {choice["id"]: choice for choice in quest.get("choices", [])}
        for choice_id, (dialogue_id, speaker, lines) in choice_ids.items():
            choice = choices_by_id.get(choice_id)
            if choice is None:
                raise SystemExit(f"Missing choice {quest_id}/{choice_id}")
            if choice.get("dialogueId") not in (None, "", dialogue_id):
                raise SystemExit(f"Choice already points to another dialogue: {quest_id}/{choice_id}")
            choice["dialogueId"] = dialogue_id
            additions[dialogue_id] = {"id": dialogue_id, "speakerName": speaker, "lines": lines}

    for dialogue_id, entry in additions.items():
        existing = dialogues_by_id.get(dialogue_id)
        if existing is not None and existing != entry:
            raise SystemExit(f"Dialogue ID already exists with different content: {dialogue_id}")
        if existing is None:
            dialogue["entries"].append(entry)

    QUESTS_PATH.write_text(json.dumps(quests, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    DIALOGUE_PATH.write_text(json.dumps(dialogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Linked {linked} Ashfall objective reactions and {sum(map(len, CHOICES.values()))} first-action responses; added {len(additions)} dialogue entries.")


if __name__ == "__main__":
    main()
