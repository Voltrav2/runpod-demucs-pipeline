import runpod
import demucs.separate
import os
import requests

def handler(event):
    input_audio = event['input'].get('audio')  # "audio_url" yerine "audio" kullandık

    if not input_audio:
        return {"error": "No audio URL provided."}

    # Eğer input_audio bir URL ise, önce indir
    if input_audio.startswith("http"):
        audio_path = "/tmp/input_audio.mp3"
        response = requests.get(input_audio)
        if response.status_code == 200:
            with open(audio_path, "wb") as f:
                f.write(response.content)
            input_audio = audio_path  # Demucs'a dosya yolu verilecek
        else:
            return {"error": "Failed to download audio file."}

    # Demucs işlemi
    output_folder = "separated"
    os.system(f"demucs -o {output_folder} {input_audio}")
    
    # Çıktı klasörünü al
    try:
        output_subfolder = os.listdir(f"{output_folder}/htdemucs")[0]  # İlk klasörü al
        return {
            "vocal": f"{output_folder}/htdemucs/{output_subfolder}/vocals.wav",
            "no_vocal": f"{output_folder}/htdemucs/{output_subfolder}/no_vocals.wav"
        }
    except Exception as e:
        return {"error": f"Failed to find separated files: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
