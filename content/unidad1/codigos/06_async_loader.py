#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_async_loader.py
------------------
Prevención de GUI Freezing (Congelamiento).
Este es el concepto más importante para UX.

Conceptos:
1. `threading`: Ejecutar tareas pesadas en segundo plano.
2. `after()`: Comunicación Thread-Safe para actualizar la UI desde el Mainloop.
3. Indicadores de Carga (Spinners/ProgressBar).

Simulamos una descarga de archivo de 5 segundos.
- Versión SIN hilos: Congela la ventana (Windows pone "No Responde").
- Versión CON hilos: La barra se mueve suavemente.
"""

import customtkinter as ctk
import threading
import time
import random

class AsyncTaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Patrón UI Asíncrono")
        self.geometry("400x300")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.lbl_status = ctk.CTkLabel(self, text="Listo", font=("Arial", 16))
        self.lbl_status.grid(row=0, column=0, pady=20)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.grid(row=1, column=0, padx=40, sticky="ew")

        # Botón Bloqueante (MALA PRÁCTICA)
        self.btn_freeze = ctk.CTkButton(self, text="Descarga Bloqueante (Bad)", fg_color="red", command=self.tarea_bloqueante)
        self.btn_freeze.grid(row=2, column=0, pady=10)

        # Botón Asíncrono (BUENA PRÁCTICA)
        self.btn_async = ctk.CTkButton(self, text="Descarga Asíncrona (Good)", fg_color="green", command=self.iniciar_thread)
        self.btn_async.grid(row=3, column=0, pady=10)

    def tarea_bloqueante(self):
        """Simula lo que NO se debe hacer."""
        self.lbl_status.configure(text="Congelado... intenta mover la ventana")
        self.update() # Forzar pintado antes de morir
        time.sleep(5) # Simula descarga
        self.lbl_status.configure(text="Terminado (Pero sufriste)")
        
    def iniciar_thread(self):
        """Lanza el hilo de trabajo."""
        self.btn_async.configure(state="disabled")
        self.lbl_status.configure(text="Descargando en background...")
        self.progress.set(0)
        
        # Creamos y lanzamos el hilo daemon (muere si cierras la app)
        t = threading.Thread(target=self.tarea_pesada_background)
        t.start()

    def tarea_pesada_background(self):
        """Código que corre en otro núcleo/hilo."""
        total_steps = 100
        for i in range(total_steps):
            time.sleep(0.05) # Simula trabajo (I/O, Red, CPU)
            
            # CRÍTICO: No llamar self.progress.set() aquí directamente si fuera Tkinter puro.
            # CTK es thread-safe para métodos simples, pero es buena práctica usar after.
            # Aquí lo simulamos enviando el progreso.
            progreso_actual = (i + 1) / total_steps
            
            # Agendamos la actualización visual en el Mainloop
            self.after(0, self.actualizar_ui, progreso_actual)

        self.after(0, self.finalizar_carga)

    def actualizar_ui(self, valor):
        self.progress.set(valor)

    def finalizar_carga(self):
        self.lbl_status.configure(text="¡Descarga Completa!")
        self.btn_async.configure(state="normal")
        messagebox_safe_info("Éxito", "Tarea terminada")

def messagebox_safe_info(titulo, mensaje):
    # Tkinter messagebox debe invocarse en main thread.
    # Como finalizar_carga fue llamado con self.after, estamos seguros.
    from tkinter import messagebox
    messagebox.showinfo(titulo, mensaje)

if __name__ == "__main__":
    app = AsyncTaskApp()
    app.mainloop()
