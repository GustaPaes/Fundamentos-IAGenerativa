
# DESAFIO AULA 02 - Produção Ready

> Transforme o classificador em algo que você confiaria para um ambiente de produção!

---

## O que deve ser feito

- [ ] **Criar parser JSON** → Garantir que o formato retornado está correto
- [ ] **Tratar erro de JSON inválido** → Capturar e processar exceções
- [ ] **Criar validação contra lista permitida** → Garantir que não seja inventada uma categoria
- [ ] **Fallback seguro** → Criar um mecanismo de tratamento para quando o modelo falhar

## Testes

- [ ] **Múltiplas execuções**: 10 repetições do mesmo teste
- [ ] **Diferentes temperaturas**: Testar com 3 valores diferentes de temperatura

## Entrega

- [ ] **Relatório comparativo** → Documento (PDF/DOC) ou Markdown com análise dos testes
- [ ] **Código fonte** → Link para repositório GitHub

---

## Dicas

- Implementar as funções no `validator.py`
- Cada tarefa deve ser uma função diferente
- Considere tratamento robusto de exceções

---

## Upgrade do Classificador (Opcional)

- [ ] Adicionar score de confiança
- [ ] Criar log estruturado
- [ ] Medir distribuição de resultados
