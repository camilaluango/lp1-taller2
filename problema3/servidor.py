#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Servidor
Objetivo: Crear un servidor de chat que maneje múltiples clientes simultáneamente usando threads
"""

import socket
import threading

HOST = 'localhost'
PORT = 10001

clients = []

def handle_client(client_socket, client_name):

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                print(f"[{client_name}] se ha desconectado.")
                clients.remove(client_socket)
                client_socket.close()
                broadcast(f"{client_name} ha salido del chat.", client_socket)
                break


            message = f"{client_name}: {data.decode()}"
            
            # Imprimir el mensaje en el servidor
            print(message)

            broadcast(message, client_socket)
            
        except ConnectionResetError:
            print(f"[{client_name}] se ha desconectado abruptamente.")
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            broadcast(f"{client_name} ha salido del chat.", client_socket)
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                pass

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Servidor a la espera de conexiones ...")

# Bucle principal para aceptar conexiones entrantes
while True:
    client, addr = server_socket.accept()
    print(f"Conexión realizada por {addr}")
    clients_name = client.recv(1024).decode()
    clients.append(client)

    # Enviar mensaje de confirmación de conexión al cliente
    client.send("ya estás conectado!".encode())
    
    # Notificar a todos los clientes que un nuevo usuario se unió al chat
    broadcast(f"{clients_name} se ha unido al Chat.", client)
    
  # args: argumentos que se pasarán a la función
    client_handler = threading.Thread(
        target=handle_client,
        args=(client, clients_name), 
        daemon=True
        )
    client_handler.start()
 
