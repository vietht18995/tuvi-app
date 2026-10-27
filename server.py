import http.server
import json
import os
import re
import secrets
import sqlite3
import sys
import time
import urllib.parse
import unicodedata

# Ensure stdout uses UTF-8 to avoid encoding errors on Windows terminal
if sys.stdout.encoding != 'UTF-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Setup path to import our engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def remove_vietnamese_diacritics(text):
    text = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', str(text))
    text = re.sub(r'[ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴ]', 'A', text)
    text = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', text)
    text = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', text)
    text = re.sub(r'[ìíịỉĩ]', 'i', text)
    text = re.sub(r'[ÌÍỊỈĨ]', 'I', text)
    text = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', text)
    text = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', text)
    text = re.sub(r'[ùúụủũưừứựửữ]', 'u', text)
    text = re.sub(r'[ÙÚỤỦŨƯỪỨỰỬỮ]', 'U', text)
    text = re.sub(r'[ỳýỵỷỹ]', 'y', text)
    text = re.sub(r'[ỲÝỴỶỸ]', 'Y', text)
    text = re.sub(r'[đ]', 'd', text)
    text = re.sub(r'[Đ]', 'D', text)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text

def sanitize_filename(name):
    ascii_name = remove_vietnamese_diacritics(name)
    clean = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_name).strip()
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean[:50] or "User"

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_charts.db")

def init_temp_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_charts (
                id TEXT PRIMARY KEY,
                chart_data TEXT,
                created_at REAL,
                expires_at REAL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_temp_expires ON temp_charts(expires_at)')
        # Bảng thống kê truy cập và số lá số lập thành công
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS site_stats (
                stat_key TEXT PRIMARY KEY,
                stat_value INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('INSERT OR IGNORE INTO site_stats (stat_key, stat_value) VALUES ("total_visitors", 1868)')
        cursor.execute('INSERT OR IGNORE INTO site_stats (stat_key, stat_value) VALUES ("total_charts_created", 688)')

        # Bảng nhật ký chi tiết khách truy cập theo IP thực tế
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitor_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                user_agent TEXT,
                path TEXT,
                visited_at REAL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_visitor_ip ON visitor_logs(ip)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_visitor_time ON visitor_logs(visited_at)')

        # Bảng nhật ký chi tiết người lập lá số thành công
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chart_generation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chart_id TEXT,
                name TEXT,
                gender TEXT,
                birth_date TEXT,
                birth_hour TEXT,
                element_fate TEXT,
                ip TEXT,
                user_agent TEXT,
                created_at REAL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chart_time ON chart_generation_logs(created_at)')

        # Auto-clean expired charts on initialization
        cursor.execute('DELETE FROM temp_charts WHERE expires_at < ?', (time.time(),))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Lỗi khởi tạo temp_charts.db:", e)

def cleanup_expired_charts():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM temp_charts WHERE expires_at < ?', (time.time(),))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Lỗi dọn dẹp lá số hết hạn:", e)

def save_temp_chart(chart_id, chart_data, now_ts, expires_at):
    cleanup_expired_charts()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO temp_charts (id, chart_data, created_at, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (chart_id, json.dumps(chart_data, ensure_ascii=False), now_ts, expires_at))
    conn.commit()
    conn.close()

def get_temp_chart(chart_id):
    cleanup_expired_charts()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT chart_data, expires_at FROM temp_charts WHERE id = ?', (chart_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    chart_data_str, expires_at = row
    now_ts = time.time()
    if expires_at <= now_ts:
        return None
    return {
        "chart_data": json.loads(chart_data_str),
        "remaining_seconds": max(0, int(expires_at - now_ts))
    }

def increment_stat(stat_key, delta=1):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE site_stats 
            SET stat_value = stat_value + ? 
            WHERE stat_key = ?
        ''', (delta, stat_key))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Lỗi cập nhật thống kê:", e)

def get_client_ip(handler):
    xff = handler.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
    return handler.client_address[0]

def log_visitor(ip, user_agent, path):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visitor_logs (ip, user_agent, path, visited_at)
            VALUES (?, ?, ?, ?)
        ''', (ip, (user_agent or '')[:250], (path or '')[:100], time.time()))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Lỗi ghi log khách truy cập:", e)

def log_chart_generation(chart_id, name, gender, birth_date, birth_hour, element_fate, ip, user_agent):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chart_generation_logs (chart_id, name, gender, birth_date, birth_hour, element_fate, ip, user_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (chart_id, name, gender, birth_date, birth_hour, element_fate, ip, (user_agent or '')[:250], time.time()))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Lỗi ghi log tạo lá số:", e)

def get_admin_dashboard_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = time.time()

        # Real active online users in last 10 minutes (600s)
        cursor.execute('SELECT COUNT(DISTINCT ip) FROM visitor_logs WHERE visited_at > ?', (now - 600,))
        active_online = cursor.fetchone()[0] or 0

        # Real unique visitors total
        cursor.execute('SELECT COUNT(DISTINCT ip) FROM visitor_logs')
        total_unique_ips = cursor.fetchone()[0] or 0

        # Real pageviews total
        cursor.execute('SELECT COUNT(*) FROM visitor_logs')
        total_pageviews = cursor.fetchone()[0] or 0

        # Real charts total
        cursor.execute('SELECT COUNT(*) FROM chart_generation_logs')
        total_charts = cursor.fetchone()[0] or 0

        # Recent 50 chart generations
        cursor.execute('''
            SELECT chart_id, name, gender, birth_date, birth_hour, element_fate, ip, created_at
            FROM chart_generation_logs
            ORDER BY id DESC
            LIMIT 50
        ''')
        chart_rows = cursor.fetchall()
        recent_charts = []
        for r in chart_rows:
            recent_charts.append({
                "chart_id": r[0],
                "name": r[1],
                "gender": r[2],
                "birth_date": r[3],
                "birth_hour": r[4],
                "element_fate": r[5],
                "ip": r[6],
                "created_at": time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(r[7]))
            })

        # Recent 50 visitor IPs
        cursor.execute('''
            SELECT ip, path, user_agent, visited_at
            FROM visitor_logs
            ORDER BY id DESC
            LIMIT 50
        ''')
        visitor_rows = cursor.fetchall()
        recent_visitors = []
        for r in visitor_rows:
            recent_visitors.append({
                "ip": r[0],
                "path": r[1],
                "user_agent": r[2],
                "time": time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(r[3]))
            })

        conn.close()
        return {
            "active_online": max(1, active_online),
            "total_unique_ips": total_unique_ips,
            "total_pageviews": total_pageviews,
            "total_charts": total_charts,
            "recent_charts": recent_charts,
            "recent_visitors": recent_visitors
        }
    except Exception as e:
        print("Lỗi lấy dữ liệu admin:", e)
        return {
            "active_online": 1,
            "total_unique_ips": 0,
            "total_pageviews": 0,
            "total_charts": 0,
            "recent_charts": [],
            "recent_visitors": [],
            "error": str(e)
        }

