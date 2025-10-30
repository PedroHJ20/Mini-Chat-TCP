# protocol.py
class Protocol:
    """
    Define as constantes do protocolo de comunicação
    entre cliente e servidor
    """
    # Comandos do cliente
    NICK = "NICK"
    MSG = "MSG"
    WHO = "WHO"
    QUIT = "QUIT"
    
    # Respostas do servidor
    OK = "OK"
    ERROR_PREFIX = "ERR"
    
    # Códigos de erro
    ERR_NICKNAME_IN_USE = "nickname_already_in_use"
    ERR_USER_NOT_FOUND = "user_not_found"
    
    # Prefixos e separadores
    DELIMITER = " "
    DM_PREFIX = "@"