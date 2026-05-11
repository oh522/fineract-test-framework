import base64
import json
import logging
import os
import time
import requests
import yaml
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class BaseApi:
    """Fineract API 请求基类 — 统一请求入口、日志、重试、异常处理"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[2] / "config" / "config.yaml"

        with open(config_path, "r", encoding="utf-8") as f:
            full_cfg = yaml.safe_load(f)

        # ✅ 多环境支持：优先读环境变量
        env = os.environ.get("TEST_ENV", full_cfg.get("env", "test"))
        cfg = full_cfg[env]["fineract"]
        logger.info(f"当前测试环境: {env} | base_url: {cfg['base_url']}")

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

    # ─── 内部工具 ──────────────────────────────────────────

    def _url(self, path: str) -> str:
        return f"{self.base_url}/fineract-provider/api/v1{path}"

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """统一请求入口：自动日志 + 指数退避重试 + 响应时间记录"""
        url = self._url(path)
        logger.info(f"→ {method.upper()} {url}")
        if kwargs.get("json"):
            logger.debug(f"  Body: {json.dumps(kwargs['json'], ensure_ascii=False)[:300]}")

        # ✅ 失败重试（指数退避，最多3次）
        last_exc = None
        for attempt in range(1, 4):
            try:
                start = time.time()
                resp = self._session.request(method, url, timeout=30, **kwargs)
                elapsed = time.time() - start
                logger.info(f"← {resp.status_code} {path} [{elapsed:.2f}s]")
                if not resp.ok:
                    logger.warning(f"  响应体: {resp.text[:300]}")
                return resp
            except requests.exceptions.ConnectionError as e:
                last_exc = e
                logger.warning(f"  连接失败 第{attempt}次重试: {e}")
                time.sleep(2 ** attempt)
            except requests.exceptions.Timeout as e:
                raise TimeoutError(f"请求超时: {url}") from e

        raise ConnectionError(f"连接失败(已重试3次): {url}") from last_exc

    # ─── HTTP 方法 ──────────────────────────────────────────

    def get(self, path: str, params: dict = None, **kwargs):
        return self._request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: dict = None, **kwargs):
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict = None, **kwargs):
        return self._request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: dict = None, **kwargs):
        return self._request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)

    # ─── 数据目录 ──────────────────────────────────────────

    def _data_dir(self) -> Path:
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir