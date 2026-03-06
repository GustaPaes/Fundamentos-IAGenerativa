"""Assistente de chat com memória, persona e integração de funções.

Este projeto demonstra um chatbot CLI com controle de histórico, limites
(de tamanho e comando de limpeza), persistência em JSON e execução de
funções Python quando o usuário solicita.
"""

import json
import os

from dotenv import load_dotenv

try:
    # quando executado como pacote (python -m projeto04.main)
    from .llm_client import LLMClient
    from .tools import (
        calcular_idade,
        calcular_imc,
        converter_temperatura,
        data_atual,
        detectar_funcao,
        gerar_senha,
    )
except ImportError:
    # quando executado como script direto (python projeto04/main.py)
    from llm_client import LLMClient
    from tools import (
        calcular_idade,
        calcular_imc,
        converter_temperatura,
        data_atual,
        detectar_funcao,
        gerar_senha,
    )

load_dotenv()

HERE = os.path.dirname(__file__)
HISTORY_FILE = os.path.join(HERE, "history.json")
MAX_HISTORY = 10

SYSTEM_PROMPT = (
    "Você é um assistente educado, objetivo e com um toque de leve humor. "
    "Sempre priorize respostas claras e breves. Quando o usuário pedir para executar "
    "uma função (por exemplo, calcular idade, converter temperatura, gerar senha ou calcular IMC), "
    "faça a execução usando as ferramentas disponíveis e retorne apenas o resultado."  # noqa: E501
)

client = None
try:
    client = LLMClient()
except Exception:
    # Degradado: sem cliente, só funções locais
    client = None


def carregar_historico() -> list:
    """Carrega histórico de mensagens do arquivo JSON ou inicia com prompt de sistema."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    # Garante que a primeira mensagem seja o system prompt
                    if data[0].get("role") != "system":
                        data.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
                    return trim_historico(data)
        except Exception:
            pass
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def salvar_historico(historico: list) -> None:
    """Salva o histórico em JSON legível."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Falha ao salvar histórico:", e)


def trim_historico(historico: list) -> list:
    """Limita o histórico às últimas MAX_HISTORY mensagens (além do system)."""
    if not historico:
        return []
    system_entry = historico[0] if historico[0].get("role") == "system" else None
    outras = historico[1:] if system_entry else historico
    if len(outras) <= MAX_HISTORY:
        return ([system_entry] if system_entry else []) + outras
    return ([system_entry] if system_entry else []) + outras[-MAX_HISTORY:]


def adicionar_mensagem(historico: list, role: str, content: str) -> list:
    historico.append({"role": role, "content": content})
    historico = trim_historico(historico)
    salvar_historico(historico)
    return historico


def executar_funcao(dados_funcao: tuple) -> str:
    """Executa a função detectada e retorna o resultado como string."""
    nome, kwargs = dados_funcao
    if nome == "calcular_idade":
        idade = calcular_idade(kwargs.get("data_nascimento", ""))
        return (
            f"Você tem {idade} anos." if idade is not None else "Não consegui extrair uma data válida."
        )
    if nome == "converter_temperatura":
        resultado = converter_temperatura(kwargs.get("texto", ""))
        return resultado or "Não consegui identificar a temperatura a ser convertida."
    if nome == "calcular_imc":
        return calcular_imc(kwargs.get("peso_kg", 0), kwargs.get("altura_m", 0))
    if nome == "gerar_senha":
        return gerar_senha(kwargs.get("tamanho", 12))
    return "Não conheço essa função."


def gerar_resposta_llm(historico: list) -> str:
    """Consulta a API do provedor configurado (OpenAI ou Groq)."""
    if client is None:
        return "Nenhuma chave de API disponível para gerar resposta."

    try:
        return client.generate_text(historico)
    except Exception as e:
        return f"Falha ao gerar resposta: {e}"


def interface_cli() -> None:
    historico = carregar_historico()
    print("=== Assistente com Memória (digite /sair para encerrar, /limpar para resetar) ===")

    while True:
        pergunta = input("Você: ").strip()
        if not pergunta:
            continue

        if pergunta.lower() in ["sair", "exit", "quit", "/sair"]:
            print("Encerrando o chat. Até mais!")
            break

        if pergunta.lower() == "/limpar":
            historico = [{"role": "system", "content": SYSTEM_PROMPT}]
            salvar_historico(historico)
            print("Assistente: Memória da conversa apagada.")
            continue

        if "data" in pergunta.lower():
            resposta = f"Hoje é {data_atual()}."
            historico = adicionar_mensagem(historico, "user", pergunta)
            historico = adicionar_mensagem(historico, "assistant", resposta)
            print("Assistente:", resposta)
            continue

        # Verifica se a pergunta aciona uma função Python
        func = detectar_funcao(pergunta)
        if func:
            resposta = executar_funcao(func)
            historico = adicionar_mensagem(historico, "user", pergunta)
            historico = adicionar_mensagem(historico, "assistant", resposta)
            print("Assistente:", resposta)
            continue

        historico = adicionar_mensagem(historico, "user", pergunta)
        resposta = gerar_resposta_llm(historico)
        historico = adicionar_mensagem(historico, "assistant", resposta)
        print("Assistente:", resposta)


if __name__ == "__main__":
    interface_cli()
