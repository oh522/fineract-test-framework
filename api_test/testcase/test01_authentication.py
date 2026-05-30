import allure
import pytest
import yaml
from pathlib import Path

from api_test.common.api.auth_api import AuthApi
from utils.assertion import assert_status, assert_field
from utils.db_helper import DBHelper

_cases = yaml.safe_load(
    (Path(__file__).parents[1] / "common/data/auth_cases.yaml")
    .read_text(encoding="utf-8")
)["failure_cases"]


@allure.feature("认证模块")
class TestAuthentication:

    @allure.story("正常登录")
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_login_success(self, auth_api: AuthApi):
        """✅ 正常登录：token 字段存在 + DB 用户未删除"""
        res = auth_api.login("mifos", "password")   # ← API 层

        assert_status(res, 200, msg="正常登录")
        assert_field(res, "base64EncodedAuthenticationKey", "userId", "authenticated")

        with DBHelper() as db:
            db.assert_user_exists("mifos")           # ← DB 校验

    @allure.story("异常登录")
    @pytest.mark.P1
    @pytest.mark.parametrize(
        "username, password, expected_codes",
        [(c["username"], c["password"], c["expected_codes"]) for c in _cases],
        ids=[c["id"] for c in _cases],
    )
    def test_login_failure(self, auth_api: AuthApi, username, password, expected_codes):
        """❌ 异常场景：从 auth_cases.yaml 数据驱动"""
        res = auth_api.login(username, password)     # ← API 层
        assert_status(res, *expected_codes, msg=f"异常登录[{username}]")

    @allure.story("缺少密码字段")
    @pytest.mark.P2
    def test_login_missing_password(self, auth_api: AuthApi):
        """❌ 缺少 password 字段"""
        res = auth_api.login_with_missing_field("mifos")  # ← API 层
        assert_status(res, 400, 401, 500)