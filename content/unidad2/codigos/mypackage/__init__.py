"""
mypackage/
----------
Este archivo __init__.py convierte un directorio en un paquete importable.

Conceptos Clave:
1. **Exposición de API:** Al hacer `from mypackage import Calculadora`, el usuario no necesita saber que Calculadora está en `core.py`.
2. **Inicialización:** Código que corre al primer import.
"""

print("📦 Inicializando mypackage...")

# Exponemos clases del módulo interno para facilitar acceso
from .core import Calculadora
from .utils import formatear_numero

# Definimos qué se exporta con 'from mypackage import *'
__all__ = ["Calculadora", "formatear_numero"]

VERSION = "1.0.0"
