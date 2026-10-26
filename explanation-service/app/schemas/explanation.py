from datetime import date as Date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MovementInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    code: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=2000)
    date: Optional[Date] = None

    @field_validator("code", "description")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O campo não pode conter apenas espaços.")
        return value


class ExplanationRequest(BaseModel):
    movement: MovementInput
    language: str = Field(default="pt-BR", min_length=2, max_length=10)


class ExplanationData(BaseModel):
    explanation: str
    limitations: list[str] = Field(default_factory=list)


class ExplanationResponse(BaseModel):
    success: bool = True
    data: ExplanationData