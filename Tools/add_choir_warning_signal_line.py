#!/usr/bin/env python3
"""Install the authored Choir warning-signal side story into its runtime catalogs."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: index for index, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


def quest(qid, title, objective, objective_id, kind, target, description, dialogue_id,
          prerequisite, reward_gold, reward_items=None):
    return {
        "id": qid,
        "arcId": "the_choir_beneath_the_lake",
        "stage": -1,
        "type": "side",
        "locationId": "choir_beneath_lake",
        "giverId": "tamsin_wren",
        "title": title,
        "objective": objective,
        "prerequisiteIds": [prerequisite] if prerequisite else [],
        "objectives": [{
            "id": objective_id,
            "kind": kind,
            "targetId": target,
            "requiredCount": 1,
            "description": description,
            **({"dialogueId": dialogue_id} if dialogue_id else {}),
        }],
        "reward": {"gold": reward_gold, "items": reward_items or []},
    }


dialogues = [
    {"id": "tamsin_signal_open", "speakerName": "TAMSIN WREN", "lines": [
        "Tôi từng lắp chuông báo nước cho hành lang phía tây. Sau khi phòng tập đóng cửa, không ai còn nhớ nhịp nào báo đường ngập.",
        "Ba hồi cũ nghe giống nhau khi đá giữ tiếng quá lâu. Người mới đến chạy theo âm vang, rồi đi sâu hơn vào chỗ nước đang dâng.",
        "Tôi muốn làm lại tín hiệu mà không bắt ai học thuộc lời giải thích. Một dấu phải báo được nguy hiểm ngay cả khi dấu kia bị nước nuốt mất."
    ]},
    {"id": "rowan_signal_bearing", "speakerName": "ROWAN HALE", "lines": [
        "Vòng đỡ bị nghiêng về phía lòng hồ. Vết xước chạy theo hướng lực kéo, còn mép kia phủ một lớp cát mịn đã bám từ lâu.",
        "Nó không ghi lại một trận lũ cụ thể. Tamsin nhận ra mẫu ren của xưởng cũ và nói chiếc vòng được lắp để thay nhanh bằng một tay.",
        "Nếu tín hiệu cần hai người mới sửa được, người thứ hai có thể đang ở bên kia hành lang khi còi vang."
    ]},
    {"id": "rowan_signal_channel", "speakerName": "ROWAN HALE", "lines": [
        "Rãnh dẫn vòng âm chạy dưới hai cột đá rồi tách làm đôi. Một nhánh đưa âm về phòng tập; nhánh còn lại kết thúc ở bức tường đá đặc.",
        "Trên lớp cặn có hai đường kéo mới hơn lớp cũ. Chúng cho biết nước đã xoay qua đây, không nói ai đã mở van hay vì sao.",
        "Tamsin đánh dấu cả hai nhánh trên sơ đồ. Chuông đặt giữa chúng có thể cho người nghe phương hướng, nhưng chưa chứng minh được khoảng cách."
    ]},
    {"id": "lyra_signal_review", "speakerName": "LYRA MOSS", "lines": [
        "Whisper Koi giữ tiếng gõ trong lớp vảy vài nhịp, nhưng mỗi con lại bơi qua một luồng nước khác. Tốt nhất là gọi nó một mẫu sống, không phải chiếc máy đo.",
        "Tamsin không cần tôi đặt tên cho tiếng chuông. Cô cần một nhịp có thể thử lại, cùng chỗ đứng và cùng khoảng chờ.",
        "Ghi cả lần chuông không vọng tới. Một cảnh báo thất bại cũng là kết quả mà người sửa sau này cần biết."
    ]},
    {"id": "tamsin_signal_brace_complete", "speakerName": "TAMSIN WREN", "lines": [
        "Bộ Chặn Xung đã giữ vòng đỡ khỏi trượt thêm. Tôi dùng tảo làm lớp đệm và để nguyên khe thoát nước; bịt kín cả khung chỉ đổi một kẹt cũ lấy một kẹt mới.",
        "Đưa nó tới khung cảnh giới phía dưới. Tôi sẽ đứng ở lối đối diện để nghe, còn Rowan có thể ghi lại điều thực sự đến được đó."
    ]},
    {"id": "rowan_signal_housing", "speakerName": "ROWAN HALE", "lines": [
        "Khung còn nguyên hai chốt nhưng vòng đỡ đã chạm vào đá. Gắn Bộ Chặn Xung vào rãnh trống sẽ giữ nó khỏi tự xoay khi nước đổi hướng.",
        "Vật liệu sẽ ở lại trong khung sau khi lắp. Nếu vòng vẫn rung lệch, ta có thể tháo chốt bảo dưỡng mà không phải đập vỡ phần tường."
    ]},
    {"id": "rowan_signal_test", "speakerName": "ROWAN HALE", "lines": [
        "Ba nhịp thử đều bắt đầu từ cùng một vạch sàn. Ở mực nước thấp, âm chạm cột bắc trước; khi áp lực tăng, dấu rung ở cột nam xuất hiện muộn hơn.",
        "Lần thứ hai, tôi đứng lệch khỏi vạch và ghi nhầm hướng. Tamsin giữ lại trang đó thay vì chép đè con số đã sửa.",
        "Khung đã báo một thay đổi. Ta vẫn chưa biết nước sẽ đổi nhanh đến đâu trong một trận lũ thật, nên chưa thể gọi nó là lời bảo đảm an toàn."
    ]},
    {"id": "warden_signal_review", "speakerName": "THE FIRST WARDEN", "lines": [
        "Một tín hiệu tốt phải được hiểu trước khi người nghe biết kỹ thuật phía sau nó. Hãy hỏi những người đi qua hành lang lần đầu xem dấu nào khiến họ dừng lại.",
        "Tamsin có thể chọn tiếng, ánh sáng hoặc cả hai. Không phương án nào thay được một lối thoát mở và một người chịu trách nhiệm kiểm tra khung."
    ]},
    {"id": "tamsin_policy_bell", "speakerName": "TAMSIN WREN", "lines": [
        "Hai tiếng ngắn sẽ là lời gọi dừng; một tiếng dài sau khoảng nghỉ báo lối phía bắc còn mở. Tôi sẽ khắc nhịp lên tấm đồng để người khác thay được.",
        "Nếu đá làm âm méo, người nghe vẫn có thể đếm khoảng nghỉ. Tôi sẽ để chỗ trống cho lần thử sau khi mùa nước đổi."
    ]},
    {"id": "tamsin_policy_lamp", "speakerName": "TAMSIN WREN", "lines": [
        "Chuông đôi vẫn là dấu chính, còn đèn nháy sẽ lặp nhịp cho những đoạn mà âm thanh không tới. Đèn cần được nhìn thấy từ hành lang, không phải từ phòng điều khiển.",
        "Ai đến sửa sẽ phải ghi rõ bóng đèn nào tắt và tiếng nào còn nghe được. Hai dấu riêng dễ kiểm tra hơn một khung kín không ai dám mở."
    ]},
    {"id": "rowan_signal_bell_trial", "speakerName": "ROWAN HALE", "lines": [
        "Tấm đồng ghi hai tiếng dừng và một tiếng gọi đường bắc, kèm khoảng lặng ở giữa. Dấu khắc có thể đọc bằng tay khi nước làm ánh đèn biến mất.",
        "Tôi để ngày thử đầu tiên cạnh ngày thay vòng. Nếu nhịp không còn đúng, người bảo trì có thể biết phép so sánh này đã cũ."
    ]},
    {"id": "rowan_signal_lamp_trial", "speakerName": "ROWAN HALE", "lines": [
        "Tấm chỉ dẫn đặt đèn ngang tầm mắt và chuông thấp hơn một sải tay. Hai tín hiệu không dùng cùng một nguồn điện hay cùng một giá đỡ.",
        "Mép giấy có sơ đồ kiểm tra từng dấu riêng. Nếu ánh sáng bị che, người trực vẫn phải ghi tiếng chuông; nếu chuông câm, đèn không tự chứng minh rằng cả đường đã thông."
    ]},
    {"id": "tamsin_signal_afterword", "speakerName": "TAMSIN WREN", "lines": [
        "Tôi đã dành nhiều năm sửa những thứ bị xem là cũ trước khi có người hỏi chúng từng dùng để làm gì. Lần này, họ hỏi cả cách kiểm tra sau khi tôi rời đi.",
        "Tôi sẽ không đóng cửa phòng tập nữa. Ai muốn học có thể tháo một vòng hỏng, lắp lại nó, rồi tự đứng ở đầu kia để nghe.",
        "Ngày mai tôi phải thay một chốt ở hành lang nam. Nó kêu lạch cạch mỗi lần cá bơi qua, và lần này tiếng ấy chỉ là tiếng chốt thôi."
    ]},
]

quests = [
    quest("side_choir_signal_open", "Tín hiệu dành cho người lạc đường",
          "Tamsin Wren muốn khôi phục một cảnh báo ngập nước từng dẫn khách rời khỏi phòng tập phía tây. Hãy nghe lý do cô bỏ nghề chuông và xác định phần nào còn dùng được.",
          "meet_tamsin", "talk", "tamsin_wren", "Nghe Tamsin kể vì sao tín hiệu cũ không còn đáng tin.",
          "tamsin_signal_open", "choir_reckoning", 8,
          [{"itemId": "echo_kelp_seed", "quantity": 1}, {"itemId": "earthworm_bait", "quantity": 3}]),
    quest("side_choir_signal_bearing", "Vòng đỡ trong tường chuông",
          "Một rãnh trên vòng đỡ bị kéo lệch khỏi hàng. Đọc dấu ren và cặn quanh nó trước khi quyết định có thể gia cố hay phải bỏ cả cụm.",
          "inspect_bearing", "inspect", "choir_signal_bearing", "Kiểm tra vòng đỡ và hướng của vết xước.",
          "rowan_signal_bearing", "side_choir_signal_open", 7),
    quest("side_choir_signal_sample", "Một mẫu nước biết giữ nhịp",
          "Lyra gợi ý dùng Whisper Koi làm mẫu đối chiếu, vì vảy cá giữ một phần tiếng gõ sau khi nó rời khỏi chuông. Câu một con ở Whisper Pool.",
          "catch_koi_sample", "fish", "whisper_koi", "Câu Whisper Koi ở Whisper Pool.",
          None, "side_choir_signal_bearing", 8),
    quest("side_choir_signal_channel", "Trục truyền dưới đáy vòm",
          "Đường dẫn âm thanh rẽ dưới các cột đá. Theo rãnh cặn để tìm nơi một tín hiệu có thể bị giữ lại, nhưng đừng suy từ hướng nước ra người đã xoay van.",
          "inspect_channel", "inspect", "choir_signal_channel", "Đọc hai nhánh của rãnh truyền âm.",
          "rowan_signal_channel", "side_choir_signal_sample", 9),
    quest("side_choir_signal_lyra", "Lyra nghe từ phía hành lang",
          "Lyra sẽ giúp chọn nhịp thử nếu có thể giữ riêng phần đo của cô với lời kể của Tamsin. Hỏi cô cách dùng Whisper Koi mà không biến một mẫu thành câu trả lời.",
          "ask_lyra", "talk", "lyra_moss", "Nghe Lyra đề xuất cách so sánh tiếng chuông.",
          "lyra_signal_review", "side_choir_signal_channel", 8),
    quest("side_choir_signal_kelp", "Sợi tảo cho lò xo",
          "Hái Echo Kelp ở luống hồ. Lá tảo làm lớp đệm cho vòng đỡ, nhưng cần chừa khe để nước và cát thoát ra khi áp lực đổi.",
          "grow_kelp", "grow", "echo_kelp", "Trồng và thu hoạch Echo Kelp.",
          None, "side_choir_signal_lyra", 9),
    quest("side_choir_signal_brace", "Khung chặn xung",
          "Dùng một Echo Kelp và một Whisper Koi ở Choir Harmonic Anvil để rèn Bộ Chặn Xung. Công thức giữ khe thoát nước hở để khung không khóa cứng khi đổi áp lực.",
          "craft_brace", "craft", "choir_pulse_brace", "Rèn Bộ Chặn Xung tại Choir Harmonic Anvil.",
          None, "side_choir_signal_kelp", 10),
    quest("side_choir_signal_mount", "Lắp khung vào chuông cảnh giới",
          "Tamsin chờ ở đầu hành lang đối diện. Lắp Bộ Chặn Xung vào khung cảnh giới để vòng đỡ không trượt thêm; nhạc cụ sẽ ở lại nơi lắp.",
          "install_brace", "interact", "choir_signal_housing", "Lắp Bộ Chặn Xung vào khung cảnh giới.",
          "rowan_signal_housing", "side_choir_signal_brace", 11),
    quest("side_choir_signal_test", "Ba lần thử ở áp lực khác nhau",
          "Đọc bảng ghi ba lượt thử và cả lần Rowan đứng sai vạch. Khung hoạt động trong những lần đo này, nhưng chưa trải qua một trận nước dâng thật.",
          "read_pressure_trials", "inspect", "choir_signal_trial_table", "Đọc ba lượt đo và sai số được giữ lại.",
          "rowan_signal_test", "side_choir_signal_mount", 10),
    quest("side_choir_signal_warden", "First Warden kiểm tra nhịp báo",
          "The First Warden yêu cầu thử cách hiểu của người đi qua hành lang trước khi chọn âm báo cuối. Hỏi ông điều gì không thể thay bằng một dấu hiệu đẹp mắt.",
          "warden_review", "talk", "first_warden", "Hỏi The First Warden về trách nhiệm duy trì tín hiệu.",
          "warden_signal_review", "side_choir_signal_test", 10),
]

choice = quest("side_choir_signal_policy", "Một hồi dài hay hai dấu riêng",
               "Tamsin có thể dùng hai nhóm tiếng chuông với khoảng nghỉ dễ đếm, hoặc ghép chuông với đèn nháy cho những hành lang bị đá chặn âm. Chọn cách cô sẽ dạy cho người trực sau này.",
               "choose_warning_design", "choice", "choir_signal_design_table",
               "Chọn sơ đồ cảnh báo cho phòng tập phía tây.", None,
               "side_choir_signal_warden", 12)
choice["choiceFlag"] = "choir_warning_policy"
choice["choiceSpeaker"] = "TAMSIN WREN"
choice["choicePrompt"] = (
    "Tôi có thể khắc một nhịp chuông đôi với khoảng nghỉ rộng để người nghe đếm được ngay cả khi âm bị méo. "
    "Hoặc ta giữ nhịp chuông làm dấu chính rồi thêm đèn nháy ở nơi tiếng không tới. Mỗi dấu bổ sung lại cần người kiểm tra, "
    "nguồn thay thế và trang ghi hỏng riêng. Tôi không muốn bảng hiệu nói rằng đường đã an toàn; nó chỉ cho biết "
    "tín hiệu nào vừa được thử và tín hiệu nào cần người trực xác nhận."
)
choice["choices"] = [
    {"id": "paired_bells", "label": "Dùng nhịp chuông đôi và khoảng nghỉ rộng.",
     "flagValue": "paired_bells", "dialogueId": "tamsin_policy_bell",
     "reward": {"gold": 0, "items": [{"itemId": "choir_two_tone_emblem", "quantity": 1}]}},
    {"id": "bell_and_lamp", "label": "Ghép chuông với đèn nháy ở đoạn khuất âm.",
     "flagValue": "bell_and_lamp", "dialogueId": "tamsin_policy_lamp",
     "reward": {"gold": 0, "items": [{"itemId": "choir_light_echo_emblem", "quantity": 1}]}},
]
quests.append(choice)

bell_route = quest("side_choir_signal_bell_trial", "Tiếng đôi qua cột đá",
                   "Tấm đồng ghi cách đếm hai tiếng dừng và tiếng gọi lối bắc. Soát lại nhịp cùng khoảng nghỉ để một nhóm sửa chữa có thể thay chuông mà không phải đoán ý người lắp.",
                   "read_bell_pattern", "inspect", "choir_bell_pair_pattern",
                   "Đọc nhịp chuông đôi và ngày thử được khắc trên tấm đồng.",
                   "rowan_signal_bell_trial", "side_choir_signal_policy", 12)
bell_route["branchFlag"] = "choir_warning_policy"
bell_route["branchValue"] = "paired_bells"
quests.append(bell_route)

lamp_route = quest("side_choir_signal_lamp_trial", "Ánh gọi khi tiếng không truyền",
                   "Sơ đồ đèn giữ một nguồn tín hiệu thứ hai ở các nhánh hành lang khuất âm. Kiểm tra vị trí lắp, đường dây và dấu cần ghi riêng khi chuông hoặc đèn hỏng.",
                   "read_lamp_pattern", "inspect", "choir_paired_light_pattern",
                   "Đọc sơ đồ kiểm tra chuông và đèn theo hai lượt riêng.",
                   "rowan_signal_lamp_trial", "side_choir_signal_policy", 12)
lamp_route["branchFlag"] = "choir_warning_policy"
lamp_route["branchValue"] = "bell_and_lamp"
quests.append(lamp_route)

afterword = quest("side_choir_signal_afterword", "Tamsin rời phòng thử",
                  "Một trong hai sơ đồ đã được ghi lại cùng ngày thử và lối để bảo dưỡng. Hỏi Tamsin cô sẽ làm gì sau khi phòng tập mở cửa lại.",
                  "talk_after_signal", "talk", "tamsin_wren", "Nghe Tamsin kể kế hoạch dạy người khác tự bảo trì.",
                  "tamsin_signal_afterword", None, 16)
afterword["prerequisiteGroups"] = [{"anyOfQuestIds": [
    "side_choir_signal_bell_trial", "side_choir_signal_lamp_trial"
]}]
quests.append(afterword)

items = [
    {"id": "choir_pulse_brace", "name": "Bộ Chặn Xung", "description": "Một vòng đỡ nhẹ bọc Echo Kelp và cân theo tiếng Whisper Koi. Khe thoát nước được giữ mở để áp lực không khóa cứng khung cảnh giới.", "category": "quest", "equipmentSlot": "", "maxStack": 1, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "choir_two_tone_emblem", "name": "Huy Hiệu Hai Nhịp", "description": "Huy hiệu của nhóm trực chuông đôi. Những khoảng nghỉ rộng dễ đếm khi âm vang bị kéo dài qua cột đá. Tăng 1 Công và 1 Giáp.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 36},
    {"id": "choir_light_echo_emblem", "name": "Huy Hiệu Đèn Vọng", "description": "Một thẻ đồng nhắc người trực thử chuông và đèn riêng rẽ ở các hành lang khuất âm. Tăng 1 Công và 2 Giáp.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 2, "healAmount": 0, "sellValue": 36},
]
recipes = [{
    "id": "forge_choir_pulse_brace", "displayName": "Rèn Bộ Chặn Xung", "stationId": "choir_harmonic_anvil",
    "discipline": "smithing", "outputItemId": "choir_pulse_brace", "outputQuantity": 1,
    "ingredients": [{"itemId": "echo_kelp", "quantity": 1}, {"itemId": "whisper_koi", "quantity": 1}],
}]

landmarks = [
    {"id": "tamsin_wren_marker", "locationId": "choir_beneath_lake", "displayName": "Tamsin Wren", "targetId": "tamsin_wren", "visualId": "choir_diver", "positionX": 5.1, "positionY": -1.1, "scale": 0.085},
    {"id": "choir_signal_bearing_marker", "locationId": "choir_beneath_lake", "displayName": "Tilted Bell Bearing", "targetId": "choir_signal_bearing", "visualId": "document", "positionX": -1.3, "positionY": 3.8, "scale": 0.085},
    {"id": "choir_signal_channel_marker", "locationId": "choir_beneath_lake", "displayName": "Submerged Resonance Channel", "targetId": "choir_signal_channel", "visualId": "signal_frame", "positionX": 3.0, "positionY": -4.5, "scale": 0.085},
    {"id": "choir_signal_housing_marker", "locationId": "choir_beneath_lake", "displayName": "West Practice Warning Frame", "targetId": "choir_signal_housing", "visualId": "signal_frame", "positionX": 6.2, "positionY": 4.5, "scale": 0.085},
    {"id": "choir_signal_trial_table_marker", "locationId": "choir_beneath_lake", "displayName": "Pressure Trial Sheet", "targetId": "choir_signal_trial_table", "visualId": "document", "positionX": -5.8, "positionY": -4.5, "scale": 0.085},
    {"id": "choir_signal_design_table_marker", "locationId": "choir_beneath_lake", "displayName": "Warning Rhythm Board", "targetId": "choir_signal_design_table", "visualId": "noticeboard", "positionX": -10.4, "positionY": 4.0, "scale": 0.085},
    {"id": "choir_bell_pair_pattern_marker", "locationId": "choir_beneath_lake", "displayName": "Paired Bell Pattern Plate", "targetId": "choir_bell_pair_pattern", "visualId": "signal_bell_test", "positionX": 8.7, "positionY": 1.0, "scale": 0.085},
    {"id": "choir_paired_light_pattern_marker", "locationId": "choir_beneath_lake", "displayName": "Paired Light Service Sheet", "targetId": "choir_paired_light_pattern", "visualId": "signal_flag_test", "positionX": -10.3, "positionY": -1.4, "scale": 0.085},
]

codex = [
    {"id": "choir_warning_install_record", "title": "The West Practice Warning Frame", "category": "Maintenance record", "writtenBy": "Tamsin Wren", "unlockQuestId": "side_choir_signal_test", "body": "Tamsin Wren repaired the west practice frame with a loose bearing, two sediment tracks, and an open drainage gap. Rowan mounted a kelp-padded pulse brace without sealing the cavity. The fit was checked in three controlled runs from the same floor mark. At low water the north column carried the first vibration; at higher pressure the south marker arrived later. One reading was taken from the wrong mark and kept beside its correction.\n\nThese trials show that the frame can carry a signal under the conditions written on the sheet. They do not reproduce a fast flood or guarantee that every passage remains open. The record asks future keepers to repeat the test after the water season changes, inspect both fasteners, and leave a clear route to remove the brace. A warning is useful only while someone can still service it."},
    {"id": "choir_warning_bell_method", "title": "Paired Bell Rhythm and Rest", "category": "Signal procedure", "writtenBy": "Tamsin Wren", "unlockQuestId": "side_choir_signal_bell_trial", "body": "The paired-bell procedure uses two short strikes to call a stop, then one longer strike after a broad rest to mark the north passage. The rest is part of the signal: it gives a listener time to separate the echo from the first impact. A small bronze plate carries the sequence so a replacement keeper can test it without learning the old crew's private shorthand.\n\nThe plate also records the day the frame was fitted. Stone can stretch or fold a sound across a gallery, and a familiar rhythm does not prove that the route beyond the bell is clear. Keepers should walk the passage after a test, mark any silent station, and replace a damaged chime rather than tightening it until it can no longer drain. The procedure is a repeatable call, not an assurance of safety."},
    {"id": "choir_warning_lamp_method", "title": "Bell and Lamp Service Sheet", "category": "Signal procedure", "writtenBy": "Tamsin Wren", "unlockQuestId": "side_choir_signal_lamp_trial", "body": "The bell remains the west practice hall's primary signal. In sections where stone interrupts its sound, a lamp flashes the same stop and passage pattern from a separate wall bracket. The sheet places the lamp at a listener's eye height and the bell below it; their supports and power sources are inspected independently. A working lamp must not conceal a silent bell, and a clear ring cannot verify a dark fixture.\n\nAt every seasonal service, a keeper should mark each device as tested, failed, or not reached. The sheet leaves space for a missing observation instead of copying last season's result. A disconnected wire and a flooded passage are different findings. The paired arrangement adds another component to maintain, but also leaves one recognizable signal when the other cannot travel through the corridor."},
    {"id": "choir_warning_return_record", "title": "A Room Open for Practice", "category": "Workshop note", "writtenBy": "Tamsin Wren", "unlockQuestId": "side_choir_signal_afterword", "body": "Tamsin reopened the practice room with a bearing that students can remove using one hand and a maintenance sheet with room for failed tests. She plans to teach the next keeper by asking them to stand at the far end, hear the call, and repeat the fitting themselves. The lesson begins with the loose frame rather than the finished diagram.\n\nThe chosen signal reflects the tools available to this shift and can be reviewed when the water changes. Neither the bell plate nor the lamp sheet promises that an unvisited corridor is safe. Tamsin kept a blank line for the next keeper's date, because the room now belongs to those who will test it again."},
]

catalog = read("prologue_quests.json")
upsert(catalog["entries"], quests)
write("prologue_quests.json", catalog)

catalog = read("dialogue_catalog.json")
upsert(catalog["entries"], dialogues)
write("dialogue_catalog.json", catalog)

catalog = read("codex_catalog.json")
upsert(catalog["entries"], codex)
write("codex_catalog.json", catalog)

catalog = read("item_catalog.json")
upsert(catalog["entries"], items)
write("item_catalog.json", catalog)

catalog = read("recipe_catalog.json")
upsert(catalog["entries"], recipes)
write("recipe_catalog.json", catalog)

catalog = read("quest_landmarks.json")
upsert(catalog["entries"], landmarks)
write("quest_landmarks.json", catalog)

print(f"Installed {len(quests)} Choir quests, {len(dialogues)} dialogues, {len(codex)} field records, ")
print(f"{len(items)} items, {len(recipes)} recipe, and {len(landmarks)} objective landmarks.")
