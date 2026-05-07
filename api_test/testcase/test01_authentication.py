from utils.db_helper import DBHelper


class TestAuthentication:

    def test_login_success(self, api):
        """✅ 正常登录"""
        res = api.post("/authentication", json={
            "username": "mifos",
            "password": "password"
        })
        assert res.status_code == 200, f"登录失败: {res.text}"

        data = res.json()
        assert "base64EncodedAuthenticationKey" in data, "响应缺少 token"
        assert "userId" in data, "响应缺少 userId"

        # 数据库验证：用户确实存在
        with DBHelper() as db:
            result = db.query_one(
                "SELECT COUNT(*) as total FROM m_appuser WHERE username = 'mifos'"
            )
            assert result["total"] == 1, "数据库中不存在该用户"

    def test_login_wrong_password(self, api):
        """❌ 密码错误"""
        res = api.post("/authentication", json={
            "username": "mifos",
            "password": "wrong_password"
        })
        assert res.status_code in [401, 403], f"错误密码应返回401/403，实际: {res.status_code}"

    def test_login_nonexistent_user(self, api):
        """❌ 用户不存在"""
        res = api.post("/authentication", json={
            "username": "not_exist_user_999",
            "password": "password"
        })
        assert res.status_code in [401, 403]

    def test_login_missing_password(self, api):
        """❌ 缺少密码字段"""
        res = api.post("/authentication", json={"username": "mifos"})
        assert res.status_code in [400, 401, 500]

    def test_login_empty_credentials(self, api):
        """❌ 空用户名和密码"""
        res = api.post("/authentication", json={
            "username": "",
            "password": ""
        })
        assert res.status_code in [400, 401]