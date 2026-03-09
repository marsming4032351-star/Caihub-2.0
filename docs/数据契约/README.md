# 数据契约

## 当前契约

- `dish_catalog.v1`
- `dish_recognition_result.v1`
- `system_blueprint.v1`

## 契约原则

- 每个契约必须有明确 owner
- 契约必须显式版本化
- 契约变更要区分兼容与不兼容
- API schema 与数据产品 schema 可以关联，但不能混为一体

## 代码位置

- `app/domains/catalog/contracts/`
- `app/domains/vision/contracts/`
- `app/domains/platform/contracts/`
