"""Validaciones estructurales para determinar si un autómata es un AFD."""


def diagnosticar_afd(automata):
    """Devuelve una lista de problemas de determinismo/estructura del autómata."""
    problemas = []
    if not automata.inicial or automata.inicial not in automata.estados:
        problemas.append(f"No existe un estado inicial válido: {automata.inicial!r}.")
    for estado in sorted(automata.aceptacion - automata.estados):
        problemas.append(f"El estado de aceptación {estado!r} no está declarado.")
    for (estado, simbolo), destinos in sorted(automata.transiciones.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        destinos = set(destinos) if isinstance(destinos, (set, frozenset, list, tuple)) else {destinos}
        if estado not in automata.estados:
            problemas.append(f"La transición parte del estado inexistente {estado!r}.")
        for destino in sorted(destinos, key=str):
            if destino not in automata.estados:
                problemas.append(f"La transición desde {estado!r} llega al estado inexistente {destino!r}.")
        if simbolo in ("", "λ", "ε", "lambda"):
            problemas.append(f"El estado {estado!r} tiene una transición λ; no es un AFD.")
        elif len(destinos) > 1:
            problemas.append(
                f"No es determinista: desde el estado {estado!r} con el símbolo {simbolo!r} "
                f"hay {len(destinos)} destinos ({', '.join(map(str, sorted(destinos, key=str)))})."
            )
    return problemas


def es_afd(automata):
    """True si el autómata es estructuralmente determinista (se permiten transiciones faltantes)."""
    return not diagnosticar_afd(automata)
