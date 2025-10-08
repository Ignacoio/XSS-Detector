import requests
url="http://127.0.0.1:5000"
timeout=6
methods= ["GET","POST"]

with open("payloads.txt", encoding="utf-8") as f:
    payloads= f.readlines()

for payload in payloads: 
    payload = payload.strip()
    params= {'name':payload}
    
    
    for m in methods:
        try:
            if m == "GET":
                r = requests.get(url, params=params, timeout=timeout)
            else:
                r = requests.post(url, params=params, timeout=timeout)
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