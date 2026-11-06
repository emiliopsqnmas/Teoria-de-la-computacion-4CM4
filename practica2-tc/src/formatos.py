import json
import xml.etree.ElementTree as ET
from automata import Automata

def cargar_jff(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    automaton = root.find('automaton')

    estados = set()
    inicial = None
    aceptacion = set()
    id_a_nombre = {}

    for state in automaton.findall('state'):
        e_id = state.get('id')
        nombre = state.get('name', f"q{e_id}")
        id_a_nombre[e_id] = nombre
        estados.add(nombre)
        if state.find('initial') is not None:
            inicial = nombre
        if state.find('final') is not None:
            aceptacion.add(nombre)

    transiciones = {}
    alfabeto = set()
    es_lambda = False
    es_nd = False

    for trans in automaton.findall('transition'):
        desde = id_a_nombre[trans.find('from').text]
        hacia = id_a_nombre[trans.find('to').text]
        read_elem = trans.find('read')
        simbolo = read_elem.text if (read_elem is not None and read_elem.text) else ''

        if simbolo == '':
            es_lambda = True
        else:
            alfabeto.add(simbolo)

        key = (desde, simbolo)
        if key not in transiciones:
            transiciones[key] = set()
        elif len(transiciones[key]) > 0:
            es_nd = True
        transiciones[key].add(hacia)

    tipo = 'AFND-lambda' if es_lambda else ('AFND' if es_nd else 'AFD')
    return Automata(tipo, alfabeto, estados, inicial, aceptacion, transiciones)

def exportar_jff(automata, ruta):
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "fa"
    automaton = ET.SubElement(root, "automaton")

    nombre_a_id = {nombre: str(i) for i, nombre in enumerate(sorted(automata.estados))}
    for nombre, e_id in nombre_a_id.items():
        state = ET.SubElement(automaton, "state", id=e_id, name=nombre)
        if nombre == automata.inicial:
            ET.SubElement(state, "initial")
        if nombre in automata.aceptacion:
            ET.SubElement(state, "final")

    for (desde, simbolo), hacia_set in automata.transiciones.items():
        destinos = hacia_set if isinstance(hacia_set, (set, frozenset)) else {hacia_set}
        for hacia in destinos:
            trans = ET.SubElement(automaton, "transition")
            ET.SubElement(trans, "from").text = nombre_a_id[desde]
            ET.SubElement(trans, "to").text = nombre_a_id[hacia]
            read_elem = ET.SubElement(trans, "read")
            if simbolo != '':
                read_elem.text = simbolo

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(ruta, encoding="utf-8", xml_declaration=True)

def exportar_json(automata, ruta):
    trans_list = []
    for (desde, lee), hacia_set in automata.transiciones.items():
        if isinstance(hacia_set, (set, frozenset)):
            hacia_list = list(hacia_set)
        else:
            hacia_list = [hacia_set]
        trans_list.append({"desde": desde, "lee": lee, "hacia": hacia_list})

    data = {
        "tipo": automata.tipo,
        "alfabeto": sorted(list(automata.alfabeto)),
        "estados": sorted(list(automata.estados)),
        "inicial": automata.inicial,
        "aceptacion": sorted(list(automata.aceptacion)),
        "transiciones": trans_list
    }
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cargar_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transiciones = {}
    for t in data["transiciones"]:
        key = (t["desde"], t["lee"])
        transiciones[key] = set(t["hacia"])

    return Automata(
        data["tipo"],
        set(data["alfabeto"]),
        set(data["estados"]),
        data["inicial"],
        set(data["aceptacion"]),
        transiciones
    )

def exportar_xml(automata, ruta):
    root = ET.Element("automata", tipo=automata.tipo)
    alf_elem = ET.SubElement(root, "alfabeto")
    for sim in sorted(automata.alfabeto):
        ET.SubElement(alf_elem, "simbolo").text = sim
        
    est_elem = ET.SubElement(root, "estados")
    for est in sorted(automata.estados):
        kwargs = {"nombre": est}
        if est == automata.inicial:
            kwargs["inicial"] = "true"
        if est in automata.aceptacion:
            kwargs["aceptacion"] = "true"
        ET.SubElement(est_elem, "estado", **kwargs)

    trans_elem = ET.SubElement(root, "transiciones")
    for (desde, lee), hacia_set in automata.transiciones.items():
        destinos = hacia_set if isinstance(hacia_set, (set, frozenset)) else {hacia_set}
        for hacia in destinos:
            ET.SubElement(trans_elem, "transicion", desde=desde, lee=lee, hacia=hacia)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(ruta, encoding="utf-8", xml_declaration=True)

def cargar_xml(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()
    tipo = root.get("tipo", "AFD")
    alfabeto = {s.text for s in root.find("alfabeto").findall("simbolo")}
    
    estados = set()
    inicial = None
    aceptacion = set()
    for e in root.find("estados").findall("estado"):
        nombre = e.get("nombre")
        estados.add(nombre)
        if e.get("inicial") == "true":
            inicial = nombre
        if e.get("aceptacion") == "true":
            aceptacion.add(nombre)
            
    transiciones = {}
    for t in root.find("transiciones").findall("transicion"):
        desde = t.get("desde")
        lee = t.get("lee", "")
        hacia = t.get("hacia")
        key = (desde, lee)
        if key not in transiciones:
            transiciones[key] = set()
        transiciones[key].add(hacia)

    return Automata(tipo, alfabeto, estados, inicial, aceptacion, transiciones)