FROM python:3.9

# Gerekli paketleri yükle
RUN apt-get update && apt-get install -y ffmpeg

# Geri kalan kurulumlar
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "rp_handler.py"]
