# 📱 Laboratorios Unidad 5: Programación Móvil (Flet)

El desarrollo móvil nativo es difícil. Flet lo hace fácil.
Convertimos aplicaciones Python en Apps Android/iOS/Web sin tocar Java ni Swift.

## 📦 Contenido

| Archivo | Nivel | Descripción | Características UI/UX |
| :--- | :--- | :--- | :--- |
| `01_flet_counter.py` | ⭐ | **Reactive State.** Entendiendo cómo se actualiza la UI automáticamente. | Botones flotantes (FAB). |
| `02_flet_responsive.py` | ⭐⭐ | **Diseño Adaptable.** Grid que cambia de columnas según el tamaño de pantalla. | Breakpoints (Mobile vs Desktop). |
| `03_shop_app.py` | ⭐⭐⭐ | **SPA Navigation.** App Multi-página con sistema de rutas robusto. | App Bar, Floating Action Button, Drawer. |
| `04_camera_access.py` | ⭐⭐ | **Hardware Bridge.** Acceso a cámara/galería usando FilePicker nativo. | Diálogos de sistema. |
| `05_api_client.py` | ⭐⭐⭐ | **Rest Client.** Consumo de API JSON Placeholder y renderizado de tarjetas. | Listado asíncrono con imágenes. |

---

## 🚀 Cómo Ejecutar

Requiere Flet:
```bash
pip install flet
```

### 1. Tienda Virtual (Shop App)
Navega entre catálogo, carrito y perfil.
```bash
python 03_shop_app.py
```

### 2. Constructor APK (Teórico)
Para convertir `01_flet_counter.py` a Android:
```bash
flet build apk 01_flet_counter.py
# (Requiere instalar Flutter SDK previamente)
```

---

## 🧠 Conceptos Clave

*   **PWA (Progressive Web App):** Tu app es una web, pero se instala como app.
*   **Reactive UI:** No modificas el botón. Modificas la variable `contador` y el botón se repinta solo.
*   **Cross-Platform:** El mismo código `main.py` corre en web, Windows y Android.
