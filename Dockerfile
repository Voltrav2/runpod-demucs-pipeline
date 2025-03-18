FROM python:3.10-slim

# Çalışma dizini oluştur
WORKDIR /app

# Gerekli paketleri yükle
RUN apt-get update && apt-get install -y ffmpeg wget && apt-get clean

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir runpod demucs torch numpy requests

# API handler dosyasını ekleyelim
COPY rp_handler.py /app/rp_handler.py
COPY runpod.json /app/runpod.json

# Çalıştırma komutu
CMD ["python", "-u", "rp_handler.py"]
