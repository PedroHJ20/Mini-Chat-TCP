#!/usr/bin/env python3
# client.py - Cliente interativo para o Mini-Chat

import socket
import sys
import threading

ENC = 'utf-8'
BUFFER_SIZE = 4096

def recv_loop(sock: socket.socket):
    try:
        f = sock.makefile('r', encoding=ENC, newline='\n')
        while True:
            line = f.readline()
            if not line:
                print('\n[Disconnected from server]')
                break
            print('\n' + line.rstrip('\n'))
            print('> ', end='', flush=True)
    except Exception as e:
        print(f'Error in receive loop: {e}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python client.py HOST PORT')
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    rt = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    rt.start()

    try:
        while True:
            line = input('> ').strip()
            if not line:
                continue
            sock.sendall((line + '\n').encode(ENC))
            if line.upper().startswith('QUIT'):
                break
    except KeyboardInterrupt:
        try:
            sock.sendall(('QUIT\n').encode(ENC))
        except Exception:
            pass
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print('Connection closed')
