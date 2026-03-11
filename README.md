# CaiHub AI Company

CaiHub 是一个面向餐饮行业的 **AI 运营系统**。

它不是单纯的菜品识别工具，也不只是一个后厨质检 SaaS。CaiHub 的目标是用 AI Agent 复刻并增强餐厅运营体系，把经验、流程和判断沉淀成可复用的数据资产。

一句话概括：

```text
CaiHub 不是在做一个识别 demo，而是在构建餐饮行业的 AI 原生运营基础设施。
```

## 核心定义

CaiHub 可以被定义为：

- 餐饮行业的 AI 运营系统
- 以 Agent 协作驱动的餐厅数字组织
- 以数据资产沉淀为终局的餐饮智能平台

核心思想：

```text
用 AI Agent 复刻餐厅运营体系，让餐饮经验变成数据资产。
```

## AI Company 组织结构

```text
Mars（Founder）
  │
  ▼
CaiHub CEO Agent
  │
  ├── Vision QA Agent（CaiBox）
  ├── Menu R&D Agent
  ├── Store Ops Agent
  ├── Marketing Agent
  └── Data Asset Agent
```

### 各 Agent 职责

- **CaiHub CEO Agent**
  - 统筹目标、协同各业务 Agent、形成组织级决策摘要
- **Vision QA Agent（CaiBox）**
  - 负责视觉质检、异常发现、多模态采集协调
- **Menu R&D Agent**
  - 负责菜单研发、菜品标准沉淀、研发迭代建议
- **Store Ops Agent**
  - 负责门店执行、SOP 稳定性、运营优化建议
- **Marketing Agent**
  - 负责增长、内容、活动与品牌传播策略
- **Data Asset Agent**
  - 负责数据沉淀、知识结构化、资产建模与输出

## 技术架构

### Layer 1 — Hardware Layer

设备输入层，包括：

- CaiBox
- 摄像头
- 照度系统
- 温度传感器

### Layer 2 — Vision Layer

视觉理解层，包括：

- 色泽识别
- 摆盘识别
- 食材识别
- 比例识别

### Layer 3 — Agent Layer

运营决策层，包括：

- Kitchen / Vision QA Agent
- Menu R&D Agent
- Store Ops Agent
- Marketing Agent
- CEO Agent

### Layer 4 — Data Asset Layer

沉淀内容包括：

- 菜品数据
- 厨房模型
- 门店运营数据
- 菜单研发知识
- 质量事件历史

最终形成：

- 餐饮行业数据资产
- 可复用的运营模型
- 可扩展的 API 与生态能力

## 当前仓库定位

当前仓库仍然是 **第一阶段后端基础仓**，但方向已经明确对齐到上面的最终架构。

当前已落地的骨架包括：

- FastAPI 后端服务
- 菜品、标准、出品事件三条主链路
- 最小质检裁决闭环
- Data Mesh 视角的数据契约与数据流
- agent / skill 注册与治理骨架
- Alembic 迁移基础设施
- OpenClaw 驱动的 AI+餐饮资讯日报自动化

也就是说：

```text
当前代码实现的是 AI Company 的平台底座，不是最终完整形态。
```

## 当前可运行自动化

仓库里现在已经包含一条可直接运行的 OpenClaw 自动化链路：

```text
ai-food-news Agent (Gemini)
  -> 搜索 AI+餐饮资讯
  -> 生成中文观察日报
  -> Gmail 自动发信
  -> launchd 开机补发 + 多时段兜底
```

对应文件：

- `scripts/send_ai_food_news_email.py`
- `scripts/run_ai_food_news_email.sh`
- `deploy/ai.caihub.ai-food-news.plist`

这个能力已经是可运行自动化，不是停留在文档层。

## 当前目录

```text
app/                      应用主目录
  api/                    接口层
  agents/                 Agent 注册表
  core/                   应用工厂、配置、生命周期
  db/                     数据库连接与初始化
  domains/                领域契约
  events/                 领域事件
  mesh/                   数据契约与数据流注册
  models/                 ORM 模型
  repositories/           数据访问层
  schemas/                API 与架构响应模型
  services/               业务与架构服务层
  skills/                 Skill 注册表
  vision/                 视觉识别组件
agents/                   Agent 资产目录
docs/                     中文文档目录
migrations/               Alembic 迁移
skills/                   Skill 资产目录
tests/                    测试目录
```

