# Mini-Chat-TCP

Grupo : 
Pedro Henrique Jerônimo Da Silva
Carlos Henrique da Costa Souza
Ludmylla Dias de Souza Santos
MATHEUS VINNYCIUS VASCONCELOS DE SANTANA



Mini Chat TCP em Python

Sistema de chat multiusuário em tempo real via protocolo TCP/IP.
Permite comunicação simultânea entre múltiplos clientes através do terminal.

Características

- Múltiplos usuários simultâneos
- Mensagens públicas (broadcast)
- Mensagens privadas (DM)
- Listagem de usuários online
- Notificações de entrada/saída
- Validação de apelidos únicos
- Interface via terminal
- Sem dependências externas

Requisitos

- Python: 3.8 ou superior
- Bibliotecas: Apenas nativas (socket, threading)
- Sistema Operacional: Windows, Linux ou macOS

Verificar versão do Python:
python --version
ou
python3 --version

Instalação e Execução

Passo 1: Baixar Arquivos
Certifique-se de ter os arquivos:
- server.py
- client.py

Passo 2: Iniciar o Servidor

Abra um terminal e execute:
python server.py

Saída esperada:
Servidor rodando em 127.0.0.1:9000

Servidor ativo! Mantenha este terminal aberto.

Passo 3: Conectar Clientes

Em novos terminais (um para cada usuário):
python client.py 127.0.0.1 9000

Primeira mensagem do servidor:
New User. Please register with: NICK 

Registre seu apelido:
NICK ana

Confirmação:
OK welcome ana

Cliente conectado e pronto para usar!

Comandos Disponíveis

Registro
NICK ana
→ Registra você como "ana"

Mensagem para Todos
MSG Olá pessoal!
→ Todos recebem: FROM ana [all]: Olá pessoal!

Mensagem Privada
MSG @joao tudo bem?
→ Apenas João recebe: FROM ana [dm]: tudo bem?

Listar Usuários
WHO
→ Mostra: Connected users: ana, joao, maria

Sair do Chat
QUIT
→ Você recebe: BYE  
→ Outros veem: User ana left the chat.

Testes Rápidos

Teste 1: Comunicação Básica
Terminal 1
python server.py

Terminal 2
python client.py 127.0.0.1 9000
NICK ana
MSG Olá!

Terminal 3
python client.py 127.0.0.1 9000
NICK joao
MSG Oi Ana!

Resultado esperado: Ambos veem as mensagens um do outro.

Teste 2: Mensagem Privada
Terminal Ana
MSG @joao essa mensagem é só pra você

Terminal João
Recebe: FROM ana [dm]: essa mensagem é só pra você

Resultado esperado: Apenas João recebe a mensagem.

Teste 3: Apelido Duplicado
Terminal 1
NICK ana

Terminal 2
NICK ana
Recebe: ERR apelido_em_uso

Resultado esperado: Segundo cliente não consegue usar "ana".

Teste 4: Usuário Inexistente
MSG @usuario_falso oi
Recebe: ERR user_not_found

Resultado esperado: Erro ao tentar enviar DM para usuário inexistente.

Teste 5: Listagem de Usuários
WHO
Recebe: Connected users: ana, joao, maria

Resultado esperado: Lista todos conectados no momento.

Conectar de Outra Máquina (Rede Local)

No Servidor:

1. Descubra o IP local:
   Windows
   ipconfig
   
   Linux/Mac
   ifconfig
   ou
   ip addr

2. Procure algo como:
   IPv4 Address: 192.168.1.100

3. Configure o firewall:
   - Liberar porta 9000 para conexões TCP

No Cliente Remoto:
python client.py 192.168.1.100 9000

Substitua 192.168.1.100 pelo IP real do servidor.

Estrutura do Projeto
mini-chat-tcp/
│
├── server.py       # Servidor TCP (executa primeiro)
├── client.py       # Cliente TCP (conecta ao servidor)
├── protocol.md     # Documentação do protocolo
└── README.md       # Este arquivo

Solução de Problemas

Erro: "Connection refused"
Causa: Servidor não está rodando.  
Solução: Execute python server.py primeiro.

