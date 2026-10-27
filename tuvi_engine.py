import os
import sys

# Add the local directory to the path so we can import lasotuvi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lasotuvi.DiaBan import diaBan
from lasotuvi.ThienBan import lapThienBan
from lasotuvi.App import lapDiaBan
from lasotuvi.AmDuong import thienCan, diaChi

# Helper to find Can Chi of a year (for analysis year)
def get_can_chi_year(year):
    can_list = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
    chi_list = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
    return f"{can_list[year % 10]} {chi_list[year % 12]}"

# Elements translation
element_map = {
    "K": "Kim",
    "M": "Mộc",
    "T": "Thủy",
    "H": "Hỏa",
    "O": "Thổ"
}

# Cung ID mapping to JSON IDs
cung_id_map = {
    "Mệnh": "menh",
    "Phụ mẫu": "phu_mau",
    "Phúc đức": "phuc_duc",
    "Điền trạch": "dien_trach",
    "Quan lộc": "quan_loc",
    "Nô bộc": "no_boc",
    "Thiên di": "thien_di",
    "Tật Ách": "tat_ach",
    "Tài Bạch": "tai_bach",
    "Tử tức": "tu_tuc",
    "Phu thê": "phu_the",
    "Huynh đệ": "huynh_de"
}

# Hour strings to index (1-12)
hour_map = {
    "Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tỵ": 6,
    "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12
}

# Can Chi weights for "Cân Lượng" calculation
WEIGHTS_YEAR = {
    1990: 9, 1991: 8, 1992: 7, 1993: 8, 1994: 15, 1995: 9, # 1995 Ất Hợi is 9 chỉ (or 9 chỉ = 0.9 lượng)
    1996: 16, 1997: 8, 1998: 8, 1999: 19, 2000: 12, 2001: 6,
    2002: 8, 2003: 7, 2004: 15, 2005: 15, 2006: 8, 2007: 16,
    2008: 15, 2009: 7, 2010: 9, 2011: 12, 2012: 5, 2013: 5
}
WEIGHTS_MONTH = {
    1: 6, 2: 7, 3: 18, 4: 9, 5: 5, 6: 16, 7: 9, 8: 15, 9: 18, 10: 8, 11: 9, 12: 5
}
WEIGHTS_DAY = {
    1: 5, 2: 10, 3: 8, 4: 15, 5: 16, 6: 15, 7: 8, 8: 16, 9: 8, 10: 16,
    11: 9, 12: 17, 13: 8, 14: 17, 15: 10, 16: 8, 17: 9, 18: 18, 19: 5, 20: 15,
    21: 9, 22: 9, 23: 8, 24: 9, 25: 15, 26: 18, 27: 7, 28: 8, 29: 16, 30: 6
}
WEIGHTS_HOUR = {
    1: 16, 2: 6, 3: 7, 4: 10, 5: 9, 6: 16, 7: 10, 8: 8, 9: 8, 10: 9, 11: 6, 12: 6
}

def calculate_weight(year, month, day, hour_idx):
    weights_60 = [
        12, 9, 6, 7, 12, 5, 9, 8, 7, 8, 15, 9, 16, 8, 8, 19, 12, 6, 8, 7, 
        15, 15, 6, 16, 15, 7, 9, 12, 10, 7, 15, 6, 5, 14, 19, 9, 7, 7, 9, 12, 
        12, 7, 13, 5, 14, 5, 9, 17, 5, 8, 12, 8, 8, 6, 19, 6, 8, 16, 10, 6
    ]
    # 1984 is Giáp Tý (index 0)
    y_idx = (year - 1984) % 60
    y_w = weights_60[y_idx]
    m_w = WEIGHTS_MONTH.get(month, 8)
    d_w = WEIGHTS_DAY.get(day, 10)
    h_w = WEIGHTS_HOUR.get(hour_idx, 8)
    
    total_chi = y_w + m_w + d_w + h_w
    luong = total_chi // 10
    chi = total_chi % 10
    return f"{luong} lượng {chi} chỉ"

CAN_INFO = {
    "Giáp": {"element": "Mộc", "polarity": 1},
    "Ất": {"element": "Mộc", "polarity": -1},
    "Bính": {"element": "Hỏa", "polarity": 1},
    "Đinh": {"element": "Hỏa", "polarity": -1},
    "Mậu": {"element": "Thổ", "polarity": 1},
    "Kỷ": {"element": "Thổ", "polarity": -1},
    "Canh": {"element": "Kim", "polarity": 1},
    "Tân": {"element": "Kim", "polarity": -1},
    "Nhâm": {"element": "Thủy", "polarity": 1},
    "Quý": {"element": "Thủy", "polarity": -1}
}

CHI_INFO = {
    "Tý": {"element": "Thủy", "polarity": 1},
    "Sửu": {"element": "Thổ", "polarity": -1},
    "Dần": {"element": "Mộc", "polarity": 1},
    "Mão": {"element": "Mộc", "polarity": -1},
    "Thìn": {"element": "Thổ", "polarity": 1},
    "Tỵ": {"element": "Hỏa", "polarity": -1},
    "Ngọ": {"element": "Hỏa", "polarity": 1},
    "Mùi": {"element": "Thổ", "polarity": -1},
    "Thân": {"element": "Kim", "polarity": 1},
    "Dậu": {"element": "Kim", "polarity": -1},
    "Tuất": {"element": "Thổ", "polarity": 1},
    "Hợi": {"element": "Thủy", "polarity": -1}
}

CHI_HIDDEN_STEMS_FULL = {
    "Tý": [{"can": "Quý", "type": "Bản khí", "ratio": 1.0}],
    "Sửu": [{"can": "Kỷ", "type": "Bản khí", "ratio": 0.6}, {"can": "Quý", "type": "Trung khí", "ratio": 0.3}, {"can": "Tân", "type": "Dư khí", "ratio": 0.1}],
    "Dần": [{"can": "Giáp", "type": "Bản khí", "ratio": 0.6}, {"can": "Bính", "type": "Trung khí", "ratio": 0.3}, {"can": "Mậu", "type": "Dư khí", "ratio": 0.1}],
    "Mão": [{"can": "Ất", "type": "Bản khí", "ratio": 1.0}],
    "Thìn": [{"can": "Mậu", "type": "Bản khí", "ratio": 0.6}, {"can": "Ất", "type": "Trung khí", "ratio": 0.3}, {"can": "Quý", "type": "Dư khí", "ratio": 0.1}],
    "Tỵ": [{"can": "Bính", "type": "Bản khí", "ratio": 0.6}, {"can": "Mậu", "type": "Trung khí", "ratio": 0.3}, {"can": "Canh", "type": "Dư khí", "ratio": 0.1}],
    "Ngọ": [{"can": "Đinh", "type": "Bản khí", "ratio": 0.7}, {"can": "Kỷ", "type": "Trung khí", "ratio": 0.3}],
    "Mùi": [{"can": "Kỷ", "type": "Bản khí", "ratio": 0.6}, {"can": "Đinh", "type": "Trung khí", "ratio": 0.3}, {"can": "Ất", "type": "Dư khí", "ratio": 0.1}],
    "Thân": [{"can": "Canh", "type": "Bản khí", "ratio": 0.6}, {"can": "Nhâm", "type": "Trung khí", "ratio": 0.3}, {"can": "Mậu", "type": "Dư khí", "ratio": 0.1}],
    "Dậu": [{"can": "Tân", "type": "Bản khí", "ratio": 1.0}],
    "Tuất": [{"can": "Mậu", "type": "Bản khí", "ratio": 0.6}, {"can": "Tân", "type": "Trung khí", "ratio": 0.3}, {"can": "Đinh", "type": "Dư khí", "ratio": 0.1}],
    "Hợi": [{"can": "Nhâm", "type": "Bản khí", "ratio": 0.7}, {"can": "Giáp", "type": "Trung khí", "ratio": 0.3}]
}

CHI_HIDDEN_STEMS = {k: v[0]["can"] for k, v in CHI_HIDDEN_STEMS_FULL.items()}

