# CaiHub Agent 核心架构：ReAct + Tool Calling + Memory

## 1. CaiHub Agent 核心架构总览

CaiHub 的 Agent 核心架构不是单纯让模型“回答问题”，而是让 Agent 在餐饮门店真实出品流程中完成可追踪、可复盘、可沉淀的运营判断。

本次架构升级把三个核心概念落到 Vision QA Agent：

- **ReAct**：让 Agent 明确表达“为什么下一步要做什么”，形成思考、行动、观察的质检链路。
- **Tool Calling**：让 Agent 调用菜品识别、标准查询、视觉检测、温度检测、质检裁决和 Memory 读写工具。
- **Memory**：把一次出品质检从临时判断沉淀为门店、菜品、标准和质量事件的数据资产。

在 CaiHub 中，Agent 不是替代所有系统，而是成为跨工具、跨数据、跨业务标准的编排层。

## 2. ReAct 在菜品出品质检中的作用

菜品出品质检不是单点识别问题，而是一个连续推理过程。Vision QA Agent 需要先确认图片中的菜品，再查询菜品标准，然后检查视觉质量和温度，最后结合历史记录做裁决。

ReAct 的价值在于：

- 把质检过程拆成可解释步骤。
- 让每个工具调用都有明确业务原因。
- 让产品和运营人员能复盘“Agent 为什么这样判断”。
- 为后续人工复核、模型优化和 SOP 改进留下过程证据。

示例：

```text
Thought: 先确认图片中的菜品是否匹配订单菜品。
Action: call:dish_recognition_tool
Observation: 菜品识别为宫保鸡丁，置信度 0.91。
```

## 3. Tool Calling 在 CaiBox / Vision QA Agent 中的作用

CaiBox 负责采集图像、温度等多模态现场数据，Vision QA Agent 负责把这些数据转成质检判断。Tool Calling 是两者之间的产品化接口。

当前 mock runtime 中包含以下工具：

- `dish_recognition_tool`：根据菜品图片识别菜品。
- `dish_standard_tool`：查询菜品在当前门店的出品标准。
- `visual_quality_tool`：检测色泽、摆盘、缺料等视觉质量。
- `temperature_tool`：检测出餐温度是否满足标准。
- `quality_decision_tool`：汇总多源结果，输出质检裁决。
- `memory_tool`：读取历史质检记录，并写入本次质检结果。

这些工具当前使用 mock 数据，未来可以替换为真实视觉模型、温度传感器、门店数据库、RAG 知识库或数据资产服务。

## 4. Memory 如何沉淀为 CaiHub 数据资产

Memory 不是聊天上下文，而是餐饮运营经验的数据化沉淀。

一次 Vision QA 质检会沉淀：

- 哪个门店、哪个订单、哪个菜品发生了质检事件。
- 识别、标准、视觉、温度、历史记录分别给出了什么证据。
- Agent 最终裁决是合格、不合格还是需人工复核。
- 问题原因、建议动作和工具调用 lineage。

当这些记录持续累积后，CaiHub 可以形成：

- 门店质量稳定性画像。
- 菜品标准执行偏差分析。
- 出品问题高频原因库。
- 训练视觉模型和质检规则的标注样本。
- 面向品牌总部、门店运营和供应链的行业数据资产。

## 5. Vision QA Agent 完整流程

### 输入

- 菜品图片：`image_url`
- 订单信息：`order_id`、`dish_id`
- 温度数据：`temperature_celsius`
- 门店信息：`store_id`

### 流程

```text
识别菜品
  -> 查询标准
  -> 调用视觉检测
  -> 调用温度检测
  -> 查询历史 Memory
  -> 生成质检裁决
  -> 写入 Memory
```

### 输出

- 质检结论：合格 / 不合格 / 需人工复核
- 问题原因：例如识别置信度不足、视觉分数低、温度偏离标准
- 建议动作：例如正常出餐、复测温度、人工确认、重新检查摆盘
- 数据资产记录：包含门店、菜品、订单、裁决、工具调用和 Memory lineage

当前演示接口：

```text
POST /api/v1/agents/vision-qa/inspect-demo
```

返回结构包括：

- `task_input`
- `react_steps`
- `tool_calls`
- `observations`
- `memory_records`
- `final_decision`
- `data_asset_record`

## 6. 产品经理视角说明

从产品经理视角看，这次升级的重点不是“多加一个接口”，而是把 AI Agent 的产品闭环做出来：

- 用户输入来自真实门店场景：菜品图片、订单、温度、门店。
- Agent 不直接给结论，而是通过 ReAct 拆解判断过程。
- 每一步判断都通过 Tool Calling 连接到可替换的业务能力。
- 最终结果不仅服务当次出餐，也写入 Memory 形成长期数据资产。

这让 CaiHub 从“识别 demo”升级为“可解释、可扩展、可沉淀的餐饮 AI 运营系统”。

## 7. AI 产品经理面试表达版

可以这样表达：

```text
我在 CaiHub 中设计并落地了一个 Vision QA Agent 的核心架构 demo。

它面向餐饮门店出品质检场景，输入菜品图片、订单、温度和门店信息。Agent 使用 ReAct 将任务拆成识别菜品、查询标准、视觉检测、温度检测、查询历史 Memory、生成裁决和写入 Memory 七个步骤。

每一步都通过 Tool Calling 调用独立工具，当前是 mock 实现，未来可以替换为视觉模型、传感器、数据库或 RAG 知识库。最终输出合格、不合格或需人工复核，并给出原因、建议动作和数据资产记录。

这个设计体现了我对 AI 产品的理解：Agent 的价值不只是生成答案，而是编排工具、沉淀过程、形成可复用的数据资产，最终服务真实业务闭环。
```
