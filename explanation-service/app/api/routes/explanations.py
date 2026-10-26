from fastapi import APIRouter

from app.schemas.explanation import (
    ExplanationRequest,
    ExplanationResponse,
)
from app.services.explanation_service import explain_movement


router = APIRouter(
    prefix="/explanations",
    tags=["Explanations"],
)


@router.post("", response_model=ExplanationResponse)
def create_explanation(
    request: ExplanationRequest,
) -> ExplanationResponse:
    result = explain_movement(request.movement)

    return ExplanationResponse(
        success=True,
        data=result,
    )