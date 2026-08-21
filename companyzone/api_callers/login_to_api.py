#Login to API

import requests

login_url = "http://127.0.0.1:8000/api/Login/"
credentials = {
    "username":"Srikanth",
    "password":"Srikanth@1234"
}
response = requests.post(login_url, json=credentials)
print(response)
print(response.history)
print(response.url)
print(response.text)
print(response.json)
