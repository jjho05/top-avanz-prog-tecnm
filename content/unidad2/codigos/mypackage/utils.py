"""
Módulo Utils (Herramientas Auxiliares)
"""
import random
import string

def formatear_numero(n):
    return f"{n:,.2f}"

def generar_id(length=8):
    """Genera un ID alfanumérico aleatorio."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
