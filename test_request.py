import requests

url = "http://127.0.0.1:5000/chat"
payload = {"question": "Hello, how are you?"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)

try:
    print("Response:", response.json())
except ValueError:
    print("Non-JSON response received:", response.text)
    