from app.schemas.architecture import AgentSummary


def list_agents() -> list[AgentSummary]:
    return [
        AgentSummary(
            agent_id="ceo-agent",
            name="CaiHub CEO Agent",
            responsibilities=["组织级目标拆解", "跨 Agent 协同", "输出经营与执行摘要"],
            inputs=["系统蓝图", "跨域事件", "运营指标", "战略目标"],
            outputs=["任务分配建议", "组织级周报", "决策支持摘要"],
        ),
        AgentSummary(
            agent_id="vision-qa-agent",
            name="Vision QA Agent",
            responsibilities=["消费多模态出品事件", "执行视觉质检辅助", "发现异常并输出反馈"],
            inputs=["出品事件", "图像", "温度", "重量", "菜品标准"],
            outputs=["质检建议", "异常标签", "质量反馈"],
        ),
        AgentSummary(
            agent_id="menu-rnd-agent",
            name="Menu R&D Agent",
            responsibilities=["沉淀菜品标准", "输出研发迭代建议", "维护菜单知识"],
            inputs=["菜品目录", "历史质量事件", "用户反馈", "研发目标"],
            outputs=["标准建议", "菜单迭代建议", "研发知识条目"],
        ),
        AgentSummary(
            agent_id="store-ops-agent",
            name="Store Ops Agent",
            responsibilities=["分析门店执行波动", "识别 SOP 风险", "输出运营优化建议"],
            inputs=["出品事件", "门店指标", "人员记录", "质量历史"],
            outputs=["门店诊断", "SOP 风险项", "运营优化动作"],
        ),
        AgentSummary(
            agent_id="marketing-agent",
            name="Marketing Agent",
            responsibilities=["生成营销动作建议", "分析活动反馈", "连接品牌与门店数据"],
            inputs=["活动数据", "门店经营数据", "菜品反馈", "品牌目标"],
            outputs=["活动建议", "内容方向", "增长诊断"],
        ),
        AgentSummary(
            agent_id="data-asset-agent",
            name="Data Asset Agent",
            responsibilities=["维护数据资产模型", "治理跨域契约", "沉淀可复用知识结构"],
            inputs=["数据契约", "数据流", "跨域事件", "历史数据"],
            outputs=["资产模型", "契约治理建议", "数据产品定义"],
        ),
    ]
