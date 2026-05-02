# utils/ai_case_gen.py
import json
import os
import base64
import requests
import yaml
import urllib3
from openai import OpenAI

# 禁用 SSL 警告
urllib3.disable_warnings()

# ========== 配置 ==========
DEEPSEEK_API_KEY = "sk-77a776b9d740407ca50fa535d6a31e57"
SWAGGER_URL = "https://localhost:8443/fineract-provider/fineract.json"

# Fineract 认证信息
USERNAME = "mifos"
PASSWORD = "password"
TENANT_ID = "default"

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# 全局保存 Swagger components，供 Schema 解析使用
swagger_components = {}


# ========== 1. 认证 ==========
def get_auth_headers() -> dict:
    """生成 Fineract 认证请求头"""
    token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Fineract-Platform-TenantId": TENANT_ID
    }


# ========== 2. 获取 Swagger 文档 ==========
def fetch_swagger(url: str) -> dict:
    """从 URL 获取 Swagger JSON"""
    response = requests.get(
        url,
        headers=get_auth_headers(),
        verify=False,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def load_swagger_file(path: str) -> dict:
    """从本地文件加载 Swagger"""
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.safe_load(f)
        return json.load(f)


# ========== 3. 解析 Schema，提取真实字段 ==========
def resolve_ref(ref: str, components: dict) -> dict:
    """解析 $ref 引用，返回真实 schema"""
    try:
        ref_name = ref.split("/")[-1]
        return components.get("schemas", {}).get(ref_name, {})
    except Exception:
        return {}


def extract_schema_fields(schema: dict, components: dict, depth: int = 0) -> dict:
    """递归解析 schema，提取所有字段和示例值（最多递归3层）"""
    if depth > 3:
        return {}

    # 处理 $ref
    if "$ref" in schema:
        schema = resolve_ref(schema["$ref"], components)

    # 处理 allOf / oneOf / anyOf
    for key in ["allOf", "oneOf", "anyOf"]:
        if key in schema:
            merged = {}
            for sub in schema[key]:
                sub_resolved = extract_schema_fields(sub, components, depth + 1)
                merged.update(sub_resolved)
            return merged

    props = schema.get("properties", {})
    required = schema.get("required", [])
    result = {}

    for field, field_schema in props.items():
        # 处理字段内部的 $ref
        if "$ref" in field_schema:
            field_schema = resolve_ref(field_schema["$ref"], components)

        field_type = field_schema.get("type", "string")
        field_example = field_schema.get("example")
        field_enum = field_schema.get("enum", [])
        field_format = field_schema.get("format", "")

        if field_example is not None:
            result[field] = field_example
        elif field_enum:
            result[field] = field_enum[0]
        elif field_type == "integer" or field_type == "number":
            result[field] = 1
        elif field_type == "boolean":
            result[field] = True
        elif field_type == "array":
            items = field_schema.get("items", {})
            if "$ref" in items:
                result[field] = []
            else:
                result[field] = []
        elif field_type == "object":
            nested = extract_schema_fields(field_schema, components, depth + 1)
            result[field] = nested if nested else {}
        elif field_format == "date":
            result[field] = "01 January 2024"
        else:
            result[field] = f"<{field}>"

    return {
        "required_fields": required,
        "all_fields": result
    }


def extract_request_example(request_body: dict, components: dict) -> dict:
    """从 requestBody 提取真实字段示例"""
    if not request_body:
        return {}
    try:
        content = request_body.get("content", {})
        schema = (
            content.get("application/json", {})
            .get("schema", {})
        )
        if not schema:
            # 尝试 multipart/form-data
            schema = (
                content.get("multipart/form-data", {})
                .get("schema", {})
            )
        if not schema:
            return {}

        return extract_schema_fields(schema, components)
    except Exception as e:
        print(f"  ⚠️  Schema 解析失败：{e}")
        return {}


def extract_path_params(parameters: list) -> list:
    """提取路径参数"""
    return [p for p in parameters if p.get("in") == "path"]


def extract_query_params(parameters: list) -> list:
    """提取查询参数"""
    return [p for p in parameters if p.get("in") == "query"]


# ========== 4. 解析接口信息 ==========
def parse_swagger(swagger: dict) -> list:
    """提取所有接口的关键信息"""
    apis = []
    paths = swagger.get("paths", {})
    print(f"DEBUG - paths 数量: {len(paths)}")

    for path, path_item in paths.items():
        for method, detail in path_item.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                continue
            if not isinstance(detail, dict):
                continue

            api_info = {
                "path": path,
                "method": method.upper(),
                "summary": detail.get("summary", ""),
                "parameters": detail.get("parameters", []),
                "requestBody": detail.get("requestBody", {}),
                "responses": detail.get("responses", {}),
                "tags": detail.get("tags", [])
            }
            apis.append(api_info)

    return apis


# ========== 5. DeepSeek 生成测试用例 ==========
def generate_test_cases(api_info: dict) -> str:
    """调用 DeepSeek 为单个接口生成 pytest 测试用例"""

    # 提取真实 Schema 字段
    request_example = extract_request_example(
        api_info.get("requestBody", {}),
        swagger_components
    )
    path_params = extract_path_params(api_info.get("parameters", []))
    query_params = extract_query_params(api_info.get("parameters", []))

    prompt = f"""
你是一个专业的 Apache Fineract 接口测试工程师，请根据以下接口信息生成完整的 pytest 测试用例。

【接口信息】
- 路径：{api_info['path']}
- 方法：{api_info['method']}
- 描述：{api_info['summary']}
- 标签：{api_info['tags']}

【路径参数】
{json.dumps(path_params, ensure_ascii=False, indent=2)}

【查询参数】
{json.dumps(query_params, ensure_ascii=False, indent=2)}

【请求体真实字段（严格按此生成，禁止编造不存在的字段）】
{json.dumps(request_example, ensure_ascii=False, indent=2)}

【生成要求】
1. 使用 pytest 框架，继承 BaseApi 类：
   from api_test.common.base_api import BaseApi

2. 必须包含四类用例（用中文注释说明每个用例的测试目的）：
   - 正常用例：使用 required_fields 里的必填字段，期望成功
   - 参数缺失用例：逐个缺少 required_fields 里的必填字段
   - 边界值用例：空字符串、极大值、极小值、0、负数等
   - 异常用例：错误类型、非法枚举值、特殊字符等

3. 断言规范：
   - 正常用例：assert resp.status_code == 200，并验证响应字段存在
   - 参数缺失/异常用例：assert resp.status_code in [400, 403, 404, 422]
   - 不要硬编码具体的业务数据 ID（使用变量或参数化）

4. 路径参数处理：
   - 如果路径含 {{pathParam}}，测试时使用 f-string 替换
   - 不存在的资源 ID 使用 999999

5. 使用 @pytest.mark.parametrize 做数据驱动

6. 只输出纯 Python 代码，不含任何 markdown 标记和解释说明

【代码结构要求】（重要，必须严格遵守）
- 测试类不能继承任何父类，直接写 class TestXxx:
- 通过方法参数 api 注入 BaseApi 实例（pytest fixture）
- 不要写 __init__ 方法

正确示例：
class TestCreateLoan:
    def test_create_loan_success(self, api):
        resp = api.post("/v1/loans", json={{...}})
        assert resp.status_code == 200

错误示例（禁止）：
class TestCreateLoan(BaseApi):   # ❌ 禁止继承
    def __init__(self):           # ❌ 禁止构造函数
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是专业的 Apache Fineract 接口测试工程师。"
                    "只输出纯 Python 代码，不含任何 markdown 标记（不含```python）。"
                    "严格按照提供的 Schema 字段生成测试数据，禁止编造不存在的字段。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )

    return response.choices[0].message.content


# ========== 6. 清理生成代码 ==========
def clean_code(code: str) -> str:
    """去除 AI 返回内容中多余的 markdown 标记"""
    code = code.strip()
    # 去除 ```python 或 ``` 开头
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    elif code.startswith("```"):
        code = code[3:].strip()
    # 去除结尾的 ```
    if code.endswith("```"):
        code = code[:-3].strip()
    return code


# ========== 7. 生成文件名 ==========
def make_filename(api_info: dict) -> str:
    """根据接口信息生成合法的文件名"""
    path_part = (
        api_info['path']
        .replace("/", "_")
        .replace("{", "")
        .replace("}", "")
        .strip("_")
    )
    method_part = api_info['method'].lower()
    if len(path_part) > 60:
        path_part = path_part[:60]
    return f"test_{method_part}_{path_part}.py"


# ========== 8. 批量生成 ==========
def batch_generate(
        swagger_source: str,
        output_dir: str = "testcase/auto_gen",
        tag_filter: str = None,
        max_count: int = None
):
    """
    批量生成测试用例
    :param swagger_source: Swagger 地址或本地文件路径
    :param output_dir:     输出目录
    :param tag_filter:     只处理指定 tag，None 表示全部
    :param max_count:      最多生成几个，None 表示全部（调试时设为 3）
    """
    global swagger_components

    # 1. 加载 Swagger
    print("📡 正在获取 Swagger 文档...")
    if swagger_source.startswith("http"):
        swagger = fetch_swagger(swagger_source)
    else:
        swagger = load_swagger_file(swagger_source)

    # 2. 保存 components 供 Schema 解析使用
    swagger_components = swagger.get("components", {})
    print(f"✅ components 中 schemas 数量：{len(swagger_components.get('schemas', {}))}")

    # 3. 解析接口
    apis = parse_swagger(swagger)
    print(f"✅ 共解析到 {len(apis)} 个接口")

    # 4. tag 过滤
    if tag_filter:
        apis = [a for a in apis if tag_filter in a.get("tags", [])]
        print(f"🔍 过滤 tag='{tag_filter}' 后剩余：{len(apis)} 个接口")

    # 5. 数量限制（调试用）
    if max_count:
        apis = apis[:max_count]
        print(f"⚠️  限制生成数量：{max_count} 个")

    if not apis:
        print("❌ 没有找到任何接口，请检查 tag_filter 参数")
        return

    # 6. 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 7. 逐个生成
    success_count = 0
    fail_count = 0

    for i, api in enumerate(apis):
        tag_name = api['tags'][0] if api['tags'] else "未分类"
        print(f"\n⏳ [{i + 1}/{len(apis)}] {api['method']} {api['path']}")
        if api['summary']:
            print(f"   描述：{api['summary']}")

        try:
            raw_code = generate_test_cases(api)
            test_code = clean_code(raw_code)

            file_name = make_filename(api)
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(test_code)

            print(f"   ✅ 已生成：{file_path}")
            success_count += 1

        except Exception as e:
            print(f"   ❌ 生成失败：{e}")
            fail_count += 1

    # 8. 汇总
    print(f"\n{'=' * 50}")
    print(f"🎉 全部完成！")
    print(f"   ✅ 成功：{success_count} 个")
    print(f"   ❌ 失败：{fail_count} 个")
    print(f"   📁 保存在：{output_dir}/")
    print(f"{'=' * 50}")


# ========== 入口 ==========
if __name__ == "__main__":

    # 核心业务模块，按优先级分批生成
    CORE_TAGS = [
        # P0 - 最核心
        "Authentication HTTP Basic",  # 1个  - 登录认证
        "Client",  # 19个 - 客户管理
        "Loans",  # 31个 - 贷款核心
        "Savings Account",  # 18个 - 储蓄账户

        # P1 - 重要流程
        "Loan Transactions",  # 22个 - 贷款交易
        "Loan Charges",  # 22个 - 贷款费用
        "Savings Account Transactions",  # 16个 - 储蓄交易
        "Reschedule Loans",  # 5个 - 贷款重组

        # P2 - 系统管理
        "Users",  # 9个 - 用户管理
        "Offices",  # 9个 - 机构管理
    ]

    for tag in CORE_TAGS:
        print(f"\n{'=' * 50}")
        print(f"🚀 开始生成模块：{tag}")
        print(f"{'=' * 50}")
        batch_generate(
            swagger_source=SWAGGER_URL,
            output_dir=f"testcase/auto_gen/{tag}",
            tag_filter=tag,
            max_count=3  # 调试时改为 3，生产时改为 None
        )