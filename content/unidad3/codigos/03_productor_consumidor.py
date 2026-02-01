#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_productor_consumidor.py
--------------------------
El problema clásico de sincronización.
Colas, Eventos y Semáforos.

Componentes:
1. `queue.Queue`: Cola thread-safe (¡No uses list!).
2. Productor: Genera "hamburguesas" (datos).
3. Consumidor: Come hamburguesas.
4. `Event`: Bandera para detener a los consumidores.

Escenario:
    Un chef cocina rápido.
    Dos clientes comen lento.
    La cola limita el buffer.
"""

import threading
import queue
import time
import random

CAPACIDAD_BUFFER = 5
NUM_PRODUCTOS = 20

def chef(q, evento_stop):
    for i in range(NUM_PRODUCTOS):
        item = f"Hamburguesa #{i+1}"
        time.sleep(random.uniform(0.1, 0.3)) # Cocinando
        
        # put bloquea si la cola está llena
        q.put(item) 
        print(f"👨‍🍳 Cocinó {item} (En espera: {q.qsize()})")
    
    print("👨‍🍳 ¡Cocina cerrada!")
    evento_stop.set() # Avisar que ya no habrá más

def cliente(id, q, evento_stop):
    while True:
        try:
            # timeout necesario para revisar el evento_stop
            item = q.get(timeout=1) 
            print(f"   😋 Cliente {id} comió {item}")
            time.sleep(random.uniform(0.4, 0.8)) # Comiendo lento
            q.task_done()
        except queue.Empty:
            if evento_stop.is_set():
                print(f"   👋 Cliente {id} se va.")
                break

def main():
    # Estructuras de sincronización
    ordenes = queue.Queue(maxsize=CAPACIDAD_BUFFER)
    cocina_cerrada = threading.Event()
    
    t_chef = threading.Thread(target=chef, args=(ordenes, cocina_cerrada))
    t_c1 = threading.Thread(target=cliente, args=(1, ordenes, cocina_cerrada))
    t_c2 = threading.Thread(target=cliente, args=(2, ordenes, cocina_cerrada))
    
    t_chef.start()
    t_c1.start()
    t_c2.start()
    
    t_chef.join()
    t_c1.join()
    t_c2.join()
    
    print("\nSimulación terminada.")

if __name__ == "__main__":
    main()
