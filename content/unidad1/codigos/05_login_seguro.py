#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_login_seguro.py
------------------
Arquitectura de Autenticación Profesional en Deskopt GUI.
Este no es un simple `if user == "admin"`.
Este script demuestra patrones de seguridad y navegación de UI.

Conceptos Avanzados:
1. Navegación entre Frames (Stack de Vistas).
2. Seguridad: Hashing de contraseñas con `hashlib` (Nunca guardar texto plano).
3. `pack_forget()` para transiciones limpias.
4. Manejo de Sesión (Objeto `Session` Global).

Instrucciones:
    Usuario: admin
    Pass:    segura123
"""

import customtkinter as ctk
from tkinter import messagebox
import hashlib

# Simulación de Base de Datos (en producción sería SQLite/Postgres)
# La contraseña almacenada es el SHA-256 de "segura123"
DB_USERS = {
    "admin": "5fd924625f6ab16a19cc9807c7c506ae1813490e4ba675f843d5a10e0baacdb8"
}

class Session:
    """Singleton para mantener el estado del usuario logueado."""
    current_user = None

def hash_password(password):
    """Retorna el hash SHA-256 hexadecimal de la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success

        self.lbl_title = ctk.CTkLabel(self, text="Acceso Corporativo", font=("Roboto", 24))
        self.lbl_title.pack(pady=40)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Iniciar Sesión", command=self._attempt_login)
        self.btn_login.pack(pady=20)
        
        # Binding de Enter para comodidad del usuario
        self.entry_pass.bind("<Return>", lambda e: self._attempt_login())

    def _attempt_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        
        if u in DB_USERS:
            # Verificación Criptográfica
            if hash_password(p) == DB_USERS[u]:
                Session.current_user = u
                self.on_success() # Callback al MainApp
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master)
        
        self.lbl_welcome = ctk.CTkLabel(self, text=f"Bienvenido, {Session.current_user}", font=("Roboto", 30))
        self.lbl_welcome.pack(pady=50, padx=50)

        self.btn_logout = ctk.CTkButton(self, text="Cerrar Sesión", fg_color="red", command=on_logout)
        self.btn_logout.pack(pady=20)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Seguro v1.0")
        self.geometry("600x500")

        # Container principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def show_login(self):
        self._clear_container()
        login = LoginFrame(self.container, on_success=self.show_dashboard)
        login.place(relx=0.5, rely=0.5, anchor="center")

    def show_dashboard(self):
        self._clear_container()
        dash = DashboardFrame(self.container, on_logout=self.show_login)
        dash.pack(fill="both", expand=True)

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
