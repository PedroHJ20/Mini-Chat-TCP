Protocolo de Comunicação - Mini Chat TCP

Visão Geral

Protocolo de aplicação baseado em texto para comunicação cliente-servidor via TCP.
Cada comando é enviado em uma linha e processado individualmente pelo servidor.

Comandos do Cliente

NICK - Registro de Apelido
Formato:
NICK <apelido>

Função: Registra o usuário no chat com um apelido único.

Regras:
- Obrigatório antes de enviar mensagens
- Apelido deve ser único no sistema
- Não permite duplicação

Exemplo:
Cliente: NICK ana
Servidor: OK welcome ana

Respostas:
- OK welcome <apelido> - Registro bem-sucedido
- ERR apelido_em_uso - Apelido já existe

MSG - Mensagem Broadcast
Formato:
MSG <mensagem>

Função: Envia mensagem para todos os usuários conectados.

Exemplo:
Cliente: MSG Olá pessoal!
Outros recebem: FROM ana [all]: Olá pessoal!

Requisitos:
- Usuário deve estar registrado (NICK)
- Mensagem é distribuída para todos exceto o remetente

MSG @ - Mensagem Privada (DM)
Formato:
MSG @<destinatario> <mensagem>

Função: Envia mensagem privada para usuário específico.

Exemplo:
Cliente: MSG @joao tudo bem?
João recebe: FROM ana [dm]: tudo bem?

Respostas:
- Entrega silenciosa (sem confirmação)
- ERR user_not_found - Destinatário não existe

WHO - Listar Usuários
Formato:
WHO

Função: Lista todos os usuários conectados no momento.

Exemplo:
Cliente: WHO
Servidor: Connected users: ana, joao, maria

QUIT - Encerrar Conexão
Formato:
QUIT

Função: Desconecta do chat de forma controlada.

Exemplo:
Cliente: QUIT
Servidor: BYE
Broadcast: User ana left the chat.

Respostas do Servidor

Confirmações (OK)
| Resposta | Significado |
|----------|-------------|
| OK welcome <apelido> | Registro aceito com sucesso |

Mensagens do Sistema
| Tipo | Formato | Descrição |
|------|---------|-----------|
| Entrada | User <apelido> joined. | Novo usuário conectou |
| Saída | User <apelido> left the chat. | Usuário desconectou |
| Registro | New User. Please register with: NICK <your_nick> | Solicitação inicial de registro |

Mensagens de Usuários
| Tipo | Formato | Descrição |
|------|---------|-----------|
| Broadcast | FROM <remetente> [all]: <mensagem> | Mensagem pública |
| Privada | FROM <remetente> [dm]: <mensagem> | Mensagem direta |

Erros (ERR)
| Código | Situação | Solução |
|--------|----------|---------|
| ERR apelido_em_uso | Apelido duplicado | Escolher outro nome |
| ERR user_not_found | Destinatário inexistente | Verificar apelido com WHO |
| ERR please_register_with_NICK | Comando antes de NICK | Registrar-se primeiro |

Fluxo de Comunicação

Cenário 1: Conexão e Broadcast
[Servidor inicia]
Servidor: Aguardando na porta 9000

[Cliente 1 conecta]
Servidor → Cliente1: New User. Please register with: NICK <your_nick>
Cliente1 → Servidor: NICK ana
Servidor → Cliente1: OK welcome ana

[Cliente 2 conecta]
Cliente2 → Servidor: NICK joao
Servidor → Cliente2: OK welcome joao
Servidor → Cliente1: User joao joined.

[Ana envia broadcast]
Cliente1 → Servidor: MSG Olá a todos!
Servidor → Cliente1: FROM ana [all]: Olá a todos!
Servidor → Cliente2: FROM ana [all]: Olá a todos!

Cenário 2: Mensagens Privadas
[João envia DM para Ana]
Cliente2 → Servidor: MSG @ana Oi, tudo bem?
Servidor → Cliente1: FROM joao [dm]: Oi, tudo bem?

[Ana responde]
Cliente1 → Servidor: MSG @joao Tudo ótimo!
Servidor → Cliente2: FROM ana [dm]: Tudo ótimo!

Cenário 3: Listagem e Saída
[João consulta usuários]
Cliente2 → Servidor: WHO
Servidor → Cliente2: Connected users: ana, joao

[Ana sai do chat]
Cliente1 → Servidor: QUIT
Servidor → Cliente1: BYE
Servidor → Cliente2: User ana left the chat.

Regras do Protocolo

1. Ordem obrigatória: NICK deve ser o primeiro comando
2. Uma linha por comando: Não quebrar comandos em múltiplas linhas
3. Case-sensitive: Comandos devem ser em MAIÚSCULAS
4. Apelidos únicos: Sistema valida duplicação automaticamente
5. Mensagens privadas: Usar @ antes do apelido destinatário
6. Desconexão limpa: Sempre usar QUIT para sair

Tabela de Comandos (Resumo)

| Comando | Sintaxe | Função | Requer NICK |
|---------|---------|--------|-------------|
| NICK | NICK <nome> | Registrar apelido | Não |
| MSG | MSG <texto> | Broadcast | Sim |
| MSG @ | MSG @<user> <texto> | Mensagem privada | Sim |
| WHO | WHO | Listar usuários | Sim |
| QUIT | QUIT | Sair do chat | Não |

Casos de Erro Comuns

Erro 1: Apelido Duplicado
Cliente1: NICK ana
Servidor: OK welcome ana

Cliente2: NICK ana
Servidor: ERR apelido_em_uso

Solução: Escolher outro apelido.

Erro 2: Usuário Não Encontrado
Cliente1: MSG @usuario_falso Olá
Servidor: ERR user_not_found

Solução: Usar WHO para verificar usuários disponíveis.

Erro 3: Mensagem Sem Registro
Cliente: MSG Olá
Servidor: ERR please_register_with_NICK

Solução: Executar NICK antes de enviar mensagens.

Diagrama de Estados
┌─────────────┐
│  CONECTADO  │
│ (sem NICK)  │
└──────┬──────┘
       │ NICK <apelido>
       ▼
┌─────────────┐
│ REGISTRADO  │◄────┐
│ (com NICK)  │     │
└──────┬──────┘     │
       │            │
       ├─ MSG ──────┤
       ├─ MSG @ ────┤
       ├─ WHO ──────┤
       │            │
       │ QUIT
       ▼
┌─────────────┐
│DESCONECTADO │
└─────────────┘

Validações do Servidor

Ao receber NICK:
- Verifica se apelido já existe
- Registra nova sessão
- Notifica outros usuários

Ao receber MSG:
- Verifica se usuário está registrado
- Identifica se é broadcast ou DM
- Valida destinatário (se DM)
- Distribui mensagem

Ao receber QUIT:
- Remove usuário da lista
- Notifica outros usuários
- Encerra conexão TCP

Observações Técnicas

- Encoding: UTF-8
- Delimitador: Nova linha (\n)
- Timeout: Sem timeout (conexão persistente)
- Tamanho máximo: Sem limite definido (prático: ~4KB)
- Concorrência: Suportada via threads no servidor
