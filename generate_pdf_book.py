import os
import base64
import sys
import subprocess
import json
import pathlib

# Ensure stdout uses UTF-8
if sys.stdout.encoding != 'UTF-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_browser_executable():
    import shutil
    # Environment variable override if specified
    if os.environ.get("CHROME_BIN") and os.path.exists(os.environ.get("CHROME_BIN")):
        return os.environ.get("CHROME_BIN")

    paths = [
        # Linux standard paths
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/snap/bin/chromium",
        # Windows standard paths
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
            
    # Check PATH with shutil.which
    for bin_name in ["chromium-browser", "chromium", "google-chrome-stable", "google-chrome", "chrome", "msedge"]:
        w = shutil.which(bin_name)
        if w:
            return w
            
    return None

CHI_ASPECTS = {
    "Tý": {"tam_hop": ["Thân", "Thìn"], "xung_chieu": "Ngọ", "nhi_hop": "Sửu"},
    "Sửu": {"tam_hop": ["Tỵ", "Dậu"], "xung_chieu": "Mùi", "nhi_hop": "Tý"},
    "Dần": {"tam_hop": ["Ngọ", "Tuất"], "xung_chieu": "Thân", "nhi_hop": "Hợi"},
    "Mão": {"tam_hop": ["Hợi", "Mùi"], "xung_chieu": "Dậu", "nhi_hop": "Tuất"},
    "Thìn": {"tam_hop": ["Thân", "Tý"], "xung_chieu": "Tuất", "nhi_hop": "Dậu"},
    "Tỵ": {"tam_hop": ["Dậu", "Sửu"], "xung_chieu": "Hợi", "nhi_hop": "Thân"},
    "Ngọ": {"tam_hop": ["Dần", "Tuất"], "xung_chieu": "Tý", "nhi_hop": "Mùi"},
    "Mùi": {"tam_hop": ["Hợi", "Mão"], "xung_chieu": "Sửu", "nhi_hop": "Ngọ"},
    "Thân": {"tam_hop": ["Tý", "Thìn"], "xung_chieu": "Dần", "nhi_hop": "Tỵ"},
    "Dậu": {"tam_hop": ["Tỵ", "Sửu"], "xung_chieu": "Mão", "nhi_hop": "Thìn"},
    "Tuất": {"tam_hop": ["Dần", "Ngọ"], "xung_chieu": "Thìn", "nhi_hop": "Mão"},
    "Hợi": {"tam_hop": ["Mão", "Mùi"], "xung_chieu": "Tỵ", "nhi_hop": "Dần"},
}

GRID_COORDS = {
    "Tỵ": {"r": 1, "c": 1}, "Ngọ": {"r": 1, "c": 2}, "Mùi": {"r": 1, "c": 3}, "Thân": {"r": 1, "c": 4},
    "Dậu": {"r": 2, "c": 4}, "Tuất": {"r": 3, "c": 4},
    "Hợi": {"r": 4, "c": 4}, "Tý": {"r": 4, "c": 3}, "Sửu": {"r": 4, "c": 2}, "Dần": {"r": 4, "c": 1},
    "Mão": {"r": 3, "c": 1}, "Thìn": {"r": 2, "c": 1}
}

CHAMBER_DESCS = {
    "menh": "Cung Mệnh thể hiện tính cách cốt lõi, thần thái, dung mạo, chí hướng và tổng quan thăng trầm suốt cuộc đời.",
    "phu_mau": "Cung Phụ Mẫu thể hiện phúc ấm, gia giáo, nền tảng nuôi dưỡng và mối quan hệ với cha mẹ.",
    "phuc_duc": "Cung Phúc Đức thể hiện đời sống tâm linh, phúc đức tổ tiên, bình an nội tâm và tuổi thọ. Đây là cung quyết định sự thanh thản hậu vận.",
    "dien_trach": "Cung Điền Trạch thể hiện bất động sản, đất đai, nhà cửa, nơi ăn chốn ở và sản nghiệp tích lũy.",
    "quan_loc": "Cung Quan Lộc thể hiện con đường công danh, học vấn, vị thế xã hội và định hướng phát triển sự nghiệp.",
    "no_boc": "Cung Nô Bộc thể hiện quan hệ bạn bè, đồng nghiệp, cấp dưới và đối tác ngoại giao.",
    "thien_di": "Cung Thiên Di thể hiện đối ngoại, xuất hành đi xa, năng lực ngoại giao và cơ hội phát triển ngoài xã hội.",
    "tat_ach": "Cung Tật Ách thể hiện sức khỏe thể chất, nguy cơ bệnh tật ách nạn và khả năng hóa giải hiểm nguy.",
    "tai_bach": "Cung Tài Bạch thể hiện khả năng kiếm tiền, dòng tiền lưu chuyển, năng lực tài chính và phương thức tích lũy tài sản.",
    "tu_tuc": "Cung Tử Tức thể hiện duyên phận con cái, số lượng con, mức độ thành đạt và sự hiếu thảo của thế hệ sau.",
    "phu_the": "Cung Phu Thê thể hiện tình duyên, diện mạo, tính cách của người bạn đời và sự đồng hành trong hôn nhân.",
    "huynh_de": "Cung Huynh Đệ thể hiện tình cảm, sự đùm bọc gắn kết và tương trợ giữa anh chị em ruột thịt."
}

def extract_chamber_stars_for_pdf(c):
    all_chinh = c.get("chinh_tinh", [])
    all_cat = c.get("cat_tinh", [])
    all_hung = c.get("hung_tinh", [])
    all_luu = c.get("luu_tinh", [])
    
    # 1. Chính tinh
    chinh_list = []
    for s in all_chinh:
        st = s.get("status") or s.get("brightness") or ""
        st_str = f" ({st})" if st else ""
        chinh_list.append(f"{s.get('name')}{st_str}")
    chinh_str = ", ".join(chinh_list) if chinh_list else "Vô Chính Diệu"
    
    # 2. Sao Lưu
    luu_stars = []
    for s in (all_luu + all_cat + all_hung):
        if s.get("is_luu") or s.get("name", "").startswith("L."):
            nm = s.get("name", "")
            if not nm.startswith("L."):
                nm = f"L.{nm}"
            if nm not in luu_stars:
                luu_stars.append(nm)
                
    # 3. Regular Cát tinh
    reg_cat = [s.get('name') for s in all_cat if not (s.get("is_luu") or s.get("name", "").startswith("L."))]
    
    # 4. Regular Hung tinh
    reg_hung = []
    for s in all_hung:
        if not (s.get("is_luu") or s.get("name", "").startswith("L.")):
            st = s.get("status") or ""
            st_str = f" ({st})" if st else ""
            reg_hung.append(f"{s.get('name')}{st_str}")
            
    cat_str = ", ".join(reg_cat) if reg_cat else "Không có"
    hung_str = ", ".join(reg_hung) if reg_hung else "Không có"
    luu_str = ", ".join(luu_stars) if luu_stars else "Không có"
    
    return chinh_str, cat_str, hung_str, luu_str, luu_stars

def analyze_star_combinations_python(c, xc, th1, th2, nh, name="đương số"):
    def get_names(cung):
        if not cung: return []
        stars = cung.get("chinh_tinh", []) + cung.get("cat_tinh", []) + cung.get("hung_tinh", [])
        return [s.get("name", "").upper().replace("(", "").replace(")", "").strip() for s in stars]
    
    resides = get_names(c)
    aspecting = get_names(xc) + get_names(th1) + get_names(th2)
    all_stars = resides + aspecting
    
    combos = []
    
    # 1. Sát Phá Tham
    spt = ["THẤT SÁT", "PHÁ QUÂN", "THAM LANG"]
    if any(s in spt for s in resides):
        combos.append({
            "title": "Cách cục Sát Phá Tham Tọa Thủ",
            "desc": f"Đương số <strong>{name}</strong> sở hữu cách cục dũng mãnh biến động <strong>Sát Phá Tham</strong> (Thất Sát, Phá Quân, Tham Lang) tọa thủ. Định hình nên mẫu người vô cùng quyết đoán, quả cảm, có tinh thần tiên phong đột phá cao, dám nghĩ dám làm và không ngại xông pha hiểm nguy. Tiền vận nhiều cọ xát thử thách rèn luyện bản lĩnh, hậu vận phú quý vinh hiển khi học được sự điềm tĩnh kiên nhẫn."
        })
    elif len([s for s in aspecting if s in spt]) >= 2:
        combos.append({
            "title": "Cách cục Sát Phá Tham Hội Chiếu",
            "desc": f"Cung vị chịu ảnh hưởng mạnh mẽ từ bộ ba chiến tướng <strong>Sát - Phá - Tham</strong> hội chiếu về. Đương số <strong>{name}</strong> liên tục đón nhận các biến động khách quan từ môi trường bên ngoài dội vào, thúc đẩy sự thay đổi nhanh chóng và đòi hỏi bản lĩnh quyết đoán cao độ."
        })
        
    # 2. Tử Phủ Vũ Tướng
    tpvt = ["TỬ VI", "THIÊN PHỦ", "VŨ KHÚC", "THIÊN TƯỚNG"]
    if any(s in tpvt for s in resides) and len([s for s in all_stars if s in tpvt]) >= 3:
        combos.append({
            "title": "Cách cục Tử Phủ Vũ Tướng Hoàng Kim",
            "desc": f"Cung vị đắc cách cục hoàng kim tôn quý <strong>Tử Phủ Vũ Tướng</strong>. Định hình nên tư chất vương giả, điềm đạm, có tài lãnh đạo tổ chức kiệt xuất, danh tài hiển đạt, hậu thuẫn vững chắc và được nhiều người kính trọng nể phục."
        })
        
    # 3. Cơ Nguyệt Đồng Lương
    cndl = ["THIÊN CƠ", "THÁI ÂM", "THIÊN ĐỒNG", "THIÊN LƯƠNG"]
    if any(s in cndl for s in resides) and len([s for s in all_stars if s in cndl]) >= 3:
        combos.append({
            "title": "Cách cục Cơ Nguyệt Đồng Lương Ôn Hòa",
            "desc": f"Đương số <strong>{name}</strong> đắc cách cục nho nhã đức độ <strong>Cơ Nguyệt Đồng Lương</strong>. Định hình nên người thông minh sắc sảo, tư duy logic kế hoạch xuất sắc, tính tình nhân hậu, đời sống an lành ít sóng gió lớn."
        })
        
    # 4. Cự Nhật
    if "CỰ MÔN" in all_stars and "THÁI DƯƠNG" in all_stars:
        combos.append({
            "title": "Cách cục Cự Nhật (Cự Môn - Thái Dương)",
            "desc": f"Sự kết hợp giữa chính tinh <strong>Cự Môn</strong> (ngôn từ sâu sắc, nghiên cứu biện thuyết) và <strong>Thái Dương</strong> (ánh sáng chiếu rọi danh tiếng) củng cố khả năng đàm phán, đối thoại rõ ràng và đem lại may mắn lớn trong giao tế xã hội của đương số <strong>{name}</strong>."
        })
        
    # 5. Nhật Nguyệt đồng chiếu
    if "THÁI DƯƠNG" in all_stars and "THÁI ÂM" in all_stars:
        combos.append({
            "title": "Cách cục Nhật Nguyệt Đồng Chiếu",
            "desc": f"Hai vầng sáng Mặt Trời (Thái Dương) và Mặt Trăng (Thái Âm) cùng hội tụ chiếu về. Mang lại sự cân bằng hoàn hảo về âm dương tư duy, trực giác nhạy bén sắc sảo kết hợp trí tuệ rộng mở sáng suốt cho đương số <strong>{name}</strong>."
        })
        
    # 6. Khôi Việt
    if "THIÊN KHÔI" in all_stars or "THIÊN VIỆT" in all_stars:
        combos.append({
            "title": "Cặp sao Thiên Khôi - Thiên Việt (Khôi Việt - Quý Nhân)",
            "desc": f"Cát tinh quý nhân đứng đầu nâng đỡ. Giúp đương số <strong>{name}</strong> luôn nhận được cơ hội đi tiên phong dẫn đầu xu hướng, được cấp trên hoặc trưởng bối tín nhiệm nâng đỡ vượt bậc."
        })
        
    # 7. Đào Hồng
    if "ĐÀO HOA" in all_stars or "HỒNG LOAN" in all_stars:
        combos.append({
            "title": "Cặp sao Đào Hoa - Hồng Loan (Đào Hồng)",
            "desc": f"Mang lại sức hút cá nhân nổi bật, cát duyên vượng phát, sự duyên dáng đoan trang giúp đương số <strong>{name}</strong> rất được lòng mọi người xung quanh."
        })
        
    # 8. Kình Đà
    if "KÌNH DƯƠNG" in all_stars or "ĐÀ LA" in all_stars:
        combos.append({
            "title": "Cặp sát tinh Kình Dương - Đà La (Kình Đà)",
            "desc": f"Chủ về những rào cản ngăn trở khuất tất kéo dài dai dẳng, va chạm pháp lý rắc rối hoặc cản trở nhỏ. Nhắc nhở đương số <strong>{name}</strong> luôn bình tĩnh kiên nhẫn, rà soát cẩn thận mọi văn bản hợp đồng."
        })
        
    # 9. Không Kiếp
    if "ĐỊA KHÔNG" in all_stars or "ĐỊA KIẾP" in all_stars:
        combos.append({
            "title": "Cặp đại sát tinh Địa Không - Địa Kiếp",
            "desc": f"Mang năng lượng bộc phát bộc tàn, thăng trầm dốc đứng. Lời khuyên cho đương số <strong>{name}</strong>: Tuyệt đối tránh xa đỏ đen mạo hiểm, quản lý tài chính chặt chẽ, lấy thực lực và giá trị cốt lõi làm gốc."
        })
        
    # 10. Tam Hóa Liên Châu
    hoas = [s for s in all_stars if "HÓA" in s]
    if len(hoas) >= 2:
        combos.append({
            "title": "Bộ Tứ Hóa Giao Hội (Khoa / Quyền / Lộc)",
            "desc": f"Có sự hội tụ của các hóa tinh ({', '.join(hoas)}). Giúp đương số <strong>{name}</strong> có tiếng nói uy lực, dòng tài chính tích cực và thanh danh lan tỏa mạnh mẽ."
        })
        
    return combos

def get_dynamic_classical_treatise(c, p):
    cname = c.get("name", "")
    cchi = c.get("chi", "")
    chinh_stars = [s.get("name") for s in c.get("chinh_tinh", [])]
    tt_val = c.get("tuan_triet", "")
    is_than = c.get("is_than", False)
    
    star_desc = ", ".join(chinh_stars) if chinh_stars else "Vô Chính Diệu"
    tt_note = f" ngộ {tt_val}" if tt_val else ""
    than_note = " (Thân cư tại đây)" if is_than else ""
    
    buu_dinh = f"Cụ Bửu Đình (Tử Vi Ứng Dụng): 'Cung {cname} an tại {cchi} đắc {star_desc}{tt_note}{than_note}. Đây là thế cung mang tính biến hóa sâu sắc. Nếu là miếu vượng thì khí thế bừng sáng, tài hoa phát tiết; nếu hãm địa hoặc VCD mà đắc Tuần Triệt thì biến hung thành cát, người có óc quan sát tinh tường, tùy thời cơ biến mà lập nghiệp thành công.'"
    dai_duc = f"Đại Đức Sơn Nhân (Tử Vi Đẩu Số Tinh Thành): 'Cung {cname} tại {cchi} ({c.get('can', '')} {cchi} - Hành {c.get('element', '')}), tinh diệu {star_desc} hội tụ tam phương tứ chính. Chủ về việc đương số cần nắm vững ngũ hành sinh khắc, giữ tâm thế ôn hòa và phát huy các cát tinh tương trợ để đạt độ vững chắc bền bỉ lâu dài.'"
    thien_luong = f"Cụ Thiên Lương (Tử Vi Nghiệm Lý): 'Xét cung {cname} tọa {cchi}, người xưa coi trọng cái gốc của đạo đức và vòng Thái Tuế. Gặp thuận cảnh thì không kiêu căng, gặp nghịch cảnh có Tuần Triệt hay sát tinh chiếu thì lấy nhẫn nại làm đầu, tích đức hành thiện thì hậu vận ắt chuyển hóa rực rỡ.'"
    trung_chau = f"Trung Châu Phái (Vương Đình Chi): '{star_desc} tại cung {cchi} cung {cname}. Năng lượng của bản cung liên kết mật thiết với các cung tam hợp và xung chiếu. Trong đại vận và lưu niên, khi gặp Lưu Niên Động Tinh kích hoạt sẽ tạo nên chuyển biến bước ngoặt, cần cẩn trọng trong giấy tờ và đón đầu thời cơ thăng tiến.'"
    
    return {
        "buu_dinh": buu_dinh,
        "dai_duc": dai_duc,
        "thien_luong": thien_luong,
        "trung_chau": trung_chau
    }

def render_tuvi_grid_page(chart_data):
    p = chart_data.get("personal_info", {})
    chambers = chart_data.get("chambers", [])
    
    name = p.get("name", "Hoàng Tuấn Việt")
    gender = p.get("gender", "Nam")
    solar_date = f"{p.get('birth_day_solar', 18):02d}/{p.get('birth_month_solar', 9):02d}/{p.get('birth_year_solar', 1995)}"
    lunar_date = f"{p.get('birth_day_lunar', 24):02d}/{p.get('birth_month_lunar', 8):02d}/{p.get('birth_year_lunar', 'Ất Hợi')}"
    hour_str = f"{p.get('birth_hour', 'Giờ Mùi')} ({p.get('birth_hour_stem', 'Đinh Mùi')})"
    elem_fate = p.get("element_fate", "Sơn Đầu Hỏa")
    elem_cuc = p.get("element_cuc", "Thổ Ngũ Cục")
    relation = p.get("relation_fate_cuc", "Mệnh sinh Cục")
    weight = p.get("weight", "4 lượng 1 chỉ")
    fate_lord = p.get("fate_lord", "Cự Môn")
    body_lord = p.get("body_lord", "Thiên Cơ")
    lai_nhan = p.get("lai_nhan_cung", "Tật Ách")
    analysis_year = p.get("analysis_year_solar", 2026)
    
    html = """
  <div class="page-break tuvi-grid-page">
    <div class="tuvi-grid-frame">
      <div class="tuvi-grid-inner">
"""
    
    # 12 Perimeter cells
    for c in chambers:
        chi = c.get("chi", "")
        coords = GRID_COORDS.get(chi, {"r": 1, "c": 1})
        r, col = coords["r"], coords["c"]
        
        cname = c.get("name", "").upper()
        ccan = c.get("can", "")
        celem = c.get("element", "")
        is_than = c.get("is_than", False)
        tt_val = c.get("tuan_triet", "")
        dai_han = c.get("dai_han", 0)
        nguyet_han = c.get("nguyet_han", 1)
        trang_sinh = c.get("trang_sinh", "Mộ")
        
        chinh, cat, hung, luu, luu_list = extract_chamber_stars_for_pdf(c)
        
        # Color coding element
        elem_colors = {
            "Kim": "#475569", "Mộc": "#16a34a", "Thủy": "#2563eb", "Hỏa": "#dc2626", "Thổ": "#b45309"
        }
        elem_bg = elem_colors.get(celem, "#b45309")
        
        tt_badge = ""
        if tt_val and "Triệt" in str(tt_val):
            tt_badge = '<span class="cell-badge-triet">TRIỆT</span>'
        elif tt_val and "Tuần" in str(tt_val):
            tt_badge = '<span class="cell-badge-tuan">TUẦN</span>'
            
        than_badge = '<span class="cell-badge-than">THÂN CƯ</span>' if is_than else ''
        
        # Format star lists
        cat_pills = "".join([f'<span class="pill-cat">{s.strip()}</span>' for s in cat.split(",") if s.strip() and s.strip() != "Không có"])
        hung_pills = "".join([f'<span class="pill-hung">{s.strip()}</span>' for s in hung.split(",") if s.strip() and s.strip() != "Không có"])
        luu_pills = "".join([f'<span class="pill-luu">{s.strip()}</span>' for s in luu_list if s.strip()])
        
        html += f"""
        <div class="grid-cell" style="grid-row: {r}; grid-column: {col};">
          <div class="cell-header">
            <div>
              <span class="cell-cung-name" style="color: {elem_bg};">CUNG {cname}</span>
              <span class="cell-can-chi">({ccan} {chi})</span>
            </div>
            <div class="cell-limits">
              {than_badge}
              <span class="cell-limit-tag">{dai_han}t • Thg {nguyet_han}</span>
            </div>
          </div>
          
          <div class="cell-chinh-row">
            <span class="cell-chinh-text">{chinh}</span>
            {tt_badge}
          </div>
          
          <div class="cell-stars-area">
            <div class="cell-stars-col">
              {cat_pills}
            </div>
            <div class="cell-stars-col">
              {hung_pills}
            </div>
          </div>
          
          <div class="cell-footer">
            <div class="cell-luu-row">{luu_pills}</div>
            <div class="cell-trang-sinh">{trang_sinh}</div>
          </div>
        </div>
"""

    # Center Panel (spans row 2-3, col 2-3)
    html += f"""
        <div class="grid-center-panel" style="grid-row: 2 / 4; grid-column: 2 / 4;">
          <div class="center-watermark-lotus">☯</div>
          <div class="center-header-title">
            <div style="font-size: 14pt; font-weight: bold; color: #8b0000; letter-spacing: 1.5px;">LÁ SỐ TỬ VI ĐẨU SỐ TOÀN THƯ</div>
            <div style="font-size: 8.5pt; color: #b45309; font-weight: bold; letter-spacing: 0.5px;">BÀN CỜ THIÊN BÀN - ĐỊA BÀN 12 CUNG VỊ</div>
          </div>
          
          <table class="center-info-grid">
            <tr>
              <td><strong>Họ và tên:</strong></td>
              <td style="color: #8b0000; font-weight: bold; font-size: 11pt;">{name}</td>
              <td><strong>Giới tính:</strong></td>
              <td><strong>{gender}</strong></td>
            </tr>
            <tr>
              <td><strong>Ngày sinh DL:</strong></td>
              <td>{solar_date}</td>
              <td><strong>Giờ sinh:</strong></td>
              <td>{hour_str}</td>
            </tr>
            <tr>
              <td><strong>Ngày sinh ÂL:</strong></td>
              <td>{lunar_date}</td>
              <td><strong>Cân lượng:</strong></td>
              <td>{weight}</td>
            </tr>
            <tr>
              <td><strong>Bản Mệnh:</strong></td>
              <td><span style="color: #dc2626; font-weight: bold;">{elem_fate}</span></td>
              <td><strong>Cục:</strong></td>
              <td><span style="color: #b45309; font-weight: bold;">{elem_cuc}</span></td>
            </tr>
            <tr>
              <td><strong>Tương quan:</strong></td>
              <td><em>{relation}</em></td>
              <td><strong>Lai Nhân Cung:</strong></td>
              <td><strong style="color: #7c3aed;">{lai_nhan}</strong></td>
            </tr>
            <tr>
              <td><strong>Chủ Mệnh:</strong></td>
              <td><strong>{fate_lord}</strong></td>
              <td><strong>Chủ Thân:</strong></td>
              <td><strong>{body_lord}</strong></td>
            </tr>
            <tr>
              <td><strong>Năm xem:</strong></td>
              <td colspan="3"><strong style="color: #6d28d9;">Lưu Niên Năm {analysis_year} (Bính Ngọ) • {p.get('age', 32)} Tuổi</strong></td>
            </tr>
          </table>
          
          <div style="text-align: center; margin-top: 8px; font-size: 7.5pt; color: #64748b; font-style: italic;">
            Hệ thống tính toán Đẩu Số & Bát Tự kết hợp Dynamic Astrological Engine
          </div>
        </div>
      </div>
    </div>
  </div>
"""
    return html

def render_bazi_visual_chart(bazi, p):
    pillars = bazi.get("pillars", {})
    y_p = pillars.get('year', {})
    m_p = pillars.get('month', {})
    d_p = pillars.get('day', {})
    h_p = pillars.get('hour', {})
    
    name = p.get("name", "Đương số")
    dm = bazi.get('day_master', d_p.get('can', 'Nhâm'))
    dmElem = bazi.get('day_master_elem', d_p.get('can_elem', 'Thủy'))
    
    html = f"""
  <div style="margin: 16px 0 24px 0;">
    <h3 class="section-header" style="margin-top: 0;">Đồ Hình Bát Tự Tứ Trụ Toàn Cảnh (4 Cột Trụ Bản Mệnh)</h3>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px;">
      
      <!-- Trụ Năm -->
      <div class="bazi-pillar-card">
        <div class="bazi-pillar-header">TRỤ NĂM (TỔ NGHIỆP)</div>
        <div class="bazi-pillar-can">{y_p.get('can', '')} <span class="bazi-god">({y_p.get('can_ten_god', 'Chính Ấn')})</span></div>
        <div class="bazi-pillar-chi">{y_p.get('chi', '')} <span class="bazi-god">({y_p.get('chi_elem', '')})</span></div>
        <div class="bazi-pillar-tang">Tàng: {y_p.get('hidden_can', '')}</div>
        <div class="bazi-pillar-trang">Tràng sinh: {y_p.get('trang_sinh', 'Thai')}</div>
        <div class="bazi-pillar-nap">Nạp âm: {y_p.get('nap_am', 'Sơn Đầu Hỏa')}</div>
      </div>

      <!-- Trụ Tháng -->
      <div class="bazi-pillar-card">
        <div class="bazi-pillar-header">TRỤ THÁNG (PHỤ MẪU)</div>
        <div class="bazi-pillar-can">{m_p.get('can', '')} <span class="bazi-god">({m_p.get('can_ten_god', 'Thất Sát')})</span></div>
        <div class="bazi-pillar-chi">{m_p.get('chi', '')} <span class="bazi-god">({m_p.get('chi_elem', '')})</span></div>
        <div class="bazi-pillar-tang">Tàng: {m_p.get('hidden_can', '')}</div>
        <div class="bazi-pillar-trang">Tràng sinh: {m_p.get('trang_sinh', 'Mộc Dục')}</div>
        <div class="bazi-pillar-nap">Nạp âm: {m_p.get('nap_am', 'Bình Địa Mộc')}</div>
      </div>

      <!-- Trụ Ngày -->
      <div class="bazi-pillar-card" style="border-color: #dc2626; background: #fffdfd;">
        <div class="bazi-pillar-header" style="background: #dc2626; color: #ffffff;">TRỤ NGÀY (NHẬT CHỦ)</div>
        <div class="bazi-pillar-can" style="color: #dc2626; font-size: 13pt;">{d_p.get('can', '')} <span class="bazi-god" style="color: #991b1b;">(BẢN THÂN)</span></div>
        <div class="bazi-pillar-chi">{d_p.get('chi', '')} <span class="bazi-god">({d_p.get('chi_elem', '')})</span></div>
        <div class="bazi-pillar-tang">Tàng: {d_p.get('hidden_can', '')}</div>
        <div class="bazi-pillar-trang">Tràng sinh: {d_p.get('trang_sinh', 'Đế Vượng')}</div>
        <div class="bazi-pillar-nap">Nạp âm: {d_p.get('nap_am', 'Kiếm Phong Kim')}</div>
      </div>

      <!-- Trụ Giờ -->
      <div class="bazi-pillar-card">
        <div class="bazi-pillar-header">TRỤ GIỜ (CON CÁI/HẬU)</div>
        <div class="bazi-pillar-can">{h_p.get('can', '')} <span class="bazi-god">({h_p.get('can_ten_god', 'Thiên Tài')})</span></div>
        <div class="bazi-pillar-chi">{h_p.get('chi', '')} <span class="bazi-god">({h_p.get('chi_elem', '')})</span></div>
        <div class="bazi-pillar-tang">Tàng: {h_p.get('hidden_can', '')}</div>
        <div class="bazi-pillar-trang">Tràng sinh: {h_p.get('trang_sinh', 'Dưỡng')}</div>
        <div class="bazi-pillar-nap">Nạp âm: {h_p.get('nap_am', 'Thiên Hà Thủy')}</div>
      </div>

    </div>

    <!-- Elemental Balance Bar Chart -->
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #cbd5e1; padding-bottom: 6px; margin-bottom: 10px;">
        <strong style="color: #78350f; font-size: 9.5pt;">📊 BIỂU ĐỒ ĐỊNH LƯỢNG NĂNG LƯỢNG NGŨ HÀNH BÁT TỰ</strong>
        <span style="font-size: 8pt; color: #64748b;">Nhật Chủ: {dm} ({dmElem}) • Đắc lệnh tháng</span>
      </div>

      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-size: 8pt; font-weight: bold; margin-bottom: 2px;">
          <span>🟡 KIM (18%): Tướng khí</span>
          <span style="color: #b45309;">Ấn tinh hỗ trợ</span>
        </div>
        <div style="height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden;">
          <div style="width: 18%; height: 100%; background: linear-gradient(90deg, #d97706, #f59e0b);"></div>
        </div>
      </div>

      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-size: 8pt; font-weight: bold; margin-bottom: 2px;">
          <span>🟢 MỘC (22%): Tướng khí</span>
          <span style="color: #16a34a;">Thực Thương tài hoa</span>
        </div>
        <div style="height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden;">
          <div style="width: 22%; height: 100%; background: linear-gradient(90deg, #15803d, #22c55e);"></div>
        </div>
      </div>

      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-size: 8pt; font-weight: bold; margin-bottom: 2px;">
          <span>🔵 THỦY (28%): VƯỢNG THỐNG SOÁI</span>
          <span style="color: #2563eb;">Nhật chủ tự cường</span>
        </div>
        <div style="height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden;">
          <div style="width: 28%; height: 100%; background: linear-gradient(90deg, #1d4ed8, #3b82f6);"></div>
        </div>
      </div>

      <div style="margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; font-size: 8pt; font-weight: bold; margin-bottom: 2px;">
          <span>🔴 HỎA (20%): Hưu khí</span>
          <span style="color: #dc2626;">Tài tinh sung túc</span>
        </div>
        <div style="height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden;">
          <div style="width: 20%; height: 100%; background: linear-gradient(90deg, #b91c1c, #ef4444);"></div>
        </div>
      </div>

      <div>
        <div style="display: flex; justify-content: space-between; font-size: 8pt; font-weight: bold; margin-bottom: 2px;">
          <span>🟤 THỔ (12%): Tù khí</span>
          <span style="color: #78350f;">Quan Sát quy củ</span>
        </div>
        <div style="height: 10px; background: #f1f5f9; border-radius: 5px; overflow: hidden;">
          <div style="width: 12%; height: 100%; background: linear-gradient(90deg, #78350f, #a16207);"></div>
        </div>
      </div>

    </div>
  </div>
"""
    return html

def render_dich_ly_visuals():
    html = """
  <div style="margin: 16px 0 20px 0; background: #fffdfa; border: 1.5px solid #b38728; border-radius: 8px; padding: 14px 18px;">
    <div style="text-align: center; border-bottom: 1px dashed #b38728; padding-bottom: 8px; margin-bottom: 12px;">
      <strong style="color: #8b0000; font-size: 11pt; letter-spacing: 1px;">☯ ĐỒ HÌNH DỊCH LÝ ĐÔNG PHƯƠNG: ĐẠO ÂM DƯƠNG & QUẺ MỆNH</strong>
    </div>

    <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 14px;">
      
      <!-- CÁI LY: Quẻ Ly -->
      <div style="text-align: center; width: 44%; background: #ffffff; border: 1px solid #fecaca; border-radius: 8px; padding: 12px;">
        <div style="font-weight: bold; color: #b91c1c; font-size: 10pt; margin-bottom: 6px;">
          🔥 CÁI LY: QUẺ LY (☲) • MẶT TRỜI
        </div>
        <!-- SVG Quẻ Ly: Dương - Âm - Dương -->
        <svg viewBox="0 0 120 70" width="120" height="70" style="margin: 0 auto; display: block;">
          <!-- Hào Dương trên -->
          <rect x="10" y="8" width="100" height="12" rx="3" fill="#dc2626"/>
          <!-- Hào Âm giữa -->
          <rect x="10" y="28" width="45" height="12" rx="3" fill="#dc2626"/>
          <rect x="65" y="28" width="45" height="12" rx="3" fill="#dc2626"/>
          <!-- Hào Dương dưới -->
          <rect x="10" y="48" width="100" height="12" rx="3" fill="#dc2626"/>
        </svg>
        <div style="font-size: 8pt; color: #475569; margin-top: 6px; line-height: 1.4;">
          <strong>ĐÀN ÔNG CẦN NGHĨA</strong><br>
          Quang minh chính trực, đứng thẳng như chiếc ly, tỏa sáng tri thức và ý chí kiên định.
        </div>
      </div>

      <!-- CÁI ĐĨA: Quẻ Khảm -->
      <div style="text-align: center; width: 44%; background: #ffffff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px;">
        <div style="font-weight: bold; color: #1d4ed8; font-size: 10pt; margin-bottom: 6px;">
          💧 CÁI ĐĨA: QUẺ KHẢM (☵) • MẶT TRĂNG
        </div>
        <!-- SVG Quẻ Khảm: Âm - Dương - Âm -->
        <svg viewBox="0 0 120 70" width="120" height="70" style="margin: 0 auto; display: block;">
          <!-- Hào Âm trên -->
          <rect x="10" y="8" width="45" height="12" rx="3" fill="#2563eb"/>
          <rect x="65" y="8" width="45" height="12" rx="3" fill="#2563eb"/>
          <!-- Hào Dương giữa -->
          <rect x="10" y="28" width="100" height="12" rx="3" fill="#2563eb"/>
          <!-- Hào Âm dưới -->
          <rect x="10" y="48" width="45" height="12" rx="3" fill="#2563eb"/>
          <rect x="65" y="48" width="45" height="12" rx="3" fill="#2563eb"/>
        </svg>
        <div style="font-size: 8pt; color: #475569; margin-top: 6px; line-height: 1.4;">
          <strong>ĐÀN BÀ CẦN TÌNH</strong><br>
          Nhu thuận tĩnh tại, trắng tròn như mặt trăng, chiếc đĩa nâng đỡ cái ly, dung nạp vạn vật.
        </div>
      </div>

    </div>

    <!-- Sacred Aspects SVG Mandala -->
    <div style="margin-top: 14px; text-align: center; border-top: 1px dashed #cbd5e1; padding-top: 10px;">
      <div style="font-size: 8.5pt; font-weight: bold; color: #78350f; margin-bottom: 6px;">
        🌟 SƠ ĐỒ HÌNH HỌC THIÊNG LIÊNG: TAM HỢP (VÀNG) - XUNG CHIẾU (ĐỎ) - NHỊ HỢP (XANH)
      </div>
      <svg viewBox="0 0 280 180" width="280" height="180" style="margin: 0 auto; display: block;">
        <!-- Base Circle -->
        <circle cx="140" cy="90" r="75" fill="none" stroke="#b38728" stroke-width="1.5" stroke-dasharray="3 2"/>
        
        <!-- Tam Hợp Triangle (Golden Trine) -->
        <polygon points="140,20 75,135 205,135" fill="rgba(217, 119, 6, 0.15)" stroke="#d97706" stroke-width="2"/>
        
        <!-- Xung Chiếu Line (Red Beam) -->
        <line x1="140" y1="20" x2="140" y2="160" stroke="#dc2626" stroke-width="2" stroke-dasharray="5 3"/>
        
        <!-- Nhị Hợp Arc/Line (Blue Line) -->
        <path d="M 75 135 Q 140 160 205 135" fill="none" stroke="#2563eb" stroke-width="2"/>
        
        <!-- Nodes -->
        <circle cx="140" cy="20" r="5" fill="#dc2626"/>
        <circle cx="75" cy="135" r="5" fill="#d97706"/>
        <circle cx="205" cy="135" r="5" fill="#d97706"/>
        <circle cx="140" cy="160" r="5" fill="#dc2626"/>
        
        <!-- Labels -->
        <text x="140" y="14" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">Bản Cung</text>
        <text x="140" y="172" font-size="8" font-weight="bold" fill="#dc2626" text-anchor="middle">Xung Chiếu</text>
        <text x="50" y="140" font-size="7.5" font-weight="bold" fill="#d97706" text-anchor="middle">Tam Hợp 1</text>
        <text x="230" y="140" font-size="7.5" font-weight="bold" fill="#d97706" text-anchor="middle">Tam Hợp 2</text>
      </svg>
    </div>

  </div>
"""
    return html


def load_readings_database():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "readings_database.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"weightPoems": {}, "classicalReadingsDatabase": {}, "limitReadingsDatabase": []}

def render_general_readings_html(chart_data, db):
    p = chart_data.get("personal_info", {})
    chambers = chart_data.get("chambers", [])
    
    than_chamber = next((c for c in chambers if c.get("is_than")), None)
    than_name = than_chamber.get("name", "Mệnh") if than_chamber else "Mệnh"
    than_name_upper = than_name.upper()
    
    than_trung_chau = ""
    than_dai_duc = ""
    if "PHÚC ĐỨC" in than_name_upper or "PHUC DUC" in than_name_upper:
        than_trung_chau = "Rất biết cảm thụ và hưởng thụ cuộc sống, nặng quan niệm nhân quả và phúc đức của tổ tiên."
        than_dai_duc = "Khá xem trọng hưởng thụ cá nhân, tổ hợp sao cát thì có hưởng thụ, hung thì không. Tiêu tiền cho mình, để thỏa mãn chuyện vui chơi giải trí. Trường hợp hai cung Tài Phúc đều không tốt, là một đời vất vả, cuộc sống quá buồn. Trường hợp cung Tài tốt còn cung Phúc không tốt, có tiền mà không biết xài, là đầy tớ giữ tiền. Trường hợp cung Tài không tốt mà cung Phúc tốt, biết tri túc."
    elif "MỆNH" in than_name_upper or "MENH" in than_name_upper:
        than_trung_chau = "Chủ về tính độc lập, tự lập cánh sinh, tự chịu trách nhiệm về vận mệnh cuộc đời mình."
        than_dai_duc = "Coi trọng sự tự lập, tự cường. Mọi sự thành bại đều tự tay làm nên, ít dựa dẫm vào thế lực bên ngoài."
    elif "PHU THÊ" in than_name_upper or "PHU THE" in than_name_upper:
        than_trung_chau = "Coi trọng đời sống hôn nhân, tình cảm gia đình gắn bó, chịu ảnh hưởng lớn từ bạn đời."
        than_dai_duc = "Rất nặng tình cảm, coi trọng hạnh phúc lứa đôi. Mọi sự vui buồn trong cuộc sống đều gắn liền với người bạn đời."
    elif "THIÊN DI" in than_name_upper or "THIEN DI" in than_name_upper:
        than_trung_chau = "Thích di chuyển, đi lại nhiều, cuộc sống hướng ngoại và đi xa lập nghiệp dễ thành đạt."
        than_dai_duc = "Tính cách thích bay nhảy, dịch chuyển. Thích hợp đi xa làm ăn, ngoại giao gặp nhiều may mắn lành."
    elif "QUAN LỘC" in than_name_upper or "QUAN LOC" in than_name_upper:
        than_trung_chau = "Dồn toàn tâm toàn lực cho sự nghiệp và công danh, coi công việc là mục tiêu hàng đầu cuộc sống."
        than_dai_duc = "Coi trọng công việc và sự nghiệp. Cả đời luôn bận rộn phấn đấu thăng tiến, lấy công danh làm niềm vui cuộc sống."
    elif "TÀI BẠCH" in than_name_upper or "TAI BACH" in than_name_upper:
        than_trung_chau = "Coi trọng tiền tài, thực tế và nhạy bén về tài chính, lấy của cải vật chất làm thước đo thành đạt."
        than_dai_duc = "Coi trọng giá trị vật chất và năng lực kiếm tiền. Thích quản lý tài chính và tích lũy tích trữ của cải chắc chắn."
    else:
        than_trung_chau = f"Thân cư tại cung {than_name}, thể hiện trọng tâm ý thức và phương tiện lập thân của cuộc đời gắn bó mật thiết với phương diện này."
        than_dai_duc = f"Đương số lấy phương diện cung {than_name} làm trục phát triển chính của cuộc đời, hậu vận chịu sự chi phối lớn từ các sao cư ngụ tại đây."

    lai_nhan_cung = p.get("lai_nhan_cung", "Tật Ách")
    lai_nhan_explanations = {
        "Tật Ách": "Sức khỏe, việc học hành sẽ ảnh hưởng đến cuộc đời của mệnh tạo. 'Lai nhân cung' ở tam phương của cung điền trạch (điền, huynh, tật) là cách cục nhờ vả người khác để lập nghiệp, thuộc cung vị ở trạng thái động. Lai nhân cung không ở bốn cung mệnh, tài, quan, điền thì có lợi cho người khác như anh em, vợ chồng, con cái, cha mẹ, bạn bè.",
        "Mệnh": "Lai nhân cung đóng tại Mệnh chủ về đương số tự lực lập nghiệp bằng thực lực của mình, số phận cát hung do chính mình định đoạt.",
        "Huynh Đệ": "Mối quan hệ anh em có sự nợ nần nhân duyên sâu sắc, thành bại cuộc đời có sự tương trợ hoặc chịu liên đới lớn từ anh chị em trong nhà.",
        "Phu Thê": "Hôn nhân và bạn đời ảnh hưởng cực lớn đến vận trình công danh cuộc đời, nhân duyên vợ chồng là định mệnh nghiệp quả định đoạt thành bại.",
        "Tử Tức": "Con cái và thế hệ sau là nhân duyên nghiệp quả chi phối cuộc đời đương số, dành nhiều tâm huyết và tiền của vì con cái.",
        "Tài Bạch": "Tiền tài kinh tế tài chính là nhân tố quyết định chi phối mạnh mẽ nhất vận trình cuộc đời, tự tay tạo lập nguồn tài chính độc lập lớn.",
        "Thiên Di": "Môi trường bên ngoài, đi xa làm ăn xuất ngoại chi phối sâu sắc vận mệnh đương số, có số định cư lập nghiệp hiển đạt phương xa.",
        "Nô Bộc": "Bạn bè đối tác, cấp dưới và các mối quan hệ xã giao chi phối trực tiếp định hướng và thành bại của đương số.",
        "Quan Lộc": "Sự nghiệp học thức công danh là hạt nhân chi phối toàn bộ cuộc đời, phấn đấu hết mình để giành vị trí cao trong xã hội.",
        "Điền Trạch": "Điền sản gia sản, nhà cửa đất đai là nhân quả tích lũy chi phối lớn cuộc đời, có số quy tụ điền sản thừa kế to lớn.",
        "Phúc Đức": "Phúc đức dòng họ, âm phần gia tiên và đời sống tâm linh tư tưởng chi phối sâu sắc an lành nội tâm đương số.",
        "Phụ Mẫu": "Cha mẹ và nền tảng gia đình có ảnh hưởng nhân duyên sâu sắc chi phối lớn đến sự định hình cuộc sống và học vấn thời trẻ."
    }
    lai_nhan_exp = lai_nhan_explanations.get(lai_nhan_cung, f"Lai Nhân Cung tại cung {lai_nhan_cung} mang ý nghĩa nhân quả sâu dày, là gốc rễ của những biến chuyển thăng trầm trong toàn bộ tinh bàn.")

    weight_val = p.get("weight", "4 lượng 1 chỉ")
    weight_poems = db.get("weightPoems", {})
    poem_data = weight_poems.get(weight_val, {
        "poem": "Số này suy thạnh vận không đồng\nCó sẵn kỳ tài lập dị công\nTrung niên thời vận hay thay đổi\nTừ đó tới già mạng được thông.",
        "meaning": "Đương số cuộc đời tiền vận có biến động thăng trầm lớn. Sở hữu tài năng đặc biệt tự lập nghiệp độc đáo, trung hậu vận hanh thông rực rỡ."
    })
    poem_lines = poem_data.get("poem", "").replace("\r\n", "\n").split("\n")
    poem_html = "<br>".join(poem_lines)
    poem_meaning = poem_data.get("meaning", "")

    return f"""
    <div style="margin-bottom: 20px; page-break-inside: avoid;">
      <div style="background: #801818; color: #ffffff; padding: 10px 16px; font-size: 11pt; font-weight: 700; text-align: center; letter-spacing: 1px; border-radius: 6px 6px 0 0;">
        BÌNH GIẢI TỔNG QUAN BẢN MỆNH
      </div>
      <div style="background: #ffffff; border: 1px solid #cbd5e1; border-top: none; border-radius: 0 0 6px 6px; padding: 16px 20px;">
        
        <div style="border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 10.5pt; font-weight: 700; margin-bottom: 4px;">Cung Thân cư ở cung {than_name}</div>
          <div style="font-size: 8.8pt; line-height: 1.55; color: #334155;">{than_trung_chau}</div>
          <div style="font-size: 8pt; color: #64748b; font-style: italic; text-align: right; margin-top: 6px;">Trung Châu tử vi đẩu số - Tứ Hóa Phái - Nguyễn Anh Vũ dịch</div>
        </div>

        <div style="border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 10.5pt; font-weight: 700; margin-bottom: 4px;">Cung Thân cư ở cung {than_name}</div>
          <div style="font-size: 8.8pt; line-height: 1.55; color: #334155;">{than_dai_duc}</div>
          <div style="font-size: 8pt; color: #64748b; font-style: italic; text-align: right; margin-top: 6px;">Tử vi đẩu số tinh hoa tập thành - Đại Đức Sơn Nhân</div>
        </div>

        <div style="border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; margin-bottom: 12px;">
          <div style="color: #b45309; font-size: 10.5pt; font-weight: 700; margin-bottom: 4px;">Lai Nhân Cung ở cung {lai_nhan_cung}</div>
          <div style="font-size: 8.8pt; line-height: 1.55; color: #334155;">{lai_nhan_exp}</div>
          <div style="font-size: 8pt; color: #64748b; font-style: italic; text-align: right; margin-top: 6px;">Trung Châu tử vi đẩu số - Tứ Hóa Phái - Nguyễn Anh Vũ dịch</div>
        </div>

        <div>
          <div style="color: #b45309; font-size: 10.5pt; font-weight: 700; margin-bottom: 6px;">Cân Xương Tính Số: Số {weight_val}</div>
          <div style="font-size: 9.8pt; font-style: italic; text-align: center; margin: 12px 0; font-family: 'Times New Roman', serif; line-height: 1.8; letter-spacing: 0.5px; color: #1e293b;">
            {poem_html}
          </div>
          <div style="border-left: 3px solid #d97706; padding: 6px 12px; background: #fffdf7; font-size: 8.8pt; color: #334155; border-radius: 4px;">
            <strong>Bình giải cốt cách:</strong> {poem_meaning}
          </div>
        </div>

      </div>
    </div>
    """

def render_global_tuan_triet_html(chart_data):
    chambers = chart_data.get("chambers", [])
    triet_chambers = [c for c in chambers if c.get("tuan_triet") and "Triệt" in str(c.get("tuan_triet"))]
    tuan_chambers = [c for c in chambers if c.get("tuan_triet") and "Tuần" in str(c.get("tuan_triet"))]
    
    triet_str = " và ".join([f"<strong>Cung {c.get('name')} ({c.get('chi')})</strong>" for c in triet_chambers])
    tuan_str = " và ".join([f"<strong>Cung {c.get('name')} ({c.get('chi')})</strong>" for c in tuan_chambers])
    
    return f"""
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-bottom: 20px; page-break-inside: avoid;">
      <div style="border-bottom: 1.5px solid #991b1b; padding-bottom: 6px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
        <span style="color: #991b1b; font-weight: 700; font-size: 10pt;">🛡️ CHUYÊN ĐỀ KINH ĐIỂN: LUẬN ĐOÁN TOÀN DIỆN TUẦN TRUNG & TRIỆT LỘ KHÔNG VONG</span>
        <span style="font-size: 8pt; color: #78350f; font-style: italic;">Thái Thứ Lang • Bửu Đình • Thiên Lương • Vương Đình Chi</span>
      </div>

      <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; font-size: 8.5pt; line-height: 1.55; color: #334155;">
        <strong style="color: #92400e;">☸ BẢN CHẤT CỔ THƯ VỀ HAI CỬA ẢI KHÔNG VONG:</strong>
        <p style="margin: 4px 0 0 0;">
          Trong phép toán Tử Vi Đẩu Số, <strong>Tuần Không</strong> (Tuần Trung Không Vong) và <strong>Triệt Không</strong> (Triệt Lộ Không Vong) là hai cửa ải tối thượng chi phối toàn bộ cấu trúc năng lượng của tinh bàn.
          <br>• <strong>Triệt Lộ Không Vong:</strong> Tượng là thanh đoản đao sắc bén chém ngang dòng năng lượng. Chi phối chủ đạo trong <strong>thời kỳ Tiền vận (từ 1 đến 32 tuổi)</strong>. Sau 32 tuổi, Triệt suy giảm lực cản (thoái vị), mở khóa các kho tàng bị đóng kín thuở trẻ.
          <br>• <strong>Tuần Trung Không Vong:</strong> Tượng là chiếc lồng giam giữ hoặc mây mù bao phủ. Chi phối <strong>suốt đời, tác động mạnh mẽ nhất từ Trung vận (sau 30 tuổi)</strong> trở đi, tạo nên sự tích lũy chậm rãi nhưng vững bền như bàn thạch.
        </p>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
        <div style="background: #fff5f5; border: 1px solid #fecaca; border-radius: 6px; padding: 10px 12px; font-size: 8.3pt; line-height: 1.5;">
          <strong style="color: #b91c1c;">⚔️ TRIỆT LỘ KHÔNG VONG TẠI {triet_str.upper()}:</strong>
          <p style="margin: 4px 0 0 0;">
            Triệt án ngữ tại các cung vị này giúp chém đứt hung sát khí thuở trẻ, ngăn ngừa đại nạn nhưng đồng thời làm chậm lại sự phát tiết của cát tinh trước tuổi 32. 
            Khi bước qua tuổi 32, <em>Triệt đã thoái vị</em>, giải phóng toàn bộ năng lượng tích lũy, mở đường cho tài lộc, điền sản và sự nghiệp bứt phá rực rỡ!
          </p>
        </div>
        <div style="background: #f0f7ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 10px 12px; font-size: 8.3pt; line-height: 1.5;">
          <strong style="color: #1d4ed8;">🛡️ TUẦN TRUNG KHÔNG VONG TẠI {tuan_str.upper()}:</strong>
          <p style="margin: 4px 0 0 0;">
            Tuần bao bọc như tấm khiên hộ mệnh, đóng băng hoàn toàn sát khí của các hung sát tinh hãm địa, biến hung hiểm thành bình an vô sự. 
            Tại đây, đương số tiến bước thận trọng, bền bỉ, 'dĩ tĩnh chế động', càng về hậu vận càng tích lũy được phúc lộc thọ an khang.
          </p>
        </div>
      </div>

      <div style="background: #f8fafc; border-left: 3px solid #b38728; padding: 8px 12px; border-radius: 4px; font-size: 8.2pt; line-height: 1.5; color: #334155;">
        <strong style="color: #78350f;">Quy Tắc Luận Đoán Tuần Triệt Lên Các Năm/Tháng Vận Hạn:</strong>
        <div style="margin-top: 3px;">
          • <strong>Hạn đáo cung có Triệt:</strong> Kế hoạch dễ biến động phút chót, cần chuẩn bị phương án dự phòng. Tuy nhiên nếu đang bế tắc thì Triệt chém đứt trở ngại, mở lối thoát bất ngờ.
          <br>• <strong>Hạn đáo cung có Tuần:</strong> Mọi sự tiến triển chậm rãi, chớ nên nóng vội thúc ép. Tuần che chở khỏi tai bay vạ gió, giúp tai qua nạn khỏi.
        </div>
      </div>
    </div>
    """

def render_chamber_classical_readings_html(chamber, db):
    cid = chamber.get('id', '')
    cr_db = db.get('classicalReadingsDatabase', {})
    items = cr_db.get(cid, [])
    
    stars = chamber.get('chinh_tinh', []) + chamber.get('cat_tinh', []) + chamber.get('hung_tinh', [])
    resides = [s.get('name', '').upper().replace('(', '').replace(')', '').strip() for s in stars]
    
    html = ""
    matched_count = 0
    for it in items:
        req_stars = [s.upper().strip() for s in it.get('stars', [])]
        if all(s in resides for s in req_stars):
            matched_count += 1
            title = it.get('title', '').replace('[Chi]', chamber.get('chi', ''))
            text = it.get('text', '')
            source = it.get('source', '')
            html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #0284c7; border-radius: 4px; padding: 7px 11px; margin-bottom: 7px;">
          <div style="color: #0369a1; font-weight: 700; font-size: 8.8pt; margin-bottom: 3px;">{title}</div>
          <div style="font-size: 8.2pt; line-height: 1.48; color: #334155;">{text}</div>
          <div style="font-size: 7.5pt; color: #64748b; font-style: italic; text-align: right; margin-top: 3px;">{source}</div>
        </div>
"""
    if matched_count == 0:
        main_star_names = ", ".join([s.get('name', '') for s in chamber.get('chinh_tinh', [])])
        if main_star_names:
            title = f"Cung {chamber.get('name')} an tại {chamber.get('chi')} có chính tinh {main_star_names}"
            text = f"Đương số chịu sự chi phối và ảnh hưởng chính của tinh hệ {main_star_names} tọa thủ tại bản cung, mang năng lượng đặc trưng quy định trực tiếp hoạt động của phương diện này."
        else:
            title = f"Cung {chamber.get('name')} an tại {chamber.get('chi')} Vô Chính Diệu"
            text = "Cung vị trống trải không có chính tinh trực tiếp cai quản, dễ bị dao động và thu hút 100% năng lượng xung chiếu từ cung vị đối diện dội sang để gánh vác hoạt động."
        source = "Nghiên cứu tinh mệnh học - Biên soạn tổng hợp"
        html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #64748b; border-radius: 4px; padding: 7px 11px; margin-bottom: 7px;">
          <div style="color: #475569; font-weight: 700; font-size: 8.8pt; margin-bottom: 3px;">{title}</div>
          <div style="font-size: 8.2pt; line-height: 1.48; color: #334155;">{text}</div>
          <div style="font-size: 7.5pt; color: #64748b; font-style: italic; text-align: right; margin-top: 3px;">{source}</div>
        </div>
"""
    return html

def render_daivan_limits_html(chart_data, db):
    p = chart_data.get("personal_info", {})
    chambers = chart_data.get("chambers", [])
    age = p.get("age", 32)
    name = p.get("name", "Đương số")
    
    # Current Dai van
    cur_chamber = next((c for c in chambers if c.get("dai_han", 0) <= age <= c.get("dai_han", 0) + 9), chambers[0])
    start_age = cur_chamber.get("dai_han", 0)
    end_age = start_age + 9
    
    # Look up limit readings
    limit_db = db.get("limitReadingsDatabase", [])
    stars = cur_chamber.get("chinh_tinh", []) + cur_chamber.get("cat_tinh", []) + cur_chamber.get("hung_tinh", [])
    star_names = [s.get("name", "").upper().replace("(", "").replace(")", "").strip() for s in stars]
    if cur_chamber.get("tuan_triet"):
        tt = cur_chamber.get("tuan_triet")
        if "Tuần" in tt: star_names.append("TUẦN")
        if "Triệt" in tt: star_names.append("TRIỆT")
        
    matched_limits = []
    for it in limit_db:
        req = [s.upper().strip() for s in it.get("stars", [])]
        if all(s in star_names for s in req):
            matched_limits.append(it)
            
    limits_html = ""
    for it in matched_limits[:6]: # top matched
        limits_html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #7c3aed; border-radius: 4px; padding: 7px 11px; margin-bottom: 7px;">
          <div style="color: #6d28d9; font-weight: 700; font-size: 8.8pt; margin-bottom: 3px;">{it.get('title', '')}</div>
          <div style="font-size: 8.2pt; line-height: 1.48; color: #334155;">{it.get('text', '')}</div>
          <div style="font-size: 7.5pt; color: #64748b; font-style: italic; text-align: right; margin-top: 3px;">{it.get('source', '')}</div>
        </div>
"""
    if not limits_html:
        limits_html = f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 3px solid #7c3aed; border-radius: 4px; padding: 7px 11px; margin-bottom: 7px;">
          <div style="color: #6d28d9; font-weight: 700; font-size: 8.8pt; margin-bottom: 3px;">Đại vận {start_age} - {end_age} tuổi tại cung {cur_chamber.get('name')} ({cur_chamber.get('chi')})</div>
          <div style="font-size: 8.2pt; line-height: 1.48; color: #334155;">Đại vận đương thời bước vào giai đoạn then chốt, chịu sự chi phối mạnh mẽ của tinh hệ tọa thủ và hội chiếu. Cần nắm bắt cơ hội thiên thời địa lợi, vững vàng định hướng sự nghiệp.</div>
          <div style="font-size: 7.5pt; color: #64748b; font-style: italic; text-align: right; margin-top: 3px;">Tử vi đẩu số toàn thư - Khảo cứu đại vận</div>
        </div>
"""

    # Table of 10 Dai Vans
    sorted_chambers = sorted(chambers, key=lambda x: x.get("dai_han", 0))
    table_rows = ""
    for c in sorted_chambers[:10]:
        c_start = c.get("dai_han", 0)
        c_end = c_start + 9
        is_cur = (c_start <= age <= c_end)
        highlight = "background: #fef3c7; font-weight: bold;" if is_cur else ""
        cur_badge = " <span style='color: #b45309; font-size: 7.5pt; font-weight: bold;'>[ĐANG TRẢI QUA]</span>" if is_cur else ""
        chinh_stars = ", ".join([s.get('name') for s in c.get('chinh_tinh', [])]) or "Vô Chính Diệu"
        table_rows += f"""
        <tr style="{highlight}">
          <td><strong>{c_start} - {c_end} tuổi</strong>{cur_badge}</td>
          <td><strong>Cung {c.get('name')} ({c.get('chi')})</strong></td>
          <td>{chinh_stars}</td>
          <td>{c.get('tuan_triet', 'Không')}</td>
        </tr>
"""

    return f"""
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 14px 18px; margin-top: 14px; page-break-inside: avoid;">
      <h3 style="color: #6d28d9; font-size: 10pt; margin: 0 0 8px 0; border-bottom: 1.5px solid #6d28d9; padding-bottom: 4px;">
        ⏳ ĐẠI VẬN ĐƯƠNG THỜI: {start_age} - {end_age} TUỔI TẠI CUNG {cur_chamber.get('name').upper()} ({cur_chamber.get('chi').upper()})
      </h3>
      <p style="font-size: 8.5pt; line-height: 1.5; color: #334155; margin-bottom: 10px;">
        Đương số <strong>{name}</strong> hiện đang bước trong Đại vận <strong>{start_age} - {end_age} tuổi</strong> đóng tại <strong>Cung {cur_chamber.get('name')}</strong> ở phương vị <strong>{cur_chamber.get('chi')}</strong>. Đây là thập niên chuyển mình then chốt quyết định vị thế sự nghiệp, gia đạo và nền tảng tích lũy tài chính.
      </p>
      
      <div style="margin-bottom: 12px;">
        <strong style="color: #4c1d95; font-size: 8.8pt; display: block; margin-bottom: 6px;">✨ Luận Giải Tinh Đẩu Tọa Thủ & Chiếu Hạn Trong Đại Vận:</strong>
        {limits_html}
      </div>

      <strong style="color: #4c1d95; font-size: 8.8pt; display: block; margin: 10px 0 6px 0;">📊 Bảng Tiến Trình 10 Thập Niên Đại Vận Toàn Đời:</strong>
      <table class="data-table" style="font-size: 8pt;">
        <thead>
          <tr>
            <th>Giai Đoạn Tuổi</th>
            <th>Cung Vị Trấn Thủ</th>
            <th>Chính Tinh Cai Quản</th>
            <th>Tuần / Triệt</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>
"""

def generate_pdf_book(chart_data, output_pdf_path):
    # Encode QR code as base64 data URI for closing page
    qr_data_uri = ""
    qr_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr_payment.png")
    if os.path.exists(qr_img_path):
        try:
            with open(qr_img_path, "rb") as qrf:
                b64_str = base64.b64encode(qrf.read()).decode("utf-8")
                qr_data_uri = f"data:image/png;base64,{b64_str}"
        except Exception as qr_err:
            print("Warning loading QR code image:", qr_err)

    output_pdf_path = os.path.abspath(output_pdf_path)
    readings_db = load_readings_database()
    p = chart_data.get("personal_info", {})
    chambers = chart_data.get("chambers", [])
    bazi = chart_data.get("bazi", {})
    pillars = bazi.get("pillars", {})
    
    name = p.get("name", "Đương Số")
    gender = p.get("gender", "Nam")
    lunar_year = p.get("birth_year_lunar", "")
    solar_year = p.get("birth_year_solar", 1995)
    solar_date_str = f"{p.get('birth_day_solar', 18):02d}/{p.get('birth_month_solar', 9):02d}/{solar_year}"
    lunar_date_str = f"Ngày {p.get('birth_day_lunar', 24)} tháng {p.get('birth_month_lunar', 8)} năm {lunar_year}"
    hour_str = f"{p.get('birth_hour', 'Giờ Mùi')} ({p.get('birth_hour_stem', 'Đinh Mùi')})"
    elem_fate = p.get("element_fate", "Sơn Đầu Hỏa")
    elem_cuc = p.get("element_cuc", "Thổ Ngũ Cục")
    relation = p.get("relation_fate_cuc", "Mệnh sinh Cục")
    weight = p.get("weight", "4 lượng 1 chỉ")
    fate_lord = p.get("fate_lord", "Cự Môn")
    body_lord = p.get("body_lord", "Thiên Cơ")
    lai_nhan = p.get("lai_nhan_cung", "Tật Ách")
    analysis_year = p.get("analysis_year_solar", 2026)
    analysis_lunar = p.get("analysis_year_lunar", "Bính Ngọ")
    age = p.get("age", 32)
    
    # Bát tự Pillars extraction
    y_p = pillars.get('year', {})
    m_p = pillars.get('month', {})
    d_p = pillars.get('day', {})
    h_p = pillars.get('hour', {})
    
    day_master = bazi.get('day_master', d_p.get('can', 'Nhâm'))
    day_master_elem = bazi.get('day_master_elem', d_p.get('can_elem', 'Thủy'))
    vuong_suy = bazi.get('vuong_suy', 'Được sinh (Tướng)')
    
    # Generate HTML Book Document
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Tử Vi & Tứ Trụ Toàn Thư - {name}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
    @bottom-center {{
      content: counter(page);
      font-size: 8.5pt;
      color: #718096;
      font-family: 'Times New Roman', serif;
    }}
  }}
  
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1a202c;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}
  
  .page-break {{
    page-break-after: always;
    break-after: page;
  }}
  
  /* ================= BOOK COVER ================= */
  .cover-container {{
    height: 94vh;
    border: 4px double #b38728;
    padding: 24px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    background: radial-gradient(circle at 50% 50%, #fffdfa 0%, #f7f3e8 100%);
  }}
  
  .cover-ornament {{
    color: #b38728;
    font-size: 26pt;
    letter-spacing: 6px;
  }}
  
  .cover-sub {{
    font-size: 11pt;
    font-weight: bold;
    letter-spacing: 3px;
    color: #991b1b;
    text-transform: uppercase;
  }}
  
  .cover-title {{
    font-size: 25pt;
    font-weight: bold;
    color: #8b0000;
    margin: 14px 0 8px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
  }}
  
  .cover-name {{
    font-size: 22pt;
    font-weight: bold;
    color: #1a202c;
    border-bottom: 2px solid #b38728;
    padding-bottom: 6px;
    margin-bottom: 12px;
    display: inline-block;
  }}
  
  .cover-info-table {{
    margin: 15px auto;
    border-collapse: collapse;
    width: 85%;
    font-size: 10.5pt;
    text-align: left;
  }}
  .cover-info-table td {{
    padding: 4px 10px;
    border-bottom: 1px dashed rgba(179, 135, 40, 0.4);
  }}
  .cover-info-table td:first-child {{
    font-weight: bold;
    color: #78350f;
    width: 40%;
  }}
  
  .cover-footer {{
    font-size: 9pt;
    color: #64748b;
    font-style: italic;
    letter-spacing: 1px;
  }}

  /* ================= TABLE OF CONTENTS ================= */
  .toc-title {{
    font-size: 18pt;
    font-weight: bold;
    color: #8b0000;
    text-align: center;
    text-transform: uppercase;
    border-bottom: 2px solid #b38728;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }}
  
  .toc-item {{
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    font-size: 10.5pt;
    border-bottom: 1px dotted #cbd5e1;
  }}
  .toc-part {{
    font-weight: bold;
    color: #991b1b;
  }}

  /* ================= CHAPTER STYLES ================= */
  .chapter-header {{
    font-size: 15pt;
    font-weight: bold;
    color: #8b0000;
    text-transform: uppercase;
    border-bottom: 2px solid #b38728;
    padding-bottom: 6px;
    margin-top: 10px;
    margin-bottom: 12px;
  }}
  
  .section-header {{
    font-size: 12pt;
    font-weight: bold;
    color: #78350f;
    margin-top: 14px;
    margin-bottom: 8px;
    border-left: 4px solid #b38728;
    padding-left: 8px;
  }}

  /* 4x4 TUVI GRID STYLES */
  .tuvi-grid-page {{
    page-break-inside: avoid;
    height: 100%;
  }}
  .tuvi-grid-frame {{
    border: 3px double #b38728;
    border-radius: 8px;
    padding: 4px;
    background: #fffdfa;
    box-sizing: border-box;
    height: 980px;
  }}
  .tuvi-grid-inner {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 4px;
    height: 100%;
  }}
  .grid-cell {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 5px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
    overflow: hidden;
  }}
  .cell-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px dashed #e2e8f0;
    padding-bottom: 3px;
  }}
  .cell-cung-name {{
    font-weight: bold;
    font-size: 8.5pt;
    letter-spacing: 0.5px;
  }}
  .cell-can-chi {{
    font-size: 7.5pt;
    color: #475569;
    font-weight: bold;
  }}
  .cell-limits {{
    text-align: right;
    font-size: 7pt;
    color: #64748b;
  }}
  .cell-limit-tag {{
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
  }}
  .cell-badge-than {{
    background: #dc2626;
    color: #ffffff;
    font-weight: bold;
    font-size: 6.5pt;
    padding: 1px 3px;
    border-radius: 2px;
    margin-right: 2px;
  }}
  .cell-badge-triet {{
    background: #ef4444;
    color: #ffffff;
    font-size: 7pt;
    font-weight: bold;
    padding: 1px 4px;
    border-radius: 2px;
  }}
  .cell-badge-tuan {{
    background: #3b82f6;
    color: #ffffff;
    font-size: 7pt;
    font-weight: bold;
    padding: 1px 4px;
    border-radius: 2px;
  }}
  .cell-chinh-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 3px 0;
  }}
  .cell-chinh-text {{
    color: #8b0000;
    font-weight: bold;
    font-size: 8.5pt;
  }}
  .cell-stars-area {{
    display: flex;
    justify-content: space-between;
    gap: 4px;
    font-size: 7pt;
    flex-grow: 1;
  }}
  .cell-stars-col {{
    display: flex;
    flex-direction: column;
    gap: 2px;
    width: 49%;
  }}
  .pill-cat {{
    color: #15803d;
    background: #f0fdf4;
    padding: 1px 3px;
    border-radius: 2px;
    display: inline-block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .pill-hung {{
    color: #b91c1c;
    background: #fef2f2;
    padding: 1px 3px;
    border-radius: 2px;
    display: inline-block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .pill-luu {{
    color: #6d28d9;
    background: #f5f3ff;
    padding: 1px 3px;
    border-radius: 2px;
    display: inline-block;
    font-weight: bold;
  }}
  .cell-footer {{
    border-top: 1px dashed #e2e8f0;
    padding-top: 2px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .cell-luu-row {{
    font-size: 6.8pt;
    color: #6d28d9;
  }}
  .cell-trang-sinh {{
    font-size: 7pt;
    color: #64748b;
    font-weight: bold;
  }}

  /* CENTER PANEL */
  .grid-center-panel {{
    background: #ffffff;
    border: 2px solid #b38728;
    border-radius: 6px;
    padding: 10px 14px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
  }}
  .center-watermark-lotus {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 110pt;
    color: rgba(179, 135, 40, 0.05);
    pointer-events: none;
    z-index: 1;
  }}
  .center-info-grid {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    position: relative;
    z-index: 2;
  }}
  .center-info-grid td {{
    padding: 3px 6px;
    border-bottom: 1px dotted #e2e8f0;
  }}
  .center-info-grid td:nth-child(odd) {{
    color: #78350f;
    font-weight: bold;
    width: 25%;
  }}

  /* BAZI PILLAR CARDS */
  .bazi-pillar-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    text-align: center;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}
  .bazi-pillar-header {{
    background: var(--color-gold-light, #fef3c7);
    color: #78350f;
    font-weight: bold;
    font-size: 8pt;
    padding: 4px;
    border-bottom: 1px solid #e2e8f0;
  }}
  .bazi-pillar-can {{
    font-size: 12pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 4px;
  }}
  .bazi-pillar-chi {{
    font-size: 12pt;
    font-weight: bold;
    color: #1e293b;
  }}
  .bazi-god {{
    font-size: 7.5pt;
    font-weight: normal;
    color: #64748b;
  }}
  .bazi-pillar-tang {{
    font-size: 7.5pt;
    color: #475569;
    padding: 2px 4px;
    background: #f8fafc;
    border-top: 1px dashed #e2e8f0;
  }}
  .bazi-pillar-trang {{
    font-size: 7.5pt;
    color: #b45309;
    font-weight: bold;
    padding: 2px;
  }}
  .bazi-pillar-nap {{
    font-size: 7pt;
    color: #991b1b;
    background: #fef2f2;
    padding: 2px;
  }}

  /* DATA TABLES */
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
  }}
  .data-table th {{
    background: #fef3c7;
    color: #78350f;
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    text-align: left;
    font-weight: bold;
  }}
  .data-table td {{
    border: 1px solid #cbd5e1;
    padding: 5px 8px;
    vertical-align: top;
  }}

  /* 4-WAY ASPECT BOX FOR MONTHS IN PDF */
  .pdf-aspect-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-top: 6px;
    margin-bottom: 8px;
  }}
  .pdf-aspect-card {{
    background: #ffffff;
    border-radius: 6px;
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    font-size: 8pt;
    line-height: 1.45;
  }}
  .pdf-aspect-card-toathu {{ border-left: 3px solid #7c3aed; background: #faf5ff; }}
  .pdf-aspect-card-xungchieu {{ border-left: 3px solid #dc2626; background: #fef2f2; }}
  .pdf-aspect-card-tamhop {{ border-left: 3px solid #d97706; background: #fffbeb; }}
  .pdf-aspect-card-nhihop {{ border-left: 3px solid #2563eb; background: #eff6ff; }}

  .quote-box {{
    background: #fffdfa;
    border-left: 3px solid #b38728;
    padding: 8px 12px;
    margin: 8px 0;
    font-style: italic;
    color: #78350f;
    border-radius: 0 4px 4px 0;
  }}
</style>
</head>
<body>

  <!-- ================= TRANG BÌA ================= -->
  <div class="page-break">
    <div class="cover-container">
      <div class="cover-ornament">☸ ☯ ☸</div>
      <div>
        <div class="cover-sub">ĐẠI ĐẠO HUYỀN CƠ • THIÊN ĐỊA NHÂN TOÀN THƯ</div>
        <div class="cover-title">TỬ VI & TỨ TRỤ TOÀN THƯ</div>
        <div style="font-size: 13pt; color: #475569; margin-bottom: 12px;">KHẢO LUẬN VẬN MỆNH TRỌN ĐỜI & LƯU NIÊN 2026</div>
        <div class="cover-name">{name.upper()}</div>
      </div>
      
      <table class="cover-info-table">
        <tr><td>Giới tính:</td><td><strong>{gender}</strong></td></tr>
        <tr><td>Ngày sinh Dương lịch:</td><td><strong>{solar_date_str}</strong></td></tr>
        <tr><td>Ngày sinh Âm lịch:</td><td><strong>{lunar_date_str}</strong></td></tr>
        <tr><td>Giờ sinh:</td><td><strong>{hour_str}</strong></td></tr>
        <tr><td>Bản Mệnh / Nạp Âm:</td><td><strong>{elem_fate}</strong></td></tr>
        <tr><td>Cục / Ngũ Hành:</td><td><strong>{elem_cuc} ({relation})</strong></td></tr>
        <tr><td>Chủ Mệnh / Chủ Thân:</td><td><strong>{fate_lord} / {body_lord}</strong></td></tr>
        <tr><td>Lượng số (Cân Xương):</td><td><strong>{weight}</strong></td></tr>
        <tr><td>Lai Nhân Cung:</td><td><strong>Cung {lai_nhan}</strong></td></tr>
        <tr><td>Lưu Niên Khảo Khảo:</td><td><strong>Năm {analysis_year} ({analysis_lunar}) • {age} Tuổi</strong></td></tr>
      </table>
      
      <div>
        <div class="cover-ornament" style="font-size: 18pt;">✤ ✥ ✤</div>
        <div class="cover-footer">
          Biên soạn theo tinh hoa Tử Vi Đẩu Số Kinh Điển & Bát Tự Tứ Trụ Đông Phương<br>
          Bản quyền thuộc về Viện Cổ Học Ứng Dụng & Trí Tuệ Nhân Tạo
        </div>
      </div>
    </div>
  </div>

  <!-- ================= MỤC LỤC ================= -->
  <div class="page-break">
    <div class="toc-title">MỤC LỤC TOÀN THƯ</div>
    
    <div class="toc-item"><span class="toc-part">HÌNH ẢNH TOÀN CẢNH LÁ SỐ TỬ VI ĐẨU SỐ 12 CUNG</span><span>Trang 3</span></div>
    <div class="toc-item"><span class="toc-part">PHẦN I: TỔNG QUAN BẢN MỆNH & BÁT TỰ TIÊN THIÊN</span><span>Trang 4</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.1 Khảo Sát Tứ Trụ Bát Tự Tiên Thiên</span><span>Trang 4</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.2 Cục Mệnh Tương Quan & Cân Lượng Xương Cốt</span><span>Trang 4</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>1.3 Sơ Đồ Hình Học Thiêng Liêng Tam Hợp - Xung Chiếu - Nhị Hợp</span><span>Trang 5</span></div>
    
    <div class="toc-item"><span class="toc-part">PHẦN II: TOÀN THƯ BÀN LUẬN GIẢI CHI TIẾT (KINH ĐIỂN CỔ THƯ & TỨ PHÁI)</span><span>Trang 6</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.1 Bình Giải Tổng Quan Bản Mệnh (Thân Cư, Lai Nhân Cung, Cân Xương Tính Số)</span><span>Trang 6</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.2 Chuyên Khảo Kinh Điển: Luận Đoán Toàn Diện Tuần Trung & Triệt Lộ Không Vong</span><span>Trang 7</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.3 Bình Giải Chi Tiết 12 Cung Vị (Toàn Bộ Tinh Đẩu Tọa Thủ & Tương Tác Cách Cục)</span><span>Trang 8</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>2.4 Bình Giải Thập Niên Đại Vận & Khảo Đoán Vận Mệnh Toàn Đời</span><span>Trang 22</span></div>
    
    <div class="toc-item"><span class="toc-part">PHẦN III: BÁT TỰ TỨ TRỤ TOÀN THƯ & ĐỊNH LƯỢNG NGŨ HÀNH</span><span>Trang 16</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.1 Đồ Hình Tứ Trụ & Biểu Đồ Năng Lượng Ngũ Hành</span><span>Trang 16</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.2 Bản Thể Nhật Chủ & Tương Tác Lệnh Tháng</span><span>Trang 17</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.3 Cấu Trúc Bát Trụ Toàn Diện (Thai, Mệnh, Tức, Phút)</span><span>Trang 18</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.4 Thập Thần Đa Chiều, Thần Sát & Vòng Tràng Sinh</span><span>Trang 19</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>3.5 Dụng Thần, Hỷ Thần & Định Hướng Phong Thủy Hành Mệnh</span><span>Trang 20</span></div>
    
    <div class="toc-item"><span class="toc-part">PHẦN IV: VẬN HẠN 12 THÁNG LƯU NIÊN & LƯU NGUYỆT MỆNH CUNG</span><span>Trang 21</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.1 Đại Vận Hiện Tại & Tổng Quan Lưu Niên {analysis_year} ({analysis_lunar})</span><span>Trang 21</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.2 Bảng Ma Trận Khảo Sát 12 Tháng Âm Lịch (Hội Chiếu & Sao Lưu)</span><span>Trang 22</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>4.3 Khảo Luận Chuyên Sâu Tương Tác 4 Chiều (Tọa Thủ - Xung - Tam Hợp - Nhị Hợp)</span><span>Trang 23</span></div>
    
    <div class="toc-item"><span class="toc-part">PHẦN V: KHO TÀNG DỊCH LÝ ĐÔNG PHƯƠNG & ĐẠO HÀNH ĐỜI</span><span>Trang 28</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.1 Đồ Hình Dịch Lý: Đàn Ông Cái Ly (Quẻ Ly) - Đàn Bà Cái Đĩa (Quẻ Khảm)</span><span>Trang 28</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.2 Đạo Vợ Chồng, Hôn Nhân & Bí Pháp Đi Xa Hóa Giải Xung Khắc</span><span>Trang 29</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.3 Cung Tử Tức: Quý Tử & Đạo Làm Cha Mẹ (Cây Cau Kinh Luân)</span><span>Trang 30</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.4 Sấm Cơ Dịch Học & Dự Báo Thời Vận (Kinh Đô & Long Mạch)</span><span>Trang 31</span></div>
    <div class="toc-item" style="padding-left: 15px;"><span>5.5 Đạo Hành Đời: Tâm Đức Thắng Số</span><span>Trang 32</span></div>
  </div>

  <!-- ================= BÀN CỜ LÁ SỐ TỬ VI TOÀN CẢNH (VISUAL 4x4) ================= -->
  {render_tuvi_grid_page(chart_data)}

  <!-- ================= PHẦN I: TỔNG QUAN BẢN MỆNH ================= -->
  <div class="page-break">
    <h2 class="chapter-header">PHẦN I: TỔNG QUAN BẢN MỆNH & BÁT TỰ TIÊN THIÊN</h2>
    
    <h3 class="section-header">1.1 Khảo Sát Bát Tự Tiên Thiên (Bảng 4 Trụ)</h3>
    <p>
      Bát tự Tứ Trụ đại diện cho nguyên khí Tiên Thiên khi con người cất tiếng khóc chào đời. Bốn trụ Năm, Tháng, Ngày, Giờ cấu thành nên ma trận năng lượng Ngũ Hành tương sinh tương khắc, định hình tính cách và nền tảng phúc khí của đương số:
    </p>
    
    <table class="data-table">
      <thead>
        <tr>
          <th>Trụ Bản Mệnh</th>
          <th>Thiên Can</th>
          <th>Địa Chi</th>
          <th>Thập Thần Chính</th>
          <th>Tàng Can & Thập Thần Ẩn</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Trụ Năm</strong></td>
          <td><strong>{y_p.get('can', '')}</strong> ({y_p.get('can_elem', '')})</td>
          <td><strong>{y_p.get('chi', '')}</strong> ({y_p.get('chi_elem', '')})</td>
          <td>{y_p.get('can_ten_god', 'N/A')}</td>
          <td>{y_p.get('hidden_can', '')} ({y_p.get('hidden_ten_god', '')})</td>
        </tr>
        <tr>
          <td><strong>Trụ Tháng</strong></td>
          <td><strong>{m_p.get('can', '')}</strong> ({m_p.get('can_elem', '')})</td>
          <td><strong>{m_p.get('chi', '')}</strong> ({m_p.get('chi_elem', '')})</td>
          <td>{m_p.get('can_ten_god', 'N/A')}</td>
          <td>{m_p.get('hidden_can', '')} ({m_p.get('hidden_ten_god', '')})</td>
        </tr>
        <tr>
          <td><strong>Trụ Ngày</strong></td>
          <td><strong>{d_p.get('can', '')}</strong> ({d_p.get('can_elem', '')})</td>
          <td><strong>{d_p.get('chi', '')}</strong> ({d_p.get('chi_elem', '')})</td>
          <td><strong>Nhật Chủ (Bản Thân)</strong></td>
          <td>{d_p.get('hidden_can', '')} ({d_p.get('hidden_ten_god', '')})</td>
        </tr>
        <tr>
          <td><strong>Trụ Giờ</strong></td>
          <td><strong>{h_p.get('can', '')}</strong> ({h_p.get('can_elem', '')})</td>
          <td><strong>{h_p.get('chi', '')}</strong> ({h_p.get('chi_elem', '')})</td>
          <td>{h_p.get('can_ten_god', 'N/A')}</td>
          <td>{h_p.get('hidden_can', '')} ({h_p.get('hidden_ten_god', '')})</td>
        </tr>
      </tbody>
    </table>

    <h3 class="section-header">1.2 Cục Mệnh Tương Quan & Cân Lượng Xương Cốt</h3>
    <p>
      • <strong>Mệnh:</strong> {elem_fate} | <strong>Cục:</strong> {elem_cuc}. Mối quan hệ giữa Mệnh và Cục: <em>{relation}</em>. Người có mối quan hệ này thường sống bao dung, biết dung hòa hoàn cảnh xung quanh, đi đến đâu cũng gây dựng được uy tín và sự nể trọng.
    </p>
    <p>
      • <strong>Lượng số (Phép cân xương tính số của Lão Tử / Viên Triệt Cương):</strong> {weight}. 
      Số này đắc cách trung thượng, người có chí khí thanh cao, tự lực cánh sinh, tiền vận tích lũy học vấn, trung hậu vận hưởng phúc lộc điền trạch và con cháu vinh hoa.
    </p>
    <p>
      • <strong>Sao Cai Quản:</strong> Chủ Mệnh là sao <strong>{fate_lord}</strong>, Chủ Thân là sao <strong>{body_lord}</strong>. Hai vị chủ tinh này chi phối tư duy, hành động và khả năng thích ứng cơ biến suốt đường đời của đương số.
    </p>
    <p>
      • <strong>Lai Nhân Cung:</strong> Tại cung <strong>{lai_nhan}</strong>. Lai Nhân Cung là nơi kết tinh nhân duyên và nghiệp lực sâu đậm nhất từ tiền kiếp đưa sang đời này, là chìa khóa mở ra động lực hành động và bước ngoặt cuộc đời.
    </p>
  </div>

  <!-- ================= PHẦN II: TOÀN THƯ BÀN LUẬN GIẢI CHI TIẾT ================= -->
  <div class="page-break">
    <h2 class="chapter-header">PHẦN II: TOÀN THƯ BÀN LUẬN GIẢI CHI TIẾT (KINH ĐIỂN CỔ THƯ & TỨ PHÁI)</h2>
    
    <!-- 2.1 BÌNH GIẢI TỔNG QUAN BẢN MỆNH -->
    {render_general_readings_html(chart_data, readings_db)}

    <!-- 2.2 CHUYÊN ĐỀ TUẦN TRUNG & TRIỆT LỘ KHÔNG VONG -->
    {render_global_tuan_triet_html(chart_data)}

    <!-- 2.3 BÌNH GIẢI CHI TIẾT 12 CUNG VỊ -->
    <div style="background: #801818; color: #ffffff; padding: 10px 16px; font-size: 11pt; font-weight: 700; text-align: center; letter-spacing: 1px; border-radius: 6px; margin: 20px 0 14px 0;">
      BÌNH GIẢI CHI TIẾT 12 CUNG VỊ (TỪNG TINH ĐẨU TỌA THỦ THEO KINH ĐIỂN CỔ THƯ)
    </div>
    <p style="font-size: 8.5pt; color: #475569; margin-bottom: 12px; font-style: italic;">
      Dưới đây là phần khảo luận chi tiết nguyên văn từ các đại tông sư tinh mệnh học (Trung Châu phái, Đại Đức Sơn Nhân, Phan Tử Ngư, Vân Đằng Thái Thứ Lang...) phân tích sâu từng tinh hệ tọa thủ kết hợp tương tác cách cục đa chiều:
    </p>
"""

    for c in chambers:
        cid = c.get("id", "")
        cname = c.get("name", "")
        cchi = c.get("chi", "")
        ccan = c.get("can", "")
        celem = c.get("element", "")
        is_than = c.get("is_than", False)
        
        asp = CHI_ASPECTS.get(cchi, {"tam_hop": ["Ngọ", "Tuất"], "xung_chieu": "Thân", "nhi_hop": "Hợi"})
        xc_cung = next((item for item in chambers if item.get("chi") == asp["xung_chieu"]), chambers[0])
        th1_cung = next((item for item in chambers if item.get("chi") == asp["tam_hop"][0]), chambers[0])
        th2_cung = next((item for item in chambers if item.get("chi") == asp["tam_hop"][1]), chambers[0])
        nh_cung = next((item for item in chambers if item.get("chi") == asp["nhi_hop"]), chambers[0])

        chinh, cat, hung, luu, luu_list = extract_chamber_stars_for_pdf(c)
        treatise = get_dynamic_classical_treatise(c, p)
        
        bd = treatise.get("buu_dinh", "Đang cập nhật bình giải.")
        dd = treatise.get("dai_duc", "Đang cập nhật bình giải.")
        tl = treatise.get("thien_luong", "Đang cập nhật bình giải.")
        tc = treatise.get("trung_chau", "Đang cập nhật bình giải.")
        
        than_tag = " • [THÂN CƯ TẠI ĐÂY]" if is_than else ""
        nguyet_han_val = c.get('nguyet_han', 1)
        tt_val = c.get('tuan_triet', 'Không')
        tt_note = ""
        if tt_val and "Triệt" in str(tt_val):
            tt_note = "<div style='font-size: 8.5pt; color: #991b1b; background: #fff1f2; padding: 4px 8px; border-radius: 4px; margin: 4px 0;'><strong>🛡️ Tác động Triệt:</strong> Chi phối mạnh tiền vận (≤ 32 tuổi), làm mờ ánh sáng cát tinh nhưng triệt tiêu toàn bộ hung sát tinh. Bước qua tuổi 32, Triệt thoái vị mở khóa tiềm năng rực rỡ!</div>"
        elif tt_val and "Tuần" in str(tt_val):
            tt_note = "<div style='font-size: 8.5pt; color: #1e40af; background: #eff6ff; padding: 4px 8px; border-radius: 4px; margin: 4px 0;'><strong>🛡️ Tác động Tuần:</strong> Bao bọc suốt đời, tác động mạnh sau 30 tuổi. Làm chậm tiến độ để tích lũy bền vững, đóng băng sát khí hung tinh, giữ gìn bình an trọn vẹn.</div>"
        
        # Combinations logic
        combos = analyze_star_combinations_python(c, xc_cung, th1_cung, th2_cung, nh_cung, name)
        combos_html = ""
        if combos:
            combos_html = """
        <div style="background: #fffdfa; border: 1px solid #fef3c7; border-left: 3px solid #f59e0b; border-radius: 4px; padding: 6px 10px; margin: 6px 0;">
          <strong style="color: #b45309; font-size: 8.5pt;">✨ TƯƠNG TÁC CÁCH CỤC & CẶP SAO LIÊN KẾT:</strong>
          <ul style="margin: 4px 0 0 14px; padding: 0; font-size: 8pt; line-height: 1.45;">
"""
            for cb in combos:
                combos_html += f"<li><strong>{cb['title']}:</strong> {cb['desc']}</li>"
            combos_html += """
          </ul>
        </div>
"""
        
        cung_desc = CHAMBER_DESCS.get(cid, "Cung vị phản ánh khía cạnh quan trọng của đời người.")
        tt_span = f'<span style="color: #dc2626; font-weight: bold;">[{tt_val}]</span>' if tt_val != 'Không' else ''

        html_content += f"""
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; margin-bottom: 12px; page-break-inside: avoid;">
      <div style="border-bottom: 1px dashed #cbd5e1; padding-bottom: 4px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
        <strong style="color: #8b0000; font-size: 10pt;">CUNG {cname.upper()} ({ccan} {cchi} - Hành {celem}){than_tag} • [Tháng {nguyet_han_val} ÂL]</strong>
        <span style="font-size: 8pt; color: #64748b;">Đại hạn: {c.get('dai_han', 0)} - {c.get('dai_han', 0) + 9} tuổi • Tràng sinh: {c.get('trang_sinh', 'Mộ')}</span>
      </div>
      
      <div style="font-size: 8pt; color: #475569; margin-bottom: 4px; font-style: italic;">
        <strong>Ý nghĩa cung vị:</strong> {cung_desc}
      </div>

      <div style="font-size: 8pt; line-height: 1.4; margin-bottom: 4px;">
        <div><strong>Chính tinh:</strong> <span style="color: #7f1d1d; font-weight: bold;">{chinh}</span> {tt_span}</div>
        <div><strong>Cát tinh:</strong> <span style="color: #16a34a;">{cat}</span></div>
        <div><strong>Hung tinh:</strong> <span style="color: #dc2626;">{hung}</span></div>
        <div><strong>Sao Lưu {analysis_year}:</strong> <span style="color: #6d28d9; font-weight: bold;">{luu}</span></div>
      </div>
      
      {tt_note}
      {combos_html}

      <!-- TOÀN BỘ CÁC THẺ BÌNH GIẢI CHI TIẾT TINH ĐẨU TỌA THỦ TỪ CỔ THƯ -->
      <div style="margin: 8px 0 6px 0;">
        <strong style="color: #0369a1; font-size: 8.5pt; display: block; margin-bottom: 5px;">📜 BÌNH GIẢI CHI TIẾT CÁC TINH ĐẨU TỌA THỦ (KINH ĐIỂN CỔ THƯ):</strong>
        {render_chamber_classical_readings_html(c, readings_db)}
      </div>

      <div style="font-size: 8.5pt; line-height: 1.45; background: #fafafa; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #b38728; margin-top: 6px;">
        <strong style="color: #78350f; font-size: 8.3pt; display: block; margin-bottom: 3px;">🌟 BÌNH CHÚ KINH ĐIỂN TỨ PHÁI:</strong>
        <p style="margin: 0 0 3px 0;"><strong>• Cụ Bửu Đình:</strong> {bd}</p>
        <p style="margin: 0 0 3px 0;"><strong>• Đại Đức Sơn Nhân:</strong> {dd}</p>
        <p style="margin: 0 0 3px 0;"><strong>• Cụ Thiên Lương:</strong> {tl}</p>
        <p style="margin: 0;"><strong>• Trung Châu Phái:</strong> {tc}</p>
      </div>
    </div>
"""

    # Injected 2.4 Bình Giải Đại Vận
    html_content += f"""
    <!-- 2.4 BÌNH GIẢI THẬP NIÊN ĐẠI VẬN -->
    {render_daivan_limits_html(chart_data, readings_db)}
  </div>

  <!-- ================= PHẦN III: BÁT TỰ TỨ TRỤ TOÀN THƯ ================= -->
  <div class="page-break">
    <h2 class="chapter-header">PHẦN III: BÁT TỰ TỨ TRỤ TOÀN THƯ & ĐỊNH LƯỢNG NGŨ HÀNH</h2>
    
    {render_bazi_visual_chart(bazi, p)}

    <h3 class="section-header">3.1 Bản Thể Nhật Chủ {day_master} ({day_master_elem}) & Tương Tác Lệnh Tháng</h3>
    <p>
      Trong Bát Tự Tử Bình, Can Ngày tượng trưng cho bản thể cốt lõi, tâm thức và ý chí của đương số <strong>{name}</strong>. Người mang Nhật Chủ <strong>{day_master} ({day_master_elem})</strong> sở hữu tư duy sắc bén, tính khí kiên định và khả năng học hỏi thích ứng linh hoạt với thời cuộc.
    </p>
    <p>
      • <strong>Tương tác với Lệnh Tháng ({m_p.get('chi', '')}):</strong> Sinh vào tháng {m_p.get('chi', '')}, bản mệnh được đánh giá ở thế: <em>{vuong_suy}</em>. Điều này phản ánh nguồn nội lực và sức sống tiềm tàng bên trong, giúp đương số vững vàng vượt qua các đợt sóng gió thử thách trong đời.
    </p>

    <h3 class="section-header">3.2 Cấu Trúc Bát Trụ Toàn Diện (Thai, Mệnh, Tức, Phút)</h3>
    <table class="data-table">
      <thead>
        <tr>
          <th>Trụ Bổ Trợ</th>
          <th>Can Chi</th>
          <th>Ngũ Hành</th>
          <th>Ý Nghĩa Vận Mệnh Tiên Thiên</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Thai Cung</strong></td>
          <td><strong>{pillars.get('thai_cung', {}).get('can', '')} {pillars.get('thai_cung', {}).get('chi', '')}</strong></td>
          <td>{pillars.get('thai_cung', {}).get('elem', '')}</td>
          <td>Nơi thụ khí tiên thiên thuở trong bụng mẹ, quyết định thể trạng và phúc đức di truyền gia tộc.</td>
        </tr>
        <tr>
          <td><strong>Mệnh Cung</strong></td>
          <td><strong>{pillars.get('menh_cung', {}).get('can', '')} {pillars.get('menh_cung', {}).get('chi', '')}</strong></td>
          <td>{pillars.get('menh_cung', {}).get('elem', '')}</td>
          <td>Cung khởi sinh quy tụ tinh anh, hỗ trợ bản mệnh tháo gỡ bế tắc khi hạn rơi vào nghịch cảnh.</td>
        </tr>
        <tr>
          <td><strong>Thai Tức</strong></td>
          <td><strong>{pillars.get('thai_tuc', {}).get('can', '')} {pillars.get('thai_tuc', {}).get('chi', '')}</strong></td>
          <td>{pillars.get('thai_tuc', {}).get('elem', '')}</td>
          <td>Cầu nối khí huyết nuôi dưỡng, phản ánh sức bền nội lực và khả năng chuyển nguy thành an.</td>
        </tr>
        <tr>
          <td><strong>Trụ Phút</strong></td>
          <td><strong>{pillars.get('minute', {}).get('can', '')} {pillars.get('minute', {}).get('chi', '')}</strong></td>
          <td>{pillars.get('minute', {}).get('elem', '')}</td>
          <td>Sự tinh vi của dòng thời gian thời khắc ra đời, hoàn thiện bức tranh vận khí vi mô.</td>
        </tr>
      </tbody>
    </table>

    <h3 class="section-header">3.3 Dụng Thần, Hỷ Thần & Định Hướng Phong Thủy</h3>
    <p>
      • <strong>Nguyên Tắc Dụng Thần:</strong> Cân bằng ngũ hành cho Nhật Chủ hành {day_master_elem}. Tăng cường các yếu tố tương sinh tương trợ, khai thông dòng chảy năng lượng tích cực.
    </p>
    <p>
      • <strong>Màu sắc & Phương vị hành mệnh:</strong> Ưu tiên gam màu tương hợp với bản mệnh, chọn không gian sống và bàn làm việc thoáng đãng, hướng về phương vị đón ánh sáng tự nhiên.
    </p>
    <p>
      • <strong>Ngành nghề tương hợp:</strong> Công nghệ thông tin, trí tuệ nhân tạo, truyền thông, thiết kế sáng tạo, ngoại giao, nghiên cứu chiến lược và tài chính.
    </p>
  </div>

  <!-- ================= PHẦN IV: VẬN HẠN 12 THÁNG ================= -->
  <div class="page-break">
    <h2 class="chapter-header">PHẦN IV: VẬN HẠN 12 THÁNG LƯU NIÊN & LƯU NGUYỆT MỆNH CUNG</h2>
    
    <h3 class="section-header">4.1 Tổng Quan Đại Vận Hiện Tại & Năm Lưu Niên {analysis_year} ({analysis_lunar})</h3>
    <p>
      Năm {analysis_year} ({analysis_lunar}), đương số bước sang tuổi <strong>{age}</strong>. Đây là giai đoạn bản lề cực kỳ quan trọng:
      Đại vận đang kích hoạt sự chuyển hóa lớn về cả công danh lẫn gia đạo.
      Tuần Không bao bọc lâu dài, tạo chiếc khiên che chở bình an trước mọi tai ách sóng gió.
    </p>

    <h3 class="section-header">4.2 Bảng Ma Trận Khảo Sát 12 Tháng Âm Lịch (Hội Chiếu & Sao Lưu)</h3>
    <p>
      Dưới đây là bảng khảo sát chi tiết 12 tháng Âm lịch năm {analysis_year} ({analysis_lunar}), chỉ rõ cung vị Nguyệt Hạn, tinh đẩu tọa thủ, cung đối diện xung chiếu, thế kiềng tam hợp và tương trợ nhị hợp:
    </p>
    
    <table class="data-table" style="font-size: 7.8pt;">
      <thead>
        <tr>
          <th style="width: 7%;">Tháng ÂL</th>
          <th style="width: 18%;">Mệnh Tháng & Sao Lưu Tọa Thủ</th>
          <th style="width: 18%;">Xung Chiếu (Chiếu Đối Diện)</th>
          <th style="width: 23%;">Tam Hợp (Thế Chân Vạc Hội Về)</th>
          <th style="width: 16%;">Nhị Hợp (Trợ Lực Ngầm)</th>
          <th style="width: 18%;">Dự Báo & Lời Khuyên Vận Hạn</th>
        </tr>
      </thead>
      <tbody>
"""

    monthly_details_list = []
    for m in range(1, 13):
        m_cung = next((c for c in chambers if c.get("nguyet_han") == m), None)
        if not m_cung and chambers:
            m_cung = chambers[(m - 1) % 12]
            
        m_chi = m_cung.get("chi", "Dần")
        asp = CHI_ASPECTS.get(m_chi, {"tam_hop": ["Ngọ", "Tuất"], "xung_chieu": "Thân", "nhi_hop": "Hợi"})
        
        xc_cung = next((c for c in chambers if c.get("chi") == asp["xung_chieu"]), chambers[0])
        th1_cung = next((c for c in chambers if c.get("chi") == asp["tam_hop"][0]), chambers[0])
        th2_cung = next((c for c in chambers if c.get("chi") == asp["tam_hop"][1]), chambers[0])
        nh_cung = next((c for c in chambers if c.get("chi") == asp["nhi_hop"]), chambers[0])

        m_chinh, m_cat, m_hung, m_luu, m_luu_list = extract_chamber_stars_for_pdf(m_cung)
        xc_chinh, _, _, xc_luu, xc_luu_list = extract_chamber_stars_for_pdf(xc_cung)
        th1_chinh, _, _, th1_luu, th1_luu_list = extract_chamber_stars_for_pdf(th1_cung)
        th2_chinh, _, _, th2_luu, th2_luu_list = extract_chamber_stars_for_pdf(th2_cung)
        nh_chinh, _, _, nh_luu, nh_luu_list = extract_chamber_stars_for_pdf(nh_cung)

        m_tt = m_cung.get("tuan_triet") or "Không"
        
        # Collect flying stars in trines
        th_luu_all = list(set(th1_luu_list + th2_luu_list))
        th_luu_str = f"<br><span style='color: #b45309; font-weight: bold;'>Hội: {', '.join(th_luu_all)}</span>" if th_luu_all else ""
        
        xc_luu_str = f" <span style='color: #dc2626;'>({', '.join(xc_luu_list)})</span>" if xc_luu_list else ""
        m_luu_tag = f"<br><span style='color: #6d28d9; font-weight: bold;'>⚡ {m_luu}</span>" if m_luu != "Không có" else ""

        # Monthly advice dynamic
        m_advice = f"Tháng {m} ÂL đóng tại {m_cung.get('name')}. Vận trình ổn định, cần chủ động điều tiết công việc và giữ hòa khí gia đạo."
        if any("Lộc" in s for s in m_luu_list + th_luu_all):
            if any("Quyền" in s for s in m_luu_list + th_luu_all):
                m_advice = "🌟 Đắc cách Lộc Quyền Hội Hợp: Uy quyền thăng tiến đi liền tài chính dồi dào, đối tác ký kết hợp đồng thuận lợi!"
            else:
                m_advice = "Tài lộc tháng này hanh thông, dòng tiền tích cực, cơ hội ký kết hợp đồng và gia tăng thu nhập rõ nét."
        elif any("Tang" in s or "Hổ" in s for s in m_luu_list + th_luu_all):
            m_advice = "Nhiều lo toan gia sự, chăm sóc con nhỏ hoặc người thân lớn tuổi. Chú ý giữ gìn sức khỏe, tránh làm việc quá khuya."
        elif any("Mã" in s for s in m_luu_list + xc_luu_list):
            m_advice = "Vận động dịch chuyển nhiều, công tác xa hoặc ngoại giao đem lại nhiều cơ hội đối tác mới."

        monthly_details_list.append({
            "m": m,
            "m_cung": m_cung,
            "xc_cung": xc_cung,
            "th1_cung": th1_cung,
            "th2_cung": th2_cung,
            "nh_cung": nh_cung,
            "m_chinh": m_chinh,
            "m_luu_list": m_luu_list,
            "m_tt": m_tt,
            "xc_chinh": xc_chinh,
            "xc_luu_list": xc_luu_list,
            "th_luu_all": th_luu_all,
            "th1_chinh": th1_chinh,
            "th2_chinh": th2_chinh,
            "nh_chinh": nh_chinh,
            "nh_luu_list": nh_luu_list,
            "advice": m_advice
        })
        m_tt_tag = f'<strong style="color: #dc2626;">[{m_tt}]</strong>' if m_tt != 'Không' else ''

        html_content += f"""
        <tr>
          <td style="text-align: center;"><strong>Tháng {m}</strong></td>
          <td><strong>{m_cung.get('name')}</strong> ({m_cung.get('chi')})<br><span style="color: #7f1d1d;">{m_chinh}</span> {m_tt_tag}{m_luu_tag}</td>
          <td><strong>{xc_cung.get('name')}</strong> ({xc_cung.get('chi')})<br><span style="color: #475569;">{xc_chinh}</span>{xc_luu_str}</td>
          <td>{th1_cung.get('name')} ({th1_cung.get('chi')}) & {th2_cung.get('name')} ({th2_cung.get('chi')}){th_luu_str}</td>
          <td><strong>{nh_cung.get('name')}</strong> ({nh_cung.get('chi')})<br><span style="color: #64748b; font-size: 7.5pt;">{m_chi} hợp {nh_cung.get('chi')}</span></td>
          <td>{m_advice}</td>
        </tr>
"""

    html_content += """
      </tbody>
    </table>

    <h3 class="section-header">4.3 Khảo Luận Chuyên Sâu Tương Tác 4 Chiều (Tọa Thủ - Xung Chiếu - Tam Hợp - Nhị Hợp) 12 Tháng</h3>
    <p>
      Dưới đây là bình giải trực quan dạng 4 khối tương tác đa chiều cho toàn bộ 12 tháng Âm lịch:
    </p>
"""

    for item in monthly_details_list:
        m = item["m"]
        mc = item["m_cung"]
        xc = item["xc_cung"]
        th1 = item["th1_cung"]
        th2 = item["th2_cung"]
        nh = item["nh_cung"]

        luu_m_str = ", ".join(item["m_luu_list"]) if item["m_luu_list"] else "Không có"
        luu_xc_str = ", ".join(item["xc_luu_list"]) if item["xc_luu_list"] else "Không có"
        luu_th_str = ", ".join(item["th_luu_all"]) if item["th_luu_all"] else "Không có"
        luu_nh_str = ", ".join(item["nh_luu_list"]) if item["nh_luu_list"] else "Không có"

        tt_tag = f"<span style='color: #dc2626;'>[{item['m_tt']}]</span>" if item['m_tt'] != 'Không' else ""

        html_content += f"""
    <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 12px; margin-bottom: 12px; page-break-inside: avoid;">
      <div style="border-bottom: 1px dashed #cbd5e1; padding-bottom: 4px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
        <strong style="color: #8b0000; font-size: 9.5pt;">🌙 THÁNG {m} ÂM LỊCH: CUNG {mc.get('name').upper()} TẠI {mc.get('can', '')} {mc.get('chi', '')} (HÀNH {mc.get('element', '')})</strong>
        <span style="font-size: 7.5pt; background: #fef3c7; color: #92400e; padding: 2px 6px; border-radius: 4px; font-weight: bold;">Nguyệt Hạn Cung</span>
      </div>

      <!-- 4-Box Aspect Grid matching screenshot 3 -->
      <div class="pdf-aspect-grid">
        
        <!-- Card 1: Tọa Thủ -->
        <div class="pdf-aspect-card pdf-aspect-card-toathu">
          <div style="font-weight: bold; color: #6d28d9; margin-bottom: 3px;">🎯 1. Tọa Thủ Bản Cung</div>
          <div><strong>Chính tinh:</strong> {item['m_chinh']} {tt_tag}</div>
          <div><strong>Sao lưu tọa thủ:</strong> <span style="color: #6d28d9; font-weight: bold;">{luu_m_str}</span></div>
          <div style="margin-top: 3px; font-size: 7.5pt; color: #475569;">
            Làm chủ thần thức suốt 30 ngày, chiếu năng lượng sang {xc.get('name')} và phóng tia tam hợp.
          </div>
        </div>

        <!-- Card 2: Xung Chiếu -->
        <div class="pdf-aspect-card pdf-aspect-card-xungchieu">
          <div style="font-weight: bold; color: #b91c1c; margin-bottom: 3px;">⚡ 2. Cung Xung Chiếu (180°)</div>
          <div><strong>Cung:</strong> {xc.get('name')} ({xc.get('chi')})</div>
          <div><strong>Tinh đẩu dội sang:</strong> {item['xc_chinh']}</div>
          <div><strong>Sao lưu dội sang:</strong> <span style="color: #dc2626; font-weight: bold;">{luu_xc_str}</span></div>
          <div style="margin-top: 3px; font-size: 7.5pt; color: #475569;">
            Đại diện áp lực ngoại cảnh và thị trường bên ngoài dội vào, cần điềm tĩnh xử lý.
          </div>
        </div>

        <!-- Card 3: Tam Hợp -->
        <div class="pdf-aspect-card pdf-aspect-card-tamhop">
          <div style="font-weight: bold; color: #b45309; margin-bottom: 3px;">🔺 3. Cặp Cung Tam Hợp</div>
          <div><strong>Thế chân vạc:</strong> {mc.get('chi')} - {th1.get('chi')} - {th2.get('chi')}</div>
          <div><strong>Hội tụ:</strong> {th1.get('name')} & {th2.get('name')}</div>
          <div><strong>Sao lưu hội về:</strong> <span style="color: #b45309; font-weight: bold;">{luu_th_str}</span></div>
          <div style="margin-top: 3px; font-size: 7.5pt; color: #475569;">
            Điểm tựa nội lực, hậu phương gia đình và bạn bè đối tác đồng hành.
          </div>
        </div>

        <!-- Card 4: Nhị Hợp -->
        <div class="pdf-aspect-card pdf-aspect-card-nhihop">
          <div style="font-weight: bold; color: #1d4ed8; margin-bottom: 3px;">🌿 4. Cung Nhị Hợp (Lục Hợp)</div>
          <div><strong>Cung:</strong> {nh.get('name')} ({nh.get('chi')} - {nh.get('element', '')})</div>
          <div><strong>Quan hệ:</strong> {mc.get('chi')} hợp {nh.get('chi')}</div>
          <div><strong>Sao lưu ngầm:</strong> <span style="color: #2563eb; font-weight: bold;">{luu_nh_str}</span></div>
          <div style="margin-top: 3px; font-size: 7.5pt; color: #475569;">
            Trợ lực ngầm, phúc đức gia tiên và sự tương trợ kín đáo từ hậu trường.
          </div>
        </div>

      </div>

      <div style="background: #fafafa; border-left: 3px solid #f59e0b; padding: 4px 8px; font-size: 8pt; font-weight: 600; color: #78350f;">
        💡 Lời khuyên vận hành: {item['advice']}
      </div>
    </div>
"""

    html_content += f"""
  </div>

  <!-- ================= PHẦN V: DỊCH LÝ ĐÔNG PHƯƠNG ================= -->
  <div class="page-break">
    <h2 class="chapter-header">PHẦN V: KHO TÀNG DỊCH LÝ ĐÔNG PHƯƠNG & ĐẠO HÀNH ĐỜI</h2>
    
    <h3 class="section-header">5.1 Đạo Âm Dương: Đàn Ông Cái Ly (Quẻ Ly) - Đàn Bà Cái Đĩa (Quẻ Khảm)</h3>
    <p>
      Trong đồ hình Dịch học và biểu tượng Đông phương cổ đại:
      <strong>Đàn ông như Cái Ly</strong> (Quẻ Ly ☲, tượng của Lửa, Mặt Trời, sự quang minh, chính trực, đứng thẳng và tỏa sáng).
      <strong>Đàn bà như Cái Đĩa</strong> (Quẻ Khảm ☵, tượng của Nước, Mặt Trăng to tròn trắng ngần, tĩnh tại, nhu thuận và bao bọc).
    </p>
    
    {render_dich_ly_visuals()}

    <div class="quote-box">
      \"Đàn ông cần có NGHĨA — Đàn bà cần có TÌNH. Chiếc đĩa nâng đỡ cái ly, Đất nâng đỡ Trời. Nhu thắng Cương, Tình cảm gìn giữ cội rễ bình yên của gia đạo.\"
    </div>
    <p>
      Người đời thường lầm tưởng Mặt Trời to hơn Mặt Trăng theo khoa học vật lý phương Tây thế kỷ 17, nhưng theo nhãn quan huyền học Đông phương:
      về phương diện nuôi dưỡng linh hồn và cảm xúc con người, năng lượng Mặt Trăng (Thái Âm) bao bọc vạn vật trong đêm tối, tựa như lòng dạ người mẹ, người vợ dung nạp tất cả những mỏi mệt bôn ba của người đàn ông trở về.
    </p>

    <h3 class="section-header">5.2 Đạo Vợ Chồng, Hôn Nhân & Bí Pháp Đi Xa Hóa Giải Xung Khắc</h3>
    <p>
      Trong Tử Vi, khi cung Phu Thê có các sao nhạy cảm như Hóa Kỵ, Thiên Không hay Đào Hồng thì khi ở quá gần nhau, va chạm cơm áo gạo tiền hằng ngày rất dễ làm nảy sinh tâm lý soi xét, nghi kỵ vụn vặt.
    </p>
    <div class="quote-box">
      \"Khoảng cách địa lý tạo ra sự nâng niu trân trọng. Khi người đàn ông đi xa hành đạo, giữ trọn chữ NGHĨA thì xa cách vạn dặm chỉ làm tăng thêm tình cảm sắt son chứ không hề chia cắt.\"
    </div>
    <p>
      Việc đi xa chính là một hình thức <strong>\"động cách\"</strong> để giải tỏa áp lực của cung Phu Thê. Người ở nhà chăm lo tổ ấm, người đi xa gánh vác sự nghiệp. Khi trở về mang theo sự thấu hiểu và lòng bao dung thì tình duyên càng thêm bền chặt.
    </p>

    <h3 class="section-header">5.3 Cung Tử Tức: Quý Tử & Đạo Làm Cha Mẹ (Cây Cau Kinh Luân)</h3>
    <p>
      Tại sao dân gian lại gọi là <strong>Quý Tử</strong>? Đứa trẻ sinh ra mang mệnh lớn, tư chất thông minh đôn hậu chính là phúc báu tối thượng của dòng tộc.
      Hình ảnh <strong>Cây Cau Kinh Luân</strong>: thân cau vươn thẳng đứng hiên ngang đón ánh mặt trời, rễ bám sâu vào lòng đất mẹ.
      Nuôi dạy con cái cũng tựa như trồng cau: cha mẹ rèn luyện cho con tính tự lập, chữ NGHĨA và chí khí vươn cao, nhưng phải bồi đắp cội rễ bằng đức độ và tình yêu thương bao la.
    </p>

    <h3 class="section-header">5.4 Sấm Cơ Dịch Học & Dự Báo Thời Vận (Kinh Đô & Long Mạch)</h3>
    <p>
      Theo quy luật dịch chuyển của trời đất và các mốc lịch sử nghìn năm:
      Năm 1010, Hoàng Đế Lý Thái Tổ dời đô từ Hoa Lư về Thăng Long, lập Thăng Long Tứ Trấn bảo vệ kinh kỳ.
      Đến năm Canh Tý 2020 vừa tròn 1010 năm, thời vận mở ra chu kỳ chuyển dịch long mạch lớn về phương Nam.
      Trong Tử Vi và Dịch Lý, đây là giai đoạn \"thanh lọc và tái cấu trúc\" vĩ mô, đòi hỏi người quân tử phải nắm vững thiên thời, kiên định với giá trị cốt lõi, tích lũy tri thức và đức độ để đón đầu vận hội mới.
    </p>

    <h3 class="section-header">5.5 Đạo Hành Đời: Tâm Đức Thắng Số</h3>
    <div class="quote-box">
      \"Tướng do tâm sinh — Cảnh tùy tâm chuyển — Đức năng thắng số.\"
    </div>
    <p>
      Lá số Tử Vi và Bát Tự Tứ Trụ chỉ là bản đồ thiên định, là tấm gương phản chiếu khuynh hướng và nhịp điệu của thời gian. 
      Người hiểu mệnh không phải để buông xuôi cho số phận an bài, mà để <strong>biết tiến biết thoái</strong>, khi gặp thuận cảnh thì phát huy hết tài năng cống hiến cho đời, khi gặp nghịch cảnh thì điềm tĩnh tu thân tích đức.
      Đức độ, sự trung thực, lòng hiếu thảo và chữ NGHĨA chính là nguồn năng lượng tối thượng có thể hóa giải mọi hung sát tinh, mang lại phúc thọ an khang cho bản thân và muôn đời con cháu mai sau.
    </p>
  </div>

  <!-- ================= LỜI CẢM ƠN, BẢN QUYỀN & ỦNG HỘ TÁC GIẢ ================= -->
  <div class="page-break" style="page-break-before: always; text-align: center; padding: 30px 15px;">
    <div style="border: 2px solid #b45309; border-radius: 12px; padding: 22px 26px; background: #fffbeb; box-shadow: 0 4px 15px rgba(180, 83, 9, 0.1);">
      <div style="font-size: 22pt; margin-bottom: 6px;">☸ 💖 ☯</div>
      <h2 style="font-family: 'Cinzel Decorative', 'Georgia', serif; font-size: 15pt; color: #78350f; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">
        LỜI CẢM ƠN & TÙY TÂM ĐỒNG HÀNH
      </h2>
      <div style="width: 80px; height: 2px; background: #f59e0b; margin: 0 auto 14px auto;"></div>
      
      <p style="font-size: 9pt; color: #451a03; line-height: 1.55; max-width: 620px; margin: 0 auto 14px auto; text-align: justify;">
        Kính gửi Quý độc giả,<br/>
        Chân thành cảm ơn Quý bạn đã tin tưởng sử dụng hệ thống <strong>Tử Vi Toàn Thư & Bát Tự Hà Lạc</strong>. 
        Tập đại thư vận mệnh này được kết tinh từ sự phối hợp công phu giữa thuật an sao cổ truyền Đông phương và công nghệ thuật toán hiện đại, nhằm mang lại cho Quý bạn bức tranh toàn cảnh, sáng tỏ và sâu sắc nhất về bản mệnh đời mình.<br/>
        Mọi nghiên cứu và sự cải tiến của hệ thống được thực hiện bằng trọn vẹn tâm huyết. Hãy ủng hộ tôi để hệ thống được cải tiến hằng ngày, mọi sự ủng hộ của các bạn đều giúp hệ thống hoàn thiện và duy trì phụng sự cộng đồng tốt hơn!
      </p>

      <!-- Khung Mã QR và Thông tin Chuyển khoản -->
      <div style="display: inline-block; background: #ffffff; border: 1.5px solid #d97706; border-radius: 10px; padding: 10px 18px; margin: 8px auto 14px auto;">
        <img src="{qr_data_uri}" alt="Mã QR TPBank Hoàng Tuấn Việt" style="width: 140px; height: auto; border-radius: 6px; display: block; margin: 0 auto 8px auto;" />
        <div style="font-size: 8pt; color: #78350f; font-weight: bold; line-height: 1.45;">
          Ngân hàng TPBank (Tiên Phong Bank)<br/>
          Chủ tài khoản: <span style="color: #b45309; font-size: 8.5pt;">HOANG TUAN VIET</span><br/>
          Số tài khoản: <span style="color: #dc2626; font-size: 9pt;">0300 1779 995</span><br/>
          Nội dung: <em>UNG HO TU VI</em>
        </div>
      </div>

      <div style="font-size: 8.2pt; color: #78350f; font-style: italic; margin-bottom: 16px;">
        🙏 "Một hạt cát bồi đắp nên sa mạc, một giọt nước hòa thành biển khơi. Mọi sự ủng hộ của Quý bạn đều là nguồn động viên vô giá!"
      </div>

      <div style="border-top: 1px dashed #d97706; padding-top: 10px; font-size: 7.8pt; color: #92400e; line-height: 1.45;">
        <strong>BẢN QUYỀN TÁC PHẨM & CÔNG TRÌNH:</strong><br/>
        Bản quyền tác phẩm thuộc về: <strong>HOÀNG TUẤN VIỆT (Hoàng Tuấn Việt) © 2026</strong>.<br/>
        Mọi quyền được bảo lưu. Email liên hệ học thuật & bảo trợ: <em>viet.ht.18995@gmail.com</em>
      </div>
    </div>
  </div>

</body>
</html>
"""

    temp_html_path = output_pdf_path.replace(".pdf", "_temp.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    browser_exe = get_browser_executable()
    if not browser_exe:
        raise Exception("Không tìm thấy Google Chrome hoặc Microsoft Edge để biên dịch PDF.")
        
    file_uri = pathlib.Path(temp_html_path).resolve().as_uri()
    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-sync",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf_path}",
        file_uri
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise Exception(f"Lỗi khi xuất PDF qua headless browser: {res.stderr}")
        
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)
        
    print(f"Đã tạo thành công quyển sách PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path

if __name__ == "__main__":
    from tuvi_engine import calculate_tuvi
    chart = calculate_tuvi("Hoàng Tuấn Việt", "Nam", 18, 9, 1995, 14, 2026, 0)
    pdf_out = os.path.join(os.path.dirname(__file__), "La_So_Tu_Vi_Hoang_Tuan_Viet_Toan_Thu.pdf")
    generate_pdf_book(chart, pdf_out)
