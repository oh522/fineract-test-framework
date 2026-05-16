from api_test.common.base_api import BaseApi


class ClientApi(BaseApi):

    def create(self, payload: dict):
        return self.post("/clients", json=payload)

    def get(self, client_id: int):
        return self.get(f"/clients/{client_id}")

    def update(self, client_id: int, payload: dict):
        return self.put(f"/clients/{client_id}", json=payload)

    def list_clients(self, limit: int = 10, offset: int = 0):
        return self.get("/clients", params={"limit": limit, "offset": offset})