import pytest


class TestListLoans:
    """List Loans 接口测试类"""

    BASE_PATH = "/loans"

    @pytest.mark.parametrize("query_params", [
        {},
        {"offset": 0, "limit": 10},
        {"offset": 0, "limit": 10, "orderBy": "id", "sortOrder": "ASC"},
        {"clientId": 1},
        {"status": "active"},
        {"accountNo": "LN-001"},
        {"externalId": "ext-001"},
        {"associations": "all"},
    ])
    def test_list_loans_success(self, api, query_params):
        """正常用例：使用各种合法查询参数组合，期望成功返回200"""
        resp = api.get(self.BASE_PATH, params=query_params)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list) or isinstance(resp.json(), dict)

    @pytest.mark.parametrize("missing_param", [
        "offset",
        "limit",
        "orderBy",
        "sortOrder",
        "clientId",
        "status",
        "accountNo",
        "externalId",
        "associations",
    ])
    def test_list_loans_missing_optional_param(self, api, missing_param):
        """参数缺失用例：逐个缺失可选参数，期望成功（因为所有参数都是可选的）"""
        params = {
            "offset": 0,
            "limit": 10,
            "orderBy": "id",
            "sortOrder": "ASC",
            "clientId": 1,
            "status": "active",
            "accountNo": "LN-001",
            "externalId": "ext-001",
            "associations": "all",
        }
        params.pop(missing_param, None)
        resp = api.get(self.BASE_PATH, params=params)
        assert resp.status_code == 200

    @pytest.mark.parametrize("offset", [-1, 0, 1, 999999])
    def test_list_loans_offset_boundary(self, api, offset):
        """边界值用例：offset边界值测试"""
        resp = api.get(self.BASE_PATH, params={"offset": offset, "limit": 10})
        assert resp.status_code == 200

    @pytest.mark.parametrize("limit", [-1, 0, 1, 10000, 999999])
    def test_list_loans_limit_boundary(self, api, limit):
        """边界值用例：limit边界值测试"""
        resp = api.get(self.BASE_PATH, params={"offset": 0, "limit": limit})
        assert resp.status_code == 200

    @pytest.mark.parametrize("client_id", [0, -1, 999999, 2**63 - 1])
    def test_list_loans_client_id_boundary(self, api, client_id):
        """边界值用例：clientId边界值测试"""
        resp = api.get(self.BASE_PATH, params={"clientId": client_id})
        assert resp.status_code == 200

    @pytest.mark.parametrize("status", ["", "invalid_status", "active", "closed", "overpaid"])
    def test_list_loans_status_boundary(self, api, status):
        """边界值用例：status边界值测试"""
        resp = api.get(self.BASE_PATH, params={"status": status})
        assert resp.status_code == 200

    @pytest.mark.parametrize("sort_order", ["", "ASC", "DESC", "asc", "desc", "INVALID"])
    def test_list_loans_sort_order_boundary(self, api, sort_order):
        """边界值用例：sortOrder边界值测试"""
        resp = api.get(self.BASE_PATH, params={"sortOrder": sort_order, "orderBy": "id"})
        assert resp.status_code == 200

    @pytest.mark.parametrize("order_by", ["", "id", "accountNo", "INVALID", "createdDate"])
    def test_list_loans_order_by_boundary(self, api, order_by):
        """边界值用例：orderBy边界值测试"""
        resp = api.get(self.BASE_PATH, params={"orderBy": order_by, "sortOrder": "ASC"})
        assert resp.status_code == 200

    @pytest.mark.parametrize("account_no", ["", "LN-001", "INVALID", "12345678901234567890"])
    def test_list_loans_account_no_boundary(self, api, account_no):
        """边界值用例：accountNo边界值测试"""
        resp = api.get(self.BASE_PATH, params={"accountNo": account_no})
        assert resp.status_code == 200

    @pytest.mark.parametrize("external_id", ["", "ext-001", "INVALID", "12345678901234567890"])
    def test_list_loans_external_id_boundary(self, api, external_id):
        """边界值用例：externalId边界值测试"""
        resp = api.get(self.BASE_PATH, params={"externalId": external_id})
        assert resp.status_code == 200

    @pytest.mark.parametrize("associations", ["", "all", "INVALID", "repaymentSchedule", "transactions"])
    def test_list_loans_associations_boundary(self, api, associations):
        """边界值用例：associations边界值测试"""
        resp = api.get(self.BASE_PATH, params={"associations": associations})
        assert resp.status_code == 200

    @pytest.mark.parametrize("offset", ["abc", 1.5, None, True])
    def test_list_loans_offset_invalid_type(self, api, offset):
        """异常用例：offset错误类型"""
        resp = api.get(self.BASE_PATH, params={"offset": offset, "limit": 10})
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("limit", ["abc", 1.5, None, True])
    def test_list_loans_limit_invalid_type(self, api, limit):
        """异常用例：limit错误类型"""
        resp = api.get(self.BASE_PATH, params={"offset": 0, "limit": limit})
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("client_id", ["abc", 1.5, None, True])
    def test_list_loans_client_id_invalid_type(self, api, client_id):
        """异常用例：clientId错误类型"""
        resp = api.get(self.BASE_PATH, params={"clientId": client_id})
        assert resp.status_code in [400, 422]

    @pytest.mark.parametrize("special_char", ["<script>", "'; DROP TABLE;", "\\n", "%00"])
    def test_list_loans_special_characters(self, api, special_char):
        """异常用例：特殊字符注入测试"""
        resp = api.get(self.BASE_PATH, params={"accountNo": special_char})
        assert resp.status_code in [200, 400, 422]

    def test_list_loans_all_params_empty(self, api):
        """异常用例：所有参数为空字符串"""
        resp = api.get(self.BASE_PATH, params={
            "offset": "",
            "limit": "",
            "orderBy": "",
            "sortOrder": "",
            "clientId": "",
            "status": "",
            "accountNo": "",
            "externalId": "",
            "associations": "",
        })
        assert resp.status_code in [200, 400, 422]