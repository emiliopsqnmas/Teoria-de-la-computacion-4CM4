# MOLINA CORDOVA CARLOS EMILIO-2025630042
# Práctica 4 – Teoría de la Computación - 4CV4

Programa desarrollado en Python para trabajar con expresiones regulares y autómatas finitos. Permite convertir expresiones regulares en autómatas, convertir autómatas en expresiones regulares y validar cadenas.

## Requisitos

- Python 3.11, 3.12 o 3.13.
- Dependencias incluidas en `requirements.txt`.

## Instalación y ejecución

Desde la carpeta `practica-4-tc`, ejecuta:

```bash
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Inicia el programa:

```bash
PYTHONPATH=src python src/app.py
```

## Funciones principales

- Convertir expresiones regulares en autómatas finitos.
- Construir autómatas mediante el método de Thompson.
- Eliminar transiciones λ y convertir AFN a AFD.
- Minimizar autómatas deterministas.
- Obtener expresiones regulares mediante el método de eliminación de estados (Rij).
- Comparar autómatas para comprobar si son equivalentes.
- Validar cadenas y utilizar validadores de teléfono, fecha y contraseña.
- Importar y exportar archivos compatibles con JFLAP (`.jff`).

## Pruebas

Para ejecutar las pruebas automatizadas:

```bash
PYTHONPATH=src python -m pytest -q
```

## Módulos principales

| Archivo | Función |
|---|---|
| `src/app.py` | Interfaz gráfica del programa. |
| `src/automata.py` | Operaciones y conversiones de autómatas. |
| `src/kleene_parser.py` | Análisis de expresiones regulares y construcción de Thompson. |
| `src/regex_simplifier.py` | Simplificación de expresiones regulares. |
| `src/validadores.py` | Validadores de teléfono, fecha y contraseña. |
| `src/formatos.py` | Importación y exportación de archivos. |

## Notación utilizada

El programa utiliza la notación del curso:

- `+` Unión.
- Concatenación: escribir las expresiones juntas.
- `*` Cerradura de Kleene.
- `λ` Cadena vacía.
- `∅` Lenguaje vacío.

La precedencia es: primero `*`, después concatenación y finalmente `+`.
