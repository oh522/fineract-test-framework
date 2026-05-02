# debug_loan.py
from api_test.common.base_api import BaseApi
import json

api = BaseApi()

# 查询所有贷款产品
resp = api.get("/loanproducts")
print(f"状态码：{resp.status_code}")
products = resp.json()
print(f"共 {len(products)} 个贷款产品：")
for p in products:
    print(f"  id: {p['id']}, name: {p['name']}, shortName: {p.get('shortName')}")