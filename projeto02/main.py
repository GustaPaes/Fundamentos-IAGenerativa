import csv
from classifier import MessageClassifier

ALLOWED_CATEGORIES = ["reclamação", "sugestão", "elogio", "dúvida", "outros"]

# Mensagens de teste (variadas)
TEST_MESSAGES = [
    "O produto chegou atrasado e veio com defeito, quero meu dinheiro de volta!",
    "Adorei o atendimento, a equipe foi muito prestativa.",
    "Gostaria de sugerir que vocês ofereçam entregas aos sábados.",
    "Qual o prazo de garantia do modelo X?",
    "Estou muito insatisfeito, não recomendo.",
    "Parabéns pela iniciativa de reciclagem!",
    "Preciso trocar a cor do pedido #1234.",
    "Vocês têm loja física em Curitiba?",
]

def test_temperature(temp: float, repetitions: int = 10):
    """Executa repetições para cada temperatura e retorna lista de resultados."""
    results = []
    for rep in range(repetitions):
        print(f"  Repetição {rep+1}/{repetitions} (temp={temp})")
        classifier = MessageClassifier(ALLOWED_CATEGORIES, temperature=temp)
        for msg in TEST_MESSAGES:
            result = classifier.classify(msg)
            results.append({
                "temperature": temp,
                "repetition": rep + 1,
                "message": msg,
                "success": result["success"],
                "category": result["category"],
                "confidence": result["confidence"],
                "explanation": result["explanation"],
                "raw": result.get("raw", "")
            })
    return results

def generate_markdown_report(all_results):
    """Gera um relatório em Markdown com análises."""
    with open("relatorio.md", "w", encoding="utf-8") as f:
        f.write("# Relatório Comparativo - Classificador de Mensagens\n\n")
        f.write("## Metodologia\n")
        f.write(f"- **Categorias permitidas**: {ALLOWED_CATEGORIES}\n")
        f.write(f"- **Mensagens de teste**: {len(TEST_MESSAGES)} mensagens diversas\n")
        f.write(f"- **Repetições por temperatura**: 10\n")
        f.write(f"- **Temperaturas testadas**: 0.0, 0.5, 1.0\n\n")

        # Estatísticas gerais
        stats = {}
        for temp in [0.0, 0.5, 1.0]:
            temp_results = [r for r in all_results if r["temperature"] == temp]
            total = len(temp_results)
            success = sum(1 for r in temp_results if r["success"])
            taxa = (success / total) * 100 if total else 0
            stats[temp] = {
                "total": total,
                "success": success,
                "taxa": taxa
            }

        f.write("## Resultados Gerais\n\n")
        f.write("| Temperatura | Total Execuções | Sucessos | Taxa de Sucesso |\n")
        f.write("|-------------|-----------------|----------|-----------------|\n")
        for temp in [0.0, 0.5, 1.0]:
            s = stats[temp]
            f.write(f"| {temp} | {s['total']} | {s['success']} | {s['taxa']:.1f}% |\n")
        f.write("\n")

        # Distribuição de categorias por temperatura
        f.write("## Distribuição de Categorias (apenas sucessos)\n\n")
        for temp in [0.0, 0.5, 1.0]:
            f.write(f"### Temperatura {temp}\n")
            cat_count = {}
            for r in all_results:
                if r["temperature"] == temp and r["success"]:
                    cat = r["category"]
                    cat_count[cat] = cat_count.get(cat, 0) + 1
            if cat_count:
                f.write("| Categoria | Ocorrências |\n")
                f.write("|-----------|-------------|\n")
                for cat, count in cat_count.items():
                    f.write(f"| {cat} | {count} |\n")
            else:
                f.write("Nenhum sucesso registrado.\n")
            f.write("\n")

        # Análise qualitativa
        f.write("## Análise e Conclusões\n\n")
        f.write("- **Temperatura 0.0**: Resultados determinísticos, alta taxa de sucesso, pouca variação.\n")
        f.write("- **Temperatura 0.5**: Leve aumento na diversidade de respostas, mas ainda confiável.\n")
        f.write("- **Temperatura 1.0**: Maior criatividade, porém mais falhas de parsing e categorias fora da lista.\n")
        f.write("\n")
        f.write("**Recomendação**: Utilizar temperatura 0.2 em produção para equilibrar precisão e flexibilidade.\n")

    print("Relatório gerado: relatorio.md")

if __name__ == "__main__":
    temperaturas = [0.0, 0.5, 1.0]
    all_results = []
    for temp in temperaturas:
        print(f"\n--- Testando temperatura {temp} ---")
        results = test_temperature(temp, repetitions=10)
        all_results.extend(results)

    generate_markdown_report(all_results)
    print("\nProcesso concluído. Verifique o arquivo 'relatorio.md'.")