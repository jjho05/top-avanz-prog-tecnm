# 🛠️ Laboratorios Unidad 0: Entorno de Desarrollo

Bienvenido al "Bootcamp" de configuración. Antes de programar sistemas complejos, debes dominar tu herramienta de trabajo.
Estos scripts no son simples "Hola Mundo"; son herramientas profesionales de diagnóstico y automatización.

## 📦 Contenido

| Archivo | Nivel | Descripción | UX Features |
| :--- | :--- | :--- | :--- |
| `01_rich_diagnostics.py` | ⭐⭐ | **Dashboard de Sistema.** Analiza tu CPU, RAM, Python y herramientas instaladas. | Usa librería `rich` para tablas, colores y barras de carga. |
| `02_pip_automation.py` | ⭐ | **DevOps Script.** Instala/Actualiza paquetes automáticamente leyendo `requirements.txt`. | Logs detallados y manejo de errores. |
| `03_type_hints.py` | ⭐⭐ | **Type Checking.** Demostración de tipado estático avanzado y genéricos. | Anotaciones modernas (Python 3.10+). |
| `04_debugging_demo.py` | ⭐⭐ | **Debugging.** Script roto intencionalmente para practicar con el Debugger de VS Code. | Tracebacks simulados. |
| `05_performance.py` | ⭐⭐⭐ | **Profiling.** Mide la velocidad de tu CPU comparando algoritmos. | Uso de `cProfile` y estadísticas. |

---

## 🚀 Cómo Ejecutar

Primero, asegúrate de instalar las dependencias visuales:
```bash
pip install rich
```

### 1. Dashboard de Diagnóstico (Recomendado)
Este es el script más importante. Ejecútalo para asegurar que tu máquina está lista para el curso.

```bash
python 01_rich_diagnostics.py
```

### 2. Automatización de Paquetes
```bash
python 02_pip_automation.py
```

---

## 🧠 Conceptos Clave

*   **TUI (Text User Interface):** Aunque sea una terminal, no tiene por qué ser fea. Usamos librerías como `rich` o `textual` para crear experiencias de usuario (UX) agradables incluso en línea de comandos.
*   **Introspección:** Python puede "mirarse a sí mismo" (`sys`, `platform`) para tomar decisiones en tiempo de ejecución.
*   **Virtual Environments:** Notarás que el script `01` te regaña si no estás en un entorno virtual. Esto es intencional para forzar buenas prácticas.
