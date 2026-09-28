#!/usr/bin/env python3
"""Add field-specific second readings to the Cinderwell Pressure Wheel archive."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS_PATH = ROOT / "Assets/Resources/Content/prologue_quests.json"
CODEX_PATH = ROOT / "Assets/Resources/Content/codex_catalog.json"
MARKER = "\n\nGhi chú lượt đo tiếp theo —"

NOTES = {
    "cinder_wheel_bearing_record": """Ghi chú lượt đo tiếp theo — căn trục trước khi hỏi ai đã khóa bánh

Rowan đặt một dải phấn qua mặt ổ trục rồi thử xoay bánh bằng tay. Dấu phấn tách ở đường rãnh thứ ba; nó cho thấy bánh chưa ngồi phẳng, không cho biết người cuối cùng lắp nó. Talia bảo cậu tháo lớp bùn ở mép ngoài trước, vì mạt kim loại mắc dưới chốt có thể làm một ổ trục tốt trông như bị khoan lệch. Sau khi làm sạch, cả ba đường khắc vẫn còn nguyên.

Cậu vẽ hướng của chúng trên mặt cắt riêng và đặt bản vẽ cũ cạnh hình mới. Hai thiết kế dùng cùng ký hiệu cho chốt, nhưng bản mới có thêm một khe để xả nước đọng. Không có dấu nào cho biết khe ấy đã được dùng khi van bị khóa. Talia giữ lại cả hai hình thay vì gạch bỏ bản đầu: người sửa sau cần thấy nơi hai phiên bản khác nhau, không chỉ biết bản nào tiện lắp hơn hôm nay.""",
    "cinder_wheel_lesson_record": """Ghi chú lượt đo tiếp theo — bài học không phải bản vẽ vận hành

Talia mở lại sổ học nghề và nhận ra mình đã chép câu hỏi của Merrick Ashford ở lề trang sau một bài kiểm tra hỏng. Khi đó cô tin ông muốn cô đoán chiếc bánh nào đúng. Sau nhiều năm, cô hiểu bài học khác đi: phải mô tả thứ đang ở trước mắt trước khi chọn một sơ đồ để thử. Bài học ấy không cho biết Merrick từng nhìn thấy chiếc bánh Lower Cistern hay chỉ dạy trên mô hình.

Cô ghi điều này bên cạnh lời kể của mình, để một học trò khác không nhầm ký ức của người thợ với hồ sơ lắp đặt. Rowan hỏi có nên tìm những người cùng lớp với cô không. Talia muốn hỏi họ, nhưng yêu cầu giữ riêng ba thứ: ngày họ học, vật họ từng sửa và điều họ nghe kể về hầm. Một câu trả lời có thể giúp định vị cuốn sổ; nó vẫn cần được đối chiếu với sắt, đá và mực nước tại chỗ.""",
    "cinder_pressure_marks_record": """Ghi chú lượt đo tiếp theo — phấn có thể đổi chỗ khi người ta dọn mương

Rowan làm một dải thước giấy với các ô cách đều nhau rồi áp nó cạnh từng vệt vôi. Talia giữ đầu còn lại, không kéo căng đến mức giấy che mất mép sần của dầm. Họ đọc khoảng cách từ cùng một góc, sau đó đổi chỗ đứng và đọc lại. Hai nhóm rộng vẫn gần nhau; nhóm thứ ba vẫn nhỏ hơn nhưng nằm sát một đường nứt mới có thể đã làm thước nghiêng.

Trên phiếu, Talia ghi ai cầm thước và mặt dầm nào hướng về cửa xả. Cô cũng đánh dấu một vùng chưa đo được vì lớp muối che mất điểm bắt đầu. Nếu người gác dọn vôi để đọc tốt hơn, lượt kế tiếp phải chụp hoặc vẽ lại bề mặt trước khi lau. Một nét trắng còn lại sau nhiều mùa có thể là dấu nước, bột sửa tường hoặc cả hai; vị trí chính xác và ngày kiểm tra khiến người đọc sau có cơ hội phân biệt chúng.""",
    "brineglass_moss_bed_record": """Ghi chú lượt đo tiếp theo — giường rêu chỉ kể về giường rêu

