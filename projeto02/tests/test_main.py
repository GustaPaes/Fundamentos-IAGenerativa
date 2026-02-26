import os

import pytest

import main


def test_run_creates_report(tmp_path, monkeypatch):
    # Force a predictable result set by monkeypatching test_temperature
    sample = [
        {"temperature": 0.0, "success": True, "category": "a", "message": "msg1", "raw": "{\"category\":\"a\"}"},
        {"temperature": 0.5, "success": False, "category": "b", "message": "msg2", "raw": "invalid", "explanation": "Erro na API: quota", "api_error": True},
    ]

    def fake_test_temp(temp, repetitions=10):
        return sample

    monkeypatch.setattr(main, "test_temperature", fake_test_temp)

    # run in temporary directory
    orig = os.getcwd()
    os.chdir(tmp_path)
    try:
        main.run(repetitions_per_temp=1)
        # relatorio.md should exist and contain key headers and dynamic sections
        path = tmp_path / "relatorio.md"
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "# Relatório Comparativo" in text
        assert "Total Execuções" in text
        assert "Falhas" in text
        assert "Erros de API" in text
        assert "Exemplos de Falhas" in text
        assert "explicação" in text
        assert "Análise e Conclusões" in text
    finally:
        os.chdir(orig)
