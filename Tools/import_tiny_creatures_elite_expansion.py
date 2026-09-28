#!/usr/bin/env python3
"""Add a second curated CC0 monster group with authored elite contracts."""

import json
import zipfile
from pathlib import Path

from import_tiny_creatures_fieldbook import ART, CONTENT, REGIONS, ROOT, read_catalog, write_catalog

ARCHIVE = ROOT / "Docs/AssetArchives/tiny-creatures-cc0.zip"

# tile, region, slug, name, rank, equipment slot, contract title, contract brief,
# post-fight field note one, field note two, equipment name, equipment description,
# move id, move reach
SPECIES = [
    (4, "af", "ashvault_flameskull", "Ashvault Flameskull", "elite", "charm",
     "Đốm lửa sau phiến giếng",
     "Mira Cole tìm thấy một hộp sọ biết bay quanh phiến đá giữ nước của làng. Hạ nó trước khi lớp lửa làm nứt vạch đo, rồi chép lại dấu than còn nguyên trên đá.",
     "Ngọn lửa bám vào vết khoan cũ chứ không lan theo gió. Tôi đánh dấu hai điểm riêng để thợ giếng không lấp nhầm một lỗ thông hơi.",
     "Phiến đo đã được che lại bằng tấm đồng. Dấu than vẫn đọc được; nó không chứng minh hộp sọ từng thuộc về một người trong làng.",
     "Mặt Dây Tàn Lửa", "Mảnh đồng giữ nhiệt được mài thành vòng bảo hộ; nó chặn bụi than khỏi cổ áo khi Rowan lướt sát nền. Tăng 1 Công và 1 Giáp.", "ranged_bolt", 7.2),
    (18, "do", "blue_drill_knight", "Azure Drill Knight", "common", "weapon",
     "Vết khoan trên khiên tập",
     "Nia Porter muốn mở lại sân khiên nơi cadet tập đội hình. Đánh bại Azure Drill Knight và ghi số vết lõm trên mặt khiên trước khi đội sửa chữa mang nó đi.",
     "Các vết lõm tập trung ở mép phải. Không vết nào xuyên qua lớp gỗ; tôi tách chúng khỏi dấu chém trên khung treo.",
     "Nia đã chuyển tấm khiên sang bàn kiểm kê thay vì trả lại kho tập. Bản ghi không nhận diện người từng sử dụng nó.",
     "Đao Cạnh Sân Tập", "Đao ngắn có sống dày để dùng trong không gian kín; chuôi được quấn hai màu cho dễ tìm trên sàn. Tăng 3 Công.", "line_charge", 5.4),
    (19, "do", "red_drill_knight", "Carmine Drill Knight", "common", "armor",
     "Móc đồng dưới giá áo",
     "Một bộ giáp đỏ kéo móc tập khỏi giá và chắn lối vào kho dụng cụ. Dẹp Carmine Drill Knight để Elara Wren kiểm lại dây đai, móc và phiếu mượn riêng từng món.",
     "Móc đồng bị cong về phía trong nên không thể dùng làm khóa cửa. Trên giáp có hai lớp sơn đỏ khác nhau.",
     "Elara ghi riêng dây đai và khung thép trong sổ kho. Bộ giáp đã được ráp lại nhiều lần, không còn là chứng cứ về một cadet cụ thể.",
     "Áo Khoác Móc Đồng", "Lớp lót dệt chặt giữ vai ổn định khi bị kéo khỏi vị trí, nhưng không thay được một cú lướt đúng lúc. Tăng 2 Giáp.", "hook", 3.7),
    (8, "db", "glassgaze_medusa", "Glassgaze Medusa", "elite", "weapon",
     "Ánh nhìn làm mờ mực",
     "Trong kho thư trả lại, mực trên ba phiếu chuyển bị hóa đục dù giấy không rách. Hạ Glassgaze Medusa để Elara đối chiếu phần chữ còn lại; đừng tự điền tên vào chỗ trống.",
     "Lớp tinh thể trên mắt phản quang về phía kệ thấp. Các phiếu bị đục có độ ẩm khác nhau nên tôi đặt chúng vào túi tách biệt.",
     "Elara đọc được ngày gửi trên một phiếu, nhưng người nhận đã nhòe. Bản ghi sẽ giữ ô đó trống cho tới khi có bản sao khác.",
     "Kiếm Gương Mờ", "Mặt thép xước tán ánh sáng thay vì phản chiếu thẳng vào mắt; mép kiếm có vạch khắc để căn độ dài từng nhát. Tăng 4 Công.", "marked_strike", 2.0,
    (15, "cw", "cinderwell_ogre", "Cinderwell Storehouse Ogre", "common", "armor",
     "Thùng gỗ bị ép lõm",
     "Talia Mercer cần lối vào kho giống thông thoáng. Đẩy Storehouse Ogre khỏi cửa và ghi lại những thùng bị ép trước khi người làm kho chuyển chúng sang hàng khác.",
     "Hai thùng rỗng bị ép từ phía ngoài; thùng thứ ba vẫn niêm kín. Tôi chụp vị trí then cửa trước khi nhóm kéo chúng ra.",
     "Talia tách hạt giống khỏi các bao rỗng để cân lại. Dấu va đập không cho biết ai đã xếp thùng sát cửa.",
     "Giáp Sườn Thùng Kho", "Các tấm gỗ cong được đóng vào dây đeo mềm, đỡ một cú va ngang mà vẫn để Rowan xoay người. Tăng 4 Giáp.", "shockwave", 4.5),
    (16, "cw", "redpass_wendigo", "Cinder-Rime Wendigo", "elite", "charm",
     "Hơi lạnh trong nhà ươm",
     "Một luồng lạnh trái mùa làm đóng băng chậu thử ở nhà ươm. Talia Mercer nhờ Rowan hạ Cinder-Rime Wendigo và kiểm tra ba khay cây ở các độ cao khác nhau.",
     "Lớp sương dày nhất nằm sát nền, còn lá phía trên không bị phủ. Tôi ghi chiều cao khay cùng thời điểm nhiệt kế hạ xuống.",
     "Nhà ươm đã được mở cửa theo giờ để thay khí. Hiện chưa rõ hơi lạnh đến từ vết nứt dưới sàn hay từ sinh vật vừa bị đánh bại.",
     "Bùa Ủ Mầm Tro", "Lá đồng giữ một túi cát ấm ở giữa các lớp vải, dùng để bảo vệ hạt qua một lần gió lạnh. Tăng 3 Công và 2 Giáp.", "line_charge", 5.9),
    (43, "cc", "cistern_ironroot_troll", "Ironroot Cistern Troll", "elite", "armor",
     "Rễ sắt trong rãnh thoát",
     "Talia Mercer phát hiện rễ kim loại chặn rãnh phía đông. Đánh bại Ironroot Cistern Troll rồi giữ nguyên hai đầu rễ để đội đo biết đoạn nào đã bị nhổ.",
     "Rễ gãy có vân đồng bên trong nhưng không nối với bánh van. Tôi để hai đầu cách nhau đúng một viên gạch.",
     "Lối thoát đã mở đủ cho nhóm lấy mẫu trở lại. Talia không ghi rễ là một phần của đường ống khi chưa có mặt cắt kim loại.",
     "Áo Tấm Rãnh Đông", "Các phiến giáp nhỏ ôm sát sườn để tránh vướng dây đo và cạnh đá sắc dưới bể. Tăng 5 Giáp.", "shockwave", 4.8),
    (47, "cc", "cistern_sump_elemental", "Sumpwater Elemental", "common", "weapon",
     "Gợn nước trong hộc cạn",
     "Một khối nước chuyển động ngược dốc trong hộc cạn. Rowan dẹp Sumpwater Elemental để nhóm đo lấy mẫu; Talia sẽ so màu nước với bản ghi của các hộc bên cạnh.",
     "Mẫu ở hộc cạn có lớp bột xám ở đáy. Tôi giữ nút chai riêng với phần nước trong để phòng cặn bị khuấy lên.",
     "Talia đánh số mẫu theo hộc, không theo thứ tự Rowan chạm vào chúng. Dòng chảy ngược đã dừng nhưng nguồn áp lực vẫn chưa rõ.",
     "Mũi Giá Đo Mạch", "Đầu thép dẹt có khía ở hai cạnh, dùng để gạt cặn khỏi khe mà không làm xước vạch đo. Tăng 6 Công.", "ranged_bolt", 6.1),
    (44, "sr", "saltflat_yeti", "Saltflat Yeti", "common", "charm",
     "Dấu chân lùi khỏi mốc",
     "Ruth Calder thấy dấu chân lớn kết thúc trước cột chỉ đường số ba. Hạ Saltflat Yeti và đo từng dấu từ mép ngoài; đừng nối chúng với đoàn người qua đèo nếu thiếu dấu tiếp theo.",
     "Khoảng cách giữa hai dấu ngắn dần khi tiến gần cột. Nền muối vỡ mất phần gót ở lượt thứ tư.",
     "Ruth vẽ phần mất gót bằng nét đứt. Dấu dừng lại trước cột, chưa cho biết con vật quay đầu hay đi trên nền đá.",
     "Bùa Mốc Muối", "Một vòng dây đánh dấu ba khoảng đo trên nền sáng, giúp nhóm quay lại đúng vết nứt sau bão muối. Tăng 4 Công và 2 Giáp.", "" , 0),
    (45, "sr", "redpass_sasquatch", "Redpass Stoneback", "common", "weapon",
     "Đá lăn không có dấu bánh",
     "Một tảng đá lăn khỏi mỏm Redpass nhưng mặt dưới không có vết bánh xe. Dẹp Redpass Stoneback rồi chép hướng trượt và phần cỏ bị ép để Ruth so với sơ đồ đèo.",
     "Cỏ bị ép thành hai dải song song, còn mặt đá chỉ có một lớp bụi. Tôi giữ sơ đồ hướng dốc riêng khỏi lời kể về đoàn xe.",
     "Ruth đã chặn lối vòng bằng cọc cảnh báo. Bản ghi chưa kết luận tảng đá do sinh vật đẩy hay do nền dốc sụt.",
     "Rìu Cọc Đèo", "Lưỡi rìu rộng để đóng cọc cảnh báo xuống nền muối cứng; phần sống có rãnh thoát bụi. Tăng 6 Công.", "line_charge", 5.6),
    (30, "sl", "lockhouse_whispering_succubus", "Lockhouse Whispering Veil", "elite", "charm",
     "Tiếng gọi sau cửa xả",
     "Âm thanh gọi người trực từ sau một cửa xả đã khóa. Ruth Calder yêu cầu Rowan hạ Whispering Veil rồi kiểm tra niêm phong trước và sau trận; không mở cửa chỉ vì giọng nói nghe quen.",
     "Tiếng gọi phát ra khi van đứng yên. Dấu phấn trên khóa đã bị kéo dọc nhưng đường kẻ vẫn liền.",
     "Ruth ghi cửa xả là chưa mở và lập lịch nghe lại với hai người trực. Một âm thanh có thể tái tạo không xác nhận người gọi đang ở phía kia.",
     "Mặt Dây Chống Vọng", "Hai lớp đồng lệch nhau làm giảm tiếng dội trong hành lang hẹp, để người gác nghe rõ tín hiệu đã thống nhất. Tăng 5 Công và 3 Giáp.", "siphon", 4.6),
    (29, "ch", "choir_saltweb_spider", "Saltweb Choir Spider", "common", "armor",
     "Sợi tơ trên chuông thấp",
     "Lyra Moss tìm thấy sợi tơ kéo ngang chuông thấp, làm mỗi nhịp ngân chậm hơn. Hạ Saltweb Choir Spider rồi đo độ trễ ba lần bằng cùng một nhịp gõ.",
     "Sợi tơ rung trễ hơn tiếng chuông nhưng lần thứ ba bị nhiễu bởi nước nhỏ. Tôi giữ cả ba số đo thay vì chọn giá trị đẹp nhất.",
     "Lyra gỡ tơ khỏi mặt chuông sau khi đã đánh dấu hướng buộc. Phép đo sau khi dọn phải được lưu thành một lượt riêng.",
     "Áo Sợi Chuông", "Các vòng dây mảnh trải lực trên vai khi bị kéo lệch, nhưng không chặn được âm thanh hay phép thuật. Tăng 6 Giáp.", "hook", 3.9),
    (50, "ch", "choir_glacier_wisp", "Glacier-Wick Wisp", "elite", "weapon",
     "Bấc xanh không có dầu",
     "Một đốm sáng xanh cháy trên chiếc đèn không có dầu ở Whisper Pool. Lyra Moss muốn đo vị trí phản chiếu trước khi hạ Glacier-Wick Wisp để tiếng nước lắng trở lại.",
     "Đốm sáng biến mất khỏi mặt nước khi nhìn thẳng nhưng trở lại ở góc xiên. Tôi đánh dấu vị trí người quan sát cạnh vị trí ảnh phản chiếu.",
     "Lyra tách nguồn sáng khỏi ảnh dưới nước trong sơ đồ. Sau trận, mặt hồ yên hơn nhưng chưa thể kết luận ánh sáng đến từ bấc hay từ mặt nước.",
     "Kiếm Bấc Xanh", "Lưỡi kiếm phủ một lớp men mờ giúp nhận ra bụi sáng bám trên mép, không làm thay đổi nhiệt độ đòn đánh. Tăng 8 Công.", "marked_strike", 2.0,
    (36, "gw", "greenwake_canopy_seraph", "Canopy Seraph", "elite", "weapon",
     "Bóng cánh trên luống giống",
     "Mara Bell nhận thấy bóng cánh quét qua luống giống nhưng không tìm thấy cành gãy. Hạ Canopy Seraph rồi đánh dấu hai lần bóng đi qua trước khi người làm vườn đổi tấm che.",
     "Bóng lệch về phía tây khi đám mây che mặt trời. Không có vết giẫm mới trên luống phía dưới.",
     "Mara đã đổi giờ che nắng để bảo vệ cây non. Bóng cánh không được ghi thành người canh giữ khu vườn.",
     "Liềm Cắt Bóng Lá", "Lưỡi cong đủ gọn để thu hoạch rễ non mà không làm bật cả luống, cán gỗ nhận biết bằng một vòng đồng. Tăng 9 Công.", "shockwave", 5.0),
    (32, "ow", "outerwake_azure_drake", "Aetherwake Azure Drake", "elite", "armor",
     "Vệt sáng cắt qua cột gió",
     "Dr. Evelyn Hart ghi một vệt sáng chạy ngược hướng gió quanh cột đo phía bắc. Hạ Aetherwake Azure Drake rồi kiểm tra vạch gió trước khi tháo tấm đồng bị cháy.",
     "Vạch trên cột bị mài từ phía ngoài vào. Hai lần đo gió sau trận lệch nhau trong giới hạn sai số của kim la bàn.",
     "Evelyn lưu tấm đồng cùng ghi chú hướng sáng, không gọi nó là tín hiệu cho tới khi có thể lặp lại phép đo.",
     "Áo Gió Lệch", "Các mảnh giáp đặt lệch tầng giảm lực gió xiên quanh cột đo; khe giữa chúng vẫn cho phép nhìn thấy bề mặt mẫu. Tăng 8 Giáp.", "ranged_bolt", 8.0),
    (37, "lo", "crownfall_glasswing_angel", "Crownfall Glasswing", "common", "charm",
     "Cánh giấy gần bàn giao",
     "Captain Alden tìm thấy những mảnh mỏng như cánh quanh bàn bàn giao hồ sơ. Hạ Crownfall Glasswing rồi ghi số mảnh còn nguyên trước khi đội cuối chuyển bàn.",
     "Các mảnh sáng ở hai mặt nhưng vỡ theo những hướng khác nhau. Tôi đặt chúng vào khay phẳng và đánh số trước khi nhặt.",
     "Alden giữ riêng bản kiểm kê mảnh vỡ và bản bàn giao. Chúng không đủ để gán một thông điệp cho người đã rời đi.",
     "Bùa Cánh Mỏng", "Lớp kính mờ giữ bụi khỏi bản đồ mà không che đường mực; dây đeo thay được khi phải chuyển tay người giữ. Tăng 5 Công và 4 Giáp.", "marked_strike", 2.2,
]

CODEX = {
    "af": ("Ashfall: Ash on the Water Stone", "Mira Cole", "Mira Cole tách dấu than khỏi vết khoan và vệt khói. Những phiến giếng bị chạm lửa không cho biết ai đã nhóm lửa; cô lưu giờ đo, hướng gió và phần đá đã được che lại.\n\nCác mẫu sau trận được giữ riêng theo vị trí. Nếu thợ giếng thay phiến đo, họ cần biết dấu nào còn nhìn thấy trước khi sửa chữa và dấu nào chỉ xuất hiện sau khi dọn đường."),
    "do": ("Dawnkeep: The Drill Yard Inventory", "Nia Porter", "Nia Porter ghi vết móp trên khiên và dây đeo ở hai trang khác nhau. Màu sơn không xác nhận ai từng đứng trong đội hình; móc cong không tự biến thành khóa cửa.\n\nCác món tập được đưa sang bàn kiểm kê để cadet có thể đối chiếu số hiệu và tình trạng. Sổ không lấp tên người mượn khi phiếu trả chưa được tìm thấy."),
    "db": ("Barracks Annex: Ink That Did Not Return", "Elara Wren", "Elara Wren giữ những phiếu có ngày gửi nhưng mất tên người nhận bên cạnh bản sao còn đọc được. Tinh thể làm đục mực được ghi theo vị trí và độ ẩm, không theo giả thuyết về người đã biến mất.\n\nKệ thấp được khóa khỏi luồng thư mới cho đến khi hoàn tất kiểm kê. Những ô trống trên danh sách vẫn được để trống để không biến một bề mặt mờ thành một kết luận."),
    "cw": ("Cinderwell: Heat at the Seed Store", "Talia Mercer", "Talia Mercer đối chiếu thùng giống bị ép với khay ươm đổi nhiệt. Dấu va đập, lớp sương và tình trạng hạt được ghi riêng; chúng không cho biết ai đã xếp hàng kho sát cửa.\n\nNhà ươm tiếp tục mở theo lịch đo để nhóm có thể so đất ở nhiều độ cao. Talia giữ cả lượt đo không thấy thay đổi vì nó cho biết khi nào nên dừng việc tìm một nguyên nhân chung."),
    "cc": ("Lower Cistern: Two Currents, One Ditch", "Talia Mercer", "Talia Mercer ghi lớp rễ kim loại, cặn xám và dòng nước đi ngược dốc trên ba sơ đồ khác nhau. Lối rãnh đã được mở để đội đo lấy mẫu, nhưng hướng dòng sau trận không tự chỉ ra ai từng đổi bánh van.\n\nCác vật liệu được đặt cạnh thước cùng ảnh vị trí trước khi dọn. Talia giữ nhãn theo hộc và theo lượt đo để mẫu ở chỗ nông không bị trộn với nước trong bể sâu."),
    "sr": ("Salt Road: Tracks Without a Cart", "Ruth Calder", "Ruth Calder so dấu chân với độ dốc, mặt muối và cỏ bị ép. Một khoảng cách ngắn dần không nói được ai đang chạy; một tảng đá lăn không chứng minh bánh xe đã đi qua.\n\nCọc cảnh báo được đặt sau khi Rowan đánh dấu hướng trượt. Phần bị mất của mỗi dấu được giữ bằng nét đứt, thay vì nối bằng trí nhớ của người đứng cạnh đường."),
    "sl": ("Lockhouse: A Voice Behind the Seal", "Ruth Calder", "Ruth Calder lưu âm thanh gọi người trực cạnh trạng thái của cửa xả. Khóa được kiểm tra hai lượt, trước và sau trận; đường phấn còn nguyên dù có vệt kéo dọc trên kim loại.\n\nLịch nghe lại cần hai người xác nhận cùng một thời điểm. Âm thanh quen thuộc không thay thế được việc mở niêm phong đúng thủ tục."),
    "ch": ("Choir: Delayed Sound, Separate Light", "Lyra Moss", "Lyra Moss ghi độ trễ của sợi tơ, chuông thấp và ánh đèn trên Whisper Pool thành những cột khác nhau. Góc nhìn của người đo và hướng nước đều được thêm vào sơ đồ phản chiếu.\n\nSau khi dọn lối, phép đo mới được đánh số thành lượt riêng. Mặt hồ yên lại không xác nhận nguồn sáng hay nguồn âm đã biến mất khỏi nơi này."),
    "gw": ("Greenwake: Shadows Across the Seed Beds", "Mara Bell", "Mara Bell đánh dấu bóng đi qua luống giống cùng hướng nắng và độ phủ mây. Không có cành gãy dưới luống; bóng cánh không chứng minh khu vườn có một người bảo vệ.\n\nLiềm mới được cất cạnh dụng cụ thu hoạch để người làm vườn không bật rễ khi cắt cây non. Các hàng cây lệch được giữ nguyên cho lần đo mùa sau."),
    "ow": ("Outer-Wake: Light Against the Wind", "Dr. Evelyn Hart", "Dr. Evelyn Hart ghi vệt sáng quanh cột đo cùng hướng gió, vết mài trên kim và sai số của la bàn. Tấm đồng cháy được giữ nguyên thay vì đánh bóng để tìm một hình dạng mong muốn.\n\nHai lượt đo sau trận không lặp lại độ lệch ban đầu. Cô lưu kết quả âm tính và chờ một điều kiện quan sát khác trước khi đặt tên cho tín hiệu."),
    "lo": ("Crownfall: A Separate Tray for Fragments", "Captain Alden Vale", "Captain Alden Vale đánh số từng mảnh gần bàn bàn giao trước khi chuyển hồ sơ cuối. Vết vỡ không khớp một hướng duy nhất, và mảnh sáng không tự trở thành chữ viết.\n\nBản kiểm kê đồ vật nằm cạnh danh sách người rời Reach nhưng không được gộp vào đó. Alden để nguyên những khoảng chưa thể giải thích cho người kế tiếp."),
}


def main():
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing source archive: {ARCHIVE}")
    if len(SPECIES) != 16 or len(CODEX) != len(REGIONS):
        raise SystemExit("Elite expansion source data is incomplete.")

    file_names = [
        "monster_catalog.json", "encounter_catalog.json", "prologue_quests.json",
        "item_catalog.json", "dialogue_catalog.json", "codex_catalog.json"
    ]
    paths, catalogs = {}, {}
    for file_name in file_names:
        paths[file_name], catalogs[file_name] = read_catalog(file_name)

    expected = []
    for tile, code, slug, *_ in SPECIES:
        expected.extend([
            f"tiny_elite_{code}_{slug}", f"side_elite_{code}_{slug}",
            f"elite_{code}_{slug}_site", f"fieldgear_{code}_{slug}",
            f"rowan_elite_{slug}_record"
        ])
    for code in REGIONS:
        if code in CODEX:
            expected.append(f"elite_codex_{code}")
    existing = {entry.get("id", "") for data in catalogs.values() for entry in data["entries"]}
    found = [entry_id for entry_id in expected if entry_id in existing]
    if found:
        if len(found) == len(expected) and all((ART / f"tiny_{tile:04d}.png").is_file()
                                               for tile, *_ in SPECIES):
            print("Tiny Creatures elite expansion is already imported; no changes made.")
            return
        raise SystemExit("Partial elite expansion detected; inspect generated catalogs before retrying.")

    additions = {name: [] for name in file_names}
    mapping_rows = []
    last_contract_by_region = {}
    with zipfile.ZipFile(ARCHIVE) as archive:
        for tile, code, slug, name, rank, slot, *_ in SPECIES:
            resource = f"tiny_{tile:04d}"
            source = f"tiny-creatures/Tiles/tile_{tile:04d}.png"
            destination = ART / f"{resource}.png"
            if destination.exists():
                raise SystemExit(f"Sprite resource already exists: {resource}")
            destination.write_bytes(archive.read(source))
            region = REGIONS[code]
            mapping_rows.append((tile, resource, f"tiny_elite_{code}_{slug}", name, rank,
                                 region["location"], slot))

    for tile, code, slug, name, rank, slot, title, brief, note_one, note_two, item_name, item_desc, move, reach in SPECIES:
        region = REGIONS[code]
        monster_id = f"tiny_elite_{code}_{slug}"
        quest_id = f"side_elite_{code}_{slug}"
        encounter_id = f"elite_{code}_{slug}_site"
        item_id = f"fieldgear_{code}_{slug}"
        dialogue_id = f"rowan_elite_{slug}_record"
        prerequisite = last_contract_by_region.get(code, region["root"])
        last_contract_by_region[code] = quest_id
        level = region["level"]
        elite = rank == "elite"
        attack_reach = 1.25
        special_reach = float(reach)
        max_health = 32 + level * 7 + (42 if elite else 0)
        attack = 4 + level + (4 if elite else 0)
        item_attack = level + (2 if slot == "weapon" else 0) if slot == "weapon" else max(1, level // 2) + (1 if elite else 0) if slot == "charm" else 0
        item_guard = 0 if slot == "weapon" else max(1, (level * 3 + 2) // 4) + (1 if elite else 0) if slot == "armor" else max(1, level // 3)
        equipment_text = item_desc + f" Tăng {item_attack} Công và {item_guard} Giáp."

        additions["monster_catalog.json"].append({
            "id": monster_id, "displayName": name, "rank": rank,
            "maxHealth": max_health, "attackDamage": attack, "attackReach": attack_reach,
            "approachSpeed": round(0.88 + min(level, 10) * 0.028 + (0.06 if elite else 0), 3),
            "lungeDistance": 1.65 if not elite else 1.9, "lungeSeconds": 0.34,
            "lungeStopDistance": 0.68, "openingDelay": round(1.3 - min(level, 8) * 0.035, 3),
            "closingSeconds": 1.12 if not elite else 1.2,
            "telegraphSeconds": 0.82 if not elite else 1.08,
            "recoverySeconds": 0.95 if not elite else 1.08,
            "counterBonusDamage": 12 if not elite else 20,
            "hitCooldown": round(0.7 - min(level, 5) * 0.025, 3),
            "spriteResource": f"tiny_{tile:04d}", "lungeSpriteResource": "",
            "spriteScale": 2.55 if not elite else 2.7, "spritePixelsPerUnit": 16,
            "specialMoveId": move, "specialMoveReach": special_reach
        })

        position_index = sum(1 for row in SPECIES[:SPECIES.index((tile, code, slug, name, rank, slot,
                          title, brief, note_one, note_two, item_name, item_desc, move, reach))]
                            if row[1] == code)
        position = region["positions"][position_index]
        additions["encounter_catalog.json"].append({
            "id": encounter_id, "monsterId": monster_id, "locationId": region["location"],
            "positionX": position[0], "positionY": position[1], "requiredQuestId": quest_id,
            "blockedQuestId": "", "blockedDialogueId": "", "contributesToQuest": True,
            "defeatObjectiveTargetId": monster_id, "defeatDialogueId": dialogue_id,
            "downDialogueId": "rowan_field_retreat",
            "reward": {"gold": 8 + level * 3, "items": []}
        })
        additions["item_catalog.json"].append({
            "id": item_id, "name": item_name, "description": equipment_text,
            "category": "equipment", "equipmentSlot": slot, "maxStack": 1,
            "attackBonus": item_attack, "guardBonus": item_guard, "healAmount": 0,
            "sellValue": 48 + level * 10
        })
        additions["prologue_quests.json"].append({
            "id": quest_id, "arcId": region["arc"], "stage": -1,
            "type": "side", "locationId": region["location"], "giverId": region["giver"],
            "title": title, "objective": brief, "prerequisiteIds": [prerequisite],
            "objectives": [{"id": f"defeat_{slug}", "kind": "defeat", "targetId": monster_id,
                            "requiredCount": 1,
                            "description": f"Đánh bại {name} và ghi lại mẫu vật tại hiện trường."}],
            "reward": {"gold": 18 + level * 3,
                       "items": [{"itemId": item_id, "quantity": 1}]}
        })
        additions["dialogue_catalog.json"].append({
            "id": dialogue_id, "speakerName": "ROWAN HALE", "lines": [note_one, note_two]
        })

    for code, region in REGIONS.items():
        if code not in CODEX:
            continue
        title, author, body = CODEX[code]
        additions["codex_catalog.json"].append({
            "id": f"elite_codex_{code}", "title": title, "category": "Field Bestiary",
            "writtenBy": author, "unlockQuestId": last_contract_by_region[code], "body": body
        })

    for name, data in catalogs.items():
        before = {entry.get("id", "") for entry in data["entries"]}
        new_ids = [entry["id"] for entry in additions[name]]
        if len(new_ids) != len(set(new_ids)) or before.intersection(new_ids):
            raise SystemExit(f"Duplicate catalog IDs found while generating {name}.")

    if len(mapping_rows) != 16 or len({row[0] for row in mapping_rows}) != 16:
        raise SystemExit("Source-to-species map must contain sixteen distinct creature sprites.")
    mapping_path = ROOT / "Docs/AssetArchives/tiny-creatures-species-map.tsv"
    with mapping_path.open(encoding="utf-8") as stream:
        existing_lines = stream.read()
    with mapping_path.open("a", encoding="utf-8") as stream:
        stream.writelines("\t".join(map(str, row)) + "\n" for row in mapping_rows)

    try:
        for name, append_entries in additions.items():
            catalogs[name]["entries"].extend(append_entries)
            write_catalog(paths[name], catalogs[name])
    except Exception:
        mapping_path.write_text(existing_lines, encoding="utf-8")
        raise

    print("Imported 16 Tiny Creatures sprites; authored 16 elite/common contracts, "
          "16 encounter placements, 16 equipment rewards, 16 field dialogues and 11 ecological records.")


if __name__ == "__main__":
    main()
