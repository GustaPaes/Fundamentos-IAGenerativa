import datetime
import random
import re
import string
from typing import Dict, Optional, Tuple


def data_atual() -> str:
    """Retorna a data atual em formato ISO (YYYY-MM-DD)."""
    return datetime.date.today().isoformat()


def calcular_idade(data_nascimento: str) -> Optional[int]:
    """Calcula idade a partir de uma data (YYYY-MM-DD ou DD/MM/YYYY)."""
    if not data_nascimento:
        return None

    # Aceita formatos comuns
    patterns = [r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})", r"(?P<d>\d{1,2})/(?P<m>\d{1,2})/(?P<y>\d{4})"]
    for pat in patterns:
        m = re.search(pat, data_nascimento)
        if m:
            year = int(m.group("y"))
            month = int(m.group("m"))
            day = int(m.group("d"))
            try:
                born = datetime.date(year, month, day)
            except ValueError:
                return None
            today = datetime.date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return age
    return None


def converter_temperatura(texto: str) -> Optional[str]:
    """Conversor simples de temperatura a partir de texto que contenha valores e unidades."""
    # Detecta formatos como 30C, 30°C, 30C para F ou 86F para C
    m = re.search(r"(?P<valor>-?\d+(?:[\.,]\d+)?)\s*°?\s*(?P<orig>[cCfF])\b", texto)
    if not m:
        return None

    valor = float(m.group("valor").replace(",", "."))
    orig = m.group("orig").upper()
    if orig == "C":
        f = valor * 9 / 5 + 32
        return f"{valor:.1f}°C é {f:.1f}°F"
    else:
        c = (valor - 32) * 5 / 9
        return f"{valor:.1f}°F é {c:.1f}°C"


def calcular_imc(peso_kg: float, altura_m: float) -> str:
    """Calcula IMC e retorna faixa de classificação."""
    if altura_m <= 0:
        return "Altura deve ser maior que zero."
    imc = peso_kg / (altura_m**2)
    faixa = ""
    if imc < 18.5:
        faixa = "Abaixo do peso"
    elif imc < 25:
        faixa = "Peso normal"
    elif imc < 30:
        faixa = "Sobrepeso"
    else:
        faixa = "Obesidade"
    return f"Seu IMC é {imc:.1f} ({faixa})."


def gerar_senha(tamanho: int = 12) -> str:
    """Gera uma senha aleatória com letras, dígitos e símbolos."""
    if tamanho < 4:
        tamanho = 4
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_"
    return "".join(random.choice(caracteres) for _ in range(tamanho))


def detectar_funcao(texto: str) -> Optional[Tuple[str, Dict[str, object]]]:
    """Tenta identificar se o texto do usuário pede para usar uma função.

    Retorna (nome_funcao, argumentos) ou None se nenhuma função foi detectada.
    """
    lower = texto.lower()

    # Calcular idade
    if "idade" in lower and ("nasc" in lower or "data" in lower or "anivers" in lower):
        # tenta extrair data
        m = re.search(r"(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})", texto)
        if m:
            return ("calcular_idade", {"data_nascimento": m.group(1)})

    # Conversão de temperatura
    if any(w in lower for w in ["celsius", "fahrenheit", "°c", "°f", "c para f", "f para c"]):
        m = re.search(r"(-?\d+(?:[\.,]\d+)?)\s*°?\s*([cCfF])\b", texto)
        if m:
            return ("converter_temperatura", {"texto": m.group(0)})

    # IMC
    if "imc" in lower or "indice de massa" in lower:
        # extrair peso e altura simples
        m = re.search(r"(\d+[\.,]?\d*)\s*(kg|kgs|quil?o?s?)", lower)
        n = re.search(r"(\d+[\.,]?\d*)\s*(m|metros?)", lower)
        if m and n:
            peso = float(m.group(1).replace(",", "."))
            altura = float(n.group(1).replace(",", "."))
            return ("calcular_imc", {"peso_kg": peso, "altura_m": altura})

    # Gerador de senha
    if "senha" in lower and any(w in lower for w in ["gerar", "criar", "nova"]):
        tamanho = 12
        m = re.search(r"(\d+)\s*(?:caracteres|chars|tamanho)", lower)
        if m:
            tamanho = int(m.group(1))
        return ("gerar_senha", {"tamanho": tamanho})

    return None
