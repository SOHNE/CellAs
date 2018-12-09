#!/usr/bin/python3
# -*- coding: utf-8 -*-
import __future__
import socket
import os
import sys

# Recursos diversos
import routines
import rank
import json

# Recursos de multithreading
# Ajudam a travar no processo atual e na sua sincronização
from _thread import start_new_thread
import threading

__author__ = "Leandro de Gonzaga Peres"

r"""
No meio do caminho

No meio do caminho tinha uma pedra 
tinha uma pedra no meio do caminho 
tinha uma pedra 
no meio do caminho tinha uma pedra. 

Nunca me esquecerei desse acontecimento 
na vida de minhas retinas tão fatigadas. 
Nunca me esquecerei que no meio do caminho 
tinha uma pedra 
tinha uma pedra no meio do caminho 
no meio do caminho tinha uma pedra

Carlos Drummond de Andrade. Alguma poesia, 1930
"""

# Necessário para liberar o processo em execução a ser interrompido
lock = threading.Lock()

# Inicializa o rank
db = rank.Rank()

def session(con, addr):
    while True:
        # Recebendo as mensagens da conexão
        try:
            mensagem = con.recv(1024)
        except:
            # Fecha a conxão em caso de erro
            con.close()

        # Conexão encerrada
        if not mensagem or mensagem == "":
            # Libera o threading na saída
            lock.release()
            con.close()
            print('[-] {0}:{1} {2}'.format(addr[0], addr[1], routines.NOW))
            break
        else:
            # Bytes para str.utf-8
            mensagem = mensagem.decode()

            if mensagem[0] == "G":  # Recuperar o rank
                if bool(db.organize()):
                    # Se for uma solicitação de toda a lista
                    if mensagem == "GALL":
                        con.send(json.dumps(db.__list__).encode('utf-8'))
                    elif mensagem in ["G", "G0"]:
                        con.send(b"UP")
                    elif mensagem[1:].isdigit():  # Seleciona
                        try:
                            toSend = []
                            for i in range(int(mensagem[1:])):
                                toSend.append(db.__list__[i])

                            con.send(json.dumps(toSend).encode('utf-8'))
                        except (IndexError):
                            # Erro, pois a lista não possui tal tamanho
                            con.send(json.dumps(toSend).encode('utf-8'))
                    
                    # Requere informação do ecossistema na qual o server se insere
                    elif mensagem[1:] == "I":
                        routines.sysinfo()

            # Introduzir
            if mensagem[0] == "+":
                if len(mensagem) > 0:
                    db.introduce(mensagem[1:])

            # Remover
            elif mensagem[0] == "-":
                if len(mensagem) > 0:
                    db.remove(mensagem[1:])

            print('[{0}] {1}:{2} {3}'.format(mensagem, addr[0], addr[1], routines.NOW))
    
    # Fechando a conexão com o Socket
    con.close()


def run():
    try:
        # Endereco IP do Servidor. No caso, um loopback ip, ou o endereço da rede local.
        IP = '127.0.0.1'
        # Porta de comunicação do servidor
        # 65535 é o valor máximo, e 0 mínimo.
        # Caso 0, será qualquer porta aberta
        PORT = 26969

        # Iniciando o socket e definindo as atribuições
        # AF_INET = IPv4
        # AF_INET6 = IPv6
        # SOCK_STREAM = TCP
        # SOCK_DGRAM = UDP
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Agrupando as informações
        self = (IP, PORT)

        # Aplicando o endereço IP e a porta no Socket
        tcp.bind(self)

        # Informações sobre o ecossistema
        routines.sysinfo()

        # Garante ao server aceitar conexões
        tcp.listen(0)

        INFO_SHOW = '\nServidor TCP iniciado em {0} na porta {1}'.format(tcp.getsockname()[0], tcp.getsockname()[1])

        print(INFO_SHOW)
        print('_' * (len(INFO_SHOW) - 1))

        while True: 
    
            # Inicia a conexão com o cliente
            client, addr = tcp.accept() 
    
            # Instância uma trava ao cliente
            lock.acquire() 
            print('[+] {0}:{1} {2}'.format(addr[0], addr[1], routines.NOW))
    
            # Inicializa um novo thread com o seu devido identificador
            start_new_thread(session, (client, addr)) 
        tcp.close()

    except (KeyboardInterrupt, SystemExit, socket.error):
        tcp.close()
        sys.exit(0)

# Garante que o servidor seja executado propriamente, e não como um módulo importado
if __name__ == "__main__":
    run()
