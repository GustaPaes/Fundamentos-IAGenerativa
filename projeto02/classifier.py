from llm_client import LLMClient
from validator import extract_json, validate_classification, safe_fallback

class MessageClassifier:
    def __init__(self, allowed_categories, temperature=0.0):
        self.allowed = allowed_categories
        self.llm = LLMClient(temperature=temperature)

    def build_prompt(self, message: str) -> str:
        categories = ", ".join(self.allowed)
        return f"""
Classifique a mensagem do cliente em uma das categorias: {categories}.

Responda APENAS com um objeto JSON no formato:
{{ "category": "categoria", "confidence": 0.0 a 1.0, "explanation": "justificativa" }}

Mensagem: "{message}"
"""

    def classify(self, message: str) -> dict:
        prompt = self.build_prompt(message)
        try:
            raw = self.llm.get_completion(prompt)
        except Exception as e:
            # Erro de API: fallback imediato
            return {
                "success": False,
                "category": "outros",
                "confidence": 0.0,
                "explanation": f"Erro na API: {e}",
                "raw": None
            }

        # Tentar extrair JSON
        parsed = extract_json(raw)
        if parsed and validate_classification(parsed, self.allowed):
            return {
                "success": True,
                "category": parsed["category"],
                "confidence": parsed.get("confidence", 0.0),
                "explanation": parsed.get("explanation", ""),
                "raw": raw
            }
        else:
            # Fallback seguro
            fallback = safe_fallback(raw)
            return {
                "success": False,
                "category": fallback["category"],
                "confidence": fallback["confidence"],
                "explanation": fallback["explanation"],
                "raw": raw,
                "_fallback": True
            }