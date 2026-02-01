#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_producer_consumer_gui.py
---------------------------
Visualizador del Patrón Productor-Consumidor.
Animación gráfica de colas sincronizadas (Queue) usando Flet.

Muestra cómo los items viajan de un hilo a otro a través de un buffer limitado.
Si el buffer se llena, el Productor se bloquea (rojo).
Si se vacía, el Consumidor se bloquea (rojo).

Requisitos:
    pip install flet
"""

import flet as ft
import threading
import time
import random
import queue

# Configuración
QUEUE_SIZE = 5
data_queue = queue.Queue(maxsize=QUEUE_SIZE)

def main(page: ft.Page):
    page.title = "Producer-Consumer Pipeline"
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.padding = 30
    
    # --- Estado Visual ---
    buffer_view = ft.Row(spacing=10, alignment="center")
    
    status_prod = ft.Container(content=ft.Text("Productor"), width=150, height=50, bgcolor="green", border_radius=10, alignment=ft.alignment.center)
    status_cons = ft.Container(content=ft.Text("Consumidor"), width=150, height=50, bgcolor="green", border_radius=10, alignment=ft.alignment.center)
    
    log_view = ft.ListView(expand=True, auto_scroll=True)

    def update_buffer_visual():
        # Reconstruir la vista del buffer basada en la Queue real
        # Nota: Acceder a queue.queue no es thread-safe puro, pero para visualización aprox está bien.
        items = list(data_queue.queue)
        controls = []
        for item in items:
            controls.append(
                ft.Container(
                    content=ft.Text(f"#{item}", color="black"),
                    width=60, height=60,
                    bgcolor="cyan",
                    border_radius=30,
                    alignment=ft.alignment.center,
                    animate=ft.animation.Animation(300, "bounceOut")
                )
            )
        # Rellenar espacios vacíos
        for _ in range(QUEUE_SIZE - len(items)):
             controls.append(
                ft.Container(width=60, height=60, border=ft.border.all(2, "grey"), border_radius=30)
            )
        buffer_view.controls = controls
        page.update()

    def log(msg, color="white"):
        log_view.controls.append(ft.Text(msg, color=color, font_family="Consolas"))
        page.update()

    # --- Hilos Lógicos ---
    def producer():
        counter = 1
        while True:
            time.sleep(random.uniform(0.5, 2.0))
            is_full = data_queue.full()
            
            if is_full:
                status_prod.bgcolor = "red"
                status_prod.content.value = "Bloqueado (Lleno)"
                page.update()
                
            # Put bloqueante
            data_queue.put(counter)
            
            # Desbloqueado
            status_prod.bgcolor = "green"
            status_prod.content.value = "Produciendo..."
            log(f"🏭 Producido Item #{counter}")
            counter += 1
            update_buffer_visual()

    def consumer():
        while True:
            time.sleep(random.uniform(1.0, 3.0)) # Consumidor es más lento a veces
            is_empty = data_queue.empty()
            
            if is_empty:
                status_cons.bgcolor = "red"
                status_cons.content.value = "Bloqueado (Vacío)"
                page.update()

            # Get bloqueante
            item = data_queue.get()
            
            # Desbloqueado
            status_cons.bgcolor = "orange" # Procesando
            status_cons.content.value = "Consumiendo..."
            update_buffer_visual()
            
            time.sleep(0.5) # Simular proceso
            log(f"✅ Consumido Item #{item}", "green")
            status_cons.bgcolor = "green"
            status_cons.content.value = "Esperando..."
            page.update()

    # --- Layout ---
    page.add(
        ft.Text("Visualización de Concurrencia", size=30, weight="bold"),
        ft.Divider(),
        ft.Row([status_prod, ft.Text("-->"), status_cons], alignment="center"),
        ft.Divider(),
        ft.Text("Buffer (Queue)", size=20),
        ft.Container(content=buffer_view, padding=20, bgcolor="black", border_radius=15),
        ft.Divider(),
        ft.Text("Log de Eventos:", size=15),
        ft.Container(content=log_view, height=200, bgcolor="black", border_radius=10, padding=10)
    )

    # Iniciar Hilos Daemon
    threading.Thread(target=producer, daemon=True).start()
    threading.Thread(target=consumer, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)
