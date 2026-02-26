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
                "raw": result.get("raw", ""),
                "api_error": result.get("api_error", False)
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
            api_err = sum(1 for r in temp_results if r.get("api_error"))
            taxa = (success / total) * 100 if total else 0
            stats[temp] = {
                "total": total,
                "success": success,
                "api_errors": api_err,
                "taxa": taxa
            }

        f.write("## Resultados Gerais\n\n")
        f.write("| Temperatura | Total Execuções | Sucessos | Falhas | Erros de API | Taxa de Sucesso |\n")
        f.write("|-------------|-----------------|----------|--------|--------------|-----------------|\n")
        for temp in [0.0, 0.5, 1.0]:
            s = stats[temp]
            failures = s['total'] - s['success']
            f.write(f"| {temp} | {s['total']} | {s['success']} | {failures} | {s['api_errors']} | {s['taxa']:.1f}% |\n")
        f.write("\n")

        # Distribuição de categorias por temperatura (apenas sucessos)
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
        # Amostra de falhas para diagnóstico
        f.write("## Exemplos de Falhas\n\n")
        # collect first few raw outputs per temperature
        for temp in [0.0, 0.5, 1.0]:
            f.write(f"### Temperatura {temp}\n")
            shown = 0
            for r in all_results:
                if r["temperature"] == temp and not r["success"]:
                    f.write(f"- Mensagem: {r.get('message','<não disponível>')}\n")
                    raw_text = str(r.get('raw',''))
                    f.write(f"  - resposta bruta: {raw_text[:200].replace('\\n',' ')}\n")
                    if r.get('explanation'):
                        f.write(f"  - explicação: {r['explanation']}\n")
                    shown += 1
                    if shown >= 3:
                        break
            if shown == 0:
                f.write("Nenhuma falha registrada.\n")
            f.write("\n")

        # Análise qualitativa
        # Análise qualitativa e conclusões dinâmicas
        f.write("## Análise e Conclusões\n\n")
        for temp in [0.0, 0.5, 1.0]:
            s = stats[temp]
            if s['total'] == 0:
                continue
            if s['success'] == 0:
                f.write(f"- Temperatura {temp}: nenhuma execução conseguiu retornar um JSON válido. "
                        "Verifique chave de API ou formatação das respostas.\n")
            else:
                taxa = s['taxa']
                f.write(f"- Temperatura {temp}: {s['success']}/{s['total']} classificações válidas ({taxa:.1f}% de sucesso).\n")
        f.write("\n")
        f.write("**Recomendações**:\n")
        f.write("- Certifique-se de fornecer uma chave OpenAI válida no ambiente.\n")
        f.write("- Ajuste a temperatura para balancear precisão (0.0–0.2 recomendado) ou aumentar criatividade conscientemente.\n")
        f.write("- Analise as falhas acima para identificar padrões de saída inválida.\n")

    print("Relatório gerado: relatorio.md")

def run(repetitions_per_temp: int = 10):
    """Executa o conjunto completo de testes e gera o relatório.

    Chamável a partir de outros módulos ou de testes para evitar
    dependência da API real de LLM.
    """
    temperaturas = [0.0, 0.5, 1.0]
    all_results = []
    for temp in temperaturas:
        print(f"\n--- Testando temperatura {temp} ---")
        results = test_temperature(temp, repetitions=repetitions_per_temp)
        all_results.extend(results)

    generate_markdown_report(all_results)
    print("\nProcesso concluído. Verifique o arquivo 'relatorio.md'.")


if __name__ == "__main__":
    run()