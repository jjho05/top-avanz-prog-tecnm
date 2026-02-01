#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_check_env.py
---------------
Script de Diagnóstico de Entorno Profesional (DevOps Ready).
Este script no solo imprime "Hola Mundo", sino que inspecciona el runtime
para asegurar que el entorno de despliegue cumple con los requisitos del curso.

Conceptos:
1. Módulo `sys`: Acceso a variables del intérprete.
2. Módulo `platform`: Datos del Hardware/OS.
3. Módulo `shutil`: Verificar herramientas externas (git, gcc).
4. Verificación de versiones con `packaging` (o tuplas simples).

Uso:
    python 01_check_env.py
"""

import sys
import platform
import shutil
import os
from datetime import datetime

# Configuración de requisitos
MIN_PYTHON_VERSION = (3, 10)
REQUIRED_TOOLS = ["git", "pip"]

def print_header(title):
    print(f"\n{'='*40}")
    print(f" {title.upper()}")
    print(f"{'='*40}")

def check_python():
    print_header("Intérprete Python")
    print(f"Executable: {sys.executable}")
    print(f"Version:    {sys.version.split()[0]}")
    print(f"Compiler:   {platform.python_compiler()}")
    print(f"Implement.: {platform.python_implementation()}")
    
    current_ver = sys.version_info[:2]
    if current_ver < MIN_PYTHON_VERSION:
        print(f"\n[ERROR] Se requiere Python {MIN_PYTHON_VERSION}+. Tienes {current_ver}.")
        return False
    else:
        print("\n[OK] Versión de Python correcta.")
        return True

def check_system():
    print_header("Sistema Operativo")
    print(f"System:     {platform.system()} {platform.release()}")
    print(f"Node:       {platform.node()}")
    print(f"Machine:    {platform.machine()}")
    print(f"Processor:  {platform.processor()}")
    print(f"Cores (Log):{os.cpu_count()}")

def check_tools():
    print_header("Herramientas Externas")
    all_ok = True
    for tool in REQUIRED_TOOLS:
        path = shutil.which(tool)
        status = f"[OK] ({path})" if path else "[FALTA]"
        if not path: all_ok = False
        print(f"{tool:<10}: {status}") 
    return all_ok

def check_virtual_env():
    print_header("Entorno Virtual")
    # sys.prefix != sys.base_prefix indica que estamos en un VENV
    is_venv = sys.prefix != sys.base_prefix
    print(f"Activo:     {'SÍ' if is_venv else 'NO'}")
    print(f"Path:       {sys.prefix}")
    
    if not is_venv:
        print("\n[ADVERTENCIA] No estás usando un entorno virtual.")
        print("Recomendación: python -m venv .venv && source .venv/bin/activate")

def main():
    print(f"Iniciando Diagnóstico - {datetime.now()}")
    
    py_ok = check_python()
    check_system()
    check_virtual_env()
    tools_ok = check_tools()
    
    print_header("Resumen")
    if py_ok and tools_ok:
        print("✅ EL ENTORNO ESTÁ LISTO PARA EL CURSO.")
        sys.exit(0)
    else:
        print("❌ HAY PROBLEMAS CRÍTICOS.")
        sys.exit(1)

if __name__ == "__main__":
    main()
