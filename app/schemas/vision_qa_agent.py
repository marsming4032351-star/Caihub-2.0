from typing import Literal

from pydantic import BaseModel, Field


QualityDecisionStatus = Literal["qualified", "unqualified", "manual_review"]


class VisionQAInspectDemoRequest(BaseModel):
    image_url: str = Field(min_length=1)
    order_id: str = Field(min_length=1, max_length=120)
    dish_id: str = Field(min_length=1, max_length=120)
    temperature_celsius: float
    store_id: str = Field(min_length=1, max_length=120)


class ReActStep(BaseModel):
    step_id: str
    thought: str
    action: str
    observation_ref: str


class ToolCallRecord(BaseModel):
    call_id: str
    tool_name: str
    request: dict[str, object]
    result: dict[str, object]


class AgentObservation(BaseModel):
    observation_id: str
    source: str
    summary: str
    payload: dict[str, object]


class AgentMemoryRecord(BaseModel):
    memory_id: str
    memory_type: str
    content: dict[str, object]


class FinalQualityDecision(BaseModel):
    status: QualityDecisionStatus
    reasons: list[str]
    suggested_actions: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


class VisionQAInspectDemoResponse(BaseModel):
    task_input: VisionQAInspectDemoRequest
    react_steps: list[ReActStep]
    tool_calls: list[ToolCallRecord]
    observations: list[AgentObservation]
    memory_records: list[AgentMemoryRecord]
    final_decision: FinalQualityDecision
    data_asset_record: dict[str, object]
