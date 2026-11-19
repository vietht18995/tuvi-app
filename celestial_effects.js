/**
 * ============================================================================
 * CINEMATIC ORIENTAL CELESTIAL REALM — 3D WEBGL EXPERIENCE (THREE.JS r128)
 * Phong cách: ĐÔNG PHƯƠNG HUYỀN HỌC • THIÊN VĂN CỔ ĐÀI (Luxury Oriental Fantasy)
 * ============================================================================
 * Kiến trúc 3 tầng không gian:
 *  - Tầng Nền (Environment): Bầu trời đêm xanh đen (#080D1C), tinh vân tím than (#51486C),
 *    dãy núi tiên cảnh 3D xa chân trời, biển mây thể tích trôi chậm, tia sáng xuyên mây
 *    (God-rays) và hạt bụi vàng lơ lửng.
 *  - Tầng 1 (Celestial Core): Đài Thiên Văn cổ đại lơ lửng + Thiên Cầu Bạch Ngọc (#E8E5D9)
 *    bao quanh bởi hệ vòng Hỗn Thiên Nghi Vàng Cổ (#C9A45C) xoay đa trục.
 *  - Tầng 2 (Four Celestial Guardians): Thanh Long, Phượng Hoàng, Kỳ Lân, Kim Quy 3D
 *    có khớp chuyển động độc lập, quỹ đạo bất đồng bộ, vảy/lông/bờm/mai chi tiết.
 *  - Tầng 3A (12 Con Giáp 3D): 12 tượng điêu khắc Ngọc Bích & Vàng Cổ (Tý -> Hợi)
 *    đặt trên bệ sen bát giác theo quỹ đạo nghiêng có chiều sâu.
 *  - Tầng 3B (Ngũ Hành 3D): 5 thực thể 3D hình khối riêng biệt (Tinh thể Kim, Cây linh mộc,
 *    Thủy cầu gợn sóng, Xoáy lửa Hỏa, Cự thạch Thổ mạch vàng).
 * ============================================================================
 */

