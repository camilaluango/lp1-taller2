#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""

import socket # libreria


HOST = 'localhost'  # Dirección del servidor
PORT = 9000        # Puerto del servidor

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

cliente.sendall(b"mundo")
respuesta = cliente.recv(1024)
print("Respuesta del servidor: ", respuesta)

cliente.close()

