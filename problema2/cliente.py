#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Cliente
Objetivo: Crear un cliente TCP que envíe un mensaje al servidor y reciba la misma respuesta
"""

import socket

HOST = 'localhost' 
PORT = 10000  

# Solicitar mensaje al usuario por consola
message = input("Mensaje: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar el socket al servidor
    sock.connect((HOST, PORT))

    print(f"Mensaje '{message}' enviado.")
    
    # Enviar mensaje al servidor
    sock.sendall(message.encode())
    
    # Recibir respuesta del servidor
    data = sock.recv(1024)

    print("Mensaje recibido: ", data.decode())

finally:
    sock.close()