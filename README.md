# Ashen Oath — Unity mobile RPG

`game-rpg` là dự án Unity mới, độc lập với `game-mobile` và `game-space`.

**Ashen Oath** là RPG 2D pixel chơi offline trên mobile. Người chơi theo chân Rowan Hale, một kỵ sĩ tập sự mất quê nhà trong cuộc đột kích của ma tộc. Cậu dần phát hiện “ma vương” là vai diễn mà những dũng sĩ đời trước tự nhận để duy trì vòng đại hiến tế 100 năm.

## Chạy thử

1. Mở `game-rpg` bằng Unity **6000.6.2f1** hoặc Unity 6 tương thích.
2. Mở `Assets/Scenes/Main.unity`.
3. Nhấn **Play**. Dự án không cần đăng nhập, máy chủ hay mạng để chơi.
4. Trên máy tính: WASD/mũi tên để đi, `E` để tương tác, `Space` để đánh hoặc giật cần khi câu cá, `Shift` để lướt né khi giao chiến, `1` để uống thuốc, `I` mở hành trang. Chạm vào trang bị trong hành trang để mặc.
5. Trên điện thoại: dùng cần điều khiển và nút cảm ứng trên màn hình.

Màn mở đầu dùng tranh pixel-art riêng, phát nhạc title ngoại tuyến và hiện nút bắt đầu hoặc tiếp tục theo save trên máy. Bản save hiện tại không bị xóa khi vào màn này.

Rowan có animation đi bộ bốn hướng, mỗi hướng bốn frame; hướng nhìn theo input và frame đầu tiên được giữ làm tư thế nghỉ. Các frame được cắt từ atlas runtime và canh chung theo chân trong exploration, combat và dodge.

Alden Vale, boss cuối của nhánh Crown of Ash, dùng hoạt ảnh idle/run/attack/hit/death theo từng pha trận. Rowan, Mira, Elara, Dr. Evelyn Hart, Jace Morrow, Nia Porter, Mara Bell, Ruth Calder và Ada Sloane có chân dung pixel riêng xuất hiện cùng thoại của họ. Soundtrack CC0 đổi theo cả 11 khu vực; các bản chiến đấu, mở đầu và gục có cue riêng, được stream offline.

Audit hiện ghi nhận 297.341 từ player-facing sau khử trùng, còn thiếu 702.660 từ. Lượt mới nhất hoàn tất tuyến Ada Sloane: thêm quest nấu Emberroot–Starlit Minnow Pottage tại bếp dã chiến Crownfall, tiêu hao món ở nhánh open-table và sửa việc trao hai charm nhánh (+225 từ duy nhất). Unity validator chạy cả hai chính sách qua farming, fishing có mồi, cooking, vật phẩm/codex đúng nhánh và save/resume; campaign 24 giờ cùng playtest điện thoại chưa xác nhận.

Artifact preview ARM64 tại [Build/AshenOath-Offline-Preview.apk](Build/AshenOath-Offline-Preview.apk) có 408,721,325 bytes; SHA-256 `2904f6a70acc202d10da71f23f46f8caba28f50712816855f64456543d8eb300`. Unity 6000.6.2f1 build exit code 0; APK ZIP qua integrity. Log `/tmp/game-rpg-crownfall-table-cooking-build.log`; validator `/tmp/game-rpg-crownfall-table-cooking-validation.log`. Có thể build lại từ menu Ashen Oath > Build Android Offline Preview APK.

Tuyến Ashfall mới **The Door Beyond the Herb Table** thêm 40 quest cho Mira Cole: khôi phục phòng điều trị đã đóng, trồng Emberlily/Moonwort, câu cá và pha Emberlily Balm dùng được trong gameplay. Mira chọn mở phòng khám cố định hoặc mang túi thuốc lưu động; hai nhánh có charm, codex và dấu hiệu bản đồ riêng. Unity validator đã mô phỏng cả hai nhánh route và qua; playtest trên thiết bị chưa chạy.
Arc 1 bổ sung 32 entry thoại cho 30 objective phản hồi và hai lựa chọn đầu: Mira/Gideon/Alden trả lời trong các cuộc gặp, còn Rowan ghi riêng điều quan sát được sau chiến đấu, điều tra, gieo trồng, câu cá và pha chế. Các objective ID, prerequisite và phần thưởng không đổi.

