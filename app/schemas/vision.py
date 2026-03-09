from pydantic import BaseModel, Field


class VisionCandidate(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class VisionFeatures(BaseModel):
    brightness: float = Field(ge=0.0, le=1.0)
    edge_density: float = Field(ge=0.0, le=1.0)
    circularity: float = Field(ge=0.0)
    green_ratio: float = Field(ge=0.0, le=1.0)
    warm_ratio: float = Field(ge=0.0, le=1.0)


class DishRecognitionRequest(BaseModel):
    image_base64: str = Field(min_length=16)


class DishRecognitionResponse(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    candidates: list[VisionCandidate]
    features: VisionFeatures
