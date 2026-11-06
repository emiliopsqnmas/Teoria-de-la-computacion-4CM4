"""Operaciones algebraicas y simplificación de expresiones regulares.

Notación: + unión, concatenación implícita, * clausura, ε cadena vacía,
∅ lenguaje vacío. La representación interna usa árboles para evitar
simplificaciones inseguras basadas en sustituciones de texto.
"""

EMPTY = ("empty",)
EPSILON = ("epsilon",)

def literal(value):
    return ("lit", str(value))

def union(*items):
    """Unión con identidad ∅, idempotencia y absorción por cerradura."""
    flat = []
    for item in items:
        if item == EMPTY:
            continue
        flat.extend(item[1] if item[0] == "union" else (item,))
    unique = []
    for item in flat:
        if item not in unique:
            unique.append(item)
    if not unique:
        return EMPTY
    if len(unique) == 1:
        return unique[0]

    # R + RR* = R* y R + R*R = R*.
    for candidate in unique:
        if candidate[0] != "concat" or len(candidate[1]) != 2:
            continue
        left, right = candidate[1]
        if right[0] == "star" and right[1] == left and left in unique:
            return star(left)
        if left[0] == "star" and left[1] == right and right in unique:
            return star(right)

    # ε + RR* = R* y ε + R*R = R*.
    if EPSILON in unique:
        for candidate in unique:
            if candidate[0] != "concat" or len(candidate[1]) != 2:
                continue
            left, right = candidate[1]
            if right[0] == "star" and right[1] == left:
                return star(left)
            if left[0] == "star" and left[1] == right:
                return star(right)

    return ("union", tuple(sorted(unique, key=render)))

def concat(*items):
    """Construye concatenación aplicando identidad, anulación y asociatividad."""
    flat = []
    for item in items:
        if item == EMPTY:
            return EMPTY
        flat.extend(item[1] if item[0] == "concat" else (item,))
    flat = [x for x in flat if x != EPSILON]
    if not flat:
        return EPSILON
    reducidos = []
    for item in flat:
        if (reducidos and reducidos[-1][0] == "star" and item[0] == "star"
                and reducidos[-1][1] == item[1]):
            continue
        reducidos.append(item)
    if len(reducidos) == 1:
        return reducidos[0]
    return ("concat", tuple(reducidos))

def star(item):
    if item in (EMPTY, EPSILON):
        return EPSILON
    if item[0] == "star":
        return item
    return ("star", item)

def _precedence(node):
    return {"union": 1, "concat": 2, "star": 3}.get(node[0], 4)

def render(node, parent=0):
    kind = node[0]
    if kind == "empty":
        value = "∅"
    elif kind == "epsilon":
        value = "ε"
    elif kind == "lit":
        value = node[1]
    elif kind == "union":
        value = "+".join(render(x, 1) for x in node[1])
    elif kind == "concat":
        value = "".join(render(x, 2) for x in node[1])
    elif kind == "star":
        value = render(node[1], 3) + "*"
    else:
        raise ValueError(f"Nodo de expresión desconocido: {kind}")
    return f"({value})" if _precedence(node) < parent else value

def simplify(node):
    """Aplica reglas algebraicas hasta alcanzar una forma estable."""
    if node[0] in ("empty", "epsilon", "lit"):
        return node
    if node[0] == "star":
        return star(simplify(node[1]))
    if node[0] == "concat":
        return concat(*(simplify(x) for x in node[1]))
    if node[0] == "union":
        result = union(*(simplify(x) for x in node[1]))
        # Absorción: R + RR* = R* y R + R*R = R*.
        if result[0] == "union":
            parts = list(result[1])
            for item in parts:
                if item[0] == "concat":
                    factors = item[1]
                    if len(factors) == 2 and (
                        (factors[0][0] == "star" and factors[0][1] in parts and factors[1] == factors[0][1]) or
                        (factors[1][0] == "star" and factors[1][1] in parts and factors[0] == factors[1][1])
                    ):
                        return star(factors[0][1] if factors[0][0] == "star" else factors[1][1])
        return result
    return node

def parse_simple_regex(expression):
    """Analizador pequeño para la notación del curso (+, concatenación, *, paréntesis)."""
    s = expression.replace(" ", "")
    if not s:
        raise ValueError("La expresión regular está vacía")
    tokens = []
    for i, ch in enumerate(s):
        tokens.append(ch)
        if i + 1 < len(s):
            nxt = s[i + 1]
            if ch not in "(+" and nxt not in ")+*":
                tokens.append(".")
    output, ops = [], []
    prec = {"+": 1, ".": 2, "*": 3}
    for ch in tokens:
        if ch not in "()+*.":
            output.append(literal(ch))
        elif ch == "(":
            ops.append(ch)
        elif ch == ")":
            while ops and ops[-1] != "(":
                output.append(ops.pop())
            if not ops:
                raise ValueError("Paréntesis no balanceados")
            ops.pop()
        elif ch == "*":
            if not output:
                raise ValueError("Operador * sin operando")
            output.append(star(output.pop()))
        else:
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[ch]:
                op = ops.pop()
                right, left = output.pop(), output.pop()
                output.append(union(left, right) if op == "+" else concat(left, right))
            ops.append(ch)
    while ops:
        op = ops.pop()
        if op == "(":
            raise ValueError("Paréntesis sin cerrar")
        right, left = output.pop(), output.pop()
        output.append(union(left, right) if op == "+" else concat(left, right))
    if len(output) != 1:
        raise ValueError("Expresión regular mal formada")
    return simplify(output[0])