Talia chia luống thử thành ba phần: rêu Brineglass Moss đang mọc, khay đối chứng không cấy và dải đất để trống cạnh chân tường. Rowan đánh số khay bằng cọc gỗ đặt ngoài mặt đất để nước tưới không xóa nhãn. Sau một lượt tưới nhỏ, cặn nhìn thấy bám lại trên vài thân rêu; phần còn lại lắng xuống khay thấp hơn. Họ không cân được hạt nhỏ nhất và không thử các chất tan mà mắt thường không thấy.

Moss mọc tốt hơn ở mặt tường ít nắng trong hai lần quan sát. Talia yêu cầu ghi hướng sáng chứ không viết “thích bóng râm” thành quy luật chung. Một hàng nhỏ, một bề mặt đá và hai lượt tưới chưa mô tả được cả hầm. Vật liệu thu được được rửa khỏi mẫu đo rồi chuyển sang recipe màng lọc thử nghiệm. Không dùng phần rêu ấy làm thức ăn, và không đổ mẫu nước trở lại hồ.""",
    "cinder_backwash_wall_record": """Ghi chú lượt đo tiếp theo — mặt tường ướt không chỉ về một hướng

Vệt bùn trên vách khô dần từ rìa, để lại một đường sẫm sát khe phụ. Talia đánh dấu hai đầu vệt và đặt một mảnh vải sạch bên dưới để hứng cặn có thể rơi. Rowan tìm thấy một đường xước đi ngược chiều dòng nhỏ trong máng, nhưng mặt đá có thể đã bị chạm khi người ta kéo dụng cụ qua. Hai dấu nằm gần nhau; chúng không tự xác nhận cùng thời điểm.

Ở bản đồ, Talia dùng mũi tên liền cho dòng cô nhìn thấy trong lượt thử, mũi tên nét đứt cho hướng suy ra từ lớp bùn. Cô muốn người đọc có thể xóa giả thuyết mà không làm mất quan sát ban đầu. Nếu lần sau vách khô hoàn toàn, ghi rằng không còn thấy đường ướt thay vì vẽ lại nó từ trí nhớ. Sự khác nhau giữa “không quan sát được” và “không có” giữ cho một dấu vết yếu không biến thành kết luận về người đã vận hành cửa xả.""",
    "cinder_pressure_wight_record": """Ghi chú lượt đo tiếp theo — tiếng va chạm không phải nhịp máy

Sau trận, Talia đếm các vết lõm trên vỏ đồng của Pressure Wight và tách chúng khỏi các vòng tròn mà đòn nện để lại trên nền. Vệt sáng dưới chân nó xuất hiện trước cú đập, đủ lâu để Rowan lướt khỏi vùng nguy hiểm. Cô ghi nhịp báo đòn theo từng lần chạm trán, nhưng không dùng nó làm đơn vị đo của bánh xe. Sinh vật chọn thời điểm tấn công; bánh xe quay theo áp lực và vị trí chốt.

Lõi thấu áp được gỡ khỏi lớp vỏ khi khu vực đã yên. Talia muốn giữ một mảnh đồng chưa nung lại để so độ cong với thiết kế. Rowan hỏi có thể gọi những vết trên giáp là công việc của kỹ sư cũ không. Cô từ chối: kim loại biến dạng sau nhiều lần chạm và trận chiến vừa xảy ra. Hồ sơ giao cho xưởng cả mẫu trước lẫn mẫu sau khi làm sạch, để phép đo không xóa mất thứ tự xử lý.""",
    "cinder_pressure_lens_record": """Ghi chú lượt đo tiếp theo — hai người đọc cùng một cạnh nứt

Rowan đặt thấu áp trên vải tối, còn Talia giữ đèn ở ba khoảng cách đã đánh dấu trên nền. Từ gần, vết nứt trông sâu hơn; từ xa, cạnh phản quang biến mất trước khi đường nứt kết thúc. Họ đổi vị trí cho nhau và ghi lại cả hai lần đọc. Không ai dùng dụng cụ sắc để dò vào khe, vì một mảnh nhỏ có thể bung ra khi mặt thấu áp chịu lực trở lại.

Talia gửi hình vẽ cho Tomas Reed cùng yêu cầu kiểm tra ứng suất ở xưởng khô. Cô không muốn Rowan lắp mảnh vỡ làm kim chỉ thị mới dù nó trong hơn kính hiện tại. Một cạnh nứt có thể chia luồng sáng thành nhiều vệt và làm người đọc tin có hai mức áp lực. Bản vẽ chỉ mô tả mặt ngoài dưới nguồn sáng cụ thể; phép đo chịu tải thuộc về thử nghiệm khác, với khung chắn và người giám sát riêng.""",
    "cinder_pressure_report_record": """Ghi chú lượt đo tiếp theo — giữ những câu hỏi trong cùng tập hồ sơ

