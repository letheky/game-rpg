#!/usr/bin/env python3
"""Lengthen selected campaign conversations while keeping each line readable."""
import json
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content" / "dialogue_catalog.json"

ADDITIONS = {
    "rowan_opening": [
        "Cậu cứ nghĩ khi ma tộc xuất hiện, mình sẽ biết phải làm gì. Nhưng giữa tro bụi này, chẳng có lời thề nào chỉ cho mình biết nên tìm ai trước.",
        "Ước mơ trở thành dũng sĩ từng giống một con đường thẳng: luyện kiếm, đánh bại Ma Vương, đem hòa bình về. Hôm nay, con đường ấy chỉ còn những người chưa tìm thấy nhau.",
        "Nếu Mira còn ở đây, cô ấy sẽ không tha thứ nếu mình đứng im chờ người khác gọi tên mình. Mình phải qua sân tập, kiểm tra từng mái hiên và hỏi từng người còn có thể trả lời.",
        "Mình vẫn muốn cứu thế giới. Nhưng trước hết, phải học cách nhìn thấy những người đang ở ngay trước mặt mình.",
    ],
    "mira_survivors": [
        "Tớ đã gọi tên cậu suốt đường tới đây. Có lúc tớ chỉ nghe tiếng gỗ cháy, nên tớ cứ gọi thêm lần nữa.",
        "Đừng nói với tớ rằng cậu ổn nếu chân còn đang run. Tớ cần cậu đứng được, không cần cậu giả vờ không sợ.",
        "Những người mắc kẹt bên sân tập có thể đang chờ ai đó mở lối. Tớ sẽ tìm họ; cậu giúp tớ dọn con warg khỏi đường đi.",
        "Sau đó chúng ta mới xem dấu khắc trên móng. Nếu cứ nhìn nó trước, tớ sẽ quên mất người trong làng vẫn đang cần mình.",
    ],
    "rowan_warden_defeated": [
        "Ứng viên thứ 99. Mình cứ tưởng danh sách chỉ là cách Order ghi lại những người đã qua kỳ thi.",
        "Trụ đá bị cạo đúng ở chỗ một cái tên có thể đã từng được viết. Lõi đồng không thể nói người ấy là ai, cũng không nói chuyện gì xảy ra sau khi họ bước qua cánh cửa này.",
        "Nếu thử thách đã chờ mình suốt nhiều năm, vậy người ta biết nó sẽ được mở lại. Mình cần một bản chép trước khi ai đó gọi dòng chữ này là truyền thuyết.",
        "Elara phải được xem cả vết cạo lẫn ký tự còn lại. Một phần chứng cứ không đủ để lấp phần kia.",
    ],
    "warden_choir_arrival": [
        "Ta không biết tiếng chuông gọi con hay chỉ vang lên sau khi con tới. Kho lưu trữ đã gán hai điều ấy làm một trong những bản chép muộn.",
        "Khi con đọc mặt trước, con sẽ thấy lời thề. Mặt sau giữ số người phải trả giá để lời thề ấy thành hiện thực. Không mặt nào tự nó là toàn bộ ký ức.",
        "Ta đã canh nơi này quá lâu đến mức đôi khi quên rằng giữ một hồ sơ không có nghĩa là biết người đã để lại nó.",
        "Hãy hỏi ta điều gì còn nhớ, rồi hỏi phiến đá đã bị sửa chỗ nào. Cả hai câu trả lời đều có thể sai theo cách khác nhau.",
    ],
    "jace_case_interview": [
        "Tôi vẫn nghe tiếng kim gió gõ vào hộp sau khi đoàn quay lại. Mỗi lần nhớ đến, tôi lại tự hỏi mình đã cứu một người bằng cách đóng cửa với bao nhiêu lời kể khác.",
        "Tôi không muốn Evelyn xóa chữ ký. Nếu tên tôi biến mất, trang giấy sẽ trông như thể kết luận ấy tự mọc lên mà không có ai chịu trách nhiệm.",
        "Nhưng giữ chữ ký cũng không có nghĩa là tôi buộc những người khác phải tin lời mình. Tôi muốn ghi lại điều tôi thấy, điều tôi đo được và lý do tôi đã vội chọn một câu kết luận.",
        "Nếu báo cáo mới còn thiếu một cái tên, hãy để khoảng trống ấy nhìn thấy được. Tôi không muốn sự im lặng của chúng ta lại bị chép thành bằng chứng.",
    ],
    "ada_forecast_intro": [
        "Một con số có thể được chép rất gọn và vẫn trả lời sai câu hỏi. “Thu hoạch” không thể đứng ở đây nếu thửa ruộng chưa được gieo.",
        "Alden cần một bảng để chia ca giữ kho. Tôi cần biết cột nào là dự tính, cột nào là phép cân và ai đã có quyền xem bản gốc.",
        "Chúng ta sẽ không bắt đầu bằng việc tìm người đáng trách. Ta sẽ bắt đầu bằng thước, ngày tháng và những ô chưa có nguồn.",
        "Nếu dữ liệu thiếu, hãy ghi là thiếu. Một khoảng trống có ngày tháng đáng tin hơn một lời giải thích được thêm vào sau này.",
    ],
    "world_will_final_arrival": [
        "Ta được tạo ra từ những lời cầu xin qua nhiều mùa đói. Mỗi lần tài nguyên suy kiệt, ta phải quyết định có bao nhiêu sinh mạng sẽ mất trước khi mùa sau bắt đầu.",
        "Chín mươi chín người đã tự nguyện mang lấy hình hài Ma Vương. Sự tự nguyện không xóa đi những gia đình bị chiến tranh cuốn vào, nhưng nó đã giữ được nhiều vùng đất sống thêm một thế kỷ.",
        "Ta không thể đưa ra sổ kho đầu tiên. Ta có các dự báo, ký ức và phép đo cậu vừa xác nhận; tất cả đều cho thấy ta đã hành động với dữ liệu không đầy đủ.",
        "Nếu cậu rời đi, Asterra có thể không chịu nổi lựa chọn ấy. Nếu cậu ở lại, vòng lặp sẽ lại đòi một người kế tiếp. Ta không còn bằng chứng để nói rằng nỗi sợ của ta là một định luật.",
        "Cậu phải chọn giữa hai rủi ro thật. Ta sẽ không gọi kết quả nào là an toàn thay cho những người sẽ sống cùng nó.",
    ],
    "alden_final_vow": [
        "Tôi từng nghĩ nếu mình chọn đứng ở cuối danh sách, những người khác có thể rời đi mà không phải biết điều gì đã xảy ra với họ.",
        "Tôi đã nhầm. Những người sống qua mỗi chu kỳ vẫn trả giá, dù tên của họ không được khắc cạnh ngai vàng.",
        "Tôi vẫn sợ rằng ngày mai sẽ thiếu lương thực, nước sạch và đất trồng. Nỗi sợ ấy có thật; nó không trao cho tôi quyền gọi mọi lựa chọn khác là điều không thể.",
        "Nếu cậu chọn giữ vòng lặp, hãy nhìn vào tôi khi đặt lời thề xuống. Nếu cậu chọn dừng nó, cũng đừng nói rằng chẳng ai đã cố cứu những người đang sống.",
        "Tôi sẽ dùng trận đấu cuối này để bảo vệ điều mình đã tin, và để chịu trách nhiệm cho cái giá của nó.",
    ],
    "warden_final_memory": [
        "Ta nhớ bàn tay người đầu tiên đặt tấm bản đồ lên bàn hội đồng. Bùn vẫn khô trên ủng của người ấy; câu hỏi thì không bao giờ được ghi vào biên bản.",
        "Ta đã chờ quá lâu để ai đó đọc được cả hai mặt hồ sơ. Chờ đợi khiến ta tưởng rằng sự thật sẽ tự sửa được quyết định cũ.",
        "Nó không thể. Người chết không quay lại khi ta gọi đúng tên họ, và người đang sống không tự có tiếng nói chỉ vì tên họ xuất hiện trong một bản lưu trữ.",
        "Ta sẽ không bảo con phải cứu ta khỏi ký ức này. Hãy để những người còn ở lại có thể phản đối con, sửa con và tiếp tục sống sau lựa chọn của con.",
        "Nếu ngày mai chưa có câu trả lời, đừng biến sự chưa biết thành lời thề mới. Hãy để nó là điều mọi người cùng được nhìn thấy.",
    ],
}


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in data["entries"]}
    missing = sorted(set(ADDITIONS) - entries.keys())
    if missing:
        raise SystemExit(f"Missing dialogue entries: {', '.join(missing)}")
    changed = 0
    added_words = 0
    for key, lines in ADDITIONS.items():
        existing = entries[key]["lines"]
        if existing[-len(lines):] == lines:
            continue
        if any(line in existing for line in lines):
            raise SystemExit(f"Partial dialogue expansion found; review {key} manually.")
        existing.extend(lines)
        added_words += sum(len(line.split()) for line in lines)
        changed += 1
    if not changed:
        print("Selected campaign dialogue already contains all supplemental lines.")
        return
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Expanded {changed} campaign scenes with {added_words} dialogue words.")


if __name__ == "__main__":
    main()
