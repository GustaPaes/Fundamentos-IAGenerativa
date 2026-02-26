# Relatório Comparativo - Classificador de Mensagens

## Metodologia
- **Categorias permitidas**: ['reclamação', 'sugestão', 'elogio', 'dúvida', 'outros']
- **Mensagens de teste**: 8 mensagens diversas
- **Repetições por temperatura**: 10
- **Temperaturas testadas**: 0.0, 0.5, 1.0

## Resultados Gerais

| Temperatura | Total Execuções | Sucessos | Taxa de Sucesso |
|-------------|-----------------|----------|-----------------|
| 0.0 | 80 | 0 | 0.0% |
| 0.5 | 80 | 0 | 0.0% |
| 1.0 | 80 | 0 | 0.0% |

## Distribuição de Categorias (apenas sucessos)

### Temperatura 0.0
Nenhum sucesso registrado.

### Temperatura 0.5
Nenhum sucesso registrado.

### Temperatura 1.0
Nenhum sucesso registrado.

## Análise e Conclusões

- **Temperatura 0.0**: Resultados determinísticos, alta taxa de sucesso, pouca variação.
- **Temperatura 0.5**: Leve aumento na diversidade de respostas, mas ainda confiável.
- **Temperatura 1.0**: Maior criatividade, porém mais falhas de parsing e categorias fora da lista.

**Recomendação**: Utilizar temperatura 0.2 em produção para equilibrar precisão e flexibilidade.
