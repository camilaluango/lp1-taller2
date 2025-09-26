#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""

import http.client

# Definir la dirección y puerto del servidor HTTP
HOST = 'localhost'
PORT = 8080  # Asegúrate de que el servidor esté escuchando en este puerto

# Crear una conexión HTTP con el servidor
conn = http.client.HTTPConnection(HOST, PORT)

# Realizar una petición GET al path raíz ('/')
conn.request("GET", "/")

# Obtener la respuesta del servidor
response = conn.getresponse()

# Leer el contenido de la respuesta
data = response.read()

# Decodificar los datos de bytes a string e imprimirlos
print("Respuesta del servidor:")
print(data.decode())

# Cerrar la conexión con el servidor
conn.close()
