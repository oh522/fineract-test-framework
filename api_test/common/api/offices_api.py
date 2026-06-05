from typing import Optional
from common.base_api import BaseApi


class OfficeApi(BaseApi):
    """机构（Offices）接口封装"""

    def retrieve_list(self, parameters: Optional[str] = None):
        """查询机构列表"""
        params = {}
        if parameters:
            params["parameters"] = parameters
        return self.get("/offices", params=params)

    def create(self, payload: dict):
        """创建机构"""
        return self.post("/offices", json=payload)

    def download_template(self, date_format: str = "dd MMMM yyyy"):
        """下载机构导入模板"""
        params = {"dateFormat": date_format}
        headers = {"Accept": "application/vnd.ms-excel"}
        return self.get("/offices/downloadtemplate", params=params, headers=headers)

    def retrieve_by_external_id(self, external_id: str):
        """通过外部 ID 查询机构"""
        return self.get(f"/offices/external-id/{external_id}")

    def update_by_external_id(self, external_id: str, payload: dict):
        """通过外部 ID 更新机构"""
        return self.put(f"/offices/external-id/{external_id}", json=payload)

    def retrieve_template(self):
        """查询机构详情模板"""
        return self.get("/offices/template")

    def upload_template(self, file_path: str, data_format: str = "dd MMMM yyyy", locale: str = "en"):
        """上传机构导入模板"""
        with open(file_path, "rb") as f:
            files = {
                'uploadInputStream': (file_path.split('/')[-1], f, 'application/vnd.ms-excel')
            }
            data = {
                'dataFormat': data_format,
                'locale': locale
            }
            return self.post("/offices/uploadtemplate", data=data, files=files)

    def retrieve(self, office_id: int):
        """查询机构详情"""
        return self.get(f"/offices/{office_id}")

    def update(self, office_id: int, payload: dict):
        """更新机构"""
        return self.put(f"/offices/{office_id}", json=payload)
