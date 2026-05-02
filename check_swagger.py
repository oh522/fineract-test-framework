# import requests
# import json
# import urllib3
# urllib3.disable_warnings()
#
# import base64
# token = base64.b64encode("mifos:password".encode()).decode()
# headers = {
#     "Authorization": f"Basic {token}",
#     "Fineract-Platform-TenantId": "default"
# }
#
# SWAGGER_URL = "https://localhost:8443/fineract-provider/fineract.json"
#
# r = requests.get(SWAGGER_URL, headers=headers, verify=False, timeout=10)
# print(f"状态码：{r.status_code}")
#
# data = r.json()
# paths = data.get("paths", {})
# print(f"✅ paths 数量：{len(paths)}")
#
# # 打印前5个接口
# for i, (path, methods) in enumerate(paths.items()):
#     if i >= 5: break
#     print(f"  {list(methods.keys())} {path}")

import requests, urllib3, base64, json
urllib3.disable_warnings()

token = base64.b64encode("mifos:password".encode()).decode()
headers = {
    "Authorization": f"Basic {token}",
    "Fineract-Platform-TenantId": "default"
}

r = requests.get("https://localhost:8443/fineract-provider/fineract.json",
                  headers=headers, verify=False)
data = r.json()

# 统计每个 tag 下的接口数量
tag_count = {}
for path, methods in data.get("paths", {}).items():
    for method, detail in methods.items():
        if not isinstance(detail, dict): continue
        for tag in detail.get("tags", ["未分类"]):
            tag_count[tag] = tag_count.get(tag, 0) + 1

# 按数量排序输出
print(f"共 {len(tag_count)} 个业务模块：\n")
for tag, count in sorted(tag_count.items(), key=lambda x: -x[1]):
    print(f"  {count:3d} 个接口  |  {tag}")