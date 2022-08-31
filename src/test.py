import requests

while True:
    requests.post("http://127.0.0.1:5000/api/shorten", headers={"url": "https://www.google.com"})