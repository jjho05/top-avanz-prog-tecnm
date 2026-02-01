#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_flet_responsive.py
---------------------
Diseño Responsivo (Mobile vs Desktop).
Detectamos el ancho de la pantalla y cambiamos el layout.

Conceptos:
1. `GridView`: Rejilla adaptable.
2. Evento `on_resized`: Escuchar cambios de tamaño de ventana.
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Galería Responsiva"
    page.padding = 10

    # Crear 20 tarjetas simuladas
    items = []
    for i in range(1, 21):
        items.append(
            ft.Container(
                content=ft.Text(f"Item {i}", size=20, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                bgcolor=ft.colors.BLUE_200,
                border_radius=10,
                height=150,
            )
        )

    # Grid que cambia columnas según el ancho
    grid = ft.GridView(
        expand=True,
        runs_count=5, # Default para monitor grande
        max_extent=200, 
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
        controls=items
    )
    
    status_text = ft.Text("Escritorio")

    def page_resize(e):
        w = page.width
        status_text.value = f"Ancho: {w}px"
        
        if w < 600:
            grid.runs_count = 2 # Móvil
            status_text.value += " (Modo Móvil)"
            page.bgcolor = ft.colors.ORANGE_50
        elif w < 1000:
            grid.runs_count = 3 # Tablet
            status_text.value += " (Modo Tablet)"
            page.bgcolor = ft.colors.YELLOW_50
        else:
            grid.runs_count = 5 # Desktop
            status_text.value += " (Modo Escritorio)"
            page.bgcolor = ft.colors.WHITE
            
        page.update()

    page.on_resized = page_resize
    
    page.add(
        ft.Row([ ft.Icon(ft.icons.DEVICES), status_text ], alignment=ft.MainAxisAlignment.CENTER),
        grid
    )
    
    # Trigger inicial
    page_resize(None)

if __name__ == "__main__":
    ft.app(target=main)
