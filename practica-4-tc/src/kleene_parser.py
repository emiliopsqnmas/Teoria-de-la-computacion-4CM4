"""Analizador de expresiones regulares y construcción de Thompson.

Notación del curso: + (unión), concatenación implícita, * (Kleene),
λ/ε (palabra vacía), ∅ (lenguaje vacío) y paréntesis.
Cada símbolo ordinario representa un símbolo del alfabeto.
"""
from dataclasses import dataclass
from typing import Optional

from automata import Automata


class Node:
    pass


@dataclass
class LiteralNode(Node):
    char: str


@dataclass
class EpsilonNode(Node):
    pass


@dataclass
class EmptyNode(Node):
    pass


@dataclass
class ConcatNode(Node):
    left: Node
    right: Node


@dataclass
class UnionNode(Node):
    left: Node
    right: Node


@dataclass
class KleeneNode(Node):
    node: Node


class RegexSyntaxError(ValueError):
    """Error sintáctico que conserva la posición original del problema."""
    def __init__(self, message: str, position: int):
        self.position = position
        super().__init__(f"{message} (posición {position + 1})")


_PRECEDENCE = {"+": 1, ".": 2, "*": 3}
_ATOMS = {"λ", "ε", "∅"}
_OPERATORS = set("+*()")


def _tokenize(expression: str):
    # Se conserva la posición original, aunque se ignoren espacios.
    tokens = [(char, pos) for pos, char in enumerate(expression) if not char.isspace()]
    if not tokens:
        raise RegexSyntaxError("La expresión regular está vacía", 0)

    normalized = []
    for char, pos in tokens:
        normalized.append(("λ" if char == "ε" else char, pos))

    # Inserta concatenación cuando termina un átomo/cierre/estrella y
    # comienza otro átomo/apertura.
    result = []
    can_end = lambda c: c not in "+("  # literal, λ, ∅, ), *
    can_start = lambda c: c not in "+*)"  # literal, λ, ∅, (
    for index, item in enumerate(normalized):
        result.append(item)
        if index + 1 < len(normalized):
            current, _ = item
            following, next_pos = normalized[index + 1]
            if can_end(current) and can_start(following):
                result.append((".", next_pos))
    return result


def _to_postfix(tokens):
    output = []
    operators = []
    expecting_operand = True
    open_positions = []

    for token, pos in tokens:
        if token == "(":
            if not expecting_operand:
                raise RegexSyntaxError("Falta un operador antes de '('", pos)
            operators.append((token, pos))
            open_positions.append(pos)
            expecting_operand = True
        elif token == ")":
            if expecting_operand:
                raise RegexSyntaxError("Paréntesis vacío o falta un operando antes de ')'", pos)
            while operators and operators[-1][0] != "(":
                output.append(operators.pop()[0])
            if not operators:
                raise RegexSyntaxError("Paréntesis de cierre sin apertura", pos)
            operators.pop()
            open_positions.pop()
            expecting_operand = False
        elif token in ("λ", "∅") or token not in _OPERATORS and token != ".":
            if not expecting_operand:
                raise RegexSyntaxError("Falta un operador entre símbolos", pos)
            output.append(token)
            expecting_operand = False
        elif token == "*":
            if expecting_operand:
                raise RegexSyntaxError("El operador '*' necesita un operando a su izquierda", pos)
            # Estrella es postfija y se emite inmediatamente.
            output.append(token)
        elif token in ("+", "."):
            if expecting_operand:
                nombre = "unión '+'" if token == "+" else "concatenación"
                raise RegexSyntaxError(f"Falta un operando antes de {nombre}", pos)
            while operators and operators[-1][0] != "(" and _PRECEDENCE[operators[-1][0]] >= _PRECEDENCE[token]:
                output.append(operators.pop()[0])
            operators.append((token, pos))
            expecting_operand = True

    if expecting_operand:
        last_pos = tokens[-1][1]
        raise RegexSyntaxError("La expresión termina con un operador o paréntesis incompleto", last_pos)
    if open_positions:
        raise RegexSyntaxError("Paréntesis de apertura sin cerrar", open_positions[-1])
    while operators:
        op, pos = operators.pop()
        if op == "(":
            raise RegexSyntaxError("Paréntesis de apertura sin cerrar", pos)
        output.append(op)
    return output


def parse_regex(regex_str: str) -> Node:
    """Analiza la expresión y devuelve su árbol sintáctico abstracto."""
    postfix = _to_postfix(_tokenize(regex_str))
    stack = []
    for token in postfix:
        if token == "λ":
            stack.append(EpsilonNode())
        elif token == "∅":
            stack.append(EmptyNode())
        elif token == "*":
            if not stack:
                raise ValueError("Error interno: '*' sin operando")
            stack.append(KleeneNode(stack.pop()))
        elif token in (".", "+"):
            if len(stack) < 2:
                raise ValueError(f"Error interno: operador '{token}' sin dos operandos")
            right, left = stack.pop(), stack.pop()
            stack.append(ConcatNode(left, right) if token == "." else UnionNode(left, right))
        else:
            stack.append(LiteralNode(token))
    if len(stack) != 1:
        raise ValueError("Expresión regular mal formada")
    return stack[0]


