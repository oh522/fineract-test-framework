import pytest


class TestSavingsAccounts:
    """Savings Account API tests"""

    BASE_PATH = "/savingsaccounts"

    # 正常用例：使用所有字段，期望成功
    @pytest.mark.parametrize(
        "payload",
        [
            {
                "clientId": 1,
                "dateFormat": "dd MMMM yyyy",
                "externalId": "123",
                "locale": "en",
                "productId": 1,
                "submittedOnDate": "01 March 2011"
            }
        ]
    )
    def test_submit_savings_application_success(self, api, payload):
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code == 200
        assert "resourceId" in resp.json()

    # 参数缺失用例：逐个缺少必填字段（clientId, productId, submittedOnDate）
    @pytest.mark.parametrize(
        "missing_field",
        [
            "clientId",
            "productId",
            "submittedOnDate"
        ]
    )
    def test_submit_savings_application_missing_required_field(self, api, missing_field):
        payload = {
            "clientId": 1,
            "dateFormat": "dd MMMM yyyy",
            "externalId": "123",
            "locale": "en",
            "productId": 1,
            "submittedOnDate": "01 March 2011"
        }
        payload.pop(missing_field)
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 边界值用例：空字符串、极大值、极小值、0、负数
    @pytest.mark.parametrize(
        "field, value",
        [
            ("clientId", ""),
            ("clientId", 0),
            ("clientId", -1),
            ("clientId", 999999999999999999999999999999),
            ("productId", ""),
            ("productId", 0),
            ("productId", -1),
            ("productId", 999999999999999999999999999999),
            ("submittedOnDate", ""),
            ("submittedOnDate", "01 Jan 1900"),
            ("submittedOnDate", "01 Jan 2100"),
            ("externalId", ""),
            ("externalId", "a" * 1000),
            ("dateFormat", ""),
            ("dateFormat", "invalid_format"),
            ("locale", ""),
            ("locale", "invalid_locale")
        ]
    )
    def test_submit_savings_application_boundary_values(self, api, field, value):
        payload = {
            "clientId": 1,
            "dateFormat": "dd MMMM yyyy",
            "externalId": "123",
            "locale": "en",
            "productId": 1,
            "submittedOnDate": "01 March 2011"
        }
        payload[field] = value
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：错误类型、非法枚举值、特殊字符
    @pytest.mark.parametrize(
        "field, value",
        [
            ("clientId", "not_a_number"),
            ("clientId", 1.5),
            ("clientId", None),
            ("clientId", [1, 2, 3]),
            ("clientId", {"key": "value"}),
            ("productId", "not_a_number"),
            ("productId", 1.5),
            ("productId", None),
            ("productId", [1, 2, 3]),
            ("productId", {"key": "value"}),
            ("submittedOnDate", 12345),
            ("submittedOnDate", None),
            ("submittedOnDate", ["01", "March", "2011"]),
            ("submittedOnDate", {"date": "01 March 2011"}),
            ("externalId", None),
            ("externalId", 12345),
            ("externalId", ["123"]),
            ("externalId", {"id": "123"}),
            ("dateFormat", 12345),
            ("dateFormat", None),
            ("dateFormat", ["dd", "MMMM", "yyyy"]),
            ("dateFormat", {"format": "dd MMMM yyyy"}),
            ("locale", 12345),
            ("locale", None),
            ("locale", ["en"]),
            ("locale", {"lang": "en"})
        ]
    )
    def test_submit_savings_application_invalid_types(self, api, field, value):
        payload = {
            "clientId": 1,
            "dateFormat": "dd MMMM yyyy",
            "externalId": "123",
            "locale": "en",
            "productId": 1,
            "submittedOnDate": "01 March 2011"
        }
        payload[field] = value
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：不存在的资源ID
    def test_submit_savings_application_nonexistent_client(self, api):
        payload = {
            "clientId": 999999,
            "dateFormat": "dd MMMM yyyy",
            "externalId": "123",
            "locale": "en",
            "productId": 1,
            "submittedOnDate": "01 March 2011"
        }
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    def test_submit_savings_application_nonexistent_product(self, api):
        payload = {
            "clientId": 1,
            "dateFormat": "dd MMMM yyyy",
            "externalId": "123",
            "locale": "en",
            "productId": 999999,
            "submittedOnDate": "01 March 2011"
        }
        resp = api.post(self.BASE_PATH, json=payload)
        assert resp.status_code in [400, 403, 404, 422]