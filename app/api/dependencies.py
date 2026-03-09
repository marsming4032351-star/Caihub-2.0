from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_session_factory
from app.repositories.dish import DishRepository
from app.repositories.production_event import ProductionEventRepository
from app.repositories.standard import DishStandardRepository
from app.services.architecture import ArchitectureService
from app.services.dishes import DishService
from app.services.production import ProductionEventService
from app.services.quality import QualityRuleService
from app.services.standards import DishStandardService
from app.services.system import SystemService


def get_db_session() -> Generator[Session, None, None]:
    session_factory = get_session_factory()
    with session_factory() as session:
        yield session


def get_dish_repository(
    session: Session = Depends(get_db_session),
) -> DishRepository:
    return DishRepository(session)


def get_dish_service(
    repository: DishRepository = Depends(get_dish_repository),
) -> DishService:
    return DishService(repository)


def get_production_event_repository(
    session: Session = Depends(get_db_session),
) -> ProductionEventRepository:
    return ProductionEventRepository(session)


def get_quality_rule_service() -> QualityRuleService:
    return QualityRuleService()


def get_dish_standard_repository(
    session: Session = Depends(get_db_session),
) -> DishStandardRepository:
    return DishStandardRepository(session)


def get_dish_standard_service(
    repository: DishStandardRepository = Depends(get_dish_standard_repository),
) -> DishStandardService:
    return DishStandardService(repository)


def get_production_event_service(
    repository: ProductionEventRepository = Depends(get_production_event_repository),
    quality_service: QualityRuleService = Depends(get_quality_rule_service),
    standard_service: DishStandardService = Depends(get_dish_standard_service),
) -> ProductionEventService:
    return ProductionEventService(repository, quality_service, standard_service)


def get_system_service() -> SystemService:
    return SystemService(get_settings())


def get_architecture_service() -> ArchitectureService:
    return ArchitectureService()
