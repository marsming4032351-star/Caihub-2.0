from app.schemas.architecture import AgentSummary


def list_agents() -> list[AgentSummary]:
    return [
        AgentSummary(
            agent_id="quality-judge",
            name="品控裁决代理",
            responsibilities=["消费出品事件", "融合识别和规则", "输出合格性裁决"],
            inputs=["出品事件", "识别结果", "菜品标准"],
            outputs=["质检结论", "扣分项", "纠偏动作"],
        ),
        AgentSummary(
            agent_id="backend-architect",
            name="后端架构代理",
            responsibilities=["维护服务边界", "推进契约版本演进", "校验 API 分层"],
            inputs=["系统蓝图", "领域契约", "接口规范"],
            outputs=["代码骨架", "架构变更提案", "治理建议"],
        ),
        AgentSummary(
            agent_id="data-governance",
            name="数据治理代理",
            responsibilities=["维护 Data Mesh 元数据", "审核数据契约", "跟踪数据流"],
            inputs=["数据契约", "事件定义", "流向配置"],
            outputs=["契约审计结果", "血缘说明", "治理规则"],
        ),
        AgentSummary(
            agent_id="skill-orchestrator",
            name="技能编排代理",
            responsibilities=["匹配技能到任务", "协调多代理执行", "沉淀复用流程"],
            inputs=["任务描述", "技能清单", "代理能力映射"],
            outputs=["执行计划", "技能调用建议", "流程模板"],
        ),
    ]