## 当前 API

- `GET /api/v1/health`
- `GET /api/v1/system/info`
- `GET /api/v1/system/architecture`
- `GET /api/v1/system/agent-runtime`
- `GET /api/v1/system/orchestration-plan`
- `GET /api/v1/dishes`
- `POST /api/v1/dishes`
- `GET /api/v1/stores`
- `POST /api/v1/stores`
- `GET /api/v1/operators`
- `POST /api/v1/operators`
- `GET /api/v1/operations/snapshots`
- `POST /api/v1/operations/snapshots`
- `GET /api/v1/data-assets`
- `POST /api/v1/data-assets`
- `GET /api/v1/data-assets/build-summary`
- `POST /api/v1/data-assets/materialize-preview`
- `POST /api/v1/data-assets/materialize`
- `GET /api/v1/standards`
- `POST /api/v1/standards`
- `GET /api/v1/production/events`
- `POST /api/v1/production/events`
- `POST /api/v1/vision/dish-recognition`

## 今日已落地成果（可视化）

```mermaid
flowchart LR
    A[Dish / Standard] --> B[Production Event]
    S[Store] --> B
    O[Operator] --> B
    B --> Q[Quality Decision Event]
    S --> OPS[Operation Snapshot]
    O --> OPS
    B --> DAS[Data Asset Build Summary]
    OPS --> DAS
    DAS --> PRE[Materialize Preview]
    PRE --> MAT[Materialized Data Asset]
    MAT --> AE[Asset Materialized Event]
    MAT --> LIN[Lineage]
    LIN --> PIDs[production_event_ids]
    LIN --> OIDs[operation_snapshot_ids]
```

这张图对应今天已经落到代码里的链路，不是 PPT 许愿。

## 当前落地状态

### 已落地代码骨架
- `dish`
- `standard`
- `production_event`
- `store`
- `operator`
- `store_operation_snapshot`
- `data_asset`
- `agent runtime overview`
- `orchestration plan`
- `data asset materialization`
- `data asset lineage`
- `asset materialized event`

### 当前最像样的一条链
```text
store / operator
  -> production event
  -> quality decision
  -> operation snapshot
  -> data asset summary
  -> materialize preview
  -> materialized data asset
  -> asset event
  -> lineage tracking
```

## 商业逻辑

CaiHub 的商业模式由四层组成：

- **设备收入**：CaiBox
- **软件订阅**：质检、标准、运营 Agent 服务
- **数据资产平台**：沉淀行业模型与知识资产
- **API 生态**：向餐饮 SaaS、品牌、供应链系统开放能力

最终目标：

```text
形成餐饮行业 AI 数据平台。
```

## 关键原则

- 先采集真实运营事件，再做 AI 解读
- 先沉淀标准和规则，再放大 Agent 决策
- 先形成数据资产闭环，再扩张生态接口
- 识别负责观察，裁决负责判断，Agent 负责编排

## 运行方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

数据库迁移并启动：

```bash
export CAIHUB_DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/caihub"
alembic upgrade head
uvicorn app.main:app --reload
```

本地快速测试环境：

```bash
export CAIHUB_AUTO_CREATE_TABLES=true
uvicorn app.main:app --reload
```

## 文档入口

- [OpenClaw 日报发信配置](docs/架构设计/OpenClaw_日报发信配置.md)
- [OpenClaw 日报补发方案](docs/架构设计/OpenClaw_日报补发方案.md)
- [OpenClaw 周报自动化方案](docs/架构设计/OpenClaw_周报自动化方案.md)
- [OpenClaw 资讯智能体架构图](docs/架构设计/OpenClaw_资讯智能体架构图.md)
- [流程图](docs/架构设计/流程图.md)
- [架构总图](docs/架构设计/架构总图.md)
- [技术实施说明](docs/架构设计/技术实施说明.md)
- [业务版项目说明](docs/架构设计/业务版项目说明.md)

## 下一步重点

- 建立 `store` / `operator` 领域
- 升级关系模型与规则引擎
- 接入真实事件总线
- 推进 Agent runtime，而不只停留在注册层
- 让数据回流形成可分析、可训练、可复用的数据资产
