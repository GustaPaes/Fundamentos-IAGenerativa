# Relatório Comparativo - Classificador de Mensagens

## Metodologia
- **Categorias permitidas**: ['reclamação', 'sugestão', 'elogio', 'dúvida', 'outros']
- **Mensagens de teste**: 8 mensagens diversas
- **Repetições por temperatura**: 10
- **Temperaturas testadas**: 0.0, 0.5, 1.0

## Resultados Gerais

| Temperatura | Total Execuções | Sucessos | Falhas | Erros de API | Taxa de Sucesso |
|-------------|-----------------|----------|--------|--------------|-----------------|
| 0.0 | 80 | 0 | 80 | 80 | 0.0% |
| 0.5 | 80 | 0 | 80 | 80 | 0.0% |
| 1.0 | 80 | 0 | 80 | 80 | 0.0% |

## Distribuição de Categorias (apenas sucessos)

### Temperatura 0.0
Nenhum sucesso registrado.

### Temperatura 0.5
Nenhum sucesso registrado.

### Temperatura 1.0
Nenhum sucesso registrado.

## Exemplos de Falhas

### Temperatura 0.0
- Mensagem: O produto chegou atrasado e veio com defeito, quero meu dinheiro de volta!
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Adorei o atendimento, a equipe foi muito prestativa.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Gostaria de sugerir que vocês ofereçam entregas aos sábados.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

### Temperatura 0.5
- Mensagem: O produto chegou atrasado e veio com defeito, quero meu dinheiro de volta!
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Adorei o atendimento, a equipe foi muito prestativa.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Gostaria de sugerir que vocês ofereçam entregas aos sábados.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

### Temperatura 1.0
- Mensagem: O produto chegou atrasado e veio com defeito, quero meu dinheiro de volta!
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Adorei o atendimento, a equipe foi muito prestativa.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}
- Mensagem: Gostaria de sugerir que vocês ofereçam entregas aos sábados.
  - resposta bruta: None
  - explicação: Erro na API: Erro na API: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}

## Análise e Conclusões

- Temperatura 0.0: nenhuma execução conseguiu retornar um JSON válido. Verifique chave de API ou formatação das respostas.
- Temperatura 0.5: nenhuma execução conseguiu retornar um JSON válido. Verifique chave de API ou formatação das respostas.
- Temperatura 1.0: nenhuma execução conseguiu retornar um JSON válido. Verifique chave de API ou formatação das respostas.

**Recomendações**:
- Certifique-se de fornecer uma chave OpenAI válida no ambiente.
- Ajuste a temperatura para balancear precisão (0.0–0.2 recomendado) ou aumentar criatividade conscientemente.
- Analise as falhas acima para identificar padrões de saída inválida.
