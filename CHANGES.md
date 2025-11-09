Changes:
# Changelog
## [2025-11-09]

### Files modificados
- `app.py`
- `XSSdetector.py`


---


### app.py
#### Added
- Se ha añadido un header de defensa `response.headers['X-Content-Type-Options'] = 'nosniff'`, que mitiga el header de ataque conocido como `X-Content-Type-Options`.
- Se ha añadido al header de defensa la politica de defensa conocida como `Content-Security-Policy`:  `response.headers['Content-Security-Policy']`
- Las medidas de seguridad se muestran "#", para que el usuario prueba las dos versiones; la version con las politicas y mitigacion de defensa y la versión insegura.
- IMPORTANTE, la politica CSP, se ha puesto lo más restrictiva posible, eso implica, que, aunque los scripts sean propios, no se podrán ejecutar. En este caso, no es necesario ponerlos en modo "self" porque el servidor tiene las minimas funciones posibles, pero lo recomendado es ser un poco más laxo con la seguridad, para poder ejecutar archivos propios.

#### Objetivo / Beneficio
- Al añadir esta capa de defensa(CSP),CSP define qué fuentes de contenido son confiables, evitando que scripts maliciosos se ejecuten en la página.
- El header X-Content-Type-Options: nosniff le indica al navegador que no adivine el tipo de un archivo y respete estrictamente el Content-Type, evitando que contenido malicioso se ejecute como scripts y reduciendo el riesgo de XSS.

---
### XSSdetector.py
#### Added
- Se han añadido dos nuevos headers de ataque: `headers = {"User-Agent": "curl/7.88.1","X-Forwarded-For": "203.0.113.195, 70.41.3.18, 150.172.238.178"}`

#### Objetivo / Beneficio
- El header `User-Agent`, indica al servidor información sobre el navegador o cliente que realiza la petición; puede ser manipulado por un atacante para evadir filtros.
- El header `X-Forwarded-For`, permite al ataque falsificar la dirección IP, gracias a una ruta, por la que la IP falsa recorre unos supuestos proxies.

# Changelog
## [2025-10-20]

### Files modificados
- `app.py`
- `XSSdetector.py`
- `payloads.txt`


---

### app.py
#### Changed
- Se ha añadido la mitigación del parametro POST con escape (al igual que el parametro GET) return f"{escape(message)}"

#### Objetivo / Beneficio
- Prevenir XSS reflejado: escapar el contenido recibido vía POST evita que caracteres especiales (<, >, &, ", ', etc.) se interpreten como HTML/JS en la respuesta, reduciendo la probabilidad de ejecución de scripts maliciosos.

---
### XSSdetector.py
#### Added
- Nuevos parametros creados: session = `requests.Session()` y `session.close()`

#### Changed:
- Se cambio la función `r = requests.get(url, params=params, timeout=timeout)` por `r = session.request("GET", url, params=params, timeout=timeout)`
- Se cambio la función  `r = requests.post(url, data=data, timeout=timeout)` por `r = session.request("POST", url, data=data, timeout=timeout)`

#### Objetivo / Beneficio
- Al añadir Session, reutilizo conexiones TCP/HTTP. Por lo que si se hacen muchas peticiones seguidas, es más rápida y consume mucho menos recursos.
- Configuración centraliza.
- El codigo se vuelve más flexible.
- En futuras mejoras nos permitirá construir y desarrollar headers.

---
### payloads.txt
#### Added
- Se han añadido los siguientes payloads:
1. "><script>alert(1)</script>
2. '><img src=x onerror=alert(1)>
3. <a href="javascript:alert(1)">link</a>
4. <body onload=alert(1)>
5. <input value="X" onfocus=alert(1) autofocus>
6. "><iframe srcdoc="<script>alert(1)</script>"></iframe>
7. &#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;
8. %3Cscript%3Ealert(1)%3C%2Fscript%3E
9. <img src=1 onerror=confirm(1)>

#### Objetivo / Beneficio
- Comprueba muchos mas tipos de payloads.






# Changelog

## [2025-10-11]

### Files modificados
- `app.py`
- `XSSdetector.py`

---

### app.py
#### Added
- Ruta POST en `'/'` para recibir form-data. (`@app.route('/', methods=['POST'])`)
- Lectura de parámetros POST mediante `request.form.get("message", "hola que tal")`.

#### Changed
- Mantener la ruta GET en `'/'` con `@app.route('/', methods=['GET'])`.
- GET sigue leyendo `name` desde query-string con `request.args.get('name', 'Juan')`.


#### Objetivo / Beneficio
- Permitir que la aplicación devuelva/refleje valores enviados por POST (útil para pruebas de XSS y para que el scanner detecte payloads en el body).
- Separar claramente el manejo GET / POST manteniendo la interfaz simple y explícita.

---
## XSSdetector.py
#### Added
- Se creo la variable `data={"message": payload}`

### Changed
- Se cambió la llamada `requests.post(url, params=params, timeout=timeout)` por `requests.post(url, data=data, timeout=timeout)`, de modo que el detector envía los payloads como form-data y puede comprobar correctamente vulnerabilidades reflejadas por POST en `app.py`.

#### Objetivo / Beneficio
- Permitir que el scanner detecte inyecciones XSS en parámetros recibidos vía cuerpo de formulario (POST), no solo en la query string (GET).  
- Mejora la cobertura de pruebas al incluir ambos vectores (GET y POST), lo que aumenta la probabilidad de encontrar vulnerabilidades reales.  
- Evita falsos negativos debidos a enviar datos en el lugar equivocado (query vs body), haciendo el escaneo más preciso y fiable.




# Changelog

## [2025-10-08]
### Added in the XSSdetector.py
- Soporte para métodos POST en el scanner.
- Manejo de excepciones Timeout y RequestException.
- Timeout de 6 segundos por petición.

### Changed
- Se añadieron un parametro: timeout=6 y una lista  methods= ["GET","POST"]
- Se limpia la cadena (`payload.strip()`) y se forma `params = {'name': payload}`
- Se itera sobre la lista methods (GET y POST) y para cada metodo:
    - Si el método es "GET", se hace una petición `GET` con `requests.get(url, params=params, timeout=timeout)`.
    - Si el método es otro (aquí "POST"), se hace una petición `POST` con `requests.post(url, params=params, timeout=timeout)`.
- Cada petición incluye un timeout para evitar que una petición se quede colgada.
- Se desarrollan dos excepciones:
    - `requests.exceptions.Timeout`: cuando la petición supera el tiempo máximo configurado; se imprime un mensaje y se continúa con el siguiente payload/método.
    - `requests.exceptions.RequestException`: captura errores generales de requests (conexión, DNS, URL inválida, etc.); se informa y se continúa.

**Objetivo y beneficio:**
- Evitar que fallos de red o peticiones lentas detengan todo el escaneo.  
- Probar tanto GET como POST con el mismo flujo de trabajo para cubrir endpoints que reciban datos por querystring o por formulario.  
- Mantener el bucle de pruebas funcionando incluso si algunas peticiones fallan, facilitando escaneos largos y menos propensos a interrupciones.

