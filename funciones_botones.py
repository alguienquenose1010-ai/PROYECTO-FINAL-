import flet as ft
from jugar import Jugar



def mostrar_inicio(page):

    page.controls.clear()

    text = ft.Text(
        "Bienvenido al juego de ajedrez.",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED,
    )

    image = ft.Image(
        src="https://flet.dev/img/logo.svg", 
        width=100, 
        height=100
    )

    button1 = ft.ElevatedButton(
        content=ft.Text("JUGAR"),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=lambda e: jugar(page)
    )
    button2 = ft.ElevatedButton(
        content=ft.Text("VER GANADORES DE PARTIDAS ANTERIORES"),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=lambda e: ver_ganadores(page)
    )

    button3 = ft.ElevatedButton(
        content=ft.Text("¿CÓMO MOVER LAS PIEZAS?"),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=lambda e: mostrar_instrucciones(page)
    )

    page.add(text, image, button1, button2, button3)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

def mostrar_instrucciones(page):

    page.controls.clear()
    page.add(ft.Text("Los movimientos se escriben en notación UCI: origen + destino."))
    page.add(ft.Text("Ejemplos:"))
    page.add(ft.Text("Peón de e2 a e4 → e2e4"))
    page.add(ft.Text("Caballo de g1 a f3 → g1f3"))
    page.add(ft.Text("Alfil de c1 a d3 → c1d3"))
    page.add(ft.Text("Enroque corto de rey → e1g1"))
    page.add(ft.Text("Enroque largo de rey → e1c1"))
    page.add(ft.ElevatedButton(content=ft.Text("Volver"), on_click=lambda e: mostrar_inicio(page)))
    page.update()

def jugar(page):

    page.controls.clear()

    instrucciones = ft.Text(
        "Jugador 1 será BLANCAS y Jugador 2 será NEGRAS.\n"
        "Reglas para los nombres:\n"
        "- Ambos deben estar completos.\n"
        "- Cada nombre debe tener al menos 3 caracteres.\n"
        "- No pueden ser iguales.",
        size=16,
        color="blue"
    )

    jugador1 = ft.TextField(hint_text="Nombre del jugador 1 (Blancas)")
    jugador2 = ft.TextField(hint_text="Nombre del jugador 2 (Negras)")
    error_text = ft.Text(value="", color="red", size=16)

    def validar(e):
        nombre1 = jugador1.value.strip()
        nombre2 = jugador2.value.strip()

        if not nombre1 or not nombre2:
            error_text.value = "⚠️ Debes ingresar ambos nombres."
        elif len(nombre1) < 3 or len(nombre2) < 3:
            error_text.value = "⚠️ Cada nombre debe tener al menos 3 caracteres."
        elif nombre1 == nombre2:
            error_text.value = "⚠️ Los nombres no pueden ser iguales."
        else:
            error_text.value = ""
            Jugar(page, nombre1, nombre2)
        page.update()

    page.add(
        instrucciones,
        jugador1,
        jugador2,
        ft.ElevatedButton(content=ft.Text("JUGAR"), on_click=validar),
        ft.ElevatedButton(content=ft.Text("Volver"), on_click=lambda e: mostrar_inicio(page)),
        error_text
    )

    page.update()

def ver_ganadores(page):
    page.controls.clear()
    try:
        with open("ganadores.txt", "r") as f:
            lineas = f.readlines()
        if lineas:
            for linea in lineas:
                page.add(ft.Text(linea.strip()))
        else:
            page.add(ft.Text("Todavia no hay ganadores."))
    except FileNotFoundError:
        page.add(ft.Text("El archivo de ganadores aun no existe."))

    page.add(ft.ElevatedButton(content=ft.Text("Volver"), on_click=lambda e: mostrar_inicio(page)))
    page.update()