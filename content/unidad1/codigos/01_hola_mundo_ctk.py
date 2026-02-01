#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_hola_mundo_ctk.py
--------------------
El "Hola Mundo" moderno para interfaces gráficas en Python.
Este script demuestra la estructura básica de una aplicación CustomTkinter
utilizando Programación Orientada a Objetos (POO), que es el estándar
profesional para GUIs.

Conceptos cubiertos:
1. Herencia de `ctk.CTk`.
2. Método `__init__` para configuración inicial.
3. Geometría inicial y título.
4. Loop de eventos (`mainloop`).

Instrucciones:
    pip install customtkinter
    python 01_hola_mundo_ctk.py
"""

import customtkinter as ctk

# Configuración global del tema (System, Dark, Light)
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana
        self.title("Hola Mundo - Tópicos Avanzados")
        self.geometry("400x250")
        self.resizable(False, False)

        # 2. Layout (Grid 2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # 3. Widgets
        self.label_bienvenida = ctk.CTkLabel(
            self, 
            text="¡Bienvenido a TAP!", 
            font=("Roboto Medium", 24)
        )
        self.label_bienvenida.grid(row=0, column=0, padx=20, pady=20)

        self.btn_accion = ctk.CTkButton(
            self, 
            text="Haz clic aquí", 
            command=self.evento_boton
        )
        self.btn_accion.grid(row=1, column=0, padx=20, pady=20)

        # Variable de estado simple (contador)
        self.contador = 0

    def evento_boton(self):
        """Callback ejecutado al presionar el botón."""
        self.contador += 1
        nuevo_texto = f"Clickeado {self.contador} veces"
        print(f"Evento disparado: {nuevo_texto}")
        
        # Actualizamos la UI
        self.label_bienvenida.configure(text=nuevo_texto)

if __name__ == "__main__":
    app = App()
    app.mainloop()
