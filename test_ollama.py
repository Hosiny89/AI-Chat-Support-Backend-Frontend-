import requests, json

url = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "gemma2:2b",
    "prompt": "Hello, how are you?"
}

response = requests.post(url, json=payload, stream=True)

full_response = ""
for line in response.iter_lines():
    if line:
        data = line.decode("utf-8")
        obj = json.loads(data)
        if "response" in obj:
            full_response += obj["response"]

print(full_response)
