# 🖼️ Laboratorios Unidad 1: GUI Moderna con Python

Olvída la terminal gris. Aquí construimos software que la gente quiera usar.
Usamos **CustomTkinter** para crear interfaces con bordes redondeados, modo oscuro y animaciones, sin la complejidad de HTML/CSS.

## 📦 Contenido

| Archivo | Nivel | Descripción | UX Pattern |
| :--- | :--- | :--- | :--- |
| `01_hola_mundo_ctk.py` | ⭐ | **Hello World.** Tu primera ventana moderna. | Theme System (Light/Dark). |
| `02_espia_eventos.py` | ⭐⭐ | **Event Listener.** Diagnostica qué ve el SO cuando mueves el mouse. | Binding de eventos en tiempo real. |
| `03_piano_virtual.py` | ⭐⭐ | **Interactivo.** Un piano funcional mapeado al teclado. | Feedback visual y sonoro inmediato. |
| `04_crud_empleados.py` | ⭐⭐⭐ | **Maestro-Detalle App.** Una aplicación gestión completa con Sidebar. | Grid Layout, Tablas (ScrollableFrame), Formularios. |
| `05_login_seguro.py` | ⭐⭐ | **Seguridad UI.** Pantalla de login con hashing real. | Manejo de Estado (Login -> Dashboard). |
| `06_async_loader.py` | ⭐⭐⭐ | **Non-Blocking UI.** Cómo cargar datos sin congelar la ventana. | Threading + ProgressBar. |
| `07_ejercicio_maestro.py` | ⭐⭐⭐⭐ | **ERP Layout.** Sistema Maestro-Detalle complejo (Referenciado en 1.1). | Grid avanzado, Sidebar, Theme Switching. |
| `08_widget_gallery.py` | ⭐⭐⭐ | **Showcase.** Galería de todos los widgets disponibles. | Sliders, Switches, Tabs, Dialogs. |

---

## 🚀 Cómo Ejecutar

Necesitas instalar las librerías modernas:
```bash
pip install customtkinter packaging pillow
```

### 1. La Joya de la Corona (CRUD)
Ejecuta la aplicación completa para ver el potencial de Python en escritorio.
```bash
python 04_crud_empleados.py
```

### 2. Piano Virtual
```bash
python 03_piano_virtual.py
```
*(Presiona las teclas `a`, `s`, `d`, `f`...)*

---

## 🧠 Conceptos Clave

*   **Event Loop:** Entender que la GUI es un bucle infinito (`mainloop`) que nunca duerme.
*   **Grid System:** El arte de alinear cajas dentro de cajas.
*   **Callback Hell:** Cómo evitar que tu código se vuelva un espagueti de funciones anidadas.
