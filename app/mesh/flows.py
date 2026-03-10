from app.schemas.architecture import DataFlowSummary


def list_data_flows() -> list[DataFlowSummary]:
    return [
        DataFlowSummary(
            flow_id="production_to_vision_qa",
            source="production.dish_production_event",
            targets=["vision-qa-agent.quality", "analytics.production_history"],
            mode="event",
            contract="dish_production_event.v1",
            description="每次真实出品先形成事件，再进入 Vision QA 质检和历史沉淀。",
        ),
        DataFlowSummary(
            flow_id="vision_to_ops_and_rnd",
            source="vision.dish_recognition_result",
            targets=["store-ops-agent.diagnosis", "menu-rnd-agent.iteration"],
            mode="event",
            contract="dish_recognition_result.v1",
            description="识别结果进入运营诊断和菜单研发迭代链路。",
        ),
        DataFlowSummary(
            flow_id="catalog_to_rnd_and_api",
            source="catalog.dish_catalog",
            targets=["menu-rnd-agent.standarding", "public-api.dishes"],
            mode="serve",
            contract="dish_catalog.v1",
            description="菜品目录既服务研发标准沉淀，也向外提供基础查询能力。",
        ),
        DataFlowSummary(
            flow_id="operations_to_data_asset",
            source="operations.store_operation_snapshot",
            targets=["data-asset-agent.modeling", "analytics.ops_history"],
            mode="event",
            contract="store_operation_snapshot.v1",
            description="门店运营快照进入资产建模和运营历史分析。",
        ),
        DataFlowSummary(
            flow_id="rnd_to_data_asset",
            source="rnd.menu_rnd_knowledge",
            targets=["data-asset-agent.knowledge_base", "ceo-agent.summary"],
            mode="read",
            contract="menu_rnd_knowledge.v1",
            description="研发知识沉淀后被数据资产层和 CEO Agent 消费。",
        ),
        DataFlowSummary(
            flow_id="marketing_to_data_asset",
            source="marketing.campaign_feedback_event",
            targets=["data-asset-agent.modeling", "marketing-agent.analysis"],
            mode="event",
            contract="campaign_feedback_event.v1",
            description="营销反馈事件进入增长分析和数据资产沉淀。",
        ),
        DataFlowSummary(
            flow_id="asset_to_ceo_and_ecosystem",
            source="asset.restaurant_data_asset",
            targets=["ceo-agent.dashboard", "external-api.ecosystem"],
            mode="serve",
            contract="restaurant_data_asset.v1",
            description="沉淀后的数据资产同时服务内部经营判断与外部 API 生态。",
        ),
        DataFlowSummary(
            flow_id="platform_to_all_agents",
            source="platform.system_blueprint",
            targets=[
                "ceo-agent",
                "vision-qa-agent",
                "menu-rnd-agent",
                "store-ops-agent",
                "marketing-agent",
                "data-asset-agent",
            ],
            mode="read",
            contract="system_blueprint.v2",
            description="系统蓝图被各 Agent 消费，用于保持协同边界和治理一致性。",
        ),
    ]
