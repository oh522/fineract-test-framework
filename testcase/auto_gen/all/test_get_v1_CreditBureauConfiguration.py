import pytest


class TestCreditBureauConfiguration:
    """
    征信机构配置查询接口测试
    接口路径: /v1/CreditBureauConfiguration
    方法: GET
    """

    # ==================== 正常用例 ====================

    @pytest.mark.parametrize("params, desc", [
        ({}, "无参数查询"),
        ({"page": 1, "size": 10}, "带分页参数查询"),
        ({"name": "央行征信"}, "按名称查询"),
        ({"status": "ACTIVE"}, "按状态查询"),
    ])
    def test_normal_query(self, api, params, desc):
        """
        正常用例：使用正确参数查询，期望成功返回
        """
        resp = api.get("/CreditBureauConfiguration", params=params)
        assert resp.status_code == 200
        assert resp.json() is not None
        # 验证响应为字符串类型（根据schema定义）
        assert isinstance(resp.json(), str)

    # ==================== 参数缺失用例 ====================

    @pytest.mark.parametrize("params, desc", [
        (None, "参数为None"),
        ("", "参数为空字符串"),
        ({"page": None}, "page参数为None"),
        ({"size": None}, "size参数为None"),
    ])
    def test_missing_params(self, api, params, desc):
        """
        参数缺失用例：缺少必填字段或参数为None，期望返回400或合理错误
        """
        resp = api.get("/CreditBureauConfiguration", params=params)
        # 根据实际接口行为，可能返回400或默认结果
        assert resp.status_code in [200, 400]
        if resp.status_code == 400:
            assert "error" in resp.text or "message" in resp.text

    # ==================== 边界值用例 ====================

    @pytest.mark.parametrize("params, desc", [
        ({"page": 0}, "page为极小值0"),
        ({"page": -1}, "page为负数"),
        ({"page": 999999999}, "page为极大值"),
        ({"size": 0}, "size为极小值0"),
        ({"size": -1}, "size为负数"),
        ({"size": 10000}, "size为极大值"),
        ({"name": ""}, "name为空字符串"),
        ({"name": "a" * 1000}, "name为超长字符串"),
        ({"status": ""}, "status为空字符串"),
    ])
    def test_boundary_params(self, api, params, desc):
        """
        边界值用例：测试参数的边界情况，期望接口能正确处理
        """
        resp = api.get("/CreditBureauConfiguration", params=params)
        assert resp.status_code in [200, 400]
        if resp.status_code == 200:
            assert isinstance(resp.json(), str)
        elif resp.status_code == 400:
            assert "error" in resp.text or "message" in resp.text

    # ==================== 异常用例 ====================

    @pytest.mark.parametrize("params, desc", [
        ({"page": "abc"}, "page为字符串类型"),
        ({"page": 1.5}, "page为浮点数"),
        ({"page": True}, "page为布尔值"),
        ({"page": [1, 2]}, "page为列表"),
        ({"page": {"key": "value"}}, "page为字典"),
        ({"size": "abc"}, "size为字符串类型"),
        ({"size": 1.5}, "size为浮点数"),
        ({"size": True}, "size为布尔值"),
        ({"name": 123}, "name为数字类型"),
        ({"name": True}, "name为布尔值"),
        ({"name": None}, "name为None"),
        ({"status": 123}, "status为数字类型"),
        ({"status": True}, "status为布尔值"),
        ({"status": None}, "status为None"),
        ({"unknown_param": "value"}, "传入未定义参数"),
    ])
    def test_invalid_params(self, api, params, desc):
        """
        异常用例：传入非法参数类型或值，期望返回400或合理错误
        """
        resp = api.get("/CreditBureauConfiguration", params=params)
        assert resp.status_code in [200, 400, 422]
        if resp.status_code == 400 or resp.status_code == 422:
            assert "error" in resp.text or "message" in resp.text or "detail" in resp.text
        elif resp.status_code == 200:
            # 如果接口容错返回200，验证响应格式
            assert isinstance(resp.json(), str)

    # ==================== 额外异常场景 ====================

    @pytest.mark.parametrize("headers, desc", [
        ({"Content-Type": "application/xml"}, "错误的Content-Type"),
        ({"Authorization": "Bearer invalid_token"}, "无效的认证token"),
        ({"Accept": "text/html"}, "不支持的Accept类型"),
    ])
    def test_invalid_headers(self, api, headers, desc):
        """
        异常用例：使用无效的请求头，期望返回401或406等错误
        """
        resp = api.get("/CreditBureauConfiguration", headers=headers)
        assert resp.status_code in [200, 401, 406, 415]
        if resp.status_code != 200:
            assert "error" in resp.text or "message" in resp.text

    def test_method_not_allowed(self, api):
        """
        异常用例：使用POST方法请求GET接口，期望返回405
        """
        resp = api.post("/CreditBureauConfiguration", json={})
        assert resp.status_code == 405
        assert "error" in resp.text or "message" in resp.text

    def test_empty_response(self, api):
        """
        异常用例：模拟空响应场景，验证接口稳定性
        """
        # 使用不存在的子路径
        resp = api.get("/CreditBureauConfiguration/invalid")
        assert resp.status_code in [404, 405]
        assert "error" in resp.text or "message" in resp.text