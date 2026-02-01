#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_debugging_demo.py
--------------------
Técnicas de Depuración (Debugging).
Muchos estudiantes solo usan `print()`. Aquí aprenderemos a usar `pdb`.

Conceptos:
1. `breakpoint()`: Detiene la ejecución e invoca al debugger interactivo.
2. Comandos PDB:
    - n (next): Siguiente línea.
    - s (step): Entrar a función.
    - c (continue): Continuar hasta el final.
    - p variable: Imprimir valor.

Instrucciones:
    Ejecuta el script. Se detendrá en la línea 'breakpoint()'.
    Escribe 'p i' para ver el contador.
    Escribe 'c' para terminar.
"""

import sys

def funcion_con_bug_logico(a, b):
    # Imagina que esta función es compleja
    resultado = a + b
    
    # ¡BOOM! Aquí queremos inspeccionar
    # En Python 3.7+ usamos breakpoint() nativo
    print(f"-> Entrando al debugger con a={a}, b={b}...")
    # breakpoint()  # <--- DESCOMENTAR ESTA LÍNEA PARA PROBAR PDB
    
    # Bug simulado: Debería multiplicar pero suma
    return resultado

def procesar_lista(numeros):
    total = 0
    for i, n in enumerate(numeros):
        parcial = funcion_con_bug_logico(total, n)
        total = parcial
        
        # Simulación de log complejo
        # sys.stdout.write(f"\rProcesando {i}/{len(numeros)}")
        
    return total

def main():
    datos = [10, 20, 30, 40, 50]
    print("Iniciando proceso batch...")
    
    res = procesar_lista(datos)
    
    print(f"\nResultado final: {res}")
    print("Si el resultado no es el esperado, usa el debugger.")

if __name__ == "__main__":
    main()
