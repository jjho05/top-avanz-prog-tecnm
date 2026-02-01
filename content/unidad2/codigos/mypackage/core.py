"""
Módulo Core (Lógica de Negocio)
"""

from .utils import generar_id

class Calculadora:
    def __init__(self):
        self.id = generar_id()
        self.history = []

    def sumar(self, a, b):
        res = a + b
        self.history.append(f"{a} + {b} = {res}")
        return res
    
    def __repr__(self):
        return f"<Calculadora ID={self.id} Ops={len(self.history)}>"
