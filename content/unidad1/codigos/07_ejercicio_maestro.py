#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ejercicio_maestro.py
--------------------
Ejercicio Maestro de Layouts (Referenciado en 1.1.md).
Simula una estructura de ERP (Enterprise Resource Planning) profesional.

Este script demuestra:
1.  Uso avanzado de `.grid()` con pesos (weights).
2.  Sidebar de navegación fijo.
3.  Cambio de tema (Light/Dark) dinámico.
4.  Formularios con validación visual.

Requisitos:
    pip install customtkinter
"""

import customtkinter as ctk
import tkinter.messagebox as tkmb

# Configuración Global
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de Ventana
        self.title("Sistema ERP - Maestro Detalle")
        self.geometry("1100x700")

        # Grid Principal: 1x2
        # Columna 0: Sidebar (Fijo)
        # Columna 1: Contenido (Flexible)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SECCIÓN 1: SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Empujar items abajo

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AdminPanel", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botones de Navegación
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.nav_dashboard)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_empleados = ctk.CTkButton(self.sidebar_frame, text="Empleados", command=self.nav_empleados)
        self.btn_empleados.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_config = ctk.CTkButton(self.sidebar_frame, text="Configuración", command=self.nav_config)
        self.btn_config.grid(row=3, column=0, padx=20, pady=10)

        # Switch de Tema (Abajo)
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Modo Oscuro:", anchor="w")
        self.theme_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.theme_switch = ctk.CTkSwitch(self.sidebar_frame, text="", command=self.change_theme)
        self.theme_switch.select() # Default Dark en macOS system
        self.theme_switch.grid(row=6, column=0, padx=20, pady=(0, 20))

        # --- SECCIÓN 2: ÁREA DE CONTENIDO PRINCIPAL ---
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Inicializar en Dashboard
        self.nav_dashboard()

    def change_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def nav_dashboard(self):
        self.clear_content()
        # Header
        lbl = ctk.CTkLabel(self.main_content, text="Dashboard Ejecutivo", font=("Arial", 24))
        lbl.pack(pady=20, padx=20, anchor="w")
        
        # Stats Grid (2x2)
        stats_frame = ctk.CTkFrame(self.main_content)
        stats_frame.pack(fill="x", padx=20)
        
        for i, (titulo, valor) in enumerate([("Ventas", "$10k"), ("Usuarios", "1,200"), ("Tickets", "45"), ("Server", "99%")]):
            card = ctk.CTkFrame(stats_frame, fg_color=("gray80", "gray25"))
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=titulo, font=("Arial", 14)).pack(pady=(10,0))
            ctk.CTkLabel(card, text=valor, font=("Arial", 20, "bold"), text_color="cyan").pack(pady=(0,10))

    def nav_empleados(self):
        self.clear_content()
        # Formulario Maestro-Detalle
        
        # Layout Interno
        self.main_content.columnconfigure(0, weight=3) # Lista
        self.main_content.columnconfigure(1, weight=2) # Formulario
        self.main_content.rowconfigure(0, weight=1)
        
        # 1. Lista (Izquierda)
        list_frame = ctk.CTkScrollableFrame(self.main_content, label_text="Directorio (Scrollable)")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        for i in range(20):
            ctk.CTkButton(list_frame, text=f"Empleado #{i+1} - Depto IT", fg_color="transparent", border_width=1).pack(fill="x", pady=2)

        # 2. Formulario (Derecha)
        form_frame = ctk.CTkFrame(self.main_content)
        form_frame.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(form_frame, text="Editar Perfil", font=("Arial", 18)).pack(pady=20)
        ctk.CTkEntry(form_frame, placeholder_text="Nombre Completo").pack(pady=10, fill="x", padx=20)
        ctk.CTkEntry(form_frame, placeholder_text="Correo Electrónico").pack(pady=10, fill="x", padx=20)
        ctk.CTkComboBox(form_frame, values=["IT", "HR", "Sales", "Admin"]).pack(pady=10, fill="x", padx=20)
        
        ctk.CTkButton(form_frame, text="Guardar Cambios", fg_color="green").pack(pady=20)
        ctk.CTkButton(form_frame, text="Eliminar", fg_color="red", hover_color="darkred").pack(pady=5)

    def nav_config(self):
        self.clear_content()
        ctk.CTkLabel(self.main_content, text="Configuración", font=("Arial", 24)).pack(pady=20)
        
        check_var = ctk.StringVar(value="on")
        ctk.CTkCheckBox(self.main_content, text="Notificaciones por Correo", variable=check_var, onvalue="on", offvalue="off").pack(pady=10, anchor="w", padx=40)
        ctk.CTkCheckBox(self.main_content, text="Autoguardado al salir").pack(pady=10, anchor="w", padx=40)
        
        ctk.CTkSlider(self.main_content, from_=0, to=100, number_of_steps=10).pack(pady=20, fill="x", padx=40)

if __name__ == "__main__":
    app = App()
    app.mainloop()
