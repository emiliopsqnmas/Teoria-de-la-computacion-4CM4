import os
import pytest
from automata import Automata
from formatos import (
    exportar_jff, cargar_jff,
    exportar_json, cargar_json,
    exportar_xml, cargar_xml
)

@pytest.fixture
def automata_afd():
    # AFD que acepta cadenas sobre {a, b} que terminan en 'a'
    estados = {'q0', 'q1'}
    alfabeto = {'a', 'b'}
    inicial = 'q0'
    aceptacion = {'q1'}
    transiciones = {
        ('q0', 'a'): 'q1',
        ('q0', 'b'): 'q0',
        ('q1', 'a'): 'q1',
        ('q1', 'b'): 'q0'
    }
    return Automata('AFD', alfabeto, estados, inicial, aceptacion, transiciones)

@pytest.fixture
def automata_lambda():
    # AFND-lambda con transiciones vacias
    estados = {'q0', 'q1'}
    alfabeto = {'a', 'b'}
    inicial = 'q0'
    aceptacion = {'q1'}
    transiciones = {
        ('q0', ''): {'q1'},
        ('q0', 'a'): {'q0'}
    }
    return Automata('AFND-lambda', alfabeto, estados, inicial, aceptacion, transiciones)

def test_simulacion_afd(automata_afd):
    aceptada_valid, _ = automata_afd.simular_cadena("ba")
    assert aceptada_valid is True

    aceptada_invalid, _ = automata_afd.simular_cadena("ab")
    assert aceptada_invalid is False

def test_simulacion_lambda(automata_lambda):
    # La cadena vacia debe ser aceptada por la lambda-clausura de q0 -> q1
    aceptada, _ = automata_lambda.simular_cadena("")
    assert aceptada is True

def test_inversion_formatos(automata_afd, tmp_path):
    f_jff = tmp_path / "test.jff"
    f_json = tmp_path / "test.json"
    f_xml = tmp_path / "test.xml"

    # Probando exportación e importación en JFF
    exportar_jff(automata_afd, str(f_jff))
    auto_jff = cargar_jff(str(f_jff))
    assert auto_jff.estados == automata_afd.estados

    # Probando exportación e importación en JSON
    exportar_json(automata_afd, str(f_json))
    auto_json = cargar_json(str(f_json))
    assert auto_json.estados == automata_afd.estados

    # Probando exportación e importación en XML
    exportar_xml(automata_afd, str(f_xml))
    auto_xml = cargar_xml(str(f_xml))
    assert auto_xml.estados == automata_afd.estados