def _merge_transitions(*mappings):
    merged = {}
    for mapping in mappings:
        for key, destinations in mapping.items():
            merged.setdefault(key, set()).update(destinations)
    return {key: frozenset(value) for key, value in merged.items()}


def thompson_construction(node: Node, state_counter: int = 0):
    """Construye un fragmento Thompson: inicio, fin, estados, transiciones, contador."""
    counter = state_counter

    def new_state(states):
        nonlocal counter
        state = f"q{counter}"
        counter += 1
        states.add(state)
        return state

    if isinstance(node, LiteralNode):
        states = set()
        start, accept = new_state(states), new_state(states)
        transitions = {(start, node.char): frozenset({accept})}
    elif isinstance(node, EpsilonNode):
        states = set()
        start, accept = new_state(states), new_state(states)
        transitions = {(start, ""): frozenset({accept})}
    elif isinstance(node, EmptyNode):
        states = set()
        start, accept = new_state(states), new_state(states)
        transitions = {}  # No existe camino: reconoce el lenguaje vacío.
    elif isinstance(node, ConcatNode):
        ls, la, lst, lt, _ = thompson_construction(node.left, counter)
        counter = _max_state_number(lst) + 1
        rs, ra, rst, rt, _ = thompson_construction(node.right, counter)
        states = set(lst) | set(rst)
        start, accept = ls, ra
        transitions = _merge_transitions(lt, rt, {(la, ""): {rs}})
    elif isinstance(node, UnionNode):
        ls, la, lst, lt, _ = thompson_construction(node.left, counter)
        counter = _max_state_number(lst) + 1
        rs, ra, rst, rt, _ = thompson_construction(node.right, counter)
        counter = _max_state_number(rst) + 1
        states = set(lst) | set(rst)
        start, accept = new_state(states), new_state(states)
        transitions = _merge_transitions(lt, rt, {(start, ""): {ls, rs}, (la, ""): {accept}, (ra, ""): {accept}})
    elif isinstance(node, KleeneNode):
        sub_start, sub_accept, sub_states, sub_transitions, _ = thompson_construction(node.node, counter)
        counter = _max_state_number(sub_states) + 1
        states = set(sub_states)
        start, accept = new_state(states), new_state(states)
        transitions = _merge_transitions(sub_transitions, {
            (start, ""): {sub_start, accept},
            (sub_accept, ""): {sub_start, accept},
        })
    else:
        raise TypeError(f"Nodo sintáctico desconocido: {type(node).__name__}")
    return start, accept, states, transitions, counter


def _max_state_number(states):
    return max((int(state[1:]) for state in states if state.startswith("q") and state[1:].isdigit()), default=-1)


def _postorder(node):
    if isinstance(node, (ConcatNode, UnionNode)):
        yield from _postorder(node.left)
        yield from _postorder(node.right)
    elif isinstance(node, KleeneNode):
        yield from _postorder(node.node)
    yield node


def _node_label(node):
    if isinstance(node, LiteralNode): return f"Símbolo '{node.char}'"
    if isinstance(node, EpsilonNode): return "Palabra vacía λ"
    if isinstance(node, EmptyNode): return "Lenguaje vacío ∅"
    if isinstance(node, ConcatNode): return "Concatenación"
    if isinstance(node, UnionNode): return "Unión (+)"
    if isinstance(node, KleeneNode): return "Cerradura (*)"
    return type(node).__name__


def construir_afn_thompson(regex_str: str):
    """Devuelve (AFN-λ final, pasos); cada paso contiene un fragmento parcial.

    Los pasos se presentan en orden de construcción postorden, indicando
    qué operación se acaba de incorporar y el fragmento resultante.
    """
    root = parse_regex(regex_str)
    steps = []
    for index, subnode in enumerate(_postorder(root), start=1):
        start, accept, states, transitions, _ = thompson_construction(subnode)
        alphabet = {symbol for (_, symbol) in transitions if symbol}
        partial = Automata("AFND-lambda", alphabet, states, start, {accept}, transitions)
        steps.append({"numero": index, "operacion": _node_label(subnode), "automata": partial})

    start, accept, states, transitions, _ = thompson_construction(root)
    alphabet = {symbol for (_, symbol) in transitions if symbol}
    final_nfa = Automata("AFND-lambda", alphabet, states, start, {accept}, transitions)
    return final_nfa, steps


def regex_a_automata_detallado(regex_str: str):
    """Devuelve AFN-λ, pasos Thompson, AFD y AFD mínimo."""
    afn_lambda, steps = construir_afn_thompson(regex_str)
    afn = afn_lambda.eliminar_transiciones_lambda()
    afd, tabla_subconjuntos = afn.construir_afd_subconjuntos()
    afd_minimo, particiones = afd.minimizar_afd()
    return {
        "afn_lambda": afn_lambda,
        "pasos_thompson": steps,
        "afn": afn,
        "afd": afd,
        "tabla_subconjuntos": tabla_subconjuntos,
        "afd_minimo": afd_minimo,
        "particiones": particiones,
    }


def regex_a_automata(regex_str: str):
    """Compatibilidad con la interfaz anterior: retorna el AFD mínimo."""
    return regex_a_automata_detallado(regex_str)["afd_minimo"]
