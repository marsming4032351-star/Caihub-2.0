"""
CaiHub — 共享 AI 视觉模块

提供菜品识别 + 质检判定的合并调用，以及底层 Qwen VL API 封装。
供 qa_check.py (CLI) 和 feishu webhook (Phase 1B) 复用。

数据流:
    图片 bytes/base64 → call_qwen_vl() → raw text → parse_response() → dict
    图片 + 标准 → judge_dish() → QAResult (菜名+分数+问题+建议)
"""

from __future__ import annotations

import base64
import json
import mimetypes
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DASHSCOPE_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
MODEL = "qwen-vl-max"

DEFAULT_STANDARDS: dict[str, str] = {
    "麻婆豆腐": "豆腐块完整不碎，红油覆盖均匀，花椒粒可见，葱花点缀，色泽红亮，份量充足",
    "宫保鸡丁": "鸡丁大小均匀约1.5cm，花生完整金黄，干辣椒段分布均匀，葱段翠绿，酱色油亮",
    "鱼香肉丝": "肉丝粗细均匀，配菜（木耳丝、笋丝、胡萝卜丝）清晰可辨，酱汁裹匀，色泽红亮",
    "回锅肉": "肉片薄厚均匀微卷，蒜苗段翠绿，豆瓣酱色均匀，肥瘦相间，有锅气感",
    "水煮鱼": "鱼片完整白嫩，汤底红亮，花椒和干辣椒覆盖表面，豆芽打底，热油浇淋痕迹明显",
    "葱烧海参": "海参完整饱满有光泽，葱段焦香金黄，酱汁浓稠裹匀呈深褐色，海参表面挂汁均匀，摆盘整齐，份量充足",
}

# 合并 prompt: 一次调用同时识别菜名 + 判定质量
JUDGE_PROMPT_WITH_DISH = """你是一位专业的餐饮出品质检员。

请对比以下菜品标准，判断这张出品照片是否达标。

【菜品名称】{dish_name}
【出品标准】{standard}

请严格按以下 JSON 格式回复，不要输出其他内容：
{{
  "dish_name": "你识别到的菜品名称",
  "passed": true 或 false,
  "score": 0-100 的整数,
  "reason": "一句话说明判定理由",
  "issues": ["问题1", "问题2"],
  "suggestions": "一句话改进建议，达标时留空字符串",
  "details": {{
    "color": "色泽评价",
    "plating": "摆盘评价",
    "portion": "份量评价"
  }}
}}
"""

JUDGE_PROMPT_AUTO = """你是一位专业的餐饮出品质检员。

请先识别这张照片中的菜品名称，然后根据通用标准判断出品质量。

如果你识别出的菜品属于以下已知菜品，请使用对应标准：
{standards_text}

如果不属于以上任何一道菜，请使用通用标准（色泽正常，摆盘整齐，份量充足，无明显瑕疵）。

请严格按以下 JSON 格式回复，不要输出其他内容：
{{
  "dish_name": "你识别到的菜品名称",
  "passed": true 或 false,
  "score": 0-100 的整数,
  "reason": "一句话说明判定理由",
  "issues": ["问题1", "问题2"],
  "suggestions": "一句话改进建议，达标时留空字符串",
  "details": {{
    "color": "色泽评价",
    "plating": "摆盘评价",
    "portion": "份量评价"
  }}
}}
"""


@dataclass
class QAResult:
    """质检判定结果。"""

    dish_name: str = "未识别"
    passed: bool = False
    score: int = 0
    reason: str = ""
    issues: list[str] = field(default_factory=list)
    suggestions: str = ""
    details: dict[str, str] = field(default_factory=dict)
    parse_error: bool = False
    api_error: Optional[str] = None


class AIVisionError(Exception):
    """AI 视觉模块错误基类。"""


class ImageError(AIVisionError):
    """图片读取/编码错误。"""


class APIError(AIVisionError):
    """DashScope API 调用错误。"""


# ---------------------------------------------------------------------------
# 底层工具函数
# ---------------------------------------------------------------------------


def encode_image(image_path: str) -> tuple[str, str]:
    """读取图片文件并 base64 编码。返回 (base64_data, mime_type)。

    Raises:
        ImageError: 文件不存在或读取失败。
    """
    path = Path(image_path)
    if not path.exists():
        raise ImageError(f"图片不存在: {image_path}")

    mime_type = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
    except OSError as e:
        raise ImageError(f"图片读取失败: {e}") from e
    return data, mime_type


