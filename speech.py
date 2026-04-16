import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")

def ouvir():
    print("🎤 Ouvindo...")
    audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype="float32")
    sd.wait()

    audio = np.squeeze(audio)

    segments, _ = model.transcribe(audio, language="pt")
    texto = "".join(seg.text for seg in segments).strip()

    return texto
