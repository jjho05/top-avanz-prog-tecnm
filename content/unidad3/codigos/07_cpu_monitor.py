#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_cpu_monitor.py
-----------------
Monitor de CPU en Tiempo Real (Hybrid UI).

Integra Matplotlib (Gráfica Científica) dentro de CustomTkinter (GUI Moderna).
Usa hilos para separar la adquisición de datos (Backend) del renderizado (Frontend).

Requisitos:
    pip install customtkinter matplotlib psutil
"""

import customtkinter as ctk
import threading
import time
import psutil
import collections
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración Visual
ctk.set_appearance_mode("Dark")

class CPUMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager Pro - Threading Monitor")
        self.geometry("900x600")

        # Layout 2x1
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Gráfica
        self.grid_rowconfigure(1, weight=0) # Stats

        # --- 1. Área de Gráfica (Matplotlib) ---
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Iniciar Matplotlib
        self.setup_chart()

        # --- 2. Área de Estadísticas ---
        self.stats_frame = ctk.CTkFrame(self, height=100)
        self.stats_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        self.lbl_cpu = ctk.CTkLabel(self.stats_frame, text="CPU: 0%", font=("Arial", 24, "bold"))
        self.lbl_cpu.pack(side="left", padx=40, pady=20)
        
        self.lbl_ram = ctk.CTkLabel(self.stats_frame, text="RAM: 0%", font=("Arial", 24, "bold"), text_color="cyan")
        self.lbl_ram.pack(side="right", padx=40, pady=20)

        # --- Backend (Hilo de Datos) ---
        self.running = True
        self.cpu_data = collections.deque([0]*60, maxlen=60) # Últimos 60 segundos
        self.ram_data = collections.deque([0]*60, maxlen=60)
        
        self.thread = threading.Thread(target=self.data_collector, daemon=True)
        self.thread.start()

        # Timer de Animación UI (Tkinter Loop)
        self.after(100, self.update_ui)

    def setup_chart(self):
        # Crear Figura
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="#2b2b2b")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#2b2b2b")
        
        # Líneas iniciales
        self.line_cpu, = self.ax.plot([], [], color="#1f6aa5", linewidth=2, label="CPU %")
        self.line_ram, = self.ax.plot([], [], color="#2cc985", linewidth=2, label="RAM %")
        
        # Estilos ejes
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 60)
        self.ax.grid(True, color="#444444", linestyle="--")
        self.ax.legend(loc="upper left", facecolor="#2b2b2b", labelcolor="white")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        # Embedding en Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def data_collector(self):
        """Hilo secundario que consulta al SO (Operación bloqueante/lenta)."""
        while self.running:
            cpu = psutil.cpu_percent(interval=1) # Bloquea 1 segundo
            ram = psutil.virtual_memory().percent
            
            # Guardamos datos (Threading safe porque deque es atómica en append/pop)
            self.cpu_data.append(cpu)
            self.ram_data.append(ram)

    def update_ui(self):
        """Loop principal de UI (Main Thread)."""
        if not self.running: return

        # 1. Actualizar Gráfica
        data_len = len(self.cpu_data)
        self.line_cpu.set_data(range(data_len), self.cpu_data)
        self.line_ram.set_data(range(data_len), self.ram_data)
        
        self.canvas.draw() # Redibujar (Costoso, por eso se hace en UI thread)

        # 2. Actualizar Textos
        if self.cpu_data:
            self.lbl_cpu.configure(text=f"CPU: {self.cpu_data[-1]}%")
            self.lbl_ram.configure(text=f"RAM: {self.ram_data[-1]}%")

        # Loop
        self.after(500, self.update_ui)

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = CPUMonitorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
