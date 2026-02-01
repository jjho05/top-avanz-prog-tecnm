#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_context_managers.py
----------------------
Gestores de Contexto (`with`).
Administran recursos automáticamente (Archivos, Conexiones DB, Locks).
Garantizan que el recurso se libere incluso si hay errores.

Conceptos:
1. Protocolo `__enter__` y `__exit__`.
2. Decorador `@contextlib.contextmanager` (Generadores).
3. Caso de uso: Cronómetro de bloque y Gestión de Archivos segura.
"""

import time
import os
from contextlib import contextmanager

# --- 1. Enfoque Basado en Clases (El Clásico) ---
class Cronometro:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def __enter__(self):
        """Se ejecuta al iniciar el 'with'."""
        self.start = time.perf_counter()
        print(f"⏳ Iniciando bloque '{self.nombre}'...")
        return self # Esto se asigna a la variable 'as x'
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Se ejecuta al salir, incluso con error."""
        end = time.perf_counter()
        duracion = end - self.start
        print(f"🏁 Bloque '{self.nombre}' finalizado en {duracion:.4f}s")
        
        if exc_type:
            print(f"   ⚠️ Salió por error: {exc_val}")
            return True # True = Suprimir error (No propagar), False = Propagar

# --- 2. Enfoque Basado en Generadores (El Moderno) ---
@contextmanager
def abrir_temporal(contenido, nombre_archivo="temp.txt"):
    """Crea un archivo, escribe, y lo BORRA al salir."""
    try:
        f = open(nombre_archivo, "w")
        f.write(contenido)
        f.close()
        print(f"📁 Archivo temporal {nombre_archivo} creado.")
        yield nombre_archivo # Pausa y entrega el valor
    finally:
        # Esto ocurre en el __exit__
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
            print(f"🗑️ Archivo temporal {nombre_archivo} eliminado.")

def main():
    # Uso de Clase
    with Cronometro("Proceso Matemático"):
        sum([i**2 for i in range(100000)])
        # time.sleep(0.5)

    print("-" * 20)

    # Uso con Error capturado
    with Cronometro("Proceso Fallido (Controlado)"):
        print("   Ejecutando código peligroso...")
        raise ValueError("Oops, algo salió mal")
    print("El programa continúa porque __exit__ retornó True.\n")
    
    print("-" * 20)

    # Uso de Generador
    with abrir_temporal("Hola Mundo", "test.tmp") as temp_file:
        print(f"   Dentro del contexto: El archivo {temp_file} existe.")
        # Simular lectura
        with open(temp_file, "r") as f:
            print(f"   Contenido leído: {f.read()}")
            
    print("   Fuera del contexto: El archivo ya no existe.")

if __name__ == "__main__":
    main()
