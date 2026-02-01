#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_decoradores_avanzados.py
---------------------------
Los decoradores son funciones que modifican otras funciones.
En frameworks como Flask o Django, son esenciales.

Conceptos:
1. `functools.wraps`: Preservar metadatos (nombre, docstring).
2. Decoradores con argumentos (`@route('/home')`).
3. Decoradores de clases.

Laboratorio:
    Crearemos un decorador `@retry` que reintenta ejecutar una función si falla,
    y un `@timer` que mide el tiempo de ejecución.
"""

import time
import functools
import random

# --- 1. Decorador Simple (Mide tiempo) ---
def timer(func):
    """Mide el tiempo de ejecución de una función."""
    @functools.wraps(func) # Buena práctica: Mantiene el nombre original
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱ [{func.__name__}] tardó {end - start:.4f}s")
        return result
    return wrapper

# --- 2. Decorador con Argumentos (Retry Logic) ---
def retry(max_attempts=3, delay=1):
    """Reintenta la función si lanza excepción."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"⚠️ Error en {func.__name__}: {e}. Reintentando ({attempts}/{max_attempts})...")
                    time.sleep(delay)
            print(f"❌ Falló tras {max_attempts} intentos.")
            return None # O lanzar excepción
        return wrapper
    return decorator

# --- 3. Uso Práctico ---

@timer
@retry(max_attempts=3, delay=0.5)
def servicio_inestable():
    """Simula una conexión a API que falla aleatoriamente."""
    if random.random() < 0.7:
        raise ConnectionError("Timeout de red simulado")
    return "Datos recibidos OK (200)"

@timer
def funcion_pesada(n):
    """Calcula suma de cuadrados."""
    return sum(i*i for i in range(n))

def main():
    print("--- Probando Decoradores ---")
    
    print("\n1. Llamando a servicio inestable:")
    res = servicio_inestable()
    print(f"Resultado: {res}")
    
    print("\n2. Llamando a función pesada:")
    funcion_pesada(1000000)
    
    # Introspección (Gracias a functools.wraps)
    print(f"\nNombre real de la función: {servicio_inestable.__name__}")
    print(f"Docstring: {servicio_inestable.__doc__}")

if __name__ == "__main__":
    main()