(function () {
  "use strict";

  // ==========================================================================
  // 1. ASSET MANIFEST (HỖ TRỢ MÔ HÌNH GLB/GLTF NGOÀI HOẶC PROCEDURAL 3D CAO CẤP)
  // ==========================================================================
  const CELESTIAL_ASSET_MANIFEST = {
    enableExternalGLB: false, // Bật thành true khi đặt file .glb vào thư mục /assets/models/
    basePath: "assets/models/",
    guardians: {
      dragon: "thanh_long_dragon.glb",
      phoenix: "phuong_hoang_phoenix.glb",
      qilin: "ky_lan_qilin.glb",
      turtle: "kim_quy_turtle.glb"
    },
    zodiacs: {
      ty: "zodiac_01_rat.glb",
      suu: "zodiac_02_ox.glb",
      dan: "zodiac_03_tiger.glb",
      mao: "zodiac_04_cat.glb",
      thin: "zodiac_05_dragon.glb",
      ty_snake: "zodiac_06_snake.glb",
      ngo: "zodiac_07_horse.glb",
      mui: "zodiac_08_goat.glb",
      than: "zodiac_09_monkey.glb",
      dau: "zodiac_10_rooster.glb",
      tuat: "zodiac_11_dog.glb",
      hoi: "zodiac_12_boar.glb"
    }
  };
  window.CELESTIAL_ASSET_MANIFEST = CELESTIAL_ASSET_MANIFEST;

  // ==========================================================================
  // 2. BẢNG DỮ LIỆU HUYỀN HỌC (TỨ LINH, 12 ĐỊA CHI, NGŨ HÀNH, THIÊN CẦU)
  // ==========================================================================
  const CORE_METADATA = {
    id: "core_observatory",
    category: "TRUNG TÂM ĐẠI TRẬN • ĐÀI THIÊN VĂN CỔ ĐẠI",
    name: "Thiên Cầu Bạch Ngọc & Hỗn Thiên Nghi",
    hanzi: "璿璣",
    meta: "Trục Bắc Đẩu • Trung Cung Thái Cực • Khởi Nguyên Tinh Bàn",
    lore: "Đài thiên văn cổ đại lơ lửng giữa tầng mây thượng giới. Tâm điểm là Thiên Cầu bằng bạch ngọc phát ánh sáng linh thiêng, bao quanh bởi 5 vòng Hỗn Thiên Nghi bằng vàng cổ khắc 28宿 (Nhị Thập Bát Tú) xoay chậm trên nhiều trục, định vị thời không cho 12 cung số.",
    palaceHint: "Trung Cung (Thái Cực) — Nơi hội tụ nguyên khí của Mệnh Chủ và Thân Chủ trước khi phân bổ 114 tinh đẩu vào 12 cung địa chi."
  };

  const GUARDIAN_LORE = {
    dragon: {
      id: "guardian_dragon",
      key: "dragon",
      category: "TỨ LINH HỘ PHÁP • ĐÔNG PHƯƠNG",
      name: "Thanh Long — Thần Rồng Ngọc Bích",
      hanzi: "青龍",
      meta: "Phương Đông • Hành Mộc • Biểu trưng Sinh Khí & Quyền Uy",
      lore: "Thần Rồng phương Đông thân dài uốn lượn mềm mại với hàng nghìn vảy ngọc lục bảo (#39AFA0) ánh vàng kim (#C9A45C), sừng hươu phân nhánh, bờm dài và mắt sáng ngọc bích. Thanh Long bay lượn theo sóng hình sin quanh đài thiên văn, dẫn dắt long mạch và công danh khoa bảng.",
      branches: ["Dần", "Mão", "Thìn"],
      tuviStars: ["Long Trì", "Thanh Long", "Hóa Quyền", "Thiên Lương"]
    },
    phoenix: {
      id: "guardian_phoenix",
      key: "phoenix",
      category: "TỨ LINH HỘ PHÁP • NAM PHƯƠNG",
      name: "Phượng Hoàng — Chu Tước Bất Tử",
      hanzi: "鳳凰",
      meta: "Phương Nam • Hành Hỏa • Biểu trưng Trí Tuệ, Văn Chương & Minh Triết",
      lore: "Thần điểu phương Nam với đôi cánh lớn nhiều lớp lông vũ vàng kim, đỏ son (#9F393D) và cam hổ phách. Khi chuyển hướng, cơ thể nghiêng uyển chuyển, mép cánh phát sáng linh quang cùng đuôi dài mềm mại kéo theo tàn lửa phượng hoàng, chủ về văn chương, danh vọng và cát khánh.",
      branches: ["Tỵ", "Ngọ", "Mùi"],
      tuviStars: ["Phượng Các", "Hóa Khoa", "Thái Dương", "Văn Xương", "Văn Khúc"]
    },
    qilin: {
      id: "guardian_qilin",
      key: "qilin",
      category: "TỨ LINH HỘ PHÁP • TÂY PHƯƠNG & TRUNG ƯƠNG",
      name: "Kỳ Lân — Nhân Thú Thần Uy",
      hanzi: "麒麟",
      meta: "Phương Tây / Trung Cung • Hành Kim - Thổ • Biểu trưng Phúc Đức & Tài Lộc",
      lore: "Thần thú đầu rồng thân mã, toàn thân phủ giáp vảy ngọc bích pha đồng cổ và vàng ròng, bờm phát sáng xanh ngọc nhạt. Bốn chân có cấu trúc giải phẫu phi nước đại trên dải vân mây, mỗi bước chân hội tụ tường thụy, hóa giải sát khí và hộ trì gia đạo hưng vượng.",
      branches: ["Thân", "Dậu", "Tuất"],
      tuviStars: ["Bạch Hổ", "Hoa Cái", "Hóa Lộc", "Vũ Khúc", "Thiên Phủ"]
    },
    turtle: {
      id: "guardian_turtle",
      key: "turtle",
      category: "TỨ LINH HỘ PHÁP • BẮC PHƯƠNG",
      name: "Kim Quy — Huyền Vũ Cổ Thần",
      hanzi: "玄武",
      meta: "Phương Bắc • Hành Thủy • Biểu trưng Trường Thọ, Huyền Cơ & Phúc Ấm",
      lore: "Rùa thần cổ đại với chiếc mai lớn bằng ngọc đen (#111827) khảm vàng cổ, trên lưng khắc đồ hình Lạc Thư và Bát Quái phát sáng nhẹ cùng linh xà Huyền Vũ quấn quanh. Kim Quy bơi lượn chậm rãi giữa biển mây, trấn giữ hậu vận, thọ nguyên và trí tuệ thâm sâu.",
      branches: ["Hợi", "Tý", "Sửu"],
      tuviStars: ["Thiên Đồng", "Thái Âm", "Thiên Cơ", "Trường Sinh"]
    }
  };

  const ZODIAC_LORE = [
    {
      index: 0, branch: "Tý", name: "Tý • Linh Thử Ngọc Bích", hanzi: "子",
      animalTitle: "Thiên Quý Linh Thử (Chuột Ngọc Ôm Kim Tiền)",
      element: "Thủy", direction: "Chính Bắc", hours: "23:00 – 01:00",
      lore: "Tượng Linh Thử điêu khắc bằng bạch ngọc và vàng cổ trên bệ sen bát giác, hai chân trước nâng đồng kim tiền cổ. Tý là cung khởi đầu của 12 Địa Chi (Nhất Dương Sinh), chủ về sự nhạy bén, mưu lược và nguồn mạch tiên thiên."
    },
    {
      index: 1, branch: "Sửu", name: "Sửu • Kim Ngưu Trấn Địa", hanzi: "丑",
      animalTitle: "Khôn Nguyên Kim Ngưu (Trâu Vàng Cặp Sừng Cung)",
      element: "Thổ", direction: "Đông Bắc Thiên Bắc", hours: "01:00 – 03:00",
      lore: "Tượng Kim Ngưu dáng đứng vững chãi, bắp vai cuồn cuộn, cặp sừng uốn cong bằng vàng cổ. Cung Sửu thuộc hành Thổ (mộ khố của Kim), tượng trưng cho sự kiên định, nhẫn nại, tích lũy hậu sản và điền trạch bền vững."
    },
    {
      index: 2, branch: "Dần", name: "Dần • Sơn Quân Linh Hổ", hanzi: "寅",
      animalTitle: "Thượng Sơn Uy Hổ (Hổ Ngọc Gầm Dương Khí)",
      element: "Mộc", direction: "Đông Bắc Thiên Đông", hours: "03:00 – 05:00",
      lore: "Tượng Linh Hổ ngẩng đầu uy nghiêm trên đài đá ngọc bích, vằn lưng khảm chỉ vàng cổ. Cung Dần là đất Tam Dương Khai Thái — nơi khởi phát mùa xuân, biểu trưng cho quyền bính, khí phách tiên phong và đại cuộc công danh."
    },
    {
      index: 3, branch: "Mão", name: "Mão • Ngọc Miêu Minh Nguyệt", hanzi: "卯",
      animalTitle: "Đông Phương Linh Miêu (Mèo Ngọc Chầu Nhật Nguyệt)",
      element: "Mộc", direction: "Chính Đông", hours: "05:00 – 07:00",
      lore: "Tượng Linh Miêu dáng ngồi thanh tao, đôi tai vểnh cao, đuôi uốn cong mềm mại. Cung Mão là cửa ngõ mặt trời mọc (Chính Đông Mộc vượng), chủ về sự tinh tế, nhân hòa, quý nhân phù trợ và tài hoa nghệ thuật."
    },
    {
      index: 4, branch: "Thìn", name: "Thìn • Thiên Long Thăng Vân", hanzi: "辰",
      animalTitle: "Thần Long Cuộn Ngọc (Rồng Ngọc Giữ Minh Châu)",
      element: "Thổ", direction: "Đông Nam Thiên Đông", hours: "07:00 – 09:00",
      lore: "Tượng Thần Long uốn mình hình chữ S nâng viên ngọc minh châu trên bệ đài Thiên La. Cung Thìn là Thủy khố kiêm vị trí Thiên La, biểu trưng cho chí khí phi phàm, biến hóa khôn lường và uy quyền bậc đế vương."
    },
    {
      index: 5, branch: "Tỵ", name: "Tỵ • Linh Xà Huyền Hỏa", hanzi: "巳",
      animalTitle: "Xích Kim Linh Xà (Rắn Thần Phun Châu)",
      element: "Hỏa", direction: "Đông Nam Thiên Nam", hours: "09:00 – 11:00",
      lore: "Tượng Linh Xà cuộn 3 vòng uyển chuyển, phần cổ bành nhẹ với vảy vàng hồng phát sáng. Cung Tỵ là đất Lục Dương cực thịnh, nơi Hỏa khí bắt đầu bùng lên, chủ về mưu trí thâm trầm, trực giác huyền học và tài vận bất ngờ."
    },
    {
      index: 6, branch: "Ngọ", name: "Ngọ • Thiên Mã Truy Phong", hanzi: "午",
      animalTitle: "Vân Đằng Thiên Mã (Ngựa Thần Tung Vó)",
      element: "Hỏa", direction: "Chính Nam", hours: "11:00 – 13:00",
      lore: "Tượng Thiên Mã tung hai chân trước đầy kiêu hãnh, bờm và đuôi bay ngược như ngọn lửa. Cung Ngọ nằm ở Chính Nam (Ly Hỏa tối vượng), biểu trưng cho danh tiếng lẫy lừng, sự bứt phá vạn dặm và khí thế quang minh chính đại."
    },
    {
      index: 7, branch: "Mùi", name: "Mùi • Tường Dương Hòa Khí", hanzi: "未",
      animalTitle: "Tam Dương Khai Thái (Dê Ngọc Sừng Xoắn Vàng)",
      element: "Thổ", direction: "Tây Nam Thiên Nam", hours: "13:00 – 15:00",
      lore: "Tượng Linh Dương với cặp sừng xoắn ốc tinh xảo và chòm râu dài thanh nhã. Cung Mùi là Mộc khố — đất Hoa Cái và Phúc Đức, tượng trưng cho sự điềm đạm, phúc lộc hậu vận, căn cơ tâm linh và quý nhân nâng đỡ."
    },
    {
      index: 8, branch: "Thân", name: "Thân • Linh Hầu Hiến Thọ", hanzi: "申",
      animalTitle: "Thông Thiên Linh Hầu (Khỉ Ngọc Dâng Đào Tiên)",
      element: "Kim", direction: "Tây Nam Thiên Tây", hours: "15:00 – 17:00",
      lore: "Tượng Linh Hầu trong tư thế linh hoạt, hai tay nâng quả đào tiên bằng vàng ròng. Cung Thân là một trong Tứ Sinh (đất Dịch Mã, Trường Sinh của Thủy), chủ về trí thông minh tuyệt đỉnh, tài ứng biến và giao thương bốn phương."
    },
    {
      index: 9, branch: "Dậu", name: "Dậu • Kim Kê Báo Hiểu", hanzi: "酉",
      animalTitle: "Bình Minh Kim Kê (Gà Vàng Mào Ngọc)",
      element: "Kim", direction: "Chính Tây", hours: "17:00 – 19:00",
      lore: "Tượng Kim Kê ưỡn ngực vươn cổ gáy gọi bình minh, bộ lông đuôi uốn vòm kiêu sa bằng vàng cổ. Cung Dậu ở Chính Tây (Kim khí tinh khiết nhất), biểu trưng cho sự chuẩn xác, lời nói sắc bén, uy tín và vẻ đẹp hoàn mỹ."
    },
    {
      index: 10, branch: "Tuất", name: "Tuất • Thiên Khuyển Hộ Pháp", hanzi: "戌",
      animalTitle: "Trung Nghĩa Thần Khuyển (Chó Ngọc Trấn Địa Võng)",
      element: "Thổ", direction: "Tây Bắc Thiên Tây", hours: "19:00 – 21:00",
      lore: "Tượng Thần Khuyển ngồi canh giữ nghiêm cẩn trên đài Địa Võng, cổ đeo vòng chuông vàng cổ. Cung Tuất là Hỏa khố, chủ về lòng trung nghĩa, trực giác tâm linh, khả năng bảo hộ gia sản và ý chí kiên cường."
    },
    {
      index: 11, branch: "Hợi", name: "Hợi • Kim Trư Phú Quý", hanzi: "亥",
      animalTitle: "Viên Mãn Kim Trư (Heo Ngọc Tụ Bảo)",
      element: "Thủy", direction: "Tây Bắc Thiên Bắc", hours: "21:00 – 23:00",
      lore: "Tượng Kim Trư thân hình tròn đầy phúc hậu đứng trên đĩnh vàng và mây lành. Cung Hợi là đất Thiên Môn (Trường Sinh của Mộc, Thủy khí mênh mông), biểu trưng cho phúc泽 viên mãn, cuộc sống sung túc và lòng bao dung."
    }
  ];

  const ELEMENT_LORE = [
    {
      id: "element_kim",
      key: "Kim",
      name: "Hành Kim • Tinh Thể Bạch Kim Đa Diện",
      hanzi: "金",
      colorHex: "#E8E5D9",
      accentHex: "#C9A45C",
      meta: "Phương Tây • Mùa Thu • Chủ về Nghĩa Khí, Quyết Đoán & Tài Tinh",
      lore: "Thực thể 3D Hành Kim là một cụm tinh thể kim loại bạch kim – vàng trắng đa diện sắc cạnh, phản chiếu ánh sáng thiên cung, bao quanh bởi 3 vòng quỹ đạo kim hoàn mỏng xoay cắt nhau. Trong Tử Vi, hành Kim ứng với Vũ Khúc, Thất Sát, chủ về cương nghị và tài chính.",
      relations: "Thổ sinh Kim • Kim sinh Thủy • Hỏa khắc Kim • Kim khắc Mộc"
    },
    {
      id: "element_moc",
      key: "Mộc",
      name: "Hành Mộc • Cổ Thụ Linh Ngọc Sinh Khí",
      hanzi: "木",
      colorHex: "#39AFA0",
      accentHex: "#6EE7B7",
      meta: "Phương Đông • Mùa Xuân • Chủ về Nhân Từ, Sinh Trưởng & Khoa Bảng",
      lore: "Thực thể 3D Hành Mộc là một cội Linh Thụ thu nhỏ bằng ngọc lục bảo mọc trên đá nổi, thân cây uốn lượn với tán lá ngọc phát quang và các hạt mầm ánh sáng xanh bay lên không trung. Trong Tử Vi, hành Mộc ứng với Thiên Cơ, Thiên Lương, Tham Lang.",
      relations: "Thủy sinh Mộc • Mộc sinh Hỏa • Kim khắc Mộc • Mộc khắc Thổ"
    },
    {
      id: "element_thuy",
      key: "Thủy",
      name: "Hành Thủy • Huyền Thủy Cầu Gợn Sóng",
      hanzi: "水",
      colorHex: "#38BDF8",
      accentHex: "#0284C7",
      meta: "Phương Bắc • Mùa Đông • Chủ về Trí Tuệ, Mềm Mại & Lưu Thông",
      lore: "Thực thể 3D Hành Thủy là một khối cầu nước thần lơ lửng trong suốt có độ khúc xạ sâu, bề mặt gợn sóng liên tục theo hàm điều hòa cùng những giọt linh thủy xoay quanh. Trong Tử Vi, hành Thủy ứng với Thái Âm, Thiên Đồng, Thiên Tướng, Phá Quân.",
      relations: "Kim sinh Thủy • Thủy sinh Mộc • Thổ khắc Thủy • Thủy khắc Hỏa"
    },
    {
      id: "element_hoa",
      key: "Hỏa",
      name: "Hành Hỏa • Chân Hỏa Linh Diễm Đa Tầng",
      hanzi: "火",
      colorHex: "#9F393D",
      accentHex: "#F59E0B",
      meta: "Phương Nam • Mùa Hạ • Chủ về Lễ Nghĩa, Quang Minh & Nhiệt Huyết",
      lore: "Thực thể 3D Hành Hỏa là cấu trúc ngọn lửa thần 7 tầng hình khối xoắn động từ lõi vàng trắng ra hồng liên và đỏ chu sa (#9F393D), liên tục phóng thích các hạt tàn lửa bay lên. Trong Tử Vi, hành Hỏa ứng với Thái Dương, Liêm Trinh, Hỏa Tinh, Linh Tinh.",
      relations: "Mộc sinh Hỏa • Hỏa sinh Thổ • Thủy khắc Hỏa • Hỏa khắc Kim"
    },
    {
      id: "element_tho",
      key: "Thổ",
      name: "Hành Thổ • Cự Thạch Cổ Sơn Mạch Vàng",
      hanzi: "土",
      colorHex: "#C9A45C",
      accentHex: "#D97706",
      meta: "Trung Ương • Tứ Quý • Chủ về Tín Nghĩa, Bao Dung & Điền Sản",
      lore: "Thực thể 3D Hành Thổ là khối cự thạch núi cổ phân tầng lơ lửng, bề mặt khắc mạch quặng vàng phát sáng ấm áp, xung quanh có 6 mảnh đá vệ tinh xoay chậm. Trong Tử Vi, hành Thổ ứng với Tử Vi, Thiên Phủ, Cự Môn, Lộc Tồn.",
      relations: "Hỏa sinh Thổ • Thổ sinh Kim • Mộc khắc Thổ • Thổ khắc Thủy"
    }
  ];

  // ==========================================================================
  // 3. STATE QUẢN LÝ TOÀN CỤC CỦA KHÔNG GIAN 3D
  // ==========================================================================
  let audioCtx = null;
  let masterGain = null;
  let isAudioMuted = false;
  let activeSoundNodes = [];

  let summonTimerId = null;
  let stageTimerIds = [];
  let countdownIntervalId = null;
  let isSummonActive = false;

  // Three.js Core
  let threeRenderer = null;
  let threeScene = null;
  let threeCamera = null;
  let threeAnimFrameId = null;
  let threeStartTime = 0;
  let isPageHidden = false;
  let prefersReducedMotion = false;

  // Scene Groups & Actors
  let envGroup = null;
  let coreObservatoryGroup = null;
  let armillaryRings = [];
  let coreJadeSphere = null;
  let guardiansList = [];
  let zodiacStatuesList = [];
  let fiveElementsList = [];
  let clickableMeshes = [];

  // Interactive Camera & Selection State
  const cameraState = {
    mode: "cinematic_intro", // 'cinematic_intro' | 'overview' | 'core' | 'guardians' | 'zodiac' | 'elements' | 'inspect'
    autoRotate: true,
    isDragging: false,
    dragMoved: false,
    pointerDownX: 0,
    pointerDownY: 0,
    sphericalTheta: 0.25,
    sphericalPhi: 1.18, // radians from Y+
    sphericalRadius: 96,
    targetTheta: 0.25,
    targetPhi: 1.18,
    targetRadius: 96,
    lookAtCurrent: null,
    lookAtTarget: null,
    inspectTargetObj: null,
    inspectOffsetRadius: 22,
    hoveredEntity: null,
    selectedEntity: null,
    activeSubDock: null
  };

  // ==========================================================================
  // 4. HỆ THỐNG ÂM THANH CỔ ĐÀI (WEB AUDIO SYNTHESIS)
  // ==========================================================================
  function initAudio() {
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return null;
      if (!audioCtx) {
        audioCtx = new AudioContextClass();
        masterGain = audioCtx.createGain();
        masterGain.gain.value = isAudioMuted ? 0.0001 : 0.28;
        masterGain.connect(audioCtx.destination);
      }
      if (audioCtx.state === "suspended") {
        audioCtx.resume();
      }
      return audioCtx;
    } catch (e) {
      return null;
    }
  }

  function playRitualSoundscape(durationSec = 10) {
    const ctx = initAudio();
    if (!ctx || !masterGain) return;
    stopAudioNodes();

    const now = ctx.currentTime;
    // Trầm âm Đại Hồng Chung (108Hz, 162Hz, 216Hz, 324Hz)
    const freqs = [108, 162, 216, 324, 432];
    freqs.forEach((f, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = idx % 2 === 0 ? "sine" : "triangle";
      osc.frequency.setValueAtTime(f, now);

      const peak = 0.055 / (idx + 1);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(peak, now + 1.2 + idx * 0.25);
      gain.gain.setValueAtTime(peak * 0.85, now + Math.max(2, durationSec - 1.8));
      gain.gain.exponentialRampToValueAtTime(0.0001, now + durationSec + 2.5);

      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(now);
      osc.stop(now + durationSec + 2.6);
      activeSoundNodes.push(osc);
    });

    playBellStrike(216, 0.14);
  }

  function playBellStrike(baseFreq = 288, volume = 0.12) {
    const ctx = initAudio();
    if (!ctx || !masterGain || isAudioMuted) return;
    const now = ctx.currentTime;
    [1, 1.5, 2.02, 2.98].forEach((ratio, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(baseFreq * ratio, now);

      const amp = volume / (i * 1.4 + 1);
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(amp, now + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.4 / (i * 0.5 + 1));

      osc.connect(gain);
      gain.connect(masterGain);
      osc.start(now);
      osc.stop(now + 2.5);
    });
  }

  function stopAudioNodes() {
    activeSoundNodes.forEach((node) => {
      try {
        node.stop();
        node.disconnect();
      } catch (e) {}
    });
    activeSoundNodes = [];
  }

  window.toggleCelestialAudio = function () {
    isAudioMuted = !isAudioMuted;
    const iconEl = document.getElementById("icon-celestial-audio");
    if (iconEl) iconEl.textContent = isAudioMuted ? "🔇" : "🔊";
    if (masterGain && audioCtx) {
      masterGain.gain.setTargetAtTime(isAudioMuted ? 0.0001 : 0.28, audioCtx.currentTime, 0.1);
    }
  };

  // ==========================================================================
  // 5. PROCEDURAL PBR TEXTURES & ENVIRONMENT MAPS (KHÔNG DÙNG SVG ĐỂ TRÁNH LỖI)
  // ==========================================================================
  let cachedTextures = null;

  function getProceduralTextures(activeThree) {
    if (cachedTextures) return cachedTextures;

    // 1. Equirectangular Reflection Texture cho Vàng Cổ & Ngọc Bích
    const envCanvas = document.createElement("canvas");
    envCanvas.width = 512;
    envCanvas.height = 256;
    const ectx = envCanvas.getContext("2d");
    const envGrad = ectx.createLinearGradient(0, 0, 0, 256);
    envGrad.addColorStop(0.0, "#080D1C");
    envGrad.addColorStop(0.35, "#182246");
    envGrad.addColorStop(0.48, "#51486C");
    envGrad.addColorStop(0.52, "#C9A45C");
    envGrad.addColorStop(0.65, "#1E293B");
    envGrad.addColorStop(1.0, "#060913");
    ectx.fillStyle = envGrad;
    ectx.fillRect(0, 0, 512, 256);
    // Thêm các dải sáng phản chiếu kim loại
    for (let i = 0; i < 18; i++) {
      const x = (i * 97) % 512;
      const y = 60 + ((i * 53) % 130);
      const r = 18 + (i % 4) * 14;
      const rg = ectx.createRadialGradient(x, y, 1, x, y, r);
      rg.addColorStop(0, "rgba(255, 240, 200, 0.55)");
      rg.addColorStop(1, "rgba(255, 240, 200, 0)");
      ectx.fillStyle = rg;
      ectx.beginPath();
      ectx.arc(x, y, r, 0, Math.PI * 2);
      ectx.fill();
    }
    const envMap = new activeThree.CanvasTexture(envCanvas);
    envMap.mapping = activeThree.EquirectangularReflectionMapping;

    // 2. Bump Map Vảy Rồng / Điêu Khắc Ngọc Cổ
    const scaleCanvas = document.createElement("canvas");
    scaleCanvas.width = 256;
    scaleCanvas.height = 256;
    const sctx = scaleCanvas.getContext("2d");
    sctx.fillStyle = "#404040";
    sctx.fillRect(0, 0, 256, 256);
    const rows = 10;
    const cols = 10;
    const cw = 256 / cols;
    const ch = 256 / rows;
    for (let r = -1; r <= rows; r++) {
      for (let c = -1; c <= cols; c++) {
        const cx = c * cw + (r % 2 === 0 ? cw * 0.5 : 0);
        const cy = r * ch;
        const g = sctx.createRadialGradient(cx, cy, 1, cx, cy, cw * 0.65);
        g.addColorStop(0, "#ffffff");
        g.addColorStop(0.65, "#909090");
        g.addColorStop(0.92, "#202020");
        g.addColorStop(1, "#101010");
        sctx.fillStyle = g;
        sctx.beginPath();
        sctx.arc(cx, cy, cw * 0.62, 0, Math.PI * 2);
        sctx.fill();
      }
    }
    const scaleBumpMap = new activeThree.CanvasTexture(scaleCanvas);
    scaleBumpMap.wrapS = activeThree.RepeatWrapping;
    scaleBumpMap.wrapT = activeThree.RepeatWrapping;
    scaleBumpMap.repeat.set(4, 2);

    // 3. Soft Cloud / Mist Particle Texture
    const cloudCanvas = document.createElement("canvas");
    cloudCanvas.width = 256;
    cloudCanvas.height = 256;
    const cctx = cloudCanvas.getContext("2d");
    const cg = cctx.createRadialGradient(128, 128, 8, 128, 128, 124);
    cg.addColorStop(0, "rgba(232, 229, 217, 0.65)");
    cg.addColorStop(0.35, "rgba(148, 163, 184, 0.32)");
    cg.addColorStop(0.7, "rgba(81, 72, 108, 0.12)");
    cg.addColorStop(1, "rgba(8, 13, 28, 0)");
    cctx.fillStyle = cg;
    cctx.fillRect(0, 0, 256, 256);
    const cloudTex = new activeThree.CanvasTexture(cloudCanvas);

    // 4. Soft Golden Glow Dot Texture (cho hạt bụi vàng & tàn lửa)
    const glowCanvas = document.createElement("canvas");
    glowCanvas.width = 64;
    glowCanvas.height = 64;
    const gctx = glowCanvas.getContext("2d");
    const gg = gctx.createRadialGradient(32, 32, 1, 32, 32, 30);
    gg.addColorStop(0, "rgba(255, 250, 230, 1)");
    gg.addColorStop(0.35, "rgba(201, 164, 92, 0.75)");
    gg.addColorStop(0.75, "rgba(201, 164, 92, 0.18)");
    gg.addColorStop(1, "rgba(201, 164, 92, 0)");
    gctx.fillStyle = gg;
    gctx.fillRect(0, 0, 64, 64);
    const glowTex = new activeThree.CanvasTexture(glowCanvas);

    // 5. Hoa văn Mai Rùa Lạc Thư / Bát Quái phát sáng nhẹ
    const shellCanvas = document.createElement("canvas");
    shellCanvas.width = 512;
    shellCanvas.height = 512;
    const shctx = shellCanvas.getContext("2d");
    shctx.fillStyle = "#0f172a";
    shctx.fillRect(0, 0, 512, 512);
    shctx.strokeStyle = "#C9A45C";
    shctx.lineWidth = 4;
    // Lục giác trung tâm & 8 cung
    for (let ring = 1; ring <= 3; ring++) {
      const rad = ring * 68;
      shctx.beginPath();
      for (let k = 0; k <= 8; k++) {
        const a = (k / 8) * Math.PI * 2;
        const px = 256 + Math.cos(a) * rad;
        const py = 256 + Math.sin(a) * rad;
        if (k === 0) shctx.moveTo(px, py);
        else shctx.lineTo(px, py);
      }
      shctx.stroke();
    }
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * Math.PI * 2;
      shctx.beginPath();
      shctx.moveTo(256 + Math.cos(a) * 35, 256 + Math.sin(a) * 35);
      shctx.lineTo(256 + Math.cos(a) * 210, 256 + Math.sin(a) * 210);
      shctx.stroke();
    }
    const shellTex = new activeThree.CanvasTexture(shellCanvas);

    cachedTextures = { envMap, scaleBumpMap, cloudTex, glowTex, shellTex };
    return cachedTextures;
  }

  // ==========================================================================
  // 6. PHẦN 1 — TÁI THIẾT KẾ TOÀN BỘ BỐ CỤC KHÔNG GIAN 3D (ENVIRONMENT)
  // ==========================================================================
  function buildCelestialEnvironment(activeThree, scene, textures) {
    const group = new activeThree.Group();
    group.name = "CelestialEnvironment";

    // 1.1 Bầu trời đêm xanh đen sâu thẳm (#080D1C) + Tinh vân tím than (#51486C)
    const skyCanvas = document.createElement("canvas");
    skyCanvas.width = 1024;
    skyCanvas.height = 512;
    const sctx = skyCanvas.getContext("2d");
    const skyGrad = sctx.createLinearGradient(0, 0, 0, 512);
    skyGrad.addColorStop(0.0, "#040711");
    skyGrad.addColorStop(0.28, "#080D1C");
    skyGrad.addColorStop(0.54, "#151934");
    skyGrad.addColorStop(0.72, "#2E294E"); // Mystic Violet nebula band
    skyGrad.addColorStop(0.88, "#111A2E");
    skyGrad.addColorStop(1.0, "#050811");
    sctx.fillStyle = skyGrad;
    sctx.fillRect(0, 0, 1024, 512);

    // Dải tinh vân tím than & lam ngọc rất nhẹ
    for (let i = 0; i < 12; i++) {
      const nx = (i * 173) % 1024;
      const ny = 140 + ((i * 67) % 180);
      const nr = 90 + (i % 4) * 45;
      const ng = sctx.createRadialGradient(nx, ny, 5, nx, ny, nr);
      ng.addColorStop(0, i % 2 === 0 ? "rgba(81, 72, 108, 0.28)" : "rgba(57, 175, 160, 0.12)");
      ng.addColorStop(1, "rgba(8, 13, 28, 0)");
      sctx.fillStyle = ng;
      sctx.beginPath();
      sctx.arc(nx, ny, nr, 0, Math.PI * 2);
      sctx.fill();
    }

    const skyTex = new activeThree.CanvasTexture(skyCanvas);
    const skyGeo = new activeThree.SphereGeometry(380, 40, 28);
    const skyMat = new activeThree.MeshBasicMaterial({
      map: skyTex,
      side: activeThree.BackSide,
      depthWrite: false
    });
    const skyDome = new activeThree.Mesh(skyGeo, skyMat);
    group.add(skyDome);

    // 1.2 Những ngọn núi tiên cảnh 3D xa phía chân trời (Immortal Horizon Peaks)
    const mountainGroup = new activeThree.Group();
    const peakCount = 28;
    const mountainMatBack = new activeThree.MeshStandardMaterial({
      color: 0x0b1326,
      roughness: 0.92,
      metalness: 0.08,
      flatShading: true
    });
    const mountainMatFront = new activeThree.MeshStandardMaterial({
      color: 0x131d36,
      emissive: 0x1e1b38,
      emissiveIntensity: 0.18,
      roughness: 0.85,
      metalness: 0.15,
      flatShading: true
    });

    for (let i = 0; i < peakCount; i++) {
      const angle = (i / peakCount) * Math.PI * 2 + (i % 2) * 0.04;
      const dist = 245 + (i % 3) * 28;
      const height = 42 + ((i * 19) % 58);
      const radius = 22 + ((i * 13) % 24);

      const coneGeo = new activeThree.ConeGeometry(radius, height, 7, 3);
      // Biến dạng nhẹ đỉnh núi để tạo dáng núi đá tiên cảnh phương Đông
      const pos = coneGeo.attributes.position;
      for (let v = 0; v < pos.count; v++) {
        const vx = pos.getX(v);
        const vy = pos.getY(v);
        const vz = pos.getZ(v);
        const ridge = Math.sin(vx * 0.15 + i) * 2.4;
        pos.setX(v, vx + ridge);
        pos.setZ(v, vz + Math.cos(vy * 0.1 + i) * 2.0);
      }
      coneGeo.computeVertexNormals();

      const peak = new activeThree.Mesh(coneGeo, i % 2 === 0 ? mountainMatBack : mountainMatFront);
      peak.position.set(
        Math.cos(angle) * dist,
        -24 + height * 0.35,
        Math.sin(angle) * dist
      );
      peak.rotation.y = angle + i;
      mountainGroup.add(peak);
    }
    group.add(mountainGroup);

    // 1.3 Biển mây thể tích trôi chậm phía dưới (Volumetric Cloud Sea Layers)
    const cloudLayers = [];
    const cloudPlaneGeo = new activeThree.PlaneGeometry(95, 95);
    for (let i = 0; i < 34; i++) {
      const cMat = new activeThree.MeshBasicMaterial({
        map: textures.cloudTex,
        transparent: true,
        opacity: 0.16 + (i % 4) * 0.04,
        depthWrite: false,
        blending: activeThree.NormalBlending
      });
      const cloudMesh = new activeThree.Mesh(cloudPlaneGeo, cMat);
      const radius = 18 + ((i * 29) % 165);
      const angle = (i / 34) * Math.PI * 2;
      cloudMesh.position.set(
        Math.cos(angle) * radius,
        -13.5 + (i % 5) * 1.9,
        Math.sin(angle) * radius
      );
      cloudMesh.rotation.x = -Math.PI / 2;
      cloudMesh.rotation.z = angle;
      const scale = 0.85 + (i % 5) * 0.32;
      cloudMesh.scale.set(scale, scale, 1);
      group.add(cloudMesh);
      cloudLayers.push({
        mesh: cloudMesh,
        baseAngle: angle,
        radius,
        speed: 0.012 + (i % 4) * 0.004,
        rotSpeed: (i % 2 === 0 ? 1 : -1) * 0.02
      });
    }

    // 1.4 Những tia sáng xuyên qua mây có chiều sâu (Celestial God-Rays)
    const godRaysGroup = new activeThree.Group();
    const rayGeo = new activeThree.CylinderGeometry(1.5, 16, 135, 16, 1, true);
    for (let i = 0; i < 6; i++) {
      const rayMat = new activeThree.MeshBasicMaterial({
        color: i % 2 === 0 ? 0xc9a45c : 0x39afa0,
        transparent: true,
        opacity: 0.042,
        side: activeThree.DoubleSide,
        depthWrite: false,
        blending: activeThree.AdditiveBlending
      });
      const ray = new activeThree.Mesh(rayGeo, rayMat);
      const a = (i / 6) * Math.PI * 2 + 0.4;
      const r = 42 + (i % 2) * 22;
      ray.position.set(Math.cos(a) * r, 38, Math.sin(a) * r);
      ray.rotation.z = 0.22;
      ray.rotation.x = -0.15;
      godRaysGroup.add(ray);
    }
    group.add(godRaysGroup);

    // 1.5 Hạt bụi vàng phát sáng lơ lửng trong không khí (Atmospheric Gold Dust)
    const dustCount = 420;
    const dustGeo = new activeThree.BufferGeometry();
    const dustPositions = new Float32Array(dustCount * 3);
    const dustPhases = new Float32Array(dustCount);
    for (let i = 0; i < dustCount; i++) {
      const r = 10 + Math.random() * 135;
      const theta = Math.random() * Math.PI * 2;
      const y = -10 + Math.random() * 68;
      dustPositions[i * 3] = Math.cos(theta) * r;
      dustPositions[i * 3 + 1] = y;
      dustPositions[i * 3 + 2] = Math.sin(theta) * r;
      dustPhases[i] = Math.random() * Math.PI * 2;
    }
    dustGeo.setAttribute("position", new activeThree.BufferAttribute(dustPositions, 3));
    const dustMat = new activeThree.PointsMaterial({
      color: 0xe8d096,
      map: textures.glowTex,
      size: 1.35,
      transparent: true,
      opacity: 0.68,
      depthWrite: false,
      blending: activeThree.AdditiveBlending
    });
    const dustPoints = new activeThree.Points(dustGeo, dustMat);
    group.add(dustPoints);

    scene.add(group);
    return {
      group,
      cloudLayers,
      godRaysGroup,
      dustPoints,
      dustPositions,
      dustPhases
    };
  }

  // ==========================================================================
  // 7. TẦNG TRUNG TÂM — CELESTIAL CORE (ĐÀI THIÊN VĂN & THIÊN CẦU BẠCH NGỌC)
  // ==========================================================================
  function buildCelestialCoreObservatory(activeThree, scene, textures) {
    const coreGroup = new activeThree.Group();
    coreGroup.name = "CelestialCoreObservatory";
    coreGroup.position.set(0, 6, 0);

    const antiqueGoldMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x3a280b,
      emissiveIntensity: 0.24,
      metalness: 0.88,
      roughness: 0.22,
      envMap: textures.envMap,
      envMapIntensity: 1.35
    });

    const darkObsidianJadeMat = new activeThree.MeshStandardMaterial({
      color: 0x121b2e,
      emissive: 0x0b1528,
      emissiveIntensity: 0.2,
      metalness: 0.35,
      roughness: 0.28,
      bumpMap: textures.scaleBumpMap,
      bumpScale: 0.08,
      envMap: textures.envMap
    });

    const emeraldAccentMat = new activeThree.MeshStandardMaterial({
      color: 0x39afa0,
      emissive: 0x11423b,
      emissiveIntensity: 0.4,
      metalness: 0.25,
      roughness: 0.2,
      envMap: textures.envMap
    });

    // 7.1 Bệ Đài Thiên Văn Bát Giác Cổ Đại Lơ Lửng (Floating Octagonal Dais)
    const daisGroup = new activeThree.Group();
    const tier1Geo = new activeThree.CylinderGeometry(13.5, 15.2, 1.8, 8);
    const tier1 = new activeThree.Mesh(tier1Geo, darkObsidianJadeMat);
    tier1.position.y = -4.2;
    daisGroup.add(tier1);

    const tier1RimGeo = new activeThree.TorusGeometry(14.5, 0.28, 12, 8);
    const tier1Rim = new activeThree.Mesh(tier1RimGeo, antiqueGoldMat);
    tier1Rim.rotation.x = Math.PI / 2;
    tier1Rim.position.y = -3.35;
    daisGroup.add(tier1Rim);

    const tier2Geo = new activeThree.CylinderGeometry(9.8, 11.4, 1.5, 8);
    const tier2 = new activeThree.Mesh(tier2Geo, darkObsidianJadeMat);
    tier2.position.y = -2.4;
    daisGroup.add(tier2);

    // Đế chóp đá lơ lửng phía dưới đài (Inverted Floating Spire)
    const underSpireGeo = new activeThree.ConeGeometry(9.5, 9.0, 8);
    const underSpire = new activeThree.Mesh(underSpireGeo, darkObsidianJadeMat);
    underSpire.rotation.x = Math.PI;
    underSpire.position.y = -9.5;
    daisGroup.add(underSpire);

    // 8 Cột Trụ Ngọc & Vàng Cổ xung quanh Đài Thiên Văn
    const pillarGeo = new activeThree.CylinderGeometry(0.36, 0.44, 4.2, 12);
    const finialGeo = new activeThree.SphereGeometry(0.55, 14, 14);
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2 + Math.PI / 8;
      const r = 11.8;
      const pillar = new activeThree.Mesh(pillarGeo, antiqueGoldMat);
      pillar.position.set(Math.cos(a) * r, -1.3, Math.sin(a) * r);
      daisGroup.add(pillar);

      const finial = new activeThree.Mesh(finialGeo, emeraldAccentMat);
      finial.position.set(Math.cos(a) * r, 1.0, Math.sin(a) * r);
      daisGroup.add(finial);
    }

    coreGroup.add(daisGroup);

    // 7.2 Trung Tâm: Thiên Cầu Bằng Bạch Ngọc (#E8E5D9) Phát Ánh Sáng Dịu Linh Thiêng
    const sphereCenterY = 7.5;
    const whiteJadeMat = new activeThree.MeshStandardMaterial({
      color: 0xe8e5d9,
      emissive: 0xd6ceb8,
      emissiveIntensity: 0.38,
      metalness: 0.12,
      roughness: 0.16,
      bumpMap: textures.scaleBumpMap,
      bumpScale: 0.04,
      envMap: textures.envMap,
      envMapIntensity: 1.2
    });
    const jadeSphereGeo = new activeThree.SphereGeometry(4.2, 48, 48);
    const jadeSphere = new activeThree.Mesh(jadeSphereGeo, whiteJadeMat);
    jadeSphere.position.y = sphereCenterY;
    jadeSphere.userData = {
      entityType: "core",
      entityData: CORE_METADATA
    };
    coreGroup.add(jadeSphere);
    clickableMeshes.push(jadeSphere);

    // Lớp Hào Quang Ngọc Nội Tại (Soft Inner Aura Shell)
    const auraGeo = new activeThree.SphereGeometry(4.85, 32, 32);
    const auraMat = new activeThree.MeshBasicMaterial({
      color: 0xe8e5d9,
      transparent: true,
      opacity: 0.16,
      side: activeThree.BackSide,
      blending: activeThree.AdditiveBlending,
      depthWrite: false
    });
    const auraMesh = new activeThree.Mesh(auraGeo, auraMat);
    jadeSphere.add(auraMesh);

    // 7.3 Hệ Vòng Thiên Văn Hỗn Thiên Nghi Vàng Cổ Xoay Đa Trục (Multi-Axis Armillary Rings)
    const rings = [];
    const ringConfigs = [
      { radius: 6.2, tube: 0.22, rotX: 0.35, rotY: 0.0, speedX: 0.22, speedY: 0.35, speedZ: 0.08 },
      { radius: 7.6, tube: 0.26, rotX: -0.62, rotY: 0.4, speedX: -0.18, speedY: 0.24, speedZ: -0.15 },
      { radius: 9.1, tube: 0.30, rotX: 1.05, rotY: -0.3, speedX: 0.12, speedY: -0.28, speedZ: 0.20 },
      { radius: 10.8, tube: 0.24, rotX: 0.18, rotY: 0.8, speedX: -0.09, speedY: 0.16, speedZ: -0.12 },
      { radius: 12.6, tube: 0.34, rotX: 1.57, rotY: 0.0, speedX: 0.0, speedY: 0.10, speedZ: 0.04 }
    ];

    ringConfigs.forEach((cfg, idx) => {
      const ringHolder = new activeThree.Group();
      ringHolder.position.y = sphereCenterY;
      ringHolder.rotation.set(cfg.rotX, cfg.rotY, 0);

      const torusGeo = new activeThree.TorusGeometry(cfg.radius, cfg.tube, 18, 96);
      const torusMesh = new activeThree.Mesh(torusGeo, antiqueGoldMat);
      torusMesh.userData = {
        entityType: "core",
        entityData: CORE_METADATA
      };
      ringHolder.add(torusMesh);
      clickableMeshes.push(torusMesh);

      // Các vạch khắc độ thiên văn & hạt châu ngọc trên mỗi vòng Hỗn Thiên Nghi
      const notchCount = 12 + idx * 4;
      const notchGeo = new activeThree.BoxGeometry(cfg.tube * 2.4, cfg.tube * 0.9, cfg.tube * 3.0);
      for (let n = 0; n < notchCount; n++) {
        const na = (n / notchCount) * Math.PI * 2;
        const notch = new activeThree.Mesh(notchGeo, n % 3 === 0 ? emeraldAccentMat : antiqueGoldMat);
        notch.position.set(Math.cos(na) * cfg.radius, Math.sin(na) * cfg.radius, 0);
        notch.rotation.z = na;
        ringHolder.add(notch);
      }

      coreGroup.add(ringHolder);
      rings.push({ group: ringHolder, cfg });
    });

    // Trục đỡ Long Trụ nối từ Bệ Đài lên Vòng Thiên Văn ngoài cùng
    const supportGeo = new activeThree.CylinderGeometry(0.45, 0.72, 6.2, 16);
    const supportPillar = new activeThree.Mesh(supportGeo, antiqueGoldMat);
    supportPillar.position.y = 0.8;
    coreGroup.add(supportPillar);

    scene.add(coreGroup);
    return {
      coreGroup,
      jadeSphere,
      auraMesh,
      rings,
      daisGroup
    };
  }

  // ==========================================================================
  // 8. PHẦN 2 — THIẾT KẾ 4 THẦN THÚ 3D (THANH LONG, PHƯỢNG HOÀNG, KỲ LÂN, KIM QUY)
  // ==========================================================================

  // 8.1 THANH LONG — THẦN RỒNG PHƯƠNG ĐÔNG (48 đốt thân uốn sóng, sừng phân nhánh, râu dài, 4 chân 4 móng)
  function buildDragon3D(activeThree, textures) {
    const root = new activeThree.Group();
    root.name = "Guardian_ThanhLong";

    const emeraldScaleMat = new activeThree.MeshStandardMaterial({
      color: 0x2c9e8f,
      emissive: 0x0c3b35,
      emissiveIntensity: 0.35,
      metalness: 0.38,
      roughness: 0.24,
      bumpMap: textures.scaleBumpMap,
      bumpScale: 0.16,
      envMap: textures.envMap,
      envMapIntensity: 1.25
    });

    const goldBellyMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x422d0b,
      emissiveIntensity: 0.3,
      metalness: 0.85,
      roughness: 0.22,
      envMap: textures.envMap
    });

    const eyeGlowMat = new activeThree.MeshBasicMaterial({ color: 0x6ee7b7 });

    // Đầu Rồng Uy Nghi (Head Group)
    const headGroup = new activeThree.Group();
    const skull = new activeThree.Mesh(new activeThree.BoxGeometry(2.2, 1.55, 2.7), emeraldScaleMat);
    headGroup.add(skull);

    const upperSnout = new activeThree.Mesh(new activeThree.BoxGeometry(1.75, 0.82, 2.4), emeraldScaleMat);
    upperSnout.position.set(0, -0.1, 2.2);
    headGroup.add(upperSnout);

    const lowerJaw = new activeThree.Mesh(new activeThree.BoxGeometry(1.5, 0.45, 2.1), goldBellyMat);
    lowerJaw.position.set(0, -0.72, 2.0);
    lowerJaw.rotation.x = 0.18;
    headGroup.add(lowerJaw);

    // Mắt phát sáng màu ngọc bích & gờ mày vàng
    [-0.95, 0.95].forEach((sideX) => {
      const eye = new activeThree.Mesh(new activeThree.SphereGeometry(0.28, 14, 14), eyeGlowMat);
      eye.position.set(sideX, 0.32, 0.95);
      headGroup.add(eye);

      const brow = new activeThree.Mesh(new activeThree.BoxGeometry(0.55, 0.22, 1.1), goldBellyMat);
      brow.position.set(sideX * 1.02, 0.65, 0.95);
      brow.rotation.z = sideX > 0 ? -0.3 : 0.3;
      headGroup.add(brow);
    });

    // Sừng hươu phân nhánh (Branching Stag Antlers)
    [-0.68, 0.68].forEach((sideX) => {
      const antlerGroup = new activeThree.Group();
      antlerGroup.position.set(sideX, 0.78, -0.35);
      const mainBeam = new activeThree.Mesh(new activeThree.CylinderGeometry(0.10, 0.22, 3.4, 10), goldBellyMat);
      mainBeam.rotation.x = -0.68;
      mainBeam.rotation.z = sideX > 0 ? -0.28 : 0.28;
      mainBeam.position.set(sideX * 0.4, 1.2, -1.0);
      antlerGroup.add(mainBeam);

      const tine1 = new activeThree.Mesh(new activeThree.ConeGeometry(0.12, 1.4, 8), goldBellyMat);
      tine1.position.set(sideX * 0.5, 1.1, -0.4);
      tine1.rotation.x = -0.3;
      antlerGroup.add(tine1);

      const tine2 = new activeThree.Mesh(new activeThree.ConeGeometry(0.10, 1.6, 8), goldBellyMat);
      tine2.position.set(sideX * 0.8, 1.9, -1.4);
      tine2.rotation.x = -0.85;
      antlerGroup.add(tine2);

      headGroup.add(antlerGroup);
    });

    // Râu rồng dài uốn lượn (Flowing Whiskers)
    const whiskers = [];
    [-0.78, 0.78].forEach((sideX) => {
      const wGroup = new activeThree.Group();
      wGroup.position.set(sideX, -0.15, 2.95);
      for (let w = 0; w < 6; w++) {
        const seg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.05, 0.07, 0.85, 8), goldBellyMat);
        seg.position.set(sideX * (w * 0.22), -w * 0.25, -w * 0.45);
        seg.rotation.z = sideX > 0 ? -0.4 : 0.4;
        seg.rotation.x = 0.5;
        wGroup.add(seg);
      }
      headGroup.add(wGroup);
      whiskers.push(wGroup);
    });

    root.add(headGroup);

    // 44 Đốt Thân Uốn Lượn Mềm Mại + Vây Lưng Vàng + 4 Chân Vuốt Sắc Nét
    const segments = [];
    const segCount = 44;
    const legIndices = [8, 10, 24, 26]; // 2 chân trước, 2 chân sau

    for (let i = 0; i < segCount; i++) {
      const t = i / (segCount - 1);
      // Độ dày thân rồng thon dần về đuôi
      const radius = i < 4
        ? 0.95 + (i / 4) * 0.32
        : 1.28 * Math.pow(1 - (t - 0.08) / 0.92, 0.65) + 0.16;

      const segGroup = new activeThree.Group();
      const bodyGeo = new activeThree.SphereGeometry(radius, 16, 14);
      bodyGeo.scale(1.0, 0.92, 1.38);
      const bodyMesh = new activeThree.Mesh(bodyGeo, emeraldScaleMat);
      segGroup.add(bodyMesh);
      clickableMeshes.push(bodyMesh);
      bodyMesh.userData = { entityType: "guardian", entityData: GUARDIAN_LORE.dragon };

      // Giáp bụng vàng kim
      const bellyGeo = new activeThree.BoxGeometry(radius * 1.15, radius * 0.42, radius * 1.45);
      const bellyMesh = new activeThree.Mesh(bellyGeo, goldBellyMat);
      bellyMesh.position.y = -radius * 0.72;
      segGroup.add(bellyMesh);

      // Vây lưng vàng cổ & bờm ngọc dọc sống lưng
      if (i % 2 === 0 && i < segCount - 3) {
        const finHeight = radius * 1.35;
        const finGeo = new activeThree.ConeGeometry(radius * 0.26, finHeight, 5);
        const finMesh = new activeThree.Mesh(finGeo, goldBellyMat);
        finMesh.position.y = radius * 1.05;
        finMesh.rotation.x = -0.42;
        segGroup.add(finMesh);
      }

      // 4 Chân Rồng với Móng Vuốt Sắc Nét
      if (legIndices.includes(i)) {
        const isRight = i === 8 || i === 24;
        const side = isRight ? 1 : -1;
        const legGroup = new activeThree.Group();
        legGroup.position.set(side * radius * 0.85, -radius * 0.35, 0);

        const upperLeg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.38, 0.28, 1.8, 10), emeraldScaleMat);
        upperLeg.position.set(side * 0.55, -0.7, 0.2);
        upperLeg.rotation.z = side * 0.48;
        legGroup.add(upperLeg);

        const lowerLeg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.26, 0.20, 1.5, 10), emeraldScaleMat);
        lowerLeg.position.set(side * 0.95, -1.75, 0.55);
        lowerLeg.rotation.x = 0.35;
        legGroup.add(lowerLeg);

        // 4 móng vuốt vàng
        for (let c = -1.5; c <= 1.5; c += 1) {
          const claw = new activeThree.Mesh(new activeThree.ConeGeometry(0.09, 0.65, 6), goldBellyMat);
          claw.position.set(side * 0.95 + c * 0.18, -2.35, 1.05);
          claw.rotation.x = Math.PI * 0.42;
          legGroup.add(claw);
        }
        segGroup.add(legGroup);
      }

      // Quạt đuôi rồng ở đốt cuối
      if (i === segCount - 1) {
        for (let f = -2; f <= 2; f++) {
          const plume = new activeThree.Mesh(new activeThree.ConeGeometry(0.18, 2.6, 6), goldBellyMat);
          plume.position.set(f * 0.22, f * 0.08, -1.2);
          plume.rotation.x = -Math.PI * 0.48;
          plume.rotation.y = f * 0.18;
          segGroup.add(plume);
        }
      }

      root.add(segGroup);
      segments.push(segGroup);
    }

    headGroup.traverse((child) => {
      if (child.isMesh) {
        child.userData = { entityType: "guardian", entityData: GUARDIAN_LORE.dragon };
        clickableMeshes.push(child);
      }
    });

    return {
      type: "dragon",
      root,
      headGroup,
      segments,
      whiskers,
      entityData: GUARDIAN_LORE.dragon
    };
  }

  // 8.2 PHƯỢNG HOÀNG — IMMORTAL PHOENIX (Cánh nhiều lớp lông vũ riêng biệt, đuôi dài mềm mại + hạt tàn lửa)
  function buildPhoenix3D(activeThree, textures) {
    const root = new activeThree.Group();
    root.name = "Guardian_PhuongHoang";

    const crimsonMat = new activeThree.MeshStandardMaterial({
      color: 0x9f393d,
      emissive: 0x541115,
      emissiveIntensity: 0.45,
      metalness: 0.35,
      roughness: 0.28,
      envMap: textures.envMap
    });

    const goldFeatherMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x6b440b,
      emissiveIntensity: 0.42,
      metalness: 0.85,
      roughness: 0.2,
      envMap: textures.envMap
    });

    const amberRimMat = new activeThree.MeshStandardMaterial({
      color: 0xf59e0b,
      emissive: 0xd97706,
      emissiveIntensity: 0.72,
      metalness: 0.5,
      roughness: 0.22
    });

    const bodyRig = new activeThree.Group();
    root.add(bodyRig);

    // Thân Phượng Hoàng khí động học
    const torsoGeo = new activeThree.SphereGeometry(1.45, 24, 20);
    torsoGeo.scale(0.88, 0.82, 2.15);
    const torso = new activeThree.Mesh(torsoGeo, crimsonMat);
    bodyRig.add(torso);

    const breastPlate = new activeThree.Mesh(new activeThree.SphereGeometry(1.22, 18, 16), goldFeatherMat);
    breastPlate.scale.set(0.82, 0.72, 1.4);
    breastPlate.position.set(0, -0.22, 0.95);
    bodyRig.add(breastPlate);

    // Cổ uốn cong chữ S, Đầu & Mỏ Vàng, Mào 5 nhánh
    const neck = new activeThree.Mesh(new activeThree.CylinderGeometry(0.42, 0.68, 2.4, 14), goldFeatherMat);
    neck.position.set(0, 1.15, 2.35);
    neck.rotation.x = 0.55;
    bodyRig.add(neck);

    const head = new activeThree.Mesh(new activeThree.SphereGeometry(0.62, 18, 16), crimsonMat);
    head.scale.set(0.9, 0.95, 1.25);
    head.position.set(0, 2.05, 3.15);
    bodyRig.add(head);

    const beak = new activeThree.Mesh(new activeThree.ConeGeometry(0.26, 1.15, 8), goldFeatherMat);
    beak.rotation.x = Math.PI * 0.46;
    beak.position.set(0, 1.98, 4.05);
    bodyRig.add(beak);

    // Mào Phượng Hoàng 5 lông vũ vương miện
    for (let c = -2; c <= 2; c++) {
      const crest = new activeThree.Mesh(new activeThree.ConeGeometry(0.09, 1.85 - Math.abs(c) * 0.2, 6), amberRimMat);
      crest.position.set(c * 0.16, 2.65, 2.55 - Math.abs(c) * 0.12);
      crest.rotation.x = -0.68;
      crest.rotation.z = -c * 0.16;
      bodyRig.add(crest);
    }

    // Đôi Cánh Lớn 3 Khớp với 28 Lông Vũ Riêng Biệt mỗi bên
    const wings = [];
    [-1, 1].forEach((side) => {
      const shoulderPivot = new activeThree.Group();
      shoulderPivot.position.set(side * 1.05, 0.35, 0.65);

      const innerBone = new activeThree.Mesh(new activeThree.BoxGeometry(3.4, 0.26, 1.15), goldFeatherMat);
      innerBone.position.set(side * 1.7, 0, 0.15);
      shoulderPivot.add(innerBone);

      // Lớp lông vũ trong (Primary & Secondary Layered Feathers)
      for (let f = 0; f < 14; f++) {
        const featherLen = 2.6 + (f / 14) * 1.8;
        const featherGeo = new activeThree.BoxGeometry(0.32, 0.06, featherLen);
        const mat = f % 3 === 0 ? goldFeatherMat : f % 3 === 1 ? crimsonMat : amberRimMat;
        const feather = new activeThree.Mesh(featherGeo, mat);
        feather.position.set(side * (0.45 + f * 0.24), -0.05 - (f % 2) * 0.04, -featherLen * 0.45);
        feather.rotation.y = side * (-0.08 - f * 0.025);
        shoulderPivot.add(feather);
      }

      // Khớp cánh ngoài (Outer Wing Tip)
      const outerPivot = new activeThree.Group();
      outerPivot.position.set(side * 3.35, 0, 0.2);

      const outerBone = new activeThree.Mesh(new activeThree.BoxGeometry(3.8, 0.20, 0.85), amberRimMat);
      outerBone.position.set(side * 1.9, 0, 0);
      outerPivot.add(outerBone);

      for (let f = 0; f < 14; f++) {
        const featherLen = 4.2 - f * 0.18;
        const featherGeo = new activeThree.BoxGeometry(0.28, 0.05, featherLen);
        const mat = f > 9 ? amberRimMat : f % 2 === 0 ? goldFeatherMat : crimsonMat;
        const feather = new activeThree.Mesh(featherGeo, mat);
        feather.position.set(side * (0.25 + f * 0.26), 0, -featherLen * 0.45);
        feather.rotation.y = side * (-0.22 - f * 0.045);
        outerPivot.add(feather);
      }

      shoulderPivot.add(outerPivot);
      bodyRig.add(shoulderPivot);
      wings.push({ side, shoulderPivot, outerPivot });
    });

    // 5 Dải Đuôi Phượng Hoàng Dài Mềm Mại Uốn Theo Luồng Khí
    const tailRibbons = [];
    for (let r = -2; r <= 2; r++) {
      const nodes = [];
      for (let n = 0; n < 12; n++) {
        const w = 0.42 * (1 - n / 15) + 0.08;
        const segGeo = new activeThree.BoxGeometry(w, 0.05, 0.95);
        const segMat = n > 8 ? amberRimMat : r % 2 === 0 ? goldFeatherMat : crimsonMat;
        const seg = new activeThree.Mesh(segGeo, segMat);
        root.add(seg);
        nodes.push(seg);
      }
      tailRibbons.push({ offsetIndex: r, nodes });
    }

    // Hạt tàn lửa nhỏ bay sau đuôi (Trailing Fire Embers)
    const emberCount = 36;
    const emberGeo = new activeThree.BufferGeometry();
    const emberPositions = new Float32Array(emberCount * 3);
    for (let i = 0; i < emberCount; i++) {
      emberPositions[i * 3] = (Math.random() - 0.5) * 3;
      emberPositions[i * 3 + 1] = (Math.random() - 0.5) * 2;
      emberPositions[i * 3 + 2] = -3 - Math.random() * 10;
    }
    emberGeo.setAttribute("position", new activeThree.BufferAttribute(emberPositions, 3));
    const emberMat = new activeThree.PointsMaterial({
      color: 0xfbbf24,
      map: textures.glowTex,
      size: 1.15,
      transparent: true,
      opacity: 0.85,
      depthWrite: false,
      blending: activeThree.AdditiveBlending
    });
    const emberPoints = new activeThree.Points(emberGeo, emberMat);
    bodyRig.add(emberPoints);

    root.traverse((child) => {
      if (child.isMesh) {
        child.userData = { entityType: "guardian", entityData: GUARDIAN_LORE.phoenix };
        clickableMeshes.push(child);
      }
    });

    return {
      type: "phoenix",
      root,
      bodyRig,
      wings,
      tailRibbons,
      emberPoints,
      emberPositions,
      entityData: GUARDIAN_LORE.phoenix
    };
  }

  // 8.3 KỲ LÂN — DIVINE QILIN (Đầu rồng, thân thú vảy ngọc & đồng cổ, bờm xanh ngọc phát sáng, 4 chân khớp phi nước đại)
  function buildQilin3D(activeThree, textures) {
    const root = new activeThree.Group();
    root.name = "Guardian_KyLan";

    const jadeArmorMat = new activeThree.MeshStandardMaterial({
      color: 0x2b8a7e,
      emissive: 0x0f3832,
      emissiveIntensity: 0.32,
      metalness: 0.42,
      roughness: 0.25,
      bumpMap: textures.scaleBumpMap,
      bumpScale: 0.14,
      envMap: textures.envMap
    });

    const antiqueBronzeGoldMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x3d280a,
      emissiveIntensity: 0.28,
      metalness: 0.86,
      roughness: 0.22,
      envMap: textures.envMap
    });

    const luminousManeMat = new activeThree.MeshStandardMaterial({
      color: 0x6ee7b7,
      emissive: 0x39afa0,
      emissiveIntensity: 0.65,
      metalness: 0.2,
      roughness: 0.25
    });

    const bodyRig = new activeThree.Group();
    root.add(bodyRig);

    // Thân Kỳ Lân cơ bắp (Chest, Ribcage, Haunches)
    const chest = new activeThree.Mesh(new activeThree.SphereGeometry(1.45, 22, 18), jadeArmorMat);
    chest.scale.set(0.95, 1.05, 1.25);
    chest.position.set(0, 0.25, 1.35);
    bodyRig.add(chest);

    const torso = new activeThree.Mesh(new activeThree.CylinderGeometry(1.18, 1.32, 3.2, 18), jadeArmorMat);
    torso.rotation.x = Math.PI / 2;
    torso.position.set(0, 0.25, -0.1);
    bodyRig.add(torso);

    const haunch = new activeThree.Mesh(new activeThree.SphereGeometry(1.35, 20, 18), jadeArmorMat);
    haunch.scale.set(0.92, 1.02, 1.2);
    haunch.position.set(0, 0.3, -1.75);
    bodyRig.add(haunch);

    // Giáp vai & giáp hông bằng Vàng Cổ
    const shoulderArmor = new activeThree.Mesh(new activeThree.BoxGeometry(2.85, 0.9, 1.5), antiqueBronzeGoldMat);
    shoulderArmor.position.set(0, 0.45, 1.45);
    bodyRig.add(shoulderArmor);

    // Cổ & Đầu Rồng Kỳ Lân + Sừng Ngọc Độc Giác + Bờm Xanh Ngọc Phát Sáng
    const neck = new activeThree.Mesh(new activeThree.CylinderGeometry(0.68, 1.05, 2.3, 14), jadeArmorMat);
    neck.position.set(0, 1.45, 2.15);
    neck.rotation.x = 0.42;
    bodyRig.add(neck);

    const head = new activeThree.Mesh(new activeThree.BoxGeometry(1.45, 1.25, 2.2), antiqueBronzeGoldMat);
    head.position.set(0, 2.45, 2.95);
    bodyRig.add(head);

    const snout = new activeThree.Mesh(new activeThree.BoxGeometry(1.1, 0.72, 1.35), jadeArmorMat);
    snout.position.set(0, 2.22, 4.15);
    bodyRig.add(snout);

    // Sừng Kỳ Lân phát sáng
    const horn = new activeThree.Mesh(new activeThree.ConeGeometry(0.24, 2.2, 8), luminousManeMat);
    horn.position.set(0, 3.55, 2.35);
    horn.rotation.x = -0.58;
    bodyRig.add(horn);

    // Bờm phát sáng màu xanh ngọc nhạt dọc cổ và lưng
    for (let m = 0; m < 9; m++) {
      const plume = new activeThree.Mesh(new activeThree.ConeGeometry(0.24, 1.55, 6), luminousManeMat);
      plume.position.set(0, 2.6 - m * 0.22, 2.1 - m * 0.42);
      plume.rotation.x = -0.82;
      bodyRig.add(plume);
    }

    // 4 Chân Giải Phẫu 2 Khớp (Upper Leg + Lower Leg + Golden Hoof) + Dải Mây Linh Khí dưới chân
    const legs = [];
    const legConfigs = [
      { name: "FL", x: -0.95, z: 1.55, phase: 0.0 },
      { name: "FR", x: 0.95, z: 1.55, phase: Math.PI * 0.65 },
      { name: "BL", x: -0.92, z: -1.65, phase: Math.PI },
      { name: "BR", x: 0.92, z: -1.65, phase: Math.PI * 1.65 }
    ];

    legConfigs.forEach((lc) => {
      const hipPivot = new activeThree.Group();
      hipPivot.position.set(lc.x, -0.25, lc.z);

      const thigh = new activeThree.Mesh(new activeThree.CylinderGeometry(0.42, 0.30, 1.85, 12), jadeArmorMat);
      thigh.position.y = -0.85;
      hipPivot.add(thigh);

      const kneePivot = new activeThree.Group();
      kneePivot.position.y = -1.75;

      const shin = new activeThree.Mesh(new activeThree.CylinderGeometry(0.28, 0.22, 1.75, 12), antiqueBronzeGoldMat);
      shin.position.y = -0.85;
      kneePivot.add(shin);

      const hoof = new activeThree.Mesh(new activeThree.CylinderGeometry(0.32, 0.38, 0.42, 12), luminousManeMat);
      hoof.position.y = -1.75;
      kneePivot.add(hoof);

      hipPivot.add(kneePivot);
      bodyRig.add(hipPivot);
      legs.push({ hipPivot, kneePivot, phase: lc.phase });
    });

    // Đuôi Kỳ Lân dạng ngọn lửa ngọc bích
    const tailPivot = new activeThree.Group();
    tailPivot.position.set(0, 0.55, -2.75);
    for (let t = -1; t <= 1; t++) {
      const tPlume = new activeThree.Mesh(new activeThree.ConeGeometry(0.32, 2.8, 7), t === 0 ? luminousManeMat : antiqueBronzeGoldMat);
      tPlume.position.set(t * 0.28, 0.35, -1.2);
      tPlume.rotation.x = -1.15;
      tPlume.rotation.z = -t * 0.2;
      tailPivot.add(tPlume);
    }
    bodyRig.add(tailPivot);

    // Dải mây linh khí nâng bước chân Kỳ Lân
    const cloudRibbonGeo = new activeThree.TorusGeometry(2.6, 0.22, 10, 36, Math.PI * 1.4);
    const cloudRibbonMat = new activeThree.MeshBasicMaterial({
      color: 0x39afa0,
      transparent: true,
      opacity: 0.38,
      blending: activeThree.AdditiveBlending,
      depthWrite: false
    });
    const cloudRibbon = new activeThree.Mesh(cloudRibbonGeo, cloudRibbonMat);
    cloudRibbon.rotation.x = Math.PI / 2;
    cloudRibbon.position.set(0, -3.5, -0.4);
    bodyRig.add(cloudRibbon);

    root.traverse((child) => {
      if (child.isMesh) {
        child.userData = { entityType: "guardian", entityData: GUARDIAN_LORE.qilin };
        clickableMeshes.push(child);
      }
    });

    return {
      type: "qilin",
      root,
      bodyRig,
      legs,
      tailPivot,
      cloudRibbon,
      entityData: GUARDIAN_LORE.qilin
    };
  }

  // 8.4 KIM QUY — CELESTIAL TURTLE (Mai lớn ngọc đen pha vàng cổ, ký tự Lạc Thư phát sáng nhẹ, đầu & 4 chân bơi lượn)
  function buildTurtle3D(activeThree, textures) {
    const root = new activeThree.Group();
    root.name = "Guardian_KimQuy";

    const obsidianShellMat = new activeThree.MeshStandardMaterial({
      color: 0x162032,
      emissive: 0xc9a45c,
      emissiveMap: textures.shellTex,
      emissiveIntensity: 0.52,
      metalness: 0.55,
      roughness: 0.26,
      bumpMap: textures.shellTex,
      bumpScale: 0.18,
      envMap: textures.envMap
    });

    const antiqueGoldMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x3d280a,
      emissiveIntensity: 0.28,
      metalness: 0.88,
      roughness: 0.22,
      envMap: textures.envMap
    });

    const darkJadeSkinMat = new activeThree.MeshStandardMaterial({
      color: 0x1e3a3a,
      emissive: 0x091e1e,
      emissiveIntensity: 0.25,
      metalness: 0.3,
      roughness: 0.35,
      bumpMap: textures.scaleBumpMap,
      bumpScale: 0.12
    });

    const bodyRig = new activeThree.Group();
    root.add(bodyRig);

    // Mai Rùa Cổ Đại Vòm Lớn (Domed Carapace)
    const domeGeo = new activeThree.SphereGeometry(3.6, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.55);
    domeGeo.scale(1.0, 0.68, 1.24);
    const carapace = new activeThree.Mesh(domeGeo, obsidianShellMat);
    carapace.position.y = -0.2;
    bodyRig.add(carapace);

    // Viền Mai Khảm Vàng Cổ (Golden Carapace Rim)
    const rimGeo = new activeThree.TorusGeometry(3.55, 0.28, 14, 48);
    rimGeo.scale(1.0, 1.24, 0.7);
    const rimMesh = new activeThree.Mesh(rimGeo, antiqueGoldMat);
    rimMesh.rotation.x = Math.PI / 2;
    rimMesh.position.y = -0.15;
    bodyRig.add(rimMesh);

    // Yếm Rùa bằng Vàng Cổ (Golden Plastron)
    const plastronGeo = new activeThree.CylinderGeometry(2.9, 2.5, 0.55, 16);
    plastronGeo.scale(1.0, 1.0, 1.22);
    const plastron = new activeThree.Mesh(plastronGeo, antiqueGoldMat);
    plastron.position.y = -0.52;
    bodyRig.add(plastron);

    // Linh Xà Huyền Vũ bằng vàng quấn quanh mai rùa
    const serpentPts = [];
    for (let s = 0; s <= 32; s++) {
      const u = s / 32;
      const ang = u * Math.PI * 2.5;
      const r = 3.2 - u * 1.4;
      serpentPts.push(new activeThree.Vector3(
        Math.cos(ang) * r,
        0.35 + u * 2.1 + Math.sin(u * Math.PI * 4) * 0.15,
        Math.sin(ang) * (r * 1.18)
      ));
    }
    const serpentCurve = new activeThree.CatmullRomCurve3(serpentPts);
    const serpentGeo = new activeThree.TubeGeometry(serpentCurve, 48, 0.22, 10, false);
    const serpentMesh = new activeThree.Mesh(serpentGeo, antiqueGoldMat);
    bodyRig.add(serpentMesh);

    // Cổ & Đầu Rùa Thần Cổ Kính (Articulated Neck & Head)
    const headPivot = new activeThree.Group();
    headPivot.position.set(0, -0.1, 4.1);
    const neck = new activeThree.Mesh(new activeThree.CylinderGeometry(0.58, 0.78, 1.6, 14), darkJadeSkinMat);
    neck.rotation.x = Math.PI * 0.38;
    neck.position.set(0, 0.15, 0.65);
    headPivot.add(neck);

    const head = new activeThree.Mesh(new activeThree.BoxGeometry(1.25, 0.95, 1.65), darkJadeSkinMat);
    head.position.set(0, 0.42, 1.55);
    headPivot.add(head);

    const crownRidge = new activeThree.Mesh(new activeThree.ConeGeometry(0.28, 0.9, 6), antiqueGoldMat);
    crownRidge.position.set(0, 1.0, 1.35);
    crownRidge.rotation.x = -0.5;
    headPivot.add(crownRidge);
    bodyRig.add(headPivot);

    // 4 Chân Bơi Lượn Giữa Tầng Mây (4 Articulated Swimming Flippers)
    const flippers = [];
    const flipperConfigs = [
      { x: -2.9, z: 2.3, side: -1, front: true },
      { x: 2.9, z: 2.3, side: 1, front: true },
      { x: -2.6, z: -2.4, side: -1, front: false },
      { x: 2.6, z: -2.4, side: 1, front: false }
    ];

    flipperConfigs.forEach((fc) => {
      const fPivot = new activeThree.Group();
      fPivot.position.set(fc.x, -0.35, fc.z);
      const flipperGeo = new activeThree.BoxGeometry(fc.front ? 2.4 : 1.85, 0.32, fc.front ? 1.15 : 0.95);
      const flipperMesh = new activeThree.Mesh(flipperGeo, darkJadeSkinMat);
      flipperMesh.position.set(fc.side * (fc.front ? 1.1 : 0.85), -0.1, 0);
      fPivot.add(flipperMesh);
      bodyRig.add(fPivot);
      flippers.push({ fPivot, side: fc.side, front: fc.front });
    });

    root.traverse((child) => {
      if (child.isMesh) {
        child.userData = { entityType: "guardian", entityData: GUARDIAN_LORE.turtle };
        clickableMeshes.push(child);
      }
    });

    return {
      type: "turtle",
      root,
      bodyRig,
      headPivot,
      flippers,
      entityData: GUARDIAN_LORE.turtle
    };
  }

  function buildFourGuardians(activeThree, scene, textures) {
    const dragon = buildDragon3D(activeThree, textures);
    const phoenix = buildPhoenix3D(activeThree, textures);
    const qilin = buildQilin3D(activeThree, textures);
    const turtle = buildTurtle3D(activeThree, textures);

    scene.add(dragon.root);
    scene.add(phoenix.root);
    scene.add(qilin.root);
    scene.add(turtle.root);

    return [dragon, phoenix, qilin, turtle];
  }

  // ==========================================================================
  // 9. PHẦN 3 — 12 CON GIÁP 3D (ANCIENT CELESTIAL JADE SCULPTURES)
  // Tượng điêu khắc bằng Ngọc Bích & Vàng Cổ đặt trên bệ sen nổi tinh xảo
  // ==========================================================================
  function buildZodiacJadeSculptureMesh(activeThree, idx, jadeMat, goldMat, highlightJadeMat) {
    const bodyGroup = new activeThree.Group();
    const headPivot = new activeThree.Group();
    const tailPivot = new activeThree.Group();

    switch (idx) {
      case 0: {
        // 0. TÝ — Linh Thử Ôm Kim Tiền (Crouching Jade Rat holding an Antique Gold Coin)
        const torso = new activeThree.Mesh(new activeThree.SphereGeometry(0.92, 18, 16), jadeMat);
        torso.scale.set(0.86, 1.08, 1.15);
        torso.position.set(0, 0.95, -0.1);
        bodyGroup.add(torso);

        headPivot.position.set(0, 1.65, 0.55);
        const head = new activeThree.Mesh(new activeThree.ConeGeometry(0.58, 1.1, 14), jadeMat);
        head.rotation.x = Math.PI * 0.44;
        head.position.set(0, 0, 0.35);
        headPivot.add(head);

        [-0.45, 0.45].forEach((sx) => {
          const ear = new activeThree.Mesh(new activeThree.CylinderGeometry(0.36, 0.36, 0.1, 14), goldMat);
          ear.rotation.x = Math.PI * 0.35;
          ear.rotation.z = sx * -0.35;
          ear.position.set(sx, 0.38, -0.05);
          headPivot.add(ear);
        });

        // Đồng Kim Tiền cổ trước ngực
        const coin = new activeThree.Mesh(new activeThree.TorusGeometry(0.45, 0.12, 10, 20), goldMat);
        coin.position.set(0, 1.05, 0.85);
        bodyGroup.add(coin);

        tailPivot.position.set(0, 0.45, -0.95);
        const tail = new activeThree.Mesh(new activeThree.TorusGeometry(0.65, 0.08, 8, 20, Math.PI * 1.15), goldMat);
        tail.rotation.y = Math.PI / 2;
        tailPivot.add(tail);
        break;
      }

      case 1: {
        // 1. SỬU — Kim Ngưu Trấn Địa (Muscular Jade & Gold Bull with Crescent Horns)
        const torso = new activeThree.Mesh(new activeThree.BoxGeometry(1.45, 1.18, 2.15), jadeMat);
        torso.position.set(0, 1.18, 0);
        bodyGroup.add(torso);

        const hump = new activeThree.Mesh(new activeThree.SphereGeometry(0.75, 16, 14), goldMat);
        hump.scale.set(0.95, 0.82, 1.1);
        hump.position.set(0, 1.72, 0.55);
        bodyGroup.add(hump);

        headPivot.position.set(0, 1.42, 1.25);
        const head = new activeThree.Mesh(new activeThree.BoxGeometry(0.95, 0.88, 1.15), jadeMat);
        head.position.set(0, -0.05, 0.35);
        headPivot.add(head);

        // Cặp sừng trâu uốn cong bằng vàng
        [-0.55, 0.55].forEach((sx) => {
          const horn = new activeThree.Mesh(new activeThree.TorusGeometry(0.58, 0.12, 10, 18, Math.PI * 0.85), goldMat);
          horn.position.set(sx, 0.35, 0.25);
          horn.rotation.z = sx > 0 ? -0.35 : Math.PI + 0.35;
          headPivot.add(horn);
        });

        // 4 chân trụ vững chãi
        [-0.48, 0.48].forEach((lx) => {
          [-0.72, 0.72].forEach((lz) => {
            const leg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.24, 0.20, 0.95, 10), goldMat);
            leg.position.set(lx, 0.48, lz);
            bodyGroup.add(leg);
          });
        });

        tailPivot.position.set(0, 1.25, -1.1);
        const tail = new activeThree.Mesh(new activeThree.CylinderGeometry(0.08, 0.14, 1.0, 8), goldMat);
        tail.position.set(0, -0.4, -0.2);
        tail.rotation.x = -0.35;
        tailPivot.add(tail);
        break;
      }

      case 2: {
        // 2. DẦN — Sơn Quân Linh Hổ (Prowling Royal Tiger with Golden Stripes)
        const chest = new activeThree.Mesh(new activeThree.SphereGeometry(0.88, 18, 16), jadeMat);
        chest.scale.set(0.95, 1.05, 1.2);
        chest.position.set(0, 1.32, 0.55);
        bodyGroup.add(chest);

        const abdomen = new activeThree.Mesh(new activeThree.CylinderGeometry(0.68, 0.78, 1.55, 14), jadeMat);
        abdomen.rotation.x = Math.PI * 0.42;
        abdomen.position.set(0, 1.12, -0.25);
        bodyGroup.add(abdomen);

        // Vằn hổ bằng vàng cổ
        for (let s = -1; s <= 1; s++) {
          const stripe = new activeThree.Mesh(new activeThree.TorusGeometry(0.76, 0.06, 8, 18, Math.PI * 1.1), goldMat);
          stripe.position.set(0, 1.18, s * 0.38);
          stripe.rotation.y = Math.PI / 2;
          bodyGroup.add(stripe);
        }

        headPivot.position.set(0, 1.88, 1.05);
        const head = new activeThree.Mesh(new activeThree.SphereGeometry(0.68, 16, 14), jadeMat);
        headPivot.add(head);
        const muzzle = new activeThree.Mesh(new activeThree.BoxGeometry(0.68, 0.48, 0.65), goldMat);
        muzzle.position.set(0, -0.12, 0.52);
        headPivot.add(muzzle);

        [-0.45, 0.45].forEach((lx) => {
          [-0.68, 0.68].forEach((lz) => {
            const leg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.22, 0.18, 1.05, 10), jadeMat);
            leg.position.set(lx, 0.52, lz);
            bodyGroup.add(leg);
          });
        });

        tailPivot.position.set(0, 1.08, -1.05);
        const tail = new activeThree.Mesh(new activeThree.TorusGeometry(0.75, 0.11, 8, 18, Math.PI * 0.9), goldMat);
        tail.rotation.y = Math.PI / 2;
        tail.position.set(0, 0.45, -0.45);
        tailPivot.add(tail);
        break;
      }

      case 3: {
        // 3. MÃO — Ngọc Miêu Minh Nguyệt (Graceful Seated Jade Cat with Long Ears)
        const body = new activeThree.Mesh(new activeThree.ConeGeometry(0.86, 1.75, 16), jadeMat);
        body.position.set(0, 0.92, -0.05);
        bodyGroup.add(body);

        const collar = new activeThree.Mesh(new activeThree.TorusGeometry(0.55, 0.09, 10, 20), goldMat);
        collar.rotation.x = Math.PI / 2;
        collar.position.set(0, 1.55, 0.1);
        bodyGroup.add(collar);

        headPivot.position.set(0, 1.92, 0.18);
        const head = new activeThree.Mesh(new activeThree.SphereGeometry(0.62, 16, 14), jadeMat);
        headPivot.add(head);

        [-0.32, 0.32].forEach((sx) => {
          const ear = new activeThree.Mesh(new activeThree.ConeGeometry(0.22, 0.78, 10), goldMat);
          ear.position.set(sx, 0.65, -0.05);
          ear.rotation.z = sx * -0.22;
          headPivot.add(ear);
        });

        tailPivot.position.set(0.35, 0.45, -0.65);
        const tail = new activeThree.Mesh(new activeThree.TorusGeometry(0.68, 0.10, 8, 20, Math.PI * 1.15), goldMat);
        tail.rotation.x = Math.PI * 0.32;
        tailPivot.add(tail);
        break;
      }

      case 4: {
        // 4. THÌN — Thiên Long Thăng Vân (Coiled Jade Dragon Statue holding a Golden Pearl)
        const coilPts = [];
        for (let i = 0; i <= 24; i++) {
          const u = i / 24;
          const a = u * Math.PI * 2.8;
          const r = 0.95 * (1 - u * 0.42);
          coilPts.push(new activeThree.Vector3(Math.cos(a) * r, 0.35 + u * 1.95, Math.sin(a) * r));
        }
        const curve = new activeThree.CatmullRomCurve3(coilPts);
        const bodyTube = new activeThree.Mesh(new activeThree.TubeGeometry(curve, 36, 0.28, 12, false), jadeMat);
        bodyGroup.add(bodyTube);

        // Ngọc Minh Châu lơ lửng
        const pearl = new activeThree.Mesh(new activeThree.SphereGeometry(0.36, 16, 16), goldMat);
        pearl.position.set(0, 1.55, 0.75);
        bodyGroup.add(pearl);

        headPivot.position.set(0, 2.35, 0.25);
        const dHead = new activeThree.Mesh(new activeThree.BoxGeometry(0.68, 0.52, 0.95), goldMat);
        headPivot.add(dHead);
        [-0.22, 0.22].forEach((sx) => {
          const horn = new activeThree.Mesh(new activeThree.ConeGeometry(0.08, 0.65, 8), jadeMat);
          horn.position.set(sx, 0.45, -0.25);
          horn.rotation.x = -0.5;
          headPivot.add(horn);
        });
        break;
      }

      case 5: {
        // 5. TỴ — Linh Xà Huyền Hỏa (Coiled Sacred Serpent with Flared Golden Hood)
        const snakePts = [];
        for (let i = 0; i <= 28; i++) {
          const u = i / 28;
          const a = u * Math.PI * 4.2;
          const r = u < 0.7 ? 0.95 - u * 0.55 : 0.25;
          const y = u < 0.7 ? 0.25 + u * 1.15 : 1.05 + (u - 0.7) * 3.2;
          snakePts.push(new activeThree.Vector3(Math.cos(a) * r, y, Math.sin(a) * r));
        }
        const sCurve = new activeThree.CatmullRomCurve3(snakePts);
        const sTube = new activeThree.Mesh(new activeThree.TubeGeometry(sCurve, 40, 0.24, 12, false), jadeMat);
        bodyGroup.add(sTube);

        headPivot.position.set(0, 2.05, 0.15);
        // Phần cổ bành Linh Xà bằng vàng cổ
        const hood = new activeThree.Mesh(new activeThree.CylinderGeometry(0.62, 0.32, 0.75, 14), goldMat);
        hood.scale.set(1.15, 1.0, 0.35);
        headPivot.add(hood);

        const sHead = new activeThree.Mesh(new activeThree.ConeGeometry(0.32, 0.75, 10), jadeMat);
        sHead.rotation.x = Math.PI * 0.46;
        sHead.position.set(0, 0.35, 0.25);
        headPivot.add(sHead);
        break;
      }

      case 6: {
        // 6. NGỌ — Thiên Mã Truy Phong (Rearing Celestial Steed with Flowing Golden Mane)
        const body = new activeThree.Mesh(new activeThree.CylinderGeometry(0.56, 0.66, 1.85, 14), jadeMat);
        body.rotation.x = -0.62;
        body.position.set(0, 1.45, 0.1);
        bodyGroup.add(body);

        headPivot.position.set(0, 2.38, 0.68);
        const neck = new activeThree.Mesh(new activeThree.CylinderGeometry(0.34, 0.48, 0.95, 12), jadeMat);
        neck.rotation.x = 0.25;
        headPivot.add(neck);

        const hHead = new activeThree.Mesh(new activeThree.BoxGeometry(0.48, 0.48, 0.95), jadeMat);
        hHead.position.set(0, 0.45, 0.32);
        hHead.rotation.x = 0.35;
        headPivot.add(hHead);

        const mane = new activeThree.Mesh(new activeThree.BoxGeometry(0.16, 1.15, 0.38), goldMat);
        mane.position.set(0, 0.2, -0.25);
        headPivot.add(mane);

        // 2 chân sau trụ + 2 chân trước tung vó
        [-0.38, 0.38].forEach((sx) => {
          const backLeg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.18, 0.15, 1.15, 10), goldMat);
          backLeg.position.set(sx, 0.55, -0.45);
          bodyGroup.add(backLeg);

          const frontLeg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.16, 0.13, 1.05, 10), goldMat);
          frontLeg.position.set(sx, 1.75, 0.85);
          frontLeg.rotation.x = 0.78;
          bodyGroup.add(frontLeg);
        });

        tailPivot.position.set(0, 0.88, -0.65);
        const tail = new activeThree.Mesh(new activeThree.ConeGeometry(0.28, 1.25, 10), goldMat);
        tail.rotation.x = -2.2;
        tail.position.set(0, -0.25, -0.45);
        tailPivot.add(tail);
        break;
      }

      case 7: {
        // 7. MÙI — Tường Dương Hòa Khí (Auspicious Jade Ram with Spiral Golden Horns)
        const torso = new activeThree.Mesh(new activeThree.CylinderGeometry(0.62, 0.68, 1.65, 14), jadeMat);
        torso.rotation.x = Math.PI / 2;
        torso.position.set(0, 1.15, 0);
        bodyGroup.add(torso);

        headPivot.position.set(0, 1.85, 0.78);
        const head = new activeThree.Mesh(new activeThree.ConeGeometry(0.46, 0.98, 12), jadeMat);
        head.rotation.x = Math.PI * 0.42;
        headPivot.add(head);

        const beard = new activeThree.Mesh(new activeThree.ConeGeometry(0.18, 0.65, 8), goldMat);
        beard.rotation.x = Math.PI;
        beard.position.set(0, -0.42, 0.32);
        headPivot.add(beard);

        [-0.42, 0.42].forEach((sx) => {
          const horn = new activeThree.Mesh(new activeThree.TorusGeometry(0.38, 0.11, 10, 20, Math.PI * 1.45), goldMat);
          horn.rotation.y = Math.PI / 2;
          horn.position.set(sx, 0.18, -0.15);
          headPivot.add(horn);
        });

        [-0.36, 0.36].forEach((lx) => {
          [-0.58, 0.58].forEach((lz) => {
            const leg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.16, 0.13, 0.95, 10), goldMat);
            leg.position.set(lx, 0.48, lz);
            bodyGroup.add(leg);
          });
        });
        break;
      }

      case 8: {
        // 8. THÂN — Linh Hầu Hiến Thọ (Immortal Monkey offering a Golden Longevity Peach)
        const torso = new activeThree.Mesh(new activeThree.SphereGeometry(0.75, 16, 14), jadeMat);
        torso.scale.set(0.88, 1.22, 0.85);
        torso.position.set(0, 1.18, 0);
        bodyGroup.add(torso);

        headPivot.position.set(0, 2.08, 0.12);
        const head = new activeThree.Mesh(new activeThree.SphereGeometry(0.54, 16, 14), jadeMat);
        headPivot.add(head);

        const headband = new activeThree.Mesh(new activeThree.TorusGeometry(0.52, 0.07, 8, 20), goldMat);
        headband.rotation.x = Math.PI / 2;
        headband.position.y = 0.18;
        headPivot.add(headband);

        // Trái Đào Tiên bằng vàng ròng nâng trước ngực
        const peach = new activeThree.Mesh(new activeThree.SphereGeometry(0.42, 16, 14), goldMat);
        peach.scale.set(1.0, 1.12, 0.95);
        peach.position.set(0, 1.45, 0.72);
        bodyGroup.add(peach);

        tailPivot.position.set(0, 0.55, -0.62);
        const tail = new activeThree.Mesh(new activeThree.TorusGeometry(0.65, 0.08, 8, 20, Math.PI * 1.25), goldMat);
        tail.rotation.y = Math.PI / 2;
        tail.position.set(0, 0.55, -0.35);
        tailPivot.add(tail);
        break;
      }

      case 9: {
        // 9. DẬU — Kim Kê Báo Hiểu (Proud Golden-Crested Rooster with Arching Tail Plumes)
        const body = new activeThree.Mesh(new activeThree.SphereGeometry(0.82, 18, 16), jadeMat);
        body.scale.set(0.82, 1.05, 1.25);
        body.position.set(0, 1.15, 0.1);
        bodyGroup.add(body);

        headPivot.position.set(0, 1.98, 0.65);
        const neck = new activeThree.Mesh(new activeThree.ConeGeometry(0.45, 0.95, 14), goldMat);
        headPivot.add(neck);

        const comb = new activeThree.Mesh(new activeThree.BoxGeometry(0.16, 0.48, 0.58), goldMat);
        comb.position.set(0, 0.58, 0.08);
        headPivot.add(comb);

        const beak = new activeThree.Mesh(new activeThree.ConeGeometry(0.16, 0.48, 8), goldMat);
        beak.rotation.x = Math.PI * 0.45;
        beak.position.set(0, 0.25, 0.42);
        headPivot.add(beak);

        tailPivot.position.set(0, 1.35, -0.68);
        for (let p = -1; p <= 1; p++) {
          const arch = new activeThree.Mesh(new activeThree.TorusGeometry(0.75 + Math.abs(p) * 0.12, 0.10, 8, 20, Math.PI * 1.05), goldMat);
          arch.rotation.y = Math.PI / 2 + p * 0.18;
          arch.position.set(p * 0.14, 0.35, -0.35);
          tailPivot.add(arch);
        }
        break;
      }

      case 10: {
        // 10. TUẤT — Thiên Khuyển Hộ Pháp (Seated Guardian Hound with Golden Collar Bell)
        const chest = new activeThree.Mesh(new activeThree.CylinderGeometry(0.55, 0.72, 1.55, 14), jadeMat);
        chest.rotation.x = -0.25;
        chest.position.set(0, 1.08, 0.12);
        bodyGroup.add(chest);

        const collar = new activeThree.Mesh(new activeThree.TorusGeometry(0.56, 0.09, 10, 20), goldMat);
        collar.rotation.x = Math.PI * 0.42;
        collar.position.set(0, 1.68, 0.28);
        bodyGroup.add(collar);

        headPivot.position.set(0, 2.02, 0.38);
        const head = new activeThree.Mesh(new activeThree.BoxGeometry(0.72, 0.68, 0.78), jadeMat);
        headPivot.add(head);
        const snout = new activeThree.Mesh(new activeThree.BoxGeometry(0.46, 0.38, 0.58), goldMat);
        snout.position.set(0, -0.1, 0.58);
        headPivot.add(snout);

        [-0.28, 0.28].forEach((sx) => {
          const ear = new activeThree.Mesh(new activeThree.ConeGeometry(0.18, 0.55, 8), goldMat);
          ear.position.set(sx, 0.52, -0.1);
          headPivot.add(ear);
        });

        tailPivot.position.set(0, 0.65, -0.68);
        const tail = new activeThree.Mesh(new activeThree.ConeGeometry(0.18, 0.95, 8), goldMat);
        tail.rotation.x = -0.58;
        tail.position.set(0, 0.38, -0.25);
        tailPivot.add(tail);
        break;
      }

      default: {
        // 11. HỢI — Kim Trư Phú Quý (Prosperous Jade & Gold Boar atop Golden Ingots)
        const torso = new activeThree.Mesh(new activeThree.SphereGeometry(1.02, 20, 16), jadeMat);
        torso.scale.set(0.96, 0.88, 1.32);
        torso.position.set(0, 1.12, 0);
        bodyGroup.add(torso);

        const saddle = new activeThree.Mesh(new activeThree.TorusGeometry(0.88, 0.10, 10, 22, Math.PI), goldMat);
        saddle.rotation.y = Math.PI / 2;
        saddle.position.set(0, 1.15, 0);
        bodyGroup.add(saddle);

        headPivot.position.set(0, 1.22, 1.18);
        const head = new activeThree.Mesh(new activeThree.SphereGeometry(0.68, 16, 14), jadeMat);
        headPivot.add(head);

        const snout = new activeThree.Mesh(new activeThree.CylinderGeometry(0.36, 0.40, 0.42, 14), goldMat);
        snout.rotation.x = Math.PI / 2;
        snout.position.set(0, -0.08, 0.58);
        headPivot.add(snout);

        [-0.28, 0.28].forEach((sx) => {
          const tusk = new activeThree.Mesh(new activeThree.ConeGeometry(0.08, 0.42, 8), highlightJadeMat);
          tusk.position.set(sx, -0.12, 0.62);
          tusk.rotation.x = 0.4;
          headPivot.add(tusk);
        });

        [-0.45, 0.45].forEach((lx) => {
          [-0.65, 0.65].forEach((lz) => {
            const leg = new activeThree.Mesh(new activeThree.CylinderGeometry(0.22, 0.18, 0.72, 10), goldMat);
            leg.position.set(lx, 0.38, lz);
            bodyGroup.add(leg);
          });
        });

        tailPivot.position.set(0, 1.25, -1.25);
        const tail = new activeThree.Mesh(new activeThree.TorusGeometry(0.24, 0.06, 8, 16, Math.PI * 1.5), goldMat);
        tailPivot.add(tail);
        break;
      }
    }

    bodyGroup.add(headPivot);
    bodyGroup.add(tailPivot);
    return { bodyGroup, headPivot, tailPivot };
  }

  function buildTwelveZodiacSculptures(activeThree, scene, textures) {
    const orbitGroup = new activeThree.Group();
    orbitGroup.name = "ZodiacSculptureOrbit";
    orbitGroup.position.set(0, 7.5, 0);
    // Độ nghiêng vòng thiên văn 12 Địa Chi để tạo chiều sâu điện ảnh
    orbitGroup.rotation.x = 0.16;
    orbitGroup.rotation.z = -0.09;

    const antiqueGoldMat = new activeThree.MeshStandardMaterial({
      color: 0xc9a45c,
      emissive: 0x3a2709,
      emissiveIntensity: 0.26,
      metalness: 0.88,
      roughness: 0.22,
      envMap: textures.envMap
    });

    const pedestalStoneMat = new activeThree.MeshStandardMaterial({
      color: 0x132038,
      emissive: 0x0b1628,
      emissiveIntensity: 0.22,
      metalness: 0.35,
      roughness: 0.32,
      envMap: textures.envMap
    });

    // Vòng chỉ mảnh bằng vàng cổ nối kết quỹ đạo 12 cung địa chi
    const orbitTrackGeo = new activeThree.TorusGeometry(45, 0.12, 12, 128);
    const orbitTrackMesh = new activeThree.Mesh(orbitTrackGeo, antiqueGoldMat);
    orbitTrackMesh.rotation.x = Math.PI / 2;
    orbitGroup.add(orbitTrackMesh);

    const statues = [];

    ZODIAC_LORE.forEach((zInfo, idx) => {
      const angle = (idx / 12) * Math.PI * 2 - Math.PI / 2;
      const radius = 45;
      const root = new activeThree.Group();
      root.position.set(
        Math.cos(angle) * radius,
        Math.sin(idx * 1.5) * 1.4,
        Math.sin(angle) * radius
      );
      // Hướng tượng nhìn vào trung tâm Thiên Cầu
      root.lookAt(0, 0, 0);

      // Mỗi con giáp có vật liệu Ngọc Bích riêng để khi được chọn có thể bừng sáng
      const jadeSculptureMat = new activeThree.MeshStandardMaterial({
        color: 0x39afa0,
        emissive: 0x0e3d36,
        emissiveIntensity: 0.32,
        metalness: 0.25,
        roughness: 0.18,
        bumpMap: textures.scaleBumpMap,
        bumpScale: 0.06,
        envMap: textures.envMap,
        envMapIntensity: 1.3
      });

      const highlightJadeMat = new activeThree.MeshStandardMaterial({
        color: 0xe8e5d9,
        emissive: 0x6ee7b7,
        emissiveIntensity: 0.45,
        metalness: 0.2,
        roughness: 0.15
      });

      // Bệ Đỡ Đài Sen Bát Giác Nổi Tinh Xảo (Floating Carved Lotus Pedestal)
      const pedestalGroup = new activeThree.Group();
      const baseTop = new activeThree.Mesh(new activeThree.CylinderGeometry(2.45, 2.85, 0.65, 8), pedestalStoneMat);
      baseTop.position.y = -0.32;
      pedestalGroup.add(baseTop);

      const goldRim = new activeThree.Mesh(new activeThree.TorusGeometry(2.55, 0.14, 10, 8), antiqueGoldMat);
      goldRim.rotation.x = Math.PI / 2;
      goldRim.position.y = 0.02;
      pedestalGroup.add(goldRim);

      const underCone = new activeThree.Mesh(new activeThree.ConeGeometry(2.1, 2.6, 8), pedestalStoneMat);
      underCone.rotation.x = Math.PI;
      underCone.position.y = -1.92;
      pedestalGroup.add(underCone);

      // Vòng sáng khi được lựa chọn (Selection Highlight Halo)
      const selectHaloGeo = new activeThree.TorusGeometry(3.15, 0.10, 12, 36);
      const selectHaloMat = new activeThree.MeshBasicMaterial({
        color: 0x6ee7b7,
        transparent: true,
        opacity: 0.0,
        blending: activeThree.AdditiveBlending,
        depthWrite: false
      });
      const selectHalo = new activeThree.Mesh(selectHaloGeo, selectHaloMat);
      selectHalo.rotation.x = Math.PI / 2;
      selectHalo.position.y = 0.12;
      pedestalGroup.add(selectHalo);

      root.add(pedestalGroup);

      // Tượng Điêu Khắc Ngọc & Vàng Cổ của Con Giáp
      const sculptureHolder = new activeThree.Group();
      sculptureHolder.scale.set(1.28, 1.28, 1.28);
      const parts = buildZodiacJadeSculptureMesh(activeThree, idx, jadeSculptureMat, antiqueGoldMat, highlightJadeMat);
      sculptureHolder.add(parts.bodyGroup);
      root.add(sculptureHolder);

      // Gán thông tin tương tác Raycast cho toàn bộ mesh của tượng và bệ
      root.traverse((child) => {
        if (child.isMesh) {
          child.userData = {
            entityType: "zodiac",
            entityData: zInfo,
            zodiacIndex: idx
          };
          clickableMeshes.push(child);
        }
      });

      orbitGroup.add(root);
      statues.push({
        index: idx,
        entityData: zInfo,
        root,
        sculptureHolder,
        headPivot: parts.headPivot,
        tailPivot: parts.tailPivot,
        jadeSculptureMat,
        selectHaloMat,
        baseAngle: angle,
        baseY: root.position.y
      });
    });

    scene.add(orbitGroup);
    return {
      orbitGroup,
      statues
    };
  }

  // ==========================================================================
  // 10. PHẦN 4 — NGŨ HÀNH 3D (5 THỰC THỂ HÌNH KHỐI & VẬT LIỆU KHÁC BIỆT)
  // ==========================================================================
  function buildFiveElementsEntities(activeThree, scene, textures) {
    const orbitGroup = new activeThree.Group();
    orbitGroup.name = "FiveElementsOrbit";
    orbitGroup.position.set(0, 9.5, 0);
    orbitGroup.rotation.x = -0.14;
    orbitGroup.rotation.z = 0.11;

    const elements = [];
    const radius = 29.5;

    ELEMENT_LORE.forEach((eInfo, idx) => {
      const angle = (idx / 5) * Math.PI * 2;
      const root = new activeThree.Group();
      root.position.set(
        Math.cos(angle) * radius,
        Math.sin(idx * 2.1) * 1.8,
        Math.sin(angle) * radius
      );

      const entityHolder = new activeThree.Group();
      root.add(entityHolder);

      const animRefs = {};

      if (eInfo.key === "Kim") {
        // KIM: Khối tinh thể kim loại đa diện sắc cạnh + những vòng mảnh xoay quanh
        const kimMat = new activeThree.MeshStandardMaterial({
          color: 0xe8e5d9,
          emissive: 0xc9a45c,
          emissiveIntensity: 0.25,
          metalness: 0.94,
          roughness: 0.12,
          envMap: textures.envMap,
          envMapIntensity: 1.5,
          flatShading: true
        });
        const goldRingMat = new activeThree.MeshStandardMaterial({
          color: 0xc9a45c,
          emissive: 0x5c4212,
          emissiveIntensity: 0.35,
          metalness: 0.9,
          roughness: 0.18,
          envMap: textures.envMap
        });

        const coreCrystal = new activeThree.Mesh(new activeThree.OctahedronGeometry(2.15, 0), kimMat);
        coreCrystal.scale.set(0.85, 1.45, 0.85);
        entityHolder.add(coreCrystal);

        // 6 tinh thể sắc cạnh vệ tinh đâm chéo
        for (let s = 0; s < 6; s++) {
          const sa = (s / 6) * Math.PI * 2;
          const shard = new activeThree.Mesh(new activeThree.OctahedronGeometry(0.95, 0), s % 2 === 0 ? kimMat : goldRingMat);
          shard.scale.set(0.55, 1.65, 0.55);
          shard.position.set(Math.cos(sa) * 1.35, (s % 2 === 0 ? 0.3 : -0.3), Math.sin(sa) * 1.35);
          shard.rotation.z = Math.cos(sa) * 0.45;
          shard.rotation.x = Math.sin(sa) * 0.45;
          entityHolder.add(shard);
        }

        // 3 vòng kim loại mảnh xoay quanh
        animRefs.rings = [];
        for (let r = 0; r < 3; r++) {
          const rMesh = new activeThree.Mesh(new activeThree.TorusGeometry(3.1 + r * 0.42, 0.06, 10, 48), goldRingMat);
          rMesh.rotation.set(r * 0.8, r * 0.5, 0);
          entityHolder.add(rMesh);
          animRefs.rings.push(rMesh);
        }
      } else if (eInfo.key === "Mộc") {
        // MỘC: Thực thể cây linh mộc thu nhỏ uốn lượn bằng ngọc xanh với hạt sáng bay lên
        const woodMat = new activeThree.MeshStandardMaterial({
          color: 0x6b4c2b,
          emissive: 0x24180b,
          emissiveIntensity: 0.25,
          metalness: 0.35,
          roughness: 0.55
        });
        const jadeCanopyMat = new activeThree.MeshStandardMaterial({
          color: 0x39afa0,
          emissive: 0x16655b,
          emissiveIntensity: 0.52,
          metalness: 0.22,
          roughness: 0.2,
          envMap: textures.envMap
        });

        // Đá nổi gốc cây
        const baseRock = new activeThree.Mesh(new activeThree.DodecahedronGeometry(1.45, 0), woodMat);
        baseRock.scale.set(1.2, 0.65, 1.2);
        baseRock.position.y = -1.65;
        entityHolder.add(baseRock);

        // Thân cây uốn lượn
        const trunkPts = [
          new activeThree.Vector3(0, -1.4, 0),
          new activeThree.Vector3(0.45, -0.4, 0.25),
          new activeThree.Vector3(-0.35, 0.65, -0.2),
          new activeThree.Vector3(0.15, 1.65, 0.1)
        ];
        const trunkCurve = new activeThree.CatmullRomCurve3(trunkPts);
        const trunkMesh = new activeThree.Mesh(new activeThree.TubeGeometry(trunkCurve, 20, 0.34, 10, false), woodMat);
        entityHolder.add(trunkMesh);

        // Tán lá ngọc bích phát sáng
        animRefs.canopy = new activeThree.Group();
        const canopyOffsets = [
          [0, 2.05, 0, 1.35],
          [-1.1, 1.45, 0.4, 0.95],
          [1.05, 1.55, -0.35, 0.98],
          [0.3, 1.35, 1.05, 0.85],
          [-0.4, 1.4, -0.95, 0.88]
        ];
        canopyOffsets.forEach(([cx, cy, cz, cr]) => {
          const leafCluster = new activeThree.Mesh(new activeThree.IcosahedronGeometry(cr, 1), jadeCanopyMat);
          leafCluster.scale.set(1.15, 0.72, 1.15);
          leafCluster.position.set(cx, cy, cz);
          animRefs.canopy.add(leafCluster);
        });
        entityHolder.add(animRefs.canopy);
      } else if (eInfo.key === "Thủy") {
        // THỦY: Khối nước lơ lửng trong suốt có khúc xạ và gợn sóng bề mặt
        const waterCoreMat = new activeThree.MeshStandardMaterial({
          color: 0x0284c7,
          emissive: 0x0369a1,
          emissiveIntensity: 0.65,
          metalness: 0.2,
          roughness: 0.1
        });
        const waterShellMat = new activeThree.MeshStandardMaterial({
          color: 0x7dd3fc,
          emissive: 0x0ea5e9,
          emissiveIntensity: 0.35,
          metalness: 0.15,
          roughness: 0.08,
          transparent: true,
          opacity: 0.74,
          envMap: textures.envMap,
          envMapIntensity: 1.6
        });

        const innerCore = new activeThree.Mesh(new activeThree.SphereGeometry(1.15, 24, 24), waterCoreMat);
        entityHolder.add(innerCore);

        const waveGeo = new activeThree.SphereGeometry(2.15, 32, 32);
        // Lưu tọa độ gốc để tạo gợn sóng thời gian thực
        const basePos = new Float32Array(waveGeo.attributes.position.array);
        const waveSphere = new activeThree.Mesh(waveGeo, waterShellMat);
        entityHolder.add(waveSphere);
        animRefs.waveSphere = waveSphere;
        animRefs.waveBasePos = basePos;

        // Các giọt linh thủy vệ tinh xoay quanh
        animRefs.droplets = new activeThree.Group();
        for (let d = 0; d < 5; d++) {
          const da = (d / 5) * Math.PI * 2;
          const drop = new activeThree.Mesh(new activeThree.SphereGeometry(0.32, 14, 14), waterShellMat);
          drop.position.set(Math.cos(da) * 3.05, Math.sin(d * 1.8) * 0.8, Math.sin(da) * 3.05);
          animRefs.droplets.add(drop);
        }
        entityHolder.add(animRefs.droplets);
      } else if (eInfo.key === "Hỏa") {
        // HỎA: Cấu trúc lửa 3D nhiều lớp xoắn động + hạt tàn lửa bay lên
        const innerFireMat = new activeThree.MeshStandardMaterial({
          color: 0xfef08a,
          emissive: 0xf59e0b,
          emissiveIntensity: 0.9,
          roughness: 0.2
        });
        const outerFireMat = new activeThree.MeshStandardMaterial({
          color: 0x9f393d,
          emissive: 0xdc2626,
          emissiveIntensity: 0.72,
          metalness: 0.25,
          roughness: 0.25,
          flatShading: true
        });

        const coreFlame = new activeThree.Mesh(new activeThree.ConeGeometry(1.15, 3.4, 8), innerFireMat);
        coreFlame.position.y = 0.25;
        entityHolder.add(coreFlame);

        animRefs.flameTongues = [];
        for (let f = 0; f < 6; f++) {
          const fa = (f / 6) * Math.PI * 2;
          const tongue = new activeThree.Mesh(new activeThree.ConeGeometry(0.72, 2.85, 6), f % 2 === 0 ? outerFireMat : innerFireMat);
          tongue.position.set(Math.cos(fa) * 0.85, -0.15 + (f % 2) * 0.35, Math.sin(fa) * 0.85);
          tongue.rotation.z = Math.cos(fa) * -0.28;
          tongue.rotation.x = Math.sin(fa) * 0.28;
          entityHolder.add(tongue);
          animRefs.flameTongues.push({ mesh: tongue, baseAngle: fa });
        }
      } else {
        // THỔ: Khối đá cổ phân tầng có mạch vàng phát sáng và mảnh đá bay quanh
        const rockMat = new activeThree.MeshStandardMaterial({
          color: 0x3b2f26,
          emissive: 0x1c140d,
          emissiveIntensity: 0.25,
          metalness: 0.28,
          roughness: 0.72,
          flatShading: true
        });
        const goldVeinMat = new activeThree.MeshStandardMaterial({
          color: 0xc9a45c,
          emissive: 0xd97706,
          emissiveIntensity: 0.75,
          metalness: 0.88,
          roughness: 0.2
        });

        const monolith = new activeThree.Mesh(new activeThree.DodecahedronGeometry(2.05, 0), rockMat);
        monolith.scale.set(0.95, 1.35, 0.95);
        entityHolder.add(monolith);

        // Mạch quặng vàng phát sáng cắt ngang khối đá cổ
        for (let v = -1; v <= 1; v++) {
          const vein = new activeThree.Mesh(new activeThree.TorusGeometry(1.82 - Math.abs(v) * 0.32, 0.11, 8, 16), goldVeinMat);
          vein.position.y = v * 0.72;
          vein.rotation.x = Math.PI / 2 + v * 0.22;
          entityHolder.add(vein);
        }

        // 6 mảnh đá vệ tinh xoay chậm xung quanh
        animRefs.shards = new activeThree.Group();
        for (let s = 0; s < 6; s++) {
          const sa = (s / 6) * Math.PI * 2;
          const shard = new activeThree.Mesh(new activeThree.DodecahedronGeometry(0.45, 0), s % 2 === 0 ? rockMat : goldVeinMat);
          shard.position.set(Math.cos(sa) * 3.15, (s % 2 === 0 ? 0.55 : -0.55), Math.sin(sa) * 3.15);
          animRefs.shards.add(shard);
        }
        entityHolder.add(animRefs.shards);
      }

      root.traverse((child) => {
        if (child.isMesh) {
          child.userData = {
            entityType: "element",
            entityData: eInfo,
            elementIndex: idx
          };
          clickableMeshes.push(child);
        }
      });

      orbitGroup.add(root);
      elements.push({
        index: idx,
        entityData: eInfo,
        root,
        entityHolder,
        animRefs
      });
    });

    scene.add(orbitGroup);
    return {
      orbitGroup,
      elements
    };
  }

  // ==========================================================================
  // 11. ANIMATION ENGINE CHO TỪNG TẦNG THỰC THỂ 3D
  // ==========================================================================
  function getDragonSpatialPoint(activeThree, theta) {
    // Quỹ đạo 3D uốn lượn tự nhiên bao quanh Thiên Cầu (bán kính 22..32, cao độ 5..21)
    const r = 25.5 + Math.sin(theta * 2.0) * 5.2;
    const x = Math.cos(theta) * r;
    const z = Math.sin(theta) * r;
    const y = 13.5 + Math.sin(theta * 3.0) * 6.5 + Math.cos(theta * 1.0) * 2.2;
    return new activeThree.Vector3(x, y, z);
  }

  function updateGuardiansAnimation(activeThree, elapsed, speedMult) {
    const t = elapsed * speedMult;

    guardiansList.forEach((g) => {
      if (g.type === "dragon") {
        // 2.1 THANH LONG: Slow majestic serpentine flight
        const headTheta = t * 0.42;
        const headPos = getDragonSpatialPoint(activeThree, headTheta);
        const lookAheadPos = getDragonSpatialPoint(activeThree, headTheta + 0.06);

        g.headGroup.position.copy(headPos);
        g.headGroup.lookAt(lookAheadPos);

        // Râu rồng bay mềm độc lập
        g.whiskers.forEach((w, wi) => {
          w.rotation.z = Math.sin(t * 3.6 + wi) * 0.24;
          w.rotation.x = 0.45 + Math.cos(t * 2.8 + wi) * 0.16;
        });

        // 44 đốt thân đi theo sóng hình sin dọc quỹ đạo không gian
        const segCount = g.segments.length;
        for (let i = 0; i < segCount; i++) {
          const lagTheta = headTheta - (i + 1) * 0.036;
          const basePt = getDragonSpatialPoint(activeThree, lagTheta);
          const nextPt = getDragonSpatialPoint(activeThree, lagTheta + 0.03);

          // Sóng uốn lượn ngang & dọc theo thân rồng
          const waveAmp = 0.85 * Math.min(1, (i + 2) / 10);
          const wavePhase = t * 5.2 - i * 0.34;
          basePt.y += Math.sin(wavePhase) * waveAmp * 0.55;
          basePt.x += Math.cos(wavePhase) * waveAmp * 0.42;

          const seg = g.segments[i];
          seg.position.copy(basePt);
          seg.lookAt(nextPt);
        }
      } else if (g.type === "phoenix") {
        // 2.2 PHƯỢNG HOÀNG: Graceful wing flapping and gliding with banking
        const pTheta = -t * 0.48 + Math.PI * 0.55;
        const pr = 31.5 + Math.cos(pTheta * 2.0) * 4.5;
        const px = Math.cos(pTheta) * pr;
        const pz = Math.sin(pTheta) * pr;
        const py = 18.5 + Math.sin(pTheta * 2.0) * 5.2;

        const nextTheta = pTheta - 0.05;
        const npr = 31.5 + Math.cos(nextTheta * 2.0) * 4.5;
        const npx = Math.cos(nextTheta) * npr;
        const npz = Math.sin(nextTheta) * npr;
        const npy = 18.5 + Math.sin(nextTheta * 2.0) * 5.2;

        g.bodyRig.position.set(px, py, pz);
        g.bodyRig.lookAt(npx, npy, npz);
        // Nghiêng thân (Banking) tự nhiên khi chuyển hướng
        g.bodyRig.rotateZ(Math.sin(pTheta * 2.0) * 0.32);

        // Nhịp vỗ cánh có độ trễ tự nhiên giữa khớp trong và khớp ngoài
        const flapCycle = t * 4.4;
        g.wings.forEach((w) => {
          const shoulderAngle = Math.sin(flapCycle) * 0.46 + 0.08;
          const outerAngle = Math.sin(flapCycle - 0.55) * 0.52;
          w.shoulderPivot.rotation.z = w.side * shoulderAngle;
          w.outerPivot.rotation.z = w.side * outerAngle;
        });

        // 5 Dải đuôi dài uốn theo luồng khí phía sau
        g.tailRibbons.forEach((ribbon) => {
          const rIdx = ribbon.offsetIndex;
          ribbon.nodes.forEach((node, nIdx) => {
            const lag = pTheta + (nIdx + 1) * 0.032;
            const lr = pr + rIdx * 0.55 + Math.sin(t * 4.2 - nIdx * 0.4 + rIdx) * 0.45;
            const lx = Math.cos(lag) * lr;
            const lz = Math.sin(lag) * lr;
            const ly = py - 0.25 + Math.sin(lag * 2.0) * 0.8 + Math.cos(t * 4.8 - nIdx * 0.45) * 0.35;
            node.position.set(lx, ly, lz);
            node.lookAt(px, py, pz);
          });
        });
      } else if (g.type === "qilin") {
        // 2.3 KỲ LÂN: Majestic celestial gallop trên dải vân mây
        const qTheta = t * 0.36 + Math.PI * 1.15;
        const qr = 35.0 + Math.sin(qTheta * 3.0) * 3.0;
        const gallopCycle = t * 6.2;
        const strideBob = Math.abs(Math.sin(gallopCycle)) * 0.85;

        const qx = Math.cos(qTheta) * qr;
        const qz = Math.sin(qTheta) * qr;
        const qy = 8.2 + Math.sin(qTheta * 2.0) * 3.6 + strideBob;

        const nTheta = qTheta + 0.05;
        const nqr = 35.0 + Math.sin(nTheta * 3.0) * 3.0;
        g.bodyRig.position.set(qx, qy, qz);
        g.bodyRig.lookAt(
          Math.cos(nTheta) * nqr,
          8.2 + Math.sin(nTheta * 2.0) * 3.6,
          Math.sin(nTheta) * nqr
        );
        // Độ nhún thân khi phi nước đại
        g.bodyRig.rotateX(Math.cos(gallopCycle) * 0.14);

        // Chuyển động khớp 4 chân không trượt
        g.legs.forEach((leg) => {
          const phase = gallopCycle + leg.phase;
          leg.hipPivot.rotation.x = Math.sin(phase) * 0.62;
          leg.kneePivot.rotation.x = Math.max(0, Math.cos(phase) * 0.78);
        });

        g.tailPivot.rotation.x = Math.sin(t * 4.5) * 0.25;
        g.cloudRibbon.rotation.z = t * 1.2;
      } else if (g.type === "turtle") {
        // 2.4 KIM QUY: Slow floating celestial movement giữa tầng mây
        const kTheta = -t * 0.22 + Math.PI * 1.72;
        const kr = 27.5;
        const kx = Math.cos(kTheta) * kr;
        const kz = Math.sin(kTheta) * kr;
        const ky = 2.2 + Math.sin(t * 1.4) * 1.65;

        const nkTheta = kTheta - 0.04;
        g.bodyRig.position.set(kx, ky, kz);
        g.bodyRig.lookAt(Math.cos(nkTheta) * kr, ky, Math.sin(nkTheta) * kr);

        // Đầu & 4 chân bơi lượn chậm rãi cổ kính
        g.headPivot.rotation.y = Math.sin(t * 1.1) * 0.18;
        g.headPivot.rotation.x = Math.cos(t * 0.9) * 0.08;

        g.flippers.forEach((fl, fi) => {
          const swimPhase = t * 2.1 + (fl.front ? 0 : Math.PI * 0.65);
          fl.fPivot.rotation.y = fl.side * (Math.sin(swimPhase) * 0.36);
          fl.fPivot.rotation.z = fl.side * (Math.cos(swimPhase) * 0.22);
        });
      }
    });
  }

  function updateZodiacAndElementsAnimation(elapsed, speedMult) {
    const t = elapsed * speedMult;

    // 12 Tượng Ngọc Con Giáp: Idle breathing, xoay đầu nhẹ, đuôi đung đưa & sáng lên khi được chọn
    zodiacStatuesList.forEach((statue, idx) => {
      const isSelected =
        cameraState.selectedEntity &&
        cameraState.selectedEntity.entityType === "zodiac" &&
        cameraState.selectedEntity.entityData.index === idx;
      const isHovered =
        cameraState.hoveredEntity &&
        cameraState.hoveredEntity.entityType === "zodiac" &&
        cameraState.hoveredEntity.entityData.index === idx;

      // Nhịp thở lơ lửng của bệ đài
      statue.root.position.y = statue.baseY + Math.sin(t * 1.8 + idx * 0.7) * 0.45;

      // Idle animation tinh tế của tượng ngọc
      const breathScale = 1.28 + Math.sin(t * 2.4 + idx) * 0.025;
      statue.sculptureHolder.scale.set(breathScale, breathScale, breathScale);

      if (statue.headPivot) {
        statue.headPivot.rotation.y = Math.sin(t * 1.5 + idx * 1.1) * 0.16;
        statue.headPivot.rotation.x = Math.cos(t * 1.2 + idx * 0.8) * 0.06;
      }
      if (statue.tailPivot) {
        statue.tailPivot.rotation.z = Math.sin(t * 2.8 + idx) * 0.22;
      }

      // Khi được chọn, tượng xoay nhẹ để người dùng quan sát & phát hào quang ngọc
      if (isSelected) {
        statue.sculptureHolder.rotation.y += 0.012 * speedMult;
        statue.jadeSculptureMat.emissiveIntensity = 0.82;
        statue.selectHaloMat.opacity = 0.85;
      } else if (isHovered) {
        statue.jadeSculptureMat.emissiveIntensity = 0.58;
        statue.selectHaloMat.opacity = 0.45;
      } else {
        statue.sculptureHolder.rotation.y *= 0.92;
        statue.jadeSculptureMat.emissiveIntensity = 0.32;
        statue.selectHaloMat.opacity = 0.0;
      }
    });

    // 5 Thực Thể Ngũ Hành: Animation đặc thù cho Kim - Mộc - Thủy - Hỏa - Thổ
    fiveElementsList.forEach((el, idx) => {
      el.root.position.y = Math.sin(t * 1.6 + idx * 1.3) * 1.2;
      el.entityHolder.rotation.y = t * 0.45 + idx;

      const refs = el.animRefs;
      if (refs.rings) {
        refs.rings.forEach((r, ri) => {
          r.rotation.x += (0.018 + ri * 0.008) * speedMult;
          r.rotation.y += (0.014 - ri * 0.006) * speedMult;
        });
      }
      if (refs.canopy) {
        const pulse = 1 + Math.sin(t * 2.6) * 0.05;
        refs.canopy.scale.set(pulse, pulse, pulse);
      }
      if (refs.waveSphere && refs.waveBasePos) {
        const posAttr = refs.waveSphere.geometry.attributes.position;
        const base = refs.waveBasePos;
        for (let v = 0; v < posAttr.count; v++) {
          const bx = base[v * 3];
          const by = base[v * 3 + 1];
          const bz = base[v * 3 + 2];
          const wave = 1 + Math.sin(by * 2.2 + t * 4.2) * 0.06 + Math.cos(bx * 2.0 - t * 3.5) * 0.04;
          posAttr.setXYZ(v, bx * wave, by * wave, bz * wave);
        }
        posAttr.needsUpdate = true;
        if (refs.droplets) refs.droplets.rotation.y = -t * 1.4;
      }
      if (refs.flameTongues) {
        refs.flameTongues.forEach((ft, fi) => {
          const s = 0.88 + Math.sin(t * 7.5 + fi * 1.4) * 0.22;
          ft.mesh.scale.set(1, s, 1);
          ft.mesh.rotation.y = t * 2.2 + ft.baseAngle;
        });
      }
      if (refs.shards) {
        refs.shards.rotation.y = -t * 0.85;
        refs.shards.rotation.z = Math.sin(t * 1.2) * 0.18;
      }
    });
  }

  // ==========================================================================
  // 12. HỆ THỐNG CAMERA ĐIỆN ẢNH 5 GIAI ĐOẠN & TƯƠNG TÁC RAYCAST 360°
  // ==========================================================================
  function updateCameraTransform(activeThree, elapsed) {
    if (!threeCamera) return;

    if (!cameraState.lookAtCurrent) {
      cameraState.lookAtCurrent = new activeThree.Vector3(0, 11, 0);
      cameraState.lookAtTarget = new activeThree.Vector3(0, 11, 0);
    }

    // Giai đoạn kịch bản điện ảnh mở đầu (5 Stages trong 10 giây đầu nếu người dùng chưa kéo/chọn)
    if (cameraState.mode === "cinematic_intro" && !cameraState.isDragging && !cameraState.selectedEntity) {
      if (elapsed < 2.0) {
        // Stage 1: Opening — Từ biển mây bay lên hướng về Đài Thiên Văn
        const p = elapsed / 2.0;
        cameraState.targetRadius = 128 - p * 32;
        cameraState.targetPhi = 1.36 - p * 0.16;
        cameraState.targetTheta = elapsed * 0.18;
        cameraState.lookAtTarget.set(0, 8 + p * 5, 0);
      } else if (elapsed < 4.2) {
        // Stage 2: Celestial Revelation — Cận cảnh Thiên Cầu Bạch Ngọc & Hỗn Thiên Nghi
        const p = (elapsed - 2.0) / 2.2;
        cameraState.targetRadius = 62 - Math.sin(p * Math.PI) * 14;
        cameraState.targetPhi = 1.15;
        cameraState.targetTheta = 0.36 + (elapsed - 2.0) * 0.35;
        cameraState.lookAtTarget.set(0, 13.5, 0);
      } else if (elapsed < 7.2) {
        // Stage 3: Guardian Awakening — Mở rộng khung hình đón Tứ Linh bay lượn
        cameraState.targetRadius = 82;
        cameraState.targetPhi = 1.08;
        cameraState.targetTheta += 0.0055;
        cameraState.lookAtTarget.set(0, 13.0, 0);
      } else {
        // Stage 4 & 5: Zodiac Formation & Interactive Overview
        cameraState.targetRadius = 92;
        cameraState.targetPhi = 1.12;
        if (cameraState.autoRotate) {
          cameraState.targetTheta += 0.0032;
        }
        cameraState.lookAtTarget.set(0, 11.5, 0);
      }
    } else if (cameraState.mode === "inspect" && cameraState.selectedEntity) {
      // Khi người dùng click một Con Giáp / Thần Thú / Ngũ Hành / Thiên Cầu
      const targetWorldPos = new activeThree.Vector3();
      if (cameraState.inspectTargetObj) {
        cameraState.inspectTargetObj.getWorldPosition(targetWorldPos);
      } else {
        targetWorldPos.set(0, 13.5, 0);
      }
      cameraState.lookAtTarget.copy(targetWorldPos);
      cameraState.lookAtTarget.y += 1.2;

      if (cameraState.autoRotate && !cameraState.isDragging) {
        cameraState.targetTheta += 0.0025;
      }
    } else {
      // Các chế độ quan sát theo tầng (overview, core, guardians, zodiac, elements)
      if (cameraState.autoRotate && !cameraState.isDragging) {
        cameraState.targetTheta += 0.0028;
      }
    }

    // Nội suy mượt mà (Smooth Damping)
    cameraState.sphericalTheta += (cameraState.targetTheta - cameraState.sphericalTheta) * 0.075;
    cameraState.sphericalPhi += (cameraState.targetPhi - cameraState.sphericalPhi) * 0.075;
    cameraState.sphericalRadius += (cameraState.targetRadius - cameraState.sphericalRadius) * 0.075;
    cameraState.lookAtCurrent.lerp(cameraState.lookAtTarget, 0.085);

    const sinPhi = Math.sin(cameraState.sphericalPhi);
    const camX = cameraState.lookAtCurrent.x + cameraState.sphericalRadius * sinPhi * Math.sin(cameraState.sphericalTheta);
    const camY = cameraState.lookAtCurrent.y + cameraState.sphericalRadius * Math.cos(cameraState.sphericalPhi);
    const camZ = cameraState.lookAtCurrent.z + cameraState.sphericalRadius * sinPhi * Math.cos(cameraState.sphericalTheta);

    threeCamera.position.set(camX, Math.max(-4, camY), camZ);
    threeCamera.lookAt(cameraState.lookAtCurrent);
  }

  // ==========================================================================
  // 13. KẾT NỐI DỮ LIỆU LÁ SỐ TỬ VI (`window.tuviData`) & BẢNG INSPECTOR
  // ==========================================================================
  function refreshCelestialChartHUD() {
    const data = window.tuviData;
    if (!data || !data.center) return;

    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el && val) el.textContent = val;
    };

    setTxt("c3d-name", data.center.name || "Đương Số");
    setTxt("c3d-year", `${data.center.solarYear || ""} (${data.center.lunarYear || ""} - ${data.center.amDuong || ""})`);
    setTxt("c3d-menh", data.center.banMenh || "Bản Mệnh");
    setTxt("c3d-cuc", data.center.cuc || "Ngũ Cục");
    setTxt("c3d-lords", `${data.center.menhChu || "—"} / ${data.center.thanChu || "—"}`);

    if (Array.isArray(data.chambers)) {
      const menhChamber = data.chambers.find((c) => c.name && c.name.toUpperCase().includes("MỆNH"));
      if (menhChamber) {
        const majorNames = (menhChamber.majorStars || []).map((s) => s.name.split(" ")[0]).join(", ");
        setTxt("c3d-menh-palace", `${menhChamber.branch} (${majorNames || "Vô Chính Diệu"})`);
      }
    }
  }
  window.refreshCelestialChartHUD = refreshCelestialChartHUD;

  function buildPalaceReadingHTML(entityType, entityData) {
    const data = window.tuviData;
    const chambers = data && Array.isArray(data.chambers) ? data.chambers : [];

    if (entityType === "zodiac") {
      const match = chambers.find((c) => c.branch === entityData.branch);
      if (!match) {
        return `
          <div class="palace-card-mini">
            <div><strong>Cung Địa Chi:</strong> ${entityData.branch} (${entityData.direction})</div>
            <div><strong>Ngũ Hành Cung:</strong> Hành ${entityData.element} • Giờ ${entityData.hours}</div>
          </div>
        `;
      }
      const majors = (match.majorStars || []).map((s) => `<span class="star-pill-major">${s.name}</span>`).join(" ");
      const goodMinors = (match.minorStarsGood || []).slice(0, 6).map((s) => `<span class="star-pill-minor">${s.name}</span>`).join(" ");
      return `
        <div class="palace-card-mini">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <strong style="color:#E8D096;font-size:0.9rem;">Cung ${match.name}${match.isThan ? " (Thân)" : ""} — Địa Chi ${match.branch}</strong>
            <span style="font-size:0.74rem;color:#6EE7B7;">Đại vận: ${match.limit || "—"}</span>
          </div>
          <div style="margin-bottom:4px;"><strong>Chính tinh tọa thủ:</strong> ${majors || '<em style="color:#94A3B8;">Vô Chính Diệu</em>'}</div>
          <div><strong>Cát tinh hội hợp:</strong> ${goodMinors || "Đang hội chiếu"}</div>
          <div style="margin-top:6px;font-size:0.76rem;color:#CBD5E1;">Vòng Trường Sinh: <strong>${match.truongSinh || "—"}</strong> • Tháng Âm: <strong>${match.month || "—"}</strong></div>
        </div>
      `;
    }

    if (entityType === "guardian") {
      const matchedChambers = chambers.filter((c) => entityData.branches.includes(c.branch));
      const chamberSummary = matchedChambers
        .map((c) => `<strong>${c.branch} (${c.name})</strong>`)
        .join(" • ");
      return `
        <div class="palace-card-mini">
          <div><strong>Tam Phương Trấn Giữ:</strong> ${chamberSummary || entityData.branches.join(" • ")}</div>
          <div style="margin-top:5px;"><strong>Tinh đẩu đồng khí:</strong> ${entityData.tuviStars.map((s) => `<span class="star-pill-major">${s}</span>`).join(" ")}</div>
        </div>
      `;
    }

    if (entityType === "element") {
      const banMenh = (data && data.center && data.center.banMenh) || "Sơn Đầu Hỏa";
      const cuc = (data && data.center && data.center.cuc) || "Thổ Ngũ Cục";
      return `
        <div class="palace-card-mini">
          <div><strong>Quy Luật Sinh Khắc:</strong> ${entityData.relations}</div>
          <div style="margin-top:5px;"><strong>Đối Chiếu Bản Mệnh:</strong> Đương số mệnh <strong style="color:#E8D096;">${banMenh}</strong> — Cục <strong style="color:#6EE7B7;">${cuc}</strong>.</div>
        </div>
      `;
    }

    return `
      <div class="palace-card-mini">
        <div>${CORE_METADATA.palaceHint}</div>
      </div>
    `;
  }

  function selectCelestialEntity(entityType, entityData, targetObject3D) {
    // Khi người dùng chủ động click khám phá thực thể, tự động giữ lại chế độ khám phá
    window.enableInteractiveExploration(true);

    cameraState.mode = "inspect";
    cameraState.selectedEntity = { entityType, entityData };
    cameraState.inspectTargetObj = targetObject3D;

    if (targetObject3D && window.THREE) {
      const wp = new window.THREE.Vector3();
      targetObject3D.getWorldPosition(wp);
      if (Math.hypot(wp.x, wp.z) > 1.0) {
        cameraState.targetTheta = Math.atan2(wp.x, wp.z) + 0.32;
      }
    }

    if (entityType === "zodiac") {
      cameraState.targetRadius = 11.5;
      cameraState.targetPhi = 1.24;
    } else if (entityType === "guardian") {
      cameraState.targetRadius = 22.0;
      cameraState.targetPhi = 1.15;
    } else if (entityType === "element") {
      cameraState.targetRadius = 11.5;
      cameraState.targetPhi = 1.18;
    } else {
      cameraState.targetRadius = 28.0;
      cameraState.targetPhi = 1.16;
    }

    playBellStrike(324, 0.08);

    // Hiển thị Right Inspector Panel
    const rightPanel = document.getElementById("cinematic-right-panel");
    if (rightPanel) rightPanel.style.display = "block";

    const setEl = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    if (entityType === "zodiac") {
      setEl("inspector-category", "THẬP NHỊ ĐỊA CHI • TƯỢNG NGỌC CỔ 3D");
      setEl("inspector-hanzi", entityData.hanzi);
      setEl("inspector-title", entityData.name);
      setEl("inspector-meta", `Hành ${entityData.element} • ${entityData.direction} • ${entityData.hours}`);
      setEl("inspector-lore", entityData.lore);
    } else if (entityType === "guardian") {
      setEl("inspector-category", entityData.category);
      setEl("inspector-hanzi", entityData.hanzi);
      setEl("inspector-title", entityData.name);
      setEl("inspector-meta", entityData.meta);
      setEl("inspector-lore", entityData.lore);
    } else if (entityType === "element") {
      setEl("inspector-category", "NGŨ HÀNH TINH KHÍ • THỰC THỂ 3D");
      setEl("inspector-hanzi", entityData.hanzi);
      setEl("inspector-title", entityData.name);
      setEl("inspector-meta", entityData.meta);
      setEl("inspector-lore", entityData.lore);
    } else {
      setEl("inspector-category", CORE_METADATA.category);
      setEl("inspector-hanzi", CORE_METADATA.hanzi);
      setEl("inspector-title", CORE_METADATA.name);
      setEl("inspector-meta", CORE_METADATA.meta);
      setEl("inspector-lore", CORE_METADATA.lore);
    }

    const readingEl = document.getElementById("inspector-chart-reading");
    if (readingEl) {
      readingEl.innerHTML = buildPalaceReadingHTML(entityType, entityData);
    }
  }

  // ==========================================================================
  // 14. PUBLIC UI CONTROLS (BOTTOM DOCK, SUB-DOCK, VIEW MODES, EXPLORE LOCK)
  // ==========================================================================
  window.setCelestialViewMode = function (mode) {
    window.enableInteractiveExploration(true);
    cameraState.selectedEntity = null;
    cameraState.inspectTargetObj = null;
    cameraState.mode = mode;

    const rightPanel = document.getElementById("cinematic-right-panel");
    if (rightPanel && mode !== "inspect") rightPanel.style.display = "none";

    if (cameraState.lookAtTarget) {
      cameraState.lookAtTarget.set(0, 11.5, 0);
    }

    if (mode === "overview") {
      cameraState.targetRadius = 92;
      cameraState.targetPhi = 1.12;
    } else if (mode === "core") {
      cameraState.targetRadius = 32;
      cameraState.targetPhi = 1.16;
      if (cameraState.lookAtTarget) cameraState.lookAtTarget.set(0, 13.5, 0);
      selectCelestialEntity("core", CORE_METADATA, coreJadeSphere);
    } else if (mode === "guardians") {
      cameraState.targetRadius = 64;
      cameraState.targetPhi = 1.06;
    } else if (mode === "zodiac") {
      cameraState.targetRadius = 78;
      cameraState.targetPhi = 0.96;
    } else if (mode === "elements") {
      cameraState.targetRadius = 54;
      cameraState.targetPhi = 1.04;
    }

    // Cập nhật trạng thái active trên Left Panel & Bottom Dock
    ["overview", "core", "guardians", "zodiac", "elements"].forEach((m) => {
      const obsBtn = document.getElementById(`obs-btn-${m}`);
      if (obsBtn) obsBtn.classList.toggle("active", m === mode);
    });
    const dockOverview = document.getElementById("dock-btn-overview");
    if (dockOverview) dockOverview.classList.toggle("active", mode === "overview");
  };

  window.resetCelestialCamera = function () {
    const subDock = document.getElementById("cinematic-sub-dock");
    if (subDock) subDock.style.display = "none";
    cameraState.activeSubDock = null;
    window.setCelestialViewMode("overview");
  };

  window.toggleCelestialAutoRotate = function () {
    cameraState.autoRotate = !cameraState.autoRotate;
    const btn = document.getElementById("dock-btn-autorotate");
    if (btn) btn.classList.toggle("active", cameraState.autoRotate);
  };

  window.toggleLeftCelestialPanel = function () {
    const body = document.getElementById("cinematic-left-body");
    if (!body) return;
    body.style.display = body.style.display === "none" ? "block" : "none";
  };

  window.enableInteractiveExploration = function (silent = false) {
    window.isExploringCelestialRealm = true;
    if (summonTimerId) {
      clearTimeout(summonTimerId);
      summonTimerId = null;
    }
    const btn = document.getElementById("btn-celestial-explore");
    const lbl = document.getElementById("lbl-celestial-explore");
    if (btn) btn.classList.add("active");
    if (lbl) lbl.textContent = "Đang Khám Phá 3D";

    const statusEl = document.getElementById("celestial-status-text");
    if (statusEl && !silent) {
      statusEl.textContent = "Chế Độ Khám Phá 3D Tự Do • Click Tứ Linh, 12 Con Giáp hoặc Ngũ Hành để xem luận giải";
    }
  };

  window.toggleCelestialSubDock = function (groupType) {
    window.enableInteractiveExploration(true);
    const subDock = document.getElementById("cinematic-sub-dock");
    if (!subDock) return;

    if (cameraState.activeSubDock === groupType && subDock.style.display !== "none") {
      subDock.style.display = "none";
      cameraState.activeSubDock = null;
      return;
    }

    cameraState.activeSubDock = groupType;
    subDock.innerHTML = "";
    subDock.style.display = "flex";

    ["guardians", "zodiac", "elements"].forEach((g) => {
      const btn = document.getElementById(`dock-btn-${g}`);
      if (btn) btn.classList.toggle("active", g === groupType);
    });

    if (groupType === "guardians") {
      guardiansList.forEach((g) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "sub-dock-chip";
        chip.textContent = `${g.entityData.hanzi} ${g.entityData.name.split("—")[0].trim()}`;
        chip.onclick = () => {
          const targetObj = g.type === "dragon" ? g.headGroup : g.bodyRig;
          selectCelestialEntity("guardian", g.entityData, targetObj);
        };
        subDock.appendChild(chip);
      });
    } else if (groupType === "zodiac") {
      zodiacStatuesList.forEach((st) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "sub-dock-chip";
        chip.textContent = `${st.entityData.hanzi} ${st.entityData.branch}`;
        chip.onclick = () => {
          selectCelestialEntity("zodiac", st.entityData, st.root);
        };
        subDock.appendChild(chip);
      });
    } else if (groupType === "elements") {
      fiveElementsList.forEach((el) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "sub-dock-chip";
        chip.textContent = `${el.entityData.hanzi} Hành ${el.entityData.key}`;
        chip.onclick = () => {
          selectCelestialEntity("element", el.entityData, el.root);
        };
        subDock.appendChild(chip);
      });
    }
  };

  window.stepSelectedEntity = function (delta) {
    if (!cameraState.selectedEntity) return;
    const { entityType, entityData } = cameraState.selectedEntity;

    if (entityType === "zodiac") {
      const nextIdx = (entityData.index + delta + 12) % 12;
      const nextStatue = zodiacStatuesList[nextIdx];
      if (nextStatue) selectCelestialEntity("zodiac", nextStatue.entityData, nextStatue.root);
    } else if (entityType === "guardian") {
      const currIdx = guardiansList.findIndex((g) => g.entityData.id === entityData.id);
      const nextIdx = (currIdx + delta + guardiansList.length) % guardiansList.length;
      const nextG = guardiansList[nextIdx];
      if (nextG) {
        const targetObj = nextG.type === "dragon" ? nextG.headGroup : nextG.bodyRig;
        selectCelestialEntity("guardian", nextG.entityData, targetObj);
      }
    } else if (entityType === "element") {
      const currIdx = fiveElementsList.findIndex((e) => e.entityData.id === entityData.id);
      const nextIdx = (currIdx + delta + fiveElementsList.length) % fiveElementsList.length;
      const nextEl = fiveElementsList[nextIdx];
      if (nextEl) selectCelestialEntity("element", nextEl.entityData, nextEl.root);
    }
  };

  // ==========================================================================
  // 15. KHỞI TẠO THREE.JS SCENE, LIGHTING & POINTER/RAYCAST EVENTS
  // ==========================================================================
  let controlsInitialized = false;

  function setupCanvasPointerControls(canvas, activeThree) {
    if (controlsInitialized) return;
    controlsInitialized = true;

    const raycaster = new activeThree.Raycaster();
    const pointerNDC = new activeThree.Vector2();

    function getPointerNDC(evt) {
      const rect = canvas.getBoundingClientRect();
      const clientX = evt.touches ? evt.touches[0].clientX : evt.clientX;
      const clientY = evt.touches ? evt.touches[0].clientY : evt.clientY;
      pointerNDC.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      pointerNDC.y = -((clientY - rect.top) / rect.height) * 2 + 1;
      return { clientX, clientY };
    }

    canvas.addEventListener("pointerdown", (evt) => {
      cameraState.isDragging = true;
      cameraState.dragMoved = false;
      cameraState.pointerDownX = evt.clientX;
      cameraState.pointerDownY = evt.clientY;
      if (cameraState.mode === "cinematic_intro") {
        cameraState.mode = "overview";
      }
    });

    window.addEventListener("pointermove", (evt) => {
      if (!isSummonActive || !threeCamera) return;

      if (cameraState.isDragging) {
        const dx = evt.clientX - cameraState.pointerDownX;
        const dy = evt.clientY - cameraState.pointerDownY;
        if (Math.abs(dx) > 4 || Math.abs(dy) > 4) {
          cameraState.dragMoved = true;
          window.enableInteractiveExploration(true);
        }
        cameraState.targetTheta -= dx * 0.0055;
        cameraState.targetPhi = Math.max(0.32, Math.min(1.48, cameraState.targetPhi - dy * 0.0045));
        cameraState.pointerDownX = evt.clientX;
        cameraState.pointerDownY = evt.clientY;
        return;
      }

      // Raycast Hover cho Tooltip động (chỉ hiện tên khi trỏ chuột vào thực thể 3D)
      getPointerNDC(evt);
      raycaster.setFromCamera(pointerNDC, threeCamera);
      const hits = raycaster.intersectObjects(clickableMeshes, false);
      const tooltipEl = document.getElementById("cinematic-hover-tooltip");

      if (hits.length > 0 && hits[0].object && hits[0].object.userData && hits[0].object.userData.entityData) {
        const uData = hits[0].object.userData;
        cameraState.hoveredEntity = uData;
        canvas.style.cursor = "pointer";

        if (tooltipEl) {
          const tagEl = document.getElementById("tooltip-tag");
          const nameEl = document.getElementById("tooltip-name");
          if (tagEl) {
            tagEl.textContent =
              uData.entityType === "zodiac"
                ? `ĐỊA CHI • HÀNH ${uData.entityData.element.toUpperCase()}`
                : uData.entityType === "guardian"
                ? "TỨ LINH HỘ PHÁP"
                : uData.entityType === "element"
                ? "NGŨ HÀNH TINH KHÍ"
                : "TRUNG TÂM ĐẠI TRẬN";
          }
          if (nameEl) {
            nameEl.textContent = `${uData.entityData.hanzi || ""} ${uData.entityData.name}`;
          }
          tooltipEl.style.display = "flex";
          tooltipEl.style.left = `${evt.clientX}px`;
          tooltipEl.style.top = `${evt.clientY - 12}px`;
        }
      } else {
        cameraState.hoveredEntity = null;
        canvas.style.cursor = cameraState.isDragging ? "grabbing" : "grab";
        if (tooltipEl) tooltipEl.style.display = "none";
      }
    });

    window.addEventListener("pointerup", (evt) => {
      if (!cameraState.isDragging) return;
      cameraState.isDragging = false;

      if (!cameraState.dragMoved && isSummonActive && threeCamera) {
        getPointerNDC(evt);
        raycaster.setFromCamera(pointerNDC, threeCamera);
        const hits = raycaster.intersectObjects(clickableMeshes, false);
        if (hits.length > 0 && hits[0].object && hits[0].object.userData && hits[0].object.userData.entityData) {
          const hitMesh = hits[0].object;
          const { entityType, entityData, zodiacIndex, elementIndex } = hitMesh.userData;
          let targetObj = hitMesh;
          if (entityType === "zodiac" && zodiacStatuesList[zodiacIndex]) {
            targetObj = zodiacStatuesList[zodiacIndex].root;
          } else if (entityType === "element" && fiveElementsList[elementIndex]) {
            targetObj = fiveElementsList[elementIndex].root;
          } else if (entityType === "guardian") {
            const gMatch = guardiansList.find((g) => g.entityData.id === entityData.id);
            if (gMatch) targetObj = gMatch.type === "dragon" ? gMatch.headGroup : gMatch.bodyRig;
          } else if (entityType === "core") {
            targetObj = coreJadeSphere;
          }
          selectCelestialEntity(entityType, entityData, targetObj);
        }
      }
    });

    canvas.addEventListener(
      "wheel",
      (evt) => {
        if (!isSummonActive) return;
        evt.preventDefault();
        window.enableInteractiveExploration(true);
        cameraState.targetRadius = Math.max(12, Math.min(145, cameraState.targetRadius + evt.deltaY * 0.045));
      },
      { passive: false }
    );
  }

  function initThreeCelestialScene() {
    const activeThree = window.THREE;
    const canvas = document.getElementById("three-celestial-canvas");
    if (!activeThree || !canvas) return false;

    prefersReducedMotion =
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (!threeRenderer) {
      threeRenderer = new activeThree.WebGLRenderer({
        canvas: canvas,
        antialias: true,
        alpha: false,
        powerPreference: "high-performance"
      });
      threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      threeRenderer.setSize(window.innerWidth, window.innerHeight);
      if (activeThree.ACESFilmicToneMapping !== undefined) {
        threeRenderer.toneMapping = activeThree.ACESFilmicToneMapping;
        threeRenderer.toneMappingExposure = 1.18;
      }
    }

    clickableMeshes = [];
    threeScene = new activeThree.Scene();
    threeScene.background = new activeThree.Color(0x080d1c);
    threeScene.fog = new activeThree.FogExp2(0x080d1c, 0.0034);

    threeCamera = new activeThree.PerspectiveCamera(
      48,
      window.innerWidth / window.innerHeight,
      0.5,
      600
    );

    const textures = getProceduralTextures(activeThree);
    threeScene.environment = textures.envMap;

    // Hệ thống ánh sáng điện ảnh phương Đông (Cinematic Oriental Lighting)
    const hemiLight = new activeThree.HemisphereLight(0xe8e5d9, 0x080d1c, 0.72);
    threeScene.add(hemiLight);

    // Key Light Vàng Cổ từ đỉnh Thiên Cung
    const keyLight = new activeThree.DirectionalLight(0xffe4b5, 1.35);
    keyLight.position.set(45, 85, 52);
    threeScene.add(keyLight);

    // Rim Light Ngọc Bích (Jade Rim Light)
    const jadeRimLight = new activeThree.DirectionalLight(0x39afa0, 0.88);
    jadeRimLight.position.set(-65, 35, -45);
    threeScene.add(jadeRimLight);

    // Mystic Violet Under-Fill Light từ biển mây
    const violetFillLight = new activeThree.DirectionalLight(0x7c6fa8, 0.55);
    violetFillLight.position.set(0, -45, 25);
    threeScene.add(violetFillLight);

    // Point Light trung tâm phát ra từ Thiên Cầu Bạch Ngọc
    const corePointLight = new activeThree.PointLight(0xe8d096, 2.2, 110, 1.5);
    corePointLight.position.set(0, 14, 0);
    threeScene.add(corePointLight);

    // Xây dựng 3 tầng không gian 3D
    envGroup = buildCelestialEnvironment(activeThree, threeScene, textures);
    const coreBuilt = buildCelestialCoreObservatory(activeThree, threeScene, textures);
    coreObservatoryGroup = coreBuilt;
    coreJadeSphere = coreBuilt.jadeSphere;
    armillaryRings = coreBuilt.rings;

    guardiansList = buildFourGuardians(activeThree, threeScene, textures);

    const zodiacBuilt = buildTwelveZodiacSculptures(activeThree, threeScene, textures);
    zodiacStatuesList = zodiacBuilt.statues;

    const elementsBuilt = buildFiveElementsEntities(activeThree, threeScene, textures);
    fiveElementsList = elementsBuilt.elements;

    setupCanvasPointerControls(canvas, activeThree);
    refreshCelestialChartHUD();

    threeStartTime = performance.now();

    function animateFrame(now) {
      if (!isSummonActive) return;
      threeAnimFrameId = requestAnimationFrame(animateFrame);
      if (isPageHidden) return;

      const elapsed = (now - threeStartTime) / 1000;
      const speedMult = prefersReducedMotion ? 0.25 : 1.0;

      // 1. Chuyển động môi trường: Biển mây trôi chậm, hạt bụi vàng lơ lửng
      if (envGroup) {
        envGroup.cloudLayers.forEach((cl) => {
          const a = cl.baseAngle + elapsed * cl.speed * speedMult;
          cl.mesh.position.x = Math.cos(a) * cl.radius;
          cl.mesh.position.z = Math.sin(a) * cl.radius;
          cl.mesh.rotation.z += 0.0005 * speedMult;
        });

        const dPos = envGroup.dustPoints.geometry.attributes.position;
        for (let i = 0; i < dPos.count; i++) {
          let y = dPos.getY(i) + 0.035 * speedMult;
          if (y > 58) y = -10;
          dPos.setY(i, y);
        }
        dPos.needsUpdate = true;
      }

      // 2. Chuyển động Tầng 1: Thiên Cầu Bạch Ngọc & 5 vòng Hỗn Thiên Nghi xoay đa trục
      if (coreObservatoryGroup) {
        coreJadeSphere.rotation.y = elapsed * 0.24 * speedMult;
        const auraScale = 1.0 + Math.sin(elapsed * 2.2) * 0.04;
        coreObservatoryGroup.auraMesh.scale.set(auraScale, auraScale, auraScale);

        armillaryRings.forEach((r) => {
          r.group.rotation.x += r.cfg.speedX * 0.012 * speedMult;
          r.group.rotation.y += r.cfg.speedY * 0.012 * speedMult;
          r.group.rotation.z += r.cfg.speedZ * 0.012 * speedMult;
        });
      }

      // 3. Chuyển động Tầng 2: Bốn Thần Thú Long - Ly - Quy - Phượng
      updateGuardiansAnimation(activeThree, elapsed, speedMult);

      // 4. Chuyển động Tầng 3: 12 Tượng Ngọc Con Giáp & 5 Thực Thể Ngũ Hành
      updateZodiacAndElementsAnimation(elapsed, speedMult);

      // 5. Cập nhật Camera Điện Ảnh & Tương Tác
      updateCameraTransform(activeThree, elapsed);

      threeRenderer.render(threeScene, threeCamera);
    }

    if (threeAnimFrameId) cancelAnimationFrame(threeAnimFrameId);
    threeAnimFrameId = requestAnimationFrame(animateFrame);
    return true;
  }

  function stopThreeCelestialScene() {
    if (threeAnimFrameId) {
      cancelAnimationFrame(threeAnimFrameId);
      threeAnimFrameId = null;
    }
  }

  window.addEventListener("resize", () => {
    if (!threeRenderer || !threeCamera || !isSummonActive) return;
    threeCamera.aspect = window.innerWidth / window.innerHeight;
    threeCamera.updateProjectionMatrix();
    threeRenderer.setSize(window.innerWidth, window.innerHeight);
  });

  document.addEventListener("visibilitychange", () => {
    isPageHidden = document.hidden;
  });

  // ==========================================================================
  // 16. LIFECYCLE ĐIỀU KHIỂN ĐẠI TRẬN 3D (START / FINISH / SKIP)
  // ==========================================================================
  const STAGE_MESSAGES = [
    { atMs: 0, text: "Giai đoạn 1/5: Khởi Mở Thiên Cung • Hội Tụ Linh Khí..." },
    { atMs: 2000, text: "Giai đoạn 2/5: Khai Mở Đài Thiên Văn & Thiên Cầu Bạch Ngọc..." },
    { atMs: 4200, text: "Giai đoạn 3/5: Triệu Hồi Tứ Linh Thần Thú — Long • Ly • Quy • Phượng..." },
    { atMs: 6800, text: "Giai đoạn 4/5: An Định 12 Tượng Ngọc Địa Chi & Ngũ Hành Tinh Khí..." },
    { atMs: 8800, text: "Giai đoạn 5/5: Hoàn Tất Tinh Bàn • Click Thực Thể 3D Để Khám Phá Hoặc Xem Lá Số!" }
  ];

  window.startCelestialSummon = function (options = {}) {
    const durationMs = options.durationMs || 10000;
    const overlay = document.getElementById("celestial-summon-overlay");
    if (!overlay) return;

    // Reset state
    window.isExploringCelestialRealm = false;
    isSummonActive = true;
    cameraState.mode = "cinematic_intro";
    cameraState.selectedEntity = null;
    cameraState.inspectTargetObj = null;
    cameraState.sphericalTheta = 0.15;
    cameraState.sphericalPhi = 1.32;
    cameraState.sphericalRadius = 122;
    cameraState.targetTheta = 0.15;
    cameraState.targetPhi = 1.22;
    cameraState.targetRadius = 96;

    const rightPanel = document.getElementById("cinematic-right-panel");
    if (rightPanel) rightPanel.style.display = "none";
    const subDock = document.getElementById("cinematic-sub-dock");
    if (subDock) subDock.style.display = "none";
    const exploreBtn = document.getElementById("btn-celestial-explore");
    const exploreLbl = document.getElementById("lbl-celestial-explore");
    if (exploreBtn) exploreBtn.classList.remove("active");
    if (exploreLbl) exploreLbl.textContent = "Tự Do Khám Phá";

    overlay.style.display = "block";
    overlay.classList.remove("fade-out");
    overlay.classList.add("active");

    initThreeCelestialScene();
    playRitualSoundscape(durationMs / 1000);

    // Thanh tiến trình & đồng hồ đếm ngược 10 giây
    const fillEl = document.getElementById("celestial-progress-fill");
    if (fillEl) {
      fillEl.style.transition = "none";
      fillEl.style.width = "0%";
      void fillEl.offsetWidth;
      fillEl.style.transition = `width ${durationMs}ms linear`;
      fillEl.style.width = "100%";
    }

    const countdownNumEl = document.getElementById("celestial-countdown-num");
    let remainingSec = Math.ceil(durationMs / 1000);
    if (countdownNumEl) countdownNumEl.textContent = String(remainingSec);

    if (countdownIntervalId) clearInterval(countdownIntervalId);
    countdownIntervalId = setInterval(() => {
      remainingSec = Math.max(0, remainingSec - 1);
      if (countdownNumEl) countdownNumEl.textContent = String(remainingSec);
      if (remainingSec <= 0) {
        clearInterval(countdownIntervalId);
        countdownIntervalId = null;
      }
    }, 1000);

    stageTimerIds.forEach((id) => clearTimeout(id));
    stageTimerIds = [];
    const statusEl = document.getElementById("celestial-status-text");
    STAGE_MESSAGES.forEach((st) => {
      const tid = setTimeout(() => {
        if (statusEl && !window.isExploringCelestialRealm) {
          statusEl.textContent = st.text;
        }
      }, st.atMs);
      stageTimerIds.push(tid);
    });

    if (summonTimerId) clearTimeout(summonTimerId);
    summonTimerId = setTimeout(() => {
      if (!window.isExploringCelestialRealm) {
        window.finishCelestialSummon();
      }
    }, durationMs);
  };

  window.finishCelestialSummon = function (onComplete) {
    const overlay = document.getElementById("celestial-summon-overlay");
    if (!overlay || !isSummonActive) {
      if (typeof onComplete === "function") onComplete();
      return;
    }

    window.isExploringCelestialRealm = false;
    isSummonActive = false;

    if (summonTimerId) {
      clearTimeout(summonTimerId);
      summonTimerId = null;
    }
    if (countdownIntervalId) {
      clearInterval(countdownIntervalId);
      countdownIntervalId = null;
    }
    stageTimerIds.forEach((id) => clearTimeout(id));
    stageTimerIds = [];

    const tooltipEl = document.getElementById("cinematic-hover-tooltip");
    if (tooltipEl) tooltipEl.style.display = "none";

    playBellStrike(432, 0.12);

    const flashEl = document.getElementById("celestial-flash");
    if (flashEl) {
      flashEl.classList.add("flash-now");
      setTimeout(() => flashEl.classList.remove("flash-now"), 900);
    }

    setTimeout(() => {
      overlay.classList.remove("active");
      overlay.style.display = "none";
      stopThreeCelestialScene();
      stopAudioNodes();
      if (typeof onComplete === "function") onComplete();
    }, 280);
  };

  window.skipCelestialSummon = function () {
    window.isExploringCelestialRealm = false;
    if (typeof window.onCelestialSummonSkipped === "function") {
      const fn = window.onCelestialSummonSkipped;
      window.onCelestialSummonSkipped = null;
      fn();
    }
    window.finishCelestialSummon();
  };

  window.openCelestialRealmInteractive = function () {
    window.startCelestialSummon({ durationMs: 60000 });
    window.enableInteractiveExploration(false);
  };
})();