Talia kẹp các trang theo thứ tự hành động: dọn lối, nhận diện dấu, trồng rêu, làm sạch mẫu, thử màng lọc và đọc mặt số. Cô thêm một cột “chưa biết” bên cạnh quan sát để người sao chép không phải nhét suy đoán vào lề. Rowan đề nghị gửi bản tường trình cho đội vận hành trước khi quyết định tay gạt. Talia đồng ý gửi, nhưng yêu cầu cả trang sai số đi cùng.

Cô còn nhớ ca khẩn năm đó và lý do mình ký lệnh khóa: bản dự báo nói kho giống cần được giữ nguyên. Hồ sơ mới không khiến lựa chọn cũ bớt nghiêm trọng. Nó chỉ tách điều cô biết lúc ký khỏi kết quả cô không đo sau đó. Những người mất nước trong ca ấy có quyền đọc cả hai. Talia muốn họ sửa nếu tìm ra nguồn khác, và muốn tên của người sửa xuất hiện bên cạnh dòng được thay đổi.""",
    "cinder_filter_recipe_record": """Ghi chú lượt đo tiếp theo — recipe cần ghi cả lần thất bại

Talia thử nén rêu Brineglass Moss vào hai tấm lưới đồng. Lớp thứ nhất quá chặt, làm nước đọng ở mép; lớp thứ hai quá thưa để giữ phần cặn có thể nhìn thấy. Rowan phác lại khoảng cách mắt lưới và ghi khối lượng moss trước khi rửa. Recipe giữ các tỷ lệ của lần lắp đang dùng, còn hai mẫu không đạt được đánh dấu “không tái sử dụng”.

Hỗn hợp hạt keo giữ phần lưới tại chỗ khi màng được đặt vào khung. Chất kết dính tiêu hao sau khi thử, vì vậy mỗi lần lắp đòi một mẻ mới và một phiếu vật liệu. Cô không muốn thợ cạo lớp đã thử rồi trộn vào batch sau; cặn thu được có thể làm đổi độ dày. Một pattern đáng tin cậy phải cho biết điều gì xảy ra khi thay đổi cỡ lưới, không chỉ tên nguyên liệu của bản lắp cuối.""",
    "cinder_filter_test_record": """Ghi chú lượt đo tiếp theo — phép thử giữ cặn không phải phép thử nước uống

Rowan chia một cốc mẫu thành hai lọ: một lọ trước màng, một lọ sau màng. Talia đợi phần lắng ổn định rồi so độ đục nhìn thấy qua vạch thủy tinh. Lọ thứ hai trong hơn ở đúng một góc sáng, nhưng còn một lớp mịn bám quanh đáy. Cô đánh dấu nguồn đèn, thời gian chờ và cách giữ hai lọ ngang nhau. Đây là phép quan sát cặn, không phải phân tích toàn bộ thứ hòa tan trong nước.

Màng giữ được một phần bùn trong lượt ấy và vẫn để dòng chảy qua. Talia ghi rõ đã có cốc nào rò ở cạnh khung, cốc nào bị lắc trên đường mang về. Nếu người khác lặp lại, họ cần cùng thể tích, cùng thời gian lắng và một lọ đối chứng chưa qua màng. Cô không ghi “đã lọc sạch” trên bảng dân cư. Họ chưa thử vi sinh, muối hòa tan hay tác động của nhiều chu kỳ sử dụng.""",
    "cinder_pressure_dial_record": """Ghi chú lượt đo tiếp theo — để mặt số nguội trước lần lặp

Talia nhận thấy kim về mốc chậm hơn khi đồng hồ đặt gần vách ấm. Cô không biết nhiệt làm đổi cơ cấu hay người đọc chỉ nhìn kim ở một góc khác. Rowan chuyển giá đỡ sang nền khô cách tường ba bước rồi đợi mặt số nguội giữa hai lượt. Lần mới mất ít nhịp hơn, nhưng hai người cũng đã bắt đầu đếm cùng lúc bằng tiếng gõ trên bàn.

