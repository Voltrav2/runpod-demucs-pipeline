import os
import torchaudio
import requests
from demucs.separate import main as demucs_separate

# Torchaudio backend ayarla
torchaudio.set_audio_backend("sox_io")

# Catbox'tan dosya indirme fonksiyonu
def download_audio(url, save_path):
    os.system(f"wget '{url}' -O {save_path}")
    if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
        raise Exception("Dosya indirme başarısız!")

# Demucs ile vokalleri ayırma fonksiyonu
def separate_audio(file_path, output_dir="separated"):
    os.makedirs(output_dir, exist_ok=True)
    demucs_separate(["--out", output_dir, file_path])
    return output_dir

# RunPod API request fonksiyonu
def send_to_runpod(audio_url):
    url = "https://api.runpod.ai/v2/ndekrltji0qa6k/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_RUNPOD_API_KEY"
    }
    data = {"input": {"audio": audio_url}}
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    AUDIO_URL = "https://files.catbox.moe/9cuuzm.mp3"
    LOCAL_AUDIO_PATH = "/tmp/test.mp3"

    print("📥 Dosya indiriliyor...")
    download_audio(AUDIO_URL, LOCAL_AUDIO_PATH)

    print("🎵 Vokal ayrıştırma işlemi başlıyor...")
    output_folder = separate_audio(LOCAL_AUDIO_PATH)

    print("🚀 RunPod'a gönderiliyor...")
    response = send_to_runpod(AUDIO_URL)
    print(response)
