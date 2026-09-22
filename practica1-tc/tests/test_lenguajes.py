import pytest
from lenguajes import prefijos, sufijos, subcadenas, kleene, positiva

def test_cadena_vacia():
    assert prefijos("") == [""]
    assert sufijos("") == [""]
    assert subcadenas("") == [""]

def test_alfabeto_un_simbolo():
    assert kleene(["a"], 2) == ["", "a", "aa"]
    assert positiva(["a"], 2) == ["a", "aa"]

def test_longitud_uno():
    assert prefijos("a") == ["", "a"]
    assert sufijos("a") == ["a", ""]

def test_diferencia_kleene_positiva_longitud_cero():
    alfabeto = ["a", "b"]
    res_kleene = kleene(alfabeto, 0)
    res_positiva = positiva(alfabeto, 0)
    
    assert res_kleene == [""]
    assert res_positiva == []
    assert res_kleene != res_positiva