Tuyến **The Hundredth Roll** vốn nối 99 nhiệm vụ kiểm tra landmark và mở một hồ sơ theo mỗi người tiền nhiệm. Cả 99 hồ sơ codex nay có thêm tư liệu hiện trường, đối chiếu nguồn và giới hạn của điều có thể kết luận; thứ tự quest và điều kiện mở khóa vẫn giữ nguyên. Phần mở rộng đã vào APK nhưng chưa được đọc thử trong game trên điện thoại.

Side quest **Waymarks Between Us** nối tám chặng qua các vùng bằng việc đo landmark, câu Blackreed Trout/Whisper Koi/Farwake Carp, trồng Salt Saffron/Skyroot và đánh bại Salt Hound ở Salt Road. Tại Outer-Wake Rowan chọn công khai bản đồ hiệu chỉnh hoặc gửi bản sao qua người đưa tin; hai kết quả có charm và codex riêng.

Tuyến phụ Arc 6 **The Wall That Learned to Bend** thêm 36 quest cho Pella Quinn ở Greenwake: điều tra vết nứt, lấy mẫu rêu, trồng Glassplum, câu Farwake Carp và pha nhựa để lắp tường. 36 codex của tuyến được mở rộng (+4.581 từ sau khử trùng) bằng ghi chép bảo quản mẫu, bàn giao dụng cụ và lịch kiểm tra có thể sửa. Người chơi chọn khớp thở có khe điều chỉnh hoặc nêm theo mùa tháo rời; hai nhánh có charm/codex riêng và không xem phép thử tại chỗ là chứng nhận an toàn kết cấu.

Tuyến Arc 4 **The Arrow Before the Answer** thêm 38 quest và 38 codex cho Silas Vane; cả 38 hồ sơ nay có ghi chú bổ sung về phép đo, quyền sở hữu lời khai, đường đi của bản sao và quy trình đính chính. Silas nhận trách nhiệm đã bắn tín hiệu ở tuổi mười tám nhưng không tự kết luận tác động của nó: Rowan khảo sát mũi tên hiệu lệnh đầu tiên bằng bản đồ, phép đo tầm nhìn ban ngày, Windglass Reed, Saltspool Skate, Roadglass Sentinel và một charm rèn tại Dawnkeep. Silas chọn ký bản tường trình công khai hoặc gửi bản riêng cho gia đình xem; hai nhánh giữ riêng quyền của người làm chứng và không kết luận mũi tên đã quyết định đường đi của đoàn xe. Tuyến Nella **The Blank Name That Stays Blank** có 21 codex bổ sung ghi cách bảo quản thẻ, đếm móc trống, kiểm soát bản sao và tiếp nhận nhân chứng; search vẫn mở, đích đến của người em vẫn chưa rõ.

Tuyến Arc 5 **The First Oath’s Missing Measure** thêm 40 quest cho The First Warden sau `choir_reckoning`: Rowan đối chiếu ký ức Warden với một phép thử âm thanh hiện tại, khảo sát Echo Kelp và Whisper Koi, đánh Choir Merrow, rồi rèn một charm ở Choir Harmonic Anvil. Người chơi chọn bản tường trình công khai bằng ngôi thứ nhất hoặc folio riêng có thể yêu cầu; mỗi nhánh giữ khác biệt giữa hồi ức và phép đo, trao codex/charm riêng rồi hội tụ.

Tuyến Arc 7 **Four Places Left Unassigned** thêm 15 quest cho Jace Morrow sau hồ sơ khảo sát: Rowan đo case bốn ngăn, trồng Skyroot, câu Farwake Carp, kiểm tra gió và receiver thụ động rồi cùng Evelyn rà bản nháp. Lựa chọn giữa công bố quy trình có thể kiểm tra hoặc giữ trang cá nhân trong folio có thể yêu cầu; hai nhánh giữ trống danh tính và kết cục của đoàn khảo sát, rồi hội tụ ở hồ sơ đính chính. Mười lăm codex của tuyến được mở rộng (+1.770 từ audit) với ghi chép về case, Skyroot, mẫu Farwake Carp, gió và receiver thụ động; không xác định nguồn tín hiệu.

