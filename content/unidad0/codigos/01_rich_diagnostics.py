#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_rich_diagnostics.py
----------------------
Diagnóstico de Entorno con UX Avanzada (Rich Library).

En lugar de imprimir texto plano aburrido, usamos 'rich' para renderizar
tablas, paneles, emojis y barras de progreso.
Esto demuestra que incluso las herramientas de CLI pueden tener una UX estelar.

Requisitos:
    pip install rich
"""

import sys
import platform
import shutil
import os
import time
from datetime import datetime

# Intentar importar rich
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import track
    from rich.layout import Layout
    from rich.text import Text
    from rich import print as rprint
except ImportError:
    print("❌ ERROR CRÍTICO: Debes instalar 'rich'.")
    print("Ejecuta: pip install rich")
    sys.exit(1)

console = Console()

# Configuración
MIN_PYTHON = (3, 10)
TOOLS = ["git", "pip", "gcc", "docker", "code"]

def get_python_info():
    ver = sys.version_info
    ver_str = f"{ver.major}.{ver.minor}.{ver.micro}"
    is_valid = ver >= MIN_PYTHON
    
    table = Table(title="🐍 Intérprete Python", expand=True, border_style="green" if is_valid else "red")
    table.add_column("Propiedad", style="cyan")
    table.add_column("Valor", style="magenta")
    
    table.add_row("Versión Actual", ver_str)
    table.add_row("Versión Mínima", f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}+")
    table.add_row("Ruta Ejecutable", sys.executable)
    table.add_row("Compiler", platform.python_compiler())
    
    status = "✅ APROBADO" if is_valid else "❌ OBSOLETO"
    return Panel(table, title=f"Estado: {status}", border_style="green" if is_valid else "red")

def get_system_info():
    table = Table(title="💻 Sistema Operativo", expand=True)
    table.add_column("Hardwre/OS", style="blue")
    table.add_column("Detalle", style="white")
    
    table.add_row("Sistema", f"{platform.system()} {platform.release()}")
    table.add_row("Arquitectura", platform.machine())
    table.add_row("Procesador", platform.processor() or "Desconocido")
    table.add_row("Núcleos CPU", str(os.cpu_count()))
    table.add_row("Hostname", platform.node())
    
    return Panel(table, border_style="blue")

def check_tools_with_progress():
    table = Table(title="🛠 Herramientas Externas", expand=True)
    table.add_column("Herramienta")
    table.add_column("Estado")
    table.add_column("Ruta")

    # Simular carga para efecto dramático (UX)
    for tool in track(TOOLS, description="Escaneando PATH..."):
        time.sleep(0.2) # Fake processing
        path = shutil.which(tool)
        if path:
            table.add_row(f"[bold green]{tool}[/]", "✅ Instalado", path)
        else:
            table.add_row(f"[bold red]{tool}[/]", "❌ No encontrado", "-")
            
    return Panel(table, border_style="yellow")

def main():
    console.clear()
    rprint(Panel.fit("[bold white on blue] Tópicos Avanzados de Programación [/]\n[italic]Diagnóstico de Entorno v2.0[/]", border_style="blue"))
    
    with console.status("[bold green]Recopilando telemetría...[/]", spinner="dots"):
        time.sleep(1) # UX Delay
        py_panel = get_python_info()
        sys_panel = get_system_info()
    
    console.print(sys_panel)
    console.print(py_panel)
    
    # Herramientas con barra de carga real
    tools_panel = check_tools_with_progress()
    console.print(tools_panel)
    
    # Venv Check
    is_venv = sys.prefix != sys.base_prefix
    if is_venv:
        rprint(Panel("✅ Entorno Virtual [bold green]ACTIVO[/]", border_style="green"))
    else:
        rprint(Panel("⚠️  [bold yellow]ADVERTENCIA:[/bold yellow] No estás en un VirtualEnv.\nRecomendado: [code]python -m venv .venv[/code]", border_style="yellow"))

    rprint("\n[bold green]➜ Diagnóstico Finalizado.[/]")

if __name__ == "__main__":
    main()
