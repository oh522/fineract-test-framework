from typing import Optional
from common.base_api import BaseApi


class UserApi(BaseApi):
    """用户接口封装"""
    def retrieve_list(self):
        return self.get("/users")

    def create(self, payload: dict):
        return self.post("/users", json=payload)

    def download_template(self, office_id: Optional[int] = None, staff_id: Optional[int] = None, date_format: str = "dd MMMM yyyy"):
        """下载用户导入模板"""
        params = {}
        if office_id:
            params["officeId"] = office_id
        if staff_id:
            params["staffId"] = staff_id
        params["dateFormat"] = date_format
        headers = {"Accept": "application/vnd.ms-excel"}
        return self.get("/users/downloadtemplate", params=params, headers=headers)

    def retrieve_user_details(self):
        return self.get("/users/template")

    def upload_template(self, file_path: str, data_format: str = "dd MMMM yyyy", locale: str = "en"):
        with open(file_path, "rb") as f:
            files = {
                'uploadInputStream': (file_path.split('/')[-1], f, 'application/vnd.ms-excel')
            }
            data = {
                'dataFormat': data_format,
                'locale': locale
            }
            return self.post("/users/uploadtemplate", data=data, files=files)

    def delete(self, user_id: int):
        return self.delete(f"/users/{user_id}")

    def retrieve(self, user_id: int):
        return self.get(f"/users/{user_id}")

    def update(self, user_id: int, payload: dict):
        return self.put(f"/users/{user_id}", json=payload)

    def change_password(self, user_id: int, payload: dict):
        return self.post(f"/users/{user_id}/changepassword", json=payload)





