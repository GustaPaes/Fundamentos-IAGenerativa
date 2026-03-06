"""Cliente LLM agnóstico (OpenAI ou Groq) para projeto04.

O projeto permite selecionar o provedor via variável de ambiente `LLM_PROVIDER`
(ou automaticamente escolhe um provider disponível com chave de API).
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

# groq é opcional; importamos apenas se disponível
try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None

load_dotenv()


class LLMClient:
    def __init__(self, provider: str = None):
        """Inicializa o cliente do LLM.

        provider: "openai" ou "groq". Se omitido, escolhe automaticamente
        com base nas chaves de API disponíveis.
        """
        self.provider = (provider or os.getenv("LLM_PROVIDER", "")).strip().lower()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")

        # Seleção automática de provider
        if not self.provider:
            if self.openai_key:
                self.provider = "openai"
            elif self.groq_key:
                self.provider = "groq"

        if self.provider == "openai":
            if not self.openai_key:
                raise ValueError("OPENAI_API_KEY não encontrado no ambiente")
            self.client = OpenAI(api_key=self.openai_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        elif self.provider == "groq":
            if Groq is None:
                raise ImportError("Biblioteca groq não instalada")
            if not self.groq_key:
                raise ValueError("GROQ_API_KEY não encontrado no ambiente")
            self.client = Groq(api_key=self.groq_key)
            self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        else:
            raise ValueError(f"Provider desconhecido: {self.provider}")

    def generate_text(self, messages: list, temperature: float = 0.2) -> str:
        """Gera texto usando o provider configurado.

        Espera `messages` no formato padrão de chat (lista de dicts com `role` e `content`).
        """

        if self.provider == "openai":
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()

        # Groq tem resposta similar, mas pode variar na estrutura das mensagens
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        # A maioria dos retornos tem choices[0].message.content
        try:
            return resp.choices[0].message.content.strip()
        except Exception:
            # fallback genérico
            try:
                return str(resp)
            except Exception:
                return ""