def encode_image_bytes(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    """将图片 bytes 编码为 base64 字符串。供 webhook 场景使用。"""
    return base64.b64encode(image_bytes).decode("utf-8")


def call_qwen_vl(image_b64: str, mime_type: str, prompt: str, api_key: str) -> str:
    """调用通义千问 VL API，返回模型原始文本回复。

    Raises:
        APIError: HTTP 错误或网络错误。
    """
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_b64}",
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1024,
    }).encode("utf-8")

    req = urllib.request.Request(
        DASHSCOPE_BASE,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise APIError(f"API 错误 ({e.code}): {error_body}") from e
    except urllib.error.URLError as e:
        raise APIError(f"网络错误: {e.reason}") from e
    except (KeyError, IndexError) as e:
        raise APIError(f"API 返回格式异常: {e}") from e


def parse_response(raw: str) -> dict:
    """解析模型返回的 JSON。容忍 markdown 代码块包裹。"""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines)

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        return {
            "dish_name": "未识别",
            "passed": False,
            "score": 0,
            "reason": f"AI 返回无法解析: {raw[:200]}",
            "issues": [],
            "suggestions": "",
            "details": {"color": "N/A", "plating": "N/A", "portion": "N/A"},
            "_parse_error": True,
        }

    # 标准化字段
    if "passed" not in result:
        result["passed"] = False
    if isinstance(result.get("passed"), str):
        result["passed"] = result["passed"].lower() in ("true", "yes", "是")
    result["score"] = max(0, min(100, int(float(result.get("score", 0)))))
    result.setdefault("dish_name", "未识别")
    result.setdefault("issues", [])
    if isinstance(result["issues"], str):
        result["issues"] = [result["issues"]] if result["issues"] else []
    result.setdefault("suggestions", "")
    result.setdefault("details", {})
    return result


# ---------------------------------------------------------------------------
# 高层业务函数
# ---------------------------------------------------------------------------


def judge_dish(
    image_b64: str,
    mime_type: str,
    api_key: str,
    dish_name: Optional[str] = None,
    standard: Optional[str] = None,
    standards: Optional[dict[str, str]] = None,
) -> QAResult:
    """一次 AI 调用完成菜名识别 + 质检判定。

    Args:
        image_b64: 图片 base64 编码。
        mime_type: 图片 MIME 类型。
        api_key: DashScope API key。
        dish_name: 已知菜名（可选）。不传则由 AI 自动识别。
        standard: 该菜品的文字标准（可选）。不传则查内置标准。
        standards: 自定义标准字典（可选）。不传则用 DEFAULT_STANDARDS。

    Returns:
        QAResult 包含菜名、分数、问题、建议等。
    """
    all_standards = standards if standards is not None else DEFAULT_STANDARDS

    if dish_name and standard:
        # 菜名和标准都已知，直接判定
        prompt = JUDGE_PROMPT_WITH_DISH.format(
            dish_name=dish_name,
            standard=standard,
        )
    elif dish_name:
        # 菜名已知但无自定义标准，查内置
        found_standard = all_standards.get(dish_name, "菜品色泽正常，摆盘整齐，份量充足，无明显瑕疵")
        prompt = JUDGE_PROMPT_WITH_DISH.format(
            dish_name=dish_name,
            standard=found_standard,
        )
    else:
        # 菜名未知，让 AI 自动识别 + 判定
        standards_text = "\n".join(
            f"- {name}: {desc}" for name, desc in all_standards.items()
        )
        prompt = JUDGE_PROMPT_AUTO.format(standards_text=standards_text)

    try:
        raw = call_qwen_vl(image_b64, mime_type, prompt, api_key)
    except APIError as e:
        return QAResult(
            dish_name=dish_name or "未识别",
            api_error=str(e),
            reason=f"AI 调用失败: {e}",
        )

    parsed = parse_response(raw)

    return QAResult(
        dish_name=parsed.get("dish_name", dish_name or "未识别"),
        passed=parsed["passed"],
        score=parsed["score"],
        reason=parsed.get("reason", ""),
        issues=parsed.get("issues", []),
        suggestions=parsed.get("suggestions", ""),
        details=parsed.get("details", {}),
        parse_error=parsed.get("_parse_error", False),
    )
