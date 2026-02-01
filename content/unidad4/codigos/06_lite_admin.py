#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_lite_admin.py
----------------
LiteAdmin: Visor de Base de Datos Gráfico.

Una herramienta tipo "DBeaver" o "HeidiSQL" pero hecha en Python/Flet puro.
Permite conectar a cualquier archivo SQLite y explorar sus tablas y datos.

Demuestra:
- Conexión DB dinámica.
- Introspección de esquema SQL (listar tablas).
- DataGrid (Tabla de datos) dinámica.

Requisitos:
    pip install flet sqlalchemy
"""

import flet as ft
from sqlalchemy import create_engine, inspect, text

def main(page: ft.Page):
    page.title = "LiteAdmin - SQLite Viewer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    
    # State
    current_engine = None
    
    # --- Logic ---
    
    def connect_db(e):
        nonlocal current_engine
        path = db_path.value
        try:
            status.value = "Conectando..."
            page.update()
            
            # SQLAlchemy connection string
            # Usa path absoluto o relativo
            db_url = f"sqlite:///{path}"
            current_engine = create_engine(db_url)
            
            # Introspección para listar tablas
            insp = inspect(current_engine)
            tables = insp.get_table_names()
            
            # Actualizar UI
            table_dropdown.options = [ft.dropdown.Option(t) for t in tables]
            table_dropdown.value = tables[0] if tables else None
            status.value = f"Conectado a: {path}"
            status.color = "green"
            
            if tables:
                load_table_data(tables[0])
            
        except Exception as err:
            status.value = f"Error: {err}"
            status.color = "red"
        
        page.update()

    def load_table_data(table_name):
        if not current_engine or not table_name: return
        
        try:
            # Raw SQL segura (solo lectura)
            with current_engine.connect() as conn:
                # 1. Obtener columnas
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 50"))
                columns = result.keys()
                rows = result.fetchall()
                
                # 2. Construir DataTable Configuration
                data_table.columns = [
                    ft.DataColumn(ft.Text(col, weight="bold")) for col in columns
                ]
                
                # 3. Construir Filas
                data_table.rows = []
                for row in rows:
                    cells = [ft.DataCell(ft.Text(str(val))) for val in row]
                    data_table.rows.append(ft.DataRow(cells=cells))
                
                rows_count.value = f"{len(rows)} filas (Limit 50)"
                
        except Exception as err:
            status.value = f"Error Query: {err}"
            status.color = "red"
        
        page.update()

    def on_table_change(e):
        load_table_data(table_dropdown.value)

    # --- UI Components ---
    
    # Toolbar
    db_path = ft.TextField(
        value="database.db", 
        label="Ruta SQLite (.db)", 
        expand=True,
        icon=ft.icons.STORAGE
    )
    
    btn_connect = ft.ElevatedButton(
        "Conectar", 
        icon=ft.icons.POWER, 
        on_click=connect_db,
        bgcolor=ft.colors.BLUE_600,
        color=ft.colors.WHITE
    )

    toolbar = ft.Row([db_path, btn_connect])

    # Status Bar
    status = ft.Text("Desconectado", color="grey")
    
    # Selector de Tabla
    table_dropdown = ft.Dropdown(
        label="Seleccionar Tabla",
        on_change=on_table_change,
        width=300
    )
    
    rows_count = ft.Text("")

    # Data Grid (Scrollable)
    data_table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Esperando datos..."))],
        rows=[],
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.BorderSide(1, "grey"),
        horizontal_lines=ft.border.BorderSide(1, "grey"),
    )
    
    grid_container = ft.Column(
        [data_table],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Main Layout
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("LiteAdmin", size=30, weight="bold", color="blue"),
                toolbar,
                ft.Divider(),
                ft.Row([table_dropdown, rows_count], alignment="spaceBetween"),
                grid_container,
                ft.Divider(),
                status
            ]),
            padding=20,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
