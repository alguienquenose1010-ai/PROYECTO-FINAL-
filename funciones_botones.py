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

    page.add(text, image, button1, button2)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

def jugar(page):
    page.controls.clear()

    jugador1 = ft.TextField(hint_text="Nombre del jugador 1")
    jugador2 = ft.TextField(hint_text="Nombre del jugador 2")

    page.add(
        jugador1,
        jugador2,
        ft.ElevatedButton(content=ft.Text("JUGAR"), on_click=lambda e: Jugar(page)),
        ft.ElevatedButton(content=ft.Text("Volver"), on_click=lambda e: mostrar_inicio(page))
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
            page.add(ft.Text("Todavía no hay ganadores."))
    except FileNotFoundError:
        page.add(ft.Text("El archivo de ganadores no existe."))

    page.add(ft.ElevatedButton(content=ft.Text("Volver"), on_click=lambda e: mostrar_inicio(page)))
    page.update()


def JUGAR(page):
    Jugar(page)