import re

def normalizar(texto: str) -> str:
    if not texto:
        return ""

    texto = texto.lower().strip()

    # Correções comuns do STT
    substituicoes = {
        "jervis": "jarvis",
        "jairies": "jarvis",
        "jarves": "jarvis",
        "javes": "jarvis",
        "gervais": "jarvis",
        "sair": "sair",
        "finalizar": "sair",
        "encerrar": "sair"
    }

    for errado, certo in substituicoes.items():
        texto = re.sub(rf"\b{errado}\b", certo, texto)

    # Remove ruídos
    texto = re.sub(r"[^\w\sáéíóúâêôãõç]", "", texto)

    # Normaliza espaços
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()
