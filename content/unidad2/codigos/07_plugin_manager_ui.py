#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_plugin_manager_ui.py
-----------------------
Gestor de Plugins con Interfaz Gráfica (CustomTkinter).

Simula un sistema de "Store" o "Extensiones" como el de VS Code.
Permite activar y desactivar funcionalidades dinámicamente sin reiniciar la app.

Conceptos:
- Carga dinámica de módulos (`importlib`).
- GUI para gestión de estado de sistema.
- Patrón Observador (La UI reacciona a los cambios en el backend).

Requisitos:
    pip install customtkinter
"""

import customtkinter as ctk
import os
import importlib
import sys

# Simulamos una interfaz de plugin
class PluginInterface:
    name = "Unknown"
    version = "0.0"
    def run(self): pass

# Crearemos plugins fake en tiempo de ejecución para la demo si no existen
os.makedirs("demo_plugins", exist_ok=True)
with open("demo_plugins/plugin_a.py", "w") as f:
    f.write('def run(): return "Hola desde Plugin A (Analítica)"\nname="Analytics Pro"\nversion="1.2"')
with open("demo_plugins/plugin_b.py", "w") as f:
    f.write('def run(): return "Hola desde Plugin B (Tema Oscuro)"\nname="Dark Theme"\nversion="2.0"')
with open("demo_plugins/plugin_c.py", "w") as f:
    f.write('def run(): return "Hola desde Plugin C (AI Copilot)"\nname="AI Copilot"\nversion="0.9 Beta"')

class PluginCard(ctk.CTkFrame):
    def __init__(self, master, filename, on_toggle):
        super().__init__(master)
        self.filename = filename
        self.on_toggle = on_toggle
        self.is_active = False
        
        # Layout
        self.lbl_name = ctk.CTkLabel(self, text=filename, font=("Arial", 14, "bold"))
        self.lbl_name.pack(side="left", padx=10, pady=10)
        
        self.btn_switch = ctk.CTkSwitch(self, text="Activo", command=self.toggle)
        self.btn_switch.pack(side="right", padx=10)
        
        # Leer metadatos sin importar (parsing simple)
        self.load_metadata()

    def load_metadata(self):
        try:
            with open(os.path.join("demo_plugins", self.filename)) as f:
                content = f.read()
                if 'name="' in content:
                    # Extracción muy básica para demo
                    start = content.find('name="') + 6
                    end = content.find('"', start)
                    self.lbl_name.configure(text=content[start:end])
        except:
            pass

    def toggle(self):
        self.is_active = self.btn_switch.get() == 1
        self.on_toggle(self.filename, self.is_active)

class PluginManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Store de Extensiones (Plugin Manager)")
        self.geometry("800x500")
        
        # Header
        ctk.CTkLabel(self, text="Gestor de Extensiones", font=("Arial", 24)).pack(pady=20)
        ctk.CTkLabel(self, text="Activa módulos dinamicamente sin reiniciar", text_color="gray").pack(pady=(0, 20))

        # Lista de Plugins
        self.scroll = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.scroll.pack(pady=10)
        
        self.load_plugins()
        
        # Área de log
        self.log_box = ctk.CTkTextbox(self, height=100, width=600)
        self.log_box.pack(pady=20)
        self.log("Sistema iniciado. Esperando plugins...")

    def log(self, msg):
        self.log_box.insert("end", f"> {msg}\n")
        self.log_box.see("end")

    def load_plugins(self):
        # Escanear carpeta
        files = [f for f in os.listdir("demo_plugins") if f.endswith(".py")]
        for f in files:
            card = PluginCard(self.scroll, f, self.handle_plugin_change)
            card.pack(fill="x", padx=10, pady=5)
            
    def handle_plugin_change(self, filename, active):
        if active:
            try:
                # Importación Dinámica Real
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, os.path.join("demo_plugins", filename))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                
                # Ejecutar
                res = mod.run()
                self.log(f"✅ PLUGIN ACTIVADO: {filename}\n   Resultado: {res}")
            except Exception as e:
                self.log(f"❌ Error cargando {filename}: {e}")
        else:
            self.log(f"⏹️ Plugin desactivado: {filename}")
            # En Python real, hacer "unimport" es casi imposible, pero aquí simulamos la desactivación lógica.

if __name__ == "__main__":
    app = PluginManagerApp()
    app.mainloop()
