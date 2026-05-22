"""
接口加密工具
- 参数签名：MD5/HMAC，发请求前自动附加
- 响应解密：AES，接收响应后自动解密
Fineract 用 Basic Auth，此模块用于有签名需求的扩展场景
"""
import hashlib
import hmac
import base64
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
# 🔍 根本原因
# 包冲突问题：环境中同时存在两个名称相似但不同的包：
# ❌ crypto (1.4.1) - 一个不相关的包，干扰了正常导入
# ✅ pycryptodome (3.23.0) - 正确的加密库（提供 Crypto 模块）
# 虽然安装了 pycryptodome，但由于 crypto 包的存在导致 Python 无法正确识别 Crypto 模块。

# ─── 第一种：参数签名（MD5） ──────────────────────────────────

SECRET_KEY = os.environ.get("API_SECRET_KEY", "your_secret_key")


def generate_md5_sign(params: dict) -> str:
    """
    MD5 签名：参数按 key 排序 → 拼接 → 加盐 → MD5
    用法：在发请求前调用，将返回值附加到参数中
    """
    # 1. 按 key 字典序排序
    sorted_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    # 2. 拼接 SECRET_KEY
    raw = sorted_str + SECRET_KEY
    # 3. MD5
    sign = hashlib.md5(raw.encode()).hexdigest()
    return sign


def generate_hmac_sign(params: dict) -> str:
    """
    HMAC-SHA256 签名（更安全，推荐使用）
    """
    sorted_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    sign = hmac.new(
        SECRET_KEY.encode(),
        sorted_str.encode(),
        hashlib.sha256
    ).hexdigest()
    return sign


def verify_sign(params: dict, received_sign: str) -> bool:
    """验证收到的签名是否合法"""
    expected = generate_md5_sign({k: v for k, v in params.items() if k != "sign"})
    return hmac.compare_digest(expected, received_sign)


# ─── 第二种：AES 响应解密 ──────────────────────────────────────

AES_KEY = os.environ.get("AES_KEY", "0123456789abcdef").encode()  # 16/24/32 字节
AES_IV = os.environ.get("AES_IV", "abcdef0123456789").encode()  # 16 字节


def aes_decrypt(cipher_text: str) -> dict:
    """
    AES-CBC 解密（适用于响应体加密的场景）
    在 base_api._request 中调用：收到响应后判断是否加密，加密则先解密再返回
    """
    raw = base64.b64decode(cipher_text)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decrypted = unpad(cipher.decrypt(raw), AES.block_size)
    return json.loads(decrypted.decode("utf-8"))


def aes_encrypt(data: dict) -> str:
    """AES-CBC 加密（用于加密请求体）"""
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(pad(raw, AES.block_size))
    return base64.b64encode(encrypted).decode()


# ─── 集成到 base_api 中的示例 ────────────────────────────────

"""
在 base_api._request 末尾加入自动解密逻辑：

    resp = self._session.request(method, url, **kwargs)

    # 如果响应是加密的（根据业务约定判断，如 header 或固定字段）
    if resp.headers.get("X-Encrypted") == "true":
        decrypted_data = aes_decrypt(resp.text)
        # 构造新的响应对象（或直接返回解密数据）
        resp._content = json.dumps(decrypted_data).encode()

    return resp

在发请求时自动附加签名：

    def post(self, path, json=None, sign=False, **kwargs):
        if sign and json:
            json["sign"] = generate_md5_sign(json)
        return self._request("POST", path, json=json, **kwargs)
"""