Tuyến **Hai hồi chuông** thêm 17 quest ở Ashfall: Harper Wills khảo sát khung chuông, gió, mép giếng và góc nhìn; Rowan dọn một Ash Goblin, trồng Moonwort, pha Phấn Dấu Mưa rồi thử tín hiệu ở hai vị trí. Lựa chọn cuối ưu tiên nhịp chuông trầm hoặc cờ tam giác có gân nổi; mỗi route có cảnh thử, quy ước codex và charm riêng. Cả hai nhánh ghi giới hạn về gió, tầm nhìn, thính giác và quyền tự chọn tham gia.

Tuyến phụ **Ashfall Muster** có năm quest sau một trong hai báo cáo mở đầu: Rowan cùng Mira Cole và Gideon Park kiểm tra cách ghi người trú ẩn, những dòng chưa xác minh, vải che và bản đồ sơ tán. Ở chặng cuối, người chơi chọn bảng chia sẻ có cảnh báo hoặc phiếu tuyến hộ gia đình; hai nhánh tặng charm và codex riêng.

Arc 8 có tuyến đo đạc phụ của Ada Sloane: đối chiếu dự báo kho lương với thước thóc, mực hồ, một vụ Emberroot và một Starlit Minnow. Người chơi chọn công khai phương pháp kèm sai số hoặc chờ các vùng rà bản có tên; hai nhánh cho vật phẩm và codex riêng, không quyết định thay ending.

Tuyến **The Table Beside the Forecast** có 25 quest cho Ada Sloane và Captain Alden Vale. Rowan phân biệt lượng thu hoạch, hạt giống dự trữ và đồ ăn thực sự đưa ra bàn, rồi trồng Emberroot, câu Starlit Minnow và nấu Emberroot Pottage hồi 20 HP. Nhánh open-table tiêu hao phần ăn; posted-rule giữ món. Hai nhánh có charm/codex riêng và Unity validator đã mô phỏng tới save/resume.

Tuyến **Ca trực còn trống** thêm 12 nhiệm vụ phụ cho Alden sau `last_oath_records`. Rowan trồng Emberroot để thử giờ nghỉ sau ca lạnh, câu Starlit Minnow rồi rèn Con Suốt Đổi Gác tại Last Oath Forge. Sau khi đối chiếu dấu mài trên kiếm, danh sách chu kỳ và quy tắc của The First Warden, người chơi chọn cuộn tên chỉ dành cho người tự xác nhận hoặc lịch theo hộ giữ riêng tên; mỗi nhánh có vật chứng, charm và codex riêng rồi hội tụ ở lời hậu từ của Alden. Validator chạy cả hai nhánh qua gieo trồng, câu cá, chế tạo, lựa chọn và save/resume.

Arc 8 có thêm ghi chép về việc hỏi đồng thuận trước khi ghi tên, quyền từ chối không cần lý do, cách yêu cầu xem hoặc đính chính hồ sơ có tên/niêm phong, và lịch gác có giờ nghỉ. 26 lượt thoại mới ở 12 cảnh kết thúc để Alden nói rõ hồi ức của ông không thay được lời khai của 99 người; Ý Chí Thế Giới thừa nhận dự báo không chứng minh rằng nó có quyền chọn thay người; Rowan tự nhận trách nhiệm cho từng lời thề. Hai ending vẫn giữ lựa chọn và hậu quả riêng, không khẳng định rằng đường chưa biết là cứu rỗi.

Có tám vùng chính và ba bản đồ phụ: Dawnkeep Cadet Barracks, Cinderwell Lower Cistern và Salt Lockhouse. Doanh trại mở sau lời thề cadet; tuyến ba nhiệm vụ với Nia Porter đối chiếu phiến điểm danh và thư gửi trả, giữ rõ điều chưa xác minh, rồi thưởng Huy hiệu Chừa Lề cùng một tư liệu codex.

