# Temel Python image'ı
FROM python:3.10-slim

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y \
    ffmpeg wget curl && \
    apt-get clean

# Çalışma dizini
WORKDIR /app

# Gerekli Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kod dosyalarını container içine kopyala
COPY . .

# Docker container başlatıldığında çalıştırılacak komut
CMD ["python", "server.py"]
