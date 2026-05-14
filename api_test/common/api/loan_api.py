from api_test.common.base_api import BaseApi


class LoanApi(BaseApi):

    def create(self, payload: dict):
        return self.post("/loans", json=payload)

    def approve(self, loan_id: int, payload: dict):
        return self.post(f"/loans/{loan_id}?command=approve", json=payload)

    def disburse(self, loan_id: int, payload: dict):
        return self.post(f"/loans/{loan_id}?command=disburse", json=payload)

    def get(self, loan_id: int):
        return self.get(f"/loans/{loan_id}")

    def repay(self, loan_id: int, payload: dict):
        return self.post(f"/loans/{loan_id}/transactions?command=repayment", json=payload)

    def get_schedule(self, loan_id: int):
        return self.get(f"/loans/{loan_id}/repaymentschedule")

    def create_product(self, payload: dict):
        return self.post("/loanproducts", json=payload)