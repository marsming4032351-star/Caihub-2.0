# CaiHub 后端仓库

CaiHub 是一个面向餐饮标准化、出品事件沉淀和数据资产治理的后端基础仓库。

当前版本已经完成第一阶段平台骨架，核心关注点包括：

- 菜品、标准、出品事件三条主链路
- Data Mesh 视角的数据域与数据流
- 显式数据契约
- agent / skill 的治理边界
- Alembic 迁移基础设施

一句话概括：

```text
CaiHub 不是只做菜品识别，而是在搭一个以标准、事件和数据资产为核心的餐饮智能平台底座。
```

## 当前状态

- 阶段：`v0.1.0`
- 类型：后端基础仓 / 平台骨架
- 已完成：API、标准、出品事件、最小质检裁决、架构蓝图、迁移基础设施
- 测试状态：`pytest` 通过

## 项目亮点

- 事件优先：先建模真实出品事件，再建模识别结果
- 标准驱动：质量裁决依赖菜品标准，而不是写死在接口层
- 契约治理：平台内置数据契约、数据流和系统蓝图
- 平台扩展：提前预留 agent / skill 扩展结构
- 工程落地：已经接入 Alembic、测试和基础服务分层

## 中文目录展示

```text
app/                      应用主目录
  api/                    接口层
  agents/                 智能体注册表
  core/                   核心配置与应用装配
  db/                     数据库连接与初始化
  domains/                领域模块与数据契约
  events/                 领域事件
  mesh/                   Data Mesh 元数据注册
  models/                 ORM 模型
  repositories/           数据访问层
  schemas/                API 与架构模型
  services/               应用服务层
  skills/                 技能注册表
  vision/                 视觉识别能力
agents/                   智能体资产目录
docs/                     中文文档目录
skills/                   技能资产目录
tests/                    测试目录
```

更详细的中文目录说明见 [docs/目录总览.md](/Users/ming/CaiHub/docs/目录总览.md)。

## 当前核心能力

- 菜品主数据管理
- 菜品标准管理
- 出品事件采集与查询
- 基于标准的最小质量裁决
- 系统架构蓝图接口
- 数据契约与数据流注册
- 视觉识别接口
- Alembic 数据库迁移

当前仓库同时保留“技术分层”和“领域分域”两种组织方式，目的不是做复杂化，而是为后续拆成真正的数据产品保留边界。

当前已经吸收旧版架构仓的几个关键理念：

- 先建模“真实出品事件”，再建模识别结果
- 识别只负责“这是什么”，裁决由规则和标准完成
- Agent 负责编排，Skill 负责能力封装与治理

## 运行方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

默认数据库目标是 PostgreSQL。先执行 Alembic 迁移，再启动服务：

```bash
export CAIHUB_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/caihub"
alembic upgrade head
uvicorn app.main:app --reload
```

如果你只是在本地快速跑测试型环境，也可以显式开启自动建表：

```bash
export CAIHUB_AUTO_CREATE_TABLES=true
uvicorn app.main:app --reload
```

## 当前 API

- `GET /api/v1/health`
  服务健康检查
- `GET /api/v1/system/info`
  平台基础信息
- `GET /api/v1/system/architecture`
  平台架构蓝图，返回数据域、契约、数据流、agents、skills
- `GET /api/v1/dishes`
  查询菜品列表
- `POST /api/v1/dishes`
  创建菜品
- `GET /api/v1/production/events`
  查询出品事件
- `POST /api/v1/production/events`
  创建出品事件并按菜品标准执行质检规则
- `GET /api/v1/standards`
  查询菜品标准
- `POST /api/v1/standards`
  创建菜品标准
- `POST /api/v1/vision/dish-recognition`
  基于 OpenCV 的菜品识别

## 文档入口

- [docs/发布说明.md](/Users/ming/CaiHub/docs/发布说明.md)
- [docs/架构设计/架构总图.md](/Users/ming/CaiHub/docs/架构设计/架构总图.md)
- [docs/架构设计/技术实施说明.md](/Users/ming/CaiHub/docs/架构设计/技术实施说明.md)
- [docs/架构设计/业务版项目说明.md](/Users/ming/CaiHub/docs/架构设计/业务版项目说明.md)
- [docs/架构设计/README.md](/Users/ming/CaiHub/docs/架构设计/README.md)
- [docs/数据契约/README.md](/Users/ming/CaiHub/docs/数据契约/README.md)
- [docs/数据流/README.md](/Users/ming/CaiHub/docs/数据流/README.md)
- [docs/智能体/README.md](/Users/ming/CaiHub/docs/智能体/README.md)
- [docs/技能/README.md](/Users/ming/CaiHub/docs/技能/README.md)
- [docs/旧仓库复用分析.md](/Users/ming/CaiHub/docs/旧仓库复用分析.md)

## 下一步建议

- 建立 `store` / `operator` 领域
- 把字符串关联升级成真实关系模型
- 为订单、商户、用户建立独立领域和契约
- 引入事件总线，让 `app/events` 从定义层走向真实发布
- 增加契约兼容性测试和 schema 导出流程
