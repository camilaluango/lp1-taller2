#!/usr/bin/env python3
import socket
import os
import hashlib

HOST = 'localhost'
PORT = 9000
BUFFER_SIZE = 4096

def calcular_checksum(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    comando = input("Comando (UPLOAD archivo | DOWNLOAD archivo | LIST | SALIR): ").strip()
    if comando.upper() == 'SALIR':
        break

    parts = comando.split()
    if parts[0] == 'UPLOAD':
        filename = parts[1]
        if not os.path.exists(filename):
            print("Archivo no encontrado.")
            continue

        filesize = os.path.getsize(filename)
        sock.send(f"UPLOAD {os.path.basename(filename)} {filesize}\n".encode())

        with open(filename, 'rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                sock.send(chunk)

        respuesta = sock.recv(BUFFER_SIZE).decode()
        print("Servidor:", respuesta)

        local_checksum = calcular_checksum(filename)
        if local_checksum in respuesta:
            print("✔️ Integridad verificada")
        else:
            print("⚠️ Checksum no coincide")

    elif parts[0] == 'DOWNLOAD':
        filename = parts[1]
        sock.send(f"DOWNLOAD {filename}\n".encode())

        header = sock.recv(BUFFER_SIZE).decode()
        if header.startswith("ERROR"):
            print("Servidor:", header)
            continue

        _, filesize = header.strip().split()
        filesize = int(filesize)
        with open(f"descargado_{filename}", 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = sock.recv(min(BUFFER_SIZE, filesize - bytes_received))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print(f"✔️ Archivo descargado como descargado_{filename}")

    elif parts[0] == 'LIST':
        sock.send("LIST\n".encode())
        respuesta = sock.recv(BUFFER_SIZE).decode()
        print("Archivos disponibles:\n", respuesta)

    else:
        print("Comando no reconocido.")

sock.close()