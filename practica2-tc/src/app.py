import flet as ft
import tkinter as tk
from tkinter import filedialog, messagebox
from automata import Automata
from formatos import cargar_jff, cargar_json, cargar_xml, exportar_jff, exportar_json, exportar_xml
from lenguajes import prefijos, sufijos

def main(page: ft.Page):
    page.title = "Simulador de Autómatas Finitos - Práctica 2"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = "adaptive"
    page.padding = 20

    estado_app = {
        "automata": Automata(
            tipo='AFD',
            alfabeto={'a', 'b'},
            estados={'q0', 'q1'},
            inicial='q0',
            aceptacion={'q1'},
            transiciones={
                ('q0', 'a'): 'q1',
                ('q0', 'b'): 'q0',
                ('q1', 'a'): 'q1',
                ('q1', 'b'): 'q0'
            }
        ),
        "nombre_archivo": "Autómata por defecto (AFD)"
    }

    lbl_info = ft.Text(
        f"Archivo: {estado_app['nombre_archivo']} | Tipo: {estado_app['automata'].tipo} | Inicial: {estado_app['automata'].inicial} | Aceptación: {list(estado_app['automata'].aceptacion)}", 
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
    txt_transiciones = ft.TextField(label="Transiciones [desde,símbolo,hacia] (ej. q0,a,q1;q1,b,q2)", width=400, multiline=True, height=60)
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
                    # Permitir transición lambda vacía representada como ''
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

    # Funciones de Exportación
    def exportar_archivo(e):
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

    # Simulación de cadenas
    txt_cadena = ft.TextField(label="Cadena a validar", width=300)

    def validar(e):
        automata_actual = estado_app["automata"]
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
        ft.Text("Simulador de Autómatas Finitos - Práctica 2", size=22, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("1. Gestión de Archivos y Exportación", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([btn_explorador, txt_ruta, btn_exportar], alignment=ft.MainAxisAlignment.START),
        ft.Divider(),
        ft.Text("2. Crear Autómata Manualmente", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_estados, txt_alfabeto, dd_tipo], alignment=ft.MainAxisAlignment.START),
        ft.Row([txt_inicial, txt_aceptacion, btn_crear], alignment=ft.MainAxisAlignment.START),
        txt_transiciones,
        ft.Divider(),
        lbl_info,
        ft.Container(height=5),
        ft.Text("3. Validación de Cadenas", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([txt_cadena, btn_validar], alignment=ft.MainAxisAlignment.START),
        lbl_resultado,
        col_traza,
        ft.Divider(),
        ft.Text("4. Operaciones sobre Cadenas (Práctica 1)", size=16, weight=ft.FontWeight.BOLD),
        txt_cadena_l1,
        ft.Row([btn_pref, btn_suf], alignment=ft.MainAxisAlignment.START),
        lbl_res_l1
    )

if __name__ == "__main__":
    ft.app(target=main)