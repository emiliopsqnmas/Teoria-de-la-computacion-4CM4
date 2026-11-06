
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


