#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 9000
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    comando = input(">> ").strip()
    if comando.upper() == "SALIR":
        break
    sock.send((comando + '\n').encode())
    respuesta = sock.recv(BUFFER_SIZE)
    print("Servidor:", respuesta.decode())

sock.close()