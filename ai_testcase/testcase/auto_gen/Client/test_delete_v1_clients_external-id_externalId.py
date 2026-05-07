import pytest


class TestDeleteClient:
    """删除客户端接口测试类"""

    # 正常用例
    @pytest.mark.parametrize("external_id", [
        "valid-client-123",
        "client_abc_456",
        "test-client-001",
        "CLIENT-2024-001",
    ])
    def test_delete_client_success(self, api, external_id):
        """正常用例：使用有效的 externalId 删除客户端，期望成功"""
        resp = api.delete(f"/clients/external-id/{external_id}")
        assert resp.status_code == 200
        response_data = resp.json()
        assert response_data is not None
        assert "resourceId" in response_data
        assert response_data["resourceId"] is not None

    # 参数缺失用例
    @pytest.mark.parametrize("external_id", [
        None,
        "",
        "   ",
    ])
    def test_delete_client_missing_parameter(self, api, external_id):
        """参数缺失用例：externalId 为空或 None，期望返回 400 或 404"""
        if external_id is None:
            resp = api.delete("/clients/external-id/")
        else:
            resp = api.delete(f"/clients/external-id/{external_id}")
        assert resp.status_code in [400, 404]
        response_data = resp.json()
        assert response_data is not None
        assert "error" in response_data or "message" in response_data

    # 边界值用例
    @pytest.mark.parametrize("external_id", [
        "a" * 255,          # 极大值：255 个字符
        "a" * 1000,         # 极大值：1000 个字符
        "a",                # 极小值：1 个字符
        "a" * 0,            # 空字符串（边界）
        "12345678901234567890",  # 20 位数字
        "a" * 256,          # 超过常见限制 255 字符
    ])
    def test_delete_client_boundary(self, api, external_id):
        """边界值用例：测试 externalId 的边界情况"""
        resp = api.delete(f"/clients/external-id/{external_id}")
        # 根据实际业务逻辑，边界值可能成功或失败，这里断言状态码在合理范围内
        assert resp.status_code in [200, 400, 404, 413]
        response_data = resp.json()
        assert response_data is not None
        if resp.status_code == 200:
            assert "resourceId" in response_data
            assert response_data["resourceId"] is not None
        else:
            assert "error" in response_data or "message" in response_data

    # 异常用例
    @pytest.mark.parametrize("external_id", [
        "invalid-client-id-!@#$%^&*()",  # 特殊字符
        "client id with spaces",         # 包含空格
        "中文客户端ID",                   # 中文字符
        "client\nid",                    # 包含换行符
        "client\tid",                    # 包含制表符
        "client/id",                     # 包含斜杠
        "client?id=1",                   # 包含问号
        "client#id",                     # 包含井号
        "client&id",                     # 包含 & 符号
        "client=id",                     # 包含等号
        "client%id",                     # 包含百分号
        "client+id",                     # 包含加号
        "client@id",                     # 包含 @ 符号
        "client:id",                     # 包含冒号
        "client;id",                     # 包含分号
        "client,id",                     # 包含逗号
        "client.id",                     # 包含点号（可能合法，但作为异常测试）
        "client~id",                     # 包含波浪号
        "client`id",                     # 包含反引号
        "client'id",                     # 包含单引号
        'client"id',                     # 包含双引号
        "client<id",                     # 包含小于号
        "client>id",                     # 包含大于号
        "client|id",                     # 包含竖线
        "client\\id",                    # 包含反斜杠
        "client[id",                     # 包含左方括号
        "client]id",                     # 包含右方括号
        "client{id",                     # 包含左花括号
        "client}id",                     # 包含右花括号
        "client(id",                     # 包含左括号
        "client)id",                     # 包含右括号
    ])
    def test_delete_client_invalid_parameter(self, api, external_id):
        """异常用例：使用包含特殊字符或非法值的 externalId，期望返回 400 或 404"""
        resp = api.delete(f"/clients/external-id/{external_id}")
        assert resp.status_code in [400, 404]
        response_data = resp.json()
        assert response_data is not None
        assert "error" in response_data or "message" in response_data

    # 额外异常用例：错误类型
    @pytest.mark.parametrize("external_id", [
        12345,           # 整数类型
        3.14159,         # 浮点数类型
        True,            # 布尔类型
        [1, 2, 3],       # 列表类型
        {"key": "value"}, # 字典类型
        None,            # None 类型
    ])
    def test_delete_client_wrong_type(self, api, external_id):
        """异常用例：externalId 为错误数据类型，期望返回 400 或 404"""
        resp = api.delete(f"/clients/external-id/{external_id}")
        assert resp.status_code in [400, 404]
        response_data = resp.json()
        assert response_data is not None
        assert "error" in response_data or "message" in response_data