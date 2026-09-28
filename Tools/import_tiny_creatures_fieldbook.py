#!/usr/bin/env python3
"""Import a curated CC0 creature subset and its authored field-contract content."""

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "Docs/AssetArchives/tiny-creatures-cc0.zip"
CONTENT = ROOT / "Assets/Resources/Content"
ART = ROOT / "Assets/Resources/Art"

REGIONS = {
    "af": {
        "location": "ashfall_village", "arc": "ashes_of_ashfall", "level": 1,
        "giver": "mira_cole", "author": "Mira Cole", "root": "ashfall_choice",
        "positions": [(-9.0, 4.0), (-9.0, -4.0), (9.0, 4.0), (9.0, -4.0)],
        "codex_title": "Ashfall: Field Notes Beyond the Well",
        "codex": "Mira Cole lập phần phụ lục này sau khi Rowan trở về từ những con đường quanh Ashfall. Cô so sánh dấu chân, lớp tro và thời điểm các sinh vật rời chỗ ẩn, nhưng không dùng chúng để suy ra ai đã mở đường cho cuộc đột kích. Một bộ xương cũ có thể nằm gần vết cháy mà không thuộc về đêm ấy; dấu móng goblin cũng có thể chồng lên dấu của người đi cứu thương.\\n\\nBốn cuộc chạm trán trong bản ghi được chọn vì chúng khiến người sống quanh giếng phải đổi lối đi. Mira yêu cầu ghi ngày, vị trí và hướng gió cạnh mỗi quan sát. Nếu Rowan chỉ nhớ mình đã thắng, các gia đình vẫn không biết đoạn đường nào an toàn vào buổi tối. Cô giữ phần kết luận ngắn: mối nguy đã bị dẹp ở những vị trí cụ thể; nguyên nhân của từng dấu vết vẫn cần chứng cứ riêng."
    },
    "do": {
        "location": "dawnkeep_outpost", "arc": "the_order_of_the_dawn", "level": 2,
        "giver": "nia_porter", "author": "Nia Porter", "root": "order_cadet_oath",
        "positions": [(-9.0, 4.0), (-9.0, -4.0), (9.0, 4.0), (9.0, -4.0)],
        "codex_title": "Dawnkeep Outpost: Tracks Beside the Drill Yard",
        "codex": "Nia Porter dùng sổ tuần tra của sân tập để ghi những loài xuất hiện ở rìa khu đồn. Cô không gọi các hiệp sĩ rỗng là cadet mất tích: giáp giống nhau không chứng minh người bên trong từng phục vụ Order. Dấu móng ở tường bắc cũng không nói được sinh vật đến từ phía nào nếu người gác không đánh dấu thời gian đổi ca.\\n\\nCác trang mới ghép lời báo của lính gác với những vết xước Rowan nhìn thấy sau giao chiến. Khi một lối đi được dọn sạch, Nia thêm giờ tuần tra thay vì xóa cả đoạn khỏi bản đồ. Cô muốn gia đình cadet có thể hỏi ai đã kiểm tra cổng, ngày nào và bằng cách nào. Sổ này vì vậy giữ cả những lần không thấy dấu mới, không chỉ các trận đánh có nhân chứng."
    },
    "db": {
        "location": "dawnkeep_barracks", "arc": "the_order_of_the_dawn", "level": 2,
        "giver": "elara_wren", "author": "Elara Wren", "root": "order_cadet_oath",
        "positions": [(-8.5, 3.7), (-8.5, -3.7), (8.5, 3.7)],
        "codex_title": "Barracks Annex: What the Returned Letters Describe",
        "codex": "Elara Wren mở phụ lục này trong căn phòng từng dùng làm kho thư chưa phát. Cô phân biệt dấu vết của một sinh vật với dấu người chạy trốn: một vệt cào chỉ cho biết móng đã chạm vào gỗ, còn hướng chạy cần ít nhất hai dấu liên tiếp. Những đồ vật bị kéo khỏi kệ cũng có thể do đội cứu hộ dọn lối, vì vậy mỗi trang ghi rõ ai đã ở đó trước khi Rowan tới.\\n\\nBa cuộc kiểm tra mới buộc Elara sửa sơ đồ luồng thư, không phải danh sách người mất tích. Cô ghi tên người báo, giờ nhận tin và phần chưa thể đối chiếu với phiếu chuyển quân. Một con quái vật bị đánh bại không trả lời lá thư nào đã tới tay người nhận; nó chỉ làm căn phòng an toàn hơn để những người còn sống tiếp tục tìm."
    },
    "cw": {
        "location": "cinderwell_basin", "arc": "crown_of_empty_fields", "level": 4,
        "giver": "talia_mercer", "author": "Talia Mercer", "root": "cinder_june_report",
        "positions": [(-9.0, 4.0), (-9.0, -4.0), (9.0, 4.0), (9.0, -4.0)],
        "codex_title": "Cinderwell: Wet Ground, Separate Causes",
        "codex": "Talia Mercer ghi các sinh vật quanh lòng chảo theo độ ẩm của đất, không theo lời đồn rằng mọi vết bệnh đều bắt đầu từ cùng một nguồn nước. Cây ăn thịt mọc ở rãnh cạn không chứng minh ai đã mở van; nấm trên bao hạt có thể xuất hiện sau khi kho bị ngập. Cô đặt từng dấu chân cạnh bản đồ mực nước và đánh dấu lúc đo.\\n\\nNhững cuộc chạm trán được Rowan xử lý giúp người tị nạn đi lại giữa bể và luống cây mà không phải tự vệ. Talia giữ riêng hai sổ: một sổ về mối nguy sinh học, một sổ về lượng nước và hạt giống. Nếu chúng được gộp thành một lời buộc tội, người ghi sổ sẽ mất khả năng sửa kết luận khi phép đo mới xuất hiện."
    },
    "cc": {
        "location": "cinder_cistern", "arc": "crown_of_empty_fields", "level": 5,
        "giver": "talia_mercer", "author": "Talia Mercer", "root": "cinder_cistern_warden",
        "positions": [(-9.0, 4.0), (-9.0, -4.0), (9.0, 4.0), (9.0, -4.0)],
        "codex_title": "Lower Cistern: Layers That Keep Moving",
        "codex": "Talia viết phần này từ bậc thang khô phía trên đường nước. Một lớp nhầy có thể làm mờ số khắc trên thành bể, nhưng không cho biết ai đã thay thước. Giun đào rãnh làm đổi hướng dòng chảy trong nhiều giờ; khối gel lấp khe tạm thời rồi tan khi nhiệt độ đổi. Cô yêu cầu Rowan ghi vị trí vết mới trước khi dọn sạch nó.\\n\\nHai mẫu canh giữ vùng bể sâu không được xem như cùng một sinh vật chỉ vì chúng đều hồi phục sau đòn đánh. Talia tách bản phác họa, kích thước vùng nguy hiểm và phản ứng với ánh đèn thành các cột khác nhau. Sau khi đường tuần tra an toàn hơn, đội đo nước có thể quay lại mà không giẫm lên bằng chứng. Bản ghi vẫn để trống câu hỏi ai đã thiết kế cửa dưới hồ."
    },
    "sr": {
        "location": "salt_road", "arc": "the_salt_road", "level": 6,
        "giver": "ruth_calder", "author": "Ruth Calder", "root": "salt_reckoning",
        "positions": [(-9.0, 4.0), (-9.0, -4.0), (9.0, 4.0), (9.0, -4.0)],
        "codex_title": "Salt Road: The Road Has More Than One Witness",
        "codex": "Ruth Calder ghi thú săn mồi và các nhóm đi qua đèo trong những cột riêng. Một dấu móng gnoll gần bánh xe caravan không chứng minh chúng gây ra vụ thảm sát; dấu chân người có thể được để lại sau khi đoàn cứu hộ quay lại nhặt thẻ tên. Rowan dọn những sinh vật đe dọa tuyến đường, còn Ruth giữ bản đồ chưa bị xóa các lối rẽ.\\n\\nMỗi cuộc tuần tra được đánh dấu theo hướng gió, độ mặn của đất và tình trạng chuông trạm. Thẻ crossing tìm thấy trên đường chỉ ra ai đã được cấp quyền qua cổng, không nhất thiết ai đã thực sự đi qua. Ruth giữ câu hỏi này trong lề sổ để người đọc không nhầm một vật được phát với một hành trình đã hoàn tất."
    },
    "sl": {
        "location": "salt_lockhouse", "arc": "the_salt_road", "level": 7,
        "giver": "ruth_calder", "author": "Ruth Calder", "root": "salt_lockhouse_bailiff",
        "positions": [(-9.5, 4.4), (-9.5, -4.4), (9.5, 4.4)],
        "codex_title": "Lockhouse: Names Beneath the Salt",
        "codex": "Ruth Calder ghi lại cuộc dọn đường sau trận Bailiff để nhóm chuyển sổ cân có thể trở lại tầng dưới. Lớp vải quấn quanh xác khô không còn mang nhãn đọc được; cô không gọi chúng là thẻ tù nhân cho đến khi đối chiếu được với hồ sơ nhận dạng. Tiếng khóc vang trong hành lang có thể dội từ nhiều buồng kín, nên vị trí âm thanh được ghi theo từng lượt nghe.\\n\\nNhững sinh vật bị Rowan đánh bại đã chặn các lối nối giữa kho hồ sơ và cửa xả. Dọn lối không đồng nghĩa với mở cửa niêm phong: Ruth đánh dấu riêng cửa đã kiểm tra, cửa còn khóa và dấu vết chưa có ảnh chụp. Bản phụ lục không khẳng định ai đã đưa người xuống lockhouse. Nó chỉ giúp đội điều tra làm việc mà không phải bỏ lại một con đường nguy hiểm sau lưng."
    },
    "ch": {
        "location": "choir_beneath_lake", "arc": "the_choir_beneath_the_lake", "level": 8,
        "giver": "lyra_moss", "author": "Lyra Moss", "root": "choir_reckoning",
        "positions": [(-10.0, 4.5), (-10.0, -4.5), (10.0, 4.5), (10.0, -4.5)],
        "codex_title": "Choir: Water, Voice and Echo",
        "codex": "Lyra Moss đo tiếng vọng sau khi những sinh vật quanh vòm chuông không còn cản đường Rowan. Cô ghi mỗi âm thanh ba lần, so độ trễ và bỏ riêng lần có tiếng giáp va vào đá. Một giọng giống người không chứng minh có người đang ở phía bên kia; nước có thể làm một nốt đơn kéo dài thành hai.\\n\\nSiren, nàng cá và đốm sáng dưới hồ được đánh dấu bằng hình thể và âm phổ quan sát được. Lyra không viết chúng là ký ức sống của người mất tích. Bản ghi chỉ cho thấy các sinh vật phản ứng khác nhau trước cùng một nhịp chuông. Cô yêu cầu người tiếp quản giữ lại cả mẫu nghe sai để lần đo sau biết những gì đã bị loại và vì sao."
    },
    "gw": {
        "location": "greenwake_refuge", "arc": "the_hundredth_champion", "level": 9,
        "giver": "the_first_warden", "author": "The First Warden", "root": "champion_star_map",
        "positions": [(-10.0, 4.5), (-10.0, -4.5), (10.0, 4.5), (10.0, -4.5)],
        "codex_title": "Greenwake: A Garden Does Not Own Its Keepers",
        "codex": "The First Warden ghi các sinh vật quanh khu vườn bằng tên mà người làm vườn chấp nhận, không dùng danh hiệu của Crown. Rễ cây có thể mọc xuyên nền đá mà không phải là lời chúc phúc; một con thú ngủ dưới tán lá cũng không chứng minh nó bảo vệ người trồng. Ông đánh dấu chỗ trú, giờ ăn và khoảng cách người đi hái cần giữ.\\n\\nNhững loài Rowan xử lý đã khiến đường ra giếng và kho hạt không còn an toàn. Bản ghi không coi việc đánh bại chúng là bài kiểm tra lòng trung thành. The First Warden giữ nguyên các luống cây còn mọc lệch khỏi hàng, vì chúng có thể đang thích nghi tốt hơn những gì người dựng hàng rào dự định. Mùa sau có thể làm phần kết luận này sai; ông muốn người đọc biết điều đó."
    },
    "ow": {
        "location": "outerwake_archive", "arc": "archive_beyond_veil", "level": 10,
        "giver": "evelyn_hart", "author": "Dr. Evelyn Hart", "root": "archive_return_report",
        "positions": [(-10.0, 4.5), (-10.0, -4.5), (10.0, 4.5), (10.0, -4.5)],
        "codex_title": "Outer-Wake: Organisms Without a Local Baseline",
        "codex": "Dr. Evelyn Hart lập phụ lục này vì sinh vật ở Outer-Wake không có mẫu so sánh đáng tin trong kho Asterra. Vảy như kính không chứng minh chúng sinh ra ngoài thế giới; lửa xanh cũng có thể là phản ứng với khoáng chất tại chỗ. Mỗi trang ghi màu dưới hai nguồn sáng, khoảng cách phát hiện và sai số trong la bàn.\\n\\nRowan dọn ba điểm tuần tra để nhóm có thể lấy mẫu mà không tiến sát tổ. Evelyn tách dấu hiệu quan sát được khỏi giả thuyết về nguồn gốc. Một sinh vật bay qua khe Veil không chứng minh tín hiệu đến từ cùng nơi. Các tệp đo được đánh số cả khi không lặp lại kết quả; điều chưa tái hiện là một phần của hồ sơ, không phải lý do để xóa trang."
    },
    "lo": {
        "location": "last_oath_reach", "arc": "two_last_oaths", "level": 11,
        "giver": "captain_alden_vale", "author": "Captain Alden Vale", "root": "last_oath_choice",
        "positions": [(-10.0, 4.5), (-10.0, -4.5), (10.0, 4.5), (10.0, -4.5)],
        "codex_title": "Crownfall: Creatures at the End of a Cycle",
        "codex": "Captain Alden Vale ký sổ tuần tra này sau khi Rowan chọn lời thề cuối. Ông tách các sinh vật hiện ra gần Cycle Heart khỏi những người đã từng phục vụ trong Order. Một chiếc vảy đen không đủ để gọi chủ nhân của nó là Ma Vương; hình sphinx trên cổng cũng không phải dấu xác nhận của Ý Chí Thế Giới.\\n\\nCác tuyến đường được ghi theo lần kiểm tra, kể cả khi hai cuộc hành trình đi theo cùng một lối. Alden cho rằng một thế giới chỉ có thể được giao lại nếu người kế tiếp biết điều gì đã được nhìn thấy tận mắt và điều gì chỉ được kể lại. Ông không dùng chiến thắng của Rowan làm bằng chứng rằng chu kỳ tiếp theo sẽ tốt hơn. Mỗi cuộc tuần tra khép một nguy cơ cụ thể, còn lựa chọn về thế giới vẫn nằm ngoài cuốn sổ này."
    }
}

