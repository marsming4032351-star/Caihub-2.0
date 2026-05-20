"""tests/test_ai_vision.py — scripts/ai_vision.py 单元测试"""

from __future__ import annotations

import base64
import json
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from scripts.ai_vision import (
    APIError,
    ImageError,
    QAResult,
    call_qwen_vl,
    encode_image,
    encode_image_bytes,
    judge_dish,
    parse_response,
)


# ---------------------------------------------------------------------------
# parse_response
# ---------------------------------------------------------------------------


class TestParseResponse:
    """parse_response 负责将 AI 返回的原始文本解析为标准 dict。"""

    def test_valid_json(self):
        raw = json.dumps({
            "dish_name": "麻婆豆腐",
            "passed": True,
            "score": 88,
            "reason": "色泽红亮",
            "issues": [],
            "suggestions": "",
            "details": {"color": "好", "plating": "好", "portion": "好"},
        })
        r = parse_response(raw)
        assert r["dish_name"] == "麻婆豆腐"
        assert r["passed"] is True
        assert r["score"] == 88
        assert r["issues"] == []

    def test_markdown_wrapped_json(self):
        raw = '```json\n{"passed": true, "score": 90}\n```'
        r = parse_response(raw)
        assert r["passed"] is True
        assert r["score"] == 90

    def test_unparseable_returns_error_dict(self):
        r = parse_response("这不是 JSON")
        assert r["_parse_error"] is True
        assert r["passed"] is False
        assert r["score"] == 0
        assert "无法解析" in r["reason"]

    def test_float_string_score(self):
        r = parse_response('{"score": "85.5"}')
        assert r["score"] == 85

    def test_float_score(self):
        r = parse_response('{"score": 92.7}')
        assert r["score"] == 92

    def test_score_clamped_high(self):
        r = parse_response('{"score": 150}')
        assert r["score"] == 100

    def test_score_clamped_low(self):
        r = parse_response('{"score": -10}')
        assert r["score"] == 0

    def test_missing_score_defaults_zero(self):
        r = parse_response('{"passed": true}')
        assert r["score"] == 0

    def test_string_issues_coerced_to_list(self):
        r = parse_response('{"issues": "光泽不足"}')
        assert r["issues"] == ["光泽不足"]

    def test_empty_string_issues_coerced_to_empty_list(self):
        r = parse_response('{"issues": ""}')
        assert r["issues"] == []

    def test_list_issues_preserved(self):
        r = parse_response('{"issues": ["a", "b"]}')
        assert r["issues"] == ["a", "b"]

    def test_passed_string_true(self):
        r = parse_response('{"passed": "true"}')
        assert r["passed"] is True

    def test_passed_string_yes(self):
        r = parse_response('{"passed": "yes"}')
        assert r["passed"] is True

    def test_passed_string_chinese(self):
        r = parse_response('{"passed": "是"}')
        assert r["passed"] is True

    def test_passed_string_false(self):
        r = parse_response('{"passed": "no"}')
        assert r["passed"] is False

    def test_missing_passed_defaults_false(self):
        r = parse_response('{"score": 50}')
        assert r["passed"] is False

    def test_defaults_filled(self):
        r = parse_response("{}")
        assert r["dish_name"] == "未识别"
        assert r["issues"] == []
        assert r["suggestions"] == ""
        assert r["details"] == {}

    def test_empty_json_object(self):
        r = parse_response("{}")
        assert r["passed"] is False
        assert r["score"] == 0


# ---------------------------------------------------------------------------
# encode_image
# ---------------------------------------------------------------------------


