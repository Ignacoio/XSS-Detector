import requests
url="http://127.0.0.1:5000"
headers = {"User-Agent": "curl/7.88.1","X-Forwarded-For": "203.0.113.195, 70.41.3.18, 150.172.238.178"}
timeout=6
methods= ["GET","POST"]

with open("payloads.txt", encoding="utf-8") as f:
    payloads= f.readlines()

session = requests.Session()

for payload in payloads: 
    payload = payload.strip()
    params= {'name':payload}
    data={"message": payload}
    
    
    for m in methods:
        try:
            if m == "GET":
                r = session.request("GET", url, params=params, timeout=timeout, headers=headers)
            else:
                 r = session.request("POST", url, data=data, timeout=timeout, headers=headers)
        except requests.exceptions.Timeout as t:
            print("se ha acabado el tiempo", t)
            continue
        except requests.exceptions.RequestException as e:
            print("hay un error en los requests", e)
            continue

        if payload in r.text:
            print(f"posiblemente vulnerable a XSS ({m}): {payload}")
        else:
            print(f"no vulnerable a XSS ({m}): {payload}")

session.close()