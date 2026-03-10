from pydantic import BaseModel, Field


class AgentRuntimeStatus(BaseModel):
    agent_id: str
    enabled: bool = True
    mode: str = Field(default="registered")
    has_runtime: bool = False
    summary: str


class AgentRuntimeOverview(BaseModel):
    total_agents: int
    runtime_ready_agents: int
    orchestration_status: str
    agents: list[AgentRuntimeStatus] = Field(default_factory=list)
