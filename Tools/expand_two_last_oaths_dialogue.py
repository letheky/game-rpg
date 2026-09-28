import json
from pathlib import Path


CATALOG = Path("Assets/Resources/Content/dialogue_catalog.json")

ADDITIONS = {
    "alden_last_oath_arrival": [
        "Tôi nói “tự nguyện” sau khi đã khép cánh cổng sau lưng đoàn quân. Chữ ký trong sổ không thể kể cho cậu biết họ còn bao nhiêu con đường để quay về.",
        "Tôi từng tin giấu nghi lễ là cách giữ họ khỏi hoảng sợ. Bí mật chỉ khiến người sống không thể hỏi chúng tôi đã chọn thay họ điều gì.",
    ],
    "world_will_final_arrival": [
        "Ta đọc được những bản ghi về người xin nhận Crown. Ta không thể chứng minh từng người đã được nghe rằng lời từ chối vẫn được chấp nhận.",
        "Mô hình của ta tính xác suất mùa đói nhưng không tính ai có quyền quyết định cái giá. Nó thiếu một biến, và ta đã không hỏi biến ấy.",
        "Chờ từng vùng trả lời có thể khiến nguồn dự trữ cạn trước khi ta có kết quả. Quyết định thay họ cũng là một lựa chọn có hậu quả; ta không thể gọi nó là phép tính vô chủ.",
    ],
    "rowan_last_oath_records": [
        "Alden, quyển sổ ghi một cái tên, không ghi người ấy có thể rời bàn lúc nào. Tôi sẽ không gọi khoảng trống đó là đồng ý.",
        "Mỗi bản lưu sẽ ghi ai giữ nó và ai được quyền sửa. Tôi không lấp chỗ trống bằng câu chuyện thuận tiện cho mình.",
    ],
    "rowan_last_oath_choice_cycle": [
        "Tôi hiểu lời ghi tên chưa trả món nợ cho người không được hỏi. Trong lời thề này, cái tên thuộc về tôi; tôi sẽ không ký thay ai khác.",
        "Tôi nhận trách nhiệm về lựa chọn của mình trước người đang sống. Khi chu kỳ lại đòi thêm một người, họ phải được nghe cả điều kiện lẫn quyền từ chối.",
    ],
    "rowan_last_oath_choice_beyond": [
        "Tôi không có kế hoạch hoàn chỉnh cho bên kia. Bản đồ sẽ ở lại cùng những người có thể sửa nó khi phép đo mới trở về.",
        "Rời đi không trao cho tôi quyền phát biểu thay cả Asterra. Tôi mang theo một câu hỏi mà chúng ta đã quá lâu không được phép đặt ra.",
    ],
    "alden_final_vow": [
        "Ta từng giữ danh sách, rồi giấu nó và gọi phần bị mất là lòng thương. Không việc nào trong số đó khiến ta vô can.",
        "Có người nói với ta rằng họ sẵn sàng. Ta nhớ vài khuôn mặt, nhưng không nhớ đủ để lấy hồi ức của mình làm biên bản cho cả 99 người.",
        "Nếu cậu hạ ta, hãy để người khác kể tiếp. Đừng biến ta thành nhân chứng cuối cùng chỉ vì ta là người cuối cùng còn sống.",
    ],
    "rowan_cycle_epilogue": [
        "Tôi sẽ không gọi bình minh này là câu trả lời. Những người ở lại phải được mở lại hồ sơ trước khi một thế hệ khác được gọi đi.",
        "Nếu họ chỉ nhớ tôi đã chọn, hãy giữ cả lý do lẫn những lời phản đối được gửi tới phiến đá.",
    ],
    "rowan_beyond_epilogue": [
        "Những người ở lại không cần đồng ý với tôi mới được giữ bản đồ. Tôi gửi kèm đường kiểm tra từng con số và bản sao để họ tự đối chiếu.",
        "Tín hiệu không hứa chuyến đi sẽ cứu Asterra. Nó chỉ cho chúng ta một lựa chọn có thể từ chối, xem lại và tiếp tục hỏi về sau.",
    ],
    "warden_final_memory": [
        "Đừng lấy lời thú nhận của ta làm giấy phép để làm điều tương tự. Ta đã thấy một đời sai lầm, không phải tương lai của mọi vùng.",
        "Nếu ký ức này còn ích lợi, thì câu hỏi phải được tiếp tục sau khi người kể chuyện đã chết.",
    ],
    "captain_alden_last_oath_down": [
        "Người ngày mai có thể chết, đúng. Người trong quá khứ cũng đã chết; ta thường dùng nỗi sợ ngày mai để thôi hỏi họ có đồng ý không.",
        "Đừng biến lời cảnh báo cuối của một kiếm sĩ thành sắc lệnh. Hãy để người đang sống buộc ta chứng minh điều ta sợ.",
    ],
    "world_will_avatar_down": [
        "Ta bảo vệ những điều kiện để sự sống tồn tại, rồi nhầm chúng với quyền quyết định thay mọi sinh vật.",
        "Hãy giữ hồ sơ mở. Sau khi ngươi rời căn phòng này, ta phải nghe câu trả lời từ những người ta từng tính thay.",
    ],
    "rowan_world_will_battle_end": [
        "Chúng ta sẽ không xóa hệ thống khỏi ký ức, cũng không giao cho nó quyền chọn người kế tiếp. Nó phải đối thoại với những người mà nó từng tính thay.",
        "Nếu Asterra đổi khác sau khi nghi lễ dừng, việc sửa đường đi phải thuộc về những người sẽ sống với hậu quả ấy.",
    ],
}


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in catalog["entries"]}
    missing = set(ADDITIONS) - set(by_id)
    if missing:
        raise SystemExit(f"Missing dialogue IDs: {sorted(missing)}")

    added = 0
    for dialogue_id, lines in ADDITIONS.items():
        existing = by_id[dialogue_id]["lines"]
        new_lines = [line for line in lines if line not in existing]
        existing.extend(new_lines)
        added += len(new_lines)

    CATALOG.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Expanded {len(ADDITIONS)} ending dialogues; appended {added} authored lines.")


if __name__ == "__main__":
    main()
