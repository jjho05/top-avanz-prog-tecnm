#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_web_scraper_concurrente.py
-----------------------------
Aplicación Real: Web Scraping Masivo.
Aquí es donde los Hilos (Threading) brillan: I/O Bound.

Escenario:
    Descargar el título de 10 páginas web.
    - Serial: 10s (aprox 1s por página).
    - ThreadPool: 1s (todas a la vez).

Nota: Usamos `urllib` estándar para no depender de `requests`, 
pero en producción usaríamos `aiohttp` o `requests`.
"""

import threading
import time
import urllib.request
import re
from concurrent.futures import ThreadPoolExecutor

SITIOS = [
    "https://www.python.org",
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.bing.com",
    "https://www.yahoo.com",
    "https://www.duckduckgo.com",
    "https://www.reddit.com",
    "https://www.amazon.com"
]

def obtener_titulo(url):
    """Descarga HTML y extrae <title>."""
    try:
        start = time.time()
        with urllib.request.urlopen(url, timeout=5) as conn:
            html = conn.read().decode('utf-8', errors='ignore')
            
        titulo = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        texto = titulo.group(1).strip() if titulo else "Sin título"
        
        duration = time.time() - start
        return f"[{duration:.2f}s] {url} -> {texto[:30]}..."
    except Exception as e:
        return f"[ERROR] {url}: {e}"

def modo_serial():
    print("\n--- MODO SERIAL (Lento) ---")
    start = time.time()
    for url in SITIOS:
        res = obtener_titulo(url)
        print(res)
    print(f"Tiempo Serial: {time.time() - start:.2f}s")

def modo_concurrente():
    print("\n--- MODO THREAD POOL (Rápido) ---")
    start = time.time()
    
    # ThreadPoolExecutor maneja los hilos por nosotros
    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = executor.map(obtener_titulo, SITIOS)
        
    for res in resultados:
        print(res)
        
    print(f"Tiempo Concurrente: {time.time() - start:.2f}s")

def main():
    print("Nota: Si no tienes internet, esto fallará con timeout.")
    
    try:
        # Probamos uno solo primero
        obtener_titulo("https://www.example.com") 
    except:
        print("❌ No hay conexión a internet. Saltando demo.")
        return

    modo_serial()
    modo_concurrente()

if __name__ == "__main__":
    main()
