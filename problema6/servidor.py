#!/usr/bin/env python3
import socket
import threading

HOST = 'localhost'
PORT = 10010
BUFFER_SIZE = 1024

salas = {}  # nombre_sala: [socket]
clientes = {}  # socket: nombre_usuario
usuarios = {}  # nombre_usuario: socket
cliente_sala = {}  # socket: nombre_sala
lock = threading.Lock()

def broadcast(sala, mensaje, remitente=None):
    with lock:
        for cliente in salas.get(sala, []):
            if cliente != remitente:
                try:
                    cliente.send(mensaje.encode())
                except:
                    pass

def handle_client(conn):
    try:
        nombre = conn.recv(BUFFER_SIZE).decode().strip()
        with lock:
            clientes[conn] = nombre
            usuarios[nombre] = conn
        conn.send("Bienvenido al servidor de salas.\n".encode())

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            comando = data.decode().strip()
            partes = comando.split(maxsplit=2)

            if partes[0] == "CREATE":
                sala = partes[1]
                with lock:
                    salas.setdefault(sala, [])
                conn.send(f"Sala '{sala}' creada.\n".encode())

            elif partes[0] == "JOIN":
                sala = partes[1]
                with lock:
                    if sala not in salas:
                        conn.send("Sala no existe.\n".encode())
                        continue
                    salas[sala].append(conn)
                    cliente_sala[conn] = sala
                conn.send(f"Unido a sala '{sala}'.\n".encode())
                broadcast(sala, f"{nombre} se ha unido a la sala.", conn)

            elif partes[0] == "LEAVE":
                with lock:
                    sala = cliente_sala.get(conn)
                    if sala and conn in salas[sala]:
                        salas[sala].remove(conn)
                        broadcast(sala, f"{nombre} ha salido de la sala.", conn)
                        conn.send(f"Saliste de la sala '{sala}'.\n".encode())
                        cliente_sala.pop(conn, None)

            elif partes[0] == "MSG":
                mensaje = partes[1] if len(partes) > 1 else ""
                sala = cliente_sala.get(conn)
                if sala:
                    broadcast(sala, f"{nombre}: {mensaje}", conn)

            elif partes[0] == "PRIVADO":
                destino = partes[1]
                mensaje = partes[2] if len(partes) > 2 else ""
                with lock:
                    receptor = usuarios.get(destino)
                    if receptor:
                        receptor.send(f"[Privado de {nombre}]: {mensaje}\n".encode())
                    else:
                        conn.send("Usuario no encontrado.\n".encode())

            elif partes[0] == "USUARIOS":
                sala = cliente_sala.get(conn)
                with lock:
                    if sala:
                        nombres = [clientes[c] for c in salas[sala]]
                        conn.send(("Usuarios en sala:\n" + "\n".join(nombres) + "\n").encode())
                    else:
                        conn.send("No estás en ninguna sala.\n".encode())

            else:
                conn.send("Comando no reconocido.\n".encode())

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        with lock:
            nombre = clientes.pop(conn, None)
            sala = cliente_sala.pop(conn, None)
            if sala and conn in salas.get(sala, []):
                salas[sala].remove(conn)
                broadcast(sala, f"{nombre} ha salido del chat.")
            usuarios.pop(nombre, None)
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor de salas activo en {HOST}:{PORT}")

while True:
    conn, _ = server.accept()
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()