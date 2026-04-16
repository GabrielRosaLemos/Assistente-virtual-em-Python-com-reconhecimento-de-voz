import requests
import sys

print("INICIO")
sys.stdout.flush()

url = "http://127.0.0.1:11434/api/chat"

payload = {
    "model": "llama3",
    "stream": False,
    "messages": [
        {"role": "user", "content": "quem é você?"}
    ]
}

print("ANTES DO POST")
sys.stdout.flush()

try:
    r = requests.post(url, json=payload, timeout=300)
    print("DEPOIS DO POST")
    print("STATUS:", r.status_code)
    print("TEXTO BRUTO:")
    print(repr(r.text))
except Exception as e:
    print("ERRO:", repr(e))

sys.stdout.flush()
