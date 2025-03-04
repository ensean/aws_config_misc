from openai import OpenAI
openai_api_key = "sk-1234"
openai_api_base_url = "http://35.78.xx.xx:8102/v1"

client = OpenAI(api_key = openai_api_key, base_url = openai_api_base_url)
response = client.completions.create(
  model="ds-r1-7b",
  prompt="鸡猪 36，共有 100 足，问鸡猪各有多少只？",
  stream=False,
  max_tokens=4096,
)
print(response.choices[0].text)