#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_hilos_vs_procesos.py
-----------------------
Demostración definitiva: CPU-Bound vs I/O-Bound.

Conceptos:
1. `threading`: Comparten memoria, limitados por GIL. Bueno para dormir (I/O).
2. `multiprocessing`: Memoria separada, sin GIL. Bueno para calcular (CPU).

Experimento:
    Calcularemos sumas masivas (CPU Heavy).
    Veremos que los Hilos NO mejoran el tiempo (a veces lo empeoran).
    Veremos que los Procesos dividen el tiempo por N núcleos.
"""

import time
import threading
import multiprocessing
import os

NUM_CORES = multiprocessing.cpu_count()
NUMERO = 50_000_000

def cpu_bound_task(n):
    """Tarea pesada: contar hasta N."""
    while n > 0:
        n -= 1

def run_threads():
    print(f"\n--- HILOS (Threading) con {NUM_CORES} workers ---")
    start = time.time()
    threads = []
    chunk = NUMERO // NUM_CORES
    
    for _ in range(NUM_CORES):
        t = threading.Thread(target=cpu_bound_task, args=(chunk,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    end = time.time()
    print(f"Tiempo Total: {end - start:.4f} segundos (El GIL duele)")

def run_processes():
    print(f"\n--- PROCESOS (Multiprocessing) con {NUM_CORES} workers ---")
    start = time.time()
    processes = []
    chunk = NUMERO // NUM_CORES
    
    for _ in range(NUM_CORES):
        p = multiprocessing.Process(target=cpu_bound_task, args=(chunk,))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    end = time.time()
    print(f"Tiempo Total: {end - start:.4f} segundos (Paralelismo Real)")

def main():
    print(f"CPU detectado: {NUM_CORES} núcleos")
    print(f"Tarea: Contar hasta {NUMERO:,}")
    
    # 1. Base (Serial)
    print("\n--- SERIAL (Sin concurrencia) ---")
    start = time.time()
    cpu_bound_task(NUMERO)
    end = time.time()
    print(f"Tiempo: {end - start:.4f} segundos")
    
    # 2. Hilos
    run_threads()
    
    # 3. Procesos
    run_processes()

if __name__ == "__main__":
    main()
