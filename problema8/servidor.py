#!/usr/bin/env python3
import socket
import threading

HOST = 'localhost'
PORT = 10020
BUFFER_SIZE = 1024

tablero = [[' ']*3 for _ in range(3)]
jugadores = []
espectadores = []
turno = 0
lock = threading.Lock()

def mostrar_tablero():
    filas = [' | '.join(row) for row in tablero]
    return '\n---------\n'.join(filas)

def enviar_a_todos(mensaje):
    for conn in jugadores + espectadores:
        try:
            conn.send((mensaje + '\n').encode())
        except:
            pass

def validar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return True
    return False

def handle_client(conn):
    global turno
    try:
        conn.send("Bienvenido. Escribe JOIN para jugar o WATCH para observar.\n".encode())
        rol = conn.recv(BUFFER_SIZE).decode().strip().upper()

        with lock:
            if rol == "JOIN" and len(jugadores) < 2:
                jugadores.append(conn)
                jugador_id = len(jugadores) - 1
                conn.send(f"Te uniste como jugador {jugador_id + 1} ({'X' if jugador_id == 0 else 'O'})\n".encode())
                enviar_a_todos(mostrar_tablero())
            elif rol == "WATCH":
                espectadores.append(conn)
                conn.send("Estás observando la partida.\n".encode())
                conn.send((mostrar_tablero() + '\n').encode())
            else:
                conn.send("No hay espacio para más jugadores.\n".encode())
                conn.close()
                return

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            comando = data.decode().strip().split()

            with lock:
                if comando[0] == "MOVE" and conn == jugadores[turno]:
                    fila, col = int(comando[1]), int(comando[2])
                    if 0 <= fila < 3 and 0 <= col < 3 and tablero[fila][col] == ' ':
                        tablero[fila][col] = 'X' if turno == 0 else 'O'
                        enviar_a_todos(mostrar_tablero())

                        if validar_ganador():
                            enviar_a_todos(f"Jugador {turno + 1} ha ganado!")
                            break

                        turno = 1 - turno
                    else:
                        conn.send("Movimiento inválido.\n".encode())

                elif comando[0] == "BOARD":
                    conn.send((mostrar_tablero() + '\n').encode())

                elif comando[0] == "EXIT":
                    conn.send("Saliendo del juego.\n".encode())
                    break

                else:
                    conn.send("Comando no reconocido o fuera de turno.\n".encode())

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        with lock:
            if conn in jugadores:
                jugadores.remove(conn)
            if conn in espectadores:
                espectadores.remove(conn)
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor de Tic-Tac-Toe activo en {HOST}:{PORT}")

while True:
    conn, _ = server.accept()
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()