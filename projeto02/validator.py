import json
import re
from typing import Optional, List, Dict, Any

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """Extrai o primeiro JSON válido de uma string (ignora markdown)."""
    # Remove blocos de código markdown
    text = re.sub(r'```json\s*|\s*```', '', text)
    # Procura por { ... } ou [ ... ] de forma ingênua (melhor usar regex)
    try:
        # Tenta parsear direto
        return json.loads(text)
    except json.JSONDecodeError:
        # Tenta encontrar o primeiro par de chaves
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
    return None

def validate_category(category: str, allowed: List[str]) -> bool:
    """Verifica se a categoria está na lista permitida (case-insensitive)."""
    return category.lower() in [c.lower() for c in allowed]

def validate_classification(data: Dict, allowed: List[str]) -> bool:
    """Valida se o dicionário tem os campos obrigatórios e categoria permitida."""
    if not isinstance(data, dict):
        return False
    if "category" not in data:
        return False
    if not validate_category(data["category"], allowed):
        return False
    # Opcional: validar confidence (se existir)
    return True

def safe_fallback(raw_response: str, default_category: str = "outros") -> Dict:
    """
    Fallback seguro: retorna um dicionário com categoria padrão e indicação de erro.
    """
    return {
        "category": default_category,
        "confidence": 0.0,
        "explanation": "Falha no parsing ou validação. Resposta bruta: " + raw_response[:100],
        "_error": True,
        "_raw": raw_response
    }