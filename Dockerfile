FROM python:3.11-slim

# Cài đặt Chromium, fonts tiếng Việt và các tiện ích hệ thống
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-dejavu-core \
    fontconfig \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces yêu cầu chạy dưới user UID 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    CHROME_BIN=/usr/bin/chromium \
    PYTHONUNBUFFERED=1

WORKDIR $HOME/app

# Cài đặt Python dependencies
COPY --chown=user requirements.txt $HOME/app/
RUN pip install --no-cache-dir --user -r requirements.txt

# Sao chép toàn bộ mã nguồn ứng dụng
COPY --chown=user . $HOME/app/

EXPOSE 7860

CMD ["python", "-u", "server.py", "7860"]
