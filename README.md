# XSS Tester (Proyecto Junior)

**Demo local de XSS reflejado + script de testing automático**.  
Objetivo: aprender a detectar XSS reflejado, documentar evidencia y mostrar la mitigación mínima.

---

## Características
- Servidor Flask local vulnerable (ruta `/` lee `?name=` y lo muestra).
- `XSSjunior.py`: script que lee `payloads.txt`, envía payloads y reporta si se reflejan.
- Versión mitigada incluida usando `markupsafe.escape()`.

---

## Requisitos
- Python 3.8+  
- Instala dependencias:
```bash
python -m pip install -r requirements.txt
