# store_operation_snapshot.v1

## 定义

门店运营快照契约，用于沉淀某一时段门店执行状态、SOP 风险、现场指标与异常摘要。

## Owner

`store-ops-agent`

## 典型字段

- `store_id`
- `snapshot_time`
- `shift`
- `operator_count`
- `quality_alert_count`
- `sop_risk_items`
- `temperature_status`
- `throughput_score`
- `notes`

## 用途

- 门店运营诊断
- SOP 风险审计
- 运营历史沉淀
- 数据资产建模输入
