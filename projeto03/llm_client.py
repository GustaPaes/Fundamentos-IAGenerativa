import os
from dotenv import load_dotenv
from openai import OpenAI

# groq is an optional provider; import only if available
try:
    from groq import Groq
except ImportError:
    Groq = None

# embeddings locais simples sem PyTorch
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    _LOCAL_VECTORIZER = None  # será criado sob demanda
except ImportError:
    _LOCAL_VECTORIZER = None

load_dotenv()

class LLMClient:
    def __init__(self, provider="openai"):
        self.provider = provider
        
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        elif provider == "groq":
            if Groq is None:
                raise ImportError("Biblioteca groq não instalada")
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def generate_text(self, system_prompt, user_prompt, temperature=0.2):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        
        elif self.provider == "groq":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            # o SDK Groq devolve um modelo `ChatCompletion` onde o texto está em
            # response.choices[0].message.content. vamos tentar tirar daí primeiro.
            text = None
            if hasattr(response, "choices") and response.choices:
                first = response.choices[0]
                msg = getattr(first, "message", None)
                if msg is not None:
                    text = getattr(msg, "content", None)
            if text:
                return text.strip()

            # se não conseguirmos, convertemos para JSON e procuramos a primeira
            # string mais significativa (exemplo: quando o retorno é APIResponse).
            try:
                data = response.json()
            except Exception:
                return str(response)

            def _first_string(obj):
                if isinstance(obj, str):
                    return obj
                if isinstance(obj, dict):
                    # preferir campos com 'content' ou 'text'
                    for k, v in obj.items():
                        if k.lower() in ("content", "text", "output", "message"):
                            res = _first_string(v)
                            if res is not None:
                                return res
                    for v in obj.values():
                        res = _first_string(v)
                        if res is not None:
                            return res
                if isinstance(obj, list):
                    for v in obj:
                        res = _first_string(v)
                        if res is not None:
                            return res
                return None

            text = _first_string(data)
            return text.strip() if text is not None else str(data)

    def get_embedding(self, text: str, model: str = "text-embedding-3-small"):
        """Gera embedding do texto.

        Tenta primeiro com a OpenAI (se disponível e com cota).
        Se falhar, usa embeddings locais baseados em frequência de palavras.
        """
        # tentar OpenAI primeiro
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and self.provider == "openai":
            try:
                resp = self.client.embeddings.create(model=model, input=text)
                return resp.data[0].embedding
            except Exception:
                pass  # continua para fallback
        elif api_key and self.provider == "groq":
            try:
                temp = OpenAI(api_key=api_key)
                resp = temp.embeddings.create(model=model, input=text)
                return resp.data[0].embedding
            except Exception:
                pass  # continua para fallback

        # fallback: embeddings locais simples baseados em frequência de palavras
        import re
        from collections import Counter
        
        # limpar e tokenizar
        words = re.findall(r'\b[a-záéíóúâêôãõç]+\b', text.lower())
        
        if not words:
            # se vazio, retornar vetor zero
            return [0.0] * 100
        
        # contar frequências
        word_freq = Counter(words)
        total_words = len(words)
        
        # criar embedding de 100 dimensões baseado em hash de palavras
        embedding = [0.0] * 100
        for word, count in word_freq.items():
            # usar hash da palavra para decidir qual dimensão
            h = hash(word) % 100
            embedding[h] += count / total_words
        
        # normalizar
        norm = sum(x**2 for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding

