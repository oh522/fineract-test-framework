from openai import OpenAI

client = OpenAI(
    api_key="sk-77a776b9d740407ca50fa535d6a31e57",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)