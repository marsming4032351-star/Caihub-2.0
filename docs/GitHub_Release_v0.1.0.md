# CaiHub v0.1.0

首个基础版本发布。

## 版本定位

`v0.1.0` 是 CaiHub 的第一版后端基础仓。

这个版本的目标不是一次性完成完整业务系统，而是先把平台后续演进最关键的边界搭起来：

- 菜品主数据
- 菜品标准
- 出品事件
- 标准驱动的质量裁决
- 数据契约与数据流
- agent / skill 治理结构
- Alembic 迁移基础设施

一句话概括：

> CaiHub 不是只做菜品识别，而是在搭一个以标准、事件和数据资产为核心的餐饮智能平台底座。

## 本次发布包含

### 核心业务能力

- 菜品管理接口
- 菜品标准接口
- 出品事件接口
- 基于标准的最小质量裁决逻辑
- OpenCV 视觉识别接口

### 平台与治理能力

- Data Mesh 视角的数据域结构
- 数据契约目录
- 数据流注册表
- 系统架构蓝图接口
- agent / skill 注册表

### 工程基础设施

- FastAPI 应用工厂
- service / repository 分层
- SQLAlchemy 2.x
- Alembic 初始迁移
- Pytest 测试覆盖基础链路

## 当前 API

- `GET /api/v1/health`
- `GET /api/v1/system/info`
- `GET /api/v1/system/architecture`
- `GET /api/v1/dishes`
- `POST /api/v1/dishes`
- `GET /api/v1/standards`
- `POST /api/v1/standards`
- `GET /api/v1/production/events`
- `POST /api/v1/production/events`
- `POST /api/v1/vision/dish-recognition`

## 当前项目特点

- 事件优先：围绕真实出品事件建模，而不是围绕单张图片建模
- 标准驱动：质量判断依赖菜品标准，不把规则写死在接口层
- 契约治理：平台内置数据契约、数据流和架构蓝图
- 平台预留：为后续 agent / skill、事件总线、分析导出预留结构

## 当前还未包含

- `store` / `operator` 实体建模
- 完整规则引擎 DSL
- 真实事件总线
- 数据分析导出链路
- agent 执行运行时

## 下一步方向

- 建立 `store` / `operator` 领域
- 把字符串关联升级成真实关系模型
- 引入事件总线
- 增加契约兼容性测试
- 推进 agent / skill 从注册层走向执行层

## 文档入口

- `README.md`
- `docs/发布说明.md`
- `docs/架构设计/架构总图.md`
- `docs/架构设计/技术实施说明.md`
- `docs/架构设计/业务版项目说明.md`
