#!/usr/bin/env python3
"""Add Gideon Park's Ashfall evacuation-cart repair route."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets" / "Resources" / "Content"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, catalog):
    (CONTENT / name).write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    positions = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in positions:
            entries[positions[entry["id"]]] = entry
        else:
            positions[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, kind, target, location, giver, speaker, objective,
# dialogue lines, codex title, codex body, visual, position
steps = [
    ("offer", "Một bánh xe cho đường phía đông", "talk", "ashfall_gideon_witness", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Hỏi Gideon vì sao ông giữ lại chiếc xe gỗ cháy sém thay vì bỏ nó sau cuộc tập kích.",
     ["Tôi từng dùng nó chở gỗ tới từng mái nhà. Từ đêm cháy, nó chỉ nằm nghiêng cạnh đường.", "Nếu dựng lại xe, đừng biến nó thành xe của Gideon. Người cần đưa thuốc, chăn hay dụng cụ phải có thể dùng nó mà không xin quyền từ một cuốn sổ."],
     "The Cart Beside the Road", "Gideon Park giữ lại chiếc xe không phải vì gỗ của nó quý hơn những gì đã cháy. Ông muốn biết một phương tiện có thể trở lại hữu ích mà không trở thành vật sở hữu của người sửa nó. Rowan đề nghị kiểm tra từng bộ phận trước khi kéo xe ra đường. Việc ấy không thay thế những chiếc xe mất trong đêm tập kích; nó chỉ cho biết liệu chiếc còn lại có thể chở đồ an toàn hay không.", "", None),
    ("wheel", "Moay-ơ nứt dọc thớ", "inspect", "ashfall_cart_wheel", "ashfall_village", "gideon_park", "ROWAN HALE",
     "Kiểm tra vết nứt quanh moay-ơ trước khi xoay bánh xe.",
     ["Vết nứt chạy qua thớ gỗ nhưng chưa chạm hết vòng sắt.", "Nếu ép bánh quay trên mặt dốc, phần còn lành có thể vỡ theo. Ta cần đo đường đi trước."],
     "The Split Hub", "Moay-ơ nứt chạy theo thớ, còn hai chốt sắt vẫn giữ vòng ngoài đúng vị trí. Gideon không gọi nó là một sửa chữa tạm đủ tốt: khi tải lệch sang mép bánh, vết nứt sẽ chịu thêm lực. Rowan đánh dấu chỗ yếu để người sau không kéo xe thử trước khi có chốt trục vừa kích thước.", "cart_wheel", (7.4, 1.7)),
    ("medicine", "Thuốc cần đi khô", "talk", "mira_cole", "ashfall_village", "mira_cole", "MIRA COLE",
     "Hỏi Mira loại hàng nào cần chuyển trước nếu chiếc xe có thể chạy lại.",
     ["Tôi có lọ thuốc đã pha và giấy liều phải giữ khô. Chúng không nặng, nhưng nắp sẽ lỏng nếu xe nảy liên tục.", "Đừng ghi người nhận trước. Hãy ghi cách buộc hàng và để người đang cần tự lấy."],
     "Mira's Dry Load", "Mira Cole đề nghị thử chở lọ thuốc rỗng bọc vải thay vì dùng một bệnh nhân làm tải thử. Giấy liều phải nằm trong túi chống mưa và được đặt phía trên chứ không ép sát thành xe. Cô không giao cho Rowan danh sách người sẽ nhận thuốc; thứ cô cần kiểm tra là độ rung và việc giấy có còn đọc được sau chuyến đi.", "", None),
    ("rut", "Rãnh bánh phía đông", "inspect", "ashfall_cart_east_rut", "ashfall_village", "gideon_park", "ROWAN HALE",
     "Đo rãnh sâu ở lối đông để quyết định bánh xe có thể vượt qua hay không.",
     ["Đất lún thành hai rãnh khác độ sâu. Kéo thẳng sẽ nghiêng thùng sang trái.", "Ta có thể vòng qua bậc đá nếu chỗ quay đầu đủ rộng."],
     "Two Ruts, One Turn", "Hai rãnh xe cũ không sâu bằng nhau. Mặt đường khô gần bậc đá nhưng đoạn thấp giữ nước và buộc người kéo phải đổi hướng sớm. Gideon ghi lại lối vòng cùng điểm quay đầu, không dùng một vệt bánh đơn lẻ để suy đoán ai đã đi qua hay thứ gì được chở. Bản đo giúp chọn đường thử, chưa xác nhận con đường có thể chịu mọi tải.", "cart_rut", (8.8, 0.4)),
    ("clear", "Tiếng chân dưới gầm xe", "defeat", "tiny_af_ash_goblin", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Đánh đuổi Ash Goblin đang kéo dải sắt khỏi lối thử xe phía đông.",
     ["Nó chui dưới sàn xe mỗi khi nghe tiếng bước chân. Đừng đập vào trục; phần còn nguyên nằm ngay phía trên nó.", "Chờ nó lao khỏi gầm rồi chặn đường về kho."],
     "The Goblin Under the Cart", "Ash Goblin đã kéo một dải sắt cong ra khỏi đường thử và dùng gầm xe làm chỗ ẩn. Rowan đợi nó rời khỏi khung gỗ trước khi phản công, để cú đánh không làm nứt thêm bánh xe. Dải sắt thu hồi được nhưng biến dạng; nó có thể làm vật liệu rèn sau khi được đo lại, song bản thân nó không chứng minh ai đã bỏ xe tại đây.", "", None),
    ("salvage", "Dải sắt và nan gỗ", "inspect", "ashfall_cart_salvage", "ashfall_village", "gideon_park", "ROWAN HALE",
     "Phân loại nan gỗ còn thẳng và dải sắt không bị nứt ở đống vật liệu cứu được.",
     ["Hai nan nứt ở đầu, nhưng một đoạn sắt còn đủ dài cho chốt trục.", "Ta sẽ mang chúng tới Tomas để kiểm tra kích thước, không dùng ngay trên bánh."],
     "Salvage Is Not a Part Yet", "Trong đống vật liệu có một đoạn sắt gần như thẳng và hai nan gỗ nứt ở đầu. Rowan chỉ giữ đoạn sắt để Tomas kiểm tra; vật liệu trông còn nguyên không có nghĩa là đã chịu được lực của xe. Gideon cấp lại phần phế liệu cho người sửa thay vì tính nó là hàng chung, để nguồn gốc và giới hạn sử dụng không bị bỏ khỏi bản ghi.", "cart_spokes", (1.8, -4.45)),
    ("measure", "Đo xe theo chiều người kéo", "talk", "ashfall_gideon_witness", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Đưa số đo rãnh đường cho Gideon và thống nhất kiểm tra xe ở tốc độ đi bộ.",
     ["Tôi nhớ xe quay gấp hơn khi đầy gỗ. Ký ức ấy không cho ta con số bán kính.", "Hãy thử với thùng nhẹ, đánh dấu chỗ bánh ngoài cùng chạm đất rồi mới chở hàng."],
     "A Turning Measure", "Gideon phân biệt điều ông nhớ về chiếc xe cũ với điều Rowan vừa đo trên con đường hiện tại. Bán kính quay phải được kiểm tra ở tốc độ đi bộ, với thùng nhẹ và người kéo có thể dừng ngay. Dấu bánh ngoài sẽ cho biết xe cần thêm chỗ trống; nó không cho phép đội sửa tự mở rộng đường qua phần đất của hộ khác.", "", None),
    ("tomas", "Một chốt không vừa với mọi bánh", "talk", "tomas_cart_dimensions", "dawnkeep_outpost", "tomas_reed", "TOMAS REED",
     "Hỏi Tomas cách biến đoạn sắt Ashfall thành chốt vừa moay-ơ mà không làm méo vòng bánh.",
     ["Chốt trục phải có vai chặn. Nếu chỉ nhét một thanh tròn vào, lực ngang sẽ đẩy nó xuyên qua gỗ.", "Mang đoạn sắt tới lò. Tôi sẽ giữ mẫu đo; bản rèn sẽ thuộc về chiếc xe, không thuộc về tôi."],
     "Tomas's Shoulder Pin", "Tomas Reed đo vai chặn theo độ dày vòng sắt và đường nứt mà Rowan ghi lại. Ông từ chối khoan thêm một lỗ để buộc bánh vào vị trí: lỗ mới sẽ cắt ngang phần gỗ còn chịu tải. Công thức chốt dùng phần sắt và một nan thẳng làm cữ. Bản mẫu ở lò giúp các thợ khác rèn lại kích thước, nhưng không thay thế việc kiểm tra chiếc xe đã sửa.", "tomas_reed", (4.4, 0.15)),
    ("spokes", "Nan gỗ làm cữ", "inspect", "dawnkeep_spare_spokes", "dawnkeep_outpost", "tomas_reed", "ROWAN HALE",
     "Chọn nan thẳng có thớ dọc đều để làm cữ rèn ở lò Tomas.",
     ["Nan này không cong khi kê ngang. Nó có thể giữ khoảng cách trong lúc làm chốt.", "Ta sẽ để lại chiếc nan làm cữ, không tính nó như bộ phận thay thế đã được kiểm chứng."],
     "The Spoke Used as a Gauge", "Nan gỗ chỉ dùng làm cữ giữ khoảng cách trong lúc rèn, không được lắp vào xe thay cho một phần chịu tải. Tomas đặt thước kim loại bên cạnh để Rowan có thể lặp lại số đo mà không phụ thuộc vào độ ẩm của gỗ. Việc tách cữ khỏi phụ tùng giúp người sửa sau không nhầm một món hỗ trợ chế tác với bộ phận có thể chở hàng trên đường.", "cart_spokes", (7.9, 1.3)),
    ("forge", "Rèn chốt vai trục", "craft", "ashfall_cart_axle_pin", "dawnkeep_outpost", "tomas_reed", "TOMAS REED",
     "Rèn một Ashfall Axle Pin tại Dawnkeep Forge bằng đoạn sắt và nan gỗ làm cữ.",
     ["Chốt đã nguội. Vai chặn nằm đúng ngoài vòng sắt và không cạ vào nan bánh.", "Đừng coi lò nguội là bài thử. Chốt vẫn phải được lắp rồi xoay bằng tay trước khi xe lăn."],
     "Ashfall Axle Pin", "Chốt vai trục được rèn từ đoạn sắt cứu ở Ashfall. Nan gỗ dùng làm cữ được giữ riêng và không bị tiêu hao như thể nó là sắt. Tomas kiểm tra vai chặn bằng thước trước khi đưa chốt cho Rowan. Độ khớp tại lò mới chỉ xác nhận kích thước ban đầu; chiếc xe cần được lắp thử và xoay không tải để phát hiện ma sát.", "", None),
    ("return", "Mang chốt về đúng chiếc xe", "talk", "ashfall_gideon_witness", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Đưa chốt vai trục cho Gideon và kể lại phép đo của Tomas.",
     ["Ông ấy giữ nan làm cữ riêng chứ? Tốt. Ta không muốn ai đẽo nó thành phụ tùng trong lúc vội.", "Lắp chốt trước, rồi quay bánh bằng tay. Chưa ai được chất đồ lên xe."],
     "The Part Returns with Its Measure", "Rowan mang về chốt đã rèn cùng phép đo và lưu ý từ Tomas. Gideon hỏi về chiếc nan làm cữ trước khi chạm vào xe, vì một bộ phận chưa thử rất dễ bị coi nhầm là phụ tùng dự phòng. Hai người thống nhất lắp chốt, xoay bánh khi xe còn kê cao, rồi mới thử tải nhẹ. Không có bước nào trong quy trình coi sự vội vàng là bằng chứng của độ bền.", "", None),
    ("install", "Lắp chốt dưới vành sắt", "interact", "ashfall_cart_wheel", "ashfall_village", "gideon_park", "ROWAN HALE",
     "Lắp Ashfall Axle Pin vào moay-ơ rồi xoay bánh bằng tay để kiểm tra độ cạ.",
     ["Vai chốt chạm sát vành nhưng không ép nan bánh sang bên.", "Bánh quay hết một vòng. Vết nứt chưa lan thêm; ta có thể thử lăn xe không tải."],
     "A Wheel That Turns by Hand", "Chốt được lắp vào moay-ơ và vai chặn nằm ngoài vòng sắt. Rowan xoay bánh đủ một vòng khi thân xe còn kê cao; bánh không cạ vào càng và vết nứt không mở rộng trong phép thử chậm này. Gideon đánh dấu bộ phận đã lắp nhưng chưa gọi xe an toàn cho hàng. Thử không tải chỉ mở bước kiểm tra tiếp theo.", "", None),
    ("test", "Lăn thử khi thùng còn trống", "interact", "ashfall_cart_test_lane", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Đẩy xe rỗng qua đoạn đường bằng và dừng trước chỗ rãnh sâu.",
     ["Bánh không lắc ở đoạn bằng. Đường thử kết thúc trước rãnh, đúng như ta đã định.", "Giờ hãy hỏi Mira về cách kê thuốc; hàng nhẹ vẫn có thể vỡ nếu buộc sai."],
     "Empty Cart Trial", "Xe rỗng lăn được trên đoạn bằng đã chọn. Rowan dừng trước rãnh sâu thay vì dùng đà để vượt qua một chỗ chưa đo. Gideon kiểm tra chốt sau khi dừng, còn Mira sẽ xem vị trí đặt hàng nhẹ. Kết quả chỉ áp dụng cho đoạn ngắn, mặt đường khô và xe không tải; mưa hoặc trọng lượng lệch có thể làm đổi hành vi của bánh.", "cart_test", (8.5, -1.1)),
    ("load", "Buộc lọ rỗng trước", "talk", "mira_cole", "ashfall_village", "mira_cole", "MIRA COLE",
     "Cho Mira xem đoạn chạy thử và thống nhất thử dây buộc với lọ rỗng bọc vải.",
     ["Túi phải treo phía trong thành xe, không được tự do đập vào nan.", "Ta có thể đánh dấu chỗ buộc bằng một nút vải tháo được. Không cần khắc tên ai lên xe."],
     "The Cloth Knot Test", "Mira chọn một nút vải có thể tháo để đánh dấu vị trí đặt túi thuốc. Nút không mang tên người bệnh và không biến chiếc xe thành quầy phát thuốc cố định. Cô muốn thử một lọ rỗng trước, lắc xe ở tốc độ đi bộ rồi kiểm tra nắp và tờ liều. Hàng thật chỉ được đặt lên xe khi người phụ trách thuốc đồng ý với cách buộc.", "", None),
    ("policy", "Xe chung hay bộ sửa riêng", "choice", "ashfall_cart_service_policy", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Chọn cách dùng đầu tiên cho chiếc xe đã sửa.",
     ["Ta đã sửa được bánh, nhưng giờ phải chọn cách giữ nó hữu ích.", "Một xe dùng chung cần lịch bàn giao dễ đọc. Bộ sửa riêng giúp các hộ tự xử lý bánh nhỏ, nhưng họ sẽ phải tự tìm đường và vật liệu."],
     "Two Ways to Keep a Cart Moving", "Một chiếc xe chung có thể chở nhiều loại hàng nhưng cần quy ước bàn giao rõ và chỗ để không chắn lối. Bộ sửa nhỏ giúp các hộ tự siết chốt khi bánh lỏng, song không thay được xe tải hay người kéo. Gideon không xem một cách là mặc nhiên công bằng hơn; Rowan phải chọn thứ có thể kiểm tra trong điều kiện Ashfall hiện có. Người dùng sau này vẫn có quyền đổi lịch hoặc từ chối nhận vật liệu.", "", None),
    ("communal_bay", "Chỗ đỗ không chắn lối", "interact", "ashfall_cart_shared_bay", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Đánh dấu chỗ đỗ xe chung bên lề để không che cửa hầm và đường tới giếng.",
     ["Khoảng trống này đủ cho xe quay đầu mà không chặn bậc xuống hầm.", "Để hai đầu dây buộc lộ ra. Người đến sau cần biết xe đang được bàn giao, không phải bị khóa riêng."],
     "The Shared Bay", "Chỗ đỗ chung được đặt lệch khỏi cửa hầm và đường đến giếng. Rowan thử lối quay đầu với xe rỗng rồi để hai đầu dây bàn giao dễ nhận ra. Vị trí này không dành riêng cho một hộ; người kéo có thể đưa xe đi nếu cần sơ tán hoặc chở thuốc. Gideon vẫn giữ quyền sửa lại vạch khi người đi đường thấy nó chắn lối.", "cart_bay", (-6.3, 3.7)),
    ("communal_turn", "Bán kính quay nhìn thấy được", "inspect", "ashfall_cart_turning_arc", "ashfall_village", "gideon_park", "ROWAN HALE",
     "Đánh dấu bánh ngoài cùng khi xe quay ở tốc độ đi bộ quanh chỗ đỗ chung.",
     ["Vạch chỉ rộng hơn bánh xe một gang tay. Ta có thể nhìn thấy khi khoảng trống bắt đầu thiếu.", "Ghi cả đoạn đường đã thử lẫn mặt đất khô; đừng dùng vạch này cho mọi lối."],
     "The Turning Arc", "Vệt quay cho thấy bánh ngoài cùng cần một khoảng trống vừa hơn chiều ngang xe. Rowan ghi điều kiện mặt đất khô và tốc độ đi bộ ngay cạnh vạch, vì một dấu không có bối cảnh dễ bị dùng sai ở lối hẹp khác. Nếu nền lún hoặc xe mang hàng cao, bán kính quay thay đổi; người kéo có thể dừng và chọn lối khác thay vì ép qua.", "cart_test", (0.9, -4.6)),
    ("communal_report", "Bàn giao lượt dùng đầu tiên", "talk", "ashfall_gideon_witness", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Báo Gideon rằng chỗ đỗ và vạch quay đã sẵn sàng cho chiếc xe chung.",
     ["Tôi sẽ để bảng lịch cạnh chỗ đỗ, nhưng không ghi sẵn ai phải kéo.", "Người mượn tự đánh dấu lúc nhận và trả xe. Nếu đường đổi, họ có thể dừng và báo lại."],
     "A Cart Shared by Choice", "Lịch dùng xe ghi thời điểm nhận và trả, không phân công người kéo theo tên hộ. Người mượn tự chọn nhận việc, báo hỏng và đề nghị đổi đường. Gideon chịu trách nhiệm kiểm tra chốt định kỳ cùng người sử dụng đầu tiên, nhưng lịch không biến một lời đồng ý hôm nay thành nghĩa vụ cho tuần sau. Chỗ đỗ và vệt quay vẫn có thể được thay đổi khi lối đi cần rộng hơn.", "", None),
    ("household_kits", "Bộ chốt có thể tháo", "interact", "ashfall_cart_kit_table", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Sắp các cữ gỗ và chốt dự phòng thành bộ sửa có thể mang về từng hộ.",
     ["Mỗi bộ có một chốt, một cữ và tờ hướng dẫn lắp lại. Không ai phải để xe nhà mình ở sân chung.", "Ghi rõ bộ nào chưa thử để đừng nhầm vật liệu mới với phụ tùng đã dùng."],
     "Portable Repair Kits", "Các bộ nhỏ chứa cữ đo, một chốt dự phòng và tờ chỉ dẫn kiểm tra độ cạ. Chúng không gồm bánh xe hoàn chỉnh và không thể sửa mọi dạng gãy. Gideon muốn mỗi hộ quyết định có nhận bộ hay không; Rowan đánh dấu bộ chưa thử bằng dây màu thay vì tên người. Việc phân tán dụng cụ giảm nhu cầu chờ xe chung nhưng cũng khiến mỗi người phải tự giữ vật liệu an toàn.", "cart_kit", (5.6, 3.8)),
    ("household_test", "Thử chốt trên bánh rời", "interact", "ashfall_cart_household_load", "ashfall_village", "mira_cole", "MIRA COLE",
     "Thử cữ và chốt trên một bánh xe rời trước khi phát bộ sửa.",
     ["Bánh rời quay đều sau khi siết. Ta đã thử nó trên giá, không trên một xe đang chở người.", "Tờ hướng dẫn phải nói rõ lúc nào nên dừng và gọi thợ."],
     "A Test on the Stand", "Mira giữ bánh xe trên giá thử, tránh biến một hộ đang dùng xe thành đối tượng thử nghiệm. Chốt lắp được và bánh quay đều khi siết đúng lực, nhưng phép thử không bao phủ khung cong hay tải nặng. Rowan thêm hướng dẫn dừng nếu tiếng cạ trở lại hoặc vòng sắt dịch chuyển. Bộ sửa là dụng cụ bảo dưỡng cơ bản, không thay công việc của thợ rèn.", "cart_test", (-8.9, -2.8)),
    ("household_report", "Quyền nhận bộ sửa", "talk", "mira_cole", "ashfall_village", "mira_cole", "MIRA COLE",
     "Đưa Mira tờ hướng dẫn và để cô quyết định hộ nào muốn nhận bộ chốt.",
     ["Tôi sẽ đặt tờ hướng dẫn ở bàn thuốc. Người cần mới lấy; không ai phải ký nhận để chứng minh mình xứng đáng.", "Gideon giữ phần còn lại để rèn thêm khi có vật liệu."],
     "Repair Stock with an Opt-In", "Mira đặt hướng dẫn ở bàn thuốc cùng số chốt còn lại, để người cần tự hỏi và lấy bộ sửa. Cô không ghi ai đã nhận để kiểm đếm mức độ khó khăn; chỉ vật liệu tồn kho được theo dõi. Gideon giữ lại cữ để rèn thêm khi có sắt tốt. Những hộ không muốn tự sửa vẫn có thể nhờ thợ hoặc mượn xe chung khi lối đi và lịch cho phép.", "", None),
    ("afterword", "Con đường không cần một người giữ chìa", "talk", "ashfall_gideon_witness", "ashfall_village", "gideon_park", "GIDEON PARK",
     "Hỏi Gideon cách ông sẽ giữ xe và bộ sửa dùng được sau chuyến đầu tiên.",
     ["Bánh xe đã có chốt kiểm tra được. Phần còn lại là hỏi người dùng xem lối đi có đổi không.", "Tôi sẽ giữ dụng cụ, không giữ quyền quyết định ai được đi."],
     "Afterword: The Road Stays Open", "Ashfall hiện có một chiếc xe đã sửa, một đường thử ngắn và một quy trình lắp chốt có thể lặp lại. Lựa chọn của Rowan quyết định làng ưu tiên xe chung với lịch bàn giao hay các bộ sửa tự nguyện cho từng hộ. Cả hai cách vẫn giữ quyền dừng khi tải hoặc mặt đường vượt quá điều đã thử. Gideon cất dụng cụ trong tầm với của người sửa tiếp theo; chiếc xe không trở thành biểu tượng rằng làng đã hồi phục hoàn toàn.", "", None),
]

items = [
    {"id": "ashfall_cart_iron", "name": "Sắt cong từ xe cũ", "description": "Đoạn sắt thu hồi ở Ashfall; Tomas có thể kiểm tra xem phần nào còn dùng được.", "category": "material", "equipmentSlot": "", "maxStack": 99, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 2},
    {"id": "ashfall_cart_spoke", "name": "Nan gỗ làm cữ", "description": "Một thanh gỗ thẳng chỉ dùng để giữ khoảng cách trong lúc rèn chốt, không phải bộ phận chịu tải.", "category": "material", "equipmentSlot": "", "maxStack": 99, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 1},
    {"id": "ashfall_cart_axle_pin", "name": "Ashfall Axle Pin", "description": "Chốt vai trục có thể tháo, vừa vòng sắt của chiếc xe Gideon đang sửa.", "category": "material", "equipmentSlot": "", "maxStack": 10, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
    {"id": "ashfall_shared_cart_charm", "name": "Bùa Lượt Xe Chung", "description": "Một thẻ gỗ có hai vạch bàn giao; nhắc người mượn ghi giờ nhận và trả xe.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
    {"id": "ashfall_household_repair_charm", "name": "Bùa Cữ Trục Gia Hộ", "description": "Một cữ kim loại nhỏ giúp Rowan ghi nhớ phép thử chốt trên bánh rời.", "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 0, "guardBonus": 2, "healAmount": 0, "sellValue": 0},
]

recipe = [{
    "id": "forge_ashfall_cart_axle_pin", "displayName": "Rèn Ashfall Axle Pin",
    "stationId": "dawnkeep_forge", "discipline": "smithing",
    "outputItemId": "ashfall_cart_axle_pin", "outputQuantity": 1,
    "ingredients": [{"itemId": "ashfall_cart_iron", "quantity": 2},
                    {"itemId": "ashfall_cart_spoke", "quantity": 1}],
}]

landmarks = [
    ("ashfall_cart_wheel", "Bánh xe moay-ơ nứt", "ashfall_village", "cart_wheel", 7.4, 1.7),
    ("ashfall_cart_east_rut", "Rãnh xe phía đông", "ashfall_village", "cart_rut", 8.8, 0.4),
    ("ashfall_cart_salvage", "Đống sắt và nan gỗ", "ashfall_village", "cart_spokes", 1.8, -4.45),
    ("ashfall_cart_test_lane", "Đoạn đường thử xe", "ashfall_village", "cart_test", 8.5, -1.1),
    ("ashfall_cart_shared_bay", "Chỗ đỗ xe chung", "ashfall_village", "cart_bay", -6.3, 3.7),
    ("ashfall_cart_turning_arc", "Vạch bán kính quay", "ashfall_village", "cart_test", 0.9, -4.6),
    ("ashfall_cart_kit_table", "Bàn bộ sửa có thể tháo", "ashfall_village", "cart_kit", 5.6, 3.8),
    ("ashfall_cart_household_load", "Giá thử bánh xe rời", "ashfall_village", "cart_test", -8.9, -2.8),
    ("tomas_cart_dimensions", "Tomas Reed và thước vai chốt", "dawnkeep_outpost", "tomas_reed", 4.4, 0.15),
    ("dawnkeep_spare_spokes", "Nan thẳng trong kho thợ rèn", "dawnkeep_outpost", "cart_spokes", 7.9, 1.3),
]

encounter = [{
    "id": "ashfall_cart_road_goblin", "monsterId": "tiny_af_ash_goblin",
    "locationId": "ashfall_village", "positionX": 6.1, "positionY": 4.05,
    "requiredQuestId": "side_ashfall_cart_clear", "blockedQuestId": "",
    "blockedDialogueId": "", "contributesToQuest": True,
    "defeatObjectiveTargetId": "tiny_af_ash_goblin",
    "defeatDialogueId": "ashfall_cart_goblin_defeated", "downDialogueId": "rowan_field_retreat",
    "reward": {"gold": 0, "items": []},
}]

dialogues, quests, codex = [], [], []
for key, title, kind, target, location, giver, speaker, objective, lines, record_title, body, visual, position in steps:
    dialogue_id = "ashfall_cart_" + key
    quest = {
        "id": "side_ashfall_cart_" + key, "arcId": "ashes_of_ashfall", "stage": -1,
        "type": "side", "locationId": location, "giverId": giver,
        "title": title, "objective": objective,
        "objectives": [{"id": "resolve_" + key, "kind": kind, "targetId": target,
                        "requiredCount": 1, "description": objective,
                        "dialogueId": dialogue_id}],
        "reward": {"gold": 8 if kind in ("talk", "choice") else 6, "items": []},
    }
    if key == "offer":
        quest["prerequisiteIds"] = ["side_ashfall_two_bells_choose"]
    elif key in ("communal_bay", "communal_turn", "communal_report"):
        quest.update({"branchFlag": "ashfall_cart_use", "branchValue": "shared",
                      "prerequisiteIds": ["side_ashfall_cart_policy" if key == "communal_bay" else
                                           "side_ashfall_cart_communal_bay" if key == "communal_turn" else
                                           "side_ashfall_cart_communal_turn"]})
    elif key in ("household_kits", "household_test", "household_report"):
        quest.update({"branchFlag": "ashfall_cart_use", "branchValue": "household",
                      "prerequisiteIds": ["side_ashfall_cart_policy" if key == "household_kits" else
                                           "side_ashfall_cart_household_kits" if key == "household_test" else
                                           "side_ashfall_cart_household_test"]})
    elif key == "afterword":
        quest["prerequisiteGroups"] = [{"anyOfQuestIds": ["side_ashfall_cart_shared_report",
                                                           "side_ashfall_cart_household_report"]}]
    else:
        previous = "offer" if key == "wheel" else None
        if previous:
            quest["prerequisiteIds"] = ["side_ashfall_cart_" + previous]
        elif key in ("medicine", "rut", "clear", "salvage", "measure", "tomas", "spokes", "forge",
                     "return", "install", "test", "load", "policy"):
            order = ["wheel", "medicine", "rut", "clear", "salvage", "measure", "tomas", "spokes", "forge",
                     "return", "install", "test", "load", "policy"]
            quest["prerequisiteIds"] = ["side_ashfall_cart_" + order[order.index(key) - 1]]
        if key == "salvage":
            quest["reward"]["items"] = [
                {"itemId": "ashfall_cart_iron", "quantity": 2},
                {"itemId": "ashfall_cart_spoke", "quantity": 1},
            ]
    if key == "policy":
        quest["choiceFlag"] = "ashfall_cart_use"
        quest["choiceSpeaker"] = "GIDEON PARK"
        quest["choicePrompt"] = "Chiếc xe vừa sửa nên được dùng theo cách nào trước?"
        quest["choices"] = [
            {"id": "shared_cart", "label": "Giữ một xe chung với lịch bàn giao", "flagValue": "shared",
             "dialogueId": "ashfall_cart_choice_shared", "reward": {"gold": 0,
             "items": [{"itemId": "ashfall_shared_cart_charm", "quantity": 1}]}},
            {"id": "household_kits", "label": "Phát bộ sửa nhỏ theo nhu cầu từng hộ", "flagValue": "household",
             "dialogueId": "ashfall_cart_choice_household", "reward": {"gold": 0,
             "items": [{"itemId": "ashfall_household_repair_charm", "quantity": 1}]}},
        ]
    quests.append(quest)
    dialogues.append({"id": dialogue_id, "speakerName": speaker, "lines": lines})
    codex.append({"id": "ashfall_cart_" + key + "_record", "title": record_title,
                  "category": "Ashfall Roadwork", "writtenBy": "Rowan Hale",
                  "unlockQuestId": quest["id"], "body": body})

dialogues.extend([
    {"id": "ashfall_cart_goblin_defeated", "speakerName": "ROWAN HALE",
     "lines": ["The goblin fled from beneath the cart. The axle and the iron salvage are still clear.",
               "I can finish the road check now without disturbing the damaged wheel or the loose spokes."]},
    {"id": "ashfall_cart_choice_shared", "speakerName": "GIDEON PARK",
     "lines": ["Xe chung có thể chở thuốc, chăn và dụng cụ nếu mỗi lượt bàn giao được ghi rõ.", "Ta sẽ để vạch quay cùng lịch cạnh chỗ đỗ để người kéo biết giới hạn đã thử."]},
    {"id": "ashfall_cart_choice_household", "speakerName": "GIDEON PARK",
     "lines": ["Bộ chốt nhỏ giúp từng hộ tự siết bánh lỏng mà không phải chờ xe chung.", "Mira sẽ giữ bản hướng dẫn. Người không muốn tự sửa vẫn có thể nhờ thợ."]},
])

landmark_entries = [{"id": key + "_marker", "locationId": location, "displayName": name,
                     "targetId": key, "visualId": visual, "positionX": x, "positionY": y,
                     "scale": 0.09} for key, name, location, visual, x, y in landmarks]

quests_catalog = read("prologue_quests.json")
dialogue_catalog = read("dialogue_catalog.json")
codex_catalog = read("codex_catalog.json")
landmark_catalog = read("quest_landmarks.json")
item_catalog = read("item_catalog.json")
recipe_catalog = read("recipe_catalog.json")
encounter_catalog = read("encounter_catalog.json")

upsert(quests_catalog["entries"], quests)
upsert(dialogue_catalog["entries"], dialogues)
upsert(codex_catalog["entries"], codex)
upsert(landmark_catalog["entries"], landmark_entries)
upsert(item_catalog["entries"], items)
upsert(recipe_catalog["entries"], recipe)
upsert(encounter_catalog["entries"], encounter)

for name, catalog in [("prologue_quests.json", quests_catalog), ("dialogue_catalog.json", dialogue_catalog),
                      ("codex_catalog.json", codex_catalog), ("quest_landmarks.json", landmark_catalog),
                      ("item_catalog.json", item_catalog), ("recipe_catalog.json", recipe_catalog),
                      ("encounter_catalog.json", encounter_catalog)]:
    write(name, catalog)

print("Upserted", len(quests), "Ashfall cart quests,")
print(len(dialogues), "dialogues,", len(codex), "codex records,", len(landmark_entries),
      "landmarks,", len(items), "items, one recipe and one gated encounter.")
