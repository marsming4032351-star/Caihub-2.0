# 数据契约

## 当前契约

- `dish_catalog.v1`
- `dish_production_event.v1`
- `dish_recognition_result.v1`
- `store_operation_snapshot.v1`
- `menu_rnd_knowledge.v1`
- `campaign_feedback_event.v1`
- `restaurant_data_asset.v1`
- `system_blueprint.v2`

## 契约原则

- 每个契约必须有明确 owner
- 契约必须显式版本化
- 契约变更要区分兼容与不兼容
- API schema 与数据产品 schema 可以关联，但不能混为一体
- 契约要服务 Agent 协作和数据资产沉淀，而不是只服务接口返回

## 当前 owner 映射

- `dish_catalog.v1` → `menu-rnd-agent`
- `dish_production_event.v1` → `vision-qa-agent`
- `dish_recognition_result.v1` → `vision-qa-agent`
- `store_operation_snapshot.v1` → `store-ops-agent`
- `menu_rnd_knowledge.v1` → `menu-rnd-agent`
- `campaign_feedback_event.v1` → `marketing-agent`
- `restaurant_data_asset.v1` → `data-asset-agent`
- `system_blueprint.v2` → `ceo-agent`

## 代码与文档位置

- `app/domains/catalog/contracts/`
- `app/domains/production/contracts/`
- `app/domains/vision/contracts/`
- `app/domains/platform/contracts/`
- `docs/数据契约/store_operation_snapshot_v1.md`
- `docs/数据契约/menu_rnd_knowledge_v1.md`
- `docs/数据契约/campaign_feedback_event_v1.md`
- `docs/数据契约/restaurant_data_asset_v1.md`