class TestEncodeImage:
    """encode_image 读取文件并返回 (base64, mime_type)。"""

    def test_valid_jpeg(self, tmp_path):
        img = tmp_path / "test.jpg"
        img.write_bytes(b"\xff\xd8\xff\xe0fake-jpeg")
        b64, mime = encode_image(str(img))
        assert base64.b64decode(b64) == b"\xff\xd8\xff\xe0fake-jpeg"
        assert mime == "image/jpeg"

    def test_valid_png(self, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNGfake")
        b64, mime = encode_image(str(img))
        assert mime == "image/png"

    def test_nonexistent_file_raises(self):
        with pytest.raises(ImageError, match="图片不存在"):
            encode_image("/no/such/file.jpg")

    def test_unreadable_file_raises(self, tmp_path):
        img = tmp_path / "locked.jpg"
        img.write_bytes(b"data")
        img.chmod(0o000)
        try:
            with pytest.raises(ImageError, match="图片读取失败"):
                encode_image(str(img))
        finally:
            img.chmod(0o644)


class TestEncodeImageBytes:
    def test_basic(self):
        data = b"hello"
        result = encode_image_bytes(data, "image/png")
        assert base64.b64decode(result) == b"hello"


# ---------------------------------------------------------------------------
# call_qwen_vl (mock API)
# ---------------------------------------------------------------------------


class TestCallQwenVL:
    """call_qwen_vl 发 HTTP 请求到 DashScope，这里 mock urlopen。"""

    def _mock_response(self, content: str) -> MagicMock:
        body = json.dumps({
            "choices": [{"message": {"content": content}}]
        }).encode("utf-8")
        resp = MagicMock()
        resp.read.return_value = body
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        return resp

    @patch("scripts.ai_vision.urllib.request.urlopen")
    def test_success(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response("hello")
        result = call_qwen_vl("base64data", "image/jpeg", "test prompt", "sk-fake")
        assert result == "hello"

    @patch("scripts.ai_vision.urllib.request.urlopen")
    def test_payload_structure(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response("ok")
        call_qwen_vl("b64", "image/png", "prompt text", "sk-key")
        req = mock_urlopen.call_args[0][0]
        payload = json.loads(req.data.decode("utf-8"))
        assert payload["model"] == "qwen-vl-max"
        assert payload["messages"][0]["content"][0]["type"] == "image_url"
        assert "data:image/png;base64,b64" in payload["messages"][0]["content"][0]["image_url"]["url"]
        assert payload["messages"][0]["content"][1]["text"] == "prompt text"
        assert req.get_header("Authorization") == "Bearer sk-key"

    @patch("scripts.ai_vision.urllib.request.urlopen")
    def test_http_error_raises_api_error(self, mock_urlopen):
        import urllib.error
        err = urllib.error.HTTPError(
            url="http://x", code=401, msg="Unauthorized",
            hdrs=None, fp=BytesIO(b"bad key"),
        )
        mock_urlopen.side_effect = err
        with pytest.raises(APIError, match="API 错误.*401"):
            call_qwen_vl("b64", "image/jpeg", "p", "bad-key")

    @patch("scripts.ai_vision.urllib.request.urlopen")
    def test_url_error_raises_api_error(self, mock_urlopen):
        import urllib.error
        mock_urlopen.side_effect = urllib.error.URLError("no network")
        with pytest.raises(APIError, match="网络错误"):
            call_qwen_vl("b64", "image/jpeg", "p", "key")

    @patch("scripts.ai_vision.urllib.request.urlopen")
    def test_malformed_response_raises_api_error(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = b'{"no_choices": true}'
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp
        with pytest.raises(APIError, match="返回格式异常"):
            call_qwen_vl("b64", "image/jpeg", "p", "key")


# ---------------------------------------------------------------------------
# judge_dish (mock call_qwen_vl)
# ---------------------------------------------------------------------------


class TestJudgeDish:
    """judge_dish 是高层函数，mock 掉底层 API 调用。"""

    GOOD_RESPONSE = json.dumps({
        "dish_name": "葱烧海参",
        "passed": True,
        "score": 92,
        "reason": "海参饱满",
        "issues": [],
        "suggestions": "",
        "details": {"color": "好", "plating": "好", "portion": "好"},
    })

    FAIL_RESPONSE = json.dumps({
        "dish_name": "麻婆豆腐",
        "passed": False,
        "score": 55,
        "reason": "豆腐碎裂",
        "issues": ["豆腐不完整", "花椒不够"],
        "suggestions": "轻翻炒",
        "details": {"color": "一般", "plating": "差", "portion": "好"},
    })

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_pass_result(self, mock_api):
        mock_api.return_value = self.GOOD_RESPONSE
        r = judge_dish("b64", "image/jpeg", "key", dish_name="葱烧海参", standard="标准")
        assert isinstance(r, QAResult)
        assert r.passed is True
        assert r.score == 92
        assert r.dish_name == "葱烧海参"
        assert r.api_error is None

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_fail_result(self, mock_api):
        mock_api.return_value = self.FAIL_RESPONSE
        r = judge_dish("b64", "image/jpeg", "key", dish_name="麻婆豆腐")
        assert r.passed is False
        assert r.score == 55
        assert len(r.issues) == 2
        assert r.suggestions == "轻翻炒"

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_api_error_returns_qa_result(self, mock_api):
        mock_api.side_effect = APIError("timeout")
        r = judge_dish("b64", "image/jpeg", "key", dish_name="test")
        assert r.api_error is not None
        assert "timeout" in r.api_error
        assert r.passed is False

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_auto_identify_mode(self, mock_api):
        mock_api.return_value = self.GOOD_RESPONSE
        r = judge_dish("b64", "image/jpeg", "key")  # no dish_name
        assert r.dish_name == "葱烧海参"
        # 验证 prompt 使用了 JUDGE_PROMPT_AUTO（包含 standards_text）
        called_prompt = mock_api.call_args[0][2]
        assert "请先识别" in called_prompt

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_dish_name_with_standard(self, mock_api):
        mock_api.return_value = self.GOOD_RESPONSE
        judge_dish("b64", "image/jpeg", "key", dish_name="回锅肉", standard="自定义标准")
        called_prompt = mock_api.call_args[0][2]
        assert "回锅肉" in called_prompt
        assert "自定义标准" in called_prompt

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_dish_name_without_standard_uses_builtin(self, mock_api):
        mock_api.return_value = self.GOOD_RESPONSE
        judge_dish("b64", "image/jpeg", "key", dish_name="麻婆豆腐")
        called_prompt = mock_api.call_args[0][2]
        assert "豆腐块完整不碎" in called_prompt

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_unknown_dish_uses_generic_standard(self, mock_api):
        mock_api.return_value = self.GOOD_RESPONSE
        judge_dish("b64", "image/jpeg", "key", dish_name="糖醋排骨")
        called_prompt = mock_api.call_args[0][2]
        assert "色泽正常" in called_prompt

    @patch("scripts.ai_vision.call_qwen_vl")
    def test_unparseable_ai_response(self, mock_api):
        mock_api.return_value = "这不是JSON"
        r = judge_dish("b64", "image/jpeg", "key", dish_name="test")
        assert r.parse_error is True
        assert r.passed is False
