#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_sqlite_raw.py
----------------
Acceso a Datos Nativo con SQLite.
Lo que aprenderás: 
1. `sqlite3` driver estándar.
2. Context Managers para conexiones.
3. El peligro mortal de la INYECCIÓN SQL.

Escenario:
    Un login inseguro vs uno seguro.
"""

import sqlite3
import os

DB_FILE = "demo.db"

def setup_db():
    if os.path.exists(DB_FILE): os.remove(DB_FILE)
    
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "secret123"))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("pepe", "1234"))
        conn.commit()

def login_INSEGURO(user, password):
    """
    ❌ EJEMPLO DE CÓDIGO VULNERABLE.
    Formatea el string directamente. UN HACKER PUEDE ENTRAR.
    """
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{password}'"
    print(f"\n[INSEGURO] Ejecutando: {query}")
    
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        try:
            c.execute(query) # <--- AQUÍ ESTÁ EL ERROR
            result = c.fetchone()
            return result is not None
        except Exception as e:
            return False

def login_SEGURO(user, password):
    """
    ✅ EJEMPLO CORRECTO.
    Usa 'Placeholder binding' (?). El driver escapa los datos.
    """
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"\n[SEGURO]   Ejecutando: {query} con params ({user}, {password})")
    
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(query, (user, password)) # <--- LA FORMA CORRECTA
        result = c.fetchone()
        return result is not None

def main():
    setup_db()
    
    print("--- 1. Login Normal ---")
    print("Login Pepe: ", login_INSEGURO("pepe", "1234"))
    
    print("\n--- 2. Ataque de SQL Injection ---")
    payload = "' OR '1'='1"
    print(f"Hacker intenta entrar con usuario: {payload}")
    
    exito = login_INSEGURO(payload, "cualquier_cosa")
    if exito:
        print("🔴 ¡HACKEADO! El sistema inseguro permitió el acceso.")
    
    print("\n--- 3. Defensa ---")
    exito = login_SEGURO(payload, "cualquier_cosa")
    if exito:
        print("🔴 ¡Hackeado nuevamente! (Imposible)")
    else:
        print("🟢 Acceso denegado. El sistema seguro neutralizó el ataque.")
        
    os.remove(DB_FILE)

if __name__ == "__main__":
    main()
