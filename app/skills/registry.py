from app.schemas.architecture import SkillSummary


def list_skills() -> list[SkillSummary]:
    return [
        SkillSummary(
            skill_id="strategy-decomposition",
            name="战略拆解技能",
            description="将经营目标拆解为多 Agent 可执行任务。",
            used_by=["ceo-agent"],
        ),
        SkillSummary(
            skill_id="agent-coordination",
            name="Agent 协同技能",
            description="协调多角色 Agent 的输入、输出和任务依赖。",
            used_by=["ceo-agent"],
        ),
        SkillSummary(
            skill_id="multimodal-capture",
            name="多模态采集技能",
            description="统一采集图像、重量、温度和光照环境元数据。",
            used_by=["vision-qa-agent"],
        ),
        SkillSummary(
            skill_id="quality-rule-engine",
            name="质检规则技能",
            description="将视觉、多模态信号与菜品标准结合，输出质量判断。",
            used_by=["vision-qa-agent", "store-ops-agent"],
        ),
        SkillSummary(
            skill_id="standard-authoring",
            name="标准编写技能",
            description="把研发经验转成结构化菜品标准和约束。",
            used_by=["menu-rnd-agent"],
        ),
        SkillSummary(
            skill_id="menu-iteration",
            name="菜单迭代技能",
            description="基于反馈、质量与经营结果提出菜单优化建议。",
            used_by=["menu-rnd-agent"],
        ),
        SkillSummary(
            skill_id="sop-audit",
            name="SOP 审计技能",
            description="识别门店执行偏差与流程不稳定环节。",
            used_by=["store-ops-agent"],
        ),
        SkillSummary(
            skill_id="ops-diagnosis",
            name="运营诊断技能",
            description="基于多维数据输出门店运营诊断和建议。",
            used_by=["store-ops-agent"],
        ),
        SkillSummary(
            skill_id="campaign-planning",
            name="营销策划技能",
            description="围绕菜品、门店和品牌目标生成活动建议。",
            used_by=["marketing-agent"],
        ),
        SkillSummary(
            skill_id="growth-analysis",
            name="增长分析技能",
            description="分析营销活动与经营结果的联动表现。",
            used_by=["marketing-agent"],
        ),
        SkillSummary(
            skill_id="contract-governance",
            name="契约治理技能",
            description="维护数据契约版本、兼容性规则和跨域治理策略。",
            used_by=["data-asset-agent"],
        ),
        SkillSummary(
            skill_id="asset-modeling",
            name="资产建模技能",
            description="把运营过程沉淀为可复用的数据资产模型。",
            used_by=["data-asset-agent"],
        ),
        SkillSummary(
            skill_id="flow-mapping",
            name="数据流编排技能",
            description="描述跨域数据流向、消费关系和资产沉淀路径。",
            used_by=["data-asset-agent"],
        ),
    ]
