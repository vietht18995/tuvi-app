import os
import sys

# Ensure UTF-8 output encoding for print
if sys.stdout.encoding != 'UTF-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Define paths
KNOWLEDGE_ROOT = r"C:\Users\VietHT\.gemini\antigravity\knowledge"
PDF_DIR = os.path.join(KNOWLEDGE_ROOT, "tuvi_pdf")
MD_DIR = os.path.join(KNOWLEDGE_ROOT, "tuvi_md")

# Create directories if they do not exist
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(MD_DIR, exist_ok=True)

def convert_pdf_to_md(pdf_path, md_path):
    try:
        import pypdf
    except ImportError:
        print("Library 'pypdf' is required. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        import pypdf
        
    print(f"Bắt đầu chuyển đổi: {os.path.basename(pdf_path)} -> {os.path.basename(md_path)}")
    try:
        reader = pypdf.PdfReader(pdf_path)
        num_pages = len(reader.pages)
        
        md_lines = []
        md_lines.append(f"# Tài liệu Tử Vi: {os.path.splitext(os.path.basename(pdf_path))[0]}\n")
        md_lines.append(f"*Nguồn: Tệp PDF gốc `{os.path.basename(pdf_path)}`*")
        md_lines.append(f"*Số trang: {num_pages}*\n")
        md_lines.append("---\n")
        
        for idx, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text:
                md_lines.append(f"## Trang {idx}\n")
                md_lines.append(text)
                md_lines.append("\n---\n")
            else:
                md_lines.append(f"## Trang {idx}\n*(Trang này không có văn bản hoặc là trang quét ảnh)*\n")
                md_lines.append("\n---\n")
                
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        print(f"Chuyển đổi thành công: {os.path.basename(pdf_path)}")
        return True
    except Exception as e:
        print(f"Lỗi khi chuyển đổi file {pdf_path}: {str(e)}")
        return False

def scan_and_convert():
    print(f"Đang quét thư mục PDF: {PDF_DIR}")
    if not os.path.exists(PDF_DIR):
        print(f"Thư mục {PDF_DIR} không tồn tại.")
        return
        
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("Không tìm thấy tệp PDF mới nào.")
        return
        
    converted_count = 0
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        md_filename = os.path.splitext(pdf_file)[0] + ".md"
        md_path = os.path.join(MD_DIR, md_filename)
        
        # Convert if MD file does not exist, or if PDF is newer than MD
        if not os.path.exists(md_path) or os.path.getmtime(pdf_path) > os.path.getmtime(md_path):
            success = convert_pdf_to_md(pdf_path, md_path)
            if success:
                converted_count += 1
                
    print(f"Hoàn thành quét. Đã chuyển đổi mới/cập nhật {converted_count} tệp.")

if __name__ == "__main__":
    scan_and_convert()
