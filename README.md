# IA Generativa

**Prof. Sabrina Bet**

Disciplina eletiva focada em conceitos e aplicações práticas de Inteligência Artificial Generativa, explorando desde integração com APIs LLM até produção de sistemas robustos.

---

## 📚 Aulas

### Aula 01 - Introdução à IA Generativa com OpenAI

**Objetivo**: Entender os fundamentos de IA Generativa e integração com APIs

**Conteúdo**:
- Conceitos fundamentais de modelos de linguagem
- Integração com OpenAI API
- Prompts efetivos
- Controle de temperatura e parâmetros
- Análise de riscos e arquitetura

**Projeto Prático** (`projeto01/`):
- Cliente OpenAI integrado
- Prompts estruturados para diferentes contextos
- Teste com modelo GPT-4o-mini

📊 [Acessar Slides](https://eletiva-aula01.lovable.app/)

---

### Aula 02 - Produção Ready: Validação e Robustez

**Objetivo**: Transformar protótipos em soluções confiáveis para produção

**Conteúdo**:
- Criação de classificadores com IA
- Validação de dados e formato JSON
- Tratamento de erros e exceções
- Testes com múltiplas execuções e temperaturas
- Implementação em ambiente de produção

**Projeto Prático** (`projeto02/`):
- Classificador de mensagens de cliente com fallback seguro
- Validação e extração JSON via `validator.py`
- Lista de categorias permitidas e confidência de classificação
- Mecanismo de testes automatizados (pytest) com múltiplas execuções e temperaturas
- Geração de relatório Markdown comparativo

📊 [Acessar Slides](https://eletiva-aula02.lovable.app)

---

## 📂 Estrutura do Repositório

```
├── projeto01/          # Aula 01 - Fundamentos
│   ├── main.py         # Script principal
│   └── requirements.txt # Dependências
│
├── projeto02/          # Aula 02 - Produção
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

- Cada aula constrói sobre conceitos da aula anterior
- Projeto 02 foca em padrões de produção (validação, fallback, testes)
- Os scripts suportam execução em modo de teste sem depender da API real
- Se não houver chave OpenAI, se as respostas não retornarem JSON válidos ou se a cota estiver esgotada, o relatório mostrará 0% de sucesso e exemplos de falhas (com explicações de erro)
- Todos os scripts opcionais podem utilizar uma chave de API OpenAI se disponível
- O cliente é configurado com `max_retries=0` para falhar rapidamente em caso de erros de quota, evitando longos bloqueios

