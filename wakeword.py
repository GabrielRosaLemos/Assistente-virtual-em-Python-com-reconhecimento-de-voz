import pvporcupine
import pyaudio
import struct

ACCESS_KEY = "GkivtNL7/GUojrwyrCPrUTgFHlqoH9iKaliDaIsXN6jvSSz3XMZBwA=="

def aguardar_jarvis():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=["jarvis"]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("👂 Aguardando palavra-chave: 'Jarvis'")

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from(
                "h" * porcupine.frame_length,
                pcm
            )

            if porcupine.process(pcm) >= 0:
                return True

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
