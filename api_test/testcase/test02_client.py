import pytest
from utils.db_helper import DBHelper


class TestCreateClient:
    """POST /clients"""

    def test_success(self, api, client_id):
        """✅ 正常查询已创建的客户（client_id 由 conftest fixture 创建）"""
        res = api.get(f"/clients/{client_id}")
        assert res.status_code == 200, f"查询失败: {res.text}"

        data = res.json()
        assert data["id"] == client_id
        assert data["firstname"] == "自动化"
        assert data["lastname"] == "测试客户"
        assert data["officeId"] == 1
        assert data["active"] is True

    def test_db_consistency(self, api, client_id):
        """✅ API 与数据库数据一致性验证"""
        api_res = api.get(f"/clients/{client_id}")
        assert api_res.status_code == 200
        api_data = api_res.json()

        with DBHelper() as db:
            db_data = db.verify_client_exists(client_id)

        assert api_data["firstname"] == db_data["firstname"], "firstname 不一致"
        assert api_data["lastname"] == db_data["lastname"], "lastname 不一致"
        assert api_data["id"] == db_data["id"], "id 不一致"
        assert db_data["status_enum"] == 300, \
            f"数据库状态应为 300(Active)，实际: {db_data['status_enum']}"

    def test_missing_firstname(self, api):
        """❌ 缺少必填字段 firstname"""
        res = api.post("/clients", json={
            "officeId": 1,
            "lastname": "测试",
            "active": False,
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
        })
        assert res.status_code in [400, 422], f"缺少 firstname 应返回错误，实际: {res.status_code}"

    def test_invalid_office(self, api):
        """❌ 不存在的 officeId"""
        res = api.post("/clients", json={
            "officeId": 999999,
            "firstname": "测试",
            "lastname": "客户",
            "active": False,
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
        })
        assert res.status_code in [400, 404]

    @pytest.mark.parametrize("firstname, desc", [
        ("",           "空字符串"),
        ("A" * 300,    "超长名称"),
        ("<script>",   "特殊字符"),
    ])
    def test_invalid_firstname(self, api, firstname, desc):
        """❌ firstname 边界值"""
        res = api.post("/clients", json={
            "officeId": 1,
            "firstname": firstname,
            "lastname": "测试",
            "active": False,
            "dateFormat": "dd MMMM yyyy",
            "locale": "en",
        })
        assert res.status_code in [400, 422], f"{desc} 应返回验证错误"


class TestGetClient:
    """GET /clients/{clientId}"""

    def test_get_existing(self, api, client_id):
        """✅ 查询存在的客户"""
        res = api.get(f"/clients/{client_id}")
        assert res.status_code == 200
        assert res.json()["id"] == client_id

    def test_get_nonexistent(self, api):
        """❌ 查询不存在的客户"""
        res = api.get("/clients/999999")
        assert res.status_code == 404