#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_seed_faker.py
----------------
Generación de Datos de Prueba (Seeding).
No puedes probar el rendimiento de tu BD con 3 registros. Necesitas 10,000.
Este script genera datos realistas simulados.

Nota: Intenta importar `faker`. Si no existe, usa un generador simple nativo.
"""

import sqlite3
import random
import time

try:
    from faker import Faker
    fake = Faker('es_MX') # Generador en Español Mexicano
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False
    print("⚠️  Librería 'faker' no instalada. Usando generador simple.")

class SimpleFaker:
    """Generador fallback si no hay librería 'faker'."""
    nombres = ["Juan", "Ana", "Pedro", "Maria", "Luis"]
    apellidos = ["Perez", "Gomez", "Lopez", "Diaz", "Hernandez"]
    
    def name(self):
        return f"{random.choice(self.nombres)} {random.choice(self.apellidos)}"
    
    def email(self):
        return f"usuario{random.randint(1000,9999)}@test.com"
    
    def address(self):
        return "Calle Conocida #123, Ciudad"

fake_gen = fake if HAS_FAKER else SimpleFaker()

def seed_database(limit=1000):
    print(f"🌱 Sembrando {limit} usuarios en 'big_data.db'...")
    
    conn = sqlite3.connect("big_data.db")
    c = conn.cursor()
    
    # Optimización: PRAGMAS para velocidad masiva
    c.execute("PRAGMA synchronous = OFF")
    c.execute("PRAGMA journal_mode = MEMORY")
    
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, nombre TEXT, email TEXT, direccion TEXT)")
    c.execute("DELETE FROM users") # Limpiar previo
    
    start = time.time()
    
    # Transacción ÚNICA gigante (Esencial para velocidad)
    usuarios = []
    for i in range(limit):
        usuarios.append((
            fake_gen.name(),
            fake_gen.email(),
            fake_gen.address().replace("\n", ", ")
        ))
    
    c.executemany("INSERT INTO users (nombre, email, direccion) VALUES (?, ?, ?)", usuarios)
    conn.commit()
    
    end = time.time()
    speed = limit / (end - start)
    print(f"✅ Terminado en {end - start:.4f}s ({speed:.0f} insert/s)")
    conn.close()

if __name__ == "__main__":
    seed_database(10000) # Intenta con 1 millón si te atreves
    import os
    # os.remove("big_data.db") # Comentar para inspeccionar con DB Browser
