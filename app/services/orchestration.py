from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.agent_task import AgentTaskEnvelope, OrchestrationPlan


class OrchestrationService:
    def build_foundation_plan(self) -> OrchestrationPlan:
        now = datetime.now(timezone.utc)
        return OrchestrationPlan(
            plan_id=str(uuid4()),
            owner_agent_id="ceo-agent",
            mission="Build a minimum viable restaurant AI operating loop.",
            status="draft",
            tasks=[
                AgentTaskEnvelope(
                    task_id=str(uuid4()),
                    assigned_agent_id="vision-qa-agent",
                    title="Establish quality observation loop",
                    objective="Turn production events into structured quality feedback.",
                    inputs=["dish_production_event.v1", "dish_recognition_result.v1"],
                    expected_outputs=["quality feedback", "anomaly tags"],
                    priority="high",
                    created_at=now,
                ),
                AgentTaskEnvelope(
                    task_id=str(uuid4()),
                    assigned_agent_id="store-ops-agent",
                    title="Capture store operation snapshots",
                    objective="Create reusable snapshots for SOP and execution diagnostics.",
                    inputs=["store_operation_snapshot.v1"],
                    expected_outputs=["ops diagnosis", "risk items"],
                    priority="high",
                    created_at=now,
                ),
                AgentTaskEnvelope(
                    task_id=str(uuid4()),
                    assigned_agent_id="data-asset-agent",
                    title="Aggregate reusable data assets",
                    objective="Combine production, operations and feedback into reusable assets.",
                    inputs=["restaurant_data_asset.v1", "campaign_feedback_event.v1"],
                    expected_outputs=["asset models", "export-ready datasets"],
                    priority="high",
                    created_at=now,
                ),
            ],
        )
