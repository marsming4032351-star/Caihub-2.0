from app.events.base import DomainEvent
from app.events.quality import quality_decision_event
from app.models.production_event import ProductionEvent
from app.repositories.production_event import ProductionEventRepository
from app.schemas.production import (
    ProductionEventCreate,
    ProductionEventRead,
    ProductionFeedback,
)
from app.services.quality import QualityRuleService
from app.services.standards import DishStandardService


class ProductionEventService:
    def __init__(
        self,
        repository: ProductionEventRepository,
        quality_service: QualityRuleService,
        standard_service: DishStandardService,
    ) -> None:
        self.repository = repository
        self.quality_service = quality_service
        self.standard_service = standard_service

    def list_events(self) -> list[ProductionEventRead]:
        return [self._to_read_model(event) for event in self.repository.list_all()]

    def create_event(self, payload: ProductionEventCreate) -> tuple[ProductionEventRead, DomainEvent]:
        standard = self.standard_service.get_standard_by_dish_key(payload.dish_id)
        if standard is None:
            standard = self.quality_service.default_standard(payload.dish_id)
        quality_result = self.quality_service.evaluate(
            capture=payload.capture,
            recognition=payload.recognition,
            standard=standard,
        )
        event = ProductionEvent(
            store_id=payload.store_id,
            store_code=payload.store_code,
            dish_id=payload.dish_id,
            operator_id=payload.operator_id,
            operator_code=payload.operator_code,
            image_url=payload.capture.image_url,
            lighting_profile=payload.capture.lighting_profile,
            camera_profile=payload.capture.camera_profile,
            temperature_celsius=payload.capture.temperature_celsius,
            weight_grams=payload.capture.weight_grams,
            standard_dish_key=quality_result.standard_dish_key,
            model_version=quality_result.model_version,
            top_label=quality_result.top_label,
            confidence=quality_result.confidence,
            plating_score=quality_result.plating_score,
            color_score=quality_result.color_score,
            deviation_score=quality_result.deviation_score,
            pass_decision=quality_result.pass_decision,
            feedback=payload.feedback.model_dump(),
        )
        created = self.repository.create(event)
        decision_event = quality_decision_event(
            event_id=str(created.id),
            dish_id=created.dish_id,
            passed=created.pass_decision,
        )
        return self._to_read_model(created), decision_event

    @staticmethod
    def _to_read_model(event: ProductionEvent) -> ProductionEventRead:
        return ProductionEventRead(
            id=event.id,
            store_id=event.store_id,
            store_code=event.store_code or event.store_id,
            dish_id=event.dish_id,
            operator_id=event.operator_id,
            operator_code=event.operator_code or event.operator_id,
            capture={
                "image_url": event.image_url,
                "lighting_profile": event.lighting_profile,
                "camera_profile": event.camera_profile,
                "temperature_celsius": event.temperature_celsius,
                "weight_grams": event.weight_grams,
            },
            quality_result={
                "standard_dish_key": event.standard_dish_key,
                "model_version": event.model_version,
                "top_label": event.top_label,
                "confidence": event.confidence,
                "plating_score": event.plating_score,
                "color_score": event.color_score,
                "deviation_score": event.deviation_score,
                "pass_decision": event.pass_decision,
            },
            feedback=ProductionFeedback.model_validate(event.feedback),
            created_at=event.created_at,
        )
