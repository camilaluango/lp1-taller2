#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 8888

peticion = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send(peticion.encode())

while True:
    data = sock.recv(4096)
    if not data:
        break
    print(data.decode(errors='ignore'))

sock.close()