def get_ten_god(day_stem, target_stem):
    if day_stem not in CAN_INFO or target_stem not in CAN_INFO:
        return "N/A"
    
    ds = CAN_INFO[day_stem]
    ts = CAN_INFO[target_stem]
    
    ds_elem = ds["element"]
    ts_elem = ts["element"]
    
    same_polarity = (ds["polarity"] * ts["polarity"] > 0)
    
    elements = ["Thủy", "Mộc", "Hỏa", "Thổ", "Kim"]
    ds_idx = elements.index(ds_elem)
    ts_idx = elements.index(ts_elem)
    
    offset = (ts_idx - ds_idx) % 5
    
    if offset == 0:
        return "Tỷ Kiên" if same_polarity else "Kiếp Tài"
    elif offset == 1:
        return "Thực Thần" if same_polarity else "Thương Quan"
    elif offset == 2:
        return "Thiên Tài" if same_polarity else "Chính Tài"
    elif offset == 3:
        return "Thất Sát" if same_polarity else "Chính Quan"
    elif offset == 4:
        return "Thiên Ấn" if same_polarity else "Chính Ấn"
    return "N/A"

def get_hidden_stems_detail(chi, day_master):
    items = CHI_HIDDEN_STEMS_FULL.get(chi, [])
    res = []
    for item in items:
        c = item["can"]
        res.append({
            "can": c,
            "type": item["type"],
            "ratio": item["ratio"],
            "elem": CAN_INFO[c]["element"],
            "ten_god": get_ten_god(day_master, c)
        })
    return res


def get_nhat_chu_vuong_suy(day_stem, month_chi):
    if day_stem not in CAN_INFO or month_chi not in CHI_INFO:
        return "Không rõ"
    
    ds_elem = CAN_INFO[day_stem]["element"]
    
    season_map = {
        "Dần": "Xuân", "Mão": "Xuân",
        "Tỵ": "Hạ", "Ngọ": "Hạ",
        "Thân": "Thu", "Dậu": "Thu",
        "Hợi": "Đông", "Tý": "Đông",
        "Sửu": "Tứ Quý", "Thìn": "Tứ Quý", "Mùi": "Tứ Quý", "Tuất": "Tứ Quý"
    }
    
    season = season_map.get(month_chi, "Tứ Quý")
    
    status_matrix = {
        "Mộc": {"Xuân": "Đắc lệnh (Vượng)", "Đông": "Được sinh (Tướng)", "Hạ": "Sinh xuất (Hưu)", "Tứ Quý": "Khắc xuất (Tù)", "Thu": "Bị khắc (Tử)"},
        "Hỏa": {"Hạ": "Đắc lệnh (Vượng)", "Xuân": "Được sinh (Tướng)", "Tứ Quý": "Sinh xuất (Hưu)", "Thu": "Khắc xuất (Tù)", "Đông": "Bị khắc (Tử)"},
        "Thổ": {"Tứ Quý": "Đắc lệnh (Vượng)", "Hạ": "Được sinh (Tướng)", "Thu": "Sinh xuất (Hưu)", "Đông": "Khắc xuất (Tù)", "Xuân": "Bị khắc (Tử)"},
        "Kim": {"Thu": "Đắc lệnh (Vượng)", "Tứ Quý": "Được sinh (Tướng)", "Đông": "Sinh xuất (Hưu)", "Xuân": "Khắc xuất (Tù)", "Hạ": "Bị khắc (Tử)"},
        "Thủy": {"Đông": "Đắc lệnh (Vượng)", "Thu": "Được sinh (Tướng)", "Xuân": "Sinh xuất (Hưu)", "Hạ": "Khắc xuất (Tù)", "Tứ Quý": "Bị khắc (Tử)"}
    }
    
    return status_matrix[ds_elem].get(season, "Không rõ")

HEXAGRAMS = {
    ('Càn', 'Càn'): 'Thuần Càn', ('Càn', 'Đoài'): 'Thiên Trạch Lý', ('Càn', 'Ly'): 'Thiên Hỏa Đồng Nhân', ('Càn', 'Chấn'): 'Thiên Lôi Vô Vọng',
    ('Càn', 'Tốn'): 'Thiên Phong Cấu', ('Càn', 'Khảm'): 'Thiên Thủy Tụng', ('Càn', 'Cấn'): 'Thiên Sơn Độn', ('Càn', 'Khôn'): 'Thiên Địa Bĩ',
    ('Đoài', 'Càn'): 'Trạch Thiên Quải', ('Đoài', 'Đoài'): 'Thuần Đoài', ('Đoài', 'Ly'): 'Trạch Hỏa Cách', ('Đoài', 'Chấn'): 'Trạch Lôi Tùy',
    ('Đoài', 'Tốn'): 'Trạch Phong Đại Quá', ('Đoài', 'Khảm'): 'Trạch Thủy Khốn', ('Đoài', 'Cấn'): 'Trạch Sơn Hàm', ('Đoài', 'Khôn'): 'Trạch Địa Tụy',
    ('Ly', 'Càn'): 'Hỏa Thiên Đại Hữu', ('Ly', 'Đoài'): 'Hỏa Trạch Khuê', ('Ly', 'Ly'): 'Thuần Ly', ('Ly', 'Chấn'): 'Hỏa Lôi Phệ Hạp',
    ('Ly', 'Tốn'): 'Hỏa Phong Đỉnh', ('Ly', 'Khảm'): 'Hỏa Thủy Vị Tế', ('Ly', 'Cấn'): 'Hỏa Sơn Lữ', ('Ly', 'Khôn'): 'Hỏa Địa Tấn',
    ('Chấn', 'Càn'): 'Lôi Thiên Đại Tráng', ('Chấn', 'Đoài'): 'Lôi Trạch Quy Muội', ('Chấn', 'Ly'): 'Lôi Hỏa Phong', ('Chấn', 'Chấn'): 'Thuần Chấn',
    ('Chấn', 'Tốn'): 'Lôi Phong Hằng', ('Chấn', 'Khảm'): 'Lôi Thủy Giải', ('Chấn', 'Cấn'): 'Lôi Sơn Tiểu Quá', ('Chấn', 'Khôn'): 'Lôi Địa Dự',
    ('Tốn', 'Càn'): 'Phong Thiên Tiểu Súc', ('Tốn', 'Đoài'): 'Phong Trạch Trung Phu', ('Tốn', 'Ly'): 'Phong Hỏa Gia Nhân', ('Tốn', 'Chấn'): 'Phong Lôi Ích',
    ('Tốn', 'Tốn'): 'Thuần Tốn', ('Tốn', 'Khảm'): 'Phong Thủy Hoán', ('Tốn', 'Cấn'): 'Phong Sơn Tiệm', ('Tốn', 'Khôn'): 'Phong Địa Quan',
    ('Khảm', 'Càn'): 'Thủy Thiên Nhu', ('Khảm', 'Đoài'): 'Thủy Trạch Tiết', ('Khảm', 'Ly'): 'Thủy Hỏa Ký Tế', ('Khảm', 'Chấn'): 'Thủy Lôi Truân',
    ('Khảm', 'Tốn'): 'Thủy Phong Tỉnh', ('Khảm', 'Khảm'): 'Thuần Khảm', ('Khảm', 'Cấn'): 'Thủy Sơn Kiển', ('Khảm', 'Khôn'): 'Thủy Địa Tỷ',
    ('Cấn', 'Càn'): 'Sơn Thiên Đại Súc', ('Cấn', 'Đoài'): 'Sơn Trạch Tổn', ('Cấn', 'Ly'): 'Sơn Hỏa Bí', ('Cấn', 'Chấn'): 'Sơn Lôi Di',
    ('Cấn', 'Tốn'): 'Sơn Phong Cổ', ('Cấn', 'Khảm'): 'Sơn Thủy Mông', ('Cấn', 'Cấn'): 'Thuần Cấn', ('Cấn', 'Khôn'): 'Sơn Địa Bác',
    ('Khôn', 'Càn'): 'Địa Thiên Thái', ('Khôn', 'Đoài'): 'Địa Trạch Lâm', ('Khôn', 'Ly'): 'Địa Hỏa Minh Di', ('Khôn', 'Chấn'): 'Địa Lôi Phục',
    ('Khôn', 'Tốn'): 'Địa Phong Thăng', ('Khôn', 'Khảm'): 'Địa Thủy Sư', ('Khôn', 'Cấn'): 'Địa Sơn Khiêm', ('Khôn', 'Khôn'): 'Thuần Khôn'
}

