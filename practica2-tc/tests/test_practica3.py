import pytest
from automata import Automata

def test_equivalencia_transformaciones():
    alfabeto = {'0', '1'}
    estados = {'q0', 'q1', 'q2'}
    inicial = 'q0'
    aceptacion = {'q2'}
    transiciones = {
        ('q0', '0'): {'q0', 'q1'},
        ('q0', '1'): {'q0'},
        ('q1', '1'): {'q2'}
    }
    
    afn = Automata('AFND', alfabeto, estados, inicial, aceptacion, transiciones)
    
    # Construcción de subconjuntos
    afd, _ = afn.construir_afd_subconjuntos()
    
    # Minimización
    afd_min, _ = afd.minimizar_afd()
    
    # Comprobar aceptación idéntica de cadenas de prueba
    cadenas_prueba = ["", "0", "1", "01", "001", "1010", "011", "0001"]
    for c in cadenas_prueba:
        res_afn, _ = afn.simular_cadena(c)
        res_afd, _ = afd.simular_cadena(c)
        res_min, _ = afd_min.simular_cadena(c)
        
        assert res_afn == res_afd == res_min, f"Discrepancia en la cadena '{c}'"
    
    # Comprobar que el AFD mínimo no tiene más estados que el AFD original
    assert len(afd_min.estados) <= len(afd.estados)