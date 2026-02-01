# Guía de Instalación Teórica

## Requisitos del Sistema

- **S.O.:** Windows 10/11, macOS, o Linux.
- **Python:** Versión 3.10 o superior (Recomendado 3.12).
- **Editor:** VS Code (Recomendado) o PyCharm.

## Instalación de Dependencias

Ejecuta el siguiente comando en la terminal para instalar todas las librerías necesarias para el curso:

```bash
pip install -r requirements.txt
```

Esto instalará:
- `customtkinter` (GUI)
- `sqlalchemy` (Datos)
- `pandas` y `matplotlib` (Visualización)
- `flet` (Móvil)

## Verificación

Para verificar que todo está correcto, ejecuta:

```bash
python -c "import customtkinter; print('Instalación Correcta')"
```
