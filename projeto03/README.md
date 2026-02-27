# projeto03 - RAG com Proteções

Sistema de RAG (Retrieval-Augmented Generation) que combina uma base de
conhecimento simples com um LLM para responder perguntas. Desenvolvido como
projeto de portfólio para a disciplina de IA generativa.

## Características principais

- Suporta provedores OpenAI e Groq para geração de texto.
- Embeddings são usados para recuperar trechos relevantes; há fallback
  local baseado em hash de palavras quando não há chave/cota.
- Busca híbrida: vetorial + léxica, com limiar de similaridade ajustável e
  lógica especial para consultas que mencionam "email".
- Leitura automática de arquivos `.txt`, `.pdf` e `.docx` na pasta
  `conhecimento/`.
- Proteção contra prompt injection e validação/normalização de saída JSON.
- CLI simples que indica quando nenhum contexto foi encontrado.
- Utilitário de depuração (`debug_retriever.py`) para inspecionar o store e
  testar consultas manualmente.

## Uso

1. Copie um conjunto de documentos para `projeto03/conhecimento/` (pode
   ser texto puro, PDF ou DOCX).
2. Crie um `.env` com `OPENAI_API_KEY` ou `GROQ_API_KEY` (podem estar
   ausentes para testar o fallback local).
3. Instale dependências:

```sh
cd projeto03
pip install -r requirements.txt
```

4. Execute:

```sh
python main.py
```

Siga as instruções na tela para escolher o provedor e digitar perguntas.

## Desenvolvimento

- `retriever.py` contém a lógica de leitura, indexação e busca.
- `llm_client.py` abstrai o provedor e gerencia o fallback de embeddings.
- `validator.py` sanitiza o JSON de saída e bloqueia prompt injections.
- `prompt.py` constrói o sistema prompt rígido usado em todas as chamadas.

Teste o comportamento de recuperação com `python ../debug_retriever.py` na
raiz do repositório.

---

Este projeto serve como exemplo de implementação de RAG com atenção a
segurança e custos, apropriado para um portfólio público no GitHub.