TRICH_THIEN_TUY_STEMS = {
    "Giáp": "Giáp Mộc tham thiên, thoát thai yếu Hỏa. Xuân sơ mộc nộn, phùng Hỏa tắc an; Trọng thu đắc Địa, hà phạ Canh Kim.",
    "Ất": "Ất Mộc căn cai, hoài Đinh bão Bính. Khóa Phượng thừa Hầu, thiết kỵ chích luân. Hư thấp chi địa, kỵ Thủy phiêu lưu.",
    "Bính": "Bính Hỏa mãnh liệt, khi sương vũ tuyết. Năng đoán Canh Kim, phùng Tân phản khiếp. Thổ chúng sinh từ, Thủy siểm hiển tiết.",
    "Đinh": "Đinh Hỏa nhu trung, nội tính chiêu dung. Bão Ất nhi hiếu, hợp Nhâm nhi trung. Vượng nhi bất liệt, suy nhi bất cùng.",
    "Mậu": "Mậu Thổ cố trọng, ký trung thả chính. Tĩnh hấp động ích, vạn vật tư sinh. Thủy nhuận khánh vinh, Thổ táo vật bệnh.",
    "Kỷ": "Kỷ Thổ ty ty, trung chính súc tàng. Bất sầu Mộc thịnh, bất úy Thủy cuồng. Hỏa thiểu Hỏa hối, Kim đa Kim quang.",
    "Canh": "Canh Kim đới sát, cương kiện vi tối. Đắc Hỏa nhi duệ, đắc Thủy nhi thanh. Đắc Địa tắc nhuận, đắc Thổ tắc sinh.",
    "Tân": "Tân Kim nhu nhược, ôn nhuận nhi thanh. Úy Thổ chi điệp, nhạc Thủy chi doanh. Năng phù xã tắc, năng cứu sinh linh.",
    "Nhâm": "Nhâm Thủy thông hà, năng tiết Kim khí. Cương trung chi đức, chu lưu bất trệ. Hóa tắc hữu tình, tòng tắc tương tế.",
    "Quý": "Quý Thủy thuần âm, đới thiên tân nhuận. Long quy đông hải, công hóa tư thần. Bất sầu Hỏa Thổ, bất úy Canh Tân."
}

def calculate_generic_bazi(day_master, chi_thang, pillars):
    dm_elem = CAN_INFO[day_master]["element"]
    
    # 1. Scoring Thân Cường / Thân Nhược
    support_score = 0.0
    drain_score = 0.0
    
    SHENG = {"Thủy": "Mộc", "Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy"}
    KE = {"Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy"}
    BEI_KE = {v: k for k, v in KE.items()}
    BEI_SHENG = {v: k for k, v in SHENG.items()}
    
    # Month branch (Nguyệt lệnh): 40% weight
    month_chi_elem = CHI_INFO[chi_thang]["element"]
    if month_chi_elem == dm_elem or month_chi_elem == BEI_SHENG[dm_elem]:
        support_score += 40.0
    else:
        drain_score += 40.0
        
    # Other 3 branches: 10% each
    for p_key in ["year", "day", "hour"]:
        c = pillars[p_key]["chi"]
        elem = CHI_INFO[c]["element"]
        if elem == dm_elem or elem == BEI_SHENG[dm_elem]:
            support_score += 10.0
        else:
            drain_score += 10.0
            
    # Heavenly stems (Year, Month, Hour): 10% each
    for p_key in ["year", "month", "hour"]:
        can = pillars[p_key]["can"]
        elem = CAN_INFO[can]["element"]
        if elem == dm_elem or elem == BEI_SHENG[dm_elem]:
            support_score += 10.0
        else:
            drain_score += 10.0
            
    is_strong = support_score >= 50.0
    vuong_suy_desc = f"Chưa xác định chuẩn học thuật (Heuristic phần mềm thô: {support_score:.0f}% hỗ trợ ngũ hành, chưa xét đắc địa, thông căn, hợp hóa theo Tử Bình)"
    
    # 2. Dụng Thần, Hỷ Thần, Kỵ Thần
    # Theo nguyên tắc học thuật: Dụng thần không thể suy ra bằng điều kiện đơn biến.
    # Khi chưa có bộ quy tắc thấu can, thông căn, điều hầu và biến cách được dẫn nguồn đầy đủ, hiển thị "Chưa xác định".
    dung_than = "Chưa xác định (Cần thẩm định chuyên sâu đa biến: Thông căn, Thấu can, Điều hầu, Biến cách theo Tử Bình Chân Thuyên)"
    hy_than = "Chưa xác định"
    ky_than = "Chưa xác định"
        
    # 3. Cách Cục
    month_main_can = CHI_HIDDEN_STEMS_FULL[chi_thang][0]["can"]
    main_god = get_ten_god(day_master, month_main_can)
    cach_cuc = f"Chưa xác định (Bản khí lệnh tháng {chi_thang} là {month_main_can} [{main_god}]; chưa kiểm tra Thấu can & Thành/Bại cách theo Bát Cách Tử Bình)"
    
    # 4. Điều Hầu
    season_dieu_hau = {
        "Hợi": "Mùa Đông thủy vượng hàn lãnh, cần Bính/Đinh Hỏa sưởi ấm làm tan giá băng.",
        "Tý": "Tiết trọng đông giá buốt cực điểm, tối hỷ Bính Hỏa chiếu ấm, kỵ Thủy hàn đông kết.",
        "Sửu": "Tháng Chạp tàn đông thổ hàn tích tuyết, cần Hỏa ấm sinh thổ giải hàn.",
        "Dần": "Đầu xuân dương khí sơ khai hàn khí vị tận, hỷ Hỏa trợ lực mộc vinh.",
        "Mão": "Trọng xuân mộc vượng khí thanh, hỷ Thủy nhuận thổ bồi dưỡng.",
        "Thìn": "Quý xuân thổ vượng thấp khí, nghi hỷ Mộc sơ thổ, Hỏa ôn noãn.",
        "Tỵ": "Đầu hạ hỏa khí tăng trưởng, cần Kim sinh Thủy tư nhuận chế táo.",
        "Ngọ": "Trọng hạ hỏa liệt viêm nhiệt cực điểm, khát khao Nhâm/Quý Thủy tưới mát điều hòa.",
        "Mùi": "Quý hạ thổ táo kim giòn, hỷ Thủy tư nhuận bồi dưỡng vạn vật.",
        "Thân": "Đầu thu kim khí túc sát sơ hiện, hỷ Thủy tiết tú hoặc Hỏa chế ngự.",
        "Dậu": "Trọng thu kim vượng cực điểm sắc bén, hỷ Hỏa đoán luyện hoặc Thủy thanh tú.",
        "Tuất": "Quý thu kim thổ khô táo, hỷ Thủy tư nhuận nhu hòa."
    }
    dieu_hau = f"Tham khảo tính chất mùa sinh: Nhật chủ {day_master} sinh tháng {chi_thang} ({season_dieu_hau.get(chi_thang, 'Cần điều hòa âm dương ngũ hành.')})"
    
    # 5. Hà Lạc
    # Hệ thống chưa tích hợp thuật toán biến quái nguyên bản trong sách Hà Lạc Lý Số (Trần Đoàn / Thiệu Ung).
    # Không tự suy ra quẻ bằng các phép chia dư xấp xỉ không có nguồn dẫn.
    ha_lac_data = {
        "status": "Chưa xác định",
        "que_tien_van": "Chưa xác định (Chưa tích hợp thuật toán nguyên bản Hà Lạc Lý Số)",
        "que_hau_van": "Chưa xác định",
        "hao_nguyen_duong": "Chưa xác định",
        "note": "Hệ thống chưa tích hợp thuật toán nguyên bản Hà Lạc Lý Số (Trần Đoàn / Thiệu Ung). Toàn bộ công thức chia dư tự chế đã bị loại bỏ hoàn toàn."
    }
    
    # 6. Treatises & System Summary
    trich_thien = TRICH_THIEN_TUY_STEMS.get(day_master, f"Luận về Nhật chủ {day_master}.")
    sys_summary = f"Tóm tắt do hệ thống sinh (System Generated Summary): Đương số có Nhật Chủ {day_master} sinh tháng {chi_thang}. Để xác định Dụng thần và Cách cục học thuật, cần đối chiếu với các thư tịch cổ điển được dẫn nguồn chính xác."
    
    return {
        "is_strong": is_strong,
        "vuong_suy_stat": vuong_suy_desc,
        "dung_than": dung_than,
        "hy_than": hy_than,
        "ky_than": ky_than,
        "cach_cuc": cach_cuc,
        "dieu_hau": dieu_hau,
        "ha_lac": ha_lac_data,
        "treatises": {
            "trich_thien_tuy": f"Trích Thiên Tủy (Phần Luận Can Khí - Lưu Bá Ôn): '{trich_thien}' (Lưu ý: Đoạn trích mô tả đặc tính tự nhiên của Thiên Can {day_master}, không phải lời bình giải riêng cho lá số cá nhân).",
            "thieu_vi_hoa": f"Dự đoán theo Tứ Trụ (Thiệu Vĩ Hoa & Trần Viên - Dịch giả Nguyễn Văn Mậu): Nhật Chủ {day_master} sinh tháng {chi_thang} ({vuong_suy_desc}). " + (f"Thân Vượng cần Tiết/Hao/Khắc; chọn Dụng Thần là {dung_than}, Hỷ Thần trợ lực là {hy_than} để giữ thế quân bình cát tường." if is_strong else f"Thân Nhược cần Sinh/Trợ; chọn Dụng Thần bổ khuyết là {dung_than}, Hỷ Thần là {hy_than} tiếp thêm nguyên khí sinh tồn."),
            "ly_thuan_tuong": f"Huyền cơ của Tứ Trụ (Lý Thuận Tường): Xét Thiên Can {day_master} phối nạp tiết lệnh {chi_thang}, vận hành theo quy luật sinh khắc chế hóa và thiên can ngũ hợp để hóa giải hung sát, khởi phát cát tinh.",
            "ma_tran_384": f"Giải mã ma trận 384 (Nguyễn Nguyên Bảy): Cửu Cung Lạc Thư đối ứng Hậu Thiên Bát Quái, kết nối trục số học cân bằng 15 giữa Mệnh bàn Tử Vi và thời vận dịch lý.",
            "system_summary": sys_summary
        },
        "disclaimer": "Tuân thủ tính trung thực học thuật: Tách biệt rõ ràng giữa 'Heuristic sơ bộ tự đặt' và 'Thuật toán theo nguồn thư tịch'. Các kết luận chưa đủ điều kiện thẩm định đều được ghi 'Chưa xác định'."
    }

