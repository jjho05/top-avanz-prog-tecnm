#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_package.py
---------------
Script para probar el paquete que acabamos de crear.
Simula ser un usuario final usando nuestra librería.
"""

try:
    # Intento de import absoluto (funciona si estás en la carpeta correcta)
    import mypackage
except ImportError:
    # Hack para que funcione en el repo sin instalar con pip
    import sys
    import os
    sys.path.append(os.getcwd())
    import mypackage

def main():
    print(f"Versión del paquete: {mypackage.VERSION}")
    
    # Usamos la clase expuesta en __init__
    calc = mypackage.Calculadora()
    print(f"Objeto creado: {calc}")
    
    res = calc.sumar(100, 250)
    print(f"Suma: {res}")
    
    # Usamos utilidad expuesta
    print(f"Formato Moneda: {mypackage.formatear_numero(12345.6789)}")

if __name__ == "__main__":
    main()
