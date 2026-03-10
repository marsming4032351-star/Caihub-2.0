from app.repositories.operator import OperatorRepository
from app.schemas.operator import OperatorCreate, OperatorRead


class OperatorService:
    def __init__(self, repository: OperatorRepository) -> None:
        self.repository = repository

    def list_operators(self) -> list[OperatorRead]:
        return [
            OperatorRead.model_validate(operator)
            for operator in self.repository.list_all()
        ]

    def create_operator(self, payload: OperatorCreate) -> OperatorRead:
        operator = self.repository.create(payload)
        return OperatorRead.model_validate(operator)
