import random
import re
from datetime import date, timedelta

from validadores import (
    VALIDADORES_CONFIG,
    construir_afd_validador,
    validar_con_validador,
)


def cadenas_telefono(rng):
    validas = ["".join(rng.choice("0123456789") for _ in range(10)) for _ in range(250)]
    invalidas = [
        "".join(rng.choice("0123456789") for _ in range(rng.choice([0, 1, 8, 9, 11, 12])))
        for _ in range(125)
    ]
    invalidas += ["55A2345678", "5512-45678", "abcdefghij", " 5512345678"]
    invalidas += ["".join(rng.choice("abcXYZ!@") for _ in range(10)) for _ in range(121)]
    return validas + invalidas


def cadenas_fecha(rng):
    validas = []
    inicio = date(1900, 1, 1)
    for _ in range(250):
        d = inicio + timedelta(days=rng.randrange(0, 365 * 125))
        validas.append(d.strftime("%Y-%m-%d"))
    invalidas = [
        "2024-00-10", "2024-13-01", "2024-01-00", "2024-01-32",
        "24-01-01", "2024/01/01", "2024-1-01", "abcd-ef-gh",
    ]
    invalidas += [
        f"{rng.randrange(1000, 10000)}-{rng.choice(['00', '13', '99'])}-{rng.randrange(1, 32):02d}"
        for _ in range(242)
    ]
    return validas + invalidas


def cadenas_password(rng):
    alfanumericos = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    validas = ["".join(rng.choice(alfanumericos) for _ in range(8)) for _ in range(250)]
    invalidas = [
        "".join(rng.choice(alfanumericos) for _ in range(n))
        for n in [0, 1, 7, 9, 10, 12] * 40
    ]
    invalidas += ["Clave 12", "Clave_12", "Clave-12", "ábcdef12", "!!!!!!!!", "1234567!", "Aaaaaaa!", "12345678", "abcdefgh", "ABCDEFGH"]
    return validas + invalidas


def test_congruencia_afd_vs_re_fullmatch_500_cadenas_por_validador():
    rng = random.Random(20261106)
    generadores = {
        "Teléfono": cadenas_telefono,
        "Fecha": cadenas_fecha,
        "Contraseña": cadenas_password,
    }
    for nombre, config in VALIDADORES_CONFIG.items():
        afd_sin_minimizar, afd_minimo = construir_afd_validador(nombre)
        assert len(afd_minimo.estados) <= len(afd_sin_minimizar.estados)
        cadenas = generadores[nombre](rng)
        assert len(cadenas) >= 500
        for cadena in cadenas:
            resultado_afd, _ = afd_minimo.simular_cadena(cadena)
            resultado_python = re.fullmatch(config["regex_py"], cadena) is not None
            assert resultado_afd == resultado_python, (nombre, cadena, resultado_afd, resultado_python)


def test_fecha_rechaza_dias_imposibles_y_acepta_bisiestos():
    assert validar_con_validador("Fecha", "2024-02-29")[0]
    assert validar_con_validador("Fecha", "2000-02-29")[0]
    assert not validar_con_validador("Fecha", "2023-02-29")[0]
    assert not validar_con_validador("Fecha", "2026-02-30")[0]
    assert not validar_con_validador("Fecha", "1900-02-29")[0]


def test_telefono_exige_exactamente_diez_digitos():
    assert validar_con_validador("Teléfono", "5512345678")[0]
    assert not validar_con_validador("Teléfono", "551234567")[0]
    assert not validar_con_validador("Teléfono", "55123456789")[0]
    assert not validar_con_validador("Teléfono", "55A2345678")[0]


def test_contrasena_exige_ocho_caracteres_alfanumericos():
    assert validar_con_validador("Contraseña", "Clave123")[0]
    assert not validar_con_validador("Contraseña", "Clave12")[0]
    assert not validar_con_validador("Contraseña", "Clave 12")[0]
    assert not validar_con_validador("Contraseña", "Clave_12")[0]


