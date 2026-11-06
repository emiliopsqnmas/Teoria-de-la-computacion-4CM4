# Simulador de Autómatas Finitos — Teoría de la Computación

Aplicación de escritorio/web con Flet para trabajar con autómatas finitos,
expresiones regulares y validadores prácticos.

## Requisitos
- Python 3.11, 3.12 o 3.13
- Dependencias de `requirements.txt`

## Instalación y ejecución
Desde esta carpeta:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python src/app.py
```

## Pruebas
```bash
PYTHONPATH=src python -m pytest -q
```

## Módulos principales
- `src/automata.py`: simulación, conversión, minimización y método Rij.
- `src/kleene_parser.py`: análisis de ER, validación sintáctica con posición del error, construcción de Thompson y conversión hasta AFD mínimo.
- `src/regex_simplifier.py`: representación algebraica y reglas de simplificación.
- `src/validadores.py`: validadores de teléfono, fecha y contraseña.
- `src/formatos.py`: importación y exportación JFLAP, JSON y XML.


Para ejecutar las pruebas desde la carpeta del proyecto:

```bash
PYTHONPATH=src pytest -q
```

La prueba automatizada de esta versión se ejecutó en Python 3.13: **14 pruebas aprobadas**.
Todavía debe verificarse la misma suite en Python 3.11 y 3.12 mediante los contenedores
configurados en `entorno/compose.yml`.



Reglas implementadas y cubiertas:
- Unión: `R + ∅ = R` y `R + R = R`.
- Concatenación: `Rε = εR = R`, `R∅ = ∅R = ∅`.
- Cerradura: `∅* = ε`, `ε* = ε` y `(R*)* = R*`.
- Cerraduras consecutivas: `R*R* = R*`.
- Absorción: `R + RR* = R*`, `R + R*R = R*`, `ε + RR* = R*` y `ε + R*R = R*`.

La simplificación se aplica al construir las operaciones y en cada actualización de
la matriz del método Rij. No se afirma que el módulo obtenga una forma algebraica
canónica para toda expresión: por ejemplo, la distributividad no se aplica como
reescritura general.

Pruebas de esta etapa: `PYTHONPATH=src pytest -q` — **18 pruebas aprobadas en Python 3.13**.
