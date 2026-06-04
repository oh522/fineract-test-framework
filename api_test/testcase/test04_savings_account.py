import allure
import pytest
from datetime import datetime

from api_test.common.api.savings_api import SavingsApi
from utils.assertion import (
    assert_status, assert_field, assert_jsonpath, assert_response_time,
)
from utils.db_helper import DBHelper

DATE_META = {"dateFormat": "dd MMMM yyyy", "locale": "en"}


@allure.feature("储蓄账户")
class TestSavingsAccount:

    @allure.story("查询账户详情")
    @pytest.mark.smoke
    @pytest.mark.P0
    def test_get_savings_account(self, savings_api: SavingsApi, savings_account_id):
        """✅ 已激活账户状态应为 Active"""
        res = savings_api.get_detail(savings_account_id)  # ← API 层

        assert_status(res, 200)
        assert_response_time(res, 3.0)
        assert_jsonpath(res, "$.status.value", "Active")

        with DBHelper() as db:
            row = db.query_one(
                "SELECT status_enum FROM m_savings_account WHERE id = %s",
                (savings_account_id,)
            )
            assert row["status_enum"] == 300, "储蓄账户状态不是 Active"

    @allure.story("存款操作")
    @pytest.mark.P1
    def test_deposit(self, savings_api: SavingsApi, savings_account_id):
        """✅ 存款后余额增加"""
        today = datetime.now().strftime("%d %B %Y")
        before_data = savings_api.get_detail(savings_account_id).json()
        summary = before_data.get("summary", {})
        account_balance = summary.get("accountBalance", 0)
        # accountBalance 可能是 float 或 dict，需要判断类型
        if isinstance(account_balance, dict):
            before = account_balance.get("amount", 0)
        else:
            before = float(account_balance) if account_balance else 0

        res = savings_api.deposit(savings_account_id, {        # ← API 层
            "transactionDate": today,
            "transactionAmount": 1000,
            "paymentTypeId": 1,
            **DATE_META,
        })
        assert_status(res, 200, msg="存款")
        assert_field(res, "resourceId")

        after_data = savings_api.get_detail(savings_account_id).json()
        summary_after = after_data.get("summary", {})
        account_balance_after = summary_after.get("accountBalance", 0)
        # accountBalance 可能是 float 或 dict，需要判断类型
        if isinstance(account_balance_after, dict):
            after = account_balance_after.get("amount", 0)
        else:
            after = float(account_balance_after) if account_balance_after else 0

        assert after > before, "存款后余额未增加"

    @allure.story("取款操作")
    @pytest.mark.P1
    def test_withdrawal(self, savings_api: SavingsApi, savings_account_id):
        """✅ 取款后余额减少"""
        today = datetime.now().strftime("%d %B %Y")

        before_data = savings_api.get_detail(savings_account_id).json()
        summary = before_data.get("summary", {})
        account_balance = summary.get("accountBalance", 0)
        # accountBalance 可能是 float 或 dict，需要判断类型
        if isinstance(account_balance, dict):
            before = account_balance.get("amount", 0)
        else:
            before = float(account_balance) if account_balance else 0

        res = savings_api.withdraw(savings_account_id, {       # ← API 层
            "transactionDate": today,
            "transactionAmount": 500,
            "paymentTypeId": 1,
            **DATE_META,
        })
        assert_status(res, 200, msg="取款")

        after_data = savings_api.get_detail(savings_account_id).json()
        summary_after = after_data.get("summary", {})
        account_balance_after = summary_after.get("accountBalance", 0)
        # accountBalance 可能是 float 或 dict，需要判断类型
        if isinstance(account_balance_after, dict):
            after = account_balance_after.get("amount", 0)
        else:
            after = float(account_balance_after) if account_balance_after else 0

        assert after < before, "取款后余额未减少"

    @allure.story("取款超出余额")
    @pytest.mark.P2
    def test_withdrawal_exceeds_balance(self, savings_api: SavingsApi, savings_account_id):
        """❌ 超额取款应返回 4xx"""
        res = savings_api.withdraw(savings_account_id, {       # ← API 层
            "transactionDate": datetime.now().strftime("%d %B %Y"),
            "transactionAmount": 99999999,
            "paymentTypeId": 1,
            **DATE_META,
        })
        assert_status(res, 400, 403, msg="超额取款")