Arc 2 còn có tuyến gia đình Nia gồm 15 nhiệm vụ: người chơi kiểm kê phong bì, huy hiệu, giờ đổi ca, dấu bàn giao, quyền truy cập và biên nhận. Mười lăm codex mới làm rõ khác biệt giữa đếm thư, giao thư và xác nhận người nhận đã đọc; hai route chia sẻ tổng số có chú giải hoặc niêm phong hồ sơ cho gia đình xem riêng, giữ quyền sửa bản sao và không đưa ra kết luận về Ellis. Arc 2 cũng có tuyến phụ năm bước về sai lệch thủy lộ: Rowan câu Blackreed Trout để xác nhận dòng nối tới hồ tại thời điểm bắt được, đọc hai mốc nước, nhờ Tomas Reed rèn Bùa Mốc Nước Cadet, đo lại ở cột thấp rồi trả cả hai số cho Nia. Codex giữ phương pháp và sai số cạnh nhau, không dùng một lần đo để kết luận ai mở cống hay Ellis đã tới đó. Tuyến Elara Wren gồm 15 quest khôi phục khu vườn cadet dưới máng phía đông: đọc phiến đổi ca, trồng Dawnmeadow Mint, câu Blackreed Trout, rèn và lắp kẹp runoff có thể tháo, rồi chọn luống chung hoặc lượt chăm sóc ngắn có thể đổi. Cả hai chính sách trao charm/codex riêng và hội tụ ở lời hậu từ; 10 codex Garden Practice mới đi theo từng quest chung của tuyến (+2.092 từ audit), còn hai kết quả nhánh giữ hồ sơ riêng. Validator trước đó mô phỏng hai chính sách qua mồi câu, crop, craft, tiêu hao kẹp và save/resume. Arc 3 có hai nhánh điều tra hậu quả của lựa chọn nước và Cistern Warden. Một tuyến phụ bảy definition đối chiếu kích thước cốc, khoảng mở van và sai số cân hạt, rồi để người chơi chọn lịch theo hộ có đồng thuận hoặc tổng lượng theo ngày kèm khiếu nại kín. Mỗi nhánh mở codex riêng và vật liệu rèn Khóa Sổ Cistern tại Dawnkeep; dữ liệu không chỉ mặt người chịu trách nhiệm khi chưa có bằng chứng; Arc 4 nối ba lời chứng tại Lockhouse với một tín hiệu chuông chưa rõ số phận Ellis; Arc 5 có hai tuyến phụ về hồ sơ Choir: ba chặng lập mục lục bản chép và 14 definition Mara Voss về tiếng nói chưa nhận dạng, đồng thuận và kiểm soát phát lại. Trong story Arc 7, sáu nhiệm vụ mới kiểm tra lại khoảng tín hiệu, đồng hồ gió, mực hồ, ghi chép của Jace và thiết bị nghe thụ động trước khi Rowan báo cáo cho Evelyn. Tuyến phụ tám bước sau báo cáo vẫn cho đo lại, dùng Skyroot và Farwake Carp để kiểm tra chéo, rèn cuộn thu từ nhựa cây cùng Astral Prism, rồi chọn gửi chuỗi nhịp trống hay chỉ lưu tín hiệu đến. Mỗi route mở codex riêng và La Bàn Gió Xa; không khẳng định nguồn phát đã được nhận diện. Hai tuyến bếp Cinderwell của Sister June và Oren Bell có tổng cộng 40 codex được mở rộng (+4.618 từ audit): tư liệu tách ký ức về bữa ăn khỏi lượng giống, khẩu phần và nhu cầu của cả basin; hạt dùng cho bếp không bị gộp vào kho dự trữ chiến lược. Arc 8 có hai route boss và epilogue riêng: Crown of Ash hoặc Beyond the Veil. Arc 6 còn có tuyến phụ Owen Reed/Mara Bell 11 quest thử lại bản đồ sao gia đình bằng số đo rễ, gió Outer-Wake và mẫu Farwake Carp, rồi chọn công bố phương pháp hoặc gửi bản sao riêng có ngày xem lại.

Catalog source có 1.001 quest (117 story, 884 side), 1.221 thoại, 735 codex, 211 loài / 223 encounter placement gồm 54 elite và 16 boss, 360 item (255 trang bị), 45 recipe, 11 luống cây và 6 điểm câu cá. Audit đếm 7.832 chuỗi player-facing và 297.341 từ sau khử trùng; còn thiếu 702.660 từ để đạt 1.000.001. Thời lượng 24 giờ chưa được xác minh bằng playtest thiết bị.

