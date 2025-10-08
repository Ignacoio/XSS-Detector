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


