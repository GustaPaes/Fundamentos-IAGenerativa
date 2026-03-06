# projeto04 - Assistente com Memória

Este projeto é um chatbot CLI que evolui um cliente de chat básico adicionando:

- Controle de memória (limpar histórico e limite de tamanho).
- Persona de assistente via mensagem de sistema.
- Integração de funções Python (idade, conversão de temperatura, IMC, gerar senha).
- Persistência de histórico em `history.json` para retomadas entre execuções.

## ✅ Como usar

1. Crie um arquivo `.env` na raiz do projeto (ou na raiz do repositório) com sua chave:

- Para usar **OpenAI**:

```text
OPENAI_API_KEY=sk-...
```

- Para usar **Groq**:

```text
GROQ_API_KEY=gsk-...
```

- (Opcional) Forçar provedor com `LLM_PROVIDER`:

```text
LLM_PROVIDER=groq  # ou openai
```

2. Instale dependências:

```bash
pip install -r projeto04/requirements.txt
```

3. Execute o chat:

```bash
python projeto04/main.py
```

4. Comandos especiais:

- `/limpar` - Apaga o histórico de conversa (mantém a persona do assistente).
- `/sair` - Encerra o programa.

## 🧠 Funcionalidades implementadas

- **Memória curada**: histórico limitado às últimas 10 mensagens para evitar gastar tokens e manter respostas relevantes.
- **Persistência**: histórico salvo em `projeto04/history.json` e restaurado ao reiniciar.
- **Persona definida**: sistema define comportamento do assistente para manter coerência de estilo.
- **Funções Python integradas**:
  - `calcular_idade` (usa data de nascimento em `YYYY-MM-DD` ou `DD/MM/YYYY`)
  - `converter_temperatura` (converte entre Celsius e Fahrenheit)
  - `calcular_imc` (recebe peso em kg e altura em m)
  - `gerar_senha` (gera senha aleatória com tamanho configurável)

## 🧪 Como testar as funcionalidades

- Pergunte: `Qual a temperatura de 20C em Fahrenheit?`
- Pergunte: `Qual a minha idade se nasci em 1990-01-01?`
- Pergunte: `Calcule meu IMC para 70kg e 1.75m.`
- Pergunte: `Gere uma senha de 16 caracteres.`

---

## Reflexões

- Um histórico muito grande aumenta o uso de **tokens**, tornando a chamada mais cara e mais lenta.
- Funções Python são melhores para cálculos determinísticos e dados sensíveis, pois não dependem da interpretação do modelo.
- O LLM pode interpretar incorretamente quando deve chamar uma função; isso pode levar a respostas erradas ou expor dados que não deveriam.
