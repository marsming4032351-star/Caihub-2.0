"""initial schema

Revision ID: 20260309_0001
Revises:
Create Date: 2026-03-09 00:00:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260309_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dishes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dishes_name"), "dishes", ["name"], unique=False)

    op.create_table(
        "dish_standards",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dish_key", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_weight_grams", sa.Float(), nullable=False),
        sa.Column("weight_tolerance_grams", sa.Float(), nullable=False),
        sa.Column("target_temperature_celsius", sa.Float(), nullable=False),
        sa.Column("temperature_tolerance_celsius", sa.Float(), nullable=False),
        sa.Column("minimum_confidence", sa.Float(), nullable=False),
        sa.Column("maximum_deviation_score", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dish_standards_dish_key"),
        "dish_standards",
        ["dish_key"],
        unique=True,
    )

    op.create_table(
        "production_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("store_id", sa.String(length=64), nullable=False),
        sa.Column("dish_id", sa.String(length=64), nullable=False),
        sa.Column("operator_id", sa.String(length=64), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("lighting_profile", sa.String(length=120), nullable=False),
        sa.Column("camera_profile", sa.String(length=120), nullable=False),
        sa.Column("temperature_celsius", sa.Float(), nullable=True),
        sa.Column("weight_grams", sa.Float(), nullable=True),
        sa.Column("standard_dish_key", sa.String(length=64), nullable=False),
        sa.Column("model_version", sa.String(length=120), nullable=False),
        sa.Column("top_label", sa.String(length=120), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("plating_score", sa.Float(), nullable=False),
        sa.Column("color_score", sa.Float(), nullable=False),
        sa.Column("deviation_score", sa.Float(), nullable=False),
        sa.Column("pass_decision", sa.Boolean(), nullable=False),
        sa.Column("feedback", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_production_events_dish_id"),
        "production_events",
        ["dish_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_production_events_operator_id"),
        "production_events",
        ["operator_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_production_events_store_id"),
        "production_events",
        ["store_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_production_events_store_id"), table_name="production_events")
    op.drop_index(op.f("ix_production_events_operator_id"), table_name="production_events")
    op.drop_index(op.f("ix_production_events_dish_id"), table_name="production_events")
    op.drop_table("production_events")
    op.drop_index(op.f("ix_dish_standards_dish_key"), table_name="dish_standards")
    op.drop_table("dish_standards")
    op.drop_index(op.f("ix_dishes_name"), table_name="dishes")
    op.drop_table("dishes")
