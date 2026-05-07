import pytest


class TestCreditBureauConfigurationMappings:
    BASE_PATH = "/CreditBureauConfiguration/mappings"

    @pytest.mark.parametrize("payload, expected_status, expected_msg", [
        # 正常用例：有效字符串参数
        ({"content": {"application/json": {"schema": {"type": "string"}}}}, 200, "success"),
        # 正常用例：包含额外字段（系统应忽略）
        ({"content": {"application/json": {"schema": {"type": "string"}}}, "extra": "value"}, 200, "success"),
    ])
    def test_normal_cases(self, api, payload, expected_status, expected_msg):
        """正常用例：正确参数，期望成功"""
        resp = api.put(self.BASE_PATH, json=payload)
        assert resp.status_code == expected_status
        assert resp.json().get("message") == expected_msg or resp.json().get("status") == "ok"

    @pytest.mark.parametrize("payload, expected_status, expected_error", [
        # 参数缺失：缺少 content 字段
        ({}, 400, "content is required"),
        # 参数缺失：content 缺少 application/json
        ({"content": {}}, 400, "application/json is required"),
        # 参数缺失：application/json 缺少 schema
        ({"content": {"application/json": {}}}, 400, "schema is required"),
        # 参数缺失：schema 缺少 type
        ({"content": {"application/json": {"schema": {}}}}, 400, "type is required"),
    ])
    def test_missing_parameters(self, api, payload, expected_status, expected_error):
        """参数缺失用例：缺少必填字段"""
        resp = api.put(self.BASE_PATH, json=payload)
        assert resp.status_code == expected_status
        assert expected_error in resp.text or expected_error in str(resp.json())

    @pytest.mark.parametrize("payload, expected_status, expected_error", [
        # 边界值：空字符串 type
        ({"content": {"application/json": {"schema": {"type": ""}}}}, 400, "invalid type"),
        # 边界值：超长字符串 type（假设限制 255 字符）
        ({"content": {"application/json": {"schema": {"type": "a" * 256}}}}, 400, "type too long"),
        # 边界值：极小值（空对象）
        ({"content": {"application/json": {"schema": {"type": "string"}}}}, 200, "success"),
        # 边界值：type 为 null
        ({"content": {"application/json": {"schema": {"type": None}}}}, 400, "type cannot be null"),
    ])
    def test_boundary_values(self, api, payload, expected_status, expected_error):
        """边界值用例：极大值、极小值、空字符串等"""
        resp = api.put(self.BASE_PATH, json=payload)
        assert resp.status_code == expected_status
        if expected_status != 200:
            assert expected_error in resp.text or expected_error in str(resp.json())

    @pytest.mark.parametrize("payload, expected_status, expected_error", [
        # 异常用例：type 为数字
        ({"content": {"application/json": {"schema": {"type": 123}}}}, 400, "invalid type"),
        # 异常用例：type 为布尔值
        ({"content": {"application/json": {"schema": {"type": True}}}}, 400, "invalid type"),
        # 异常用例：type 为数组
        ({"content": {"application/json": {"schema": {"type": ["string"]}}}}, 400, "invalid type"),
        # 异常用例：type 为对象
        ({"content": {"application/json": {"schema": {"type": {"key": "value"}}}}}, 400, "invalid type"),
        # 异常用例：非法 type 值
        ({"content": {"application/json": {"schema": {"type": "invalid_type"}}}}, 400, "unsupported type"),
        # 异常用例：请求体为列表
        ([{"content": {"application/json": {"schema": {"type": "string"}}}}], 400, "invalid request format"),
        # 异常用例：请求体为字符串
        ("invalid", 400, "invalid request format"),
    ])
    def test_exception_cases(self, api, payload, expected_status, expected_error):
        """异常用例：错误类型、非法值"""
        resp = api.put(self.BASE_PATH, json=payload)
        assert resp.status_code == expected_status
        assert expected_error in resp.text or expected_error in str(resp.json())