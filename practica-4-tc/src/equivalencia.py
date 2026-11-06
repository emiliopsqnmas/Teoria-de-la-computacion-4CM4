"""Comparación formal de equivalencia entre autómatas deterministas.

Las transiciones faltantes se interpretan como rechazo (estado pozo implícito).
La búsqueda en el producto devuelve una cadena testigo cuando los lenguajes difieren.
"""
from collections import deque

from validacion_afd import diagnosticar_afd


def _destino(automata, estado, simbolo):
    if estado is None:
        return None
    destinos = automata.transiciones.get((estado, simbolo))
    if not destinos:
        return None
    destinos = set(destinos)
    if len(destinos) != 1:
        raise ValueError("La comparación requiere AFD deterministas.")
    return next(iter(destinos))


def comparar_afd(afd_a, afd_b):
    """Compara dos AFD y devuelve (equivalentes, testigo, detalle).

    testigo es la cadena más corta encontrada que uno acepta y el otro rechaza.
    None significa que no existe testigo y los lenguajes son equivalentes.
    """
    problemas_a = diagnosticar_afd(afd_a)
    problemas_b = diagnosticar_afd(afd_b)
    if problemas_a or problemas_b:
        detalle = []
        if problemas_a:
            detalle.append("Primer autómata: " + " ".join(problemas_a))
        if problemas_b:
            detalle.append("Segundo autómata: " + " ".join(problemas_b))
        raise ValueError("No se pueden comparar: " + " ".join(detalle))

    alfabeto = sorted(set(afd_a.alfabeto) | set(afd_b.alfabeto))
    inicial = (afd_a.inicial, afd_b.inicial)
    pendientes = deque([(inicial, "")])
    visitados = {inicial}

    while pendientes:
        (estado_a, estado_b), cadena = pendientes.popleft()
        acepta_a = estado_a is not None and estado_a in afd_a.aceptacion
        acepta_b = estado_b is not None and estado_b in afd_b.aceptacion
        if acepta_a != acepta_b:
            return False, cadena, (
                f"El primer AFD {'acepta' if acepta_a else 'rechaza'} la cadena "
                f"y el segundo {'acepta' if acepta_b else 'rechaza'}."
            )

        for simbolo in alfabeto:
            siguiente = (
                _destino(afd_a, estado_a, simbolo),
                _destino(afd_b, estado_b, simbolo),
            )
            if siguiente not in visitados:
                visitados.add(siguiente)
                pendientes.append((siguiente, cadena + simbolo))

    return True, None, "Ambos AFD reconocen exactamente el mismo lenguaje."


def comparar_minimizados(afd_a, afd_b):
    """Minimiza ambos AFD antes de comprobar la equivalencia."""
    minimo_a, _ = afd_a.minimizar_afd()
    minimo_b, _ = afd_b.minimizar_afd()
    equivalente, testigo, detalle = comparar_afd(minimo_a, minimo_b)
    return {
        "equivalentes": equivalente,
        "testigo": testigo,
        "detalle": detalle,
        "afd_a_minimo": minimo_a,
        "afd_b_minimo": minimo_b,
    }
