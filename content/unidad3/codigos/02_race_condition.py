#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_race_condition.py
--------------------
El peligro oculto: Condición de Carrera (Race Condition).
Ocurre cuando dos hilos modifican una variable compartida al mismo tiempo.

Escenario:
    Un banco tiene $100.
    100 hilos intentan depositar $1.
    100 hilos intentan retirar $1.
    El final debería ser $100.
    SIN LOCKS: El resultado es impredecible (ej. $95, $102).

Solución:
    Descomentar la linea `lock.acquire()` y `lock.release()`.
"""

import threading
import time

class CuentaBancaria:
    def __init__(self):
        self.saldo = 0
        self.lock = threading.Lock()
    
    def transaccion(self, cantidad):
        # --- ZONA CRITICA ---
        # self.lock.acquire() # <--- DESCOMENTAR PARA ARREGLAR
        
        copia_local = self.saldo
        # time.sleep(0.00001) # El context switch ocurre aquí
        copia_local += cantidad
        self.saldo = copia_local
        
        # self.lock.release() # <--- DESCOMENTAR PARA ARREGLAR
        # --- FIN ZONA CRITICA ---

def main():
    cuenta = CuentaBancaria()
    hilos = []
    
    print("Iniciando 1000 transacciones simultáneas...")
    
    # 500 depositos, 500 retiros
    for _ in range(500):
        t1 = threading.Thread(target=cuenta.transaccion, args=(1,))
        t2 = threading.Thread(target=cuenta.transaccion, args=(-1,))
        hilos.append(t1)
        hilos.append(t2)
        t1.start()
        t2.start()
        
    for t in hilos:
        t.join()
        
    print(f"Saldo Final Esperado: 0")
    print(f"Saldo Final Real:     {cuenta.saldo}")
    
    if cuenta.saldo != 0:
        print("❌ ¡CONDICIÓN DE CARRERA DETECTADA! El dinero desapareció/apareció.")
        print("Edita el archivo y descomenta los locks para arreglarlo.")
    else:
        print("✅ Suerte... o ya usaste locks.")

if __name__ == "__main__":
    main()
