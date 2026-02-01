#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_package_explorer.py
----------------------
Explorador de Paquetes Gráfico (UI).

Este script utiliza Flet (Flutter para Python) para crear una herramienta visual
que permite inspeccionar la estructura interna de cualquier paquete o carpeta.
Demuestra "Introspección" aplicada a una Interfaz Gráfica Moderna.

Requisitos:
    pip install flet
"""

import flet as ft
import os
import inspect
import importlib.util

def main(page: ft.Page):
    page.title = "Python Package Explorer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # --- Lógica de Introspección ---
    def get_file_icon(filename: str):
        if filename.endswith(".py"): return ft.icons.CODE
        if filename.endswith(".pyc"): return ft.icons.DataObject
        if filename == "__init__.py": return ft.icons.SETTINGS
        return ft.icons.INSERT_DRIVE_FILE

    def load_directory_structure(path: str):
        items = []
        try:
            with os.scandir(path) as it:
                for entry in sorted(it, key=lambda e: (not e.is_dir(), e.name)):
                    if entry.name.startswith(".") or entry.name == "__pycache__":
                        continue
                        
                    if entry.is_dir():
                        items.append(
                            ft.ExpansionTile(
                                title=ft.Text(entry.name, weight="bold"),
                                leading=ft.Icon(ft.icons.FOLDER, color="blue"),
                                controls=load_directory_structure(entry.path), # Recursión
                                bgcolor=ft.colors.BLUE_50 if "mypackage" in entry.path else None
                            )
                        )
                    else:
                        items.append(
                            ft.ListTile(
                                title=ft.Text(entry.name),
                                leading=ft.Icon(get_file_icon(entry.name), color="green" if entry.name.endswith(".py") else "grey"),
                                subtitle=ft.Text(f"{entry.stat().st_size} bytes"),
                                on_click=lambda e, p=entry.path: show_code(p)
                            )
                        )
        except Exception as e:
            items.append(ft.Text(f"Error: {e}", color="red"))
        return items

    # --- UI Components ---
    
    code_view = ft.Markdown("Selecciona un archivo...", selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
    
    def show_code(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Renderizado básico de sintaxis
            code_view.value = f"```python\n{content}\n```"
            page.update()
        except Exception as e:
            code_view.value = f"Error leyendo archivo: {e}"
            page.update()

    # Layout Principal
    sidebar = ft.ListView(expand=True, spacing=10)
    
    # Cargar el directorio actual (donde está mypackage)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sidebar.controls = load_directory_structure(current_dir)

    page.add(
        ft.Row(
            [
                # Panel Izquierdo (Árbol)
                ft.Container(
                    content=sidebar,
                    width=300,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=10,
                    padding=10,
                ),
                # Panel Derecho (Visor de Código)
                ft.Container(
                    content=ft.Column([
                        ft.Text("Visor de Código Fuente", size=20, weight="bold"),
                        ft.Divider(),
                        ft.Container(
                            content=code_view,
                            expand=True,
                        )
                    ], scroll="auto"),
                    expand=True,
                    bgcolor=ft.colors.BACKGROUND,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=10,
                    padding=20,
                )
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
