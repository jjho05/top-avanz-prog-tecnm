#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_introspeccion_profunda.py
----------------------------
La Introspección (Reflection) es la capacidad de un programa para 
examinarse a sí mismo en tiempo de ejecución.
Fundamental para Frameworks, ORMs y herramientas de Debugging.

Conceptos:
1. `type()`, `id()`, `dir()`: La trinidad básica.
2. `inspect`: Módulo estándar para inspeccionar objetos vivos.
3. `getattr`, `setattr`: Manipulación dinámica.
4. Análisis de Frames y Stack Trace.

Laboratorio:
    Analizaremos una función desconocida para ver sus argumentos y código fuente.
"""

import inspect
import types

class CajaNegra:
    """Una clase misteriosa para analizar."""
    SECRETO = 42
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._privado = "Shh"

    def procesar(self, a: int, b: int = 10) -> int:
        """Suma a y b y multiplica por el secreto."""
        return (a + b) * self.SECRETO

def analista_de_codigo(obj):
    print(f"\n🔍 --- ANALIZANDO: {obj} ---")
    
    # 1. Identidad básica
    print(f"Tipo:       {type(obj)}")
    print(f"ID Memoria: {hex(id(obj))}")
    
    # 2. Miembros (dir)
    print(f"Atributos (dir): {len(dir(obj))} encontrados.")
    
    # 3. Inspección Profunda (inspect)
    if inspect.isclass(obj):
        print(">> Es una CLASE")
        try:
            # Obtener código fuente
            src = inspect.getsource(obj)
            print(f">> Source Code Preview:\n{src[:100]}...")
        except OSError:
            print(">> No se puede acceder al source (probablemente nativo C).")
            
    elif inspect.isfunction(obj) or inspect.ismethod(obj):
        print(">> Es una FUNCION/METODO")
        # Firma (Signature)
        sig = inspect.signature(obj)
        print(f">> Firma: {sig}")
        
        # Parámetros por separado
        for name, param in sig.parameters.items():
            print(f"   - Arg: {name:<10} Default: {param.default} Anotación: {param.annotation}")

def main():
    # Caso 1: Analizar una clase
    analista_de_codigo(CajaNegra)
    
    # Caso 2: Analizar una instancia
    instancia = CajaNegra("Test")
    analista_de_codigo(instancia)
    
    # Caso 3: Metaprogramación - Modificar en runtime
    print("\n🛠 --- HACKING EN RUNTIME ---")
    print(f"Antes: {instancia.procesar(1)}")
    
    # Inyectamos un nuevo atributo
    setattr(instancia, "nuevo_attr", 999)
    print(f"Inyectado: {instancia.nuevo_attr}")
    
    # Monkey Patching: Reemplazamos el método
    def hack(self, a, b=0):
        return "Hackeado"
    
    # Bindeamos la función a la instancia
    instancia.procesar = types.MethodType(hack, instancia)
    print(f"Despues: {instancia.procesar(1)}")

if __name__ == "__main__":
    main()
