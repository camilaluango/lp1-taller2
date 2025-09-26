#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""

import socket # libreria


HOST = 'localhost'  # Dirección del servidor
PORT = 9000        # Puerto del servidor

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("Servidor a la espera de conexiones ...")

cliente, direccion = servidor.accept()
print(f"Conexión realizada por {direccion}")

datos = cliente.recv(1024)
cliente.sendall(b"Hola!" + datos) #ojo debe ser binario no cadena
cliente

