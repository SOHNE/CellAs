# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Importando o módulo socket do Python
import socket

# Importando, com a devida importância, as informações de conexões com o servidor
from lib.config import *

# Necessário para conversão do rank em bytes
import json

# Necessário para o tratamento de erro da lista de execução vazia
import queue

# Importa a conexão threading do cliente
from .socketThread import SocketClientThread, ClientCommand, ClientReply

# Informações acerca deste 'pacote'
__author__ = "Leandro Peres"
__all__ = ['connect', 'Request', 'Insert', 'Get']

r"""
Sobre a esquemática da conexão:

O Queue funciona como uma lista de execução.
Dito isto, para viabilizar uma nova execução, há um arquétipo de comando
chamado cmd_q (definida no código socketThread) que na qual insere
uma determinada execução na lista.

Já o reply_q é a respota das execuções do thread inseridos no queue.
"""

# Define a identificação da conexão
# IP/HOST, Porta
self = '127.0.0.1', 26969

# Inicializa a conexão
connection = SocketClientThread()
connection.start()

def connect(blocking=True):
    r"""
    Método para conexão por thread e queue com o servidor.
    
    Returns:
        :bool:
    """
    try:
        connection.cmd_q.put(ClientCommand(ClientCommand.CONNECT, self))
        reply = connection.reply_q.get(block=blocking)
        return bool(reply.type)
    except queue.Empty:
        pass

def Request(n=6):
    r"""
    Método para requisição da lista __list__ em rank/__init__.py
    
    Args:
        :n: int: Tamanho total da lista a ser recebida
    """
    toSend = 'G{0}'.format(n).encode('utf-8')
    connection.cmd_q.put(ClientCommand(ClientCommand.SEND, toSend ) )
    connection.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, toSend))

def Insert(name, score):
    r"""
    Método para inserção da lista __list__ em rank/__init__.py
    
    Args:
        :name: str: Identificação por nome/apelido do jogador
        :score: int: Pontuação obtida pela jogatina atual
    """
    toSend = '+{0},{1},0.0'.format(name, score).encode('utf-8')
    connection.cmd_q.put(ClientCommand(ClientCommand.SEND, toSend ) )

def Get(blocking=True):
    r"""
    Método para obtenção da resposta do servidor.
    
    Returns:
        :list: Retorna a lista, em ordem decrescente com referência ao score, de dicionários do rank
    """
    try:
        reply = connection.reply_q.get(block=blocking)
        if reply.data not in [None, "timed out", "[Errno 32] Broken pipe", "[WinError 10061] Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente"]:
            return json.loads(reply.data.decode('utf-8'))

    except queue.Empty:
        pass