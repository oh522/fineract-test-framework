import uuid
import pytest
from datetime import datetime, timedelta

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


def _base_savings_payload(client_id: int, product_id: int) -> dict:
    """构建最小可用储蓄账户创建 payload"""
    today = datetime.now()
    return {
        "clientId": client_id,
        "productId": product_id,
        "submittedOnDate": today.strftime("%d %B %Y"),
        **DATE_META,
    }


class TestCreateSavingsAccount:
    """POST /savingsaccounts"""

    def test_success(self, api, client_id, savings_product_id):
        """正常创建储蓄账户"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200, f"创建失败: {res.text}"

        data = res.json()
        assert "savingsId" in data, "响应缺少 savingsId"
        assert isinstance(data["savingsId"], int)
        assert "resourceId" in data

    def test_with_external_id(self, api, client_id, savings_product_id):
        """创建时指定 externalId"""
        ext_id = f"SAV-{uuid.uuid4().hex[:8]}"
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["externalId"] = ext_id
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code == 200, f"创建失败: {res.text}"

        data = res.json()
        assert data.get("resourceExternalId") == ext_id, "externalId 不匹配"

    def test_with_nominal_annual_interest_rate(self, api, client_id, savings_product_id):
        """创建时指定年利率"""
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["nominalAnnualInterestRate"] = 5.0
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code == 200
        assert "savingsId" in res.json()

    @pytest.mark.parametrize("field", [
        "clientId", "productId", "submittedOnDate",
    ])
    def test_missing_required_field(self, api, client_id, savings_product_id, field):
        """缺少必填字段"""
        payload = _base_savings_payload(client_id, savings_product_id)
        del payload[field]
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code in [400, 422], f"缺少 {field} 应返回错误，实际: {res.status_code}"

    def test_invalid_client(self, api, savings_product_id):
        """不存在的客户"""
        payload = _base_savings_payload(999999, savings_product_id)
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code in [400, 404], f"无效客户应返回错误，实际: {res.status_code}"

    def test_invalid_product(self, api, client_id):
        """不存在的储蓄产品"""
        payload = _base_savings_payload(client_id, 999999)
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code in [400, 404], f"无效产品应返回错误，实际: {res.status_code}"

    @pytest.mark.parametrize("rate, desc", [
        (-1,         "负利率"),
        (0,          "零利率"),
        (101,        "超过100%利率"),
    ])
    def test_invalid_interest_rate(self, api, client_id, savings_product_id, rate, desc):
        """利率边界值"""
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["nominalAnnualInterestRate"] = rate
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code in [400, 403, 422], f"{desc} 应返回错误，实际: {res.status_code}"

    def test_invalid_date_format(self, api, client_id, savings_product_id):
        """日期格式错误"""
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["submittedOnDate"] = "2025-01-01"  # 应为 dd MMMM yyyy
        del payload["dateFormat"]
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code in [400, 422], f"错误日期格式应返回错误，实际: {res.status_code}"

    def test_empty_body(self, api):
        """空请求体"""
        res = api.post("/savingsaccounts", json={})
        assert res.status_code in [400, 422]


class TestGetSavingsAccounts:
    """GET /savingsaccounts"""

    def test_list(self, api):
        """查询储蓄账户列表"""
        res = api.get("/savingsaccounts")
        assert res.status_code == 200, f"查询失败: {res.text}"

        data = res.json()
        assert "totalFilteredRecords" in data
        assert "pageItems" in data
        assert isinstance(data["pageItems"], list)

    def test_list_with_pagination(self, api):
        """分页查询"""
        res = api.get("/savingsaccounts", params={"offset": 0, "limit": 5})
        assert res.status_code == 200
        data = res.json()
        assert len(data["pageItems"]) <= 5

    def test_list_with_status_filter(self, api):
        """按状态过滤"""
        res = api.get("/savingsaccounts", params={"status": "active"})
        assert res.status_code == 200

    def test_list_external_id(self, api):
        """查询列表返回 externalId 字段"""
        res = api.get("/savingsaccounts")
        assert res.status_code == 200
        data = res.json()
        if data["pageItems"]:
            assert "externalId" in data["pageItems"][0]


class TestGetSavingsAccountTemplate:
    """GET /savingsaccounts/template"""

    def test_template(self, api):
        """获取储蓄账户创建模板"""
        res = api.get("/savingsaccounts/template")
        assert res.status_code == 200, f"获取模板失败: {res.text}"

        data = res.json()
        assert "productOptions" in data, "响应缺少 productOptions"

    def test_template_with_client(self, api, client_id):
        """指定 clientId 获取模板"""
        res = api.get("/savingsaccounts/template", params={"clientId": client_id})
        assert res.status_code == 200
        data = res.json()
        assert "productOptions" in data

    def test_template_with_product(self, api, savings_product_id):
        """指定 productId 获取模板"""
        res = api.get("/savingsaccounts/template", params={"productId": savings_product_id})
        assert res.status_code == 200


class TestGetSavingsAccount:
    """GET /savingsaccounts/{accountId}"""

    def test_get_active(self, api, savings_account_id):
        """查询已激活的储蓄账户（savings_account_id 由 conftest 创建→审批→激活）"""
        res = api.get(f"/savingsaccounts/{savings_account_id}")
        assert res.status_code == 200, f"查询失败: {res.text}"

        data = res.json()
        assert data["id"] == savings_account_id
        assert data["status"]["value"] == "Active"

    def test_get_nonexistent(self, api):
        """查询不存在的储蓄账户"""
        res = api.get("/savingsaccounts/999999")
        assert res.status_code == 404

    def test_get_with_associations(self, api, savings_account_id):
        """查询账户详情附带关联数据"""
        res = api.get(f"/savingsaccounts/{savings_account_id}", params={
            "associations": "transactions"
        })
        assert res.status_code == 200
        data = res.json()
        assert "transactions" in data

    def test_get_fields(self, api, savings_account_id):
        """验证返回字段完整性"""
        res = api.get(f"/savingsaccounts/{savings_account_id}")
        assert res.status_code == 200
        data = res.json()
        assert "id" in data
        assert "accountNo" in data
        assert "productName" in data
        assert "clientId" in data
        assert "currency" in data


class TestUpdateSavingsAccount:
    """PUT /savingsaccounts/{accountId}"""

    def test_update_external_id(self, api, savings_account_id):
        """修改储蓄账户的 externalId"""
        ext_id = f"UPD-{uuid.uuid4().hex[:8]}"
        res = api.put(f"/savingsaccounts/{savings_account_id}", json={
            "externalId": ext_id,
        })
        assert res.status_code == 200, f"修改失败: {res.text}"

        data = res.json()
        assert data.get("resourceExternalId") == ext_id, "externalId 更新不成功"

    def test_update_nonexistent(self, api):
        """修改不存在的储蓄账户"""
        res = api.put("/savingsaccounts/999999", json={
            "externalId": "test",
        })
        assert res.status_code in [400, 404], f"修改不存在账户应返回错误，实际: {res.status_code}"

    def test_update_nominal_annual_interest_rate(self, api, savings_account_id):
        """修改年利率"""
        res = api.put(f"/savingsaccounts/{savings_account_id}", json={
            "nominalAnnualInterestRate": 4.5,
        })
        assert res.status_code == 200


class TestDeleteSavingsAccount:
    """DELETE /savingsaccounts/{accountId}"""

    def test_delete_new_account(self, api, client_id, savings_product_id):
        """删除新建状态的储蓄账户（未审批可删除）"""
        # 创建一个新账户用于删除
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        res = api.delete(f"/savingsaccounts/{sid}")
        assert res.status_code == 200, f"删除失败: {res.text}"

        data = res.json()
        assert "resourceId" in data

    def test_delete_nonexistent(self, api):
        """删除不存在的储蓄账户"""
        res = api.delete("/savingsaccounts/999999")
        assert res.status_code in [400, 404], f"删除不存在账户应返回错误，实际: {res.status_code}"


class TestApproveSavingsAccount:
    """POST /savingsaccounts/{accountId}?command=approve"""

    def test_approve(self, api, client_id, savings_product_id):
        """正常审批储蓄账户"""
        # 创建账户
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json={
            "approvedOnDate": today,
            **DATE_META,
        })
        assert res.status_code == 200, f"审批失败: {res.text}"

        data = res.json()
        assert data["resourceId"] == sid

        # 验证状态
        res = api.get(f"/savingsaccounts/{sid}")
        assert res.status_code == 200
        assert res.json()["status"]["value"] == "Approved"

    def test_approve_nonexistent(self, api):
        """审批不存在的储蓄账户"""
        today = datetime.now().strftime("%d %B %Y")
        res = api.post("/savingsaccounts/999999?command=approve", json={
            "approvedOnDate": today,
            **DATE_META,
        })
        assert res.status_code in [400, 404]

    def test_approve_without_date(self, api, client_id, savings_product_id):
        """审批时缺少日期"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        res = api.post(f"/savingsaccounts/{sid}?command=approve", json={})
        assert res.status_code in [400, 422], f"缺少审批日期应返回错误，实际: {res.status_code}"

    def test_approve_already_approved(self, api, client_id, savings_product_id):
        """重复审批同一账户"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")
        approve_payload = {"approvedOnDate": today, **DATE_META}

        # 第一次审批
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json=approve_payload)
        assert res.status_code == 200

        # 重复审批
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json=approve_payload)
        assert res.status_code in [400, 403, 409]


class TestActivateSavingsAccount:
    """POST /savingsaccounts/{accountId}?command=activate"""

    def test_activate(self, api, client_id, savings_product_id):
        """正常激活储蓄账户"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")

        # 审批
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json={
            "approvedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200

        # 激活
        res = api.post(f"/savingsaccounts/{sid}?command=activate", json={
            "activatedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200, f"激活失败: {res.text}"

        # 验证状态
        res = api.get(f"/savingsaccounts/{sid}")
        assert res.status_code == 200
        assert res.json()["status"]["value"] == "Active"

    def test_activate_without_approval(self, api, client_id, savings_product_id):
        """未审批直接激活"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")
        res = api.post(f"/savingsaccounts/{sid}?command=activate", json={
            "activatedOnDate": today, **DATE_META,
        })
        assert res.status_code in [400, 403, 409]

    def test_activate_nonexistent(self, api):
        """激活不存在的储蓄账户"""
        today = datetime.now().strftime("%d %B %Y")
        res = api.post("/savingsaccounts/999999?command=activate", json={
            "activatedOnDate": today, **DATE_META,
        })
        assert res.status_code in [400, 404]

    def test_activate_without_date(self, api, client_id, savings_product_id):
        """激活时缺少日期"""
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json={
            "approvedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200

        res = api.post(f"/savingsaccounts/{sid}?command=activate", json={})
        assert res.status_code in [400, 422]


class TestCloseSavingsAccount:
    """POST /savingsaccounts/{accountId}?command=close"""

    def test_close(self, api, savings_account_id):
        """正常关闭储蓄账户"""
        today = datetime.now().strftime("%d %B %Y")
        res = api.post(f"/savingsaccounts/{savings_account_id}?command=close", json={
            "closedOnDate": today,
            "withdrawBalance": True,
            **DATE_META,
        })
        assert res.status_code == 200, f"关闭失败: {res.text}"

        data = res.json()
        assert data["resourceId"] == savings_account_id

        # 验证状态
        res = api.get(f"/savingsaccounts/{savings_account_id}")
        assert res.status_code == 200
        assert res.json()["status"]["value"] == "Closed"

    def test_close_nonexistent(self, api):
        """关闭不存在的储蓄账户"""
        today = datetime.now().strftime("%d %B %Y")
        res = api.post("/savingsaccounts/999999?command=close", json={
            "closedOnDate": today,
            "withdrawBalance": True,
            **DATE_META,
        })
        assert res.status_code in [400, 404]

    def test_close_without_date(self, api, savings_account_id):
        """关闭时缺少日期"""
        res = api.post(f"/savingsaccounts/{savings_account_id}?command=close", json={
            "withdrawBalance": True,
        })
        assert res.status_code in [400, 422]


class TestBlockSavingsAccount:
    """POST /savingsaccounts/{accountId}?command=block"""

    def test_block_and_unblock(self, api, client_id, savings_product_id):
        """冻结后解冻储蓄账户"""
        # 创建 → 审批 → 激活
        res = api.post("/savingsaccounts", json=_base_savings_payload(client_id, savings_product_id))
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        today = datetime.now().strftime("%d %B %Y")
        res = api.post(f"/savingsaccounts/{sid}?command=approve", json={
            "approvedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200
        res = api.post(f"/savingsaccounts/{sid}?command=activate", json={
            "activatedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200

        # 冻结
        res = api.post(f"/savingsaccounts/{sid}?command=block", json={
            "blockedOnDate": today, **DATE_META,
        })
        assert res.status_code == 200, f"冻结失败: {res.text}"

        # 验证状态
        res = api.get(f"/savingsaccounts/{sid}")
        assert res.status_code == 200
        assert res.json()["status"]["value"] == "Block"

        # 解冻
        res = api.post(f"/savingsaccounts/{sid}?command=unblock", json={})
        assert res.status_code == 200, f"解冻失败: {res.text}"

        # 验证状态
        res = api.get(f"/savingsaccounts/{sid}")
        assert res.status_code == 200
        assert res.json()["status"]["value"] == "Active"

    def test_block_nonexistent(self, api):
        """冻结不存在的储蓄账户"""
        today = datetime.now().strftime("%d %B %Y")
        res = api.post("/savingsaccounts/999999?command=block", json={
            "blockedOnDate": today, **DATE_META,
        })
        assert res.status_code in [400, 404]


class TestUnblockSavingsAccount:
    """POST /savingsaccounts/{accountId}?command=unblock"""

    def test_unblock_nonexistent(self, api):
        """解冻不存在的储蓄账户"""
        res = api.post("/savingsaccounts/999999?command=unblock", json={})
        assert res.status_code in [400, 404]

    def test_unblock_not_blocked(self, api, savings_account_id):
        """解冻未冻结的储蓄账户"""
        res = api.post(f"/savingsaccounts/{savings_account_id}?command=unblock", json={})
        assert res.status_code in [400, 403, 409]


class TestSavingsAccountByExternalId:
    """GET/DELETE /savingsaccounts/external-id/{externalId}"""

    def test_get_by_external_id(self, api, client_id, savings_product_id):
        """按 externalId 查询储蓄账户"""
        ext_id = f"SAV-EXT-{uuid.uuid4().hex[:8]}"
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["externalId"] = ext_id
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code == 200
        sid = res.json()["savingsId"]

        res = api.get(f"/savingsaccounts/external-id/{ext_id}")
        assert res.status_code == 200, f"按 externalId 查询失败: {res.text}"

        data = res.json()
        assert data["id"] == sid
        assert data["externalId"] == ext_id

    def test_get_by_nonexistent_external_id(self, api):
        """查询不存在的 externalId"""
        res = api.get("/savingsaccounts/external-id/NONEXISTENT_ID_999")
        assert res.status_code in [400, 404]

    def test_delete_by_external_id(self, api, client_id, savings_product_id):
        """按 externalId 删除储蓄账户"""
        ext_id = f"SAV-DEL-{uuid.uuid4().hex[:8]}"
        payload = _base_savings_payload(client_id, savings_product_id)
        payload["externalId"] = ext_id
        res = api.post("/savingsaccounts", json=payload)
        assert res.status_code == 200

        res = api.delete(f"/savingsaccounts/external-id/{ext_id}")
        assert res.status_code == 200, f"按 externalId 删除失败: {res.text}"

        data = res.json()
        assert "resourceId" in data

    def test_delete_by_nonexistent_external_id(self, api):
        """删除不存在的 externalId"""
        res = api.delete("/savingsaccounts/external-id/NONEXISTENT_ID_999")
        assert res.status_code in [400, 404]
