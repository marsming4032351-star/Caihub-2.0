from app.schemas.architecture import DataFlowSummary


def list_data_flows() -> list[DataFlowSummary]:
    return [
        DataFlowSummary(
            flow_id="production_to_quality",
            source="production.dish_production_event",
            targets=["quality.rule_engine", "analytics.production_history"],
            mode="event",
            contract="dish_production_event.v1",
            description="每次真实出品先形成事件，再进入规则判定和历史沉淀。",
        ),
        DataFlowSummary(
            flow_id="catalog_to_api",
            source="catalog.dish_catalog",
            targets=["public-api.dishes", "merchant-console.menu"],
            mode="serve",
            contract="dish_catalog.v1",
            description="目录域通过事务接口向前台和商户后台提供菜品数据。",
        ),
        DataFlowSummary(
            flow_id="vision_to_catalog",
            source="vision.dish_recognition_result",
            targets=["catalog.enrichment", "quality.rule_engine", "analytics.model_quality"],
            mode="event",
            contract="dish_recognition_result.v1",
            description="识别结果以事件形式进入目录增强、规则判定和模型评估链路。",
        ),
        DataFlowSummary(
            flow_id="platform_to_agents",
            source="platform.system_blueprint",
            targets=["agents.backend-architect", "agents.data-governance"],
            mode="read",
            contract="system_blueprint.v1",
            description="平台架构蓝图被代理系统消费，用于治理和自动化生成。",
        ),
    ]
