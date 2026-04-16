import pyttsx3

engine = pyttsx3.init()

# Ajustes de voz
engine.setProperty("rate", 175)   # velocidade (150–190 é bom)
engine.setProperty("volume", 1.0) # volume máximo

def falar(texto: str):
    if not texto:
        return
    engine.say(texto)
    engine.runAndWait()

    engine.setProperty("rate", 160)   # fala mais calma
    engine.setProperty("volume", 0.9)