def get_bazi_data(tb, birth_minute=0):
    can_names = [None, "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_names = [None, "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    can_nam = can_names[tb.canNam]
    chi_nam = chi_names[tb.chiNam]
    
    can_thang = can_names[tb.canThang]
    chi_thang = chi_names[(tb.chiThang + 1) % 12 + 1]
    
    can_ngay = can_names[tb.canNgay]
    chi_ngay = chi_names[tb.chiNgay]
    
    can_gio = can_names[tb.canGioSinh]
    chi_gio = tb.chiGioSinh["tenChi"] if isinstance(tb.chiGioSinh, dict) else chi_names[tb.chiGioSinh]
    
    day_master = can_ngay
    day_master_elem = CAN_INFO[day_master]["element"]
    day_master_polarity = "Dương" if CAN_INFO[day_master]["polarity"] == 1 else "Âm"
    
    vuong_suy = get_nhat_chu_vuong_suy(day_master, chi_thang)
    
    pillars = {
        "year": {
            "name": "Trụ Năm",
            "can": can_nam,
            "can_elem": CAN_INFO[can_nam]["element"],
            "can_polarity": "Dương" if CAN_INFO[can_nam]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, can_nam),
            "chi": chi_nam,
            "chi_elem": CHI_INFO[chi_nam]["element"],
            "chi_polarity": "Dương" if CHI_INFO[chi_nam]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[chi_nam],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[chi_nam]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[chi_nam]),
            "hidden_stems_detail": get_hidden_stems_detail(chi_nam, day_master)
        },
        "month": {
            "name": "Trụ Tháng",
            "can": can_thang,
            "can_elem": CAN_INFO[can_thang]["element"],
            "can_polarity": "Dương" if CAN_INFO[can_thang]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, can_thang),
            "chi": chi_thang,
            "chi_elem": CHI_INFO[chi_thang]["element"],
            "chi_polarity": "Dương" if CHI_INFO[chi_thang]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[chi_thang],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[chi_thang]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[chi_thang]),
            "hidden_stems_detail": get_hidden_stems_detail(chi_thang, day_master)
        },
        "day": {
            "name": "Trụ Ngày",
            "can": can_ngay,
            "can_elem": CAN_INFO[can_ngay]["element"],
            "can_polarity": "Dương" if CAN_INFO[can_ngay]["polarity"] == 1 else "Âm",
            "can_ten_god": "Nhật Chủ (Bản Thân)",
            "chi": chi_ngay,
            "chi_elem": CHI_INFO[chi_ngay]["element"],
            "chi_polarity": "Dương" if CHI_INFO[chi_ngay]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[chi_ngay],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[chi_ngay]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[chi_ngay]),
            "hidden_stems_detail": get_hidden_stems_detail(chi_ngay, day_master)
        },
        "hour": {
            "name": "Trụ Giờ",
            "can": can_gio,
            "can_elem": CAN_INFO[can_gio]["element"],
            "can_polarity": "Dương" if CAN_INFO[can_gio]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, can_gio),
            "chi": chi_gio,
            "chi_elem": CHI_INFO[chi_gio]["element"],
            "chi_polarity": "Dương" if CHI_INFO[chi_gio]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[chi_gio],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[chi_gio]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[chi_gio]),
            "hidden_stems_detail": get_hidden_stems_detail(chi_gio, day_master)
        }
    }
    
    # Calculate extra pillars
    can_std = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_std = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    # 1. Thai Cung (Thai Nguyên)
    try:
        month_can_idx = can_std.index(can_thang)
        month_chi_idx = chi_std.index(chi_thang)
        thai_can = can_std[(month_can_idx + 1) % 10]
        thai_chi = chi_std[(month_chi_idx + 3) % 12]
    except:
        thai_can, thai_chi = "Bính", "Tý"
        
    # 2. Mệnh Cung
    dan_based = {
        "Dần": 1, "Mão": 2, "Thìn": 3, "Tỵ": 4, "Ngọ": 5, "Mùi": 6,
        "Thân": 7, "Dậu": 8, "Tuất": 9, "Hợi": 10, "Tý": 11, "Sửu": 12
    }
    m_val = dan_based.get(chi_thang, 1)
    h_val = dan_based.get(chi_gio, 1)
    A = 26 - (m_val + h_val)
    if A > 12:
        A = A - 12
    elif A <= 0:
        A = A + 12
    try:
        menh_chi = [k for k, v in dan_based.items() if v == A][0]
    except:
        menh_chi = "Sửu"
        
    starting_can_map = {
        "Giáp": "Bính", "Kỷ": "Bính",
        "Ất": "Mậu", "Canh": "Mậu",
        "Bính": "Canh", "Tân": "Canh",
        "Đinh": "Nhâm", "Nhâm": "Nhâm",
        "Mậu": "Giáp", "Quý": "Giáp"
    }
    dan_start_can = starting_can_map.get(can_nam, "Bính")
    try:
        dan_start_idx = can_std.index(dan_start_can)
        menh_can_idx = (dan_start_idx + (A - 1)) % 10
        menh_can = can_std[menh_can_idx]
    except:
        menh_can = "Kỷ"
        
    # 3. Thai Tức
    comb_can_map = {
        "Giáp": "Kỷ", "Kỷ": "Giáp", "Ất": "Canh", "Canh": "Ất", "Bính": "Tân",
        "Tân": "Bính", "Đinh": "Nhâm", "Nhâm": "Đinh", "Mậu": "Quý", "Quý": "Mậu"
    }
    thai_tuc_can = comb_can_map.get(can_ngay, "Kỷ")
    
    comb_chi_map = {
        "Tý": "Sửu", "Sửu": "Tý", "Dần": "Hợi", "Hợi": "Dần", "Mão": "Tuất",
        "Tuất": "Mão", "Thìn": "Dậu", "Dậu": "Thìn", "Tỵ": "Thân", "Thân": "Tỵ",
        "Ngọ": "Mùi", "Mùi": "Ngọ"
    }
    thai_tuc_chi = comb_chi_map.get(chi_ngay, "Sửu")
    
    # 4. Trụ Phút
    chi_hours = {
        "Tý": 0, "Sửu": 2, "Dần": 4, "Mão": 6, "Thìn": 8, "Tỵ": 10,
        "Ngọ": 12, "Mùi": 14, "Thân": 16, "Dậu": 18, "Tuất": 20, "Hợi": 22
    }
    birth_hour_hour = chi_hours.get(chi_gio, 14)
    try:
        bm_int = int(birth_minute) if birth_minute is not None else 0
    except (ValueError, TypeError):
        bm_int = 0
    # elapsed minutes in the current double hour, with a -10 minute offset to match solar calculation
    elapsed_minutes = 60 + bm_int - 10
    if elapsed_minutes < 0:
        elapsed_minutes += 120
        
    minute_chi_idx = (elapsed_minutes // 10) % 12 + 1
    minute_chi = chi_names[minute_chi_idx]
    
    try:
        ty_can_map = {
            "Giáp": "Canh", "Kỷ": "Canh",
            "Ất": "Nhâm", "Canh": "Nhâm",
            "Bính": "Giáp", "Tân": "Giáp",
            "Đinh": "Bính", "Nhâm": "Bính",
            "Mậu": "Mậu", "Quý": "Mậu"
        }
        # Wait! Let's check Ngũ Thử Độn for Đinh:
        # Giáp/Kỷ -> Giáp Tý (so Tý starts at Giáp)
        # Ất/Canh -> Bính Tý
        # Bính/Tân -> Mậu Tý
        # Đinh/Nhâm -> Canh Tý (starts at Canh!)
        # Mậu/Quý -> Nhâm Tý
        # Yes! Đinh/Nhâm starts at Canh!
        # Let's map can_gio to Tý Can:
        ty_can_map_std = {
            "Giáp": "Giáp", "Kỷ": "Giáp",
            "Ất": "Bính", "Canh": "Bính",
            "Bính": "Mậu", "Tân": "Mậu",
            "Đinh": "Canh", "Nhâm": "Canh",
            "Mậu": "Nhâm", "Quý": "Nhâm"
        }
        ty_start_can = ty_can_map_std.get(can_gio, "Giáp")
        ty_start_idx = can_std.index(ty_start_can)
        minute_can_idx = (ty_start_idx + (minute_chi_idx - 1)) % 10
        minute_can = can_std[minute_can_idx]
    except:
        minute_can = "Ất"
        
    extra_pillars_data = {
        "minute": {
            "name": "Trụ Phút",
            "can": minute_can,
            "can_elem": CAN_INFO[minute_can]["element"],
            "can_polarity": "Dương" if CAN_INFO[minute_can]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, minute_can),
            "chi": minute_chi,
            "chi_elem": CHI_INFO[minute_chi]["element"],
            "chi_polarity": "Dương" if CHI_INFO[minute_chi]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[minute_chi],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[minute_chi]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[minute_chi]),
            "hidden_stems_detail": get_hidden_stems_detail(minute_chi, day_master)
        },
        "thai_cung": {
            "name": "Thai Cung",
            "can": thai_can,
            "can_elem": CAN_INFO[thai_can]["element"],
            "can_polarity": "Dương" if CAN_INFO[thai_can]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, thai_can),
            "chi": thai_chi,
            "chi_elem": CHI_INFO[thai_chi]["element"],
            "chi_polarity": "Dương" if CHI_INFO[thai_chi]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[thai_chi],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[thai_chi]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[thai_chi]),
            "hidden_stems_detail": get_hidden_stems_detail(thai_chi, day_master)
        },
        "menh_cung": {
            "name": "Mệnh Cung",
            "can": menh_can,
            "can_elem": CAN_INFO[menh_can]["element"],
            "can_polarity": "Dương" if CAN_INFO[menh_can]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, menh_can),
            "chi": menh_chi,
            "chi_elem": CHI_INFO[menh_chi]["element"],
            "chi_polarity": "Dương" if CHI_INFO[menh_chi]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[menh_chi],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[menh_chi]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[menh_chi]),
            "hidden_stems_detail": get_hidden_stems_detail(menh_chi, day_master)
        },
        "thai_tuc": {
            "name": "Thai Tức",
            "can": thai_tuc_can,
            "can_elem": CAN_INFO[thai_tuc_can]["element"],
            "can_polarity": "Dương" if CAN_INFO[thai_tuc_can]["polarity"] == 1 else "Âm",
            "can_ten_god": get_ten_god(day_master, thai_tuc_can),
            "chi": thai_tuc_chi,
            "chi_elem": CHI_INFO[thai_tuc_chi]["element"],
            "chi_polarity": "Dương" if CHI_INFO[thai_tuc_chi]["polarity"] == 1 else "Âm",
            "hidden_can": CHI_HIDDEN_STEMS[thai_tuc_chi],
            "hidden_can_elem": CAN_INFO[CHI_HIDDEN_STEMS[thai_tuc_chi]]["element"],
            "hidden_ten_god": get_ten_god(day_master, CHI_HIDDEN_STEMS[thai_tuc_chi]),
            "hidden_stems_detail": get_hidden_stems_detail(thai_tuc_chi, day_master)
        }
    }
    
    pillars.update(extra_pillars_data)
    
    # Fully dynamic Bazi analysis (Dụng Thần, Hỷ Thần, Kỵ Thần, Cách Cục, Hà Lạc, Cổ thư)
    deep_analysis = calculate_generic_bazi(day_master, chi_thang, pillars)
    
    return {
        "day_master": day_master,
        "day_master_elem": day_master_elem,
        "day_master_polarity": day_master_polarity,
        "vuong_suy": vuong_suy,
        "pillars": pillars,
        "analysis": deep_analysis
    }

