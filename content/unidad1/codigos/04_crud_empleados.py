#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_crud_empleados.py
--------------------
Aplicación Maestra de Unidad 1.
Simula un sistema CRUD (Create, Read, Update, Delete) de gestión de empleados.

Conceptos Avanzados:
1. Arquitectura Maestro-Detalle (Lista a la izquierda, Detalles a la derecha).
2. Variables de Control (StringVar, IntVar) para Data Binding.
3. Validaciones de entrada.
4. Comunicación entre componentes.
5. Manejo de listas dinámicas con CTkScrollableFrame.

Instrucciones:
    pip install customtkinter
    python 04_crud_empleados.py
"""

import customtkinter as ctk
from tkinter import messagebox

# Configuración Inicial
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Empleado:
    """Modelo de Datos simple."""
    def __init__(self, id_emp, nombre, departamento, activo):
        self.id = id_emp
        self.nombre = nombre
        self.departamento = departamento
        self.activo = activo

class CrudApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Talento - Unit 1 Final Project")
        self.geometry("900x600")

        # --- ESTADO DE LA APLICACIÓN (STATE) ---
        self.db_empleados = [
            Empleado(1, "Ana García", "Ingeniería", True),
            Empleado(2, "Carlos López", "Ventas", True),
            Empleado(3, "Sofía RAM", "RRHH", False)
        ]
        self.current_id_counter = 4
        self.selected_empleado_id = None

        # --- VARIABLES DE CONTROL (BINDING) ---
        self.var_id = ctk.StringVar()
        self.var_nombre = ctk.StringVar()
        self.var_depto = ctk.StringVar(value="Ingeniería")
        self.var_activo = ctk.BooleanVar(value=True)

        self._init_ui()
        self._refresh_list()

    def _init_ui(self):
        # Layout Principal: 2 Columnas
        self.grid_columnconfigure(0, weight=1) # Lista (30%)
        self.grid_columnconfigure(1, weight=2) # Formulario (70%)
        self.grid_rowconfigure(0, weight=1)

        # === PANEL IZQUIERDO: LISTA ===
        self.frame_list = ctk.CTkFrame(self, corner_radius=0)
        self.frame_list.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_list = ctk.CTkLabel(self.frame_list, text="Directorio", font=("Arial", 20, "bold"))
        self.lbl_list.pack(pady=10)

        self.scroll_list = ctk.CTkScrollableFrame(self.frame_list)
        self.scroll_list.pack(fill="both", expand=True, padx=10, pady=10)

        # === PANEL DERECHO: FORMULARIO ===
        self.frame_form = ctk.CTkFrame(self, corner_radius=0, fg_color=("white", "gray20"))
        self.frame_form.grid(row=0, column=1, sticky="nsew")

        self.lbl_form = ctk.CTkLabel(self.frame_form, text="Detalles del Empleado", font=("Arial", 20))
        self.lbl_form.pack(pady=20)

        # Campos
        self._crear_campo("ID:", self.var_id, readonly=True)
        self._crear_campo("Nombre Completo:", self.var_nombre)
        
        # Combo Departamento
        lbl_depto = ctk.CTkLabel(self.frame_form, text="Departamento:")
        lbl_depto.pack(anchor="w", padx=20)
        self.combo_depto = ctk.CTkComboBox(
            self.frame_form, 
            variable=self.var_depto,
            values=["Ingeniería", "Ventas", "RRHH", "Dirección", "Legal"]
        )
        self.combo_depto.pack(fill="x", padx=20, pady=(0, 10))

        # Switch Activo
        self.switch_activo = ctk.CTkSwitch(self.frame_form, text="Empleado Activo", variable=self.var_activo)
        self.switch_activo.pack(anchor="w", padx=20, pady=10)

        # Botonera
        self.frame_btns = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_btns.pack(pady=30, fill="x", padx=20)

        self.btn_new = ctk.CTkButton(self.frame_btns, text="Nuevo / Limpiar", fg_color="gray", command=self.limpiar_form)
        self.btn_new.pack(side="left", expand=True, padx=5)

        self.btn_save = ctk.CTkButton(self.frame_btns, text="Guardar", fg_color="green", command=self.guardar)
        self.btn_save.pack(side="left", expand=True, padx=5)

        self.btn_del = ctk.CTkButton(self.frame_btns, text="Eliminar", fg_color="red", command=self.eliminar)
        self.btn_del.pack(side="left", expand=True, padx=5)

    def _crear_campo(self, label, variable, readonly=False):
        lbl = ctk.CTkLabel(self.frame_form, text=label)
        lbl.pack(anchor="w", padx=20)
        
        state = "disabled" if readonly else "normal"
        entry = ctk.CTkEntry(self.frame_form, textvariable=variable, state=state)
        entry.pack(fill="x", padx=20, pady=(0, 10))
        return entry

    def _refresh_list(self):
        """Reconstruye la lista de tarjetas basada en self.db_empleados"""
        # Limpiar widgets anteriores
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        for emp in self.db_empleados:
            card = self._create_card(emp)
            card.pack(fill="x", pady=5)

    def _create_card(self, emp: Empleado):
        card = ctk.CTkButton(
            self.scroll_list, 
            text=f"{emp.nombre}\n{emp.departamento}", 
            height=60,
            fg_color="#1f538d",
            anchor="w",
            command=lambda e=emp: self.cargar_empleado(e)
        )
        return card

    def cargar_empleado(self, emp: Empleado):
        """Pasa los datos del objeto al Formulario (Variables)"""
        self.selected_empleado_id = emp.id
        self.var_id.set(str(emp.id))
        self.var_nombre.set(emp.nombre)
        self.var_depto.set(emp.departamento)
        self.var_activo.set(emp.activo)
        print(f"Cargado ID: {emp.id}")

    def limpiar_form(self):
        self.selected_empleado_id = None
        self.var_id.set("NUEVO")
        self.var_nombre.set("")
        self.var_depto.set("Ingeniería")
        self.var_activo.set(True)

    def guardar(self):
        nombre = self.var_nombre.get()
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        if self.selected_empleado_id is None:
            # CREATE
            new_emp = Empleado(
                self.current_id_counter,
                nombre,
                self.var_depto.get(),
                self.var_activo.get()
            )
            self.db_empleados.append(new_emp)
            self.current_id_counter += 1
            messagebox.showinfo("Éxito", "Empleado creado")
        else:
            # UPDATE
            for emp in self.db_empleados:
                if emp.id == self.selected_empleado_id:
                    emp.nombre = nombre
                    emp.departamento = self.var_depto.get()
                    emp.activo = self.var_activo.get()
                    break
            messagebox.showinfo("Éxito", "Empleado actualizado")

        self.limpiar_form()
        self._refresh_list()

    def eliminar(self):
        if self.selected_empleado_id is None:
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar ID {self.selected_empleado_id}?"):
            self.db_empleados = [e for e in self.db_empleados if e.id != self.selected_empleado_id]
            self.limpiar_form()
            self._refresh_list()

if __name__ == "__main__":
    app = CrudApp()
    app.mainloop()
