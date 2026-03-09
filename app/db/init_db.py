from app.db.model_registry import target_metadata
from app.db.session import get_engine


def initialize_database() -> None:
    engine = get_engine()
    target_metadata.create_all(bind=engine)