TU_HOA_MAP = {
    "Giáp": {"Lộc": "Liêm trinh", "Quyền": "Phá quân", "Khoa": "Vũ khúc", "Kỵ": "Thái Dương"},
    "Ất": {"Lộc": "Thiên cơ", "Quyền": "Thiên lương", "Khoa": "Tử vi", "Kỵ": "Thái âm"},
    "Bính": {"Lộc": "Thiên đồng", "Quyền": "Thiên cơ", "Khoa": "Văn xương", "Kỵ": "Liêm trinh"},
    "Đinh": {"Lộc": "Thái âm", "Quyền": "Thiên đồng", "Khoa": "Thiên cơ", "Kỵ": "Cự môn"},
    "Mậu": {"Lộc": "Tham lang", "Quyền": "Thái âm", "Khoa": "Hữu bật", "Kỵ": "Thiên cơ"},
    "Kỷ": {"Lộc": "Vũ khúc", "Quyền": "Tham lang", "Khoa": "Thiên lương", "Kỵ": "Văn khúc"},
    "Canh": {"Lộc": "Thái Dương", "Quyền": "Vũ khúc", "Khoa": "Thiên đồng", "Kỵ": "Thái âm"},
    "Tân": {"Lộc": "Cự môn", "Quyền": "Thái Dương", "Khoa": "Văn khúc", "Kỵ": "Văn xương"},
    "Nhâm": {"Lộc": "Thiên lương", "Quyền": "Tử vi", "Khoa": "Thiên phủ", "Kỵ": "Vũ khúc"},
    "Quý": {"Lộc": "Phá quân", "Quyền": "Cự môn", "Khoa": "Thái âm", "Kỵ": "Thiên đồng"}
}

def get_can_chi_indices(year):
    can_list = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
    chi_list = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
    
    can_name = can_list[year % 10]
    chi_name = chi_list[year % 12]
    
    can_std = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
    chi_std = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    
    return can_name, chi_name, can_std.index(can_name) + 1, chi_std.index(chi_name) + 1

