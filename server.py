# server.py
import socket
import threading
import time

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}  # Dicionário: nick -> socket
        self.lock = threading.Lock()
        self.server_socket = None

    def start(self):
        """Inicia o servidor de chat"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"🚀 Servidor de chat ouvindo em {self.host}:{self.port}")
        print("Pressione Ctrl+C para parar o servidor")

        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"📞 Nova conexão de {address}")
                
                # Criar thread para cada cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado.")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, address):
        """Gerencia a comunicação com um cliente específico"""
        nick = None
        try:
            # Fase de registro do apelido
            nick = self.register_nickname(client_socket)
            if nick is None:
                return

            # Loop principal de mensagens
            while True:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break

                # Processar comando
                if data.upper() == 'WHO':
                    self.list_users(client_socket)
                elif data.upper() == 'QUIT':
                    break
                elif data.startswith('@'):
                    self.send_direct_message(nick, data)
                else:
                    # Mensagem broadcast
                    self.broadcast(f"FROM {nick} [all]: {data}\n", exclude=nick)

        except Exception as e:
            print(f"❌ Erro com cliente {nick}: {e}")
        finally:
            if nick:
                self.remove_client(nick, client_socket)

    def register_nickname(self, client_socket):
        """Registra apelido único para o cliente"""
        client_socket.send("Digite seu apelido: ".encode('utf-8'))
        nick = client_socket.recv(1024).decode('utf-8').strip()

        with self.lock:
            if nick in self.clients or nick == "":
                client_socket.send("ERR nickname_already_in_use\n".encode('utf-8'))
                client_socket.close()
                return None
            
            self.clients[nick] = client_socket
            client_socket.send("OK\n".encode('utf-8'))
            # Notificar todos sobre o novo usuário
            self.broadcast(f"👉 Usuário '{nick}' entrou no chat\n", exclude=nick)
            print(f"✅ Usuário '{nick}' registrado")
            return nick

    def broadcast(self, message, exclude=None):
        """Envia mensagem para todos os clientes, exceto o exclude"""
        with self.lock:
            disconnected_clients = []
            for nick, sock in self.clients.items():
                if nick != exclude:
                    try:
                        sock.send(message.encode('utf-8'))
                    except:
                        disconnected_clients.append(nick)
            
            # Remove clientes desconectados
            for nick in disconnected_clients:
                if nick in self.clients:
                    try:
                        self.clients[nick].close()
                    except:
                        pass
                    del self.clients[nick]

    def send_direct_message(self, sender_nick, message):
        """Envia mensagem direta para um usuário"""
        # A mensagem deve estar no formato "@destinatario mensagem"
        parts = message.split(' ', 1)
        if len(parts) < 2:
            return

        dest_nick = parts[0][1:]  # Remove o '@'
        msg_content = parts[1]

        with self.lock:
            if dest_nick in self.clients:
                try:
                    dest_socket = self.clients[dest_nick]
                    dest_socket.send(f"FROM {sender_nick} [dm]: {msg_content}\n".encode('utf-8'))
                    print(f"📨 DM de {sender_nick} para {dest_nick}")
                except:
                    self.remove_client(dest_nick, dest_socket)
            else:
                # Informar ao remetente que o usuário não foi encontrado
                if sender_nick in self.clients:
                    try:
                        self.clients[sender_nick].send("ERR user_not_found\n".encode('utf-8'))
                    except:
                        self.remove_client(sender_nick, self.clients[sender_nick])

    def list_users(self, client_socket):
        """Lista os usuários conectados para o cliente que solicitou"""
        with self.lock:
            users = list(self.clients.keys())
            user_list = ", ".join(users)
            response = f"👥 Usuários conectados ({len(users)}): {user_list}\n"
            try:
                client_socket.send(response.encode('utf-8'))
            except:
                pass

    def remove_client(self, nick, client_socket):
        """Remove cliente e notifica os outros"""
        with self.lock:
            if nick in self.clients:
                del self.clients[nick]
                self.broadcast(f"👋 Usuário '{nick}' saiu do chat\n", exclude=nick)
                print(f"❌ Usuário '{nick}' desconectado")
        try:
            client_socket.close()
        except:
            pass

if __name__ == "__main__":
    server = ChatServer()
    server.start()