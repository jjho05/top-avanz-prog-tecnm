#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_widget_gallery.py
--------------------
Galería de Componentes UI Modernos.
Una muestra exhaustiva de todos los widgets disponibles en CustomTkinter.
Sirve como "Cheat Sheet" visual para el estudiante.

Incluye:
- Tabview (Pestañas).
- Sliders y Progress Bars.
- Textbox con scroll.
- Radio Buttons y Checkboxes.
- Diálogos Modales (Input Dialog).
"""

import customtkinter as ctk

class WidgetGallery(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Galería de Widgets UI Modernos")
        self.geometry("900x600")
        
        # Grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Sidebar (Para controles globales) ---
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="Widget\nGallery", font=("Impact", 20))
        self.logo.grid(row=0, column=0, padx=20, pady=20)
        
        self.btn_dialog = ctk.CTkButton(self.sidebar, text="Abrir Diálogo", command=self.open_dialog)
        self.btn_dialog.grid(row=1, column=0, padx=20, pady=10)
        
        # --- Área Principal (Scrollable Frame) ---
        self.scroll = ctk.CTkScrollableFrame(self, label_text="Componentes")
        self.scroll.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.scroll.grid_columnconfigure(0, weight=1)
        self.scroll.grid_columnconfigure(1, weight=1)
        
        # 1. Botones y Variantes
        self.add_section("Botones", 0)
        ctk.CTkButton(self.scroll, text="Primario").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(self.scroll, text="Secundario", fg_color="transparent", border_width=2).grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(self.scroll, text="Peligro", fg_color="red", hover_color="darkred").grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.scroll, text="Desactivado", state="disabled").grid(row=2, column=1, padx=10, pady=10)
        
        # 2. Inputs de Texto
        self.add_section("Entradas", 3)
        ctk.CTkEntry(self.scroll, placeholder_text="Escribe algo...").grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkEntry(self.scroll, placeholder_text="Password", show="*").grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        
        # 3. Sliders y Switches
        self.add_section("Controles Deslizantes", 5)
        ctk.CTkSlider(self.scroll, from_=0, to=100).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ctk.CTkProgressBar(self.scroll).grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # 4. Selección
        self.add_section("Selección", 8)
        self.chk_var = ctk.StringVar(value="on")
        ctk.CTkCheckBox(self.scroll, text="Acepto Términos", variable=self.chk_var, onvalue="on", offvalue="off").grid(row=9, column=0, padx=10, pady=10)
        ctk.CTkSwitch(self.scroll, text="Modo Avión").grid(row=9, column=1, padx=10, pady=10)
        
        # 5. Tab View (Pestañas)
        self.add_section("Pestañas", 10)
        self.tabview = ctk.CTkTabview(self.scroll, height=150)
        self.tabview.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.tabview.add("Perfil")
        self.tabview.add("Ajustes")
        self.tabview.add("Logs")
        
        ctk.CTkLabel(self.tabview.tab("Perfil"), text="Contenido del Perfil").pack(pady=20)
        ctk.CTkLabel(self.tabview.tab("Ajustes"), text="Contenido de Ajustes").pack(pady=20)

    def add_section(self, title, row):
        lbl = ctk.CTkLabel(self.scroll, text=title, font=("Arial", 16, "bold"), anchor="w")
        lbl.grid(row=row, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")

    def open_dialog(self):
        dialog = ctk.CTkInputDialog(text="Ingresa tu nombre:", title="Diálogo Modal")
        print("Input:", dialog.get_input())

if __name__ == "__main__":
    app = WidgetGallery()
    app.mainloop()
