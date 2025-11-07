#!/usr/bin/env python3
# server.py - Mini-Chat TCP multiusuário

import socket
import threading
import sys
import traceback
from typing import Dict, Tuple

HOST = '0.0.0.0'
PORT = 9000
BUFFER_SIZE = 4096
ENC = 'utf-8'

clients: Dict[str, Tuple[socket.socket, Tuple[str, int]]] = {}
clients_lock = threading.Lock()

def send_line(sock: socket.socket, line: str):
    try:
        sock.sendall((line + "\n").encode(ENC))
    except Exception:
        raise

def broadcast(sender_nick: str, message: str):
    with clients_lock:
        for nick, (csock, _) in list(clients.items()):
            if nick == sender_nick:
                continue
            try:
                send_line(csock, f"FROM {sender_nick} [all]: {message}")
            except Exception:
                print(f"Erro enviando para {nick}, removendo")
                remove_client(nick)

def send_dm(sender_nick: str, dest_nick: str, message: str) -> bool:
    with clients_lock:
        if dest_nick in clients:
            dest_sock, _ = clients[dest_nick]
            try:
                send_line(dest_sock, f"FROM {sender_nick} [dm]: {message}")
                return True
            except Exception:
                print(f"Erro enviando DM para {dest_nick}, removendo")
                remove_client(dest_nick)
                return False
        else:
            return False

def list_users() -> str:
    with clients_lock:
        return ", ".join(sorted(clients.keys()))

def remove_client(nick: str):
    with clients_lock:
        if nick in clients:
            sock, addr = clients.pop(nick)
            try:
                sock.close()
            except Exception:
                pass
            notify = f"User {nick} left"
            print(notify)
            for other_nick, (osock, _) in list(clients.items()):
                try:
                    send_line(osock, notify)
                except Exception:
                    pass

def handle_client(conn: socket.socket, addr: Tuple[str, int]):
    conn_file = conn.makefile('r', encoding=ENC, newline='\n')
    nick = None
    try:
        send_line(conn, "New User. Please register with: NICK <your_nick>")
        while True:
            line = conn_file.readline()
            if not line:
                print(f"Conexão fechada por {addr} antes de registrar")
                return
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split(' ', 1)
            cmd = parts[0].upper()
            if cmd == 'NICK' and len(parts) == 2:
                candidate = parts[1].strip()
                if not candidate:
                    send_line(conn, "ERR invalid_nick")
                    continue
                with clients_lock:
                    if candidate in clients:
                        send_line(conn, "ERR nick_in_use")
                    else:
                        nick = candidate
                        clients[nick] = (conn, addr)
                        send_line(conn, f"OK Welcome {nick}")
                        for other_nick, (osock, _) in list(clients.items()):
                            if other_nick == nick:
                                continue
                            try:
                                send_line(osock, f"User {nick} joined")
                            except Exception:
                                pass
                        print(f"User {nick} registered from {addr}")
                        break
            else:
                send_line(conn, "ERR please_register_with_NICK")

        while True:
            line = conn_file.readline()
            if not line:
                print(f"{nick} disconnected abruptly")
                break
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split(' ', 1)
            cmd = parts[0].upper()
            arg = parts[1] if len(parts) > 1 else ''

            if cmd == 'MSG':
                if not arg:
                    send_line(conn, "ERR empty_message")
                    continue
                if arg.lstrip().startswith('@'):
                    rest = arg.lstrip()
                    try:
                        at, content = rest.split(' ', 1)
                    except ValueError:
                        send_line(conn, "ERR malformed_dm")
                        continue
                    dest_nick = at[1:]
                    ok = send_dm(nick, dest_nick, content)
                    if not ok:
                        send_line(conn, "ERR user_not_found")
                    else:
                        send_line(conn, f"OK dm_sent to {dest_nick}")
                else:
                    broadcast(nick, arg)
                    send_line(conn, "OK broadcast_sent")

            elif cmd == 'WHO':
                users = list_users()
                send_line(conn, f"OK {users}")

            elif cmd == 'QUIT':
                send_line(conn, "OK goodbye")
                break

            else:
                send_line(conn, "ERR unknown_command")

    except Exception as e:
        print(f"Exception handling client {addr}: {e}")
        traceback.print_exc()
    finally:
        if nick:
            remove_client(nick)
        else:
            try:
                conn.close()
            except Exception:
                pass

def run_server(host: str = HOST, port: int = PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Chat server listening on {host}:{port}")
        try:
            while True:
                conn, addr = s.accept()
                print(f"Connection from {addr}")
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("Shutting down server")
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    elif len(sys.argv) == 2:
        PORT = int(sys.argv[1])
    run_server(HOST, PORT)
