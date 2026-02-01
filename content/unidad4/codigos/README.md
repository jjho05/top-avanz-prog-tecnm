# 🗄️ Laboratorios Unidad 4: Acceso a Datos (ORM & SQL)

Olvída los Strings SQL concatenados. Aquí aprendes a hablar con la Base de Datos como un profesional.
Usamos **SQLAlchemy 2.0** (El estándar moderno) y **Pydantic** para validación.

## 📦 Contenido

| Archivo | Nivel | Descripción | Características UI/UX |
| :--- | :--- | :--- | :--- |
| `06_lite_admin.py` | ⭐⭐⭐ | **Mini DBeaver.** Herramienta visual (Flet) para inspeccionar cualquier archivo `.db`. | **GUI Completa.** DataGrid dinámico y navegación de tablas. |
| `07_analisis_ventas.py` | ⭐⭐⭐⭐ | **BI Dashboard.** Reporte ejecutivo con gráficas científicas. | **Pandas + Matplotlib.** Integración Data Science en GUI. |
| `08_crud_sql_ui.py` | ⭐⭐⭐ | **Sistema ABCC.** Gestión completa de empleados (Altas, Bajas, Cambios). | **Formularios.** Ventanas modales y validación. |
| `01_sqlite_raw.py` | ⭐ | **SQL Puro.** Cómo usar la librería estándar de forma segura (parameterized queries). | Anti-SQL Injection demo. |
| `02_sqlalchemy_models.py` | ⭐⭐⭐ | **ORM Moderno.** Mapeo Objeto-Relacional Declarativo. | Tipado estático. |
| `03_migrations.py` | ⭐⭐⭐⭐ | **Evolución.** Cómo cambiar la BD sin borrar los datos (Alembic style). | Logs estructurados. |
| `04_repository_pattern.py` | ⭐⭐⭐ | **Arquitectura.** Separación de capas (Service -> Repository -> DB). | Clean Code. |
| `05_seed_faker.py` | ⭐⭐ | **Data Gen.** Crea 1,000 usuarios falsos en segundos para testear. | Barra de progreso. |

---

## 🚀 Cómo Ejecutar

Requiere SqlAlchemy y Flet:
```bash
pip install sqlalchemy flet faker
```

### 1. Generar Datos (Seed)
Primero, crea una base de datos con datos de prueba.
```bash
python 05_seed_faker.py
# Esto creará 'database.db' lleno de usuarios.
```

### 2. Explorador Gráfico (LiteAdmin)
Abre la herramienta visual y conecta a `database.db`.
```bash
python 06_lite_admin.py
```

---

## 🧠 Conceptos Clave

*   **ACID:** Las 4 reglas que garantizan que el dinero no desaparezca.
*   **ORM (Object Relational Mapping):** Convertir filas de tablas a Objetos Python y viceversa.
*   **N+1 Problem:** El error de rendimiento más común al usar ORMs (hacer 1000 queries en lugar de 1).
