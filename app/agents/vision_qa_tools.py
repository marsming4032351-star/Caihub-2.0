from app.schemas.vision_qa_agent import FinalQualityDecision, QualityDecisionStatus


def dish_recognition_tool(image_url: str, expected_dish_id: str) -> dict[str, object]:
    return {
        "recognized_dish_id": expected_dish_id,
        "label": "宫保鸡丁",
        "confidence": 0.91,
        "model_version": "mock-vision-v1",
        "image_url": image_url,
    }


def dish_standard_tool(dish_id: str, store_id: str) -> dict[str, object]:
    return {
        "dish_id": dish_id,
        "store_id": store_id,
        "standard_name": "宫保鸡丁出品标准",
        "target_temperature_celsius": 65.0,
        "temperature_tolerance_celsius": 8.0,
        "minimum_visual_score": 0.78,
        "key_checks": ["色泽", "摆盘", "份量", "温度"],
    }


def visual_quality_tool(
    image_url: str,
    recognized_dish_id: str,
    standard: dict[str, object],
) -> dict[str, object]:
    score = 0.86
    minimum_score = float(standard["minimum_visual_score"])
    return {
        "image_url": image_url,
        "dish_id": recognized_dish_id,
        "visual_score": score,
        "passed": score >= minimum_score,
        "findings": ["色泽正常", "摆盘轻微偏移", "未发现明显漏料"],
    }


def temperature_tool(
    temperature_celsius: float,
    standard: dict[str, object],
) -> dict[str, object]:
    target = float(standard["target_temperature_celsius"])
    tolerance = float(standard["temperature_tolerance_celsius"])
    delta = round(abs(temperature_celsius - target), 2)
    return {
        "temperature_celsius": temperature_celsius,
        "target_temperature_celsius": target,
        "delta_celsius": delta,
        "passed": delta <= tolerance,
    }


def memory_tool(
    store_id: str,
    dish_id: str,
    final_decision: dict[str, object] | None = None,
) -> dict[str, object]:
    if final_decision is None:
        return {
            "mode": "read",
            "records": [
                {
                    "memory_id": f"mem-{store_id}-{dish_id}-last",
                    "summary": "近 7 天该菜品出品稳定，偶发温度偏低。",
                    "quality_pass_rate": 0.93,
                }
            ],
        }

    return {
        "mode": "write",
        "record": {
            "memory_id": f"mem-{store_id}-{dish_id}-current",
            "summary": "本次 Vision QA 裁决已沉淀为门店菜品质检事件。",
            "final_status": final_decision["status"],
        },
    }


def quality_decision_tool(
    recognition: dict[str, object],
    visual_quality: dict[str, object],
    temperature: dict[str, object],
    historical_memory: dict[str, object],
) -> FinalQualityDecision:
    reasons: list[str] = []
    suggested_actions: list[str] = []

    if recognition["confidence"] < 0.75:
        reasons.append("菜品识别置信度不足")
        suggested_actions.append("请人工确认菜品是否与订单一致")

    if not visual_quality["passed"]:
        reasons.append("视觉质检分数低于菜品标准")
        suggested_actions.append("重新检查摆盘、份量和缺料情况")

    if not temperature["passed"]:
        reasons.append("出餐温度偏离标准范围")
        suggested_actions.append("复测温度并检查保温流程")

    if not reasons:
        reasons.append("识别、视觉和温度检测均满足当前 mock 标准")
        suggested_actions.append("正常出餐并沉淀为合格样本")

    status: QualityDecisionStatus
    if len(reasons) == 1 and visual_quality["passed"] and temperature["passed"]:
        status = "qualified"
    elif recognition["confidence"] < 0.75:
        status = "manual_review"
    else:
        status = "unqualified"

    memory_records = historical_memory.get("records", [])
    confidence = 0.88 if memory_records else 0.82
    if status != "qualified":
        confidence -= 0.08

    return FinalQualityDecision(
        status=status,
        reasons=reasons,
        suggested_actions=suggested_actions,
        confidence=round(confidence, 2),
    )
