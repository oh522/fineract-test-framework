from api_test.common.base_api import BaseApi


class ClientApi(BaseApi):

    def create(self, payload: dict):
        """创建客户"""
        return self.post("/clients", json=payload)

    def get_detail(self, client_id: int):
        """查询客户详情"""
        return self.get(f"/clients/{client_id}")

    def update(self, client_id: int, payload: dict):
        """更新客户信息"""
        return self.put(f"/clients/{client_id}", json=payload)

    def list_clients(self, limit: int = 10, offset: int = 0):
        """查询客户列表"""
        return self.get("/clients", params={"limit": limit, "offset": offset})
