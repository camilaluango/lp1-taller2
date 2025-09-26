#!/usr/bin/env python3
import socket
import threading

BUFFER_SIZE = 8192
HOST = 'localhost'
PORT = 8888

def log(mensaje):
    print("[LOG]", mensaje)

def handle_client(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        first_line = request.split(b'\n')[0].decode()
        log(f"Solicitud: {first_line}")

        if first_line.startswith("CONNECT"):
            destino = first_line.split()[1]
            host, port = destino.split(":")
            port = int(port)

            try:
                server_socket = socket.create_connection((host, port))
                client_socket.send(b"HTTP/1.1 200 Connection established\r\n\r\n")
                forward_data(client_socket, server_socket)
            except Exception as e:
                log(f"Error CONNECT: {e}")
                client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")

        else:
            lines = request.decode().split("\r\n")
            host_line = [line for line in lines if line.lower().startswith("host:")]
            if not host_line:
                client_socket.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                return

            host = host_line[0].split(":")[1].strip()
            port = 80

            try:
                server_socket = socket.create_connection((host, port))
                server_socket.send(request)

                while True:
                    data = server_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    client_socket.send(data)
            except Exception as e:
                log(f"Error HTTP: {e}")
                client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")

    except Exception as e:
        log(f"Error general: {e}")
    finally:
        client_socket.close()

def forward_data(sock1, sock2):
    def pipe(src, dst):
        try:
            while True:
                data = src.recv(BUFFER_SIZE)
                if not data:
                    break
                dst.send(data)
        except:
            pass
        finally:
            src.close()
            dst.close()

    threading.Thread(target=pipe, args=(sock1, sock2), daemon=True).start()
    threading.Thread(target=pipe, args=(sock2, sock1), daemon=True).start()

proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy.bind((HOST, PORT))
proxy.listen(100)
print(f"Proxy HTTP activo en {HOST}:{PORT}")

while True:
    client_sock, _ = proxy.accept()
    threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()