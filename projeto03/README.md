# projeto03 — RAG com Proteções (Prática / Portfólio)

Sistema RAG (Retrieval‑Augmented Generation) focado em segurança, robustez
e documentação para uso em portfólio. O objetivo é demonstrar integração
com LLMs, estratégias de fallback e salvaguardas contra prompt injection.

**Principais recursos**

- Suporte a provedores `OpenAI` e `Groq` para geração e (quando possível)
  geração de embeddings.
- **Fallback local de embeddings**: quando não houver chave/cota, o
  cliente gera um embedding simples (hash 100‑dim) permitindo operação
  offline ou em ambientes de teste.
- **Busca híbrida (vetorial + léxica)** com threshold de similaridade
  conservador (~0.30) para evitar matches irrelevantes; a busca léxica é
  utilizada como complemento.
- **Detecção e bloqueio de prompt injection**: entradas maliciosas são
  identificadas por `validator.py` e não são encaminhadas ao LLM.
- **Padronização condicional de contato**: quando a consulta pede
  explicitamente `email`/`telefone` e o trecho recuperado contém contato,
  o CLI retorna uma resposta padronizada e determinística; em outros
  casos o modelo recebe o contexto normalmente.
- **Leitura multi‑formato**: `.txt`, `.pdf`, `.docx` em
  `projeto03/conhecimento/`.
- **Utilitários**: `debug_retriever.py`, `projeto03/test_flow.py` e
  `test_main_contact.py` para validar e depurar o retriever/fallback.

## Instalação Rápida

```bash
cd projeto03
pip install -r requirements.txt
# opcional: crie um .env com OPENAI_API_KEY ou GROQ_API_KEY
```

## Como usar

1. Coloque documentos em `projeto03/conhecimento/` (p.ex. `conhecimento.txt`).
2. Rode `python main.py` e escolha o provedor (`openai`/`groq`).
3. Digite perguntas — exemplos:

- `qual email de suporte` → tentará recuperar o trecho com contato e,
  caso exista, retornará resposta padronizada.
- `que dia é hoje` → se não houver contexto aplicável, o CLI indicará
  isso e o modelo responderá sem contexto.

## Arquitetura (arquivos principais)

- `retriever.py` — leitura de arquivos, chunking, cálculo de embeddings e
  busca híbrida.
- `llm_client.py` — adaptador para provedores + fallback de embeddings
  locais.
- `validator.py` — detecção de prompt injection e validação/normalização
  do JSON de saída.
- `prompt.py` — constrói o prompt de sistema seguro usado nas chamadas.
- `main.py` — CLI que junta tudo, aplica regras de segurança e exibe
  respostas ao usuário.

## Testes & Debug

- `python debug_retriever.py` (na raiz) — imprime chunks e similaridades
  para consultas de exemplo.
- `python projeto03/test_flow.py` — simula fluxo com uma consulta de
  prompt injection e uma de contato.
- `python test_main_contact.py` — teste rápido para validação de extração
  de contato (executar do workspace root).

## Boas práticas e notas para recrutadores

- Projeto pensado para demonstrar decisões de engenharia: limites de
  confiança, fallbacks e proteção contra abusos de LLM.
- Código organizado, fácil de estender para suportar indexadores reais
  (FAISS, Weaviate) ou embeddings de alta qualidade.
- Fácil de rodar localmente em máquinas com ou sem chave de API — útil
  para entrevistas técnicas e avaliações de arquitetura.

---

Se quiser que eu gere um `CONTRIBUTING.md`, um badge de status simples ou
um `requirements.txt` enxuto para CI, eu posso adicionar em seguida.