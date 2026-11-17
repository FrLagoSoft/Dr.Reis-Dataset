# Quick test script for api.py, starts the server at local 5000 and makes some requests to it. Requests are easily visible below with show...

import requests

BASE = "http://127.0.0.1:5000"


def show(title, r):
    print(f"--- {title} ---")
    print("Status:", r.status_code)
    print(r.json())
    print()


show("GET /hello", requests.get(BASE + "/hello"))
show("GET /data?limit=3", requests.get(BASE + "/data", params={"limit": 3}))

new = {"temperature_c": 24.5, "ph": 8.1, "note": "test reading"}
show("POST /data", requests.post(BASE + "/data", json=new))

# should come back with 400 since ph is missing
show("POST /data (bad)", requests.post(BASE + "/data", json={"temperature_c": 25}))

show("GET /data after POST", requests.get(BASE + "/data", params={"limit": 1}))
show("GET /nope (404)", requests.get(BASE + "/nope"))
