import pytest

from validator import extract_json, validate_category, validate_classification, safe_fallback


def test_extract_json_plain():
    assert extract_json('{"category": "sugestão"}') == {"category": "sugestão"}


def test_extract_json_with_text():
    text = "Aqui está a resposta:\n```json\n{\"category\":\"elogio\"}\n```"
    assert extract_json(text) == {"category": "elogio"}


def test_extract_json_invalid():
    assert extract_json("não é um json") is None
    assert extract_json("{invalido:}") is None


def test_validate_category_case_insensitive():
    allowed = ["Reclamação", "Sugestão"]
    assert validate_category("reclamação", allowed)
    assert validate_category("Sugestão", allowed)
    assert not validate_category("elogio", allowed)


def test_validate_classification():
    allowed = ["a", "b"]
    assert validate_classification({"category": "a"}, allowed)
    assert not validate_classification({}, allowed)
    assert not validate_classification({"category": "c"}, allowed)
    assert not validate_classification("bad", allowed)


def test_safe_fallback_contains_keys():
    fb = safe_fallback("rawresponse", default_category="outros")
    assert fb["category"] == "outros"
    assert fb["confidence"] == 0.0
    assert fb["_error"] is True
    assert "rawresponse" in fb["_raw"]
