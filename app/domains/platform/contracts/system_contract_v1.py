from pydantic import BaseModel, Field


class SystemBlueprintContractV1(BaseModel):
    app_name: str
    version: str
    mesh_domains: list[str] = Field(default_factory=list)
    data_contract_count: int = Field(ge=0)
    agent_count: int = Field(ge=0)
    skill_count: int = Field(ge=0)