# region, sprite tile index, slug, name, rank, equipment slot, quest title,
# authored quest brief, two unique post-fight field notes, equipment name,
# equipment description, attack pattern
SPECIES = [
    ("af", 1, "ashbound_zombie", "Ashbound Zombie", "common", "weapon", "Tro ấm dưới giếng",
     "Mira Cole nhận thấy tro quanh giếng ấm lên sau hoàng hôn. Hãy đánh bại Ashbound Zombie ở rìa làng để người gánh nước có thể đi lại, rồi ghi lại lớp tro không bị xới.",
     "Lớp tro quanh khớp tay nó ẩm hơn tro trên mặt đường. Tôi ghi nhiệt độ và giờ, nhưng chưa biết nó tới từ giếng hay từ một đống than cũ.",
     "Người dân có thể trở lại lấy nước tối nay. Dấu chân quanh thành giếng vẫn phải được so với lời khai của những người đã chạy qua đây.",
     "Đoản Kiếm Tro Tàn", "Lưỡi ngắn do Mira bọc lại từ thép cứu hộ, có rãnh thoát bụi thay vì một ký hiệu Order. Tăng 1 Công.", ""),
    ("af", 2, "grave_skeleton", "Grave Skeleton", "common", "armor", "Bộ xương ngoài hàng rào",
     "Một bộ xương đứng chặn lối phía bắc, nơi đội cứu hộ thường đưa người bị thương ra khỏi làng. Dẹp mối nguy đó để lối đi mở lại; đừng xem lớp giáp rỉ là bằng chứng về chủ nhân.",
     "Các mảnh xương không đồng màu và không khớp vào một bộ áo giáp. Tôi ghi từng mảnh tại chỗ trước khi kéo chúng khỏi lối.",
     "Lối cứu thương đã thông. Bộ giáp có thể được lắp từ nhiều nơi; Elara sẽ cần xem dấu dập trước khi ghi tên một đơn vị.",
     "Áo Lót Xương Rời", "Áo lót nhẹ khâu từ những tấm da cứu hộ, có lớp đệm thay được khi bị bụi tro cào rách. Tăng 1 Giáp.", ""),
    ("af", 11, "ash_goblin", "Ash Goblin", "common", "charm", "Dấu chân nhỏ ở kho lương",
     "Gideon Park phát hiện những túi đậu bị rạch nhưng không bị lấy đi. Đánh bại Ash Goblin đang lẩn gần kho, giữ nguyên các đường cắt để Mira phân biệt vết móng với vết dao.",
     "Vết rạch đi qua bao chứ không nhắm vào thức ăn. Tôi giữ một mép vải có dấu móng, còn Mira sẽ đối chiếu với dụng cụ của đội cứu hộ.",
     "Gideon có thể khóa kho mà không bỏ các túi giống xuống đất. Một lần đột nhập không giải thích được những bao lương đã biến mất từ tuần trước.",
     "Móc Túi Người Sống Sót", "Mặt dây nhỏ giữ ba mảnh vải có dấu cắt khác nhau, giúp nhận ra một túi cứu trợ đã bị mở lại. Tăng 1 Công và 1 Giáp.", "hook"),
    ("af", 40, "well_imp", "Cinder Imp", "common", "weapon", "Tàn lửa không có nguồn",
     "Một Cinder Imp quấy phá lò sưởi trú ẩn mỗi khi người dân nhóm lửa. Hạ nó trước giờ phát thuốc, rồi đối chiếu màu tàn với than ở bếp để không gộp hai nguồn nhiệt.",
     "Tàn lửa trên lưng nó tắt nhanh hơn than bếp, nhưng màu dưới khói giống nhau. Tôi lấy hai mẫu riêng và đánh số trước khi chúng nguội.",
     "Mira đã nhóm lại bếp. Người bị ho có thể dùng nước ấm; chuyện ngọn lửa của con imp bắt đầu ở đâu vẫn chưa rõ.",
     "Lưỡi Gạt Tàn Cam", "Thợ rèn làng mài lưỡi cong để gạt than khỏi khe lò mà không làm tung bụi vào thức ăn. Tăng 2 Công.", "shockwave"),

    ("do", 17, "dawnkeep_green_knight", "Green Knight", "common", "weapon", "Hiệp sĩ rỗng ngoài sân tập",
     "Nia Porter nghe tiếng giáp kéo lê ngoài hàng bia phía đông. Đánh bại Green Knight để cadet trở lại sân, rồi ghi số hiệu còn đọc được trước khi mưa làm sạch vết khắc.",
     "Số trên miếng vai bị dũa mất phần cuối. Màu sơn xanh không trùng với màu áo huấn luyện hiện tại của Dawnkeep.",
     "Nia niêm phong miếng vai để gia đình có thể xem. Một bộ giáp từng ở sân tập không chứng minh người mặc nó đã được điểm danh.",
     "Kiếm Gác Sân Dawnkeep", "Thanh kiếm ngắn cân bằng cho người đứng gác bia tập; chuôi bọc vải sáng để dễ phân biệt trong kho. Tăng 2 Công.", "line_charge"),
    ("do", 20, "dawnkeep_wight", "Roster Wight", "common", "armor", "Bóng đứng sau bia tên",
     "Một Roster Wight đứng sau bia khắc tên cadet mỗi lần đổi ca. Dẹp nó để Nia kiểm tra các rãnh chữ; không suy ra danh tính từ hình dáng bóng người.",
     "Nó dừng trước hàng cuối nhưng không chạm vào bia. Tôi đo dấu chân và hướng nhìn thay vì viết rằng nó đang đọc tên ai.",
     "Các rãnh chữ vẫn nguyên. Nia sẽ đối chiếu chúng với bản dập cũ, còn hành vi của cái bóng được ghi là quan sát riêng.",
     "Giáp Vai Chừa Lề", "Miếng giáp lệch một bên để người mang vẫn nhìn thấy cánh tay đồng đội trong đội hình hẹp. Tăng 2 Giáp.", ""),
    ("do", 25, "gate_werewolf", "Gate Werewolf", "common", "charm", "Tiếng cào ở cổng hàng",
     "Người chuyển thư không dám qua cổng phía tây vì Gate Werewolf cào vào chốt gỗ. Hạ nó trước chuyến thư kế tiếp; giữ lại mảnh gỗ có răng cắm để xem chiều móng.",
     "Các vết cào hướng ra ngoài, nhưng gỗ có thể đã bị lật khi sửa chốt. Tôi ghi cả mặt bản lề và mặt đường.",
     "Cổng mở lại cho người đưa tin. Nia sẽ hỏi ca gác trước, vì vết cào tự nó không nói ai đã đóng cổng.",
     "Móc Cổng Hai Mặt", "Chiếc móc nhỏ được đúc hai đầu, một đầu giữ then và đầu kia gạt bản lề kẹt mà không phá dấu sơn. Tăng 1 Công và 2 Giáp.", "hook"),
    ("do", 70, "dawnkeep_gargoyle", "Dawnkeep Gargoyle", "elite", "weapon", "Thú đá trên mái cổng",
     "Dawnkeep Gargoyle lao xuống khi người gác bước dưới mái cổng. Hạ nó trong sân trống để tránh thương tích, sau đó báo đúng vị trí mảnh đá rơi cho Nia.",
     "Mặt dưới cánh đá không có vết khắc của Order. Các mảnh rơi nằm về phía sân, dù hướng lao cuối cùng lại quay ra đường.",
     "Sân đã an toàn để sửa mái. Nia đánh dấu chỗ rơi bằng hai màu phấn để người sửa chữa không xóa mất đường lao.",
     "Nanh Đá Mài Mỏng", "Mũi kiếm ngắn lấy cảm hứng từ cạnh đá vỡ, đủ cứng để cắt dây mục nhưng không mang phù hiệu của người gác. Tăng 4 Công.", "shockwave"),

    ("db", 3, "barracks_vampire", "Letter Vault Vampire", "common", "armor", "Cánh thư bị hút sạch mực",
     "Elara Wren tìm thấy những lá thư nhạt màu trong kho trả lại. Đánh bại Letter Vault Vampire để dọn lối, rồi chụp vị trí từng phong bì trước khi ai đó sắp chúng theo người gửi.",
     "Mực biến mất ở phần địa chỉ trước, còn lời nhắn bên trong vẫn đọc được. Tôi tách ba phong bì thay vì gọi tất cả là thư chưa gửi.",
     "Các lá thư đã được đặt trong túi trong suốt. Elara sẽ không suy số người nhận từ số phong bì cho đến khi sổ phát thư được kiểm tra.",
     "Áo Choàng Mực Bạc", "Lớp áo xám bạc có cổ cao, phủ ngoài giấy tờ khi mang qua hành lang bụi. Tăng 2 Giáp.", "siphon"),
    ("db", 66, "barracks_dark_mage", "Dusk Archive Mage", "common", "weapon", "Đèn tím trong kho trả lại",
     "Một Dusk Archive Mage thắp những đốm sáng tím giữa các kệ thư. Elara muốn lối đi an toàn trước khi tiếp tục đọc; hạ nó rồi ghi kệ nào bị xê dịch, không đoán nội dung phép.",
     "Đốm sáng tắt cùng lúc ở ba kệ khác nhau. Tôi không biết đó là tín hiệu hay chỉ là cách luồng khí chạy qua căn phòng.",
     "Elara đã dựng lại giá sách theo dấu bụi. Những lá thư đổi vị trí được đánh dấu riêng thay vì đặt lại vào ngăn gần nhất.",
     "Trượng Đọc Lề", "Một thanh trượng mảnh có vòng đồng giữ bản đồ kho, giúp soi khe tối mà không phải tháo cả kệ. Tăng 3 Công.", "line_charge"),
    ("db", 68, "barracks_harpy", "Barracks Harpy", "common", "charm", "Mái hiên có lông xám",
     "Harpy đậu trên máng thoát nước, làm các mảnh giấy bay vào sân. Dẹp nó để Elara thu những mảnh còn đọc được; ghi hướng gió trước khi ghép chúng lại.",
     "Giấy rơi về phía cổng trong hai lần gió đổi. Tôi đánh dấu chiều bay nhưng chưa ghép các mảnh thành câu.",
     "Mảnh giấy đã được đặt theo số trang, không theo nét chữ. Một câu ghép thiếu góc có thể dẫn tới người nhận sai.",
     "Mề Đay Lông Mái", "Một mề đay bọc lớp lông xám đã làm sạch, giữ bản đồ kho khỏi trượt khỏi áo khi gió lùa. Tăng 2 Công và 1 Giáp.", "hook"),

    ("cw", 9, "cinderwell_maneater", "Cinderwell Man-Eater", "common", "weapon", "Rễ bò qua rãnh nước",
     "Talia Mercer thấy rễ dày bò qua rãnh dẫn vào luống cứu đói. Đánh bại Cinderwell Man-Eater để mở lại lối đo, rồi ghi hai điểm rễ chạm mép nước.",
     "Hai chỗ rễ chạm nước đều cách van một quãng khác nhau. Mẫu đất gần luống mặn hơn mẫu phía cửa vào.",
     "Talia đánh dấu rãnh cần gia cố. Rễ có thể góp phần chặn dòng, nhưng lịch mở van vẫn phải được xem riêng.",
     "Liềm Cắt Rễ Cinderwell", "Lưỡi liềm rèn từ thép cứu hộ, cong vừa đủ để cắt rễ mà không khoét sâu vào bờ đất. Tăng 4 Công.", "hook"),
    ("cw", 14, "cinderwell_funguy", "Ration Fungus", "common", "armor", "Nấm mọc trên bao hạt",
     "Một Ration Fungus phủ kín lối tới kho hạt. Dọn nó trước khi người tị nạn mang bao giống ra ruộng; Talia cần biết bào tử nằm ở mặt trong hay ngoài lớp bố.",
     "Bào tử dày nhất ở phần bao từng chạm nền, không ở mép buộc. Tôi niêm phong cả hai mẫu để tránh nhầm bụi kho với nấm.",
     "Kho đã thông và các bao còn kín được chuyển lên kệ cao. Sổ giống sẽ ghi điều kiện bảo quản thay vì đổ lỗi cho người vận chuyển.",
     "Áo Khoác Sợi Bào Tử", "Vải nhiều lớp trượt qua gai khô và giữ tay áo kín khi chuyển bao giống khỏi nền ẩm. Tăng 3 Giáp.", ""),
    ("cw", 88, "cinderwell_muck", "Cinderwell Muck", "common", "charm", "Vệt đen dưới cột đo",
     "Talia phát hiện một khối Cinderwell Muck che vạch nước thấp. Hạ nó để đọc thước, rồi ghi con số trước khi lau thành bể.",
     "Vạch thứ ba bị che bởi lớp nhầy mới; vạch thứ tư chỉ có rêu cũ. Tôi ghi lần đọc này kèm ánh sáng và giờ đo.",
     "Con số đã được lưu cạnh lần đo trước. Không lượt nào được xóa dù mực nước hiện tại thấp hơn dự kiến.",
     "Khóa Sổ Nước Đen", "Móc đồng giữ hai tờ đo cạnh nhau để người ghi không đánh tráo mốc cũ bằng con số mới. Tăng 2 Công và 2 Giáp.", "shockwave"),
    ("cw", 103, "cinderwell_hellhound", "Canal Hellhound", "common", "weapon", "Chó lửa bên bờ giống",
     "Một Canal Hellhound đuổi người làm ruộng khỏi bờ kênh. Hạ nó ở nền đất trống; Talia muốn đánh dấu khoảng từ dấu chân tới mép nước để đội sửa bờ có đường làm việc.",
     "Dấu chân dừng trước đoạn đất nứt, không xuyên qua bờ kênh. Tôi đánh dấu nơi nó đổi hướng và khoảng cách tới kho giống.",
     "Đội sửa bờ có thể dựng tấm chắn trước khi đưa xe hạt qua. Talia vẫn cần một lượt đo sau khi đất khô.",
     "Đoản Kiếm Kênh Khô", "Kiếm gọn có khấc cách đều, tiện ghi khoảng cách tạm thời khi không mang được thước dài xuống bờ. Tăng 5 Công.", "line_charge"),

    ("cc", 76, "cistern_grave_worm", "Grave-Water Worm", "common", "armor", "Đường hầm dưới bậc đá",
     "Một Grave-Water Worm làm sụt bậc thang dẫn xuống bể phụ. Đánh bại nó để thợ đo quay lại, rồi đánh dấu hai điểm đất rỗng trước khi lấp đường hầm.",
     "Đường hầm chạy dọc theo bờ đá chứ không cắt qua cửa van. Đất lún ở điểm thứ hai mềm hơn, có thể đã chịu nước lâu hơn.",
     "Bậc thang đã được chống tạm. Talia yêu cầu giữ lại một đoạn đất rỗng để so sánh sau đợt xả kế tiếp.",
     "Giáp Đệm Bậc Sâu", "Tấm giáp đeo hông có đệm da dày, che các cạnh đá va vào người khi đi qua đường hầm thấp. Tăng 4 Giáp.", "hook"),
    ("cc", 82, "cistern_gel_cube", "Sluice Gel Cube", "common", "weapon", "Khối trong làm mờ số khắc",
     "Một Sluice Gel Cube phủ lên thước khắc trong bể phụ. Dẹp nó trước khi nhựa trong đông lại; chụp thước từ cùng góc để Talia kiểm tra độ méo.",
     "Nhìn xuyên khối gel, các vạch gần rìa lệch hơn vạch giữa. Tôi không dùng ảnh qua lớp gel làm số đo chính thức.",
     "Thước đã được lau và chụp lại. Talia giữ cả ảnh bị méo để người khác biết vì sao một lần đọc cũ khác sổ.",
     "Mũi Đục Khối Nước", "Mũi đục răng thưa cắt được lớp gel khô khỏi thước mà không làm sâu thêm nét khắc. Tăng 5 Công.", "shockwave"),
    ("cc", 84, "cistern_queen_slime", "Cistern Slime Queen", "elite", "charm", "Màng sáng phủ cửa xả",
     "Cistern Slime Queen chặn cửa xả thứ hai, nơi đội đo cần lấy mẫu nước cuối mùa. Đánh bại nó mà không phá bánh van; Talia sẽ đối chiếu màu màng với lọ mẫu.",
     "Màng trên cửa xả có ba dải màu, còn mẫu trong lọ chỉ có hai. Ánh đèn xanh làm dải giữa sáng lên nhưng không đổi màu lọ.",
     "Cửa xả mở lại và bánh van còn nguyên. Talia không kết luận chất trong màng đã đi vào nước uống.",
     "Ấn Chốt Ba Dải", "Bùa có ba vòng màu đặt cạnh nhau, giúp đọc thang chỉ thị dưới ánh đèn sai màu. Tăng 3 Công và 2 Giáp.", "siphon"),
    ("cc", 111, "cistern_hydra", "Sluice Hydra", "elite", "armor", "Ba đầu ở buồng điều áp",
     "Sluice Hydra quấn quanh buồng điều áp và tấn công mọi người tiến tới bánh khóa. Đánh bại nó để nhóm đo dùng lại hành lang; giữ ba dấu móng riêng thay vì gọi là một đường duy nhất.",
     "Ba vết móng có độ sâu khác nhau và quay về ba hướng. Tôi đánh dấu thứ tự nhìn thấy nhưng không biết đầu nào tạo ra vết cũ nhất.",
     "Nhóm đã dựng rào quanh buồng điều áp. Bản ghi chu kỳ sẽ bắt đầu lại từ số không để không trộn dữ liệu trước và sau trận.",
     "Giáp Cân Ba Nhịp", "Bộ giáp đai chia trọng lượng hai bên hông, giúp đứng vững khi nền buồng điều áp rung. Tăng 5 Giáp.", "line_charge"),

    ("sr", 12, "saltroad_orc", "Saltroad Orc", "common", "weapon", "Dây thừng bị kéo khỏi xe",
     "Ruth Calder tìm thấy một sợi dây kéo dài từ xe hàng tới bãi muối. Đánh bại Saltroad Orc đang canh lối, rồi giữ nút dây nguyên vẹn để so với nút buộc trên caravan.",
     "Nút dây được thắt từ phía có thể với tới thùng xe. Tôi chụp hai mặt trước khi tháo, nhưng chưa biết ai đã kéo đầu còn lại.",
     "Đoàn xe có thể đi vòng qua bãi an toàn hơn. Ruth giữ nguyên nút buộc trong túi niêm phong để đội caravan tự đối chiếu.",
     "Lưỡi Rạch Dây Caravan", "Lưỡi thẳng có rãnh mở dây thừng mà không cắt sợi bên trong; người đi đường dùng nó thay cho dao dài. Tăng 6 Công.", ""),
    ("sr", 41, "saltroad_adder", "Saltroad Adder", "common", "armor", "Vết trườn dưới thẻ qua đường",
     "Một Saltroad Adder nằm dưới cọc thẻ qua đường, khiến người đưa tin không thể lấy bản sao. Dẹp nó và đo khoảng từ vệt trườn tới mép đường.",
     "Vệt trườn bị bánh xe cắt ngang ở một chỗ, nhưng đất mặn làm các mép khó phân tuổi. Tôi ghi độ dài, không ghi hướng đi.",
     "Cọc thẻ được chuyển ra nền đá. Ruth sẽ kiểm tra danh sách người nhận riêng với dấu đường, không ghép chúng thành một bằng chứng.",
     "Áo Chắn Vảy Muối", "Những miếng da chồng lớp chặn cát mặn cào vào sườn khi đi qua đường hẹp. Tăng 4 Giáp.", ""),
    ("sr", 91, "pass_gnoll", "Pass Gnoll", "common", "charm", "Hốc cờ trên sườn đèo",
     "Một Pass Gnoll dựng ổ gần hốc cờ nơi ba người sống sót từng chỉ ba hướng khác nhau. Đánh bại nó và để nguyên cọc cờ; Ruth sẽ ghi lại hướng ngọn vải trước khi mang đi.",
     "Vải cờ bị sờn ở mép tây, còn cọc nghiêng về phía đông. Gió hôm nay thổi ngược hướng đó nên tôi ghi cả thời điểm.",
     "Cọc cờ đã được dựng thẳng sau khi chụp ảnh. Lời kể của ba người vẫn được lưu thành ba hướng riêng.",
     "Nút Cờ Ba Lời Kể", "Nút đồng giữ một mảnh vải mẫu có thể đổi mà không thay vị trí cọc trên bản đồ. Tăng 3 Công và 2 Giáp.", "hook"),
    ("sr", 92, "salt_hyena", "Saltroad Hyena", "common", "weapon", "Tiếng cười bên thùng hàng",
     "Một Saltroad Hyena lục thùng hàng rỗng bên lề đường, khiến đoàn vận chuyển đổi tuyến. Dẹp nó trước buổi chợ và đánh dấu thùng nào đã bị mở từ trước.",
     "Nắp thùng có hai vết cạy chồng lên nhau. Vết thấp cũ hơn nhưng không đủ để biết ai đã mở nắp trước.",
     "Đường chợ đã thông. Ruth không tính những thùng rỗng vào danh sách hàng thất lạc cho đến khi caravan xác nhận số niêm phong.",
     "Đao Mở Thùng Niêm", "Đao bản ngắn chỉ dùng cắt sáp và dây niêm phong tại chốt có người chứng kiến. Tăng 7 Công.", "line_charge"),

    ("sl", 96, "lockhouse_mummy", "Lockhouse Mummy", "common", "weapon", "Vải bọc không có tên",
     "Một Lockhouse Mummy nằm chắn lối tới sổ cân. Đánh bại nó để Ruth kiểm tra vải quấn; tách nhãn còn dính khỏi phần vải không có chữ.",
     "Một mẩu nhãn ghi số ngăn, không ghi tên người. Các sợi chỉ xanh giống dây niêm kho nhưng có thể đến từ nhiều cuộn.",
     "Sổ cân đã được lấy ra mà không vứt bỏ lớp bọc. Ruth để phần chưa nhận dạng trong hồ sơ vật chứng.",
     "Đoản Đao Gỡ Niêm", "Lưỡi mảnh cắt được dây sáp mà không chạm vào giấy nằm sát con dấu. Tăng 7 Công.", ""),
    ("sl", 99, "lockhouse_banshee", "Salt Lockhouse Banshee", "common", "armor", "Tiếng gọi trong buồng trống",
     "Tiếng Salt Lockhouse Banshee vang từ buồng không có cửa sổ. Hạ nó để Ruth quay lại hành lang; ghi vị trí đứng của Rowan khi nghe thấy âm đầu tiên.",
     "Âm thanh đến từ bên trái ở lần đầu và từ phía sau ở lần thứ hai. Vách cong có thể làm lệch hướng, nên tôi đánh dấu hai điểm đứng.",
     "Hành lang đã yên để đội kiểm kê quay lại. Không ai thêm tên vào sổ người mất tích dựa trên tiếng gọi chưa định danh.",
     "Áo Khoác Lót Âm", "Lớp lót dày giảm tiếng kim loại va nhau khi đi qua hành lang vang âm; không che kín tai người gác. Tăng 5 Giáp.", "siphon"),
    ("sl", 97, "salt_lockhouse_lich", "Lockhouse Lich", "elite", "charm", "Người giữ ngăn không có chìa",
     "Lockhouse Lich canh ngăn hồ sơ không có chìa khóa trong sổ bàn giao. Đánh bại nó để Ruth mở cửa bằng quy trình niêm phong kép, rồi ghi số ngăn trước khi di chuyển bất cứ tập giấy nào.",
     "Bụi trên ổ khóa không có vết chìa mới. Ba tập hồ sơ đã bị kéo ra một khoảng bằng nhau, nhưng gáy của chúng quay về hai hướng.",
     "Ruth đã đánh số ảnh và niêm phong cửa lại. Ngăn hồ sơ được mở theo biên bản, không phải vì cái lich đứng trước nó.",
     "Ấn Niêm Kho Hai Lớp", "Bùa hai mặt phân biệt con dấu đã mở một lần với con dấu mới thay, giúp giữ hồ sơ bàn giao liền mạch. Tăng 4 Công và 3 Giáp.", "shockwave"),

    ("ch", 27, "choir_siren", "Bellwater Siren", "common", "weapon", "Nốt kéo dài dưới vòm",
     "Một Bellwater Siren phát âm trầm mỗi khi người lặn xuống vòm chuông. Lyra cần lối đo yên; hạ nó rồi ghi ba lượt âm, kể cả lượt không nghe thấy gì.",
     "Lượt thứ hai ngắn hơn hai lượt kia đúng một nhịp. Tôi đặt dấu hỏi thay vì nối chúng thành câu trả lời.",
     "Lyra đã lưu cả khoảng im lặng giữa các lượt. Không ai xóa mẫu ngắn chỉ vì nó không khớp với giả thuyết.",
     "Kiếm Gõ Chuông Câm", "Lưỡi kiếm có sống rỗng phát một nốt ngắn khi chạm đá, giúp người đo lấy cùng một mốc âm thanh. Tăng 8 Công.", "siphon"),
    ("ch", 28, "choir_merrow", "Choir Merrow", "common", "armor", "Vảy rời ở lối vòm",
     "Lyra Moss phát hiện vảy sáng xếp thành hàng ở lối dưới vòm. Dọn Bellwater Merrow khỏi khu vực và chụp hàng vảy trước khi dòng nước đổi hướng.",
     "Mỗi vảy phản chiếu ánh đèn theo một góc khác. Tôi không thể dùng màu ảnh làm bằng chứng chúng thuộc cùng một con vật.",
     "Lối vòm đã mở cho đội ghi âm. Lyra giữ các vảy trong những lọ riêng cho tới khi xác định được chúng rơi cùng lượt.",
     "Áo Dệt Vảy Vòm Sâu", "Áo giáp nhẹ đan từ vảy đã rơi tự nhiên, các miếng có thể thay nếu phát hiện chúng không cùng nguồn. Tăng 6 Giáp.", "line_charge"),
    ("ch", 90, "choir_will_o_wisp", "Bellwater Will-o'-Wisp", "common", "charm", "Đốm sáng ngoài bản đồ",
     "Một Bellwater Will-o'-Wisp xuất hiện ở mép bản đồ sonar rồi biến mất khi chuông rung. Hạ nó để Lyra đo lại mốc; ghi cả tọa độ trước và sau tiếng chuông.",
     "Đốm sáng xuất hiện lệch khỏi mốc sonar hai mét rồi tắt. Tôi không biết nó di chuyển hay chỉ phản chiếu bọt khí.",
     "Bản đồ được cập nhật bằng hai điểm có ghi giờ. Lyra để đường nối nét đứt vì chưa có lượt quan sát thứ ba.",
     "Móc Sáng Dưới Hồ", "Mặt dây phát ánh xanh khi ở gần chuông đã hiệu chỉnh, không tự chỉ hướng tới nguồn phát. Tăng 4 Công và 3 Giáp.", "shockwave"),
    ("ch", 112, "choir_kraken", "Deep Choir Kraken", "elite", "weapon", "Xúc tu khóa cửa chuông",
     "Deep Choir Kraken quấn các xúc tu quanh cửa phòng chuông dự phòng. Đánh bại nó mà không làm nứt khung đá; Lyra cần đo tiếng vọng sau khi hành lang thông.",
     "Vết hút bám trên mặt đá có kích thước khác nhau. Cửa không có vết nứt mới; rung động lớn nhất đến từ chân vòm phía nam.",
     "Lyra đo lại âm thanh khi nước đứng yên. Một lần đo sau giao chiến không thể thay cho mẫu lấy trước đó.",
     "Thương Mở Vòm Sâu", "Mũi thương mở đường giữa các vòng xúc tu nhưng có chặn ở chuôi để không đâm vào đá khi áp sát. Tăng 10 Công.", "hook"),

    ("gw", 26, "greenwake_dryad", "Rootbound Dryad", "common", "armor", "Rễ ôm quanh lối giếng",
     "The First Warden thấy rễ mới ôm lấy lối xuống giếng, buộc người hái phải đi vòng qua ruộng giống. Đánh bại Rootbound Dryad rồi ghi phần rễ sống nằm ngoài hàng rào.",
     "Rễ cong về phía nước nhưng hai nhánh lại mọc ra xa giếng. Tôi đánh dấu hướng mọc, chưa ghi rằng chúng tìm kiếm nước.",
     "Lối đi đã được dọn mà không chặt phần rễ sống ngoài rào. The First Warden sẽ xem cây thay đổi thế nào trong mùa tới.",
     "Áo Rễ Dệt Greenwake", "Lớp áo có sợi gai thay được, không bám đất ẩm khi quỳ xuống kiểm tra luống. Tăng 7 Giáp.", "siphon"),
    ("gw", 102, "greenwake_satyr", "Grove Satyr", "common", "weapon", "Dấu móng cạnh hàng cây",
     "Một Grove Satyr chạy giữa hai hàng cây và làm hỏng cọc đánh dấu mùa. Dẹp mối nguy để người làm vườn quay lại; giữ nguyên một cọc nghiêng cho tới khi chụp ảnh.",
     "Cọc gãy theo chiều gió chứ không theo đường chạy nhìn thấy. Tôi chụp nó trước khi dựng lại.",
     "Hàng cây được đánh dấu lại bằng dây màu khác. Owen sẽ so sản lượng thay vì cho rằng lần gãy cọc làm lệch cả vụ.",
     "Đao Tỉa Hàng Cây", "Lưỡi cong nhỏ dùng cắt dây leo khỏi cọc mà không làm tổn thương rễ đang mọc. Tăng 9 Công.", "line_charge"),
    ("gw", 114, "greenwake_treant", "Greenwake Treant", "common", "charm", "Gốc cây chắn kho hạt",
     "Một Greenwake Treant đứng chắn cửa kho giống sau cơn mưa. The First Warden yêu cầu Rowan hạ nó ở nền đất trống và ghi phần gỗ đã mục trước khi thợ chuyển kho.",
     "Lõi gỗ mục có vòng tuổi rộng hơn phía ngoài. Tôi lấy mẫu từ mảnh đã rơi, không khoan vào thân còn sống.",
     "Cửa kho đã thông cho đội chuyển hạt. Bản ghi không gọi nó là cây canh giữ; không có ai xác nhận ý định của nó.",
     "Khuyên Cành Không Gãy", "Mề đay từ nhánh rơi tự nhiên, có lõi gỗ ép giữ dây đeo khỏi đứt khi mang túi hạt nặng. Tăng 5 Công và 4 Giáp.", "shockwave"),
    ("gw", 107, "greenwake_manticore", "Crownroot Manticore", "elite", "weapon", "Bóng gai phía trên hàng rễ",
     "Crownroot Manticore săn người hái ở lối cao trên Greenwake. Đánh bại nó trong khoảng trống và báo số gai gãy cho Owen, không gom các mảnh từ nhiều ngày thành một mẫu.",
     "Ba gai gãy có lớp đất khô, một gai còn ẩm. Tôi tách chúng theo độ ẩm thay vì xếp theo màu.",
     "Người hái có thể đi tuyến thấp trong lúc Owen đánh dấu đường cao. Mối nguy đã được dẹp; dấu gai cũ vẫn cần được nhận dạng.",
     "Mũi Giáo Tán Rễ", "Mũi giáo có khe thoát gai mắc, giúp người gác lối cao không phải giật mạnh làm rách cán. Tăng 11 Công.", "hook"),

    ("ow", 31, "outerwake_mist_dragon", "Outer-Wake Mist Dragon", "common", "weapon", "Cánh qua sương đo",
     "Một Mist Dragon bay xuyên qua ba mốc đo khiến Evelyn Hart không biết dụng cụ rung vì gió hay vì cánh. Dẹp nó khỏi đường lấy mẫu; Rowan phải ghi lại lượt đo bị gián đoạn.",
     "Kim rung đúng lúc bóng cánh che bầu trời. Tôi giữ lượt này trong bảng và đánh dấu nó là bị nhiễu, không xóa khỏi chuỗi.",
     "Evelyn sẽ đo lại khi vùng trời trống. Mẫu cũ vẫn có ích để mô tả điều kiện sai số.",
     "Kiếm Mù Sương Viền Lam", "Lưỡi kiếm bắt ánh xanh dưới trời mù, có rãnh trống để bụi khoáng không che vạch khắc. Tăng 10 Công.", "line_charge"),
    ("ow", 46, "outerwake_fire_elemental", "Cinder-Star Elemental", "common", "armor", "Lõi nóng bên mẫu khoáng",
     "Cinder-Star Elemental làm nóng hộp đựng mẫu ngoài vòm. Hạ nó trước khi Evelyn chạm vào hộp, rồi để nguyên lớp khoáng bám đáy cho nhóm đo nhiệt.",
     "Đáy hộp nóng hơn nắp dù đặt trên cùng tấm kim loại. Tôi ghi thời gian nguội thay vì gọi lớp bám là nhiên liệu.",
     "Mẫu đã được chuyển bằng kẹp cách nhiệt. Evelyn sẽ so nhiệt độ với hộp dự phòng còn niêm kín.",
     "Áo Giáp Chịu Nhiệt Ngoài Vòm", "Các lớp gốm mỏng chia nhiệt sang hai bên thân thay vì giữ nó sát hộp đo. Tăng 8 Giáp.", "shockwave"),
    ("ow", 49, "outerwake_air_elemental", "Star-Gale Elemental", "common", "charm", "Vòng xoáy quanh bảng tín hiệu",
     "Star-Gale Elemental xoáy quanh bảng tín hiệu và làm lệch dải băng xác định hướng gió. Dẹp nó, ghi vị trí từng nút dây; không chỉnh lại trước khi Evelyn chụp ảnh.",
     "Dải băng xoay cùng chiều ở hai độ cao khác nhau. Tôi ghi số vòng mỗi phút và giữ dây nguyên trạng.",
     "Bảng tín hiệu được cố định lại sau khi chụp. Hướng gió đã thay đổi, còn nguồn gây nhiễu chưa được xác định.",
     "Vòng Cân Hướng Outer-Wake", "Vòng đồng giữ các dải phương hướng riêng biệt để một luồng gió xoáy không kéo cả bảng lệch theo. Tăng 5 Công và 4 Giáp.", "hook"),
    ("ow", 108, "outerwake_chimera", "Archive Chimera", "elite", "weapon", "Ba bóng trên nền bụi",
     "Archive Chimera xuất hiện gần ba mẫu vật đặt cách nhau. Hạ nó mà không dịch chuyển nhãn; Evelyn cần biết bóng thứ hai có che mẫu cùng lúc với tiếng gió hay không.",
     "Ba bóng không chồng nhau ở cùng thời điểm. Tôi đánh dấu vị trí đèn, không kết luận rằng sinh vật có ba thân.",
     "Các mẫu vẫn còn đúng nhãn. Evelyn sẽ thử lại bằng nguồn sáng thấp hơn để kiểm tra hình phản chiếu.",
     "Đao Ba Mép Lưu Trữ", "Lưỡi đao ba cạnh thay được từng mép sau khi lấy mẫu khoáng, tránh lẫn các vết mẻ khác nhau. Tăng 12 Công.", "siphon"),

    ("lo", 33, "crownfall_black_dragon", "Crownfall Black Dragon", "common", "armor", "Vảy ở chân Cycle Heart",
     "Alden Vale tìm thấy vảy đen ở chân Cycle Heart nhưng không thể xác nhận nó thuộc về ai. Hạ Black Dragon để Rowan kiểm tra khu vực; ghi vảy nằm trên hay dưới lớp bụi đỏ.",
     "Vảy nằm dưới bụi đỏ ở phía bắc và trên bụi ở phía nam. Hai thời điểm rơi không giống nhau.",
     "Alden giữ hai mẫu trong hai túi khác nhau. Không mẫu nào được ghi tên Ma Vương khi chưa có đối chiếu.",
     "Áo Giáp Vảy Hai Thời", "Hai lớp vảy ép theo hướng ngược nhau, bảo vệ khi lướt qua đá vụn nhưng không mang huy hiệu của vòng trước. Tăng 8 Giáp.", "line_charge"),
    ("lo", 39, "crownfall_devil", "Last-Oath Devil", "common", "weapon", "Tiếng gọi không có người trả lời",
     "Last-Oath Devil gọi tên những người trong danh sách cuối, khiến đội canh mất liên lạc vài phút. Đánh bại nó và ghi câu nào được nghe rõ nhất trước khi đối chiếu bản danh sách.",
     "Tiếng gọi thiếu họ và lặp sai thứ tự hai cái tên. Tôi không cho rằng nó đã đọc từ cuốn danh sách thật.",
     "Đội canh đã nối lại tín hiệu bằng đèn tay. Alden yêu cầu ghi nguyên câu nghe được, không viết câu mà người nghe mong đợi.",
     "Kiếm Chặn Lời Thề", "Chuôi kiếm có chốt khóa giữ chắc khi người cầm phải đổi giữa tư thế gác và tư thế chiến đấu. Tăng 12 Công.", "hook"),
    ("lo", 118, "last_oath_owlbear", "Crownfall Owlbear", "common", "charm", "Dấu vuốt gần ngọn đèn trống",
     "Một Crownfall Owlbear đi quanh những ngọn đèn chờ người trở về. Đánh bại nó ở bãi đá để ngọn lửa không tắt; ghi ngọn nào còn dầu trước khi thắp lại.",
     "Ngọn đèn phía đông còn dầu nhưng bấc đã tắt. Tôi đánh dấu mức dầu riêng với lý do lửa tắt.",
     "Alden thắp lại đèn sau khi Rowan dọn bãi đá. Ngọn lửa không được ghi là lời hứa rằng ai đó chắc chắn sẽ trở về.",
     "Mề Đay Đèn Chưa Tắt", "Tấm đồng giữ một mẩu bấc dự phòng trong khoang khô, đủ để nhóm lửa khi gió làm tắt đèn chờ. Tăng 6 Công và 5 Giáp.", "shockwave"),
    ("lo", 109, "cycle_sphinx", "Cycle Sphinx", "elite", "weapon", "Câu hỏi khắc trên nền",
     "Cycle Sphinx chặn lối tới bàn giao cuối cùng và hỏi Rowan một câu chỉ có thể trả lời bằng dữ liệu. Hạ nó để Alden mở đường; ghi nguyên câu hỏi, không ghi đáp án của người khác.",
     "Câu hỏi lặp lại sau tiếng va chạm nhưng thiếu một từ ở lần thứ hai. Tôi chép cả hai phiên âm cạnh nhau.",
     "Alden sẽ giữ nguyên câu hỏi trong biên bản bàn giao. Chiến thắng không biến phần còn thiếu thành một câu trả lời chắc chắn.",
     "Kiếm Bàn Giao Không Khóa", "Lưỡi kiếm có chuôi mở, biểu trưng cho hồ sơ còn được phép sửa khi chứng cứ mới xuất hiện. Tăng 14 Công.", "siphon"),
]

