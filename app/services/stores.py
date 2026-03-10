from app.repositories.store import StoreRepository
from app.schemas.store import StoreCreate, StoreRead


class StoreService:
    def __init__(self, repository: StoreRepository) -> None:
        self.repository = repository

    def list_stores(self) -> list[StoreRead]:
        return [StoreRead.model_validate(store) for store in self.repository.list_all()]

    def create_store(self, payload: StoreCreate) -> StoreRead:
        store = self.repository.create(payload)
        return StoreRead.model_validate(store)
