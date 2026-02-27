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
Construção mais avançada que combina embeddings e busca por similaridade
enquanto protege contra tentativas de instruir o modelo com prompts
maliciosos. Suporta múltiplos provedores (OpenAI ou Groq), embeddings
locais quando a cota OpenAI não está disponível, e leitura de arquivos
TXT/PDF/DOCX na pasta `conhecimento/`.

Destaques:
- Vetorização local (hash de palavras) para operação offline.
- Recuperação híbrida (vetorial + léxica) para maior precisão.
- Prompt de sistema rigoroso e validação JSON melhorada.
- Estrutura de leitura multi-formato em `retriever.py`.


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

