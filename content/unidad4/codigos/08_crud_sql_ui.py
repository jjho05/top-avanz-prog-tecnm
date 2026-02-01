#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_crud_sql_ui.py
-----------------
Sistema ABCC (Altas, Bajas, Cambios, Consultas) Completo.

Interfaz Gráfica transaccional para gestión de empleados.
Demuestra la integración completa entre la Capa de Datos (SQLAlchemy)
y la Capa de Presentación (CustomTkinter).

Características:
- Tabla interactiva con selección.
- Formulario modal para Crear/Editar.
- Validación de datos.
- Confirmación de borrado.
"""

import customtkinter as ctk
import tkinter.messagebox as tkmb
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Modelo de Datos ---
Base = declarative_base()
class Empleado(Base):
    __tablename__ = 'empleados_crud'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    puesto = Column(String)
    salario = Column(Float)

engine = create_engine('sqlite:///empresa.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class EmpleadoForm(ctk.CTkToplevel):
    def __init__(self, parent, on_save, empleado=None):
        super().__init__(parent)
        self.title("Empleado")
        self.geometry("400x300")
        self.on_save = on_save
        self.empleado = empleado
        
        # Campos
        ctk.CTkLabel(self, text="Nombre:").pack(pady=(20, 5))
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.pack()
        
        ctk.CTkLabel(self, text="Puesto:").pack(pady=5)
        self.entry_puesto = ctk.CTkEntry(self)
        self.entry_puesto.pack()
        
        ctk.CTkLabel(self, text="Salario Mensual:").pack(pady=5)
        self.entry_salario = ctk.CTkEntry(self)
        self.entry_salario.pack()
        
        # Pre-llenar si es edición
        if empleado:
            self.entry_nombre.insert(0, empleado.nombre)
            self.entry_puesto.insert(0, empleado.puesto)
            self.entry_salario.insert(0, str(empleado.salario))
            
        ctk.CTkButton(self, text="Guardar", command=self.save).pack(pady=20)
        
    def save(self):
        try:
            nombre = self.entry_nombre.get()
            puesto = self.entry_puesto.get()
            salario = float(self.entry_salario.get())
            
            if not nombre: raise ValueError("Nombre requerido")
            
            self.on_save(nombre, puesto, salario, self.empleado)
            self.destroy()
        except ValueError as e:
            tkmb.showerror("Error", str(e))

class CrudApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Personal v2.0")
        self.geometry("800x600")
        
        self.session = Session()
        
        # Toolbar
        self.toolbar = ctk.CTkFrame(self, height=50)
        self.toolbar.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(self.toolbar, text="Nuevo Empleado", command=self.add_empleado, fg_color="green").pack(side="left", padx=10)
        ctk.CTkButton(self.toolbar, text="Editar", command=self.edit_empleado).pack(side="left", padx=10)
        ctk.CTkButton(self.toolbar, text="Eliminar", command=self.delete_empleado, fg_color="red").pack(side="left", padx=10)
        ctk.CTkButton(self.toolbar, text="Recargar", command=self.load_data).pack(side="right", padx=10)
        
        # Lista (Scrollable)
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.selected_id = None
        self.load_data()

    def load_data(self):
        # Limpiar UI
        for w in self.scroll.winfo_children(): w.destroy()
        self.selected_id = None
        
        empleados = self.session.query(Empleado).all()
        
        # Headers
        headers = ctk.CTkFrame(self.scroll, height=30)
        headers.pack(fill="x")
        ctk.CTkLabel(headers, text="ID", width=50).pack(side="left")
        ctk.CTkLabel(headers, text="Nombre", width=200).pack(side="left")
        ctk.CTkLabel(headers, text="Puesto", width=150).pack(side="left")
        ctk.CTkLabel(headers, text="Salario", width=100).pack(side="left")
        
        for emp in empleados:
            row = ctk.CTkButton(
                self.scroll, 
                text="", 
                fg_color="transparent", 
                border_width=1,
                corner_radius=0,
                height=35,
                command=lambda id=emp.id: self.select_row(id)
            )
            row.pack(fill="x", pady=2)
            
            # Row Content Hack (Labels inside Button is tricky, better Frame inside scroll)
            # Simplificación: Usar el texto del botón
            row.configure(text=f"ID: {emp.id} | {emp.nombre} | {emp.puesto} | ${emp.salario:,.2f}", anchor="w", hover_color="gray")

    def select_row(self, id):
        self.selected_id = id
        tkmb.showinfo("Selección", f"Empleado ID {id} seleccionado")

    def add_empleado(self):
        EmpleadoForm(self, self.save_empleado)

    def edit_empleado(self):
        if not self.selected_id: return
        emp = self.session.query(Empleado).get(self.selected_id)
        EmpleadoForm(self, self.save_empleado, emp)

    def delete_empleado(self):
        if not self.selected_id: return
        if tkmb.askyesno("Confirmar", "¿Eliminar empleado?"):
            emp = self.session.query(Empleado).get(self.selected_id)
            self.session.delete(emp)
            self.session.commit()
            self.load_data()

    def save_empleado(self, nombre, puesto, salario, empleado_existente):
        if empleado_existente:
            empleado_existente.nombre = nombre
            empleado_existente.puesto = puesto
            empleado_existente.salario = salario
        else:
            nuevo = Empleado(nombre=nombre, puesto=puesto, salario=salario)
            self.session.add(nuevo)
        
        self.session.commit()
        self.load_data()

if __name__ == "__main__":
    app = CrudApp()
    app.mainloop()