Erro: "Address already in use"
Causa: Porta 9000 ocupada por outro processo.  
Solução: 
- Encerre o processo anterior
- Ou altere a porta no código

Erro: "No module named 'socket'"
Causa: Python desatualizado ou instalação incorreta.  
Solução: Reinstale Python 3.8+

Cliente não recebe mensagens
Causa: Não executou comando NICK.  
Solução: Sempre registre apelido antes: NICK seu_nome

Não consegue conectar de outra máquina
Causa: Firewall bloqueando porta 9000.  
Solução: 
- Libere porta 9000 no firewall
- Verifique se ambas máquinas estão na mesma rede

Conceitos Técnicos Aplicados

Programação de Redes
- Sockets TCP para comunicação confiável
- Modelo cliente-servidor
- Comunicação bidirecional

Concorrência
- Threading para múltiplas conexões
- Sincronização de recursos compartilhados
- Gerenciamento de estado por cliente

Protocolo de Aplicação
- Comandos estruturados em texto
- Respostas padronizadas
- Tratamento de erros

Fluxo de Execução
┌──────────┐         ┌──────────┐         ┌──────────┐
│ Cliente1 │         │ Servidor │         │ Cliente2 │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                    │                    │
     │───CONNECT──────────>│                   │
     │<──"Register"────────│                   │
     │───NICK ana──────────>│                   │
     │<──OK welcome────────│                   │
     │                     │<──CONNECT──────────│
     │                     │───"Register"──────>│
     │                     │<──NICK joao────────│
     │<──User joao joined──│───OK welcome──────>│
     │                     │                    │
     │───MSG Olá!──────────>│                   │
     │<──FROM ana [all]────│───FROM ana [all]──>│
     │                     │                    │
     │───MSG @joao oi──────>│                   │
     │                     │───FROM ana [dm]───>│
     │                     │                    │
     │───QUIT──────────────>│                   │
     │<──BYE───────────────│                   │
     │                     │───User ana left───>│
     X                     │                    │

Checklist de Execução

- Python 3.8+ instalado e verificado
- Arquivos server.py e client.py prontos
- Servidor iniciado (python server.py)
- Cliente 1 conectado e registrado
- Cliente 2 conectado e registrado
- Teste de broadcast realizado
- Teste de mensagem privada realizado
- Comando WHO testado
- Comando QUIT testado
- Todos os casos de erro verificados

Documentação Adicional

- protocol.md: Especificação completa do protocolo
- Comentários no código: Explicações técnicas detalhadas

Casos de Uso

Uso 1: Chat de Equipe Local
Equipe na mesma rede local pode usar para comunicação rápida sem internet.

Uso 2: Educacional
Aprender conceitos de redes, sockets e concorrência na prática.

Uso 3: Prototipagem
Base para desenvolvimento de sistemas de mensagens mais complexos.

Exemplo Completo de Sessão
TERMINAL 1: SERVIDOR
python server.py
Servidor rodando em 127.0.0.1:9000

TERMINAL 2: ANA
python client.py 127.0.0.1 9000
New User. Please register with: NICK 
NICK ana
OK welcome ana
MSG Olá a todos!
FROM ana [all]: Olá a todos!
WHO
Connected users: ana, joao
MSG @joao oi joão, tudo bem?
QUIT
BYE

TERMINAL 3: JOÃO
python client.py 127.0.0.1 9000
New User. Please register with: NICK 
NICK joao
OK welcome joao
User ana joined.
FROM ana [all]: Olá a todos!
MSG Oi Ana!
FROM joao [all]: Oi Ana!
FROM ana [dm]: oi joão, tudo bem?
MSG @ana tudo ótimo!
User ana left the chat.
QUIT
BYE

Informações do Projeto

Autor: Pedro Henrique  
Instituição: [Sua Instituição]  
Disciplina: Redes de Computadores  
Data: Novembro 2025  
Versão: 1.0  
Licença: Uso Acadêmico

Status do Projeto

Completo e funcional  
Testado e validado  
Documentação completa  
Pronto para apresentação

Dúvidas? Consulte protocol.md para detalhes técnicos do protocolo.
