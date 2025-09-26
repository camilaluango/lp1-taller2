#!/usr/bin/env python3
import socket
import threading
import json

HOST = 'localhost'
PORT = 0  # Puerto dinámico
BUFFER_SIZE = 1024
estado = {}
servidores = []

def sincronizar_estado():
    for ip, port in servidores:
        try:
            s = socket.create_connection((ip, port))
            s.send(b"SINC\n")
            s.send(json.dumps(estado).encode())
            s.close()
        except:
            pass

def handle_client(conn):
    global estado
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            comando = data.decode().strip()

            if comando == "GET":
                conn.send(json.dumps(estado).encode())

            elif comando.startswith("SET"):
                _, clave, valor = comando.split()
                estado[clave] = valor
                sincronizar_estado()
                conn.send(b"OK\n")

            elif comando == "SINC":
                datos = conn.recv(BUFFER_SIZE).decode()
                estado = json.loads(datos)
                conn.send(b"SINCRONIZADO\n")

            else:
                conn.send(b"Comando no reconocido\n")
    except:
        pass
    finally:
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, 0))
ip, port = server.getsockname()
print(f"Servidor backend activo en {ip}:{port}")
server.listen(5)

while True:
    conn, _ = server.accept()
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()