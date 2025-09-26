#!/usr/bin/env python3
import socket
import threading
import os
import hashlib

HOST = 'localhost'
PORT = 9000
BUFFER_SIZE = 4096
BASE_DIR = './archivos'

os.makedirs(BASE_DIR, exist_ok=True)

def calcular_checksum(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def handle_client(conn, addr):
    print(f"[+] Conexión desde {addr}")
    try:
        while True:
            command = conn.recv(BUFFER_SIZE).decode().strip()
            if not command:
                break

            parts = command.split()
            if parts[0] == 'UPLOAD':
                filename = parts[1]
                filesize = int(parts[2])
                filepath = os.path.join(BASE_DIR, os.path.basename(filename))

                with open(filepath, 'wb') as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        chunk = conn.recv(min(BUFFER_SIZE, filesize - bytes_received))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)

                checksum = calcular_checksum(filepath)
                conn.send(f"UPLOAD OK {checksum}\n".encode())

            elif parts[0] == 'DOWNLOAD':
                filename = parts[1]
                filepath = os.path.join(BASE_DIR, os.path.basename(filename))

                if not os.path.exists(filepath):
                    conn.send("ERROR Archivo no encontrado\n".encode())
                    continue

                filesize = os.path.getsize(filepath)
                conn.send(f"OK {filesize}\n".encode())

                with open(filepath, 'rb') as f:
                    while chunk := f.read(BUFFER_SIZE):
                        conn.send(chunk)

            elif parts[0] == 'LIST':
                archivos = os.listdir(BASE_DIR)
                respuesta = '\n'.join(archivos) + '\n'
                conn.send(respuesta.encode())

            else:
                conn.send("ERROR Comando no reconocido\n".encode())

    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor activo en {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()