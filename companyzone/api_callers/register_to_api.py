#Resister through API

import requests

register_url = "http://127.0.0.1:8000/api/Register/"
data = {
    "username":"Srikanth",
    "password":"Srikanth@1234",
    "email":"srikanth@gmail.com"
}
response = requests.post(register_url, json=data)
print(response)
print(response.history)
print(response.url)
print(response.text)
print(response.json)
