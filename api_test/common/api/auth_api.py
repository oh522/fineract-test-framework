from api_test.common.base_api import BaseApi


class AuthApi(BaseApi):
    """认证接口封装 — 每个接口对应一个方法，语义清晰"""

    def login(self, username: str, password: str):
        return self.post("/authentication", json={
            "username": username,
            "password": password,
        })

    def login_with_missing_field(self, username: str):
        """缺少 password 字段的异常场景"""
        return self.post("/authentication", json={"username": username})