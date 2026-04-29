import base64
import requests
import yaml
from pathlib import Path

class BaseApi:
    """Fineract API 请求基类，封装通用的 GET/POST 请求。"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[2] / "config" / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)["fineract"]

        self.base_url = cfg["base_url"].rstrip("/")
        self.tenant_id = cfg["tenant_id"]

        token = base64.b64encode(
            f"{cfg['username']}:{cfg['password']}".encode()
        ).decode()
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update({
            "Authorization": f"Basic {token}",
            "Fineract-Platform-TenantId": self.tenant_id,
            "Content-Type": "application/json",
        })

    def _url(self, path: str) -> str:
        return f"{self.base_url}/fineract-provider/api/v1{path}"

    def get(self, path: str, params: dict = None, **kwargs):
        resp = self._session.get(self._url(path), params=params, **kwargs)
        return resp

    def post(self, path: str, json: dict = None, **kwargs):
        resp = self._session.post(self._url(path), json=json, **kwargs)
        return resp
# import base64
# import urllib3
#
# import requests
# import yaml
# from pathlib import Path
#
#
# # 禁用 SSL 警告
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#
# class BaseApi:
#     """Fineract API 请求基类，封装通用的 GET/POST 请求。"""
#
#     def __init__(self, config_path: str = None):
#         if config_path is None:
#             config_path = Path(__file__).parents[2] / "config" / "config.yaml"
#         with open(config_path, "r", encoding="utf-8") as f:
#             cfg = yaml.safe_load(f)["fineract"]
#
#         self.base_url = cfg["base_url"].rstrip("/")
#         self.tenant_id = cfg["tenant_id"]
#
#         token = base64.b64encode(
#             f"{cfg['username']}:{cfg['password']}".encode()
#         ).decode()
#
#         self._session = requests.Session()
#
#         # 强制禁用 SSL 验证（兼容多种 SSL 库版本）
#         self._session.verify = False
#
#         # 配置 SSL 上下文，禁用主机名验证
#         self._session.mount('https://', requests.adapters.HTTPAdapter(
#             max_retries=3,
#             pool_connections=10,
#             pool_maxsize=10
#         ))
#
#         self._session.headers.update({
#             "Authorization": f"Basic {token}",
#             "Fineract-Platform-TenantId": self.tenant_id,
#             "Content-Type": "application/json",
#         })
#
#     def _url(self, path: str) -> str:
#         return f"{self.base_url}/fineract-provider/api/v1{path}"
#
#     def get(self, path: str, params: dict = None, **kwargs):
#         resp = self._session.get(self._url(path), params=params, **kwargs)
#         return resp
#
#     def post(self, path: str, json: dict = None, **kwargs):
#         resp = self._session.post(self._url(path), json=json, **kwargs)
#         return resp
