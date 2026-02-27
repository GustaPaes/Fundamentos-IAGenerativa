import os

from llm_client import LLMClient
from retriever import load_conhecimento, build_vector_store, simple_retriever
from validator import validate_json, detect_prompt_injection
from prompt import build_system_prompt

def main():
    provider = input("Escolha o provedor (openai/groq): ").strip().lower()
    client = LLMClient(provider=provider)

    conhecimento_text = load_conhecimento()
    try:
        vector_store = build_vector_store(conhecimento_text, client)
        if vector_store:
            print(f"✓ Base de conhecimento carregada ({len(vector_store)} trechos indexados)")
        else:
            print("⚠ Nenhum trecho foi indexado; usando embeddings locais...")
    except NotImplementedError as e:
        print(f"Não foi possível construir o vetor store: {e}")
        vector_store = []

    while True:
        query = input("Digite sua pergunta (ou 'sair' para encerrar): ").strip()
        if query.lower() == "sair":
            break

        # proteção contra prompt injection na entrada do usuário
        if detect_prompt_injection(query):
            print("Erro: tentativa de prompt injection detectada.")
            continue

        contexto = simple_retriever(query, vector_store, client)
        if not contexto:
            print("(nenhum contexto recuperado; respondendo com modelo puro)")
        system_prompt = build_system_prompt()
        response_text = client.generate_text(system_prompt, contexto)
        try:
            is_valid, data = validate_json(response_text)
            if is_valid and data.get("status") == "sucesso":
                print(f"Resposta: {data.get('resposta', 'Sem resposta disponível')}")
            else:
                # status é "não encontrado" ou outro
                print(f"Resposta: {data.get('resposta', data.get('status', 'Sem informações'))}")
        except ValueError as e:
            print(f"[Erro ao processar resposta: {e}]")

if __name__ == "__main__":
    main()
