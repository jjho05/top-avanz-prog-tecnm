#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_piano_virtual.py
-------------------
Laboratorio 1.3: Binding Avanzado y Latencia Cero.
Simula un piano octava simple (Do-Do) que se puede tocar con el teclado
o con el mouse.

Conceptos:
1. Binding múltiple (Teclado + Mouse).
2. Manejo de estados visuales (Press/Release).
3. Uso de Lambdas para pasar argumentos en bindings.
4. Generación de sonido (Beep simple cross-platform).

Instalación:
    pip install customtkinter
    (Windows viene con winsound nativo.
     Mac/Linux requiere configuración extra para beeps, aquí simularemos visualmente)
"""

import customtkinter as ctk
import time
import sys

# Intento de importar sonido nativo
try:
    import winsound
    def play_note(freq):
        # Frecuencia en Hz, Duración en ms
        # winsound bloquea el hilo, así que usamos un flag asíncrono básico 
        # o aceptamos el micro-bloqueo para este demo simple.
        winsound.Beep(freq, 150) 
except ImportError:
    def play_note(freq):
        print(f"♪ Notal: {freq}Hz (Sonido no disponible en este OS sin librerias externas)")

class PianoKey(ctk.CTkButton):
    """Componente personalizado que representa una tecla de piano."""
    def __init__(self, master, note, freq, key_char, color="white"):
        super().__init__(master)
        
        self.note = note
        self.freq = freq
        self.key_char = key_char
        self.orig_color = color
        self.active_color = "#3B8ED0" if color == "white" else "#14375e"

        self.configure(
            text=f"{note}\n({key_char.upper()})",
            width=60 if color == "white" else 40,
            height=200 if color == "white" else 120,
            fg_color=self.orig_color,
            text_color="black" if color == "white" else "white",
            hover_color="#add8e6",
            border_width=1,
            border_color="black",
            corner_radius=4,
            command=self.play # Click mouse
        )
        
    def play(self):
        """Dispara el sonido y la animación."""
        print(f"Tocando: {self.note}")
        play_note(self.freq)

    def press(self):
        """Estado visual presionado."""
        self.configure(fg_color=self.active_color)
        self.play()

    def release(self):
        """Restaurar estado visual."""
        self.configure(fg_color=self.orig_color)

class PianoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Laboratorio 1.3: Piano Virtual Binding")
        self.geometry("600x300")
        self.resizable(False, False)
        
        # Datos de las notas (Frecuencias de 4ta octava)
        # Teclas Blancas
        self.keys_data = [
            ("Do", 261, "a"),
            ("Re", 293, "s"),
            ("Mi", 329, "d"),
            ("Fa", 349, "f"),
            ("Sol", 392, "g"),
            ("La", 440, "h"),
            ("Si", 493, "j"),
            ("Do+", 523, "k"),
        ]
        
        # Diccionario para mapeo rápido Tecla -> Widget
        self.key_map = {}
        
        self._init_ui()
        self._bind_keyboard()
        
        # Instrucciones
        lbl = ctk.CTkLabel(self, text="Usa el teclado (A-S-D-F...) o el Mouse para tocar.")
        lbl.pack(pady=10)

    def _init_ui(self):
        container = ctk.CTkFrame(self)
        container.pack(pady=20, padx=20)
        
        for note, freq, char in self.keys_data:
            key_widget = PianoKey(container, note, freq, char)
            key_widget.pack(side="left", padx=2)
            self.key_map[char] = key_widget

    def _bind_keyboard(self):
        """
        Aquí es donde ocurre la magia del Binding.
        Mapeamos eventos físicos (<Key>) a lógica de aplicación.
        """
        # Bind global para capturar teclas sin importar el foco
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<KeyRelease>", self._on_key_release)

    def _on_key_press(self, event):
        char = event.char.lower()
        if char in self.key_map:
            # Evitar repetición automática del SO (para que no parpadee)
            # En un piano real, mantener presionado no redispara el martillo.
            # (Simplificado para este demo)
            self.key_map[char].press()

    def _on_key_release(self, event):
        char = event.char.lower()
        if char in self.key_map:
            self.key_map[char].release()

if __name__ == "__main__":
    app = PianoApp()
    app.mainloop()
