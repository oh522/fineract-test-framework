from utils.db_helper import DBHelper


def test_login_success(api):
    """登录成功"""
    res = api.post("/authentication", json={
        "username": "mifos",
        "password": "password"
    })

    assert res.status_code == 200, f"登录失败: {res.text}"
    assert "base64EncodedAuthenticationKey" in res.json()
    with DBHelper() as db:
        result = db.query_one("SELECT COUNT(*) as total FROM m_appuser WHERE username = 'mifos'")
        assert result['total'] == 1



