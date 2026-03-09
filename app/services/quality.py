from dataclasses import dataclass

from app.models.standard import DishStandard
from app.schemas.production import (
    ProductionCaptureInput,
    ProductionQualityResult,
    ProductionRecognitionInput,
)


@dataclass(frozen=True)
class StandardSnapshot:
    dish_key: str
    target_weight_grams: float
    weight_tolerance_grams: float
    target_temperature_celsius: float
    temperature_tolerance_celsius: float
    minimum_confidence: float
    maximum_deviation_score: float


class QualityRuleService:
    def default_standard(self, dish_key: str) -> StandardSnapshot:
        return StandardSnapshot(
            dish_key=dish_key,
            target_weight_grams=350.0,
            weight_tolerance_grams=60.0,
            target_temperature_celsius=65.0,
            temperature_tolerance_celsius=12.0,
            minimum_confidence=0.75,
            maximum_deviation_score=0.35,
        )

    def evaluate(
        self,
        capture: ProductionCaptureInput,
        recognition: ProductionRecognitionInput,
        standard: DishStandard | StandardSnapshot,
    ) -> ProductionQualityResult:
        confidence = recognition.confidence
        temperature_score = 1.0
        if capture.temperature_celsius is not None:
            temperature_delta = abs(
                capture.temperature_celsius - standard.target_temperature_celsius
            )
            divisor = max(standard.temperature_tolerance_celsius * 2, 1.0)
            temperature_score = max(0.0, 1.0 - temperature_delta / divisor)

        weight_score = 1.0
        if capture.weight_grams is not None:
            weight_delta = abs(capture.weight_grams - standard.target_weight_grams)
            divisor = max(standard.weight_tolerance_grams * 2, 1.0)
            weight_score = max(0.0, 1.0 - weight_delta / divisor)

        plating_score = round((confidence * 0.7 + weight_score * 0.3), 4)
        color_score = round((confidence * 0.6 + temperature_score * 0.4), 4)
        deviation_score = round(
            max(0.0, 1.0 - ((plating_score + color_score) / 2.0)),
            4,
        )
        pass_decision = (
            confidence >= standard.minimum_confidence
            and deviation_score <= standard.maximum_deviation_score
        )

        return ProductionQualityResult(
            standard_dish_key=standard.dish_key,
            model_version=recognition.model_version,
            top_label=recognition.top_label,
            confidence=confidence,
            plating_score=plating_score,
            color_score=color_score,
            deviation_score=deviation_score,
            pass_decision=pass_decision,
        )
