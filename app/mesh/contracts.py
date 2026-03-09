from app.schemas.architecture import DataContractSummary


def list_data_contracts() -> list[DataContractSummary]:
    return [
        DataContractSummary(
            domain="catalog",
            product="dish_catalog",
            version="v1",
            owner="catalog-team",
            description="菜品目录主数据契约，服务菜单、检索和商户展示。",
            schema_ref="app/domains/catalog/contracts/dish_contract_v1.py",
        ),
        DataContractSummary(
            domain="production",
            product="dish_production_event",
            version="v1",
            owner="quality-team",
            description="出品事件契约，绑定一次真实出品、多模态采集和质检结果。",
            schema_ref="app/domains/production/contracts/dish_event_contract_v1.py",
        ),
        DataContractSummary(
            domain="vision",
            product="dish_recognition_result",
            version="v1",
            owner="vision-team",
            description="菜品识别结果契约，服务推荐、质检和模型评估。",
            schema_ref="app/domains/vision/contracts/recognition_contract_v1.py",
        ),
        DataContractSummary(
            domain="platform",
            product="system_blueprint",
            version="v1",
            owner="platform-team",
            description="平台架构元数据契约，服务治理、审计和自动化代理。",
            schema_ref="app/domains/platform/contracts/system_contract_v1.py",
        ),
    ]
