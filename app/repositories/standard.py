from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.standard import DishStandard
from app.schemas.standard import DishStandardCreate


class DishStandardRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[DishStandard]:
        result = self.session.execute(
            select(DishStandard).order_by(DishStandard.updated_at.desc())
        )
        return result.scalars().all()

    def get_by_dish_key(self, dish_key: str) -> DishStandard | None:
        result = self.session.execute(
            select(DishStandard).where(DishStandard.dish_key == dish_key)
        )
        return result.scalar_one_or_none()

    def create(self, payload: DishStandardCreate) -> DishStandard:
        standard = DishStandard(**payload.model_dump())
        self.session.add(standard)
        self.session.commit()
        self.session.refresh(standard)
        return standard