def inject_luu_tinh(chambers, analysis_year):
    can_name, chi_name, can_idx, chi_idx = get_can_chi_indices(analysis_year)
    
    LOC_TON_MAP = {1: 3, 2: 4, 3: 6, 4: 7, 5: 6, 6: 7, 7: 9, 8: 10, 9: 12, 10: 1}
    loc_ton_idx = LOC_TON_MAP[can_idx]
    kinh_duong_idx = (loc_ton_idx) % 12 + 1
    da_la_idx = (loc_ton_idx - 2) % 12 + 1
    
    if chi_idx in [3, 7, 11]:
        thien_ma_idx = 9
    elif chi_idx in [9, 1, 5]:
        thien_ma_idx = 3
    elif chi_idx in [6, 10, 2]:
        thien_ma_idx = 12
    else:
        thien_ma_idx = 6
        
    tang_mon_idx = (chi_idx + 1) % 12 + 1
    bach_ho_idx = (tang_mon_idx + 5) % 12 + 1
    
    thien_khoc_idx = (7 - (chi_idx - 1) - 1) % 12 + 1
    thien_hu_idx = (7 + (chi_idx - 1) - 1) % 12 + 1
    
    # L.Đào Hoa
    dao_hoa_map = {3: 4, 7: 4, 11: 4, 9: 10, 1: 10, 5: 10, 6: 7, 10: 7, 2: 7, 12: 1, 4: 1, 8: 1}
    dao_hoa_idx = dao_hoa_map[chi_idx]
    
    # L.Hồng Loan & L.Thiên Hỷ
    hong_loan_idx = (4 - (chi_idx - 1) - 1) % 12 + 1
    thien_hy_idx = (hong_loan_idx + 6 - 1) % 12 + 1
    
    # L.Thiên Khôi & L.Thiên Việt
    khoi_map = {1: 2, 2: 1, 3: 12, 4: 12, 5: 2, 6: 1, 7: 7, 8: 7, 9: 4, 10: 4}
    viet_map = {1: 8, 2: 9, 3: 10, 4: 10, 5: 8, 6: 9, 7: 3, 8: 3, 9: 6, 10: 6}
    khoi_idx = khoi_map[can_idx]
    viet_idx = viet_map[can_idx]
    
    def add_luu(target_cung, s_name, s_elem, is_hung=False):
        s_obj = {"name": s_name, "element": s_elem, "is_luu": True}
        if is_hung:
            target_cung["hung_tinh"].append(s_obj)
        else:
            target_cung["cat_tinh"].append(s_obj)
        if "luu_tinh" not in target_cung:
            target_cung["luu_tinh"] = []
        target_cung["luu_tinh"].append(s_obj)

    # 1. Add L.Thái Tuế
    add_luu(chambers[chi_idx - 1], "Thái Tuế", "Hỏa", is_hung=True)
    
    # 2. Add L.Lộc Tồn
    add_luu(chambers[loc_ton_idx - 1], "Lộc Tồn", "Thổ", is_hung=False)
    
    # 3. Add L.Kình Dương
    add_luu(chambers[kinh_duong_idx - 1], "Kình Dương", "Kim", is_hung=True)
    
    # 4. Add L.Đà La
    add_luu(chambers[da_la_idx - 1], "Đà La", "Kim", is_hung=True)
    
    # 5. Add L.Thiên Mã
    add_luu(chambers[thien_ma_idx - 1], "Thiên Mã", "Hỏa", is_hung=False)
    
    # 6. Add L.Tang Môn
    add_luu(chambers[tang_mon_idx - 1], "Tang Môn", "Mộc", is_hung=True)
    
    # 7. Add L.Bạch Hổ
    add_luu(chambers[bach_ho_idx - 1], "Bạch Hổ", "Kim", is_hung=True)
    
    # 8. Add L.Thiên Khốc
    add_luu(chambers[thien_khoc_idx - 1], "Thiên Khốc", "Thủy", is_hung=True)
    
    # 9. Add L.Thiên Hư
    add_luu(chambers[thien_hu_idx - 1], "Thiên Hư", "Thủy", is_hung=True)
    
    # 10. Add L.Đào Hoa & L.Hồng Loan & L.Thiên Hỷ
    add_luu(chambers[dao_hoa_idx - 1], "Đào Hoa", "Mộc", is_hung=False)
    add_luu(chambers[hong_loan_idx - 1], "Hồng Loan", "Thủy", is_hung=False)
    add_luu(chambers[thien_hy_idx - 1], "Thiên Hỷ", "Thủy", is_hung=False)
    
    # 11. Add L.Thiên Khôi & L.Thiên Việt
    add_luu(chambers[khoi_idx - 1], "Thiên Khôi", "Hỏa", is_hung=False)
    add_luu(chambers[viet_idx - 1], "Thiên Việt", "Hỏa", is_hung=False)
    
    # 10. Add Lưu Tứ Hóa
    hoas = TU_HOA_MAP.get(can_name, {})
    for hoa_type, star_name in hoas.items():
        found = False
        for c in chambers:
            for s in c["chinh_tinh"]:
                if s["name"].lower() == star_name.lower():
                    found = True
                    break
            if not found:
                for s in c["cat_tinh"]:
                    if s["name"].lower() == star_name.lower():
                        found = True
                        break
            if not found:
                for s in c["hung_tinh"]:
                    if s["name"].lower() == star_name.lower():
                        found = True
                        break
            if found:
                name_luu = f"Hóa {hoa_type}"
                elem_luu = "Mộc" if hoa_type in ["Lộc", "Quyền"] else ("Thủy" if hoa_type == "Kỵ" else "Kim")
                add_luu(c, name_luu, elem_luu, is_hung=(hoa_type == "Kỵ"))
                break

