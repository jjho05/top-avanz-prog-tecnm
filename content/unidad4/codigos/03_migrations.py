#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_migrations.py
----------------
Simulador de Migraciones de Base de Datos.
¿Qué pasa cuando lanzas la versión 2.0 de tu app y necesitas una nueva columna?
No puedes borrar la BD y crearla de nuevo (perderías datos).
Necesitas ALTER TABLE.

Este script simula un sistema de control de versiones para la BD.
"""

import sqlite3
import os

DB_FILE = "sistema.db"

# Historial de cambios (Schema Evolution)
MIGRACIONES = [
    # Versión 1: Estructura inicial
    """CREATE TABLE productos (
        id INTEGER PRIMARY KEY, 
        nombre TEXT, 
        precio REAL
    )""",
    
    # Versión 2: Agregar stock
    """ALTER TABLE productos ADD COLUMN stock INTEGER DEFAULT 0""",
    
    # Versión 3: Agregar categoría
    """ALTER TABLE productos ADD COLUMN categoria TEXT DEFAULT 'General'"""
]

def get_current_version(cursor):
    """Obtiene la versión actual de la BD."""
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS meta (version INTEGER)")
        cursor.execute("SELECT version FROM meta")
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            # Inicializar en 0
            cursor.execute("INSERT INTO meta (version) VALUES (0)")
            return 0
    except Exception:
        return 0

def aplicar_migraciones():
    print(f"--- Sistema de Migraciones ---")
    
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        
        # 1. Verificar versión
        version_actual = get_current_version(c)
        print(f"Versión de BD actual: v{version_actual}")
        print(f"Versión de Código:    v{len(MIGRACIONES)}")
        
        # 2. Aplicar cambios pendientes
        if version_actual < len(MIGRACIONES):
            print("\n🔄 Actualizando esquema...")
            for v in range(version_actual, len(MIGRACIONES)):
                sql = MIGRACIONES[v]
                print(f"   Ejecutando migración v{v+1}...")
                try:
                    c.execute(sql)
                    # Actualizar meta
                    c.execute("UPDATE meta SET version = ?", (v + 1,))
                    conn.commit()
                    print("   ✅ Éxito.")
                except Exception as e:
                    print(f"   ❌ Error crítico en v{v+1}: {e}")
                    break
        else:
            print("\n✅ La base de datos está al día.")

def main():
    # Primera ejecución
    print("\n[DIA 1] Lanzamiento inicial")
    aplicar_migraciones()
    
    # Borremos la versión "meta" para engañar al sistema (Simular que es una BD vieja)
    # PERO, en este script, la lista MIGRACIONES es estática.
    # Para probar el concepto, ejecutarías este script varias veces agregando strings a la lista MIGRACIONES.
    
    # Limpieza (Para que el lab sea repetible)
    if input("\n¿Borrar DB de prueba? (s/n): ") == 's':
        os.remove(DB_FILE)

if __name__ == "__main__":
    main()
