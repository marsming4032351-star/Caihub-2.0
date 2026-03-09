# CaiHub 后端仓库

这是 CaiHub 平台的第一版后端项目仓库。它不再只按普通 FastAPI 服务来组织，而是开始引入以下核心约束：

- Data Mesh 视角的数据域划分
- 显式数据契约
- 可追踪的数据流
- 面向自动化协作的 agents / skills 设计
- 出品事件优先的后端建模方式
- 模型识别与规则裁决分离

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

## 当前架构重点

- `app/api`
  FastAPI 路由与依赖注入
- `app/services`
  业务服务和架构蓝图服务
- `app/repositories`
  SQLAlchemy 数据访问
- `app/domains`
  按领域沉淀数据契约
- `app/mesh`
  Data Mesh 元数据、契约清单、数据流清单
- `app/events`
  事件模型，方便后续接入异步数据流
- `app/agents` 与 `app/skills`
  运行时的代理和技能注册表

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

- 为订单、商户、用户建立独立领域和契约
- 引入事件总线，让 `app/events` 从定义层走向真实发布
- 增加契约兼容性测试和 schema 导出流程