Cô ghi cả phương pháp cũ và mới, không thay giá trị 17/19 bằng một con số trung bình. Nếu có thể, lần sau một người quan sát kim còn người kia bấm giờ bằng đồng hồ độc lập. Nếu không, phải ghi chính xác ai đếm và có dùng nhịp gõ hay không. Mặt số đo chuyển động của kim trong điều kiện của nó; nó không tự nói bánh đã làm gì trước khi họ đến.""",
    "talia_cistern_signature_record": """Ghi chú lượt đo tiếp theo — chữ ký được đọc cùng ngày tháng

Talia đặt chữ ký hiện tại dưới bản sao lệnh cũ, không đặt lên hàng trống dành cho người duyệt tiếp theo. Cô viết hôm nay mình đã được xem những gì: vị trí ba vệt vôi, một lõi thấu áp có nứt, và phiếu lọc cặn của một lượt. Cô chưa xem đủ hồ sơ nhận nước để biết ai chịu ảnh hưởng sau lệnh khóa. Cách liệt kê ấy giúp người thân tìm được câu hỏi cụ thể thay vì phải chấp nhận lời xin lỗi chung.

Rowan hỏi liệu cô có ký một lệnh như vậy lần nữa không. Talia nói cô cần xem phép đo, người sẽ giữ quyền mở van và cách cư dân khiếu nại trước. Cô không thể hứa câu trả lời trước khi biết điều kiện hôm ấy. Một chữ ký chịu trách nhiệm cho quyết định, nhưng ngày ký và giấy tờ đi cùng nó mới cho biết quyết định được đưa ra trong hoàn cảnh nào. Cô để một dòng trống cho người rà soát sau.""",
    "cinder_ratchet_bracket_record": """Ghi chú lượt đo tiếp theo — chốt phải dừng trước khi bánh dừng

Rowan chạy tay gạt qua ba nấc khi trục chưa nhận tải, rồi lặp lại với một dòng nước nhỏ. Ở nấc cuối, khung rung nhẹ và chốt thép chạm cạnh khe. Talia yêu cầu dừng thử ở đó, tháo lò xo và xem có mạt kim loại mới không. Một tiếng va đủ rõ để nghe không phải là dấu hiệu rằng cơ cấu có thể chịu nhiều lần mở đóng.

Họ đặt một tấm gỗ chắn phía sau để vết trượt không lẫn với dấu cũ trên tường. Người trực sau được dạy cách nhìn điểm dừng, nhưng không bị giao nhiệm vụ ép tay gạt về hết hành trình nếu nó mắc. Talia muốn dòng hướng dẫn có một bước gọi thợ trước khi nói đến thao tác khẩn cấp. Cơ cấu có thể giới hạn một chuyển động sai; nó không thay thế việc kiểm tra dầm, chốt và đường thoát nước.""",
    "cinder_bypass_policy_review": """Ghi chú lượt đo tiếp theo — ghi cả thời gian chờ của hai phương án

Talia treo một đồng hồ cát cạnh bảng chốt chung và một tấm bảng trống cạnh sổ người giữ ca. Cô ghi mất bao lâu để tìm đúng hướng dẫn, mất bao lâu để báo một dấu mới và ai có thể trả lời vào ban đêm. Tay gạt công khai ngắn đường từ câu hỏi tới thao tác, nhưng người sử dụng phải đọc đúng vạch và biết khi nào dừng. Lịch ca giúp có người theo dõi van, nhưng một lượt bị bỏ trống có thể kéo dài thời gian chờ.

Hai cách không thể so bằng tổng nước duy nhất. Talia thêm ba cột: ai được thao tác, nơi lưu khiếu nại và lối báo nguy cơ khẩn cấp. Người dân được mời đọc bản nháp, không phải chọn thay ngay tại cuộc họp. Cô muốn lần rà tiếp theo đếm số yêu cầu chưa được trả lời mà không đưa tên người gửi lên bảng chung.""",
    "cinder_shared_rill_record": """Ghi chú lượt đo tiếp theo — quyền dùng đi cùng quyền dừng

Hai cư dân thử chốt vào ngày khô và một người mang bản hướng dẫn ra đọc cạnh mương. Họ phát hiện mực chỉ bị rêu che ở góc thấp, nơi trẻ nhỏ thường ngồi đợi nước. Talia dời tấm hướng dẫn lên cao hơn nhưng để lại bản vạch cũ trong sổ, để biết dấu nào đã bị thay và khi nào. Một chốt cứng giới hạn hành trình; người vận hành vẫn cần cách báo nếu lớp sắt mòn.

