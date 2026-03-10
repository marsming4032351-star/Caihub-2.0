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
                "先采集真实运营事件，再做 AI 解读。",
                "先沉淀标准和规则，再放大 Agent 决策。",
                "识别负责观察，裁决负责判断，Agent 负责编排。",
                "每次出品、运营和营销动作都应转化为可复用的数据资产。",
                "CaiHub 的目标不是单点工具，而是餐饮行业的 AI 运营系统。",
            ],
            mesh_domains=domains,
            data_contracts=contracts,
            data_flows=list_data_flows(),
            agents=list_agents(),
            skills=list_skills(),
        )
