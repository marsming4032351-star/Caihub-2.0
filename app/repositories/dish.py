from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dish import Dish
from app.schemas.dish import DishCreate


class DishRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Dish]:
        result = self.session.execute(select(Dish).order_by(Dish.created_at.desc()))
        return result.scalars().all()

    def create(self, payload: DishCreate) -> Dish:
        dish = Dish(**payload.model_dump())
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish
