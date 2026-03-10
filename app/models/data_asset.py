from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DataAsset(Base):
    __tablename__ = "data_assets"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    asset_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_domains: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    quality_summary: Mapped[str] = mapped_column(Text, nullable=False)
    ops_summary: Mapped[str] = mapped_column(Text, nullable=False)
    marketing_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    knowledge_refs: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    lineage: Mapped[dict[str, list[str]]] = mapped_column(JSON, nullable=False, default=dict)
    training_value_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    api_export_ready: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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
