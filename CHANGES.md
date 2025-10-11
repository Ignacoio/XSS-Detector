Changes:
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


