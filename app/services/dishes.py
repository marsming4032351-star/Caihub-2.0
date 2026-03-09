from app.repositories.dish import DishRepository
from app.schemas.dish import DishCreate, DishRead


class DishService:
    def __init__(self, repository: DishRepository) -> None:
        self.repository = repository

    def list_dishes(self) -> list[DishRead]:
        return [
            DishRead.model_validate(dish)
            for dish in self.repository.list_all()
        ]

    def create_dish(self, payload: DishCreate) -> DishRead:
        dish = self.repository.create(payload)
        return DishRead.model_validate(dish)
