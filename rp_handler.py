import runpod
import subprocess
import os
import requests

OUTPUT_DIR = "/app/separated"

# Catbox'a yükleme fonksiyonu
def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    files = {"fileToUpload": open(file_path, "rb")}
    data = {"reqtype": "fileupload"}
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        return response.text.strip()
    else:
        return None

# RunPod işleyicisi
def handler(job):
    audio_url = job["input"]["audio"]

    # MP3 dosyasını indir
    input_path = "/tmp/input.mp3"
    subprocess.run(["wget", "-O", input_path, audio_url], check=True)

    # Demucs ile ayrıştır
    subprocess.run(["demucs", "-o", OUTPUT_DIR, input_path], check=True)

    # Çıktıyı bul
    separated_path = os.path.join(OUTPUT_DIR, "htdemucs", "input", "vocals.wav")

    # Catbox'a yükle
    catbox_url = upload_to_catbox(separated_path)

    if catbox_url:
        return {"catbox_url": catbox_url}
    else:
        return {"error": "Catbox upload failed"}

# RunPod servisini başlat
runpod.serverless.start({"handler": handler})
