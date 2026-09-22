import flet as ft
from lenguajes import prefijos, sufijos, subcadenas, kleene, positiva

def main(page: ft.Page):
    page.title = "Operaciones Básicas sobre Lenguajes"
    page.padding = 20
    page.scroll = "auto"

    cadena_input = ft.TextField(label="Cadena de entrada (para prefijos/sufijos/subcadenas)", width=400)
    alfabeto_input = ft.TextField(label="Alfabeto (separado por comas, ej: a,b)", width=300)
    longitud_input = ft.TextField(label="Longitud máxima", width=150, value="2")

    salida = ft.Text(value="", selectable=True)

    def procesar_cadena(e):
        val = cadena_input.value or ""
        p = prefijos(val)
        s = sufijos(val)
        sub = subcadenas(val)
        salida.value = (
            f"Cadena: '{val}'\n\n"
            f"Prefijos ({len(p)}): {p}\n\n"
            f"Sufijos ({len(s)}): {s}\n\n"
            f"Subcadenas ({len(sub)}): {sub}"
        )
        page.update()

    def procesar_lenguaje(e):
        raw_alfabeto = alfabeto_input.value or ""
        alfabeto = [x.strip() for x in raw_alfabeto.split(",") if x.strip()]
        try:
            n = int(longitud_input.value)
        except ValueError:
            n = 0

        res_kleene = kleene(alfabeto, n)
        res_pos = positiva(alfabeto, n)

        salida.value = (
            f"Alfabeto: {alfabeto} | Longitud máx: {n}\n\n"
            f"Cerradura de Kleene Σ* ({len(res_kleene)} cadenas):\n{res_kleene}\n\n"
            f"Cerradura Positiva Σ+ ({len(res_pos)} cadenas):\n{res_pos}"
        )
        page.update()

    btn_cadena = ft.ElevatedButton("Calcular Prefijos / Sufijos / Subcadenas", on_click=procesar_cadena)
    btn_lenguaje = ft.ElevatedButton("Calcular Σ* y Σ+", on_click=procesar_lenguaje)

    page.add(
        ft.Text("Práctica 1 - Teoría de la Computación", size=20, weight="bold"),
        ft.Divider(),
        cadena_input,
        btn_cadena,
        ft.Divider(),
        ft.Row([alfabeto_input, longitud_input]),
        btn_lenguaje,
        ft.Divider(),
        ft.Text("Resultados:", weight="bold"),
        salida
    )

ft.app(target=main)