import flet as ft
import tkinter as tk
from tkinter import filedialog
from automata import Automata
from formatos import cargar_jff, cargar_json, cargar_xml, exportar_jff, exportar_json, exportar_xml
from lenguajes import prefijos, sufijos
from practica3_utils import validar_lote_cadenas
from kleene_parser import regex_a_automata, regex_a_automata_detallado
from validadores import VALIDADORES_CONFIG, validar_con_validador, construir_afd_validador

def main(page: ft.Page):
    page.title = "Simulador de Autómatas Finitos - Prácticas 2, 3 y 4"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"
    page.padding = 20

    estado_app = {
        "automata": None,
        "nombre_archivo": "Ningún autómata cargado"
    }

    lbl_info = ft.Text(
        "Estado: Esperando archivo o creación manual de autómata", 
        weight=ft.FontWeight.BOLD
    )
    
    txt_ruta = ft.TextField(label="Ruta del archivo seleccionado", width=350, read_only=True)
    lbl_resultado = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    col_traza = ft.Column()

    def abrir_explorador(e):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de autómata",
            filetypes=[("Archivos compatibles", "*.jff;*.json;*.xml"), ("Todos los archivos", "*.*")]
        )
        root.destroy()

        if not file_path:
            return

        txt_ruta.value = file_path
        try:
            if file_path.endswith('.jff'):
                estado_app["automata"] = cargar_jff(file_path)
            elif file_path.endswith('.json'):
                estado_app["automata"] = cargar_json(file_path)
            elif file_path.endswith('.xml'):
                estado_app["automata"] = cargar_xml(file_path)
            else:
                lbl_resultado.value = "✘ Formato no soportado"
                lbl_resultado.color = "red"
                page.update()
                return

            estado_app["nombre_archivo"] = file_path.split("/")[-1].split("\\")[-1]
            auto = estado_app["automata"]
            
            lbl_info.value = f"Archivo: {estado_app['nombre_archivo']} | Tipo: {auto.tipo} | Inicial: {auto.inicial} | Aceptación: {list(auto.aceptacion)}"
            lbl_resultado.value = "✔ Autómata cargado con éxito."
            lbl_resultado.color = "green"
            col_traza.controls.clear()
        except Exception as ex:
            lbl_resultado.value = f"✘ Error al cargar: {ex}"
            lbl_resultado.color = "red"
        page.update()

    btn_explorador = ft.ElevatedButton("📂 Cargar Archivo", on_click=abrir_explorador)

    # Controles para Crear Autómata Manualmente
    txt_estados = ft.TextField(label="Estados (ej. q0,q1,q2)", width=200)
    txt_alfabeto = ft.TextField(label="Alfabeto (ej. a,b)", width=150)
    txt_inicial = ft.TextField(label="Inicial (ej. q0)", width=120)
    txt_aceptacion = ft.TextField(label="Aceptación (ej. q2)", width=150)
    txt_transiciones = ft.TextField(label="Transiciones [desde,símbolo,hacia] (ej. q0,lambda,q1; q1,a,q2)", width=400, multiline=True, height=60)
    dd_tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-lambda"),
        ],
        value="AFD",
        width=130
    )

    def crear_automata_manual(e):
        try:
            estados = {s.strip() for s in txt_estados.value.split(",") if s.strip()}
            alfabeto = {s.strip() for s in txt_alfabeto.value.split(",") if s.strip()}
            inicial = txt_inicial.value.strip()
            aceptacion = {s.strip() for s in txt_aceptacion.value.split(",") if s.strip()}
            
            transiciones = {}
            partes = txt_transiciones.value.split(";")
            for p in partes:
                if not p.strip():
                    continue
                sub = p.split(",")
                if len(sub) == 3:
                    desde, simbolo, hacia = sub[0].strip(), sub[1].strip(), sub[2].strip()
                    if simbolo == 'lambda' or simbolo == 'ε':
                        simbolo = ''
                    key = (desde, simbolo)
                    if key not in transiciones:
                        transiciones[key] = set()
                    transiciones[key].add(hacia)

            nuevo_auto = Automata(
                tipo=dd_tipo.value,
                alfabeto=alfabeto,
                estados=estados,
                inicial=inicial,
                aceptacion=aceptacion,
                transiciones=transiciones
            )

            estado_app["automata"] = nuevo_auto
            estado_app["nombre_archivo"] = "Autómata Creado Manualmente"

            lbl_info.value = f"Archivo: {estado_app['nombre_archivo']} | Tipo: {nuevo_auto.tipo} | Inicial: {nuevo_auto.inicial} | Aceptación: {list(nuevo_auto.aceptacion)}"
            lbl_resultado.value = "✔ ¡Autómata creado exitosamente!"
            lbl_resultado.color = "green"
            col_traza.controls.clear()
        except Exception as ex:
            lbl_resultado.value = f"✘ Error al crear autómata: {ex}"
            lbl_resultado.color = "red"
        page.update()

    btn_crear = ft.ElevatedButton("⚙️ Crear Autómata Manual", on_click=crear_automata_manual)

    def exportar_archivo(e):
        if not estado_app["automata"]:
            lbl_resultado.value = "✘ Primero debes cargar o crear un autómata"
            lbl_resultado.color = "red"
            page.update()
            return

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.asksaveasfilename(
            title="Guardar Autómata",
            defaultextension=".json",
            filetypes=[
                ("Archivo JSON", "*.json"),
                ("Archivo JFF (JFLAP)", "*.jff"),
                ("Archivo XML", "*.xml")
            ]
        )
        root.destroy()

        if not file_path:
            return

        try:
            auto = estado_app["automata"]
            if file_path.endswith('.jff'):
                exportar_jff(auto, file_path)
            elif file_path.endswith('.json'):
                exportar_json(auto, file_path)
            elif file_path.endswith('.xml'):
                exportar_xml(auto, file_path)
            else:
                exportar_json(auto, file_path + ".json")

            lbl_resultado.value = f"✔ Autómata exportado con éxito a {file_path}"
            lbl_resultado.color = "green"
        except Exception as ex:
            lbl_resultado.value = f"✘ Error al exportar: {ex}"
            lbl_resultado.color = "red"
        page.update()

    btn_exportar = ft.ElevatedButton("💾 Exportar Autómata Actual", on_click=exportar_archivo)

    # --- ACCIONES DE LA PRÁCTICA 3 Y OPERACIONES SOBRE AUTÓMATA ---
    def ejecutar_eliminar_lambda(e):
        auto = estado_app["automata"]
        if not auto:
            lbl_resultado.value = "✘ No hay autómata cargado"
            page.update()
            return
        nuevo = auto.eliminar_transiciones_lambda()
        estado_app["automata"] = nuevo
        lbl_info.value = f"Transiciones λ eliminadas | Tipo: {nuevo.tipo} | Estados: {list(nuevo.estados)} | Aceptación: {list(nuevo.aceptacion)}"
        lbl_resultado.value = "✔ Transiciones λ eliminadas exitosamente."
        lbl_resultado.color = "green"
        page.update()

    def ejecutar_subconjuntos(e):
        auto = estado_app["automata"]
        if not auto:
            lbl_resultado.value = "✘ No hay autómata cargado"
            page.update()
            return
        afd, tabla = auto.construir_afd_subconjuntos()
        estado_app["automata"] = afd
        lbl_info.value = f"Convertido a AFD (Subconjuntos) | Inicial: {afd.inicial} | Estados: {list(afd.estados)}"
        lbl_resultado.value = "✔ Construcción de subconjuntos aplicada con éxito."
        lbl_resultado.color = "green"
        
        col_traza.controls.clear()
        col_traza.controls.append(ft.Text("Tabla de Subconjuntos Generada:", weight=ft.FontWeight.BOLD))
        for fila in tabla:
            col_traza.controls.append(ft.Text(f"Estado {fila['estado']} {fila['subconjunto']} -> Transiciones: {fila['transiciones']}"))
        page.update()

    def ejecutar_minimizar(e):
        auto = estado_app["automata"]
        if not auto:
            lbl_resultado.value = "✘ No hay autómata cargado"
            page.update()
            return
        afd_min, particiones = auto.minimizar_afd()
        estado_app["automata"] = afd_min
        lbl_info.value = f"AFD Minimizado | Estados: {list(afd_min.estados)} | Inicial: {afd_min.inicial}"
        lbl_resultado.value = "✔ Minimización de AFD completada."
        lbl_resultado.color = "green"

        col_traza.controls.clear()
        col_traza.controls.append(ft.Text("Particiones en el proceso de minimización:", weight=ft.FontWeight.BOLD))
        for idx, part in enumerate(particiones):
            col_traza.controls.append(ft.Text(f"Ronda {idx}: {[set(g) for g in part]}"))
        page.update()

    def ejecutar_automata_a_regex(e):
        auto = estado_app["automata"]
        if not auto:
            lbl_resultado.value = "✘ No hay autómata cargado"
            page.update()
            return
        try:
            expr, pasos = auto.automata_a_regex_rij()
            lbl_resultado.value = f"✔ Expresión Regular obtenida: {expr}"
            lbl_resultado.color = "green"
            col_traza.controls.clear()
            col_traza.controls.append(ft.Text(f"Resultado Final ER: {expr}", weight=ft.FontWeight.BOLD))
            col_traza.controls.append(ft.Text("Pasos de eliminación (Método Rij):"))
            for numero, (elim, matriz) in enumerate(pasos, start=1):
                col_traza.controls.append(
                    ft.Text(f"Paso {numero}: se elimina el estado {elim}", weight=ft.FontWeight.BOLD)
                )
                for origen, destinos in matriz.items():
                    conexiones = [
                        f"{destino}: {expresion}"
                        for destino, expresion in destinos.items()
                        if expresion != "∅"
                    ]
                    if conexiones:
                        col_traza.controls.append(
                            ft.Text(f"  Desde {origen} -> " + " | ".join(conexiones), size=12)
                        )
            page.update()
        except Exception as ex:
            lbl_resultado.value = f"✘ Error: {ex}"
            lbl_resultado.color = "red"
            page.update()

    def ejecutar_lote(e):
        auto = estado_app["automata"]
        if not auto:
            lbl_resultado.value = "✘ No hay autómata cargado"
            page.update()
            return
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        archivo_in = filedialog.askopenfilename(title="Seleccionar archivo de cadenas (txt)")
        root.destroy()
        
        if not archivo_in:
            return

        try:
            archivo_out = archivo_in.replace(".txt", "_informe.txt")
            total = validar_lote_cadenas(auto, archivo_in, archivo_out)
            lbl_resultado.value = f"✔ Lote procesado: {total} cadenas evaluadas. Informe guardado en {archivo_out}"
            lbl_resultado.color = "green"
        except Exception as ex:
            lbl_resultado.value = f"✘ Error en lote: {ex}"
            lbl_resultado.color = "red"
        page.update()

    btn_elim_lambda = ft.ElevatedButton("⚡ Eliminar Transiciones λ", on_click=ejecutar_eliminar_lambda)
    btn_subconjuntos = ft.ElevatedButton("🔄 Construir AFD (Subconjuntos)", on_click=ejecutar_subconjuntos)
    btn_minimizar = ft.ElevatedButton("📉 Minimizar AFD", on_click=ejecutar_minimizar)
    btn_auto_regex = ft.ElevatedButton("📈 Autómata a ER (Rij)", on_click=ejecutar_automata_a_regex)
    btn_lote = ft.ElevatedButton("📁 Validar Lote de Cadenas", on_click=ejecutar_lote)

    # --- ACCIONES DE LA PRÁCTICA 4 (EXPRESIÓN REGULAR Y VALIDADORES) ---
    txt_regex = ft.TextField(label="Expresión Regular (ej. (a+b)*abb)", width=360)
    pasos_thompson = []
    indice_paso_thompson = {"valor": 0}
    col_thompson = ft.Column(spacing=5)
    lbl_paso_thompson = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def mostrar_paso_thompson():
        col_thompson.controls.clear()
        if not pasos_thompson:
            lbl_paso_thompson.value = "No hay una construcción de Thompson para mostrar."
            page.update()
            return
        indice = indice_paso_thompson["valor"]
        paso = pasos_thompson[indice]
        auto = paso["automata"]
        lbl_paso_thompson.value = (
            f"Paso {indice + 1} de {len(pasos_thompson)}: {paso['operacion']}"
        )
        col_thompson.controls.append(ft.Text(
            f"Estado inicial: {auto.inicial} | Estado final: {', '.join(sorted(auto.aceptacion))}"
        ))
        col_thompson.controls.append(ft.Text(f"Estados: {', '.join(sorted(auto.estados))}"))
        col_thompson.controls.append(ft.Text("Transiciones:"))
        if auto.transiciones:
            for (desde, simbolo), destinos in sorted(auto.transiciones.items()):
                etiqueta = "λ" if simbolo == "" else simbolo
                col_thompson.controls.append(ft.Text(
                    f"  {desde} --{etiqueta}--> {', '.join(sorted(destinos))}"
                ))
        else:
            col_thompson.controls.append(ft.Text("  Sin transiciones (representa ∅)."))
        btn_paso_anterior.disabled = indice == 0
        btn_paso_siguiente.disabled = indice >= len(pasos_thompson) - 1
        page.update()

    def paso_thompson_anterior(e):
        if indice_paso_thompson["valor"] > 0:
            indice_paso_thompson["valor"] -= 1
            mostrar_paso_thompson()

    def paso_thompson_siguiente(e):
        if indice_paso_thompson["valor"] < len(pasos_thompson) - 1:
            indice_paso_thompson["valor"] += 1
            mostrar_paso_thompson()

    btn_paso_anterior = ft.ElevatedButton("← Anterior", on_click=paso_thompson_anterior, disabled=True)
    btn_paso_siguiente = ft.ElevatedButton("Siguiente →", on_click=paso_thompson_siguiente, disabled=True)

    def ejecutar_regex_a_afd(e):
        try:
            expr = txt_regex.value or ""
            resultado = regex_a_automata_detallado(expr)
            afn_lambda = resultado["afn_lambda"]
            afd = resultado["afd"]
            afd_min = resultado["afd_minimo"]
            pasos_thompson[:] = resultado["pasos_thompson"]
            indice_paso_thompson["valor"] = 0
            estado_app["automata"] = afd_min
            estado_app["nombre_archivo"] = f"Regex: {expr}"
            lbl_info.value = (
                f"ER convertida | AFN-λ: {len(afn_lambda.estados)} estados | "
                f"AFD: {len(afd.estados)} estados | AFD mínimo: {len(afd_min.estados)} estados"
            )
            lbl_resultado.value = "✔ Thompson y las conversiones hasta AFD mínimo se completaron."
            lbl_resultado.color = "green"
            col_traza.controls.clear()
            mostrar_paso_thompson()
            page.update()
        except Exception as ex:
            lbl_resultado.value = f"✘ Error en ER: {ex}"
            lbl_resultado.color = "red"
            page.update()

    btn_regex_afd = ft.ElevatedButton("🔤 ER a AFD (Kleene)", on_click=ejecutar_regex_a_afd)

    # Validadores Prácticos
    dd_validador = ft.Dropdown(
        label="Validador Práctico",
        options=[ft.dropdown.Option(k) for k in VALIDADORES_CONFIG.keys()],
        value="Teléfono",
        width=200
    )
    txt_val_cadena = ft.TextField(label="Cadena a probar", width=200)

    lbl_info_validador = ft.Text(size=13, color="blue")

    def ejecutar_validador(e):
        val_nombre = dd_validador.value
        cadena = txt_val_cadena.value or ""
        try:
            afd, afd_minimo = construir_afd_validador(val_nombre)

            # Hacer que el AFD mínimo del validador quede disponible
            # para las funciones generales de simulación y exportación.
            estado_app["automata"] = afd_minimo
            estado_app["nombre_archivo"] = f"AFD mínimo del validador: {val_nombre}"
            lbl_info.value = (
                f"Autómata listo para exportar | Validador: {val_nombre} | "
                f"Tipo: AFD mínimo | Estados: {len(afd_minimo.estados)}"
            )

            aceptada, traza = afd_minimo.simular_cadena(cadena)
            # La fecha requiere además comprobar que el día exista realmente.
            aceptada_final, msg = validar_con_validador(val_nombre, cadena)
            if aceptada_final:
                lbl_resultado.value = f"✔ Validador '{val_nombre}': CADENA ACEPTADA ({msg})"
                lbl_resultado.color = "green"
            else:
                lbl_resultado.value = f"✘ Validador '{val_nombre}': CADENA RECHAZADA ({msg})"
                lbl_resultado.color = "red"
            lbl_info_validador.value = (
                f"Simulación mediante AFD mínimo: {'aceptada' if aceptada else 'rechazada'} | "
                f"Estados del AFD antes de minimizar: {len(afd.estados)} | "
                f"Estados del AFD mínimo: {len(afd_minimo.estados)} | "
                f"Estados recorridos: {len(traza)}"
            )
        except Exception as ex:
            lbl_resultado.value = f"✘ Error al ejecutar validador: {ex}"
            lbl_resultado.color = "red"
            lbl_info_validador.value = ""
        page.update()

    btn_probar_validador = ft.ElevatedButton("🔎 Probar Validador", on_click=ejecutar_validador)

    # Simulación de cadenas
    txt_cadena = ft.TextField(label="Cadena a validar", width=300)

    def validar(e):
        automata_actual = estado_app["automata"]
        if not automata_actual:
            lbl_resultado.value = "✘ Primero debes cargar o crear un autómata"
            lbl_resultado.color = "red"
            page.update()
            return

        cadena = txt_cadena.value or ""
        aceptada, traza = automata_actual.simular_cadena(cadena)
        
        if aceptada:
            lbl_resultado.value = f"✔ Cadena '{cadena}' ACEPTADA"
            lbl_resultado.color = "green"
        else:
            lbl_resultado.value = f"✘ Cadena '{cadena}' RECHAZADA"
            lbl_resultado.color = "red"

        col_traza.controls.clear()
        col_traza.controls.append(ft.Text("Recorrido Paso a Paso:", weight=ft.FontWeight.BOLD))
        for idx, paso in enumerate(traza):
            col_traza.controls.append(ft.Text(f"Paso {idx}: Estado(s) = {set(paso)}"))
        
        page.update()

    btn_validar = ft.ElevatedButton("Validar Cadena", on_click=validar)

    # Operaciones de Lenguajes (Práctica 1)
    txt_cadena_l1 = ft.TextField(label="Cadena para Operaciones", width=300)
    lbl_res_l1 = ft.Text(size=14)

    def op_prefijos(e):
        res = prefijos(txt_cadena_l1.value or "")
        lbl_res_l1.value = f"Prefijos: {list(res)}"
        page.update()

    def op_sufijos(e):
        res = sufijos(txt_cadena_l1.value or "")
        lbl_res_l1.value = f"Sufijos: {list(res)}"
        page.update()

    btn_pref = ft.ElevatedButton("Calcular Prefijos", on_click=op_prefijos)
    btn_suf = ft.ElevatedButton("Calcular Sufijos", on_click=op_sufijos)

    page.add(
        ft.Text("Simulador de Autómatas Finitos - Prácticas 2, 3 y 4", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("1. Gestión de Archivos y Exportación", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([btn_explorador, txt_ruta, btn_exportar], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("2. Crear Autómata Manualmente", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_estados, txt_alfabeto, dd_tipo], alignment=ft.MainAxisAlignment.START),
        ft.Row([txt_inicial, txt_aceptacion, btn_crear], alignment=ft.MainAxisAlignment.START),
        txt_transiciones,
        ft.Divider(),
        ft.Text("3. Operaciones y Conversiones sobre Autómata (Prácticas 3 y 4)", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([btn_elim_lambda, btn_subconjuntos, btn_minimizar], alignment=ft.MainAxisAlignment.START),
        ft.Row([btn_auto_regex, btn_lote], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("4. Expresiones Regulares y Validadores Prácticos (Práctica 4)", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_regex, btn_regex_afd], alignment=ft.MainAxisAlignment.START),
        ft.Text("Construcción de Thompson: avance por los autómatas parciales", weight=ft.FontWeight.BOLD),
        lbl_paso_thompson,
        ft.Row([btn_paso_anterior, btn_paso_siguiente], alignment=ft.MainAxisAlignment.START),
        col_thompson,
        ft.Row([dd_validador, txt_val_cadena, btn_probar_validador], alignment=ft.MainAxisAlignment.START),
        lbl_info_validador,
        ft.Divider(),
        lbl_info,
        ft.Container(height=5),
        ft.Text("5. Validación de Cadenas", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_cadena, btn_validar], alignment=ft.MainAxisAlignment.START),
        lbl_resultado,
        col_traza,
        ft.Divider(),
        ft.Text("6. Operaciones sobre Cadenas (Práctica 1)", size=16, weight=ft.FontWeight.BOLD),
        txt_cadena_l1,
        ft.Row([btn_pref, btn_suf], alignment=ft.MainAxisAlignment.START),
        lbl_res_l1
    )

if __name__ == "__main__":
    ft.app(target=main)