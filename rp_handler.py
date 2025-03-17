import runpod
import demucs.separate
import os

def handler(event):
    input_audio = event['input'].get('audio_url')

    # Burada Demucs işlemini gerçekleştireceğiz
    output_folder = "separated"
    os.system(f"demucs -o {output_folder} {input_audio}")

    # Ayrıştırılmış dosyaların yollarını döndür
    return {
        "vocal": f"{output_folder}/htdemucs/vocals.wav",
        "no_vocal": f"{output_folder}/htdemucs/no_vocals.wav"
    }

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
