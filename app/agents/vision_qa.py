from app.agents.vision_qa_tools import (
    dish_recognition_tool,
    dish_standard_tool,
    memory_tool,
    quality_decision_tool,
    temperature_tool,
    visual_quality_tool,
)
from app.schemas.vision_qa_agent import (
    AgentMemoryRecord,
    AgentObservation,
    ReActStep,
    ToolCallRecord,
    VisionQAInspectDemoRequest,
    VisionQAInspectDemoResponse,
)


class VisionQAAgent:
    def inspect_demo(
        self,
        task_input: VisionQAInspectDemoRequest,
    ) -> VisionQAInspectDemoResponse:
        react_steps: list[ReActStep] = []
        tool_calls: list[ToolCallRecord] = []
        observations: list[AgentObservation] = []
        memory_records: list[AgentMemoryRecord] = []

        def record_tool_call(
            call_id: str,
            tool_name: str,
            request: dict[str, object],
            result: dict[str, object],
            thought: str,
            action: str,
        ) -> None:
            observation_id = f"obs-{call_id}"
            tool_calls.append(
                ToolCallRecord(
                    call_id=call_id,
                    tool_name=tool_name,
                    request=request,
                    result=result,
                )
            )
            observations.append(
                AgentObservation(
                    observation_id=observation_id,
                    source=tool_name,
                    summary=action,
                    payload=result,
                )
            )
            react_steps.append(
                ReActStep(
                    step_id=f"react-{call_id}",
                    thought=thought,
                    action=f"call:{tool_name}",
                    observation_ref=observation_id,
                )
            )

        recognition_request = {
            "image_url": task_input.image_url,
            "expected_dish_id": task_input.dish_id,
        }
        recognition = dish_recognition_tool(**recognition_request)
        record_tool_call(
            "001",
            "dish_recognition_tool",
            recognition_request,
            recognition,
            "先确认图片中的菜品是否匹配订单菜品。",
            "完成菜品识别并获得置信度。",
        )

        standard_request = {
            "dish_id": task_input.dish_id,
            "store_id": task_input.store_id,
        }
        standard = dish_standard_tool(**standard_request)
        record_tool_call(
            "002",
            "dish_standard_tool",
            standard_request,
            standard,
            "识别完成后，需要查询该菜品在当前门店的出品标准。",
            "获得视觉、温度和关键检查项标准。",
        )

        visual_request = {
            "image_url": task_input.image_url,
            "recognized_dish_id": str(recognition["recognized_dish_id"]),
            "standard": standard,
        }
        visual_quality = visual_quality_tool(**visual_request)
        record_tool_call(
            "003",
            "visual_quality_tool",
            visual_request,
            visual_quality,
            "用菜品标准约束视觉检测，而不是只看模型标签。",
            "完成色泽、摆盘和缺料的 mock 视觉质检。",
        )

        temperature_request = {
            "temperature_celsius": task_input.temperature_celsius,
            "standard": standard,
        }
        temperature = temperature_tool(**temperature_request)
        record_tool_call(
            "004",
            "temperature_tool",
            temperature_request,
            temperature,
            "温度会影响出品质量，需要和视觉结果合并判断。",
            "完成温度与标准范围的比对。",
        )

        memory_read_request = {
            "store_id": task_input.store_id,
            "dish_id": task_input.dish_id,
        }
        historical_memory = memory_tool(**memory_read_request)
        record_tool_call(
            "005",
            "memory_tool",
            memory_read_request,
            historical_memory,
            "读取历史质检 Memory，判断本次问题是否属于门店长期模式。",
            "获得该门店该菜品的历史质量摘要。",
        )
        for record in historical_memory["records"]:
            memory_records.append(
                AgentMemoryRecord(
                    memory_id=str(record["memory_id"]),
                    memory_type="historical_quality_summary",
                    content=record,
                )
            )

        decision_request = {
            "recognition": recognition,
            "visual_quality": visual_quality,
            "temperature": temperature,
            "historical_memory": historical_memory,
        }
        final_decision = quality_decision_tool(**decision_request)
        record_tool_call(
            "006",
            "quality_decision_tool",
            decision_request,
            final_decision.model_dump(),
            "汇总识别、标准、视觉、温度和历史 Memory，形成最终裁决。",
            "输出合格、不合格或需人工复核的质检结论。",
        )

        memory_write_request = {
            "store_id": task_input.store_id,
            "dish_id": task_input.dish_id,
            "final_decision": final_decision.model_dump(),
        }
        written_memory = memory_tool(**memory_write_request)
        record_tool_call(
            "007",
            "memory_tool",
            memory_write_request,
            written_memory,
            "裁决不是终点，需要把过程沉淀为可复用的数据资产。",
            "写入本次质检 Memory 记录。",
        )
        memory_records.append(
            AgentMemoryRecord(
                memory_id=str(written_memory["record"]["memory_id"]),
                memory_type="vision_qa_quality_event",
                content=written_memory["record"],
            )
        )

        data_asset_record = {
            "asset_type": "vision-qa-quality-event",
            "source_agent": "vision-qa-agent",
            "store_id": task_input.store_id,
            "dish_id": task_input.dish_id,
            "order_id": task_input.order_id,
            "final_status": final_decision.status,
            "lineage": {
                "tool_call_ids": [tool_call.call_id for tool_call in tool_calls],
                "memory_ids": [record.memory_id for record in memory_records],
            },
        }

        return VisionQAInspectDemoResponse(
            task_input=task_input,
            react_steps=react_steps,
            tool_calls=tool_calls,
            observations=observations,
            memory_records=memory_records,
            final_decision=final_decision,
            data_asset_record=data_asset_record,
        )


def get_vision_qa_agent() -> VisionQAAgent:
    return VisionQAAgent()
