from api_test.common.base_api import BaseApi


class SavingsApi(BaseApi):

    def create_product(self, payload: dict):
        """创建储蓄产品"""
        return self.post("/savingsproducts", json=payload)

    def create_account(self, payload: dict):
        """创建储蓄账户"""
        return self.post("/savingsaccounts", json=payload)

    def approve_account(self, account_id: int, payload: dict):
        """审批储蓄账户"""
        return self.post(f"/savingsaccounts/{account_id}?command=approve", json=payload)

    def activate_account(self, account_id: int, payload: dict):
        """激活储蓄账户"""
        return self.post(f"/savingsaccounts/{account_id}?command=activate", json=payload)

    def get_detail(self, account_id: int):
        """查询储蓄账户详情"""
        return self.get(f"/savingsaccounts/{account_id}")

    def deposit(self, account_id: int, payload: dict):
        """存款"""
        return self.post(
            f"/savingsaccounts/{account_id}/transactions?command=deposit",
            json=payload,
        )

    def withdraw(self, account_id: int, payload: dict):
        """取款"""
        return self.post(
            f"/savingsaccounts/{account_id}/transactions?command=withdrawal",
            json=payload,
        )