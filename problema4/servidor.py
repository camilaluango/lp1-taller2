#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Servidor
Objetivo: Implementar un servidor web simple que responda peticiones HTTP GET
y sirva archivos estáticos comprendiendo headers HTTP
"""

import http.server
import socketserver

# Definir la dirección y puerto del servidor HTTP
HOST = 'localhost'
PORT = 8080

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Manejador personalizado de peticiones HTTP.
    Hereda de SimpleHTTPRequestHandler que proporciona funcionalidad básica
    para servir archivos estáticos y manejar peticiones HTTP.
    """
    pass  # Usamos el comportamiento por defecto

# Crear una instancia de servidor HTTP
with socketserver.TCPServer((HOST, PORT), MyRequestHandler) as httpd:
    print(f"Servidor HTTP activo en http://{HOST}:{PORT}")
    
    # Iniciar el servidor y ponerlo en ejecución continua
    httpd.serve_forever()

