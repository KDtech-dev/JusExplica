from pydantic import BaseModel, ConfigDict, Field


class AIRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    texto: str = Field(min_length=1, max_length=10000)


class AIData(BaseModel):
    explanation: str


class AIResponse(BaseModel):
    success: bool = True
    data: AIData
