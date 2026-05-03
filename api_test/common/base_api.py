import base64
import pytest
import requests
import yaml
from pathlib import Path
import json



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

    def put(self, path: str, json: dict = None, **kwargs):
        resp = self._session.put(self._url(path), json=json, **kwargs)
        return resp

    def load_json_data(self, filename, key="base", **overrides):
        """
        从JSON文件加载测试数据，并支持覆盖字段

        Args:
            filename: JSON文件名（相对于data目录）
            key: JSON中的键名，默认"base"
            **overrides: 需要覆盖的字段

        Returns:
            dict: 处理后的数据
        """
        # 数据目录路径 - 指向 api_test/data
        data_dir = Path(__file__).parents[1] / "data"
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)

        filepath = data_dir / filename

        # 检查文件是否存在
        if not filepath.exists():
            raise FileNotFoundError(f"JSON文件不存在: {filepath}")

        # 读取JSON文件
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON文件格式错误: {filepath}\n{e}")

        # 检查键是否存在
        if key not in all_data:
            available_keys = list(all_data.keys())
            raise KeyError(f"键 '{key}' 不存在于 {filename} 中。可用的键: {available_keys}")

        # 获取指定数据
        data = all_data[key].copy()

        # 应用覆盖字段
        if overrides:
            data.update(overrides)

        return data

    def load_and_send(self, endpoint, method="POST", filename="loan_payload.json",
                      key="base", params=None, **overrides):
        """
        加载JSON数据并直接发送请求

        Args:
            endpoint: API端点（如 /loans）
            method: HTTP方法 (POST/GET/PUT)
            filename: JSON文件名
            key: JSON中的键名
            params: URL查询参数
            **overrides: 需要覆盖的数据字段

        Returns:
            response: API响应
        """
        # 加载数据
        data = self.load_json_data(filename, key, **overrides)

        # 根据方法发送请求
        method = method.upper()
        if method == "POST":
            return self.post(endpoint, json=data)
        elif method == "PUT":
            return self.put(endpoint, json=data)
        elif method == "GET":
            return self.get(endpoint, params=params or data)
        else:
            raise ValueError(f"不支持的HTTP方法: {method}")
