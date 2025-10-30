# client.py
import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        """Inicia o cliente de chat"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            
            print(f"✅ Conectado ao servidor {self.host}:{self.port}")
            print("Comandos disponíveis:")
            print("  - WHO: Listar usuários online")
            print("  - QUIT: Sair do chat")
            print("  - @usuario mensagem: Mensagem direta")
            print("  - mensagem normal: Mensagem para todos\n")

            # Thread para receber mensagens do servidor
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            # Loop principal para enviar mensagens
            self.send_messages()

        except ConnectionRefusedError:
            print(f"❌ Não foi possível conectar ao servidor {self.host}:{self.port}")
            print("Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
        finally:
            self.stop()

    def receive_messages(self):
        """Recebe mensagens do servidor em uma thread separada"""
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    print("🔌 Conexão encerrada pelo servidor.")
                    self.running = False
                    break
                print(message, end='')  # end='' para não quebrar linha dupla
            except:
                if self.running:  # Só mostra erro se não foi desconexão intencional
                    print("❌ Erro na conexão com o servidor.")
                break

    def send_messages(self):
        """Envia mensagens para o servidor"""
        while self.running:
            try:
                message = input().strip()
                
                if not message:
                    continue
                    
                if message.upper() == 'QUIT':
                    self.socket.send(message.encode('utf-8'))
                    time.sleep(0.1)  # Dar tempo para o servidor processar
                    break
                else:
                    self.socket.send(message.encode('utf-8'))
                    
            except KeyboardInterrupt:
                print("\n🛑 Saindo do chat...")
                break
            except Exception as e:
                print(f"❌ Erro ao enviar mensagem: {e}")
                break

    def stop(self):
        """Encerra o cliente"""
        self.running = False
        if self.socket:
            try:
                self.socket.send("QUIT".encode('utf-8'))
            except:
                pass
            self.socket.close()
        print("👋 Cliente encerrado.")

if __name__ == "__main__":
    # Permite especificar host e porta por argumentos
    host = 'localhost'
    port = 12345
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    client = ChatClient(host, port)
    client.start()