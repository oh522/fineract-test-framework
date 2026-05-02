import requests
import urllib3

urllib3.disable_warnings()

url = "https://localhost:8443/fineract-provider/api/v1/clients/1?command=activate"


payload = {
    "activationDate": "02 May 2026",
    "dateFormat": "dd MMMM yyyy",
    "locale": "en"
}

headers = {
    "Authorization": "Basic xxxxx",  # 你的token
    "Content-Type": "application/json"
}

res = requests.post(url, json=payload, headers=headers, verify=False)

print("状态码:", res.status_code)
print("响应:", res.text)