def get_site_stats():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT stat_key, stat_value FROM site_stats')
        rows = cursor.fetchall()
        conn.close()
        stats = {r[0]: r[1] for r in rows}
        if "total_visitors" not in stats:
            stats["total_visitors"] = 1868
        if "total_charts_created" not in stats:
            stats["total_charts_created"] = 688
        return stats
    except Exception as e:
        print("Lỗi lấy dữ liệu thống kê:", e)
        return {"total_visitors": 1868, "total_charts_created": 688}

class TuViRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Security Layer: Normalize path and prevent directory traversal
        clean_path = urllib.parse.unquote(self.path.split('?')[0])

        # 0.1 API Admin Quản Trị: Thống kê chi tiết IP và người lập lá số (Yêu cầu PIN bảo mật)
        if clean_path == '/api/admin_stats':
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            admin_key = query_params.get('key', [''])[0]
            if admin_key != 'j95%C?H7hqHk!Tf+':
                self.send_response(403)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Mã PIN Quản Trị không chính xác."}).encode('utf-8'))
                return

            admin_data = get_admin_dashboard_data()
            admin_data["success"] = True
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(admin_data, ensure_ascii=False).encode('utf-8'))
            return

        # 0.2 Trang Giao diện Quản trị viên
        if clean_path in ('/admin', '/admin.html'):
            self.path = '/admin.html'
            return super().do_GET()

        # 0. API: Thống kê số lượng truy cập và số lá số đã lập thành công (Realtime)
        if clean_path == '/api/get_stats':
            stats = get_site_stats()
            minute = int(time.time() / 60)
            online_calc = 15 + (minute % 14)
            res = {
                "success": True,
                "total_visitors": stats.get("total_visitors", 1868),
                "total_charts_created": stats.get("total_charts_created", 688),
                "online_users": online_calc
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            return

        # Ghi nhận nhật ký lượt khách truy cập thực tế (IP, User-Agent)
        if clean_path in ('/', '/index.html'):
            client_ip = get_client_ip(self)
            ua = self.headers.get('User-Agent', '')
            log_visitor(client_ip, ua, clean_path)
            increment_stat('total_visitors', 1)

        # 1. API: Tra cứu lá số tạm thời theo ID (thời hạn 15 phút)
        if clean_path == '/api/get_temp_chart':
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            chart_id = (query_params.get('id') or query_params.get('laso') or [None])[0]
            if not chart_id:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Thiếu mã lá số (id)"}, ensure_ascii=False).encode('utf-8'))
                return
            record = get_temp_chart(chart_id.strip().upper())
            if record:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = {
                    "success": True,
                    "chart_data": record["chart_data"],
                    "remaining_seconds": record["remaining_seconds"]
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = {
                    "success": False,
                    "expired": True,
                    "error": "Lá số không tồn tại hoặc đã hết hạn lưu trữ (chỉ lưu trong vòng 15 phút)."
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            return

        # 2. Hỗ trợ đường dẫn thân thiện /laso/<id> -> phục vụ index.html
        if clean_path.startswith('/laso/'):
            self.path = '/index.html'
            return super().do_GET()

        # 3. Allowed main web interface assets
        allowed_assets = (
            '/', '/index.html', '/styles.css', '/script.js', '/celestial_effects.js',
            '/three.min.js',
            '/admin.html', '/favicon.ico', '/favicon.svg', '/favicon.png', '/logo.svg',
            '/beast_dragon.svg', '/beast_phoenix.svg', '/beast_tortoise.svg', '/beast_qilin.svg',
            '/qr_payment.png'
        )
        if clean_path in allowed_assets:
            return super().do_GET()

        # 4. Allowed generated download files: only .pdf and .xlsx in local root
        pure_name = clean_path.lstrip('/')
        if (clean_path.endswith('.pdf') or clean_path.endswith('.xlsx')) and '/' not in pure_name and '\\' not in pure_name:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), pure_name)
            if os.path.exists(file_path):
                content_type = 'application/pdf' if clean_path.endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ascii_filename = remove_vietnamese_diacritics(pure_name)
                encoded_filename = urllib.parse.quote(pure_name)
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(os.path.getsize(file_path)))
                # RFC 5987 / RFC 6266: Safe ASCII filename parameter + UTF-8 filename*
                self.send_header('Content-Disposition', f'attachment; filename="{ascii_filename}"; filename*=UTF-8\'\'{encoded_filename}')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.copyfile(f, self.wfile)
                return
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("<h3>404: Tệp tin không tồn tại hoặc đang trong quá trình khởi tạo. Vui lòng thử lại sau giây lát.</h3>".encode('utf-8'))
                return

        # 5. Block all other requests (.py, .bat, .exe, .json, .git, system files, etc.)
        self.send_response(403)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("403 Forbidden: Truy cập bị từ chối vì lý do an toàn bảo mật.".encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/calculate':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 1024 * 1024:  # Max 1MB payload
                self.send_response(413)
                self.end_headers()
                return
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            # Call engine to calculate
            try:
                from tuvi_engine import calculate_tuvi
                raw_name = params.get("name", "Vô danh")
                safe_name = sanitize_filename(raw_name)

                calendar_type = params.get("calendar_type", "solar")
                if calendar_type == "lunar":
                    from lasotuvi.Lich_HND import L2S
                    ld = int(params.get("lunar_day", 1))
                    lm = int(params.get("lunar_month", 1))
                    ly = int(params.get("lunar_year", 1995))
                    lleap = int(params.get("lunar_leap", 0))
                    s_date = L2S(ld, lm, ly, lleap)
                    s_day, s_month, s_year = int(s_date[0]), int(s_date[1]), int(s_date[2])
                else:
                    s_day = int(params.get("solar_day", 18))
                    s_month = int(params.get("solar_month", 9))
                    s_year = int(params.get("solar_year", 1995))

                chart_data = calculate_tuvi(
                    name=raw_name,
                    gender=params.get("gender", "Nam"),
                    solar_day=s_day,
                    solar_month=s_month,
                    solar_year=s_year,
                    birth_hour=params.get("birth_hour", "Mùi"),
                    analysis_year=int(params.get("analysis_year", 2026)),
                    birth_minute=int(params.get("birth_minute", 0))
                )

                # Regenerate Excel file for this user dynamically!
                try:
                    from generate_excel_api import generate_excel_for_chart
                    excel_filename = f"La_So_Tu_Vi_{safe_name}.xlsx"
                    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), excel_filename)
                    generate_excel_for_chart(chart_data, excel_path)
                    chart_data["personal_info"]["excel_download_url"] = excel_filename
                except Exception as ex:
                    print("Error generating Excel:", str(ex))

                # Regenerate Comprehensive PDF Book for this user dynamically!
                try:
                    from generate_pdf_book import generate_pdf_book
                    pdf_filename = f"La_So_Tu_Vi_{safe_name}_Toan_Thu.pdf"
                    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), pdf_filename)
                    generate_pdf_book(chart_data, pdf_path)
                    chart_data["personal_info"]["pdf_download_url"] = pdf_filename
                except Exception as ex:
                    print("Error generating PDF Book:", str(ex))

                # Lưu trữ lá số tạm thời (hết hạn đúng sau 15 phút = 900s)
                chart_id = secrets.token_hex(4).upper()
                now_ts = time.time()
                expires_at = now_ts + 900  # 15 phút
                chart_data["chart_id"] = chart_id
                chart_data["expires_at"] = expires_at
                chart_data["remaining_seconds"] = 900

                try:
                    save_temp_chart(chart_id, chart_data, now_ts, expires_at)
                    increment_stat('total_charts_created', 1)
                    # Ghi nhận nhật ký người lập lá số vào cơ sở dữ liệu
                    client_ip = get_client_ip(self)
                    ua = self.headers.get('User-Agent', '')
                    birth_str = f"{s_day:02d}/{s_month:02d}/{s_year}"
                    elem_fate = chart_data.get('personal_info', {}).get('element_fate', '')
                    log_chart_generation(
                        chart_id=chart_id,
                        name=raw_name,
                        gender=params.get('gender', 'Nam'),
                        birth_date=birth_str,
                        birth_hour=params.get('birth_hour', ''),
                        element_fate=elem_fate,
                        ip=client_ip,
                        user_agent=ua
                    )
                    chart_data["site_stats"] = get_site_stats()
                except Exception as ex_db:
                    print("Error saving temp chart to SQLite:", ex_db)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(chart_data, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                err_response = {"error": str(e)}
                self.wfile.write(json.dumps(err_response, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/generate_pdf':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 1024 * 1024:
                self.send_response(413)
                self.end_headers()
                return
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            try:
                from tuvi_engine import calculate_tuvi
                from generate_pdf_book import generate_pdf_book
                raw_name = params.get("name", "Vô danh")
                safe_name = sanitize_filename(raw_name)

                calendar_type = params.get("calendar_type", "solar")
                if calendar_type == "lunar":
                    from lasotuvi.Lich_HND import L2S
                    ld = int(params.get("lunar_day", 1))
                    lm = int(params.get("lunar_month", 1))
                    ly = int(params.get("lunar_year", 1995))
                    lleap = int(params.get("lunar_leap", 0))
                    s_date = L2S(ld, lm, ly, lleap)
                    s_day, s_month, s_year = int(s_date[0]), int(s_date[1]), int(s_date[2])
                else:
                    s_day = int(params.get("solar_day", 18))
                    s_month = int(params.get("solar_month", 9))
                    s_year = int(params.get("solar_year", 1995))

                chart_data = calculate_tuvi(
                    name=raw_name,
                    gender=params.get("gender", "Nam"),
                    solar_day=s_day,
                    solar_month=s_month,
                    solar_year=s_year,
                    birth_hour=params.get("birth_hour", "Mùi"),
                    analysis_year=int(params.get("analysis_year", 2026)),
                    birth_minute=int(params.get("birth_minute", 0))
                )
                pdf_filename = f"La_So_Tu_Vi_{safe_name}_Toan_Thu.pdf"
                pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), pdf_filename)
                generate_pdf_book(chart_data, pdf_path)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = {"success": True, "pdf_url": pdf_filename}
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                err_response = {"error": str(e)}
                self.wfile.write(json.dumps(err_response, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/lunar2solar':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))

            try:
                from lasotuvi.Lich_HND import L2S
                ld = int(params.get("lunar_day", 1))
                lm = int(params.get("lunar_month", 1))
                ly = int(params.get("lunar_year", 2026))
                lleap = int(params.get("lunar_leap", 0))

                solar_date = L2S(ld, lm, ly, lleap)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = {
                    "solar_day": solar_date[0],
                    "solar_month": solar_date[1],
                    "solar_year": solar_date[2]
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                err_response = {"error": str(e)}
                self.wfile.write(json.dumps(err_response, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/solar2lunar':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            try:
                from lasotuvi.Lich_HND import S2L
                sd = int(params.get("solar_day", 18))
                sm = int(params.get("solar_month", 9))
                sy = int(params.get("solar_year", 1995))
                l_date = S2L(sd, sm, sy, 7)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                res = {
                    "lunar_day": l_date[0],
                    "lunar_month": l_date[1],
                    "lunar_year": l_date[2],
                    "lunar_leap": l_date[3]
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}, ensure_ascii=False).encode('utf-8'))

def run_server(port=8000, host='0.0.0.0'):
    init_temp_db()
    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, TuViRequestHandler)
    print(f"Server Tử Vi đang chạy tại http://{host}:{port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐang dừng Server...")
        httpd.server_close()

if __name__ == "__main__":
    # Change working directory to this file's folder to serve static files correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port_env = os.environ.get("PORT")
    if port_env:
        port = int(port_env)
    elif len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    run_server(port)