Tuyến Sister June **A Pot for the Road Back** thêm 16 quest cho Cinderwell: đánh dẹp pantry Muck, trồng barley, câu Emberscale Perch ở Warm Run rồi nấu Stone-Pot Broth tại bếp mới. Người chơi phân phối bát đầu tiên cho ca trực còn lại hoặc đóng gói cho đội lên đường; nhánh thưởng charm/codex riêng, còn bát thứ hai dùng hồi 36 HP.

Tuyến Cinderwell của Oren Bell **The Tin Behind the Scale** thêm 24 quest sau hậu từ của June. Rowan mở chiếc hộp hạt mẹ Oren để lại, trồng hai hàng barley, câu Emberscale Perch rồi nấu Tin-Keeper’s Barley Cake hồi 44 HP. Lựa chọn đặt gói hạt cuối lên kệ trao đổi hoặc giữ trong hòm mùa đông mở hai quest/codex/bùa riêng; phần route chung biến ký ức gia đình thành món ăn có thể tiếp tục thay đổi. Validator Unity mô phỏng cả hai nhánh qua hai vụ trồng, câu cá, nấu bánh và save/resume.

Tuyến Ashfall **The Cart Beside the Road** thêm 22 quest cho Gideon Park: Rowan kiểm tra xe sơ tán, dọn đường thử, thu hồi sắt, đo vai trục với Tomas Reed rồi rèn chốt ở Dawnkeep Forge. Chốt bị tiêu hao khi lắp; sprite xe và trạng thái sửa được lưu theo tiến độ quest. Hai mươi hai codex tuyến được mở rộng (+2.848 từ audit), từ kiểm tra moay-ơ và tải thử đến cách bàn giao xe chung hoặc bộ dụng cụ tự nguyện. Hai lựa chọn cuối có charm/codex riêng. Unity validator đã mô phỏng cả hai cách sử dụng xe qua save/resume.

Tuyến liên vùng **The Open Joint Atlas** thêm 30 quest cho Arc 2: Tomas Reed đề nghị Rowan kiểm chứng thước hàm điều chỉnh tại Ashfall, Salt Road, Cinderwell, Greenwake, Choir và Outer-Wake. Người chơi trồng Windglass Reed/Glassplum, câu Saltspool Skate/Whisper Koi/Farwake Carp, rèn dụng cụ ở Dawnkeep Forge rồi thử tại giá xe. 30 codex tuyến này được mở rộng (+3.624 từ audit), với ghi chú về hiệu chỉnh, custody dụng cụ, điều kiện mẫu và bản sửa hướng dẫn. Hai cách phát hành bản hướng dẫn khác nhau quyền chỉnh sửa và phạm vi chia sẻ; mỗi nhánh mở charm/codex riêng. Các bài đo nêu rõ điều kiện và giới hạn để một số đo địa phương không bị biến thành tiêu chuẩn cho mọi nơi.

Lower Cistern có tuyến phụ 17 quest sau Cistern Warden: Rowan kiểm tra bánh khóa, trồng Brineglass Moss, hạ Pressure Wight rồi chế và lắp màng lọc để so cặn trong một lượt thử. Talia giữ rõ rằng kết quả không chứng nhận nước uống an toàn. Người chơi chọn tay gạt có chốt giới hạn hoặc lịch vận hành theo ca; hai route có charm/codex riêng và hội tụ ở hậu từ. Validator mô phỏng cả hai qua farming, encounter, crafting, tiêu hao vật phẩm và save/resume.

Ba tuyến phụ mới kéo dài 41 quest: Jace Morrow mở lại báo cáo khảo sát bằng phép đo Skyroot/Farwake lặp được; Lyra Moss viết và chọn cách chia sẻ giai điệu của mình; Mara Bell thử hai vụ Glassplum trước khi chọn điều khoản chia sẻ giống. Các nhánh có landmark, vật phẩm, recipe/crop dùng được, codex riêng và đã được validator mô phỏng qua gameplay services cùng save/resume.

