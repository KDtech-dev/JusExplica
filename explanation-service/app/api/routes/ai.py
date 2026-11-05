from fastapi import APIRouter, HTTPException

from app.schemas.ai import AIData, AIRequest, AIResponse
from app.services.ai_connection import (
    AIConfigurationError,
    AIUnavailableError,
    explicar_texto,
)


router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("", response_model=AIResponse)
def create_ai_explanation(request: AIRequest) -> AIResponse:
    try:
        explanation = explicar_texto(request.texto)
    except AIConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail="O serviço de IA não está configurado.",
        ) from exc
    except AIUnavailableError as exc:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível gerar o texto. Tente novamente mais tarde.",
        ) from exc

    return AIResponse(data=AIData(explanation=explanation))
