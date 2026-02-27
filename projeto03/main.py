import os

from llm_client import LLMClient
from retriever import load_conhecimento, build_vector_store, simple_retriever
from validator import validate_json, detect_prompt_injection
from prompt import build_system_prompt

def main():
    while True:
        provider = input("Escolha o provedor (openai/groq): ").strip().lower()
        try:
            client = LLMClient(provider=provider)
            break
        except ValueError as e:
            print(f"Erro: {e}. Digite 'openai' ou 'groq'.")

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
        # If no context recovered, call the model with empty context
        # determine if this is a contact query
        query_lower = query.lower()
        contact_query = any(k in query_lower for k in ("email", "e-mail", "contato", "suporte", "telefone"))

        # if user asked for contact info but retriever didn't return a contact
        # chunk, try a lexicographic pass across the whole store to find it
        if contact_query and contexto:
            # if contexto doesn't contain an email/phone, try to find one in store
            import re
            if not (re.search(r"[\w\.-]+@[\w\.-]+", contexto) or re.search(r"\(\d{2}\)\s*\d{4,5}-\d{4}", contexto)):
                from retriever import find_contact_chunk
                found = find_contact_chunk(vector_store)
                if found:
                    contexto = found

        standardized = False
        if not contexto:
            print("(nenhum contexto recuperado; respondendo com modelo puro)")
            system_prompt = build_system_prompt()
            response_text = client.generate_text(system_prompt, contexto)
        else:
            # Only produce a deterministic, standardized contact reply when the
            # user query explicitly asks for contact info (email/telefone/contato).
            import re
            query_lower = query.lower()
            contact_query = any(k in query_lower for k in ("email", "e-mail", "contato", "suporte", "telefone"))

            def extract_contact(text: str):
                email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
                phone_match = re.search(r"\(\d{2}\)\s*\d{4,5}-\d{4}", text)
                hours_match = re.search(r"segunda a sexta-feira[^,\.]*|de segunda a sexta[^,\.]*", text, re.IGNORECASE)
                return email_match.group(0) if email_match else None, phone_match.group(0) if phone_match else None, (hours_match.group(0).strip() if hours_match else None)

            if contact_query:
                email, phone, hours = extract_contact(contexto)
                if email or phone:
                    parts = []
                    if email:
                        parts.append(f"e-mail: {email}")
                    if phone:
                        parts.append(f"telefone: {phone}")
                    if hours:
                        parts.append(f"horário: {hours}")
                    response_text = "Você pode entrar em contato conosco por " + " ou ".join(parts) + "."
                    standardized = True
                else:
                    # contact query but no explicit contact in retrieved context: fall back to model
                    system_prompt = build_system_prompt()
                    response_text = client.generate_text(system_prompt, contexto)
            else:
                # non-contact query with context: send context to model
                system_prompt = build_system_prompt()
                response_text = client.generate_text(system_prompt, contexto)
        # If we produced a standardized response (contact), print it directly
        if standardized:
            print(f"Resposta: {response_text}")
            continue

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
