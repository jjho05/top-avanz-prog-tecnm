#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_performance.py
-----------------
Introducción al Profiling (Análisis de Rendimiento).
¿Tu código es lento? No adivines. Mide.

Conceptos:
1. `time.perf_counter()`: Medición precisa de tiempo de pared.
2. `cProfile`: Profiler determinista integrado en Python.
3. Complejidad Algorítmica (Big O) demostrada en la práctica.

Compararemos:
    - Concatenación de strings con '+' (Lento, O(n^2)).
    - Concatenación con 'join' (Rápido, O(n)).
"""

import time
import cProfile
import io
import pstats

ITERACIONES = 50000

def metodo_lento():
    """Concatena strings uno por uno. Crea copias en memoria cada vez."""
    resultado = ""
    for i in range(ITERACIONES):
        resultado += str(i)
    return resultado

def metodo_rapido():
    """Usa una lista y join. O(n)."""
    lista = []
    for i in range(ITERACIONES):
        lista.append(str(i))
    return "".join(lista)

def medir_tiempo(func, nombre):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    print(f"[{nombre}] Tiempo: {end - start:.4f} segundos")

def main():
    print(f"--- Benchmark (N={ITERACIONES}) ---")
    
    # 1. Medición simple
    medir_tiempo(metodo_lento, "String + (Lento)")
    medir_tiempo(metodo_rapido, "String .join (Rápido)")
    
    # 2. Profiling Profundo
    print("\n--- Analizando con cProfile ---")
    pr = cProfile.Profile()
    pr.enable()
    
    # Ejecutamos ambos
    metodo_lento()
    metodo_rapido()
    
    pr.disable()
    
    # Reporte
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats(10) # Top 10 funciones más lentas
    print(s.getvalue())

if __name__ == "__main__":
    main()
