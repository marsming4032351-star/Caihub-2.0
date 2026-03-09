from fastapi import APIRouter, Depends

from app.schemas.vision import DishRecognitionRequest, DishRecognitionResponse
from app.vision.recognizer import DishRecognizer, get_dish_recognizer

router = APIRouter()


@router.post(
    "/dish-recognition",
    response_model=DishRecognitionResponse,
    summary="Recognize a dish from an image",
)
def recognize_dish(
    payload: DishRecognitionRequest,
    recognizer: DishRecognizer = Depends(get_dish_recognizer),
) -> DishRecognitionResponse:
    return recognizer.recognize(payload.image_base64)
