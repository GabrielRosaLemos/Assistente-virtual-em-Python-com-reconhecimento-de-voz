import json
import requests
from pathlib import Path
from datetime import datetime

from tts import falar
from speech import ouvir
from normalizacao import normalizar
from wakeword import aguardar_jarvis


# =========================
# CONFIGURAÇÕES
# =========================

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

BASE_DIR = Path(__file__).parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_FILE = MEMORY_DIR / "memory.json"

MEMORY_DIR.mkdir(exist_ok=True)


# =========================
# MEMÓRIA
# =========================

def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except:
            return {}
    return {}

def save_memory(mem):
    MEMORY_FILE.write_text(
        json.dumps(mem, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def update_memory(mem, user, jarvis):
    mem["last_interaction"] = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "jarvis": jarvis
    }


# =========================
# OLLAMA
# =========================

def perguntar_jarvis(pergunta, memoria):
    contexto = ""

    if "name" in memoria:
        contexto += f"O nome do usuário é {memoria['name']}.\n"

    if "last_interaction" in memoria:
        contexto += (
            f"Última conversa: "
            f"{memoria['last_interaction']['user']} → "
            f"{memoria['last_interaction']['jarvis']}\n"
        )

    prompt = f"""
Você é JARVIS, um assistente inteligente, educado e direto.
Responda de forma clara, objetiva e natural.

{contexto}

Usuário: {pergunta}
JARVIS:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=60)
    r.raise_for_status()

    return r.json()["response"].strip()


# =========================
# MAIN (ALEXA MODE)
# =========================

def main():
    memoria = load_memory()

    print("🤖 JARVIS ONLINE (modo sempre ativo)")
    falar("Jarvis online. Aguardando comando.")

    while True:
        try:
            print("👂 Aguardando 'Jarvis'...")
            aguardar_jarvis()

            falar("Sim?")
            print("🎤 Ouvindo pergunta...")
            pergunta = ouvir()

            if not pergunta:
                continue

            pergunta = normalizar(pergunta)
            print(f"Você › {pergunta}")

            # ENCERRAR
            if pergunta in ["sair", "encerrar", "desligar"]:
                resposta = "Até mais, Gabriel."
                print(f"Jarvis › {resposta}")
                falar(resposta)
                break

            # RESPOSTAS CURTAS
            if pergunta in ["obrigado", "valeu", "ok", "beleza"]:
                resposta = "Sempre à disposição."
                falar(resposta)
                continue

            # APRENDER NOME
            if pergunta.startswith("meu nome é"):
                nome = pergunta.split("meu nome é", 1)[1].strip()
                memoria["name"] = nome
                save_memory(memoria)
                resposta = f"Prazer em conhecê-lo, {nome}."
                falar(resposta)
                continue

            # LLM
            resposta = perguntar_jarvis(pergunta, memoria)
            print(f"Jarvis › {resposta}")
            falar(resposta)

            update_memory(memoria, pergunta, resposta)
            save_memory(memoria)

        except KeyboardInterrupt:
            falar("Sistema desligado.")
            break
        except Exception as e:
            print(f"[ERRO] {e}")
            falar("Ocorreu um erro interno.")


if __name__ == "__main__":
    main()
