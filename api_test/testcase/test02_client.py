import allure
import pytest
import time

from api_test.common.api.client_api import ClientApi
from utils.assertion import (
    assert_status, assert_value, assert_jsonpath,
    assert_list_not_empty, assert_response_time,
)
from utils.db_helper import DBHelper

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


@allure.feature("客户管理")
class TestClient:

    @allure.story("查询客户详情")
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_get_client(self, client_api: ClientApi, client_id):
        """✅ 查询已创建客户，状态 Active + DB 验证"""
        res = client_api.get_detail(client_id)       # ← API 层

        assert_status(res, 200, msg="查询客户")
        assert_response_time(res, 3.0)
        assert_value(res, "id", client_id)
        assert_jsonpath(res, "$.status.value", "Active")

        with DBHelper() as db:
            db.assert_client_active(client_id)       # ← DB 校验

    @allure.story("查询客户列表")
    @pytest.mark.P1
    def test_list_clients(self, client_api: ClientApi):
        """✅ 列表分页结构验证"""
        res = client_api.list_clients(limit=5)       # ← API 层

        assert_status(res, 200)
        assert_list_not_empty(res, "pageItems")

    @allure.story("更新客户信息")
    @pytest.mark.P1
    def test_update_client(self, client_api: ClientApi, client_id):
        """✅ 更新后重新查询，验证字段已变更"""
        new_name = f"更新_{int(time.time())}"

        put_res = client_api.update(client_id, {  # ← API 层
            "firstname": new_name,
            "lastname": f"测试_{int(time.time())}",
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
        })
        assert_status(put_res, 200, msg="更新客户")

        get_res = client_api.get_detail(client_id)  # ← API 层
        assert_value(get_res, "firstname", new_name)

    @allure.story("查询不存在的客户")
    @pytest.mark.P2
    def test_get_nonexistent_client(self, client_api: ClientApi):
        """❌ 不存在的 ID 应返回 404"""
        res = client_api.get_detail(999999999)       # ← API 层
        assert_status(res, 404, msg="不存在的客户")

    @allure.story("创建客户-缺少必填字段")
    @pytest.mark.P2
    @pytest.mark.parametrize("missing_field,payload", [
        ("officeId",  {"firstname": "测", "lastname": "试",
                       "legalFormId": 1, "active": True,
                       "activationDate": "01 January 2023", **DATE_META}),
        ("firstname", {"officeId": 1, "lastname": "试",
                       "legalFormId": 1, "active": True,
                       "activationDate": "01 January 2023", **DATE_META}),
    ], ids=["缺officeId", "缺firstname"])
    def test_create_missing_field(self, client_api: ClientApi, missing_field, payload):
        """❌ 缺少必填字段应返回 4xx"""
        res = client_api.create(payload)             # ← API 层
        assert_status(res, 400, 403, 422, msg=f"缺少{missing_field}")