#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_sqlalchemy_models.py
-----------------------
Introducción al ORM (Object Relational Mapping) moderno.
SQLAlchemy 2.0 Style (Declarative Base).

Ventajas:
1. No escribes SQL a mano.
2. Tu código funciona en SQLite, Postgres y MySQL sin cambios.
3. Validación de tipos en Python.

Requisitos: pip install sqlalchemy
"""

from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

# --- 1. Definición del Modelo (Clases) ---
class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relación 1 a N (Un usuario tiene muchas direcciones)
    direcciones: Mapped[List["Direccion"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.nombre}>"

class Direccion(Base):
    __tablename__ = "direcciones"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    calle: Mapped[str] = mapped_column(String)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    
    usuario: Mapped["Usuario"] = relationship(back_populates="direcciones")

    def __repr__(self):
        return f"<Dir {self.calle}>"

# --- 2. Operaciones ---
def main():
    # Crear engine en memoria (volátil)
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    # Crear tablas (DDL)
    print("🛠 Creando tablas...")
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        # INSERT
        print("\n📝 Insertando datos...")
        u1 = Usuario(nombre="Juan Perez", email="juan@example.com")
        u1.direcciones.append(Direccion(calle="Av. Tecnológico #100"))
        u1.direcciones.append(Direccion(calle="Calle Falsa 123"))
        
        session.add(u1)
        session.commit()
        
        # SELECT (Query)
        print("\n🔍 Consultando...")
        stmt = select(Usuario).where(Usuario.nombre == "Juan Perez")
        user = session.scalars(stmt).one()
        
        print(f"Usuario encontrado: {user.nombre}")
        print(f"Direcciones: {user.direcciones}")
        
        # UPDATE
        print("\n✏️ Actualizando...")
        user.nombre = "Juan P. Detallista"
        session.commit()
        
        # DELETE (Cascada)
        print("\n🗑 Eliminando usuario...")
        session.delete(user)
        session.commit()
        
        # Verificar cascada (Direcciones deben morir)
        count = session.scalar(select(Direccion).count())
        print(f"Direcciones restantes: {count} (Esperado: 0)")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Falta instalar sqlalchemy. Ejecuta: pip install sqlalchemy")
