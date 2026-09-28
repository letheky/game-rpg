#!/usr/bin/env python3
"""Install Pella Quinn's 36-quest Greenwake root-wall route."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "Assets/Resources/Content"


def read(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def write(name, value):
    (CONTENT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert(entries, additions):
    indexes = {entry["id"]: i for i, entry in enumerate(entries)}
    for entry in additions:
        if entry["id"] in indexes:
            entries[indexes[entry["id"]]] = entry
        else:
            indexes[entry["id"]] = len(entries)
            entries.append(entry)


# key, title, location, giver, kind, target, objective, speaker, lines,
# codex title, codex body, marker visual, marker position
common = [
    ("open", "Vết phồng trong bức tường rễ", "greenwake_refuge", "pella_quinn", "talk", "pella_quinn",
     "Gặp Pella Quinn ở Greenwake. Bức tường đá ôm vườn rễ đã phồng lên sau mùa mưa; cô muốn biết phần nào dịch chuyển trước khi thay một viên đá.", "PELLA QUINN",
     ["Tôi từng đóng dấu 'đá xấu' lên sổ của cha. Bức tường đổ, còn chữ ấy sống lâu hơn cả lần sửa.", "Mara nói rễ cây có thể đổi hướng qua từng mùa. Tôi muốn đo lại trước khi đổ lỗi cho đá hoặc cho người xây."],
     "Pella Quinn trở lại Greenwake", "Pella Quinn từng phụ cha dựng các bờ đá quanh vườn rễ. Sau một trận mưa, đoạn tường phía đông nứt ra và cô ghi ngắn gọn rằng đá đã hỏng. Pella rời Greenwake trước khi có đợt khảo sát tiếp theo; nhiều năm sau, Mara tìm được rễ cây đã trườn qua mặt trong của móng. Pella không biết rễ có làm lệch bức tường hay chỉ đi theo khe có sẵn. Cô trở lại để sửa hồ sơ cùng cấu trúc, nhưng sẽ không thay một phán đoán cũ bằng một phán đoán mới khi chưa có phép đo lặp lại.", "pella_quinn", (4.7, 1.5)),
    ("sill", "Chân móng cách rễ một gang", "greenwake_refuge", "pella_quinn", "inspect", "pella_wall_sill",
     "Khảo sát mặt móng phía đông. Ghi nơi đá chạm đất, nơi có khoảng hở và độ sâu của vệt lún mà không nối các điểm thành một nguyên nhân duy nhất.", "ROWAN HALE",
     ["Mép ngoài còn phẳng, nhưng phía trong có một khoảng hở rộng bằng hai đốt tay.", "Tôi ghi cả hai mặt. Một đường nứt chưa cho biết lực bắt đầu từ phía nào."],
     "Móng đông: hai mặt khác nhau", "Bản khảo sát ghi mặt ngoài của bức tường còn phẳng trong khi lớp đất phía trong đã lún. Một khoảng hở dưới viên đá thứ ba thay đổi theo vị trí, nhưng người đo cũ không đánh dấu điểm đặt thước. Rowan đo từ cùng một mốc đá, giữ khoảng hở lớn nhất và nhỏ nhất cạnh nhau. Các số này mô tả một mặt móng vào ngày khảo sát; chúng không xác định nước, rễ hay sức nén của đất là nguyên nhân chính. Nếu lần đo kế tiếp dùng mốc khác, hai dãy số sẽ không thể so sánh.", "stone_rill", (9.1, -2.7)),
    ("mortar", "Vữa đã bật khỏi khe cũ", "greenwake_refuge", "pella_quinn", "inspect", "pella_mortar_record",
     "Đọc vệt vữa trên viên đá bật khỏi hàng. Pella muốn giữ lại chiều rơi và mặt gãy để biết viên đá có bị kéo hay bị đẩy.", "ROWAN HALE",
     ["Bột vữa nằm ở mặt trong, nhưng mưa cũng cuốn đất qua khe này.", "Tôi sẽ ghi hướng rơi và độ ẩm. Dấu bột riêng lẻ không chỉ ra ai hay thứ gì đã làm đá dịch chuyển."],
     "Mặt gãy không phải lời khai", "Viên đá được tìm thấy úp mặt vữa xuống lớp đất ẩm. Một phần bột nằm phía trong tường, song dòng nước mưa có thể mang nó qua khe sau khi viên đá rời vị trí. Không còn ảnh chụp hiện trường trước khi dọn vườn, nên Pella không thể khôi phục chính xác hướng rơi. Rowan lưu mặt gãy, chiều của viên đá và tình trạng đất lúc tìm thấy. Ghi chú không gọi đây là dấu tay, dấu rễ hay bằng chứng phá hoại; cả ba giả thuyết đều cần dữ liệu khác.", "document", (5.5, -4.0)),
    ("mara", "Mara nhớ lần vỡ tường", "greenwake_refuge", "mara_bell", "talk", "mara_bell",
     "Hỏi Mara Bell về các rễ Glassplum gần móng. Cô từng ghi lịch tưới quanh bức tường nhưng không thể xác nhận rễ nào đã chạm đá.", "MARA BELL",
     ["Tôi đã ghi ngày tưới, không ghi đường đi của từng rễ. Từ sổ ấy không thể nhìn ngược một mùa đã qua.", "Pella không cần tôi tha thứ cho một bản ghi cũ. Cô cần một cách để người sau sửa được bản ghi mới."],
     "Sổ tưới và khoảng trống dưới đá", "Mara giữ lịch tưới qua nhiều vụ, nhưng các dấu chỉ ngày và thời lượng. Bản đồ rễ được vẽ sau khi tường nứt, nên không cho biết cây đã phát triển theo khe nào trước đó. Mara nói có thể kiểm tra những rễ còn sống trong luống hiện tại, song không thể dùng chúng làm đại diện cho cây của mùa cũ. Cô cũng nhắc Rowan rằng một lịch tưới đúng không đồng nghĩa phép đo tường đúng. Hai sổ cần được đặt cạnh nhau với phạm vi riêng, thay vì để một loại dữ liệu lấp khoảng trống của loại kia.", "", (0, 0)),
    ("first_bed", "Một lứa Glassplum nữa", "greenwake_refuge", "pella_quinn", "grow", "glassplum",
     "Trồng và thu hoạch Glassplum tại Greenwake. Pella cần một mẫu rễ sống để so với khoảng hở, không phải một vụ mùa dùng để suy ra mọi khu vườn.", "PELLA QUINN",
     ["Tôi sẽ đánh dấu vị trí trong luống trước khi gieo. Cùng một giống cây vẫn có thể gặp đất và nước khác nhau.", "Lấy một mẫu có nhãn, nhưng để phần rễ còn lại tiếp tục phát triển."],
     "Một lứa cây trong một luống", "Lứa Glassplum này được trồng ở mép luống phía đông, cách bức tường một sải tay. Lịch thu hoạch và vị trí gieo được ghi cạnh nhau để lần sau có thể lặp phép đo. Cây sống qua một chu kỳ hoạt động trong điều kiện tưới hiện tại; kết quả không cho biết rễ đã đi tới độ sâu nào dưới móng. Mara giữ nguyên phần rễ còn lại trong đất để không biến một mẫu nhỏ thành toàn bộ cây. Pella dùng một nhánh đã cắt tỉa làm thước so sánh mềm, không dùng nó để đẩy đá trở lại vị trí.", "", (0, 0)),
    ("ring", "Vòng tăng trưởng bên mép đá", "greenwake_refuge", "pella_quinn", "inspect", "pella_growth_ring",
     "So kích thước hai vòng tăng trưởng trên nhánh đã cắt với bề rộng khe đá. Ghi chênh lệch và hướng nhánh, không suy ra tốc độ nứt của tường.", "ROWAN HALE",
     ["Nhánh gần tường dày hơn nhánh ở đầu luống, nhưng chúng không được cắt cùng ngày.", "Ta có thể lưu phép so này làm câu hỏi cho vụ sau, không phải kết luận về lực đẩy."],
     "Hai vòng không tạo thành niên đại", "Hai vòng tăng trưởng cho thấy nhánh gần tường rộng hơn nhánh phía đầu luống. Thời điểm cắt không trùng nhau; khoảng cách giữa các vòng cũng bị một vết cọ làm mờ. Pella muốn dùng số đo để khoanh khu vực cần xem lại, nhưng không đủ dữ kiện để gọi một vòng là năm tường nứt. Rowan đặt thước trên cả hai nhánh cùng một chiều và ghi vùng sai số bằng nét đôi. Năm sau, người làm vườn có thể lặp lại việc đo ở đúng hai vị trí hoặc chọn mẫu mới nếu cây đã đổi hướng.", "document", (1.7, 2.2)),
    ("mite", "Tiếng gõ dưới luống", "greenwake_refuge", "pella_quinn", "defeat", "greenwake_rootwall_mite",
     "Đánh bại Vine Stalker đang chui ra từ một hốc dưới bức tường. Pella muốn mở lại lối khảo sát, không xem con quái là lời giải cho vết nứt.", "PELLA QUINN",
     ["Nó trú trong một khe đã có sẵn; ta chưa biết khe xuất hiện trước hay sau khi con vật đến.", "Dọn đường để kiểm tra mặt trong. Đừng ghi 'thủ phạm' vào sổ chỉ vì một trận đánh."],
     "Vine Stalker trong khe tường", "Vine Stalker xuất hiện từ một hốc dưới luống, nơi đất đã rời khỏi chân móng. Rowan dọn con đường hẹp để Pella có thể quan sát lớp đá bên trong. Con quái có thể đã mở rộng khe, tìm tới một khe cũ hoặc chỉ trú ở đó sau khi đất trôi; không có dấu vết nào phân biệt được ba khả năng. Pella thu một bó sợi nâu mắc trên cạnh đá làm vật liệu thử. Cô yêu cầu không dùng bó sợi ấy để kết luận loài này gây ra mọi vết nứt ở Greenwake.", "", (0, 0)),
    ("fiber", "Sợi nâu mắc vào mặt đá", "greenwake_refuge", "pella_quinn", "inspect", "pella_mite_residue",
     "Khảo sát sợi nâu còn lại sau trận. Pella phân biệt vật liệu rơi ra từ ổ với vật liệu bị kéo dọc theo khe.", "ROWAN HALE",
     ["Sợi bị tưa ở đầu chạm đá. Ta chưa biết nó mắc lại trước hay sau lúc con vật chạy qua.", "Tôi đóng gói một đoạn sạch làm mẫu keo, còn mảnh đất và hướng kéo sẽ nằm trong bản ghi riêng."],
     "Mẫu sợi, không phải dấu thủ phạm", "Một đoạn sợi thực vật nâu còn mắc trên cạnh đá sau khi Vine Stalker bị đánh bại. Đầu sợi tưa, nhưng đất quanh đó đã bị khuấy lên trong trận. Rowan giữ một phần sạch cho phép thử vật liệu và để phần bẩn trong khay tách biệt. Hai mẫu có thể giúp người thợ kiểm tra độ bám của lớp keo; chúng không xác định thời điểm khe mở hoặc sinh vật nào đã đi qua. Pella ghi cả việc hốc vừa bị xáo trộn để người xem sau biết giới hạn của mẫu.", "sealed_case", (-7.0, -4.6)),
    ("talia", "Talia đọc màu đá", "cinderwell_basin", "pella_quinn", "talk", "talia_mercer",
     "Hỏi Talia Mercer về lớp màu trên viên đá. Cô có thể so một mẫu với nước lấy tại chỗ, không chứng nhận cả kênh hay cả mùa.", "TALIA MERCER",
     ["Màu nâu có thể là bùn, oxit hoặc cả hai. Tôi chỉ biết nguồn mẫu và ngày lấy.", "Nếu Pella muốn thử keo, dùng cùng viên đá cho mẫu đối chứng rồi giữ lại lớp chưa xử lý."],
     "Talia đặt giới hạn cho mẫu đá", "Talia không gọi vệt nâu là gỉ chỉ bằng mắt. Bùn, oxit sắt hoặc nhiều lớp vật liệu có thể tạo màu tương tự; cần tách một mẫu nhỏ và ghi cách làm sạch. Cô đưa Pella một viên đối chứng đã đánh dấu nhưng không lấy mẫu từ giữa dòng nước đang dùng. Phép thử giúp thợ rèn biết lớp keo bám lên đá đã rửa như thế nào. Nó không đo chất lượng nước, nồng độ khoáng trong toàn basin hay độ bền của bức tường qua mùa mưa.", "", (0, 0)),
    ("cinderstone", "Bậc đá từ đập cũ", "cinderwell_basin", "pella_quinn", "inspect", "pella_cinderwell_stone",
     "Đọc đường cắt trên viên đá lưu ở Cinderwell. Đá này từng được dùng làm bậc kênh, nhưng kích thước không biến nó thành vật thay thế cho mọi móng.", "ROWAN HALE",
     ["Vết đục đi cùng thớ đá, còn vết sẫm bám ở cạnh thấp.", "Chúng ta ghi cách viên này được đặt ở kênh cũ; không mang kích thước ấy áp vào tường Greenwake."],
     "Một bậc đá từ nơi khác", "Viên đá lưu tại Cinderwell được cắt thành bậc thoát nước, không phải khối chịu lực của một tường vườn. Vết đục chạy cùng thớ và cạnh dưới sẫm màu sau nhiều lần ướt. Pella dùng nó để xem thợ cũ xử lý mép đá, chứ không sao chép kích thước. Lớp đá, hướng nước và tải trọng của hai công trình khác nhau. Ghi chú nhắc người đọc hỏi viên đá từng làm việc ở đâu trước khi đưa nó vào một bản vẽ mới.", "document", (1.1, 2.7)),
    ("moss", "Rêu mọc ở chân cống", "cinder_cistern", "pella_quinn", "grow", "brineglass_moss",
     "Trồng và thu hoạch Brineglass Moss ở Lower Cistern. Rêu sẽ làm vật liệu thử; phép thử không đại diện cho toàn bộ cống hoặc nguồn nước.", "PELLA QUINN",
     ["Rêu này lớn ở nơi có khe ẩm. Nó không cho biết đá Greenwake chứa cùng loại muối.", "Tôi sẽ ghi riêng luống trồng và viên mẫu nhận keo để không nhập nhằng hai nơi."],
     "Rêu thử trong một luống", "Brineglass Moss được trồng trong plot của Lower Cistern, nơi có bóng râm và dòng nước chậm. Rowan thu hoạch một lượng nhỏ sau chu kỳ trồng; Pella dùng phần đó làm phụ gia cho mẻ keo. Vật liệu cho phép cô quan sát cách hỗn hợp bám trên viên đối chứng. Nó không chứng minh loại rêu này mọc tự nhiên trên tường Greenwake, cũng không chứng nhận nước cống sạch. Nhãn mẫu giữ rõ nguồn trồng để không biến thử nghiệm chế tạo thành bản đồ sinh thái.", "", (0, 0)),
    ("survey", "Sơ đồ áp lực bị lật mặt", "cinder_cistern", "pella_quinn", "inspect", "pella_cistern_survey",
     "Đọc mặt sau tờ sơ đồ kênh Cinderwell. Phần bị úp ghi giờ mở van nhưng không có lượng nước hay người xác nhận.", "ROWAN HALE",
     ["Mặt trước chỉ có mũi tên. Ở mặt sau còn một khoảng giờ với hai nét sửa.", "Tờ này giúp ta biết van từng được vận hành trong ca nào, chứ không cho biết áp lực đã tới Greenwake."],
     "Sơ đồ có mặt sau", "Tờ sơ đồ từng được dùng để chỉ hướng nước trong Lower Cistern. Mặt sau ghi hai khoảng giờ và một lần gạch sửa; đơn vị đo không còn ở đầu trang. Pella nhận ra nét đục trên lề giống dấu của xưởng nhà cô, nhưng không thể xác định ai đã ghi nếu thiếu sổ đối chiếu. Ghi chú hữu ích cho việc lần theo lịch vận hành địa phương, không nối áp lực Cinderwell với bức tường ở Greenwake. Rowan chụp lại cả hai mặt trong sổ và ghi thứ tự mà họ tìm thấy tờ giấy.", "sealed_case", (-2.4, -2.5)),
    ("fish", "Mẫu cá ở hồ không phải mẫu nước", "outerwake_archive", "pella_quinn", "fish", "farwake_carp",
     "Câu một Farwake Carp tại Celestial Pool để thử dầu bản lề trên mẫu kim loại. Ghi riêng nơi bắt cá và nơi thử vật liệu.", "ROWAN HALE",
     ["Một con cá có thể cho ta lượng dầu đủ bôi bản lề thử. Nó không đại diện cho mọi mùa trong hồ.", "Tôi sẽ ghi ngày câu và chuyển phần dầu sang lọ riêng trước khi mang về Greenwake."],
     "Farwake Carp và lọ dầu thử", "Một Farwake Carp được câu tại Celestial Pool vào ngày Rowan mang dụng cụ tới. Cá cung cấp một ít dầu để Pella bôi lên bản lề mẫu; phép thử không dùng trực tiếp trên tường và không thay khảo sát chất lượng nước. Chỉ một lần câu không thể ước tính số cá, mùa sinh sản hay lượng dầu mà cộng đồng có thể lấy bền vững. Nhãn lọ ghi rõ hồ, ngày và mục đích thử để không nhầm nó với vật liệu được phê duyệt cho toàn vùng.", "", (0, 0)),
    ("evelyn", "Evelyn đối chiếu nhiệt", "outerwake_archive", "pella_quinn", "talk", "evelyn_hart",
     "Nhờ Dr. Evelyn Hart đọc hai mốc nhiệt của đá đối chứng. Cô muốn biết chúng được đo cùng thời điểm hay chỉ cùng một thiết bị.", "DR. EVELYN HART",
     ["Cùng nhiệt kế không có nghĩa là cùng điều kiện. Một viên nằm dưới mái, viên kia phơi nắng.", "Ta có thể ghi độ thay đổi trong ngày nếu giữ vị trí, giờ và bóng râm ở cạnh số đo."],
     "Evelyn yêu cầu đủ điều kiện đo", "Evelyn phát hiện hai số nhiệt Pella mang tới được lấy bằng cùng một nhiệt kế nhưng ở hai bề mặt khác nhau. Một mẫu nằm dưới mái, mẫu kia phơi nắng; thời điểm đọc cũng lệch hơn một giờ. Thiết bị giống nhau không bù được điều kiện khác nhau. Evelyn đề nghị đo lại theo cặp ở cùng khoảng giờ và ghi vùng bóng râm, không hiệu chỉnh hai số cũ để chúng trông đồng nhất. Số đo nhiệt có thể giải thích cách lớp thử khô; nó chưa cho biết chu kỳ nóng-lạnh của toàn Greenwake.", "", (0, 0)),
    ("workorder", "Phiếu sửa không gửi", "greenwake_refuge", "pella_quinn", "inspect", "pella_old_workorder",
     "Tìm phiếu sửa còn kẹp sau bản vẽ của cha Pella. Một nửa ghi số viên thay, nửa còn lại không có chữ ký bàn giao.", "PELLA QUINN",
     ["Cha tôi đã ghi đủ số đá để dựng lại mặt ngoài, nhưng dòng chuyển ca chưa bao giờ được điền.", "Tôi không thể biến chỗ trống thành lời nhận lỗi của một người đã khuất. Nó chỉ cho thấy việc bàn giao thiếu một bước."],
     "Phiếu sửa dừng giữa hai ca", "Phiếu sửa có số lượng đá thay thế, loại vữa và vị trí xếp từng hàng. Dòng cuối chừa trống tên người nhận ca; không còn mực ở mặt sau hay dấu phụ cho biết người thợ đã tiếp tục ở trang khác. Pella nhớ cha mình giao bản vẽ cho đội Greenwake, nhưng ký ức ấy không xác nhận liệu người nhận có nhìn thấy tờ phiếu này. Cô để trống ô bàn giao trong bản phục dựng và thêm nơi để người tiếp quản ghi tên theo lựa chọn của họ, thay vì điền một phỏng đoán vào sổ cũ.", "document", (6.0, 4.2)),
    ("second_bed", "Cành thứ hai, vết cắt thứ hai", "greenwake_refuge", "pella_quinn", "grow", "glassplum",
     "Trồng lứa Glassplum thứ hai ở phía trong luống. Đặt hạt ở khoảng cách khác và ghi giờ tưới để đối chiếu, không gộp hai luống thành một mẫu.", "MARA BELL",
     ["Lứa đầu gần tường hơn, lứa này ở phía trong. Ta sẽ giữ lại cả hai dù cây nào cho quả đẹp hơn.", "Một kết quả không thuận tiện vẫn là dữ liệu nếu người đọc biết nó đến từ đâu."],
     "Hai luống, hai lần tưới", "Lứa thứ hai được trồng phía trong luống và nhận nước vào một lượt khác với vụ đầu. Cả hai dùng hạt từ cùng một gói, nhưng không cùng vị trí hay lịch tưới. Mara khuyên giữ lại cả hai kết quả, kể cả khi một nhánh phát triển chậm hơn. Nếu chỉ lưu cây lớn nhất, bản ghi sẽ che mất chính điều kiện cần biết khi so rễ với móng tường. Rowan ghi riêng ngày gieo, vị trí và thời điểm tưới rồi không tính trung bình hai luống thành một phép đo.", "", (0, 0)),
    ("measure", "Hai số đo chênh nhau", "greenwake_refuge", "pella_quinn", "inspect", "pella_two_bed_reading",
     "Đối chiếu khoảng cách rễ ở hai luống. Ghi độ lệch cạnh từng vị trí thay vì lấy trung bình làm kích thước cho mọi giống cây.", "ROWAN HALE",
     ["Khoảng hẹp xuất hiện ở luống phía trong, nhưng giờ tưới và độ râm cũng khác.", "Tôi ghi được độ lệch. Chưa thể tách ảnh hưởng của nắng khỏi ảnh hưởng của khoảng cách."],
     "Khoảng lệch giữ bên cạnh mẫu", "Hai điểm đo rễ cho kết quả khác nhau dù chúng đến từ cùng một gói hạt. Luống phía trong có bóng râm lâu hơn và nhận nước muộn hơn; vì thế độ lệch không thể quy cho vị trí đơn lẻ. Rowan ghi khoảng thay vì một giá trị trung bình, để người dựng khớp không lấy con số giữa làm chuẩn cứng. Lần đo sau cần giữ dụng cụ, giờ tưới hoặc vùng sáng ổn định nếu muốn tách các yếu tố. Pella đánh dấu những điều kiện còn thay đổi bằng ký hiệu mở, không xóa chúng khỏi bản đồ.", "cycle_tablet", (-2.6, -3.2)),
    ("craft_resin", "Nấu nhựa mấu rễ có thể tháo", "greenwake_refuge", "pella_quinn", "craft", "greenwake_rootwall_resin",
     "Pha nhựa thử từ sợi Vine Stalker, Glassplum và Brineglass Moss tại Still House. Mẻ này dành cho mẫu đá, không dùng làm lớp chống thấm nước.", "MARA BELL",
     ["Ta cần lớp bám giữ được một lần thử và vẫn có thể gỡ khỏi viên đối chứng.", "Nếu phải phá đá mới tháo được, mẻ này không phù hợp cho bức tường đang dùng."],
     "Mẻ nhựa thử có thể gỡ", "Mẻ nhựa dùng sợi nâu lấy ở khe Greenwake, một phần Glassplum và Brineglass Moss trồng tại Lower Cistern. Mara nấu mẻ nhỏ ở Still House rồi để nguội trên viên đá đối chứng. Công thức được chọn vì bám đủ lâu cho phép so các khớp, nhưng chưa được thử qua mùa mưa hoặc tải trọng lớn. Rowan ghi lượng từng thành phần và giữ một mảnh đá chưa phủ làm đối chứng. Nhựa không được dùng để trám nguồn nước, dán đá chịu lực hay thay vữa của toàn bức tường.", "", (0, 0)),
    ("choice", "Thử khung trước khi sửa", "greenwake_refuge", "pella_quinn", "choice", "pella_rootwall_policy_board",
     "Nghe Pella và Mara trình bày hai cách gia cố. Trước khi chọn, mang bảng thử tới và cân nhắc ai sẽ phải bảo dưỡng từng kiểu mối ghép.", "PELLA QUINN",
     ["Hai bản thử đều dùng cùng mẻ nhựa và cùng mốc đá. Một cách nhường chỗ cho rễ; cách kia cho phép thay miếng chêm theo mùa.", "Tôi từng tin rằng bức tường chỉ cần đứng yên. Giờ tôi muốn để người làm vườn biết chính xác phần nào cần họ kiểm tra."],
     "Hai phương án cho tường rễ", "Pella chuẩn bị hai mẫu từ cùng một viên đá và cùng mẻ nhựa. Khớp bản lề giữ một khoảng thở để rễ lớn thêm; miếng chêm rời chịu một phần áp lực và có thể thay ở lần bảo trì sau. Cả hai đều cần người kiểm tra, nhưng theo lịch khác nhau. Mẫu bàn thử không tái hiện mưa lớn, chuyển động đất hay toàn bộ chiều dài bức tường. Pella quyết định để người làm vườn chọn phương án kèm trách nhiệm bảo trì, đồng thời ghi rõ điều gì vẫn chưa được thử.", "noticeboard", (-1.8, 4.5)),
]

hinge = [
    ("hinge_install", "Lắp mối ghép có khoảng thở", "greenwake_refuge", "pella_quinn", "interact", "pella_rootwall_joint",
     "Lắp nhựa mấu rễ vào khớp bản lề trên bức tường. Vật liệu sẽ bị tiêu hao; Pella sẽ giữ khe mở để rễ không bị ép kín.", "PELLA QUINN",
     ["Đưa khớp vào rãnh rồi dừng trước khi nó chạm đầu rễ.", "Khoảng trống này là một phần của mối ghép, không phải chỗ còn thiếu đá."],
     "Khớp bản lề Greenwake", "Khớp mới giữ hai viên đá cách nhau một khoảng nhỏ, đủ để nhánh rễ còn lại không bị ép vào mép sắc. Nhựa thử được dùng hết trong lớp lót; sau khi khô, khớp vẫn có thể tháo khi cần kiểm tra. Pella đánh dấu điểm gắn bằng vạch đồng để người làm vườn tìm được mà không phải bới đất quanh rễ. Lắp xong không chứng minh tường chịu được mọi cơn mưa. Nó tạo một chỗ quan sát có thể mở lại mà không phá toàn bộ hàng đá.", "rootwall_joint", (-9.1, -2.5)),
    ("hinge_gap", "Khe nhỏ chưa thành đường nứt", "greenwake_refuge", "pella_quinn", "inspect", "pella_hinge_gap",
     "Đọc khoảng hở dưới khớp sau khi nhựa se. Ghi độ rộng tại ba điểm và giữ mốc đo nguyên vẹn.", "ROWAN HALE",
     ["Ba điểm không bằng nhau; phần trên rộng hơn phần sát đất.", "Ta cần nhìn lại cùng các mốc sau một lượt tưới, không tự ép số đo cho thẳng hàng."],
     "Ba điểm ở khớp thở", "Sau khi nhựa se, khoảng hở rộng nhất nằm gần đỉnh khớp, nơi ít đất đỡ nhất. Hai điểm thấp hơn vẫn đo được nhưng có sai số vì bề mặt đá sần. Rowan vẽ ba dấu mốc lên phiếu theo thứ tự từ trên xuống. Nếu lần sau dùng điểm khác, chuỗi so sánh sẽ mất ý nghĩa. Pella không lấp phần rộng nhất chỉ để đường đo trông đều; độ không đều có thể là phản ứng của vật liệu với viên đá hiện tại.", "stone_rill", (-9.2, 2.3)),
    ("hinge_bed", "Lứa thứ ba ở mép khớp", "greenwake_refuge", "pella_quinn", "grow", "glassplum",
     "Thu hoạch thêm một lứa Glassplum gần hàng đá đã gia cố. Quan sát cây sau một lượt tưới nhưng không xem nó là thử nghiệm qua mùa.", "MARA BELL",
     ["Một lượt tưới giữ lá đứng thẳng. Ta chưa biết khớp phản ứng thế nào sau khi đất khô.", "Tôi sẽ ghi màu lá và ngày chăm, không biến chúng thành dấu hiệu tường an toàn."],
     "Lá sau lượt tưới", "Glassplum gần khớp vẫn đứng sau một lượt tưới. Lá phía tường đậm màu hơn lá phía trong, nhưng chúng còn khác nhau về ánh sáng buổi sáng. Mara ghi vị trí từng cụm lá và ngày lấy mẫu. Quan sát chỉ kéo dài trong một lượt tưới; rễ có thể phản ứng chậm hơn phần thân nhìn thấy. Pella giữ lịch kiểm tra khớp độc lập với lịch chăm cây để người đọc không nhầm sức sống của luống với độ bền của công trình.", "", (0, 0)),
    ("hinge_mara", "Mara kiểm tra phần rễ còn sống", "greenwake_refuge", "pella_quinn", "talk", "mara_bell",
     "Mời Mara Bell kiểm tra rễ cạnh khớp. Cô sẽ ghi phần cây còn nguyên và phần đã cắt để mở chỗ cho việc đo.", "MARA BELL",
     ["Tôi sẽ để lại nhánh non sát khe. Nếu nó đổi hướng, ta cần nhìn thấy điều ấy trước khi chạm vào đá.", "Nhánh đã cắt được dán nhãn riêng; tôi không trộn nó vào lịch cây đang sống."],
     "Rễ đang sống và phần đã cắt", "Mara tách phần rễ còn sống cạnh khớp khỏi đoạn đã cắt để lấy mẫu. Hai phần có thể khác nhau về độ ẩm và độ đàn hồi; gộp chúng sẽ làm mất điều kiện của từng mẫu. Cô quyết định không buộc nhánh non vào tường để tránh ép cây đi theo hình muốn có của con người. Pella bổ sung ngày tái kiểm tra sau lượt chăm tiếp theo. Lịch này là lời nhắc kiểm tra, không phải giả định rằng cây sẽ giữ nguyên hướng đến lúc đó.", "", (0, 0)),
    ("hinge_flow", "Nước đi qua mép đá", "cinderwell_basin", "pella_quinn", "inspect", "pella_hinge_flow",
     "So vệt nước trên hai phiến đá đối chứng sau một lần tưới. Một phiến có khớp bản lề, phiến còn lại giữ nguyên.", "ROWAN HALE",
     ["Phiến có khớp giữ lại ít bùn hơn trong lần thử này, nhưng chúng không nằm cùng độ dốc.", "Tôi ghi vị trí đặt mẫu để lần sau đổi chỗ và xem độ nghiêng ảnh hưởng ra sao."],
     "Một lần tưới trên hai phiến đá", "Hai phiến được tưới từ cùng một gáo nước. Phiến có khớp bản lề giữ ít bùn hơn ở cạnh dưới trong lần thử, nhưng độ dốc và vị trí đặt chưa đồng nhất. Rowan không gọi đây là khả năng thoát nước của cả bức tường. Pella đánh dấu hướng dòng và đề xuất đảo vị trí hai phiến ở lần thử kế tiếp. Nếu kết quả đổi theo chỗ đặt, độ dốc có thể giải thích nhiều hơn loại khớp.", "document", (-4.9, 1.0)),
    ("hinge_talia", "Talia đọc vệt bùn sau lượt thử", "cinderwell_basin", "pella_quinn", "talk", "talia_mercer",
     "Hỏi Talia cách giữ riêng đất trên phiến thử khỏi mẫu nước trong basin. Cô yêu cầu ghi rõ nguồn và dụng cụ lấy mẫu.", "TALIA MERCER",
     ["Hai lớp bùn có thể giống màu mà khác nguồn. Đừng rửa chúng vào cùng một khay.", "Tôi sẽ giữ phiếu của phép thử này với ngày lấy mẫu, không thêm nó vào sổ nước sinh hoạt."],
     "Bùn thử không phải mẫu nước", "Talia chỉ nhận phần bùn đã được thu riêng trên phiến thử. Cô ghi nó là vật liệu bám, không gán cho nước trong basin. Khay được tráng riêng để không mang cặn vào các phép đo khác. Mẫu này có thể giúp so độ bám dưới cùng thao tác tưới; nó không cho biết chất gì hòa tan trong nước hay có an toàn để uống hay không. Pella chấp nhận giới hạn ấy và sửa nhãn ở bản vẽ, vốn trước đó chỉ ghi 'nước bẩn'.", "", (0, 0)),
    ("hinge_review", "Vạch bảo trì nằm dưới mái", "greenwake_refuge", "pella_quinn", "inspect", "pella_hinge_review",
     "Đọc lịch bảo trì đặt dưới mái. Ngày xem lại khớp cần tách khỏi lịch thu hoạch và có chỗ để người sau đổi lịch.", "ROWAN HALE",
     ["Pella đã để trống ô sau lượt mưa lớn. Lịch không thể đoán trước ngày mưa ấy.", "Tôi thêm dấu nhắc khi có thay đổi ở rễ, còn khoảng thời gian sẽ do người trông vườn sửa."],
     "Lịch kiểm tra có thể sửa", "Lịch được treo dưới mái để nước không làm nhòe mực. Pella ghi lần kiểm tra đầu, dấu mốc khớp và một điều kiện kích hoạt lần xem tiếp theo: nếu rễ đổi hướng hoặc đất xói sau mưa, người chăm cần quay lại sớm hơn. Không có ngày cố định nào đại diện cho mọi kiểu thời tiết. Ô để sửa được giữ rộng hơn cột ngày, nhắc người sau rằng lịch là công cụ của khu vườn chứ không phải mệnh lệnh không thể đổi.", "noticeboard", (2.8, 4.5)),
    ("hinge_report", "Bức tường có chỗ để dịch chuyển", "greenwake_refuge", "pella_quinn", "talk", "pella_quinn",
     "Báo cho Pella kết quả thử khớp bản lề. Cô sẽ ghi khoảng giới hạn và nhờ Mara cùng người làm vườn nhận việc kiểm tra.", "PELLA QUINN",
     ["Tôi đã thay dòng 'đá xấu' bằng ngày, điểm đo và tên mẫu mà mình thực sự kiểm tra.", "Khớp có thể tháo. Nếu rễ đi hướng khác, người sau không cần phá cả bức tường để biết."],
     "Bản ghi của khớp bản lề", "Pella sửa phiếu cũ bằng một ghi chú mới, không xóa dòng phán đoán ban đầu. Bản sửa nêu khoảng cách khớp, mẫu cây cạnh tường, một lượt tưới và giới hạn của phiến đá đối chứng. Mara nhận việc quan sát rễ trong lịch làm vườn; người sửa tường giữ khóa tháo khớp. Nếu hai người không thể tới cùng ngày, sổ vẫn có chỗ ghi ai đã kiểm tra phần nào. Kết quả là một phương án bảo trì có thể sửa, không phải lời hứa rằng tường sẽ không nứt nữa.", "", (0, 0)),
]

slot = [
    ("slot_install", "Lắp miếng chêm có thể thay", "greenwake_refuge", "pella_quinn", "interact", "pella_rootwall_joint",
     "Lắp nhựa mấu rễ vào rãnh giữ miếng chêm rời. Miếng chêm sẽ chịu lực tạm thời và được thay khi mốc rễ vượt vạch.", "PELLA QUINN",
     ["Để miếng chêm ở ngoài cùng. Người bảo trì cần rút nó ra mà không bẩy viên đá kế bên.", "Tường sẽ không tự biết lúc nào đã đến mùa thay. Ta phải ghi mốc kiểm tra."],
     "Miếng chêm rời Greenwake", "Miếng chêm được giữ trong một rãnh mở, không bị trám kín với lớp vữa cũ. Pella muốn người làm vườn nhìn thấy vạch đo và rút chêm ra khi khoảng rễ thay đổi. Nhựa thử giữ miếng chêm khỏi trượt trong lần kiểm tra, nhưng không được xem là lớp chống nước. Một người có thể tháo nó bằng dụng cụ thường mà không phải phá hàng đá. Cách lắp này đòi hỏi lịch kiểm tra đều hơn phương án bản lề; nếu lịch bị bỏ quên, khe có thể khép mà không ai nhận ra.", "rootwall_joint", (-9.1, -2.5)),
    ("slot_ticks", "Ba vạch trên miếng chêm", "greenwake_refuge", "pella_quinn", "inspect", "pella_slot_ticks",
     "Đọc vạch trên miếng chêm rời. Xác nhận vạch nào là mốc thay và vạch nào chỉ là giới hạn của mẫu thử.", "ROWAN HALE",
     ["Vạch giữa được Pella đánh dấu cho lần thử, còn hai mép chỉ cho biết dụng cụ đã chạm tới đâu.", "Nếu lấy giới hạn thiết bị làm lịch thay, ta sẽ thay chêm trước khi biết rễ đã đổi chưa."],
     "Mốc thay không phải cỡ cây", "Ba vạch nằm trên miếng chêm: hai vạch biên là giới hạn cơ học của mẫu thử, còn vạch giữa là vị trí lúc lắp. Pella không dùng vạch biên làm ngưỡng sinh trưởng vì chúng được chọn theo dụng cụ, không theo rễ. Người chăm cây sẽ so mốc giữa với rễ lộ ra mỗi lần dọn đất, rồi ghi lý do nếu thay sớm. Phiếu hiện chưa có số liệu của cả một mùa, nên vạch vẫn chỉ dẫn cho lần xem tiếp theo.", "document", (-9.0, 2.5)),
    ("slot_owen", "Owen không gộp lịch trời với lịch rễ", "greenwake_refuge", "pella_quinn", "talk", "owen_reed",
     "Hỏi Owen Reed liệu biến đổi tín hiệu sao có thể cho biết ngày rễ nở. Anh nhắc Rowan giữ các lịch khác đơn vị tách biệt.", "OWEN REED",
     ["Bản đồ sao ghi chu kỳ của tín hiệu, không phải nhịp lớn của cây.", "Nếu ta đặt hai lịch cạnh nhau thì phải ghi chúng được đo bằng gì, chứ không vẽ một đường nối cho đẹp."],
     "Hai chu kỳ không tự tạo thành một nguyên nhân", "Owen đặt bản lịch gió cạnh phiếu tăng trưởng của Glassplum. Một bản dùng lần quan sát trời đêm; bản kia dựa trên lượt tưới và thu hoạch. Chúng có thể giúp sắp xếp chuyến kiểm tra để người đo tới đúng thời điểm, nhưng không chứng minh tín hiệu sao điều khiển rễ cây. Owen không đồng ý dùng đường kẻ nối hai cột ngày khi chưa có giả thuyết kiểm tra được. Pella thêm nhãn đơn vị và giữ lịch rễ độc lập với lịch trời.", "", (0, 0)),
    ("slot_fish", "Một mẫu thứ hai từ Celestial Pool", "outerwake_archive", "pella_quinn", "fish", "farwake_carp",
     "Câu thêm một Farwake Carp để lặp thao tác lấy dầu. Ghi đây là lần thứ hai, không gộp hai con thành ước tính nguồn cá.", "ROWAN HALE",
     ["Cùng một điểm câu và cùng loại mồi giúp so thao tác, nhưng hai lần câu vẫn là hai mẫu nhỏ.", "Tôi giữ lọ mới riêng. Nếu kết quả khác, ngày và cách bảo quản có thể là nguyên nhân."],
     "Lần câu lặp lại", "Rowan câu thêm một Farwake Carp ở cùng Celestial Pool để lặp quy trình lấy dầu. Mẫu được lưu trong lọ riêng, dù vị trí và mồi giống lần trước. Hai lượt bắt không đủ để ước lượng đàn cá; chúng chỉ cho thấy thao tác có thể lặp lại trong thời gian ngắn. Pella cần một bản lề mẫu khác nếu muốn biết dầu có đổi ma sát giữa các miếng chêm. Ngày lưu, nhiệt độ nơi cất và dụng cụ lấy dầu được ghi ở cả hai nhãn.", "", (0, 0)),
    ("slot_calendar", "Lịch thay chêm theo dấu rễ", "greenwake_refuge", "pella_quinn", "inspect", "pella_slot_calendar",
     "Đọc lịch thay miếng chêm. Pella đặt dấu kiểm tra theo tình trạng rễ và khoảng đá, không theo ngày cố định của một mùa.", "PELLA QUINN",
     ["Vạch thay cần đi cùng một quan sát: rễ đã chạm tới đâu và khe còn mở bao nhiêu.", "Tôi không muốn người sau tháo chêm chỉ vì lịch nói hôm nay là ngày thứ ba mươi."],
     "Lịch bảo trì dựa trên quan sát", "Lịch mới đặt hai ô cạnh nhau: vị trí rễ nhìn thấy và độ rộng khe đá. Người bảo trì chỉ rút miếng chêm khi một trong hai mốc vượt ngưỡng đã ghi trong bản thử, rồi phải ghi lại ai đã xem. Ngày trên lịch là lời nhắc quay lại, không phải lệnh thay tự động. Pella để trống cột kết quả sau thay để đội vườn có thể kiểm tra liệu thao tác đó có làm khe rộng hơn. Cấu trúc lịch không chứng minh ngưỡng hiện tại đã đúng cho mọi cây.", "cycle_tablet", (3.8, -2.1)),
    ("slot_moss", "Thu thêm rêu cho bản lót", "cinder_cistern", "pella_quinn", "grow", "brineglass_moss",
     "Thu hoạch một lứa Brineglass Moss thứ hai. Pella dùng riêng mẫu này để so lớp lót rãnh chêm, không trộn với mẻ nhựa cũ.", "ROWAN HALE",
     ["Mẻ trước đã dùng gần hết luống. Tôi sẽ ghi ngày trồng mới trước khi cân sợi.", "Mẫu này dành cho rãnh chêm; không thêm kết quả của nó vào phép thử bản lề."],
     "Mẫu rêu thứ hai", "Lứa rêu thứ hai được trồng sau khi mẻ đầu đã nấu, với ngày gieo mới và một phần đất khác trong plot. Rowan tách nó khỏi mẫu cũ để biết vật liệu nào đi vào phép thử rãnh chêm. Cả hai lứa vẫn đến từ cùng một Lower Cistern plot, nên không đại diện cho mọi vùng có Brineglass Moss. Mẫu mới giúp chuẩn bị lớp lót dự phòng; nó không chứng minh cấu trúc sẽ bền nếu rêu không được cung cấp ở mùa sau.", "", (0, 0)),
    ("slot_service", "Hộp dụng cụ có chìa chung", "greenwake_refuge", "pella_quinn", "inspect", "pella_slot_handoff",
     "Kiểm tra hộp dụng cụ cạnh vườn. Chìa có thể giao giữa ca nhưng lịch giao phải để người nhận sửa và trả lại.", "MARA BELL",
     ["Hộp có đủ dụng cụ để rút chêm. Chìa khóa chưa có chỗ ghi người đang giữ.", "Tôi sẽ đặt sổ cạnh móc treo, để việc bàn giao không phụ thuộc vào trí nhớ của một người."],
     "Chìa khóa được bàn giao", "Hộp dụng cụ có cờ lê rút chêm và thước đo khớp. Trước đây chìa được treo ở cửa mà không có sổ, nên Mara không thể biết dụng cụ đang ở đâu khi cần kiểm tra gấp. Bản mới thêm ô giờ mượn, giờ trả và một dòng cho người kế tiếp chỉnh lịch. Họ có thể từ chối ca hoặc chuyển chìa cho người khác. Hộp không tạo ra người bảo trì tự động; nó chỉ làm rõ trách nhiệm đang nằm ở đâu khi một người không thể tiếp tục.", "sealed_case", (-7.0, 2.9)),
    ("slot_report", "Miếng chêm có người nhận việc", "greenwake_refuge", "pella_quinn", "talk", "pella_quinn",
     "Báo cho Pella kết quả của phương án miếng chêm rời. Cô sẽ ghi rõ lịch xem lại và người có quyền sửa lịch đó.", "PELLA QUINN",
     ["Tôi giữ dòng sửa cũ bên cạnh cách lắp mới. Không ai phải giả vờ rằng bản đầu chưa từng được tin.", "Miếng chêm có thể thay, còn lịch chăm cây có thể đổi. Điều quan trọng là hai việc ấy không bị nhập thành một."],
     "Bản ghi miếng chêm theo mùa", "Pella cập nhật bản vẽ bằng vị trí rãnh, mốc đo và quy trình bàn giao chìa hộp dụng cụ. Người làm vườn giữ quyền thay lịch khi mưa đến sớm hoặc không có ai trực; người xây tường ghi nguyên nhân mỗi lần rút chêm. Bản ghi vẫn giữ dòng cũ về đá hỏng để người đọc thấy vì sao đội sửa đã chọn cách lắp trước đây. Phương án mới không bảo đảm khớp luôn an toàn. Nó giúp người sau nhận ra lúc nào cần kiểm tra và có thể sửa hướng dẫn mà không xóa lịch sử.", "", (0, 0)),
]

afterword = (
    "afterword", "Dòng sửa được để mở", "greenwake_refuge", "pella_quinn", "talk", "pella_quinn",
    "Trở lại gặp Pella sau khi hoàn tất một phương án. Cô ghi quyết định vào sổ nhưng để người làm vườn tiếp theo sửa cách bảo trì.", "PELLA QUINN",
    ["Tôi từng xem một ô trống như lỗi của người viết. Giờ tôi biết có khi nó là chỗ dành cho người tới sau.", "Cảm ơn Rowan đã giúp tôi thay cách đọc dòng cũ mà không bắt tôi chối bỏ nó."],
    "Sổ tường Greenwake có dòng dành cho người sau", "Bản cuối giữ cả dòng kết luận cũ lẫn phương án được chọn. Pella ghi tên người chịu trách nhiệm xem khớp, vị trí bản nhựa dự phòng và nơi đặt dụng cụ. Cô không điền sẵn ngày cho nhiều mùa tiếp theo; người chăm vườn sẽ bổ sung sau khi quan sát cây. Bức tường đã được gia cố theo một mẫu nhỏ, còn các đoạn khác vẫn cần kiểm tra riêng. Sổ đóng lại bằng một ô mở dành cho sai số hoặc cách sửa mới, để công trình không phụ thuộc vào việc người kế tiếp phải coi bản vẽ cũ là hoàn hảo.", "", (0, 0)
)


def quest_id(key):
    return "side_greenwake_rootwall_" + key


def make_quest(step, previous=None, branch=None):
    key, title, location, giver, kind, target, objective, speaker, lines, record_title, body, visual, position = step
    qid = quest_id(key)
    did = "greenwake_rootwall_" + key + "_dialogue"
    objectives = []
    if key == "choice":
        objectives.append({"id": "rootwall_choice_conversation", "kind": "talk", "targetId": "pella_quinn",
                           "requiredCount": 1, "description": "Nghe Pella trình bày hai kết quả thử trước khi quyết định.",
                           "dialogueId": did})
        objectives.append({"id": "rootwall_policy_decision", "kind": "choice", "targetId": target,
                           "requiredCount": 1, "description": "Chọn cách gia cố và ghi rõ việc bảo trì đi kèm."})
    else:
        objectives.append({"id": "rootwall_" + key + "_objective", "kind": kind, "targetId": target,
                           "requiredCount": 1, "description": objective, "dialogueId": did})
    entry = {
        "id": qid, "arcId": "the_hundredth_champion", "stage": -1, "type": "side",
        "locationId": location, "giverId": giver, "title": title, "objective": objective,
        "prerequisiteIds": [quest_id(previous)] if previous else [], "objectives": objectives,
        "reward": {"gold": 8 + (len(key) % 6), "items": []}
    }
    if key == "open":
        entry["prerequisiteIds"] = ["champion_star_map"]
        entry["reward"]["items"] = [
            {"itemId": "glassplum_seed", "quantity": 3},
            {"itemId": "brineglass_moss_spore", "quantity": 2},
            {"itemId": "earthworm_bait", "quantity": 6}
        ]
    if key == "choice":
        entry.update({
            "choiceFlag": "greenwake_rootwall_method", "choiceSpeaker": "PELLA QUINN",
            "choicePrompt": "Chọn kiểu gia cố cho bức tường rễ. Cả hai cần người theo dõi; khác nhau ở cách tiếp cận phần rễ.",
            "choices": [
                {"id": "breathing_hinge", "label": "Giữ một khe thở có thể tháo để rễ đổi hướng.",
                 "flagValue": "breathing_hinge", "dialogueId": "greenwake_rootwall_choice_hinge",
                 "reward": {"gold": 0, "items": [{"itemId": "greenwake_rootwall_hinge_charm", "quantity": 1}]}},
                {"id": "seasonal_shim", "label": "Dùng miếng chêm rời, thay theo mốc quan sát mỗi mùa.",
                 "flagValue": "seasonal_shim", "dialogueId": "greenwake_rootwall_choice_shim",
                 "reward": {"gold": 0, "items": [{"itemId": "greenwake_rootwall_shim_charm", "quantity": 1}]}}
            ]
        })
    if branch:
        entry["branchFlag"], entry["branchValue"] = "greenwake_rootwall_method", branch
    if key == "afterword":
        entry["prerequisiteIds"] = []
        entry["prerequisiteGroups"] = [{"anyOfQuestIds": [
            quest_id("hinge_report"), quest_id("slot_report")
        ]}]
    return entry, {"id": did, "speakerName": speaker, "lines": lines}, {
        "id": "greenwake_rootwall_" + key + "_record", "title": record_title,
        "category": "Greenwake Rootwall Survey", "writtenBy": speaker.title(),
        "unlockQuestId": qid, "body": body
    }


def main():
    if len(common) != 19 or len(hinge) != 8 or len(slot) != 8:
        raise RuntimeError("The authored route must contain 36 quest definitions.")
    quests, dialogues, codex, landmarks = [], [], [], []
    previous = None
    for step in common:
        entry, dialogue, record = make_quest(step, previous)
        quests.append(entry); dialogues.append(dialogue); codex.append(record)
        previous = step[0]
        if step[5] == "pella_rootwall_policy_board":
            dialogues.extend([
                {"id": "greenwake_rootwall_choice_hinge", "speakerName": "PELLA QUINN", "lines": [
                    "Tôi chọn khớp bản lề để nhánh rễ có thể đi tiếp. Mara sẽ xem cây; tôi sẽ xem đá.",
                    "Nếu khe rộng thêm, người sau tháo khớp và đo lại thay vì chèn đá cho vừa." ]},
                {"id": "greenwake_rootwall_choice_shim", "speakerName": "PELLA QUINN", "lines": [
                    "Tôi chọn miếng chêm để có thể thay phần chịu lực mà không tháo cả hàng tường.",
                    "Lịch kiểm tra cần người nhận việc; nếu thiếu người, họ được đổi lịch chứ không bị ghi lỗi." ]}
            ])
    for branch_steps, branch_value in [(hinge, "breathing_hinge"), (slot, "seasonal_shim")]:
        previous = "choice"
        for step in branch_steps:
            entry, dialogue, record = make_quest(step, previous, branch_value)
            quests.append(entry); dialogues.append(dialogue); codex.append(record)
            previous = step[0]
    entry, dialogue, record = make_quest(afterword, "afterword")
    quests.append(entry); dialogues.append(dialogue); codex.append(record)

    # Install the route's reusable pixel landmarks only for authored inspect/choice steps.
    marker_rows = [
        ("pella_wall_sill_marker", "pella_wall_sill", "stone_rill", "Chân móng phía đông", "greenwake_refuge", (9.1, -2.7)),
        ("pella_mortar_record_marker", "pella_mortar_record", "document", "Mặt gãy trong đất ẩm", "greenwake_refuge", (5.5, -4.0)),
        ("pella_growth_ring_marker", "pella_growth_ring", "document", "Vòng tăng trưởng", "greenwake_refuge", (1.7, 2.2)),
        ("pella_mite_residue_marker", "pella_mite_residue", "sealed_case", "Khay sợi mắc ở đá", "greenwake_refuge", (-7.0, -4.6)),
        ("pella_cinderwell_stone_marker", "pella_cinderwell_stone", "document", "Bậc đá cũ", "cinderwell_basin", (1.1, 2.7)),
        ("pella_cistern_survey_marker", "pella_cistern_survey", "sealed_case", "Sơ đồ lật mặt", "cinder_cistern", (-2.4, -2.5)),
        ("pella_old_workorder_marker", "pella_old_workorder", "document", "Phiếu sửa dở dang", "greenwake_refuge", (6.0, 4.2)),
        ("pella_two_bed_reading_marker", "pella_two_bed_reading", "cycle_tablet", "Bảng đo hai luống", "greenwake_refuge", (-2.6, -3.2)),
        ("pella_rootwall_joint_marker", "pella_rootwall_joint", "rootwall_joint", "Khớp tường rễ", "greenwake_refuge", (-9.1, -2.5)),
        ("pella_hinge_gap_marker", "pella_hinge_gap", "stone_rill", "Vạch khe bản lề", "greenwake_refuge", (-9.2, 2.3)),
        ("pella_hinge_flow_marker", "pella_hinge_flow", "document", "Phiến thử dòng nước", "cinderwell_basin", (-4.9, 1.0)),
        ("pella_hinge_review_marker", "pella_hinge_review", "noticeboard", "Lịch bảo trì dưới mái", "greenwake_refuge", (2.8, 4.5)),
        ("pella_slot_ticks_marker", "pella_slot_ticks", "document", "Ba vạch trên chêm", "greenwake_refuge", (-9.0, 2.5)),
        ("pella_slot_calendar_marker", "pella_slot_calendar", "cycle_tablet", "Lịch quan sát rễ", "greenwake_refuge", (3.8, -2.1)),
        ("pella_slot_handoff_marker", "pella_slot_handoff", "sealed_case", "Hộp dụng cụ có sổ", "greenwake_refuge", (-7.0, 2.9)),
        ("pella_quinn_actor", "pella_quinn", "pella_quinn", "Pella Quinn", "greenwake_refuge", (4.7, 1.5)),
        ("pella_policy_board_marker", "pella_rootwall_policy_board", "noticeboard", "Bảng phương án gia cố", "greenwake_refuge", (-1.8, 4.5)),
    ]
    for marker_id, target_id, visual, display, location, pos in marker_rows:
        landmarks.append({"id": marker_id, "locationId": location, "displayName": display,
                          "targetId": target_id, "visualId": visual, "positionX": pos[0],
                          "positionY": pos[1], "scale": 0.085})

    items = [
        {"id": "greenwake_root_vine_fiber", "name": "Sợi nâu từ hốc rễ",
         "description": "Mẫu sợi thực vật mắc dưới bức tường Greenwake. Dùng để thử độ bám trên đá đối chứng; chưa xác định sinh vật nào đã kéo sợi qua khe.",
         "category": "material", "maxStack": 99, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 1},
        {"id": "greenwake_rootwall_resin", "name": "Nhựa Mấu Rễ",
         "description": "Mẻ nhựa nhỏ từ sợi nâu, Glassplum và Brineglass Moss. Có thể tháo khỏi viên đá thử; không phải keo chống nước hay vữa chịu tải.",
         "category": "material", "maxStack": 9, "attackBonus": 0, "guardBonus": 0, "healAmount": 0, "sellValue": 0},
        {"id": "greenwake_rootwall_hinge_charm", "name": "Khuyên Rễ Thở",
         "description": "Bùa của Pella dành cho người để lại khoảng điều chỉnh. Tăng 1 Công và 1 Giáp.",
         "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 1, "guardBonus": 1, "healAmount": 0, "sellValue": 0},
        {"id": "greenwake_rootwall_shim_charm", "name": "Chốt Khe Theo Mùa",
         "description": "Bùa ghi dấu một mối ghép có thể thay và lịch kiểm tra có thể sửa. Tăng 2 Giáp.",
         "category": "equipment", "equipmentSlot": "charm", "maxStack": 1, "attackBonus": 0, "guardBonus": 2, "healAmount": 0, "sellValue": 0},
    ]
    recipe = {"id": "brew_greenwake_rootwall_resin", "displayName": "Pha Nhựa Mấu Rễ",
              "stationId": "greenwake_alchemy_still", "discipline": "alchemy",
              "outputItemId": "greenwake_rootwall_resin", "outputQuantity": 1,
              "ingredients": [{"itemId": "greenwake_root_vine_fiber", "quantity": 1},
                              {"itemId": "glassplum", "quantity": 1},
                              {"itemId": "brineglass_moss", "quantity": 1}]}
    encounter = {"id": "greenwake_rootwall_vine_stalker", "monsterId": "crawl_vine_stalker",
                 "locationId": "greenwake_refuge", "positionX": -4.6, "positionY": -4.6,
                 "requiredQuestId": quest_id("mite"), "blockedQuestId": "", "blockedDialogueId": "",
                 "contributesToQuest": True, "defeatObjectiveTargetId": "greenwake_rootwall_mite",
                 "defeatDialogueId": "greenwake_rootwall_mite_dialogue", "downDialogueId": "rowan_field_retreat",
                 "reward": {"gold": 14, "items": [{"itemId": "greenwake_root_vine_fiber", "quantity": 1}]}}

    for filename, additions in [
        ("prologue_quests.json", quests), ("dialogue_catalog.json", dialogues),
        ("codex_catalog.json", codex), ("quest_landmarks.json", landmarks),
        ("item_catalog.json", items), ("recipe_catalog.json", [recipe]),
        ("encounter_catalog.json", [encounter])
    ]:
        catalog = read(filename)
        upsert(catalog["entries"], additions)
        write(filename, catalog)
    print(f"Installed {len(quests)} quests, {len(dialogues)} dialogue entries, {len(codex)} records, "
          f"{len(landmarks)} landmarks, {len(items)} items, one recipe and one encounter placement.")


if __name__ == "__main__":
    main()
