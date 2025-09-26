#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Cliente
Objetivo: Crear un cliente de chat que se conecte a un servidor y permita enviar/recibir mensajes en tiempo real
"""

import socket
import threading

HOST = 'localhost'
PORT = 10001

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
sock.connect((HOST, PORT))

# Solicitar nombre de usuario al cliente
client_name = input("¿Cuál es tu nombre? ")

# Enviar el nombre al servidor
sock.sendall(client_name.encode())


def receive_messages():
    """
    Función ejecutada en un hilo separado para recibir mensajes del servidor
    de forma continua sin bloquear el hilo principal.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Conexión cerrada por el servidor.")
                break
            
            message = data.decode()
            print("\n" + message)
        except:
            print("Error al recibir datos.")
            break

# Crear y lanzar el hilo de recepción
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Bucle principal para enviar mensajes

while True:
    try:
        message = input("Mensaje: ")
        if message.lower() == "salir":
            print("Cerrando conexión...")
            sock.close()
            break
        sock.sendall(message.encode())
    except:
        print("Error al enviar mensaje.")
        break
