import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI com a chave de API
client = OpenAI(api_key=openai)

# Teste simples com tratamento de erros
try:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente técnico."},
            {
                "role": "user",
                "content": (
                    "Explique IA Generativa para um diretor técnico, "
                    "focando em riscos e arquitetura. "
                    "Resultado em 3 parágrafos."
                )
            }
        ],
        temperature=0.7
    )
    print(resposta.choices[0].message.content)
except Exception as e:
    print(f"Erro ao chamar API OpenAI: {e}")
    print("Verifique se a variável OPENAI_API_KEY está definida e se a quota não foi excedida.")
