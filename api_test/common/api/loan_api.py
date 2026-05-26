from api_test.common.base_api import BaseApi


class LoanApi(BaseApi):

    def create_product(self, payload: dict):
        """创建贷款产品"""
        return self.post("/loanproducts", json=payload)

    def apply(self, payload: dict):
        """提交贷款申请"""
        return self.post("/loans", json=payload)

    def approve(self, loan_id: int, payload: dict):
        """审批贷款"""
        return self.post(f"/loans/{loan_id}?command=approve", json=payload)

    def disburse(self, loan_id: int, payload: dict):
        """放款"""
        return self.post(f"/loans/{loan_id}?command=disburse", json=payload)

    def get_detail(self, loan_id: int):
        """查询贷款详情"""
        return self.get(f"/loans/{loan_id}")

    def get_schedule(self, loan_id: int):
        """查询还款计划"""
        return self.get(f"/loans/{loan_id}", params={"template": "true"})

    def repay(self, loan_id: int, payload: dict):
        """还款"""
        return self.post(
            f"/loans/{loan_id}/transactions?command=repayment",
            json=payload,
        )