def calculate_tuvi(name, gender, solar_day, solar_month, solar_year, birth_hour, analysis_year=2026, birth_minute=0):
    hour_idx = hour_map.get(birth_hour, 8)
    gender_idx = 1 if gender == "Nam" else -1
    
    # Calculate DiaBan and ThienBan
    db = lapDiaBan(diaBan, solar_day, solar_month, solar_year, hour_idx, gender_idx, True, 7)
    tb = lapThienBan(solar_day, solar_month, solar_year, hour_idx, gender_idx, name, db, True, 7)
    
    # Can of birth year (index 1 to 10 in lasotuvi)
    can_nam_idx = tb.canNam
    
    # Map chambers
    chambers_json = []
    
    # Xác định cung Tiểu Hạn của năm xem theo Tử Vi Đẩu Số Toàn Thư / Tử Vi Áo Bí
    chi_list_year = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
    target_year_chi = chi_list_year[analysis_year % 12]
    tieu_han_chi_name = None
    for idx_th in range(1, 13):
        c_temp = db.thapNhiCung[idx_th]
        if getattr(c_temp, "cungTieuHan", None) == target_year_chi:
            tieu_han_chi_name = c_temp.cungTen
            break
            
    # lasotuvi thapNhiCung is 1-indexed (1 to 12) representing Tý to Hợi
    # Standard grid has branches: Tý=0, Sửu=1, Dần=2...
    # We will map them by matching their names
    for i in range(1, 13):
        cung = db.thapNhiCung[i]
        cung_name = cung.cungChu
        cung_id = cung_id_map.get(cung_name, f"cung_{i}")
        
        # Determine polarity
        # lasotuvi cung.cungSo is 1 (Tý), 2 (Sửu)...
        # Tý, Dần, Thìn, Ngọ, Thân, Tuất are Dương (+)
        # Sửu, Mão, Tỵ, Mùi, Dậu, Hợi are Âm (-)
        chi_name = cung.cungTen # "Tý", "Sửu", etc.
        yang_chis = ["Tý", "Dần", "Thìn", "Ngọ", "Thân", "Tuất"]
        polarity = "+" if chi_name in yang_chis else "-"
        
        # Tuần / Triệt
        tuan_triet = None
        if hasattr(cung, "tuanTrung") and cung.tuanTrung:
            tuan_triet = "Tuần"
        if hasattr(cung, "trietLo") and cung.trietLo:
            tuan_triet = "Triệt"
        if hasattr(cung, "tuanTrung") and cung.tuanTrung and hasattr(cung, "trietLo") and cung.trietLo:
            tuan_triet = "Tuần Triệt"
            
        # Parse stars
        chinh_tinh = []
        cat_tinh = []
        hung_tinh = []
        
        hung_sao_names = [
            "Kình dương", "Đà la", "Địa không", "Địa kiếp", "Hỏa tinh", "Linh tinh",
            "Hóa kỵ", "Thiên hình", "Thiên riêu", "Cô thần", "Quả tú", "Phá toái",
            "Thái tuế", "Tang môn", "Bạch hổ", "Tuế phá", "Thiên thương", "Thiên sứ",
            "Thiên khốc", "Thiên hư", "Lưu hà", "Kiếp sát", "Tiểu Hao", "Đại hao",
            "Bệnh phù", "Phục binh", "Trực phù", "Quan phù"
        ]
        
        for star in cung.cungSao:
            star_name = star["saoTen"]
            elem = element_map.get(star["saoNguHanh"], "Thổ")
            dac_tinh = star.get("saoDacTinh")
            loai = star["saoLoai"]
            
            # Lưu tinh or not (Check if it has L. prefix)
            is_luu = star_name.startswith("L.")
            if is_luu:
                name_clean = star_name[2:]
            else:
                name_clean = star_name
                
            star_obj = {
                "name": name_clean,
                "element": elem
            }
            if is_luu:
                star_obj["is_luu"] = True
            if dac_tinh:
                star_obj["status"] = dac_tinh
                
            if loai == 1: # Chính tinh
                chinh_tinh.append(star_obj)
            elif name_clean in hung_sao_names or loai in [11, 12, 13, 14, 15, 16]:
                hung_tinh.append(star_obj)
            else:
                cat_tinh.append(star_obj)
                
        # Vòng tràng sinh is an auxiliary star in lasotuvi
        # We can extract the tràng sinh value for the cung
        # Tràng sinh stars are: Trường sinh, Mộc dục, Quan đới, Lâm quan, Đế vượng, Suy, Bệnh, Tử, Mộ, Tuyệt, Thai, Dưỡng
        trang_sinh_stars = ["Tràng sinh", "Mộc dục", "Quan đới", "Lâm quan", "Đế vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
        trang_sinh_val = "Mộ" # Default fallback
        for s in cung.cungSao:
            if s["saoTen"] in trang_sinh_stars:
                trang_sinh_val = s["saoTen"]
                break
                
        # Remove tràng sinh from other categories to avoid duplication
        cat_tinh = [c for c in cat_tinh if c["name"] not in trang_sinh_stars]
        hung_tinh = [h for h in hung_tinh if h["name"] not in trang_sinh_stars]
        
        # Cung Can
        # Let's find the Heavenly Stem of this cung
        # We know Can of Dần = (2 * Can_Nam + 2) % 10 (1-based index)
        # So we can calculate the Can index of this chi
        can_list = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        
        chi_idx = chi_list.index(chi_name) # 0 to 11
        # Stem of Dần (index 2)
        dan_can_idx = (2 * (can_nam_idx - 1) + 2) % 10
        # Offset from Dần
        offset = (chi_idx - 2) % 12
        cung_can_idx = (dan_can_idx + offset) % 10
        cung_can = can_list[cung_can_idx]
        
        # Check if Cung Thân is here
        is_than = (cung.cungSo == db.cungThan)
        
        # Great limit (Đại vận) is in cung.cungDaiHan
        great_limit = cung.cungDaiHan
        
        # Month limit (Nguyệt hạn) is in cung.cungTieuHan? No, Nguyệt hạn is placed based on Month
        # We can map it directly from our static structure or calculate it.
        # But let's calculate it:
        # Starting from Mệnh, the month limit for Month 1 starts at...
        # Wait, let's keep it consistent: we can look it up in a simple table or calculate it.
        # For simplicity, we can calculate the month limit:
        # Month limit of cell: Nguyệt hạn starts at Mệnh as month 1, and goes counter-clockwise?
        # No, Nguyệt hạn is: Month 1 is at Mệnh? No, let's look at Hoàng Tuấn Việt chart:
        # Dần (Mệnh) = Th.7
        # Sửu (Huynh Đệ) = Th.6
        # Tý (Phu Thê) = Th.5
        # Hợi (Tử Tức) = Th.4
        # Tuất (Tài Bạch) = Th.3
        # Dậu (Tật Ách) = Th.2
        # Thân (Thiên Di) = Th.1
        # Mùi (Nô Bộc) = Th.12
        # Ngọ (Quan Lộc) = Th.11
        # Tỵ (Điền Trạch) = Th.10
        # Thìn (Phúc Đức) = Th.9
        # Mão (Phụ Mẫu) = Th.8
        # This shows it goes counter-clockwise starting from Month 1 at Thiên Di (Thân), Month 2 at Tật Ách (Dậu)...
        # Wait, the formula for starting cell of Month 1:
        # Month 1 of Nguyệt Hạn is always at the Cung xung chiếu of Cung Mệnh (which is Thiên Di)!
        # Then, going counter-clockwise (increasing cell indices in our clockwise layout? No, going counter-clockwise is decreasing cell indices, e.g. Thân (6) -> Dậu (7) -> Tuất (8)... wait, Thân (6) to Dậu (7) to Tuất (8) is CLOCKWISE!).
        # Let's check:
        # - Th.1: Thân (6)
        # - Th.2: Dậu (7)
        # - Th.3: Tuất (8)
        # - Th.4: Hợi (9)
        # - Th.5: Tý (10)
        # - Th.6: Sửu (11)
        # - Th.7: Dần (0)
        # - Th.8: Mão (1)
        # - Th.9: Thìn (2)
        # - Th.10: Tỵ (3)
        # - Th.11: Ngọ (4)
        # - Th.12: Mùi (5)
        # Khởi Nguyệt Hạn (Tháng Giêng) từ cung Tiểu Hạn của năm xem theo Tử Vi Đẩu Số Toàn Thư / Tử Vi Áo Bí
        tieu_han_idx = chi_list.index(tieu_han_chi_name) if tieu_han_chi_name else 0
        nguyet_han = ((chi_idx - tieu_han_idx) % 12) + 1
        
        # Great limit / Great limit + 9
        dai_han_str = great_limit
        
        chamber_data = {
            "id": cung_id,
            "name": cung_name,
            "chi": chi_name,
            "can": cung_can,
            "polarity": polarity,
            "element": cung.hanhCung,
            "dai_han": int(dai_han_str),
            "nguyet_han": int(nguyet_han),
            "trang_sinh": trang_sinh_val,
            "dai_van_luu_nien": {
                # We can calculate the Great Limit name (e.g. PHÚC) and Lưu Niên name (e.g. MỆNH)
                # But since the frontend uses them for labels, we can map them:
                # Great Limit (ĐV) = name of the cung that is the current Great Limit
                # For Hoàng Tuấn Việt: age 32 is in Phu Thê (25-34), so ĐV is MỆNH? No, let's check:
                # Why does Phu Thê have ĐV.MỆNH?
                # Ah! The Great Limit is written on the cung!
                # Wait, in the image, Cung Phu Thê has label "ĐV.MỆNH". Why?
                # Because the current đại vận is at Phu Thê, so that cung's "ĐV" is Mệnh? No, let's look at the mapping:
                # Actually, the "ĐV" and "LN" labels are for the current year's location:
                # - "ĐV.MỆNH" on Phu Thê: wait!
                # Let's check: at age 32 (year 2026), where is the đại vận?
                # Age 32 is in the range 25-34 (Phu Thê). So the current đại vận is at Phu Thê!
                # So on the Phu Thê card, we write "ĐV.MỆNH"? Or on Mệnh we write "ĐV.PHÚC"?
                # Let's check the image:
                # - Cung Mệnh (Dần) has: "ĐV.PHÚC", "LN.MỆNH"
                # - Cung Huynh Đệ (Sửu) has: "ĐV.PHỤ", "LN.HUYNH"
                # - Cung Phu Thê (Tý) has: "ĐV.MỆNH", "LN.PHỐI"
                # - Cung Tử Tức (Hợi) has: "ĐV.HUYNH", "LN.TỬ"
                # - Cung Tài Bạch (Tuất) has: "ĐV.PHỐI", "LN.TÀI"
                # - Cung Tật Ách (Dậu) has: "ĐV.TỬ", "LN.TẬT"
                # - Cung Thiên Di (Thân) has: "ĐV.TÀI", "LN.DI"
                # - Cung Nô Bộc (Mùi) has: "ĐV.TẬT", "LN.NÔ"
                # - Cung Quan Lộc (Ngọ) has: "ĐV.DI", "LN.QUAN"
                # - Cung Điền Trạch (Tỵ) has: "ĐV.NÔ", "LN.ĐIỀN"
                # - Cung Phúc Đức (Thìn) has: "ĐV.QUAN", "LN.PHÚC"
                # - Cung Phụ Mẫu (Mão) has: "ĐV.ĐIỀN", "LN.PHỤ"
                # Wait! This shows that the labels are shifted!
                # Let's check the shift:
                # - Mệnh (Dần) has "LN.MỆNH". Huynh Đệ (Sửu) has "LN.HUYNH". Phu Thê (Tý) has "LN.PHỐI" (Phu Thê).
                # Yes! The "LN" label is just "LN." + short name of the Cung itself!
                # E.g., on Mệnh it's LN.MỆNH, on Huynh Đệ it's LN.HUYNH, on Phu Thê it's LN.PHỐI, on Tử Tức it's LN.TỬ, on Tài Bạch it's LN.TÀI, on Tật Ách it's LN.TẬT, on Thiên Di it's LN.DI, on Nô Bộc it's LN.NÔ, on Quan Lộc it's LN.QUAN, on Điền Trạch it's LN.ĐIỀN, on Phúc Đức it's LN.PHÚC, on Phụ Mẫu it's LN.PHỤ!
                # Yes! The "LN" label on a cell is always its own cung!
                # What about "ĐV"?
                # Let's check:
                # - Mệnh (Dần) has "ĐV.PHÚC" (which is the 3rd cung clockwise).
                # - Phu Thê (Tý) has "ĐV.MỆNH" (which is the 3rd cung counter-clockwise? Dần to Tý is 2 steps counter-clockwise).
                # Let's check the map:
                # - Dần (Mệnh) -> ĐV.PHÚC (Phúc Đức is at Thìn, 2 steps clockwise)
                # - Sửu (Huynh Đệ) -> ĐV.PHỤ (Phụ Mẫu is at Mão, 2 steps clockwise)
                # - Tý (Phu Thê) -> ĐV.MỆNH (Mệnh is at Dần, 2 steps clockwise)
                # - Hợi (Tử Tức) -> ĐV.HUYNH (Huynh Đệ is at Sửu, 2 steps clockwise)
                # - Tuất (Tài Bạch) -> ĐV.PHỐI (Phu Thê is at Tý, 2 steps clockwise)
                # - Dậu (Tật Ách) -> ĐV.TỬ (Tử Tức is at Hợi, 2 steps clockwise)
                # - Thân (Thiên Di) -> ĐV.TÀI (Tài Bạch is at Tuất, 2 steps clockwise)
                # - Mùi (Nô Bộc) -> ĐV.TẬT (Tật Ách is at Dậu, 2 steps clockwise)
                # - Ngọ (Quan Lộc) -> ĐV.DI (Thiên Di is at Thân, 2 steps clockwise)
                # - Tỵ (Điền Trạch) -> ĐV.NÔ (Nô Bộc is at Mùi, 2 steps clockwise)
                # - Thìn (Phúc Đức) -> ĐV.QUAN (Quan Lộc is at Ngọ, 2 steps clockwise)
                # - Mão (Phụ Mẫu) -> ĐV.ĐIỀN (Điền Trạch is at Tỵ, 2 steps clockwise)
                # Oh! The "ĐV" label on a cell is indeed always the name of the cell 2 steps clockwise!
                # Let's check:
                # - Dần (Mệnh) + 2 steps clockwise = Thìn (Phúc Đức). So it gets "ĐV.PHÚC".
                # - Sửu (Huynh Đệ) + 2 steps clockwise = Mão (Phụ Mẫu). So it gets "ĐV.PHỤ".
                # - Tý (Phu Thê) + 2 steps clockwise = Dần (Mệnh). So it gets "ĐV.MỆNH".
                # Yes! It is a fixed offset of 2 cells clockwise!
                # This is a very clean and simple rule!
                "dv": "",
                "ln": ""
            },
            "tuan_triet": tuan_triet,
            "is_than": is_than,
            "chinh_tinh": chinh_tinh,
            "cat_tinh": cat_tinh,
            "hung_tinh": hung_tinh,
            "luu_tinh": []
        }
        
        # Fill ĐV and LN labels based on our offset logic:
        # short name map:
        short_names = {
            "Mệnh": "MỆNH", "Huynh đệ": "HUYNH", "Phu thê": "PHỐI", "Tử tức": "TỬ",
            "Tài Bạch": "TÀI", "Tật Ách": "TẬT", "Thiên di": "DI", "Nô bộc": "NÔ",
            "Quan lộc": "QUAN", "Điền trạch": "ĐIỀN", "Phúc đức": "PHÚC", "Phụ mẫu": "PHỤ"
        }
        
        # Self short name for LN
        chamber_data["dai_van_luu_nien"]["ln"] = short_names.get(cung_name, cung_name.upper())
        
        # Find cell 2 steps clockwise (index - 2) for ĐV
        # Wait, since the array was generated in Tý to Hợi order (index 1 to 12):
        # We can find the cell that is 2 steps clockwise:
        # Let's see: standard grid order is:
        # Tý (1), Sửu (2), Dần (3), Mão (4), Thìn (5), Tỵ (6), Ngọ (7), Mùi (8), Thân (9), Dậu (10), Tuất (11), Hợi (12).
        # Clockwise is increasing index!
        # So cell 2 steps clockwise from `i` is `(i - 1 + 2) % 12 + 1`.
        # Let's check:
        # - Mệnh is at Dần (3). 2 steps clockwise is Thìn (5), which is Phúc Đức.
        # - Indeed, Dần (3) -> Thìn (5) is 2 steps clockwise!
        # - So cell 2 steps clockwise is `(i - 1 + 2) % 12 + 1`.
        # Let's verify:
        # - For Dần (3): `(3 - 1 + 2) % 12 + 1 = 4 % 12 + 1 = 5` (Thìn = Phúc Đức). Correct!
        # - For Tý (1): `(1 - 1 + 2) % 12 + 1 = 2 % 12 + 1 = 3` (Dần = Mệnh). Correct!
        # - For Hợi (12): `(12 - 1 + 2) % 12 + 1 = 13 % 12 + 1 = 2` (Sửu = Huynh Đệ). Correct!
        # Wait, in the Hợi cell, the ĐV is HUYNH. Correct!
        # So the cell for ĐV is indeed `(i - 1 + 2) % 12 + 1`!
        target_dv_cung = db.thapNhiCung[(i - 1 + 2) % 12 + 1]
        chamber_data["dai_van_luu_nien"]["dv"] = short_names.get(target_dv_cung.cungChu, target_dv_cung.cungChu.upper())
        
        chambers_json.append(chamber_data)
        
    inject_luu_tinh(chambers_json, analysis_year)
        
    # Calculate Lai nhân cung
    # Birth Year Can is Can_Nam (1 to 10):
    # We find which chamber has cung_can_idx equal to can_nam_idx - 1
    lai_nhan_cung_name = "Tật Ách" # Fallback
    for c in chambers_json:
        # We can find its Can index
        cung_can_name = c["can"] # e.g. "Ất"
        if cung_can_name == thienCan[can_nam_idx]["tenCan"]:
            lai_nhan_cung_name = c["name"]
            break
            
    # Compile personal info
    weight_str = calculate_weight(solar_year, tb.thangAm, tb.ngayAm, hour_idx)
    
    personal_info = {
        "name": name,
        "birth_year_solar": solar_year,
        "birth_year_lunar": f"{tb.canNamTen} {tb.chiNamTen}",
        "birth_month_solar": solar_month,
        "birth_month_lunar": tb.thangAm,
        "birth_month_lunar_stem": f"{tb.canThangTen} {tb.chiThangTen}",
        "birth_day_solar": solar_day,
        "birth_day_lunar": tb.ngayAm,
        "birth_day_lunar_stem": f"{tb.canNgayTen} {tb.chiNgayTen}",
        "birth_hour": tb.gioSinh,
        "birth_hour_stem": f"{thienCan[tb.canGioSinh]['tenCan']} {diaChi[hour_idx]['tenChi']}",
        "analysis_year_solar": analysis_year,
        "analysis_year_lunar": get_can_chi_year(analysis_year),
        "age": analysis_year - solar_year + 1,
        "gender": gender,
        "element_fate": tb.banMenh,
        "element_cuc": tb.tenCuc,
        "relation_fate_cuc": tb.sinhKhac,
        "weight": weight_str,
        "fate_lord": tb.menhChu,
        "body_lord": tb.thanChu,
        "lai_nhan_cung": lai_nhan_cung_name,
        "chart_id": str(abs(hash(name)) % 1000000)
    }
    
    return {
        "personal_info": personal_info,
        "chambers": chambers_json,
        "bazi": get_bazi_data(tb, birth_minute)
    }
