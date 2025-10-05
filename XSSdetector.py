import requests
url="http://127.0.0.1:5000"
with open("payloads.txt", encoding="utf-8") as f:
    payloads= f.readlines()

for payload in payloads: 
    payload = payload.strip()
    params= {'name':payload}
    r= requests.get(url, params=params)

    if payload in r.text:
     print(f"posiblemente vulnerable a XSS: {payload}")

    else:
     print(f"no vulnerable a XSS: {payload}")