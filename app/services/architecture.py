from app.agents.registry import list_agents
from app.mesh.contracts import list_data_contracts
from app.mesh.flows import list_data_flows
from app.schemas.architecture import ArchitectureBlueprintResponse
from app.skills.registry import list_skills


class ArchitectureService:
    def get_blueprint(self) -> ArchitectureBlueprintResponse:
        contracts = list_data_contracts()
        domains = sorted({contract.domain for contract in contracts})
        return ArchitectureBlueprintResponse(
            core_principles=[
                "事件优先：系统围绕真实出品事件建模，而不是围绕单张图片建模。",
                "多模态采集：视觉、重量、温度、时间共同构成有效判断输入。",
                "模型与规则分离：识别负责对齐语义，裁决由标准与规则引擎完成。",
                "数据资产沉淀：每次出品都应转化为可追溯、可复用的数据资产。",
                "Agent 负责编排，Skill 负责能力封装，并通过契约受治理。",
            ],
            mesh_domains=domains,
            data_contracts=contracts,
            data_flows=list_data_flows(),
            agents=list_agents(),
            skills=list_skills(),
        )
