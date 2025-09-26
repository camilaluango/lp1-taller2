#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Servidor
Objetivo: Crear un servidor TCP que devuelva exactamente lo que recibe del cliente
"""

import socket

HOST = 'localhost' 
PORT = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

while True:

    print("Servidor a la espera de conexiones ...")

    conn, addr = sock.accept()
    print(f"Conexión realizada por {addr}")

    try:
        data = conn.recv(1024)
        if not data:
            print("No se recibieron datos. Cerrando conexión.")
            continue

        # Mostrar los datos recibidos (en formato bytes)
        print("Datos recibidos:", data)
    
        conn.sendall(data)  # Enviar de vuelta los mismos datos al cliente

    finally:
        conn.close()