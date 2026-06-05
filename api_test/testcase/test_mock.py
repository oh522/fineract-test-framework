"""
Mock 测试（
第一种：responses 库拦截请求（适合测试环境不稳定/第三方未开发完）
第二种：pytest-mock / unittest.mock（适合单元测试）
"""
import pytest
import responses as resp_mock
from unittest.mock import patch, MagicMock

from api_test.common.base_api import BaseApi


# ─── 第一种：responses 库（拦截 HTTP 请求） ───────────────────

class TestWithResponsesMock:

    @resp_mock.activate
    def test_login_mock(self):
        """
        Mock 登录接口：
        适用场景 — Fineract 环境不可用时，用预设数据验证测试逻辑是否正确
        """
        # 注册 Mock 响应
        resp_mock.add(
            resp_mock.POST,
            "https://localhost:8443/fineract-provider/api/v1/authentication",
            json={
                "userId": 1,
                "username": "mifos",
                "base64EncodedAuthenticationKey": "bWlmb3M6cGFzc3dvcmQ=",
                "authenticated": True,
            },
            status=200,
        )

        api = BaseApi()
        res = api.post("/authentication", json={"username": "mifos", "password": "password"})

        assert res.status_code == 200
        assert res.json()["authenticated"] is True
        assert len(resp_mock.calls) == 1  # 验证确实发出了一次请求

    @resp_mock.activate
    def test_server_error_mock(self):
        """Mock 服务器 500 错误，验证客户端异常处理逻辑"""
        resp_mock.add(
            resp_mock.GET,
            "https://localhost:8443/fineract-provider/api/v1/clients/1",
            json={"errors": [{"developerMessage": "Internal Server Error"}]},
            status=500,
        )
        api = BaseApi()
        res = api.get("/clients/1")
        assert res.status_code == 500

    @resp_mock.activate
    def test_timeout_simulation(self):
        """Mock 超时场景"""
        import requests
        resp_mock.add(
            resp_mock.POST,
            "https://localhost:8443/fineract-provider/api/v1/loans",
            body=requests.exceptions.Timeout("连接超时"),
        )
        api = BaseApi()
        with pytest.raises((TimeoutError, Exception)):
            api.post("/loans", json={})


# ─── 第二种：unittest.mock（Mock 内部依赖，如 DBHelper） ──────

class TestWithUnitMock:

    def test_login_db_verify_with_mock(self, api):
        """
        Mock 数据库查询：
        适用场景 — 不想真正连数据库时，验证测试用例逻辑是否正确
        """
        # 真实调用接口，但 Mock 掉数据库部分
        res = api.post("/authentication", json={"username": "mifos", "password": "password"})
        assert res.status_code == 200

        mock_row = {"is_deleted": 0, "username": "mifos"}

        with patch("utils.db_helper.DBHelper") as MockDB:
            # 设置 Mock 返回值
            mock_instance = MockDB.return_value.__enter__.return_value
            mock_instance.query_one.return_value = mock_row

            from utils.db_helper import DBHelper
            with DBHelper() as db:
                row = db.query_one("SELECT * FROM m_appuser WHERE username = %s", ("mifos",))
                assert row["is_deleted"] == 0

    def test_api_with_mock_session(self):
        """Mock requests.Session，完全隔离网络"""
        with patch("requests.Session") as mock_session_cls:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.ok = True
            mock_resp.json.return_value = {
                "userId": 1,
                "authenticated": True,
                "base64EncodedAuthenticationKey": "xxx",
            }
            mock_resp.elapsed.total_seconds.return_value = 0.1
            mock_resp.text = '{"userId":1}'

            mock_session = MagicMock()
            mock_session.request.return_value = mock_resp
            mock_session_cls.return_value = mock_session

            api = BaseApi()
            res = api.post("/authentication", json={"username": "mifos", "password": "password"})
            assert res.status_code == 200
            assert res.json()["authenticated"] is True