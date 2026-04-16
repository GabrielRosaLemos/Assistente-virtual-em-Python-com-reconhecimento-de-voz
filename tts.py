import subprocess
import tempfile
import os
import winsound

PIPER_PATH = r"C:\Users\Gabriel\jarvis\piper\piper.exe"
VOICE_PATH = r"C:\Users\Gabriel\jarvis\piper\voices\pt_BR-faber-medium.onnx"

def falar(texto: str):
    if not texto.strip():
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    try:
        processo = subprocess.Popen(
            [PIPER_PATH, "-m", VOICE_PATH, "-f", wav_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8"
        )

        processo.communicate(texto, timeout=15)

        if os.path.exists(wav_path):
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)

    except Exception as e:
        print(f"[TTS ERRO] {e}")

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
