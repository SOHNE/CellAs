"""
Simple socket client thread sample.

Eli Bendersky (eliben@gmail.com)
This code is in the public domain

Código disponível em: https://github.com/eliben/code-for-blog/tree/master/2011/socket_client_thread_sample
Acesso em: 30 de Novembro de 2018

Referência base para o async: http://docs.python.org/c-api/init.html#PyThreadState_SetAsyncExc
"""
import socket
import struct
import threading
import queue
import inspect
import ctypes

def _async_raise(thread_obj, exception):
    found = False
    target_tid = 0
    for tid, tobj in threading._active.items():
        if tobj is thread_obj:
            found = True
            target_tid = tid
            break

    if not found:
        raise ValueError("Invalid thread object")

    ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, ctypes.py_object(exception))
    if ret == 0:
        raise ValueError("Invalid thread ID")
    elif ret > 1:
         # Por que devemos notificar mais de um thread?
         # Porque nós temos um buraco no interpretador no nível da linguagem C.
         # Então é melhor limpar a bagunça.
        ctypes.pythonapi.PyThreadState_SetAsyncExc(target_tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class ClientCommand(object):
    r""" Um comando para o encadeamento do cliente.
         Cada tipo de comando tem seus dados associados:

        CONNECT:    (host, port) tuple
        SEND:       Data string
        RECEIVE:    None
        CLOSE:      None
    """
    CONNECT, SEND, RECEIVE, CLOSE = range(4)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class ClientReply(object):
    r""" Uma resposta do segmento do cliente.
         Cada tipo de resposta tem seus dados associados:

        ERROR:      String de erro
        SUCCESS:    Depende do comando - para receber é o recebido
                     cadeia de dados, para outros Nenhum.
    """
    ERROR, SUCCESS = range(2)

    def __init__(self, type, data=None):
        self.type = type
        self.data = data


class SocketClientThread(threading.Thread):
    r""" Implementa o threading.Thread interface (start, join, etc.) e
         pode ser controlado pelo atributo Queue cmd_q. Respostas são colocadas em
         o atributo da fila reply_q.
    """
    def __init__(self, cmd_q=None, reply_q=None):
        super(SocketClientThread, self).__init__()
        self.main = queue.Queue
        self.cmd_q = self.main()
        self.reply_q = self.main()
        self.alive = threading.Event()
        self.alive.set()
        self._kill = False
        self.socket = None

        self.handlers = {
            ClientCommand.CONNECT: self._handle_CONNECT,
            ClientCommand.CLOSE: self._handle_CLOSE,
            ClientCommand.SEND: self._handle_SEND,
            ClientCommand.RECEIVE: self._handle_RECEIVE,
        }

    def run(self):
        while self.alive.isSet():
            try:
                if self._kill:
                    self.terminate()
                # Queue.get com tempo limite para permitir a verificação de self.alive
                cmd = self.cmd_q.get(True, 0.1)
                self.handlers[cmd.type](cmd)
            except queue.Empty:
                continue

    def join(self, timeout=2):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def _handle_CONNECT(self, cmd):
        try:
            self.socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(6)
            self.socket.connect((cmd.data[0], cmd.data[1]))
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_CLOSE(self, cmd):
        self.socket.close()
        self._kill = True
        reply = ClientReply(ClientReply.SUCCESS)
        self.reply_q.put(reply)

    def _handle_SEND(self, cmd):

        try:
            self.socket.sendall(cmd.data)
            self.reply_q.put(self._success_reply())
        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _handle_RECEIVE(self, cmd):
        try:
            header_data = self._recv_n_bytes(1024)
            if header_data:
                q = self._success_reply(header_data)
                self.reply_q.put(q)
                return

        except IOError as e:
            self.reply_q.put(self._error_reply(str(e)))

    def _recv_n_bytes(self, n):
        r"""
         Método conveniente para receber exatamente n bytes do self.socket
         (assumindo que esteja aberto e conectado).
        """
        while True:
            chunk = self.socket.recv(n)
            if chunk:
                return chunk

    def _get_my_tid(self):
        r"""determines this (self's) thread id"""
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")
        
        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id
        
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                return tid
        
        raise AssertionError("could not determine the thread's id")
    
    def raise_exc(self, exctype):
        r"""levanta a exceção dada no contexto desta discussão"""
        _async_raise(self._get_my_tid(), exctype)
    
    def terminate(self):
        r"""Argumentos SystemExit no contexto do segmento dado, que deve
         fazer com que o fio saia silenciosamente"""
        self.raise_exc(SystemExit)

    def _error_reply(self, errstr):
        return ClientReply(ClientReply.ERROR, errstr)

    def _success_reply(self, data=None):
        return ClientReply(ClientReply.SUCCESS, data)
