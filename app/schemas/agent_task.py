from datetime import datetime

from pydantic import BaseModel, Field


class AgentTaskEnvelope(BaseModel):
    task_id: str
    assigned_agent_id: str
    title: str
    objective: str
    inputs: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    priority: str = Field(default="normal")
    status: str = Field(default="planned")
    created_at: datetime


class OrchestrationPlan(BaseModel):
    plan_id: str
    owner_agent_id: str
    mission: str
    status: str = Field(default="draft")
    tasks: list[AgentTaskEnvelope] = Field(default_factory=list)
