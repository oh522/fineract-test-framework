"""
统一断言工具 — 封装常用断言，失败时输出详细信息
"""


def assert_status(resp, *expected_codes, msg: str = ""):
    """断言响应状态码"""
    codes = list(expected_codes)
    assert resp.status_code in codes, (
        f"{'[' + msg + '] ' if msg else ''}"
        f"期望状态码 {codes}，实际 {resp.status_code}\n"
        f"响应体: {resp.text[:500]}"
    )


def assert_field(resp, *fields):
    """断言响应 JSON 中包含指定字段"""
    data = resp.json()
    for field in fields:
        assert field in data, f"响应缺少字段 '{field}'，实际响应: {data}"


def assert_value(resp, field: str, expected):
    """断言响应 JSON 中某字段值等于期望值"""
    data = resp.json()
    actual = data.get(field)
    assert actual == expected, (
        f"字段 '{field}' 期望 {expected!r}，实际 {actual!r}\n响应: {data}"
    )