Field Bestiary có 58 sprite CC0 16×16; Verdant Memory có thêm 54 sprite CC0 32×32; và Crawl thêm 55 sprite CC0 32×32. Mỗi loài có encounter thật, mục tiêu quest, ghi chú sau trận và trang bị riêng. Hai hợp đồng nhiều mục tiêu trên mỗi bản đồ mở dần qua 11 vùng, cùng 11 field study khóa tới khi hoàn thành. Tổng hiện có 211 loại quái, 54 elite và 16 boss. Sprite dùng point filtering; nguồn, license, archive và mapping nằm trong [asset ledger](Docs/ASSET_SOURCES.md).

Đây là campaign slice có thể chơi đến một trong hai kết thúc, chưa phải bản phát hành hoàn chỉnh. Arc 2–7 chưa được mở rộng đủ nhịp truyện/thời lượng; validator chưa thay thế playtest tay trên điện thoại. Source hiện có 1.001 quest (117 story, 884 side), 360 item (255 trang bị), 211 loài quái và APK 408,721,325 bytes. Còn thiếu 702.660 từ để đạt 1.000.001; thời lượng chơi 24 giờ chưa được đo.

## Thư mục

- `Assets/Scripts` — runtime, điều khiển, giao diện, chiến đấu và lưu offline.
- `Assets/Resources/Art` — hình nền tám vùng chính và ba bản đồ phụ, sprite nhân vật cùng pose chiến đấu hiện có.
- `Assets/Resources/Audio` — soundtrack vùng, sáu ambience stream theo khu vực (dế, đồng hồ, sông, chim, suối và gió), bước chân theo mặt nền, SFX chiến đấu và bốn cue câu cá; nguồn, license và hash nằm trong `Docs/ASSET_SOURCES.md` cùng `Docs/Licenses/`.
- `Assets/Resources/VFX` — bốn hiệu ứng pixel cho cảnh báo tầm đánh, chém, né và nhận thưởng; gói nguồn CC0 và script tái tạo được lưu trong `Docs/ASSET_SOURCES.md`.
- `Assets/Resources/Content` — catalog nhiệm vụ, hội thoại, tư liệu sổ chứng cứ, vật phẩm, monster, encounter, điểm câu cá, farm plot và recipe.
- `Docs` — thiết kế sản phẩm, cốt truyện, kế hoạch phase và kiểm kê nguồn asset.

Trạng thái build/QA và số lượng nội dung thực tế được ghi trong [PHASE_STATUS.md](Docs/PHASE_STATUS.md).

## Tiến độ sản phẩm

Đây là nền tảng và vertical slice đầu, chưa phải bản phát hành hoàn chỉnh. Arc 5 có các tuyến phụ của Tamsin Wren (14 quest) và The First Warden (40 quest); Arc 7 tiếp tục câu chuyện Jace Morrow bằng 15 quest về đoàn khảo sát mất tích. Các tuyến giữ rõ giới hạn của chứng cứ và có kết quả nhánh riêng. Các cổng nội dung cuối được giữ trong [PRODUCT_PLAN.md](Docs/PRODUCT_PLAN.md): ít nhất 8 arc, 24 giờ chơi tuyến chính, hơn 1.000.000 từ nội dung, 200 loại quái, 50 tinh anh, 16 boss, 200 trang bị, 1.000 nhiệm vụ và gói cài Android trên 400 MB. Không dùng file đệm để giả dung lượng hay từ lặp để đạt số từ.

## Asset

Background Crownfall Reach và một số sprite Arc 8 được tạo riêng cho dự án. Các nguồn asset miễn phí và cách sàng lọc license được ghi trong [ASSET_SOURCES.md](Docs/ASSET_SOURCES.md). Mỗi asset bên thứ ba phải có URL, tác giả, license và yêu cầu ghi công trước khi được thêm vào bản phát hành.

Nhạc khám phá dùng “RPG Village Exploration Music” của Hitctrl theo CC-BY 3.0; nhạc combat “Chiptune Battle Music” của pmiller và ba trường âm thanh Park ambiences của Thimras phát hành CC0. Mở nút **CREDITS** trong game để xem ghi công và license; danh sách đầy đủ có trong [sổ asset](Docs/ASSET_SOURCES.md).
