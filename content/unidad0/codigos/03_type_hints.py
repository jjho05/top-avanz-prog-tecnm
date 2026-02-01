#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_type_hints.py
----------------
Python Moderno: Tipado Estático y Dataclasses.
Python es dinámico, pero el código profesional usa Type Hints para
prevenir errores antes de ejecutar (usando herramientas como `mypy`).

Conceptos:
1. Sintaxis de tipos: `name: str`, `age: int`.
2. Tipos complejos: `List`, `Dict`, `Optional`, `Union` (o `|` en 3.10+).
3. `dataclasses`: Clases de datos sin boilerplate.

Uso:
    python 03_type_hints.py
    (Idealmente revisar con: mypy 03_type_hints.py)
"""

from dataclasses import dataclass
from typing import List, Optional

# --- 1. DATACLASSES ---
# Reduce el código de __init__, __repr__, __eq__ automáticamente.

@dataclass
class Estudiante:
    nombre: str
    matricula: str
    promedio: float
    activo: bool = True
    semestre: int = 1

    def es_honorifico(self) -> bool:
        """Retorna True si el promedio es de excelencia."""
        return self.promedio >= 95.0

# --- 2. FUNCIONES CON TYPE HINTS ---

def calcular_promedio_curso(estudiantes: List[Estudiante]) -> Optional[float]:
    """
    Calcula el promedio general del grupo.
    Retorna None si la lista está vacía.
    """
    if not estudiantes:
        return None
    
    suma = sum(e.promedio for e in estudiantes)
    return round(suma / len(estudiantes), 2)

def buscar_por_matricula(estudiantes: List[Estudiante], target: str) -> Estudiante | None:
    """Busca un estudiante. Retorna el objeto o None (Sintaxis Python 3.10+)."""
    for e in estudiantes:
        if e.matricula == target:
            return e
    return None

def main() -> None:
    # Creación de objetos limpia
    grupo = [
        Estudiante("Ana", "2023001", 98.5),
        Estudiante("Beto", "2023002", 82.0, semestre=3),
        Estudiante("Carla", "2023003", 70.5, activo=False)
    ]
    
    # Intento de error de tipo (Descomentar para ver que el editor se queja)
    # grupo.append(Estudiante("Error", 12345, "Noventa")) 

    promedio_gral = calcular_promedio_curso(grupo)
    print(f"Promedio del Grupo: {promedio_gral}")
    
    # Uso de método tipado
    mejor = grupo[0]
    if mejor.es_honorifico():
        print(f"¡{mejor.nombre} es estudiante de honor!")

    # Búsqueda
    buscado = buscar_por_matricula(grupo, "2023002")
    if buscado:
        print(f"Encontrado: {buscado}")
    else:
        print("No existe.")

if __name__ == "__main__":
    main()
