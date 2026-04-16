import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

for i, voice in enumerate(voices):
    print(f"[{i}]")
    print("  ID:", voice.id)
    print("  Nome:", voice.name)
    print("  Idioma:", voice.languages)
    print("-" * 30)
