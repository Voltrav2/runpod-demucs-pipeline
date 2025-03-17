import runpod
import demucs.separate
import os
import requests

def handler(event):
    input_audio = event['input'].get('audio')

    if not input_audio:
        return {"error": "Audio URL is missing."}

    # Dosyayı indir
    local_audio_path = "/tmp/input_audio.mp3"
    try:
        response = requests.get(input_audio, stream=True)
        if response.status_code == 200:
            with open(local_audio_path, "wb") as audio_file:
                for chunk in response.iter_content(chunk_size=8192):
                    audio_file.write(chunk)
        else:
            return {"error": "Failed to download audio file."}
    except Exception as e:
        return {"error": f"Error downloading file: {str(e)}"}

    # Demucs işlemini çalıştır
    output_folder = "/app/separated"
    os.system(f"demucs -o {output_folder} {local_audio_path}")

    # Çıktıları döndür
    return {
        "vocal": f"{output_folder}/htdemucs/input_audio/vocals.wav",
        "no_vocal": f"{output_folder}/htdemucs/input_audio/no_vocals.wav"
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
