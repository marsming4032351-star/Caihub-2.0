# 架构设计

## 总体目标

CaiHub 后端不是单纯的 CRUD 服务，而是一个面向平台演进的仓库骨架，核心关注点包括：

- 领域边界
- Data Mesh
- 数据契约
- 数据流
- 智能体与技能协作

## 推荐阅读顺序

- [架构总图.md](/Users/ming/CaiHub/docs/架构设计/架构总图.md)
- [技术实施说明.md](/Users/ming/CaiHub/docs/架构设计/技术实施说明.md)
- [业务版项目说明.md](/Users/ming/CaiHub/docs/架构设计/业务版项目说明.md)

## 分层与分域并存

当前项目采用两套视角共同组织：

- 技术分层：`api`、`services`、`repositories`
- 领域分域：`domains/catalog`、`domains/vision`、`domains/platform`

技术分层保证 FastAPI 服务落地简单，领域分域为未来拆成独立数据产品保留空间。
