# 🧩 Laboratorios Unidad 2: Componentes y Librerías

Domina la arquitectura de software en Python.
Estos laboratorios demuestran cómo pasar de "scripts sueltos" a "sistemas modulares" y cómo funcionan las entrañas del lenguaje.

## 📦 Contenido

| Archivo | Nivel | Descripción | Características UI/UX |
| :--- | :--- | :--- | :--- |
| `06_package_explorer.py` | ⭐⭐⭐ | **Visualizador de Paquetes.** App gráfica (Flet) que muestra la estructura de árbol de este directorio. | **GUI Completa.** TreeView interactivo y visor de sintaxis markdown. |
| `07_plugin_manager_ui.py` | ⭐⭐⭐ | **Plugin Store.** Interfaz gráfica para cargar módulos dinámicamente. | **CustomTkinter.** Simula VS Code Extensions. |
| `01_introspeccion_profunda.py` | ⭐⭐ | **Metaprogramación.** Script que inspecciona objetos en vivo. | Output formateado con `rich`. |
| `02_plugin_loader.py` | ⭐⭐⭐ | **Sistema de Plugins.** Carga dinámica de módulos externos sin reiniciar. | Arquitectura extensible. |
| `03_decoradores_avanzados.py` | ⭐⭐ | **Decorators.** Modificación de comportamiento de funciones en runtime. | |
| `04_slots_vs_dict.py` | ⭐⭐ | **Benchmark.** Comparativa de uso de memoria RAM. | Métricas precisas. |
| `05_context_managers.py` | ⭐ | **Protocolo With.** Gestión segura de recursos. | |
| `mypackage/` | 📦 | **Paquete Demo.** Estructura canónica de una librería. | `__init__.py` configurado. |

---

## 🚀 Cómo Ejecutar

Requiere Flet:
```bash
pip install flet rich
```

### 1. Explorador Gráfico
¡Mira tu código con estilo moderno!
```bash
python 06_package_explorer.py
```

### 2. Sistema de Plugins
```bash
python 02_plugin_loader.py
```

---

## 🧠 Conceptos Clave

*   **Introspección:** La capacidad del código de examinarse a sí mismo (`inspect`, `dir`, `type`).
*   **Modularidad:** Dividir un problema gigante en piezas pequeñas (`packages`).
*   **Metaprogramación:** Código que escribe o modifica otro código (Decoradores, Metaclases).
