#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_plugin_loader.py
-------------------
Arquitectura de Plugins Dinámica.
Cómo cargar código Python nuevo sin reiniciar la aplicación principal.
Es la base de sistemas como VS Code, Django Apps o WordPress.

Conceptos:
1. `importlib.import_module`: Importar por string.
2. `pkgutil.iter_modules`: Escanear directorios buscando módulos.
3. Definición de una Interfaz (Protocolo ABstracto).
"""

import importlib
import pkgutil
import os
import sys
from abc import ABC, abstractmethod

# --- 1. Definición del Contrato (Interface) ---
class PluginInterface(ABC):
    @abstractmethod
    def run(self):
        """Ejecuta la acción del plugin."""
        pass
    
    @property
    @abstractmethod
    def name(self):
        """Nombre legible del plugin."""
        pass

# --- 2. Sistema de Plugins ---
class PluginManager:
    def __init__(self, plugin_package_name):
        self.package_name = plugin_package_name
        self.plugins = []

    def discover_plugins(self):
        """Escanea la carpeta del paquete buscando módulos que cumplan la interfaz."""
        print(f"🔍 Buscando plugins en '{self.package_name}'...")
        
        # Debemos asegurar que el CWD está en el path
        sys.path.append(os.getcwd())
        
        try:
            # Importar el paquete contenedor (debe existir la carpeta/__init__.py)
            package = importlib.import_module(self.package_name)
            
            # Iterar sobre sus contenidos
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                full_name = f"{self.package_name}.{name}"
                self._load_plugin(full_name)
                
        except ImportError as e:
            print(f"❌ Error: No se encuentra el paquete de plugins ({e})")
            print("Crea una carpeta 'plugins_repo' con un '__init__.py' vacio para probar.")

    def _load_plugin(self, module_name):
        try:
            module = importlib.import_module(module_name)
            # Buscar clases que hereden de PluginInterface
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, PluginInterface) and attr is not PluginInterface:
                    # Instanciar y registrar
                    instance = attr()
                    self.plugins.append(instance)
                    print(f"✅ Cargado: {instance.name}")
        except Exception as e:
            print(f"⚠️ Error cargando {module_name}: {e}")

    def run_all(self):
        print(f"\n🚀 Ejecutando {len(self.plugins)} plugins...")
        for p in self.plugins:
            print(f"--- {p.name} ---")
            p.run()

# --- 3. Simulación (Creación de plugins falsos en memoria/disco) ---
# Para que este script funcione "Out of the Box", crearemos la estructura temporalmente

def setup_demo_env():
    os.makedirs("plugins_repo", exist_ok=True)
    with open("plugins_repo/__init__.py", "w") as f: f.write("")
    
    # Plugin 1: Hola Mundo
    with open("plugins_repo/hello.py", "w") as f:
        f.write('''
from __main__ import PluginInterface
class HelloPlugin(PluginInterface):
    name = "Hola Mundo Plugin"
    def run(self):
        print("¡Hola desde un archivo cargado dinámicamente!")
''')
    
    # Plugin 2: Calculadora
    with open("plugins_repo/calc.py", "w") as f:
        f.write('''
from __main__ import PluginInterface
class CalcPlugin(PluginInterface):
    name = "Math Plugin"
    def run(self):
        print(f"2 + 2 = {2+2}")
''')

def main():
    setup_demo_env()
    
    manager = PluginManager("plugins_repo")
    manager.discover_plugins()
    manager.run_all()
    
    # Cleanup (Opcional, para no ensuciar)
    # import shutil; shutil.rmtree("plugins_repo")

if __name__ == "__main__":
    main()
