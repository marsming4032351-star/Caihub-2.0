from app.models.standard import DishStandard
from app.repositories.standard import DishStandardRepository
from app.schemas.standard import DishStandardCreate, DishStandardRead


class DishStandardService:
    def __init__(self, repository: DishStandardRepository) -> None:
        self.repository = repository

    def list_standards(self) -> list[DishStandardRead]:
        return [
            DishStandardRead.model_validate(standard)
            for standard in self.repository.list_all()
        ]

    def create_standard(self, payload: DishStandardCreate) -> DishStandardRead:
        standard = self.repository.create(payload)
        return DishStandardRead.model_validate(standard)

    def get_standard_by_dish_key(self, dish_key: str) -> DishStandard | None:
        return self.repository.get_by_dish_key(dish_key)
