"""
CaiHub Phase 0 — AI 菜品质检验证脚本

用法:
    python scripts/qa_check.py <图片路径> [--dish <菜名>] [--standard <标准描述>]

示例:
    python scripts/qa_check.py photos/mapo-tofu-001.jpg --dish 麻婆豆腐
    python scripts/qa_check.py photos/kung-pao.jpg --dish 宫保鸡丁 --standard "鸡丁大小均匀，花生完整，葱段翠绿"

环境变量:
    DASHSCOPE_API_KEY  — 通义千问 API Key (必需)

结果保存到 data/qa_results.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from .ai_vision import (
    DEFAULT_STANDARDS,
    MODEL,
    ImageError,
    encode_image,
    judge_dish,
)


def save_result(image_path: str, dish_name: str, standard: str, result: dict) -> Path:
    """追加结果到 data/qa_results.json。"""
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "data"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "qa_results.json"

    record = {
        "image_path": str(Path(image_path).resolve()),
        "dish_name": dish_name,
        "standard": standard,
        "passed": result["passed"],
        "score": result["score"],
        "reason": result["reason"],
        "details": result.get("details", {}),
        "model": MODEL,
        "timestamp": datetime.now().isoformat(),
    }

    records: list[dict] = []
    if output_file.exists():
        try:
            records = json.loads(output_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            records = []

    records.append(record)
    output_file.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(description="CaiHub AI 菜品质检验证")
    parser.add_argument("image", help="菜品照片路径")
    parser.add_argument("--dish", default="未指定菜品", help="菜品名称")
    parser.add_argument("--standard", default=None, help="出品标准描述（不指定则使用内置标准）")
    args = parser.parse_args()

    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("错误: 请设置环境变量 DASHSCOPE_API_KEY")
        print("  export DASHSCOPE_API_KEY='sk-xxxxxxxx'")
        sys.exit(1)

    standard = args.standard
    if standard is None:
        standard = DEFAULT_STANDARDS.get(args.dish)
    if standard is None:
        standard = "菜品色泽正常，摆盘整齐，份量充足，无明显瑕疵"
        print(f"提示: 未找到「{args.dish}」的内置标准，使用通用标准")

    print(f"菜品: {args.dish}")
    print(f"标准: {standard}")
    print(f"图片: {args.image}")
    print(f"模型: {MODEL}")
    print("—" * 40)
    print("正在调用 AI 判定...")

    try:
        image_b64, mime_type = encode_image(args.image)
    except ImageError as e:
        print(f"错误: {e}")
        sys.exit(1)

    result = judge_dish(
        image_b64=image_b64,
        mime_type=mime_type,
        api_key=api_key,
        dish_name=args.dish,
        standard=standard,
    )

    if result.api_error:
        print(f"错误: {result.api_error}")
        sys.exit(1)

    passed_text = "✅ 达标" if result.passed else "❌ 不达标"
    print(f"\n判定结果: {passed_text}")
    print(f"分数: {result.score}/100")
    print(f"原因: {result.reason}")

    if result.details:
        print(f"色泽: {result.details.get('color', 'N/A')}")
        print(f"摆盘: {result.details.get('plating', 'N/A')}")
        print(f"份量: {result.details.get('portion', 'N/A')}")

    if result.issues:
        print(f"\n问题:")
        for issue in result.issues:
            print(f"  • {issue}")

    if result.suggestions:
        print(f"建议: {result.suggestions}")

    # 转为 dict 保存（保持原有格式兼容）
    result_dict = {
        "passed": result.passed,
        "score": result.score,
        "reason": result.reason,
        "details": result.details,
    }
    output_file = save_result(args.image, result.dish_name, standard, result_dict)
    print(f"\n结果已保存: {output_file}")


if __name__ == "__main__":
    main()
