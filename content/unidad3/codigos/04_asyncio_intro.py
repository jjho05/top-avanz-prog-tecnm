#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_asyncio_intro.py
-------------------
Introducción a Asyncio (Asynchronous I/O).
El modelo de concurrencia moderno de Python (single-threaded cooperative).

Diferencia con Hilos:
- Hilos: El SO decide cuándo cambiar (Preemptive).
- Asyncio: TU decides cuándo pausar con `await` (Cooperative).

Escenario:
    Hervir agua, tostar pan y freír huevos "al mismo tiempo".
"""

import asyncio
import time

async def hervir_agua():
    print("💧 Poniendo agua a hervir (3s)...")
    await asyncio.sleep(3) # Cede el control aquí
    print("💧 ¡Agua hirviendo!")
    return "Agua Caliente"

async def tostar_pan():
    print("🍞 Tostando pan (2s)...")
    await asyncio.sleep(2)
    print("🍞 ¡Pan tostado!")
    return "Tostada"

async def freir_huevos():
    print("🍳 Friendo huevos (4s)...")
    await asyncio.sleep(4) # Tarea más lenta
    print("🍳 ¡Huevos listos!")
    return "Huevos Fritos"

async def preparar_desayuno():
    start = time.perf_counter()
    print("👨‍🍳 Iniciando desayuno asíncrono...")
    
    # gather ejecuta todo concurrentemente y espera a que TODO termine
    resultados = await asyncio.gather(
        hervir_agua(),
        tostar_pan(),
        freir_huevos()
    )
    
    end = time.perf_counter()
    print(f"\n✅ Desayuno servido: {resultados}")
    print(f"Tiempo Total: {end - start:.2f}s (vs 9s secuencial)")

def main():
    # En Python 3.7+ usamos asyncio.run
    asyncio.run(preparar_desayuno())

if __name__ == "__main__":
    main()
