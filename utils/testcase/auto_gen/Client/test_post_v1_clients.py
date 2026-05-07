import pytest


class TestCreateClient:
    """测试创建客户接口"""

    base_payload = {
        "activationDate": "04 March 2009",
        "active": True,
        "address": [],
        "datatables": [],
        "dateFormat": "dd MMMM yyyy",
        "dateOfBirth": "01 January 2024",
        "emailAddress": "test@test.com",
        "externalId": "123",
        "firstname": "Client_FirstName",
        "fullname": "Client of group",
        "groupId": 1,
        "lastname": "Client_LastName",
        "legalFormId": 1,
        "locale": "en",
        "middlename": "Client_MiddleName",
        "mobileNo": "+353851239876",
        "officeId": 1
    }

    # 正常用例：使用所有字段，期望成功
    def test_create_client_success(self, api):
        """正常用例：使用完整字段创建客户，期望返回200"""
        payload = self.base_payload.copy()
        resp = api.post("/clients", json=payload)
        assert resp.status_code == 200
        assert "clientId" in resp.json()
        assert "officeId" in resp.json()
        assert "resourceId" in resp.json()

    # 参数缺失用例：逐个缺少 required_fields 中的字段（当前 required_fields 为空，故无缺失用例）
    # 边界值用例：空字符串、极大值、极小值、0、负数等
    @pytest.mark.parametrize("field, value, description", [
        ("firstname", "", "空字符串"),
        ("firstname", "a" * 256, "极大值（超长字符串）"),
        ("firstname", "a", "极小值（单字符）"),
        ("lastname", "", "空字符串"),
        ("lastname", "a" * 256, "极大值（超长字符串）"),
        ("lastname", "a", "极小值（单字符）"),
        ("middlename", "", "空字符串"),
        ("middlename", "a" * 256, "极大值（超长字符串）"),
        ("fullname", "", "空字符串"),
        ("fullname", "a" * 256, "极大值（超长字符串）"),
        ("emailAddress", "", "空字符串"),
        ("emailAddress", "a" * 256, "极大值（超长字符串）"),
        ("mobileNo", "", "空字符串"),
        ("mobileNo", "a" * 256, "极大值（超长字符串）"),
        ("externalId", "", "空字符串"),
        ("externalId", "a" * 256, "极大值（超长字符串）"),
        ("officeId", 0, "极小值0"),
        ("officeId", -1, "负数"),
        ("officeId", 999999999, "极大值"),
        ("groupId", 0, "极小值0"),
        ("groupId", -1, "负数"),
        ("groupId", 999999999, "极大值"),
        ("legalFormId", 0, "极小值0"),
        ("legalFormId", -1, "负数"),
        ("legalFormId", 999999999, "极大值"),
        ("active", "", "空字符串"),
        ("active", "true", "字符串而非布尔值"),
        ("active", 1, "整数而非布尔值"),
        ("dateOfBirth", "", "空字符串"),
        ("dateOfBirth", "invalid", "非法日期格式"),
        ("activationDate", "", "空字符串"),
        ("activationDate", "invalid", "非法日期格式"),
        ("locale", "", "空字符串"),
        ("locale", "invalid", "非法locale"),
        ("dateFormat", "", "空字符串"),
        ("dateFormat", "invalid", "非法日期格式"),
    ])
    def test_create_client_boundary_and_abnormal(self, api, field, value, description):
        """边界值/异常用例：测试字段的边界值和异常值，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/clients", json=payload)
        assert resp.status_code in [400, 403, 404, 422]

    # 异常用例：错误类型、非法枚举值、特殊字符等
    @pytest.mark.parametrize("field, value, description", [
        ("firstname", 123, "整数类型而非字符串"),
        ("firstname", None, "None值"),
        ("firstname", ["a"], "列表类型"),
        ("firstname", {"a": "b"}, "字典类型"),
        ("lastname", 123, "整数类型而非字符串"),
        ("lastname", None, "None值"),
        ("lastname", ["a"], "列表类型"),
        ("lastname", {"a": "b"}, "字典类型"),
        ("middlename", 123, "整数类型而非字符串"),
        ("middlename", None, "None值"),
        ("middlename", ["a"], "列表类型"),
        ("middlename", {"a": "b"}, "字典类型"),
        ("fullname", 123, "整数类型而非字符串"),
        ("fullname", None, "None值"),
        ("fullname", ["a"], "列表类型"),
        ("fullname", {"a": "b"}, "字典类型"),
        ("emailAddress", 123, "整数类型而非字符串"),
        ("emailAddress", None, "None值"),
        ("emailAddress", ["a"], "列表类型"),
        ("emailAddress", {"a": "b"}, "字典类型"),
        ("mobileNo", 123, "整数类型而非字符串"),
        ("mobileNo", None, "None值"),
        ("mobileNo", ["a"], "列表类型"),
        ("mobileNo", {"a": "b"}, "字典类型"),
        ("externalId", 123, "整数类型而非字符串"),
        ("externalId", None, "None值"),
        ("externalId", ["a"], "列表类型"),
        ("externalId", {"a": "b"}, "字典类型"),
        ("officeId", None, "None值"),
        ("officeId", "abc", "字符串类型而非整数"),
        ("officeId", [1], "列表类型"),
        ("officeId", {"a": 1}, "字典类型"),
        ("groupId", None, "None值"),
        ("groupId", "abc", "字符串类型而非整数"),
        ("groupId", [1], "列表类型"),
        ("groupId", {"a": 1}, "字典类型"),
        ("legalFormId", None, "None值"),
        ("legalFormId", "abc", "字符串类型而非整数"),
        ("legalFormId", [1], "列表类型"),
        ("legalFormId", {"a": 1}, "字典类型"),
        ("active", None, "None值"),
        ("active", [True], "列表类型"),
        ("active", {"a": True}, "字典类型"),
        ("dateOfBirth", 123, "整数类型而非字符串"),
        ("dateOfBirth", None, "None值"),
        ("dateOfBirth", ["a"], "列表类型"),
        ("dateOfBirth", {"a": "b"}, "字典类型"),
        ("activationDate", 123, "整数类型而非字符串"),
        ("activationDate", None, "None值"),
        ("activationDate", ["a"], "列表类型"),
        ("activationDate", {"a": "b"}, "字典类型"),
        ("locale", 123, "整数类型而非字符串"),
        ("locale", None, "None值"),
        ("locale", ["a"], "列表类型"),
        ("locale", {"a": "b"}, "字典类型"),
        ("dateFormat", 123, "整数类型而非字符串"),
        ("dateFormat", None, "None值"),
        ("dateFormat", ["a"], "列表类型"),
        ("dateFormat", {"a": "b"}, "字典类型"),
        ("address", None, "None值"),
        ("address", "abc", "字符串类型而非数组"),
        ("address", {"a": "b"}, "字典类型"),
        ("datatables", None, "None值"),
        ("datatables", "abc", "字符串类型而非数组"),
        ("datatables", {"a": "b"}, "字典类型"),
    ])
    def test_create_client_wrong_type(self, api, field, value, description):
        """异常用例：测试错误类型字段，期望返回4xx"""
        payload = self.base_payload.copy()
        payload[field] = value
        resp = api.post("/clients", json=payload)
        assert resp.status_code in [400, 403, 404, 422]