# Projetos de IA Generativa

Este repositório reúne três aplicações demonstrativas de inteligência
artificial generativa construídas como parte de desafios práticos. Cada
projeto é independente e pode ser executado isoladamente; todos usam a
mesma estrutura básica de cliente para LLMs e podem funcionar com a API
do OpenAI ou de outros provedores.

## 📁 Visão Geral dos Projetos

| Projeto     | Descrição rápida                                                 |
|-------------|------------------------------------------------------------------|
| **projeto01** | Cliente simples de chat com OpenAI; foco em aprendizado de integração e prompts.         |
| **projeto02** | Classificador de mensagens de clientes com robustez em produção (JSON, validação, fallback, relatórios). |
| **projeto03** | Sistema RAG (recuperação augmentada por geração) usando base de conhecimento; inclui proteção contra prompt injection e vetor store em memória. |

### projeto01 – Cliente de Chat
Um script mínimo que se conecta à API da OpenAI (`gpt-4o-mini` por
default), envia prompts e exibe respostas. Ideal para entender como
configurar o ambiente, definir mensagens de sistema/usuário e lidar com
parâmetros como temperatura e max tokens.

Arquivos principais:
- `main.py` – interface de linha de comando.
- `requirements.txt` – depende apenas de `openai` e `python-dotenv`.

### projeto02 – Classificador de Mensagens
Utiliza um LLM para categorizar mensagens de cliente em classes como
"reclamação", "elogio", etc. Contém validação robusta do JSON retornado
pelo modelo, proteção contra prompt injection e mecanismo de fallback
quando a API falha. Gera relatórios Markdown com estatísticas de
desempenho e inclui uma suite de testes (`pytest`).

Arquivos-chave:
- `classifier.py` – lógica de classificação e fallback.
- `validator.py` – parsing/validação de JSON e injeção de prompts.
- `main.py` – executa várias repetições e emite `relatorio.md`.
- `tests/` – casos de testes que não dependem da API.

### projeto03 – RAG com Proteções
Projeto mais completo do trio: um motor de _Retrieval-Augmented
Generation_ alimentado por uma base de conhecimento simples, com todas as
salvaguardas necessárias para uso em produção (pelo menos na versão de
prova de conceito).

O usuário digita uma pergunta e o programa tenta recuperar o trecho mais
relevante do conjunto de documentos dentro de `projeto03/conhecimento`.
Se não houver contexto adequado, o sistema deixa claro (`nenhum contexto`
no CLI) e o modelo responde apenas com o prompt de sistema. Para evitar
respostas fantasiosas, há uma dupla verificação:

- **Busca híbrida**: primeiro tentativa vetorial (embeddings); se a
	similaridade for baixa (< ~0.30) ou não houver palavras-chave em comum,
	fazemos uma segunda rodada léxica baseada em interseção de termos.
- **Tratamento especial de e‑mails**: consultas que mencionam “email”
	retornam diretamente o trecho contendo `@` ou a palavra `suporte`.

Além disso, o código prepara o modelo com um prompt de sistema estrito e
passa as respostas por `validator.py` para garantir que o LLM sempre retorne
JSON bem-formado e não seja induzido por _prompt injection_.

As embeddings são geradas via OpenAI/Groq quando disponíveis; na falta de
chave ou cota, o cliente automaticamente recorre a um vetor hash de 100
dimensões (sem dependências externas). Há também um pequeno utilitário
`debug_retriever.py` (na raiz do workspace) que imprime os chunks indexados
e mostra como a similaridade é calculada para facilitar ajustes.

Destaques:
- Vetorização local e fallback inteligente para continuar offline.
- Thresholds de similaridade calibrados para não responder a perguntas
	irrelevantes (“que dia é hoje” agora retorna vazio em vez de qualquer
	trecho).
- Lógica léxica complementar com exclusão de stopwords e detecção de e‑mail.
- Proteção robusta contra prompt injection e validação de saída JSON.
- Leitura automática de `.txt`, `.pdf` e `.docx` na pasta de conhecimento.


## 📂 Estrutura do Repositório

```
├── projeto01/          # Cliente de chat básico
│   ├── main.py         # Script principal
│   └── requirements.txt # Dependências
│
├── projeto02/          # Classificador de mensagens com validação
│   ├── main.py          # Classificador principal e geração de relatórios
│   ├── classifier.py    # Lógica de classificação com fallbacks
│   ├── llm_client.py    # Cliente LLM abstrato
│   ├── validator.py     # Validação, parser JSON e fallback seguro
│   ├── requirements.txt # Dependências (incluindo pytest)
│   ├── relatorio.md     # Relatório de análises gerado pelo script
│   └── tests/           # Suite de testes automatizados (pytest)
│
└── README.md          # Este arquivo
```

---

## 🚀 Como Começar

1. Clone ou acesse o repositório
2. Navegue até o projeto desejado
3. Instale as dependências: `pip install -r requirements.txt`
4. Configure sua chave de API OpenAI em um arquivo `.env`
5. Execute: `python main.py`

---

## 🔧 Requisitos

- Python 3.8+
- Chave de API OpenAI
- Dependências listadas em `requirements.txt`

---

## 📝 Notas Importantes

- O repositório contém três projetos independentes, cada um com um foco diferente (chat, classificação e RAG).
- Os componentes incluem validação de JSON, proteção contra prompt injection e fallback seguro para APIs.
- Todos os scripts suportam execução em modo de teste sem depender da API real, útil para desenvolver offline.
- Se não houver chave OpenAI ou a cota estiver esgotada, o `projeto03` utiliza embeddings locais para continuar operando.
- Os projetos podem ser usados como base para experimentos pessoais e portfólio público.
- O cliente LLM usa `max_retries=0` para falhar rapidamente em caso de erros de quota, evitando longos bloqueios.

