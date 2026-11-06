"""Validadores prácticos construidos y ejecutados mediante AFD.

El AFD valida el patrón regular. Para fechas, datetime añade la comprobación
semántica de calendario (por ejemplo, febrero y años bisiestos), que no queda
cubierta únicamente por el patrón de forma.
"""
from datetime import date
import re  # Se conserva para las pruebas de congruencia con re.fullmatch.
from kleene_parser import parse_regex, thompson_construction
from automata import Automata

DIGITO = "(" + "+".join("0123456789") + ")"


def repetir(expresion: str, cantidad: int) -> str:
    return "".join(f"({expresion})" for _ in range(cantidad))


# Diez dígitos exactos.
REGEX_TELEFONO_CURSO = repetir(DIGITO, 10)
REGEX_TELEFONO_PY = r"[0-9]{10}"

# AAAA-MM-DD. El AFD exige cuatro dígitos, mes 01..12 y día 01..31.
# La existencia exacta del día se comprueba después con datetime.date.
DIGITOS = DIGITO
MES = "(0(" + "+".join("123456789") + ")+1(0+1+2))"
DIA = "(0(" + "+".join("123456789") + ")+1" + DIGITOS + "+2" + DIGITOS + "+3(0+1))"
REGEX_FECHA_CURSO = repetir(DIGITOS, 4) + "-" + MES + "-" + DIA
REGEX_FECHA_PY = r"[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])"

# Criterio definido para contraseña: exactamente 8 caracteres ASCII alfanuméricos.
CARACTER_ALFANUMERICO = "(" + "+".join(
    list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + list("abcdefghijklmnopqrstuvwxyz") + list("0123456789")
) + ")"
REGEX_PASSWORD_CURSO = repetir(CARACTER_ALFANUMERICO, 8)
REGEX_PASSWORD_PY = r"[A-Za-z0-9]{8}"

VALIDADORES_CONFIG = {
    "Teléfono": {
        "regex_curso": REGEX_TELEFONO_CURSO,
        "regex_py": REGEX_TELEFONO_PY,
        "ejemplo_valido": "5512345678",
        "descripcion": "Exactamente 10 dígitos (0-9).",
    },
    "Fecha": {
        "regex_curso": REGEX_FECHA_CURSO,
        "regex_py": REGEX_FECHA_PY,
        "ejemplo_valido": "2024-02-29",
        "descripcion": "Formato AAAA-MM-DD; el calendario se comprueba adicionalmente.",
    },
    "Contraseña": {
        "regex_curso": REGEX_PASSWORD_CURSO,
        "regex_py": REGEX_PASSWORD_PY,
        "ejemplo_valido": "Clave123",
        "descripcion": "Exactamente 8 caracteres ASCII: letras mayúsculas, minúsculas o dígitos; sin espacios ni símbolos.",
    },
}

_CACHE = {}


def construir_afd_validador(nombre: str):
    """Devuelve (afd_sin_minimizar, afd_minimo) construidos con Thompson."""
    if nombre not in VALIDADORES_CONFIG:
        raise ValueError(f"Validador '{nombre}' no encontrado.")
    if nombre not in _CACHE:
        expresion = VALIDADORES_CONFIG[nombre]["regex_curso"]
        arbol = parse_regex(expresion)
        inicial, final, estados, transiciones, _ = thompson_construction(arbol)
        afn_lambda = Automata(
            tipo="AFND-lambda", alfabeto={s for (_, s) in transiciones if s != ""},
            estados=estados, inicial=inicial, aceptacion={final}, transiciones=transiciones
        )
        afn = afn_lambda.eliminar_transiciones_lambda()
        afd, _ = afn.construir_afd_subconjuntos()
        afd_minimo, _ = afd.minimizar_afd()
        _CACHE[nombre] = (afd, afd_minimo)
    return _CACHE[nombre]


def validar_con_validador(tipo: str, valor: str):
    """Valida la cadena simulándola en el AFD mínimo del validador."""
    if tipo not in VALIDADORES_CONFIG:
        return False, f"Validador '{tipo}' no encontrado."
    if valor is None or valor == "":
        return False, "El campo está vacío."

    try:
        _, afd_minimo = construir_afd_validador(tipo)
        aceptada, _ = afd_minimo.simular_cadena(valor)
        if not aceptada:
            return False, "La cadena fue rechazada por el AFD mínimo."

        if tipo == "Fecha":
            anio, mes, dia = map(int, valor.split("-"))
            try:
                date(anio, mes, dia)
            except ValueError:
                return False, "El AFD reconoce el formato, pero la fecha no existe en el calendario."
        return True, "Cadena aceptada por el AFD mínimo."
    except Exception as exc:
        return False, f"No fue posible ejecutar el validador: {exc}"
