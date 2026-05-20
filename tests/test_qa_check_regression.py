"""tests/test_qa_check_regression.py — qa_check.py CLI 回归测试

确保 Phase 1A 重构后 CLI 接口保持兼容。
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
QA_CHECK_MODULE = "scripts.qa_check"


def run_qa_check(*args: str, env_override: dict | None = None) -> subprocess.CompletedProcess:
    """用 subprocess 运行 qa_check，模拟真实 CLI 调用。"""
    import os
    env = os.environ.copy()
    env.pop("DASHSCOPE_API_KEY", None)  # 默认不设
    if env_override:
        env.update(env_override)
    return subprocess.run(
        [sys.executable, "-m", QA_CHECK_MODULE, *args],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


class TestCLIHelp:
    """--help 输出应保持兼容。"""

    def test_help_exits_zero(self):
        r = run_qa_check("--help")
        assert r.returncode == 0

    def test_help_shows_description(self):
        r = run_qa_check("--help")
        assert "CaiHub" in r.stdout
        assert "质检" in r.stdout

    def test_help_shows_arguments(self):
        r = run_qa_check("--help")
        assert "image" in r.stdout
        assert "--dish" in r.stdout
        assert "--standard" in r.stdout


class TestMissingAPIKey:
    """不设 DASHSCOPE_API_KEY 时应退出 1 并提示。"""

    def test_no_api_key_exits_nonzero(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(str(img))
        assert r.returncode == 1

    def test_no_api_key_shows_error(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(str(img))
        assert "DASHSCOPE_API_KEY" in r.stdout


class TestMissingImage:
    """不存在的图片路径应退出 1。"""

    def test_nonexistent_image_exits_nonzero(self):
        r = run_qa_check(
            "/nonexistent/path.jpg",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        assert r.returncode == 1

    def test_nonexistent_image_shows_error(self):
        r = run_qa_check(
            "/nonexistent/path.jpg",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        assert "图片不存在" in r.stdout or "错误" in r.stdout


class TestNoArguments:
    """不传任何参数应退出 2（argparse error）。"""

    def test_no_args_exits_nonzero(self):
        r = run_qa_check()
        assert r.returncode == 2


class TestDishParameter:
    """--dish 参数兼容性。"""

    def test_with_known_dish_shows_builtin_standard(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(
            str(img), "--dish", "麻婆豆腐",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        # 会因为 API 调用失败而退出，但应该先打印菜品和标准信息
        assert "麻婆豆腐" in r.stdout
        assert "豆腐块完整" in r.stdout

    def test_with_unknown_dish_shows_generic_standard(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(
            str(img), "--dish", "糖醋排骨",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        assert "通用标准" in r.stdout

    def test_without_dish_uses_default_name(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(
            str(img),
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        assert "未指定菜品" in r.stdout


class TestCustomStandard:
    """--standard 参数兼容性。"""

    def test_custom_standard_displayed(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(
            str(img), "--dish", "测试菜", "--standard", "我的自定义标准",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        assert "我的自定义标准" in r.stdout


class TestEndToEndMocked:
    """用 mock 完整跑通 CLI 主流程（不真正调用 API）。"""

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_pass_flow(self, mock_api, tmp_path):
        mock_api.return_value = json.dumps({
            "dish_name": "麻婆豆腐",
            "passed": True,
            "score": 88,
            "reason": "色泽红亮",
            "issues": [],
            "suggestions": "",
            "details": {"color": "好", "plating": "好", "portion": "好"},
        })
        img = tmp_path / "mapo.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")
        r = run_qa_check(
            str(img), "--dish", "麻婆豆腐",
            env_override={"DASHSCOPE_API_KEY": "sk-fake"},
        )
        # Note: subprocess 不会捕获 in-process mock，
        # 这个测试验证 CLI 参数解析和前置逻辑正确性。
        # API 调用在 subprocess 中不会被 mock，所以会失败。
        # 真正的 E2E mock 需要 in-process 测试。
        # 此处主要验证参数输出正确。
        assert "麻婆豆腐" in r.stdout

    def test_in_process_pass_flow(self, tmp_path, monkeypatch):
        """in-process 测试：mock API 后完整跑通 main()。"""
        img = tmp_path / "mapo.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")

        monkeypatch.setenv("DASHSCOPE_API_KEY", "sk-fake")
        monkeypatch.setattr(
            "sys.argv",
            ["qa_check", str(img), "--dish", "麻婆豆腐"],
        )

        good_response = json.dumps({
            "dish_name": "麻婆豆腐",
            "passed": True,
            "score": 88,
            "reason": "色泽红亮",
            "issues": [],
            "suggestions": "",
            "details": {"color": "好", "plating": "好", "portion": "好"},
        })

        with patch("scripts.ai_vision.call_qwen_vl", return_value=good_response):
            from scripts.qa_check import main
            # main() 会在最后 save_result，需要 mock data 目录
            monkeypatch.chdir(tmp_path)
            (tmp_path / "data").mkdir(exist_ok=True)
            # main 正常退出不 raise
            main()

    def test_in_process_fail_flow(self, tmp_path, monkeypatch, capsys):
        """不达标流程：显示问题和建议。"""
        img = tmp_path / "bad.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake")

        monkeypatch.setenv("DASHSCOPE_API_KEY", "sk-fake")
        monkeypatch.setattr(
            "sys.argv",
            ["qa_check", str(img), "--dish", "回锅肉"],
        )

        fail_response = json.dumps({
            "dish_name": "回锅肉",
            "passed": False,
            "score": 60,
            "reason": "肥瘦不均",
            "issues": ["肥瘦比例失调", "蒜苗不够翠绿"],
            "suggestions": "注意选肉部位",
            "details": {"color": "一般", "plating": "一般", "portion": "好"},
        })

        with patch("scripts.ai_vision.call_qwen_vl", return_value=fail_response):
            from scripts.qa_check import main
            monkeypatch.chdir(tmp_path)
            (tmp_path / "data").mkdir(exist_ok=True)
            main()

        captured = capsys.readouterr()
        assert "不达标" in captured.out
        assert "60" in captured.out
        assert "肥瘦比例失调" in captured.out
        assert "注意选肉部位" in captured.out
