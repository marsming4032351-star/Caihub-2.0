from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StoreOperationSnapshot(Base):
    __tablename__ = "store_operation_snapshots"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    store_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    shift: Mapped[str] = mapped_column(String(64), nullable=False)
    operator_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quality_alert_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sop_risk_items: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    temperature_status: Mapped[str] = mapped_column(String(32), nullable=False)
    throughput_score: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
