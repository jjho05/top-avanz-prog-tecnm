#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_analisis_ventas.py
---------------------
Dashboard Ejecutivo de Ventas (Data Science UI).

Combina la potencia de SQL (SQLite) con el análisis de datos (Pandas)
y la visualización científica (Matplotlib), todo dentro de una GUI moderna.

Flujo:
1. Genera datos aleatorios de ventas en SQLite (si no existen).
2. Lee los datos a un DataFrame de Pandas.
3. Renderiza gráficas de Barras y Pastel.

Requisitos:
    pip install customtkinter pandas matplotlib sqlalchemy faker
"""

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np

# Configuración Visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Generación de Datos Fake (Para Demo) ---
def seed_data(engine):
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, producto TEXT, cantidad INTEGER, monto REAL, categoria TEXT)"))
        # Verificar si hay datos
        res = conn.execute(text("SELECT count(*) FROM ventas")).scalar()
        if res < 10:
            print("Generando datos de muestra...")
            data = []
            productos = ["Laptop", "Mouse", "Monitor", "Teclado", "Headset"]
            categorias = ["Electrónica", "Accesorios", "Audio"]
            for _ in range(100):
                p = np.random.choice(productos)
                c = "Electrónica" if p in ["Laptop", "Monitor"] else ("Audio" if p=="Headset" else "Accesorios")
                data.append({
                    "producto": p,
                    "cantidad": np.random.randint(1, 10),
                    "monto": np.random.uniform(50, 2000),
                    "categoria": c
                })
            pd.DataFrame(data).to_sql("ventas", engine, if_exists="append", index=False)

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sales Intelligence Dashboard")
        self.geometry("1100x700")

        # Database connection
        self.engine = create_engine("sqlite:///ventas_demo.db")
        seed_data(self.engine) # Asegurar datos

        # Layout Main
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="Business\nIntelligence", font=("Arial", 20, "bold")).pack(pady=30)
        ctk.CTkButton(self.sidebar, text="Actualizar Datos", command=self.refresh_data).pack(pady=10, padx=20)
        
        # Content Area
        self.content = ctk.CTkScrollableFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Charts Containers
        self.kpi_frame = ctk.CTkFrame(self.content, height=100)
        self.kpi_frame.pack(fill="x", pady=(0, 20))
        
        self.charts_row = ctk.CTkFrame(self.content, fg_color="transparent")
        self.charts_row.pack(fill="both", expand=True)

        # Cargar Dashboard
        self.refresh_data()

    def refresh_data(self):
        # 1. Pipeline de Datos (ETL)
        df = pd.read_sql("SELECT * FROM ventas", self.engine)
        
        # 2. Calcular KPIs
        total_ventas = df['monto'].sum()
        total_ordenes = len(df)
        top_prod = df.groupby('producto')['cantidad'].sum().idxmax()
        
        # 3. Renderizar KPIs
        for widget in self.kpi_frame.winfo_children(): widget.destroy()
        
        self.create_kpi_card(self.kpi_frame, "Ingresos Totales", f"${total_ventas:,.2f}", "green")
        self.create_kpi_card(self.kpi_frame, "Ordenes", f"{total_ordenes}", "blue")
        self.create_kpi_card(self.kpi_frame, "Top Producto", top_prod, "orange")

        # 4. Renderizar Gráficos
        for widget in self.charts_row.winfo_children(): widget.destroy()
        
        # Gráfico 1: Ventas por Categoría (Pastel)
        fig1 = Figure(figsize=(5, 4), dpi=100, facecolor="#333333")
        ax1 = fig1.add_subplot(111)
        cat_sales = df.groupby('categoria')['monto'].sum()
        ax1.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
        ax1.set_title("Ventas por Categoría", color="white")
        self.embed_chart(fig1, self.charts_row)

        # Gráfico 2: Top Productos (Barras)
        fig2 = Figure(figsize=(5, 4), dpi=100, facecolor="#333333")
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor("#333333")
        prod_sales = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False).head(5)
        prod_sales.plot(kind='bar', ax=ax2, color="#00dac6")
        ax2.set_title("Top 5 Productos (Unidades)", color="white")
        ax2.tick_params(colors='white')
        self.embed_chart(fig2, self.charts_row)

    def create_kpi_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, border_width=2, border_color=color)
        card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        ctk.CTkLabel(card, text=title, font=("Arial", 12)).pack(pady=(10, 0))
        ctk.CTkLabel(card, text=value, font=("Arial", 22, "bold"), text_color=color).pack(pady=(5, 10))

    def embed_chart(self, fig, parent):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(side="left", fill="both", expand=True, padx=10)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
