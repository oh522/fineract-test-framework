import pytest
from api_test.common.base_api import BaseApi

class TestCreateOffice:
    # 正常用例：使用所有字段创建办公室，期望成功
    def test_create_office_success(self, api):
        payload = {
            "dateFormat": "dd MMMM yyyy",
            "externalId": "SYS54-88",
            "locale": "en",
            "name": "Good Friday",
            "openingDate": "01 January 2024",
            "parentId": 2
        }
        resp = api.post("/v1/offices", json=payload)
        assert resp.status_code == 200
        assert "officeId" in resp.json()
        assert "resourceId" in resp.json()

    # 参数缺失用例：逐个缺少字段，期望失败
    @pytest.mark.parametrize("missing_field", [
        "dateFormat",
        "externalId",
        "locale",
        "name",
        "openingDate",
        "parentId"
    ])
    def test_create_office_missing_fields(self, api, missing_field):
        payload = {
            "dateFormat": "dd MMMM yyyy",
            "externalId": "SYS54-88",
            "locale": "en",
            "name": "Good Friday",
            "openingDate": "01 January 2024",
            "parentId": 2
        }
        del payload[missing_field]
        resp = api.post("/v1/offices", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：测试各种边界值情况
    @pytest.mark.parametrize("field,value,expected_status", [
        # 空字符串测试
        ("name", "", 400),
        ("externalId", "", 400),
        ("dateFormat", "", 400),
        ("locale", "", 400),
        ("openingDate", "", 400),
        # 极大值测试
        ("name", "A" * 1000, 400),
        ("externalId", "B" * 500, 400),
        # 极小值测试
        ("parentId", 0, 400),
        ("parentId", -1, 400),
        # 特殊字符测试
        ("name", "Office@#$%^&*()", 200),
        ("externalId", "EXT-123!@#", 200),
        # 日期格式边界
        ("openingDate", "31 December 2024", 200),
        ("openingDate", "01 January 1900", 200),
    ])
    def test_create_office_boundary_values(self, api, field, value, expected_status):
        payload = {
            "dateFormat": "dd MMMM yyyy",
            "externalId": "SYS54-88",
            "locale": "en",
            "name": "Good Friday",
            "openingDate": "01 January 2024",
            "parentId": 2
        }
        payload[field] = value
        resp = api.post("/v1/offices", json=payload)
        assert resp.status_code == expected_status

    # 异常用例：测试错误类型和非法值
    @pytest.mark.parametrize("field,value,expected_status", [
        # 错误类型测试
        ("parentId", "not_a_number", 400),
        ("parentId", None, 400),
        ("openingDate", 12345, 400),
        ("name", 12345, 400),
        # 非法枚举值测试
        ("locale", "invalid_locale", 400),
        ("dateFormat", "invalid_format", 400),
        # 特殊字符和注入测试
        ("name", "<script>alert('xss')</script>", 400),
        ("externalId", "'; DROP TABLE offices; --", 400),
        # 不存在的父ID
        ("parentId", 999999, 400),
        # 无效日期格式
        ("openingDate", "2024-01-0