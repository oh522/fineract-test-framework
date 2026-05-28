"""
统一断言工具 — 统一错误格式，便于快速定位失败原因
"""
import jsonpath


def assert_status(resp, *expected_codes, msg: str = ""):
    """断言 HTTP 状态码"""
    codes = list(expected_codes)
    prefix = f"[{msg}] " if msg else ""
    assert resp.status_code in codes, (
        f"{prefix}期望状态码 {codes}，"
        f"实际 {resp.status_code}\n响应体: {resp.text[:500]}"
    )


def assert_field(resp, *fields):
    """断言响应 JSON 中存在指定字段"""
    data = resp.json()
    for field in fields:
        assert field in data, (
            f"响应缺少字段 '{field}'，实际字段: {list(data.keys())}"
        )


def assert_value(resp, field: str, expected, msg: str = ""):
    """断言响应 JSON 某字段值等于期望值"""
    data = resp.json()
    actual = data.get(field)
    prefix = f"[{msg}] " if msg else ""
    assert actual == expected, (
        f"{prefix}字段 '{field}' 期望 {expected!r}，"
        f"实际 {actual!r}\n完整响应: {data}"
    )


def assert_jsonpath(resp, path: str, expected, msg: str = ""):
    """
    用 JSONPath 断言深层嵌套字段
    示例：assert_jsonpath(resp, "$.status.value", "Active")
    """
    data = resp.json()
    results = jsonpath.jsonpath(data, path)
    prefix = f"[{msg}] " if msg else ""
    assert results, (
        f"{prefix}JSONPath '{path}' 未匹配到任何值，响应: {data}"
    )
    actual = results[0]
    assert actual == expected, (
        f"{prefix}JSONPath '{path}' 期望 {expected!r}，实际 {actual!r}"
    )


def assert_list_not_empty(resp, field: str = "pageItems"):
    """断言列表类响应不为空"""
    data = resp.json()
    items = data.get(field, [])
    assert isinstance(items, list) and len(items) > 0, (
        f"'{field}' 应为非空列表，实际: {items}"
    )


def assert_response_time(resp, max_seconds: float = 3.0):
    """断言接口响应时间不超过阈值"""
    elapsed = resp.elapsed.total_seconds()
    assert elapsed <= max_seconds, (
        f"接口响应时间 {elapsed:.2f}s 超过阈值 {max_seconds}s"
    )
