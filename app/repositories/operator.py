from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.operator import Operator
from app.schemas.operator import OperatorCreate


class OperatorRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self) -> list[Operator]:
        result = self.session.execute(
            select(Operator).order_by(Operator.created_at.desc())
        )
        return result.scalars().all()

    def create(self, payload: OperatorCreate) -> Operator:
        operator = Operator(**payload.model_dump())
        self.session.add(operator)
        self.session.commit()
        self.session.refresh(operator)
        return operator