def read_catalog(name):
    path = CONTENT / name
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("entries"), list):
        raise ValueError(f"{name} has no entries list")
    return path, data

def write_catalog(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def make_equipment(row, region):
    level = region["level"]
    elite = row[4] == "elite"
    slot = row[5]
    if slot == "weapon":
        attack = level + (2 if elite else 0)
        guard = 0
    elif slot == "armor":
        attack = 0
        guard = max(1, (level * 3 + 2) // 4) + (1 if elite else 0)
    else:
        attack = max(1, level // 2) + (1 if elite else 0)
        guard = max(1, level // 3)
    return {
        "id": f"fieldgear_{region['code']}_{row[2]}",
        "name": row[10],
        "description": row[11],
        "category": "equipment",
        "equipmentSlot": slot,
        "maxStack": 1,
        "attackBonus": attack,
        "guardBonus": guard,
        "healAmount": 0,
        "sellValue": 32 + region["level"] * 8
    }

def main():
    if not ARCHIVE.is_file():
        raise SystemExit(f"Missing asset archive: {ARCHIVE}")
    if len(SPECIES) != 42:
        raise SystemExit(f"Expected 42 authored entries, found {len(SPECIES)}")

    names = {
        "monster_catalog.json": [], "encounter_catalog.json": [],
        "prologue_quests.json": [], "item_catalog.json": [],
        "dialogue_catalog.json": [], "codex_catalog.json": []
    }
    paths = {}
    catalogs = {}
    for name in names:
        paths[name], catalogs[name] = read_catalog(name)

    expected_ids = []
    for region_code, tile, slug, *_ in SPECIES:
        region = REGIONS[region_code] | {"code": region_code}
        expected_ids.extend([
            f"tiny_{region_code}_{slug}", f"field_{region_code}_{slug}",
            f"fieldgear_{region_code}_{slug}", f"side_field_{region_code}_{slug}",
            f"field_{region_code}_{slug}_site", f"rowan_field_{slug}_record"
        ])
    existing_ids = set()
    for name, data in catalogs.items():
        existing_ids.update(entry.get("id", "") for entry in data["entries"])
    present = [item_id for item_id in expected_ids if item_id in existing_ids]
    if present:
        if len(present) == len(expected_ids) and all((ART / f"tiny_{row[1]:04d}.png").exists() for row in SPECIES):
            print("Tiny Creatures fieldbook is already imported; no changes made.")
            return
        raise SystemExit("Partial Tiny Creatures import detected; inspect catalogs before retrying.")

    archive_info = []
    with zipfile.ZipFile(ARCHIVE) as source:
        license_text = source.read("tiny-creatures/License.txt").decode("utf-8")
        (ROOT / "Docs/Licenses/tiny-creatures-cc0.txt").write_text(license_text, encoding="utf-8")
        for row in SPECIES:
            tile = row[1]
            resource_name = f"tiny_{tile:04d}"
            destination = ART / f"{resource_name}.png"
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read(f"tiny-creatures/Tiles/tile_{tile:04d}.png"))
            region = REGIONS[row[0]]
            archive_info.append((tile, resource_name, f"tiny_{row[0]}_{row[2]}", row[3], row[4],
                                 region["location"], row[5]))

    quest_by_region = {}
    for row in SPECIES:
        code, tile, slug, name, rank, slot, title, brief, note_one, note_two, item_name, item_desc, move = row
        region = REGIONS[code] | {"code": code}
        monster_id = f"tiny_{code}_{slug}"
        quest_id = f"side_field_{code}_{slug}"
        item_id = f"fieldgear_{code}_{slug}"
        encounter_id = f"field_{code}_{slug}_site"
        dialogue_id = f"rowan_field_{slug}_record"
        previous_quest = quest_by_region.get(code, region["root"])
        quest_by_region[code] = quest_id
        level = region["level"]
        elite = rank == "elite"
        special_move = move
        special_reach = 5.0 if move in {"shockwave", "siphon", "hook", "line_charge"} else 0
        size = 2.75 if elite else (2.55 if level < 8 else 2.65)
        max_health = 32 + level * 7 + (42 if elite else 0)
        damage = 4 + level + (4 if elite else 0)

        names["monster_catalog.json"].append({
            "id": monster_id, "displayName": name, "rank": rank,
            "maxHealth": max_health, "attackDamage": damage, "attackReach": 1.0,
            "approachSpeed": round(0.88 + min(level, 10) * 0.028 + (0.06 if elite else 0), 3),
            "lungeDistance": 1.65 if not elite else 1.9, "lungeSeconds": 0.34,
            "lungeStopDistance": 0.68, "openingDelay": round(1.3 - min(level, 8) * 0.035, 3),
            "closingSeconds": 1.12 if not elite else 1.2,
            "telegraphSeconds": 0.82 if not elite else 1.0,
            "recoverySeconds": 0.95 if not elite else 1.08,
            "counterBonusDamage": 12 if not elite else 20, "hitCooldown": round(0.7 - min(level, 5) * 0.025, 3),
            "spriteResource": f"tiny_{tile:04d}", "lungeSpriteResource": "",
            "spriteScale": size, "spritePixelsPerUnit": 16,
            "specialMoveId": special_move, "specialMoveReach": special_reach
        })

        position = region["positions"][sum(1 for item in SPECIES[:SPECIES.index(row)] if item[0] == code)]
        names["encounter_catalog.json"].append({
            "id": encounter_id, "monsterId": monster_id, "locationId": region["location"],
            "positionX": position[0], "positionY": position[1],
            "requiredQuestId": quest_id, "blockedQuestId": "", "blockedDialogueId": "",
            "contributesToQuest": True, "defeatObjectiveTargetId": monster_id,
            "defeatDialogueId": dialogue_id, "downDialogueId": "rowan_field_retreat",
            "reward": {"gold": 3 + level * 2, "items": []}
        })

        names["item_catalog.json"].append(make_equipment(row, region))
        objective_id = f"defeat_{slug}"
        objective_description = f"Đánh bại {name} và hoàn tất ghi nhận ngoài hiện trường."
        names["prologue_quests.json"].append({
            "id": quest_id, "arcId": region["arc"], "stage": -1,
            "type": "side", "locationId": region["location"], "giverId": region["giver"],
            "title": title, "objective": brief, "prerequisiteIds": [previous_quest],
            "objectives": [{"id": objective_id, "kind": "defeat", "targetId": monster_id,
                            "requiredCount": 1, "description": objective_description}],
            "reward": {"gold": 10 + level * 3, "items": [{"itemId": item_id, "quantity": 1}]}
        })
        names["dialogue_catalog.json"].append({
            "id": dialogue_id, "speakerName": region["author"].upper(),
            "lines": [note_one, note_two]
        })

    names["dialogue_catalog.json"].append({
        "id": "rowan_field_retreat", "speakerName": "ROWAN HALE",
        "lines": [
            "Tôi cần lùi lại trước khi cố tiến thêm. Không có ghi chép nào đáng để đổi lấy một vết thương có thể tránh được.",
            "Vị trí đã được đánh dấu, và tôi còn có thể quay lại khi hồi sức. Trận đánh dừng ở đây; dấu vết vẫn chờ được kiểm tra."
        ]
    })

    for code, region in REGIONS.items():
        entries = [row for row in SPECIES if row[0] == code]
        if not entries:
            continue
        final_quest = quest_by_region[code]
        names["codex_catalog.json"].append({
            "id": f"field_codex_{code}",
            "title": region["codex_title"],
            "category": "Field Bestiary",
            "writtenBy": region["author"],
            "unlockQuestId": final_quest,
            "body": region["codex"]
        })

    # Validate the complete append set before writing any catalog.
    for name, append_entries in names.items():
        ids = [entry["id"] for entry in catalogs[name]["entries"]] + [entry["id"] for entry in append_entries]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"Duplicate ID found while generating {name}")
    if len(archive_info) != 42:
        raise SystemExit("The source-to-species map does not cover all imported sprites.")

    mapping = ROOT / "Docs/AssetArchives/tiny-creatures-species-map.tsv"
    mapping.write_text(
        "source_tile\tresource_name\tmonster_id\tdisplay_name\trank\tlocation_id\tequipment_slot\n" +
        "".join("\t".join(map(str, entry)) + "\n" for entry in archive_info),
        encoding="utf-8"
    )

    for name, append_entries in names.items():
        catalogs[name]["entries"].extend(append_entries)
        write_catalog(paths[name], catalogs[name])
    print("Imported 42 CC0 creature sprites; authored 42 hunt quests, 42 equipment rewards, 42 encounter placements, 42 victory records, one retreat exchange, and 11 fieldbook entries.")

if __name__ == "__main__":
    main()
