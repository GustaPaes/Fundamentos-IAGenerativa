import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model="gpt-4o-mini", temperature=0.0, max_retries: int = 0):
        # limitar retries evita longos bloqueios quando a cota expira (429)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=max_retries)
        self.model = model
        self.temperature = temperature

    def get_completion(self, prompt, max_tokens=150):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Levanta exceção para ser tratada em nível superior
            raise Exception(f"Erro na API: {e}")