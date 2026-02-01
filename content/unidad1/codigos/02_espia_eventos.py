#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_espia_eventos.py
-------------------
Laboratorio de introspección de eventos.
Este script muestra en tiempo real qué eventos están ocurriendo y
qué datos trae consigo el objeto `event` de Tkinter.

Conceptos cubiertos:
1. Binding global con `bind_all`.
2. Extracción de datos del objeto `event` (x, y, char, keysym).
3. Diferencia entre eventos de Mouse y Teclado.

Instrucciones:
    python 02_espia_eventos.py
    
    1. Mueve el mouse sobre la ventana.
    2. Haz clics.
    3. Presiona teclas.
    4. Observa la consola y la etiqueta en pantalla.
"""

import customtkinter as ctk

ctk.set_appearance_mode("Dark")

class EventSpyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Laboratorio 1.2: Espía de Eventos")
        self.geometry("500x400")
        
        # UI Setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        # Área de visualización grande
        self.info_box = ctk.CTkTextbox(self, font=("Consolas", 14), activate_scrollbars=True)
        self.info_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.info_box.insert("0.0", "--- ESPERANDO EVENTOS ---\n")
        
        # Botón de limpieza
        self.btn_clear = ctk.CTkButton(self, text="Limpiar Log", command=self.clear_log)
        self.btn_clear.grid(row=1, column=0, pady=10)
        
        # BINDINGS
        # bind_all escucha en TODA la aplicación, no importa dónde esté el foco.
        
        # 1. Mouse
        self.bind_all("<Button-1>", self.report_mouse)   # Clic Izquierdo
        self.bind_all("<Button-3>", self.report_mouse)   # Clic Derecho
        # self.bind_all("<Motion>", self.report_motion)  # DEMASIADO RUIDOSO (Descomentar con cuidado)
        
        # 2. Teclado
        self.bind_all("<Key>", self.report_key)

    def log(self, message):
        """Agrega texto al cuadro de texto de la UI."""
        self.info_box.insert("end", message + "\n")
        self.info_box.see("end") # Auto-scroll al final

    def clear_log(self):
        self.info_box.delete("0.0", "end")

    def report_mouse(self, event):
        """Manejador para eventos de clic."""
        msg = f"[MOUSE] Tipo: {event.type} | Botón: {event.num} | Pos: ({event.x}, {event.y})"
        self.log(msg)
        print(msg) # También a terminal

    def report_key(self, event):
        """Manejador para eventos de teclado."""
        # Filtramos teclas especiales que no tienen char imprimible
        char_safe = event.char if event.char.isprintable() else repr(event.char)
        msg = f"[KEYQB] KeySym: {event.keysym:<10} | Char: {char_safe:<5} | Codigo: {event.keycode}"
        self.log(msg)
        print(msg)

if __name__ == "__main__":
    print("Iniciando Espía de Eventos...")
    app = EventSpyApp()
    app.mainloop()
