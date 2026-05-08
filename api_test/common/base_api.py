import base64
import json
import logging
import requests
import yaml
from pathlib import Path

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class BaseApi:
    """Fineract API 请求基类"""

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

    # ========== 内部工具 ==========

    def _url(self, path: str) -> str:
        return (f"{self.base_url}/fineract-provider/ap"
                f"i/v1{path}")

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """统一请求入口，带日志和异常处理"""
        url = self._url(path)
        logger.info(f"→ {method.upper()} {url}")
        if "json" in kwargs and kwargs["json"]:
            logger.debug(f"  Body: {json.dumps(kwargs['json'], ensure_ascii=False)[:200]}")

        try:
            resp = self._session.request(method, url, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"无法连接到 Fineract: {url}\n原因: {e}") from e
        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"请求超时: {url}") from e

        logger.info(f"← {resp.status_code} {path}")
        if not resp.ok:
            logger.warning(f"  响应: {resp.text[:300]}")

        return resp

    # ========== HTTP 方法 ==========

    def get(self, path: str, params: dict = None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: dict = None, **kwargs):
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict = None, **kwargs):
        return self._request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs):  # ← 补充 delete
        return self._request("DELETE", path, **kwargs)

    # ========== 数据加载 ==========

    def _data_dir(self) -> Path:
        """返回 data 目录路径，不存在则自动创建"""
        data_dir = Path(__file__).parents[1] / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