Ai cũng có quyền không chạm vào tay gạt. Nếu ai nhìn thấy nứt hoặc nghe tiếng lạch cạch mới, có thể treo thẻ tạm dừng lên cán và báo người trực. Thẻ không khóa dòng nước, vì nó chỉ là thông báo cho người đến sau. Rowan ghi thao tác đã thử bằng dòng nhỏ, không gọi đó là phép đo lưu lượng cho cả mùa. Bản hướng dẫn cho phép điều chỉnh trong một ngưỡng; nó không hứa hẹn rằng từng hộ sẽ nhận lượng nước bằng nhau.""",
    "cinder_steward_schedule_record": """Ghi chú lượt đo tiếp theo — ca trực cần một người được phép nghỉ

Talia thêm cột “chưa có người nhận ca” sau khi hai người cùng gạch tên khỏi một khung giờ. Cô không tự điền tên người thay thế mà ghi ai đã được báo và lúc nào cần hỏi lại. Trước đây, bảng lịch được chép như thể người trực luôn có mặt; một lần vắng biến thành một cột bỏ trống mà không ai biết có chuyện gì xảy ra. Bản mới lưu cả khoảng trống và cách chuyển việc.

Người giữ ca có thể yêu cầu hoãn hoặc đổi ca mà không giải thích việc riêng của mình trên bảng ngoài. Người đang chờ biết thời điểm hỏi lại, còn người nhận ca sau được phép đọc tình trạng van trước khi nhận trách nhiệm. Talia ghi rằng lịch này cần đủ người tự nguyện mới vận hành; giấy phân công không tạo ra người trực. Nếu thiếu người, thẻ cảnh báo giữ van ở trạng thái kiểm tra và công khai việc trì hoãn.""",
    "cinder_bypass_afterword_record": """Ghi chú lượt đo tiếp theo — mở hồ sơ cho người mang phép đo khác

Talia chuẩn bị một ngăn thứ hai trong hộp mẫu, dành cho kết quả không khớp với hai lượt đầu. Cô yêu cầu người kế tiếp ghi thiết bị, vị trí lấy mẫu và nhiệt độ trước khi so sánh. Nếu một cách đo mới đọc được thứ mà phiếu cũ bỏ sót, người ấy có thể thêm trang thay vì sửa đè con số ban đầu. Sai lệch là lý do để kiểm tra lại, không phải lý do loại người đo.

Hộp hiện giữ lọ cặn, lát rêu khô, phiếu áp lực và hai chính sách vận hành. Talia để tên người phụ trách tiếp theo ở mặt trong chứ không ghi một ngày duyệt cứng; ca mưa hoặc sửa cống có thể buộc họ lùi lịch. Cô dặn Rowan rằng một quy trình mở không có nghĩa mọi người phải đồng ý với kết luận. Nó chỉ cho biết nơi thấy bằng chứng, cách xin sửa và người giữ trách nhiệm trả lời.""",
}


def main() -> None:
    quest_entries = json.loads(QUESTS_PATH.read_text(encoding="utf-8"))["entries"]
    codex_data = json.loads(CODEX_PATH.read_text(encoding="utf-8"))
    quests = {entry["id"]: entry for entry in quest_entries}
    codex = {entry["id"]: entry for entry in codex_data["entries"]}
    missing = sorted(set(NOTES) - codex.keys())
    if missing:
        raise SystemExit(f"Missing Pressure Wheel records: {', '.join(missing)}")
    for entry_id, note in NOTES.items():
        entry = codex[entry_id]
        quest = quests.get(entry.get("unlockQuestId"))
        if quest is None or quest.get("arcId") != "crown_of_empty_fields":
            raise SystemExit(f"Pressure Wheel record is not linked to an Arc 3 quest: {entry_id}")
        if MARKER in entry.get("body", ""):
            raise SystemExit(f"Supplemental Pressure Wheel note already exists: {entry_id}")

    before = sum(len(entry["body"].split()) for entry in codex_data["entries"] if entry["id"] in NOTES)
    for entry_id, note in NOTES.items():
        codex[entry_id]["body"] += MARKER + "\n" + note
    after = sum(len(entry["body"].split()) for entry in codex_data["entries"] if entry["id"] in NOTES)
    CODEX_PATH.write_text(json.dumps(codex_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {len(NOTES)} Cinderwell Pressure Wheel records by {after - before} whitespace-delimited words.")


if __name__ == "__main__":
    main()
