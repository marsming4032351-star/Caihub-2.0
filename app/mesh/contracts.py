from app.schemas.architecture import DataContractSummary


def list_data_contracts() -> list[DataContractSummary]:
    return [
        DataContractSummary(
            domain="catalog",
            product="dish_catalog",
            version="v1",
            owner="menu-rnd-agent",
            description="菜品目录主数据契约，服务菜单研发、展示与标准绑定。",
            schema_ref="app/domains/catalog/contracts/dish_contract_v1.py",
        ),
        DataContractSummary(
            domain="production",
            product="dish_production_event",
            version="v1",
            owner="vision-qa-agent",
            description="一次真实出品的事件契约，绑定图像、多模态输入和质量结果。",
            schema_ref="app/domains/production/contracts/dish_event_contract_v1.py",
        ),
        DataContractSummary(
            domain="vision",
            product="dish_recognition_result",
            version="v1",
            owner="vision-qa-agent",
            description="视觉识别结果契约，服务质检、目录增强和模型评估。",
            schema_ref="app/domains/vision/contracts/recognition_contract_v1.py",
        ),
        DataContractSummary(
            domain="operations",
            product="store_operation_snapshot",
            version="v1",
            owner="store-ops-agent",
            description="门店运营快照契约，沉淀门店执行状态、SOP 风险和现场指标。",
            schema_ref="docs/数据契约/store_operation_snapshot_v1.md",
        ),
        DataContractSummary(
            domain="rnd",
            product="menu_rnd_knowledge",
            version="v1",
            owner="menu-rnd-agent",
            description="菜单研发知识契约，沉淀菜品标准、迭代建议和研发经验。",
            schema_ref="docs/数据契约/menu_rnd_knowledge_v1.md",
        ),
        DataContractSummary(
            domain="marketing",
            product="campaign_feedback_event",
            version="v1",
            owner="marketing-agent",
            description="营销反馈事件契约，关联活动、菜品反馈和经营结果。",
            schema_ref="docs/数据契约/campaign_feedback_event_v1.md",
        ),
        DataContractSummary(
            domain="asset",
            product="restaurant_data_asset",
            version="v1",
            owner="data-asset-agent",
            description="跨域沉淀后的餐饮数据资产契约，服务分析、训练和 API 输出。",
            schema_ref="docs/数据契约/restaurant_data_asset_v1.md",
        ),
        DataContractSummary(
            domain="platform",
            product="system_blueprint",
            version="v2",
            owner="ceo-agent",
            description="AI Company 级系统蓝图契约，描述 Agent、Skill、数据域和数据流。",
            schema_ref="app/domains/platform/contracts/system_contract_v1.py",
        ),
    ]
