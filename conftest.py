import pytest
from api_test.common.base_api import BaseApi
# 全局共享的 BaseApi 实例
_api_instance = BaseApi()

@pytest.fixture(scope="session", autouse=True)
def api():
    """提供全局 BaseApi 实例"""
    return _api_instance

@pytest.fixture(scope="session")
def auth_session():
    """全局登录，自动应用于所有测试"""
    resp = _api_instance.post("/authentication", json={
        "username": "mifos",
        "password": "password",
        "tenantId": "default"
    })

    assert resp.status_code == 200, f"登录失败：{resp.text}"
    token = resp.json().get("base64EncodedAuthenticationKey")
    assert token, f"未获取到 token：{resp.json()}"
    # ✅ 用实例的 _session，不用类的
    _api_instance._session.headers.update({
        "Authorization": f"Basic {token}"
    })
    print(f"\n✅ 全局登录成功，token：{token[:16]}...")