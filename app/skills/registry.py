from app.schemas.architecture import SkillSummary


def list_skills() -> list[SkillSummary]:
    return [
        SkillSummary(
            skill_id="quality-rule-engine",
            name="质检规则技能",
            description="将视觉、多模态信号与菜品标准结合，输出合格性裁决。",
            used_by=["quality-judge"],
        ),
        SkillSummary(
            skill_id="multimodal-capture",
            name="多模态采集技能",
            description="统一采集图像、重量、温度和光照环境元数据。",
            used_by=["quality-judge", "data-governance"],
        ),
        SkillSummary(
            skill_id="api-design",
            name="接口设计技能",
            description="生成和校验 FastAPI 接口、Schema 与错误模型。",
            used_by=["backend-architect"],
        ),
        SkillSummary(
            skill_id="contract-governance",
            name="契约治理技能",
            description="维护数据契约版本、兼容性规则和样例载荷。",
            used_by=["data-governance", "backend-architect"],
        ),
        SkillSummary(
            skill_id="flow-mapping",
            name="数据流编排技能",
            description="描述数据流向、输入输出依赖和下游消费关系。",
            used_by=["data-governance", "skill-orchestrator"],
        ),
    ]
