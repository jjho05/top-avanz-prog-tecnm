#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_api_client.py
----------------
Consumo de API RESTful.
Las apps móviles modernas no tienen base de datos local; consumen JSON de la nube.
Usamos `httpx` (o `requests` y `threading`) para no bloquear la UI.

Conceptos:
1. HTTP GET Request.
2. Deserialización JSON -> Objetos Python.
3. Renderizado dinámico de `ListView`.
"""

import flet as ft
import urllib.request
import json
import threading

def main(page: ft.Page):
    page.title = "Noticias (API Client)"
    
    lista_noticias = ft.ListView(expand=True, spacing=10, padding=20)
    loading = ft.ProgressBar(width=400, color="blue", visible=False)

    def cargar_datos(e):
        loading.visible = True
        btn_cargar.disabled = True
        lista_noticias.controls.clear()
        page.update()

        # Operación Bloqueante en un Hilo separado (Ver Unidad 3)
        def worker():
            try:
                url = "https://jsonplaceholder.typicode.com/posts?_limit=10"
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
                
                # Actualizar UI (Flet es Thread-Safe internamente para .update())
                for post in data:
                    item = ft.Container(
                        content=ft.Column([
                            ft.Text(post['title'], weight="bold", size=16),
                            ft.Text(post['body'], color=ft.colors.GREY_700),
                            ft.Divider()
                        ]),
                        bgcolor=ft.colors.WHITE,
                        padding=10,
                        border_radius=5
                    )
                    lista_noticias.controls.append(item)
                
            except Exception as err:
                lista_noticias.controls.append(ft.Text(f"Error: {err}", color="red"))
            
            loading.visible = False
            btn_cargar.disabled = False
            page.update()

        threading.Thread(target=worker, daemon=True).start()

    btn_cargar = ft.FloatingActionButton(
        icon=ft.icons.REFRESH,
        on_click=cargar_datos
    )

    page.add(
        ft.AppBar(title=ft.Text("Ultimas Noticias"), bgcolor=ft.colors.INDIGO),
        ft.Column([loading], alignment="center"),
        lista_noticias,
    )
    page.floating_action_button = btn_cargar

if __name__ == "__main__":
    ft.app(target=main)
