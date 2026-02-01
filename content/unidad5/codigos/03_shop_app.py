#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_shop_app.py
--------------
Navegación y Rutas (SPA - Single Page Application).
Simula una tienda con múltiples vistas.

Conceptos:
1. `page.on_route_change`: Manejador de URL virtual.
2. `page.views`: Pila de vistas (Historial de navegación).
3. `AppBar`: Barra superior de aplicación móvil.
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Tienda Flet"

    def route_change(route):
        page.views.clear()
        
        # --- VISTA 1: HOME ---
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Catálogo"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Ver iPhone 15", on_click=lambda _: page.go("/producto/1")),
                    ft.ElevatedButton("Ver Laptop Gamer", on_click=lambda _: page.go("/producto/2")),
                ],
            )
        )
        
        # --- VISTA 2: DETALLE PRODUCTO ---
        if page.route.startswith("/producto"):
            try:
                prod_id = page.route.split("/")[-1]
                
                # Datos falsos
                nombre = "iPhone 15" if prod_id == "1" else "Laptop Gamer"
                precio = "$999" if prod_id == "1" else "$1500"
                icono = ft.icons.PHONE_IPHONE if prod_id == "1" else ft.icons.COMPUTER
                
                page.views.append(
                    ft.View(
                        f"/producto/{prod_id}",
                        [
                            ft.AppBar(title=ft.Text(nombre), bgcolor=ft.colors.SURFACE_VARIANT),
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(icono, size=100, color=ft.colors.BLUE),
                                    ft.Text(nombre, size=30, weight="bold"),
                                    ft.Text(precio, size=20, color=ft.colors.GREEN),
                                    ft.ElevatedButton("Comprar ahora", bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE),
                                    ft.OutlinedButton("Volver", on_click=lambda _: page.go("/")),
                                ], horizontal_alignment="center"),
                                alignment=ft.alignment.center,
                                padding=50
                            )
                        ],
                    )
                )
            except:
                pass
                
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
