#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_pip_automation.py
--------------------
Script de Automatización de Dependencias.
Demuestra cómo Python puede gestionarse a sí mismo.

Conceptos:
1. `subprocess`: Ejecutar comandos de terminal desde Python.
2. `importlib`: Verificar si un paquete ya está importable.
3. Gestión de `requirements.txt`.

Escenario:
    Este script intenta importar `requests` y `customtkinter`. 
    Si no existen, pregunta al usuario si desea instalarlos y ejecuta pip.
"""

import subprocess
import sys
import importlib.util

PACKAGES_TO_CHECK = [
    ("requests", "requests"),          # (nombre_import, nombre_pip)
    ("customtkinter", "customtkinter"),
    ("PIL", "pillow"),                 # PIL se instala como 'pillow'
    ("sqlalchemy", "sqlalchemy")
]

def install_package(package_name):
    """Instala un paquete usando pip vía subprocess."""
    print(f"📦 Instalando {package_name}...")
    try:
        # sys.executable asegura que usamos el pip del mismo entorno que este python
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} instalado correctamente.")
    except subprocess.CalledProcessError:
        print(f"❌ Error al instalar {package_name}.")

def check_and_install():
    print("--- Verificador de Dependencias ---")
    
    missing = []
    
    for import_name, pip_name in PACKAGES_TO_CHECK:
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f"[FALTA] {pip_name} (No se encuentra el módulo '{import_name}')")
            missing.append(pip_name)
        else:
            print(f"[OK]    {pip_name}")

    if not missing:
        print("\n🎉 Todas las dependencias están satisfechas.")
        return

    print(f"\nPaquetes faltantes: {', '.join(missing)}")
    resp = input("¿Desea instalar los faltantes ahora? (s/n): ").lower()
    
    if resp == 's':
        for pkg in missing:
            install_package(pkg)
        print("\nRe-ejecuta este script para verificar.")
    else:
        print("Operación cancelada.")

def generate_requirements():
    """Genera un archivo requirements.txt con las versiones actuales."""
    print("\n📄 Generando requirements.txt...")
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    with open("requirements.txt", "w") as f:
        f.write(result.stdout)
    print("✅ Archivo requirements.txt creado.")

if __name__ == "__main__":
    check_and_install()
    # generate_requirements() # Descomentar si se desea generar snapshot
