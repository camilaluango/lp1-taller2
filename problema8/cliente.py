#!/usr/bin/env python3
import socket
import threading

HOST = 'localhost'
PORT = 10020
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

threading.Thread(target=recibir, args=(sock,), daemon=True).start()

while True:
    comando = input(">> ").strip()
    if comando.upper() == "EXIT":
        sock.send(b"EXIT\n")
        break
    sock.send((comando + '\n').encode())

sock.close()