#!/usr/bin/env python3
import socket
import threading
import random

HOST = 'localhost'
PORT = 9000
BUFFER_SIZE = 1024

servidores_backend = [
    ('localhost', 10001),
    ('localhost', 10002),
    ('localhost', 10003)
]

def reenviar_a_backend(data):
    for intento in range(len(servidores_backend)):
        ip, port = random.choice(servidores_backend)
        try:
            s = socket.create_connection((ip, port), timeout=2)
            s.send(data)
            respuesta = s.recv(BUFFER_SIZE)
            s.close()
            return respuesta
        except:
            continue
    return "Todos los servidores están caídos\n".encode('utf-8')

def handle_client(conn):
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            respuesta = reenviar_a_backend(data)
            conn.send(respuesta)
    except:
        pass
    finally:
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)
print(f"Balanceador activo en {HOST}:{PORT}")

while True:
    conn, _ = server.accept()
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()