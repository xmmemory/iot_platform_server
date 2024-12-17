
import requests 
resp = requests.post("http://127.0.0.1:9013/login", json={"username": "lrl001","password": "123"})
print(resp, resp.text)