import pytest

from classifier import MessageClassifier


class DummyLLM:
    def __init__(self, *args, **kwargs):
        pass

    def get_completion(self, prompt, max_tokens=150):
        # Always return a valid JSON matching one of the allowed categories
        return '{"category": "ELOGIO", "confidence": 0.8, "explanation": "teste"}'


def test_classify_success(monkeypatch):
    monkeypatch.setattr("classifier.LLMClient", DummyLLM)
    cl = MessageClassifier(["reclamação", "elogio"])
    res = cl.classify("qualquer coisa")
    assert res["success"] is True
    assert res["category"].lower() == "elogio"
    assert res["confidence"] == 0.8


def test_classify_invalid_json(monkeypatch):
    class BrokenLLM(DummyLLM):
        def get_completion(self, prompt, max_tokens=150):
            return "not a json"

    monkeypatch.setattr("classifier.LLMClient", BrokenLLM)
    cl = MessageClassifier(["reclamação", "elogio"])
    res = cl.classify("mensagem")
    assert res["success"] is False
    assert res.get("_fallback") is True
    assert res["category"] == "outros"


def test_classify_api_error(monkeypatch):
    class ErrorLLM(DummyLLM):
        def get_completion(self, prompt, max_tokens=150):
            raise Exception("token limit")

    monkeypatch.setattr("classifier.LLMClient", ErrorLLM)
    cl = MessageClassifier(["a"])
    res = cl.classify("mensagem")
    assert res["success"] is False
    assert res["category"] == "outros"
    assert "Erro na API" in res["explanation"]
    assert res.get("api_error") is True
