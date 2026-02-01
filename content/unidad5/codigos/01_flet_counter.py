#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_flet_counter.py
------------------
Hola Mundo Reactivo con Flet.
Flet permite construir apps Flutter con Python.

Conceptos:
1. `page`: El lienzo.
2. `page.add()`: Agregar controles.
3. `page.update()`: ¡La magia! Actualiza la UI sin recargar toda la ventana.

Requisitos: pip install flet
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Contador Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Estado (Variable mutable)
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update() # Refrescar UI

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # Layout (Row centra los botones)
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click, bgcolor=ft.colors.RED_100),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click, bgcolor=ft.colors.GREEN_100),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Text("¡Hecho con Python puro!", size=12, color=ft.colors.GREY)
    )

if __name__ == "__main__":
    ft.app(target=main)
