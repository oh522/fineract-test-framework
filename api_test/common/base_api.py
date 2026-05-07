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
        return f"{self.base_url}/fineract-provider/api/v1{path}"

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

    def load_json_data(self, filename: str, key: str = "base", **overrides) -> dict:
        """
        从 JSON 文件加载测试数据，支持字段覆盖。

        Args:
            filename: JSON 文件名（相对于 data 目录）
            key:      JSON 中的键名，默认 "base"
            **overrides: 需要覆盖的字段

        Returns:
            dict: 合并后的数据副本
        """
        filepath = self._data_dir() / filename

        if not filepath.exists():
            raise FileNotFoundError(f"数据文件不存在: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON 格式错误: {filepath}\n{e}") from e

        if key not in all_data:
            raise KeyError(
                f"键 '{key}' 不存在于 {filename}，可用键: {list(all_data.keys())}"
            )

        data = all_data[key].copy()
        data.update(overrides)  # overrides 为空时 update({}) 无副作用，不需要判断
        return data

    def load_and_send(
        self,
        endpoint: str,
        method: str = "POST",
        filename: str = "loan_payload.json",
        key: str = "base",
        params: dict = None,
        **overrides,
    ) -> requests.Response:
        """
        加载 JSON 数据并直接发送请求。

        Args:
            endpoint: API 端点（如 /loans）
            method:   HTTP 方法（POST/PUT/GET/DELETE）
            filename: JSON 文件名
            key:      JSON 中的键名
            params:   GET 请求的查询参数（仅 GET 时有效）
            **overrides: 覆盖 JSON 中的字段
        """
        method = method.upper()
        data = self.load_json_data(filename, key, **overrides)

        if method == "GET":
            return self.get(endpoint, params=params)  # GET 不传 body
        elif method in ("POST", "PUT", "DELETE"):
            return self._request(method, endpoint, json=data)
        else:
            raise ValueError(f"不支持的 HTTP 方法: {method}")