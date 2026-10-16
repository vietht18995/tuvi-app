import http.server
import json
import os
import sys
import urllib.parse

# Ensure stdout uses UTF-8 to avoid encoding errors on Windows terminal
if sys.stdout.encoding != 'UTF-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Setup path to import our engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import re

def sanitize_filename(name):
    # Only allow alphanumeric, spaces, hyphens, and Vietnamese unicode characters
    clean = re.sub(r'[^\w\s-]', '', str(name), flags=re.UNICODE).strip()
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean[:50] or "User"

class TuViRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Security Layer: Normalize path and prevent directory traversal
        clean_path = urllib.parse.unquote(self.path.split('?')[0])
        
        # 1. Allowed main web interface assets
        if clean_path in ('/', '/index.html', '/styles.css', '/script.js', '/favicon.ico', '/favicon.svg', '/favicon.png', '/logo.svg'):
            return super().do_GET()
            
        # 2. Allowed generated download files: only .pdf and .xlsx in local root
        pure_name = clean_path.lstrip('/')
        if (clean_path.endswith('.pdf') or clean_path.endswith('.xlsx')) and '/' not in pure_name and '\\' not in pure_name:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), pure_name)
            if os.path.exists(file_path):
                return super().do_GET()
                
        # 3. Block all other requests (.py, .bat, .exe, .json, .git, system files, etc.)
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
            super().do_POST()

def run_server(port=8000):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, TuViRequestHandler)
    print(f"Server Tử Vi đang chạy tại http://localhost:{port}...")
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
