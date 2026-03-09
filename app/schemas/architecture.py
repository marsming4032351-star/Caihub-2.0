from pydantic import BaseModel, Field


class DataContractSummary(BaseModel):
    domain: str
    product: str
    version: str
    owner: str
    description: str
    schema_ref: str


class DataFlowSummary(BaseModel):
    flow_id: str
    source: str
    targets: list[str] = Field(default_factory=list)
    mode: str
    contract: str
    description: str


class AgentSummary(BaseModel):
    agent_id: str
    name: str
    responsibilities: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)


class SkillSummary(BaseModel):
    skill_id: str
    name: str
    description: str
    used_by: list[str] = Field(default_factory=list)


class ArchitectureBlueprintResponse(BaseModel):
    core_principles: list[str] = Field(default_factory=list)
    mesh_domains: list[str] = Field(default_factory=list)
    data_contracts: list[DataContractSummary] = Field(default_factory=list)
    data_flows: list[DataFlowSummary] = Field(default_factory=list)
    agents: list[AgentSummary] = Field(default_factory=list)
    skills: list[SkillSummary] = Field(default_factory=list)
