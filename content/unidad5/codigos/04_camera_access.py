#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_camera_access.py
-------------------
Acceso a Hardware (Simulado/Nativo).
En aplicaciones Web/Móvil (PWA), el acceso a la cámara se hace vía "File Picker".
El navegador le pregunta al usuario: "¿Cámara o Galería?".

Conceptos:
1. `FilePicker`: Diálogo nativo del SO.
2. `Image`: Widget para mostrar la foto seleccionada.
3. Callbacks asíncronos para manejar la subida.
"""

import flet as ft
import shutil
import os

def main(page: ft.Page):
    page.title = "Acceso a Cámara/Galería"
    
    # Widget de Imagen vacía al inicio
    img_viewer = ft.Image(
        src="https://via.placeholder.com/300?text=Sin+Foto",
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
    )
    
    status_text = ft.Text("No se ha seleccionado nada.")

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file = e.files[0]
            status_text.value = f"Cargando: {file.name}"
            # En una app real, aquí subiríamos el archivo a la nube.
            # Aquí solo lo mostraremos localmente.
            img_viewer.src = file.path
            status_text.value = f"Mostrando: {file.name} ({file.size} bytes)"
            page.update()
        else:
            status_text.value = "Selección cancelada."
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker) # Importante: agregarlo al overlay

    page.add(
        ft.Column(
            [
                ft.Text("Selfie App", size=40, weight="bold"),
                img_viewer,
                status_text,
                ft.ElevatedButton(
                    "Abrir Cámara / Galería",
                    icon=ft.icons.CAMERA_ALT,
                    on_click=lambda _: file_picker.pick_files(
                        allow_multiple=False,
                        file_type=ft.FilePickerFileType.IMAGE
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
