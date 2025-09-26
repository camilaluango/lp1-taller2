#!/usr/bin/env python3
import socket
import threading

HOST = 'localhost'
PORT = 10010
BUFFER_SIZE = 1024

def recibir(sock):
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            print("\n" + data.decode())
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

nombre = input("¿Cuál es tu nombre? ")
sock.send(nombre.encode())

threading.Thread(target=recibir, args=(sock,), daemon=True).start()

while True:
    comando = input(">> ").strip()
    if comando.upper() == "SALIR":
        sock.close()
        break
    sock.send(comando.encode())