from app.schemas.explanation import MovementInput
from app.services.explanation_service import (
    classify_movement,
    explain_movement,
    normalize_text,
)


def test_normalizes_accents_and_spaces():
    result = normalize_text("  CONCLUSOS   para DECISÃO! ")

    assert result == "conclusos para decisao"


def test_classifies_known_movement():
    result = classify_movement("Conclusos para decisão")

    assert result is not None
    assert result["name"] == "conclusos_decisao"


def test_classification_ignores_case_and_accents():
    result = classify_movement("CONCLUSOS PARA DECISAO")

    assert result is not None
    assert result["name"] == "conclusos_decisao"


def test_does_not_match_partial_word():
    result = classify_movement("O processo foi desintimado")

    assert result is None


def test_unknown_movement_returns_generic_explanation():
    movement = MovementInput(
        code="999",
        description="Movimentação não cadastrada no catálogo",
    )

    result = explain_movement(movement)

    assert "não consigo explicar" in result.explanation
    assert len(result.limitations) >= 2