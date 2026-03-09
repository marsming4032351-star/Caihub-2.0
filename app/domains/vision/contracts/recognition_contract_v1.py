from pydantic import BaseModel, Field


class RecognitionCandidateContractV1(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class DishRecognitionContractV1(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str = Field(default="opencv-heuristic-v1")
    candidates: list[RecognitionCandidateContractV1] = Field(default_factory=list)