def test_simplificador_algebraico_basico():
    from regex_simplifier import parse_simple_regex, render, EMPTY, EPSILON, literal, union, concat, star

    a = literal("a")
    assert render(union(a, a)) == "a"                 # R + R = R
    assert render(concat(a, EPSILON)) == "a"          # Rε = R
    assert render(concat(a, EMPTY)) == "∅"             # R∅ = ∅
    assert render(star(star(a))) == "a*"               # (R*)* = R*
    assert render(parse_simple_regex("a+a")) == "a"
    assert render(parse_simple_regex("a+aa*")) == "a*"


def test_rij_devuelve_pasos_con_matriz_y_simplifica():
    from automata import Automata

    auto = Automata(
        tipo="AFD",
        alfabeto={"a"},
        estados={"q0", "q1"},
        inicial="q0",
        aceptacion={"q1"},
        transiciones={("q0", "a"): {"q1"}, ("q1", "a"): {"q1"}},
    )
    expresion, pasos = auto.automata_a_regex_rij()
    assert expresion == "aa*"
    assert len(pasos) == 2
    assert all(isinstance(matriz, dict) for _, matriz in pasos)


def test_analizador_notacion_curso_lambda_y_vacio():
    from kleene_parser import regex_a_automata

    afd_lambda = regex_a_automata("λ")
    assert afd_lambda.simular_cadena("")[0]
    assert not afd_lambda.simular_cadena("a")[0]

    afd_vacio = regex_a_automata("∅")
    assert not afd_vacio.simular_cadena("")[0]
    assert not afd_vacio.simular_cadena("a")[0]

    afd_cerradura_vacio = regex_a_automata("∅*")
    assert afd_cerradura_vacio.simular_cadena("")[0]
    assert not afd_cerradura_vacio.simular_cadena("a")[0]


def test_analizador_rechaza_expresiones_mal_formadas_con_posicion():
    import pytest
    from kleene_parser import parse_regex, RegexSyntaxError

    for expresion in ["a+", "+a", "a++b", "(a+b", "a)b", "()"]:
        with pytest.raises(RegexSyntaxError, match=r"posición"):
            parse_regex(expresion)


def test_thompson_muestra_pasos_y_no_colisiona_estados():
    from kleene_parser import construir_afn_thompson, regex_a_automata

    afn, pasos = construir_afn_thompson("(0(1+2)+1(0+1+2))")
    assert pasos
    assert len(afn.estados) == len(set(afn.estados))
    afd = regex_a_automata("(0(1+2)+1(0+1+2))")
    assert afd.simular_cadena("01")[0]
    assert afd.simular_cadena("12")[0]
    assert not afd.simular_cadena("1")[0]



def test_exportacion_jflap_de_todas_las_etapas_regex(tmp_path):
    from kleene_parser import regex_a_automata_detallado
    from formatos import exportar_jff, cargar_jff

    resultado = regex_a_automata_detallado("(a+b)*ab")
    etapas = ["afn_lambda", "afn", "afd", "afd_minimo"]
    cadenas = ["", "a", "b", "ab", "aab", "babab", "abb", "ba"]

    for etapa in etapas:
        ruta = tmp_path / f"{etapa}.jff"
        original = resultado[etapa]
        exportar_jff(original, str(ruta))
        recuperado = cargar_jff(str(ruta))
        assert recuperado.estados == original.estados
        assert recuperado.inicial == original.inicial
        assert recuperado.aceptacion == original.aceptacion
        for cadena in cadenas:
            assert recuperado.simular_cadena(cadena)[0] == original.simular_cadena(cadena)[0]


def test_conversion_regex_entrega_cuatro_etapas_y_mantiene_lenguaje():
    from kleene_parser import regex_a_automata_detallado

    resultado = regex_a_automata_detallado("(a+b)*ab")
    assert set(("afn_lambda", "afn", "afd", "afd_minimo")).issubset(resultado)
    cadenas = ["", "a", "b", "ab", "aab", "babab", "abb", "ba"]
    referencia = resultado["afn_lambda"]
    for etapa in ("afn", "afd", "afd_minimo"):
        for cadena in cadenas:
            assert resultado[etapa].simular_cadena(cadena)[0] == referencia.simular_cadena(cadena)[0]


