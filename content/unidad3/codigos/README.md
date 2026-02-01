# 🧵 Laboratorios Unidad 3: Programación Concurrente

Paralelismo real vs la ilusión de la concurrencia.
Aquí verás cómo Python maneja múltiples tareas y los peligros de compartir memoria.

## 📦 Contenido

| Archivo | Nivel | Descripción | Características UI/UX |
| :--- | :--- | :--- | :--- |
| `06_race_visualizer.py` | ⭐⭐⭐ | **Race Simulator.** GUI Interactiva que demuestra visualmente la corrupción de datos. | **CustomTkinter App.** Animaciones y controles en tiempo real. |
| `07_cpu_monitor.py` | ⭐⭐⭐⭐ | **Realtime Monitor.** Gráficas de CPU/RAM en vivo. | **Hybrid UI.** Matplotlib embebido en CustomTkinter + Threading. |
| `08_producer_consumer_gui.py` | ⭐⭐⭐ | **Pipeline Visual.** Animación de items moviéndose entre hilos. | **Flet.** Visualización de Queue Buffer. |
| `01_hilos_vs_procesos.py` | ⭐⭐ | **Benchmark.** Compara velocidad de Hilos (ligero) vs Procesos (pesado). | Métricas de CPU. |
| `02_race_condition.py` | ⭐⭐ | **El Error.** Demo de script bancario perdiendo dinero por falta de Locks. | |
| `03_productor_consumidor.py` | ⭐⭐⭐ | **Pipeline.** Patrón de diseño clave para sistemas distribuidos. | Logs de colores. |
| `04_asyncio_intro.py` | ⭐⭐⭐ | **Async/Await.** El futuro de Python (usado en FastAPI). | |
| `05_web_scraper_concurrente.py` | ⭐⭐⭐⭐ | **Caso Real.** Descarga 50 sitios web en 2 segundos. | ThreadPoolExecutor. |

---

## 🚀 Cómo Ejecutar

Requiere CustomTkinter:
```bash
pip install customtkinter
```

### 1. El Simulador Gráfico (Race Visualizer)
Abre la app y corre la carrera **sin** activar el "Lock". Verás fallar el contador.
Luego actívalo y ve cómo se arregla (pero va más lento).

```bash
python 06_race_visualizer.py
```

### 2. Web Scraper Veloz
Mira cómo tu terminal vuela.
```bash
python 05_web_scraper_concurrente.py
```

---

## 🧠 Conceptos Clave

*   **GIL (Global Interpreter Lock):** El candado que impide que Python use 100% de todos tus CPUs a la vez.
*   **Race Condition:** Cuando dos hilos tocan la misma variable y se sobrescriben mutuamente.
*   **Deadlock:** Cuando dos hilos se esperan mutuamente para siempre (el abrazo de la muerte).
