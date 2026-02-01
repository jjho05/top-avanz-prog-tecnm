#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_race_visualizer.py
---------------------
Visualizador de Race Conditions (GUI Moderno).

Esta aplicación gráfica demuestra visualmente qué ocurre cuando múltiples hilos
modifican una variable compartida sin sincronización (Locks).

Conceptos:
- Interfaz Gráfica Thread-Safe (comunicación Queue).
- Visualización de "Carreras" (Race Conditions).
- Impacto del GIL y Atomicidad.

Requisitos:
    pip install customtkinter
"""

import threading
import time
import customtkinter as ctk

# --- Configuración Visual ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RaceCar(ctk.CTkFrame):
    """Componente visual que representa un 'Hilo/Auto'."""
    def __init__(self, master, name, color):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text=name, width=50)
        self.label.pack(side="left", padx=5)
        
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(side="left", padx=10, pady=10)
        self.progress.configure(progress_color=color)

    def set_progress(self, val):
        self.progress.set(val)

class RaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Race Condition Visualizer")
        self.geometry("600x400")

        # Estado Compartido (La Memoria "Corruptible")
        self.shared_counter = 0
        self.target_ops = 100
        self.lock = threading.Lock()
        self.use_lock = ctk.BooleanVar(value=False)

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkLabel(self, text="Carrera de Hilos: Sin Sincronización", font=("Arial", 20, "bold"))
        self.header.pack(pady=20)

        # Controles
        controls = ctk.CTkFrame(self)
        controls.pack(pady=10)
        
        self.btn_start = ctk.CTkButton(controls, text="Iniciar Carrera", command=self.start_race)
        self.btn_start.pack(side="left", padx=10)
        
        self.chk_lock = ctk.CTkCheckBox(controls, text="Activar Mutex (Lock)", variable=self.use_lock)
        self.chk_lock.pack(side="left", padx=10)

        # Corredores
        self.racers_frame = ctk.CTkFrame(self)
        self.racers_frame.pack(pady=20)
        
        self.car1 = RaceCar(self.racers_frame, "Hilo A", "cyan")
        self.car1.pack(pady=5)
        self.car2 = RaceCar(self.racers_frame, "Hilo B", "magenta")
        self.car2.pack(pady=5)

        # Resultados
        self.result_lbl = ctk.CTkLabel(self, text="Esperando inicio...", font=("Consolas", 14))
        self.result_lbl.pack(pady=20)

    def start_race(self):
        self.shared_counter = 0
        self.car1.set_progress(0)
        self.car2.set_progress(0)
        self.btn_start.configure(state="disabled")
        self.result_lbl.configure(text="Corriendo...", text_color="white")

        # Lanzar hilos
        t1 = threading.Thread(target=self.run_thread, args=(self.car1, 1))
        t2 = threading.Thread(target=self.run_thread, args=(self.car2, 1))
        
        t1.start()
        t2.start()

        # Monitor (Hilo UI)
        self.monitor_race(t1, t2)

    def run_thread(self, car_ui, increment):
        """Simula trabajo intensivo."""
        for i in range(self.target_ops):
            time.sleep(0.02) # Simular I/O
            
            # SECCIÓN CRITICA
            if self.use_lock.get():
                with self.lock:
                    self.shared_counter += increment
            else:
                # Race Condition simulada (Read-Modify-Write manual)
                temp = self.shared_counter
                time.sleep(0.001) # Forzar context switch
                self.shared_counter = temp + increment
            
            # Actualizar GUI (Debe ser thread-safe en teoría, CTK aguanta un poco, 
            # pero lo correcto sería usar after/queue. Aquí simplificamos para demo).
            progress = (i + 1) / self.target_ops
            car_ui.set_progress(progress)

    def monitor_race(self, t1, t2):
        if t1.is_alive() or t2.is_alive():
            self.after(100, lambda: self.monitor_race(t1, t2))
        else:
            self.finish_race()

    def finish_race(self):
        self.btn_start.configure(state="normal")
        expected = self.target_ops * 2
        actual = self.shared_counter
        
        if actual == expected:
            msg = f"✅ PERFECTO: {actual}/{expected}"
            color = "green"
        else:
            msg = f"❌ ERROR (RACE CONDITION): {actual}/{expected}"
            color = "red"
            
        self.result_lbl.configure(text=msg, text_color=color)

if __name__ == "__main__":
    app = RaceApp()
    app.mainloop()
