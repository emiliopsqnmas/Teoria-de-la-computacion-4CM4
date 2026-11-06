def prefijos(cadena: str) -> list[str]:
    """Devuelve todos los prefijos de una cadena dada."""
    return [cadena[:i] for i in range(len(cadena) + 1)]

def sufijos(cadena: str) -> list[str]:
    """Devuelve todos los sufijos de una cadena dada."""
    return [cadena[i:] for i in range(len(cadena) + 1)]

def subcadenas(cadena: str) -> list[str]:
    """Devuelve todas las subcadenas únicas de una cadena dada."""
    resultado = set()
    n = len(cadena)
    for i in range(n + 1):
        for j in range(i, n + 1):
            resultado.add(cadena[i:j])
    return sorted(list(resultado), key=lambda x: (len(x), x))

def kleene(alfabeto: list[str], max_longitud: int) -> list[str]:
    """Calcula la cerradura de Kleene Σ* hasta una longitud máxima."""
    if max_longitud < 0:
        return []
    resultado = [""]
    actuales = [""]
    for _ in range(max_longitud):
        siguientes = [c + simbolo for c in actuales for simbolo in alfabeto]
        resultado.extend(siguientes)
        actuales = siguientes
    return resultado

def positiva(alfabeto: list[str], max_longitud: int) -> list[str]:
    """Calcula la cerradura positiva Σ+ hasta una longitud máxima."""
    res_kleene = kleene(alfabeto, max_longitud)
    return [c for c in res_kleene if c != ""]