def test_diagnostico_afd_detecta_transicion_lambda_y_no_determinismo():
    from automata import Automata
    from validacion_afd import diagnosticar_afd, es_afd

    no_determinista = Automata(
        tipo="AFND-lambda", alfabeto={"a"}, estados={"q0", "q1", "q2"},
        inicial="q0", aceptacion={"q2"},
        transiciones={("q0", "a"): {"q1", "q2"}, ("q1", ""): {"q2"}},
    )
    problemas = diagnosticar_afd(no_determinista)
    assert not es_afd(no_determinista)
    assert any("estado 'q0'" in p and "símbolo 'a'" in p for p in problemas)
    assert any("transición λ" in p for p in problemas)


def test_diagnostico_afd_acepta_afd_con_transiciones_parciales():
    from automata import Automata
    from validacion_afd import diagnosticar_afd, es_afd

    afd = Automata(
        tipo="AFD", alfabeto={"a", "b"}, estados={"q0", "q1"},
        inicial="q0", aceptacion={"q1"}, transiciones={("q0", "a"): {"q1"}},
    )
    assert diagnosticar_afd(afd) == []
    assert es_afd(afd)


def test_rij_guarda_matriz_reducida_en_cada_eliminacion():
    from automata import Automata
    afd = Automata(
        tipo="AFD", alfabeto={"a", "b"}, estados={"q0", "q1", "q2"},
        inicial="q0", aceptacion={"q2"},
        transiciones={("q0", "a"): {"q1"}, ("q1", "b"): {"q2"}},
    )
    expresion, pasos = afd.automata_a_regex_rij()
    assert len(pasos) == 3
    for estado_eliminado, matriz in pasos:
        assert estado_eliminado not in matriz
        assert all(estado_eliminado not in destinos for destinos in matriz.values())
    assert expresion not in ("", "∅")



def test_equivalencia_afd_minimizados_acepta_lenguajes_iguales():
    from automata import Automata
    from equivalencia import comparar_minimizados

    a = Automata("AFD", {"a", "b"}, {"q0", "q1"}, "q0", {"q1"},
                 {("q0", "a"): {"q1"}, ("q1", "a"): {"q1"}})
    b = Automata("AFD", {"a", "b"}, {"s", "f", "muerto"}, "s", {"f"},
                 {("s", "a"): {"f"}, ("s", "b"): {"muerto"},
                  ("f", "a"): {"f"}, ("f", "b"): {"muerto"},
                  ("muerto", "a"): {"muerto"}, ("muerto", "b"): {"muerto"}})
    resultado = comparar_minimizados(a, b)
    assert resultado["equivalentes"] is True
    assert resultado["testigo"] is None


def test_equivalencia_devuelve_testigo_mas_corto():
    from automata import Automata
    from equivalencia import comparar_afd

    acepta_a = Automata("AFD", {"a"}, {"q0", "q1"}, "q0", {"q1"},
                        {("q0", "a"): {"q1"}})
    rechaza_todo = Automata("AFD", {"a"}, {"s"}, "s", set(), {})
    equivalente, testigo, detalle = comparar_afd(acepta_a, rechaza_todo)
    assert equivalente is False
    assert testigo == "a"
    assert "acepta" in detalle


def test_equivalencia_rechaza_automata_no_determinista():
    import pytest
    from automata import Automata
    from equivalencia import comparar_afd

    afnd = Automata("AFND", {"a"}, {"q0", "q1", "q2"}, "q0", {"q2"},
                    {("q0", "a"): {"q1", "q2"}})
    afd = Automata("AFD", {"a"}, {"s"}, "s", set(), {})
    with pytest.raises(ValueError, match="No se pueden comparar"):
        comparar_afd(afnd, afd)
