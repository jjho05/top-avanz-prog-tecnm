#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_slots_vs_dict.py
-------------------
Optimización de Memoria: __slots__ vs __dict__.
Por defecto, Python guarda los atributos de un objeto en un diccionario.
Esto es flexible pero costoso en RAM.
`__slots__` le dice a Python que reserve espacio fijo para atributos predefinidos,
eliminando el diccionario dinámico.

Conceptos:
1. `sys.getsizeof`: Medir tamaño en bytes.
2. `pympler` (simulado): Para medir árboles de objetos.
3. Diferencias de tiempo de acceso.

Instrucciones:
    python 04_slots_vs_dict.py
"""

import sys
import time
import timeit

# Clase Estándar (Usa __dict__)
class PixelDict:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Clase Optimizada (Usa __slots__)
class PixelSlots:
    __slots__ = ['x', 'y', 'z']
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def main():
    N = 1_000_000 # Un millón de objetos
    
    print(f"--- Creando {N} objetos de cada tipo ---")
    
    # 1. Medición de Tiempo de Creación
    start = time.time()
    lista_dict = [PixelDict(1, 2, 3) for _ in range(N)]
    t_dict = time.time() - start
    print(f"Tiempo Clase Normal: {t_dict:.4f} s")
    
    start = time.time()
    lista_slots = [PixelSlots(1, 2, 3) for _ in range(N)]
    t_slots = time.time() - start
    print(f"Tiempo Clase Slots:  {t_slots:.4f} s ({(t_dict/t_slots):.1f}x más rápido)")
    
    # 2. Medición aproximada de RAM (Solo referencias + objetos básicos)
    # Nota: sys.getsizeof no mide recursivamente todo, pero sirve de proxy.
    
    size_dict_obj = sys.getsizeof(lista_dict[0]) + sys.getsizeof(lista_dict[0].__dict__)
    size_slots_obj = sys.getsizeof(lista_slots[0])
    
    print("\n--- Tamaño por Objeto (Estimado) ---")
    print(f"Normal (__dict__): ~{size_dict_obj} bytes")
    print(f"Slots:             ~{size_slots_obj} bytes")
    print(f"Ahorro memoria:    {100 * (1 - size_slots_obj/size_dict_obj):.1f}%")

    # 3. Acceso a atributos
    print("\n--- Velocidad de Acceso (Lectura) ---")
    t_read_dict = timeit.timeit("o.x", globals={"o": lista_dict[0]}, number=10_000_000)
    t_read_slots = timeit.timeit("o.x", globals={"o": lista_slots[0]}, number=10_000_000)
    
    print(f"Lectura Dict:  {t_read_dict:.4f} s")
    print(f"Lectura Slots: {t_read_slots:.4f} s (Más rápido)")
    
    print("\nConclusión: Usa __slots__ si vas a crear MILLONES de objetos pequeños.")

if __name__ == "__main__":
    main()
