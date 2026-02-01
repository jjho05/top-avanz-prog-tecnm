#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_repository_pattern.py
------------------------
Arquitectura Limpia: Patrón Repositorio.
El objetivo es separar la Lógica de Negocio de la Base de Datos.
Si mañana cambiamos SQLite por MongoDB, la App no debería romperse.

Capas:
1. Modelo (Entidad pura).
2. Repositorio (Interface de acceso a datos).
3. Servicio (Lógica de negocio).
"""

from abc import ABC, abstractmethod
import sqlite3

# --- 1. Modelo (Entidad) ---
class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio
    
    def __repr__(self):
        return f"<Prod {self.nombre} ${self.precio}>"

# --- 2. Abstracción del Repositorio ---
class IProductoRepository(ABC):
    @abstractmethod
    def get_by_id(self, id): pass
    
    @abstractmethod
    def add(self, producto): pass

# --- 3. Implementación Concreta (SQLite) ---
class SQLiteProductoRepository(IProductoRepository):
    def __init__(self, connection):
        self.conn = connection
        self.conn.execute("CREATE TABLE IF NOT EXISTS productos (id INTEGER, nombre TEXT, precio REAL)")

    def get_by_id(self, id):
        c = self.conn.cursor()
        c.execute("SELECT id, nombre, precio FROM productos WHERE id = ?", (id,))
        row = c.fetchone()
        return Producto(*row) if row else None

    def add(self, producto):
        self.conn.execute("INSERT INTO productos VALUES (?, ?, ?)", 
                          (producto.id, producto.nombre, producto.precio))
        self.conn.commit()

# --- 4. Implementación Concreta (Memoria - para Tests) ---
class MockProductoRepository(IProductoRepository):
    def __init__(self):
        self._db = {}

    def get_by_id(self, id):
        return self._db.get(id)

    def add(self, producto):
        self._db[producto.id] = producto

# --- 5. Servicio de Negocio (No sabe qué DB usa) ---
class TiendaService:
    def __init__(self, repo: IProductoRepository):
        self.repo = repo
        
    def registrar_producto(self, id, nombre, precio):
        if precio < 0:
            raise ValueError("Precio negativo no permitido")
        p = Producto(id, nombre, precio)
        self.repo.add(p)
        print(f"✅ Producto '{nombre}' registrado.")

# --- Uso ---
def main():
    print("--- Caso 1: Usando SQLite ---")
    conn = sqlite3.connect(":memory:")
    repo_sql = SQLiteProductoRepository(conn)
    servicio = TiendaService(repo_sql)
    servicio.registrar_producto(1, "Laptop SQL", 1500.00)
    
    print("\n--- Caso 2: Usando RAM (Test ultra rápido) ---")
    repo_mock = MockProductoRepository()
    servicio_test = TiendaService(repo_mock)
    servicio_test.registrar_producto(2, "Laptop Mock", 999.99)
    
    print("\nConclusión: El Servicio funciona IGUAL con ambas DBs.")

if __name__ == "__main__":
    main()
