# !/usr/bin/python3
# -*- coding: utf-8 -*-
import __future__
import os
import sys
from .analytics import *
import pygame as pg
import json
import platform

# Imporanto o módulo para saber a linguagem do sistema
from locale import getdefaultlocale as locale

r"""
185
"Não gosto!" - Por quê? - "porque não me sinto a sua altura".
E que homem respondeu assim alguma vez?

Nietzsche, F. Além do bem e do mal, 1886
"""

# Definindo variáveis de ambiente do Python
os.environ['PYTHONIOENCODING'] = 'UTF-8'
# Assegurando que o jogo inicie no centro da tela
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
os.environ['SDL_VIDEO_CENTERED'] = '1'

sys.path.insert(0, '')

try:
    import psutil
except (ImportError):
    pass

# Título e versão do jogo
TITLE, __version__ = "CellAs", "6.12.2018a"

# Garantindo a codificação utf-8 no terminal do windows
if os.name == "nt":
    os.system("@echo off > nul")
    os.system("chcp 65001 > nul")
    os.system("set PYTHONIOENCODING=UTF-8")
    os.system("cls")
else:
    os.system('clear')

# Diretório da aplicação -retirando a pasta /lib
APP_DIR = os.path.dirname(os.path.abspath(__file__))[:-4]

def path_join(*args):
    r"""
    Relativo à informação acerca do diretório em execução

    * Args:
        args (str): O nome do arquivo.

    Returns:
        str: Retorna o caminho absoluto do arquivo.
    """
    return os.path.join(APP_DIR, *args)


# Carregando o arquivo de configuração do usuário
with open(path_join('config.json'), 'r', encoding="UTF-8") as file:
    USER_CONFIG = json.loads(file.read())


# Sobre as configurações em si e por si
WH_SUPPORTED = {0: [800, 600], 1: [1024, 768]}
#WIDTH = WH_SUPPORTED[USER_CONFIG['window']['size']][0]
#HEIGHT = WH_SUPPORTED[USER_CONFIG['window']['size']][1]
WIDTH = 800
HEIGHT = 600
FPS = USER_CONFIG['fps']
SYS_SHOW = USER_CONFIG['info']

# Linguagem da interface do jogo.
# Caso seja SYS, recupera a linguagem do sistema operativo
LANG = USER_CONFIG['lang'] if USER_CONFIG['lang'] != 'SYS' else locale()[0]

SOUNDS = USER_CONFIG['sounds']
VOLUME = USER_CONFIG['volume']
QUIT_TIME = USER_CONFIG['exit_time'] * 10

# Sobre a conexão com o servidor
HOST = USER_CONFIG['server']['host']
PORT = USER_CONFIG['server']['port']


# Recuperar o id de execução do CellAs
PID = os.getpid()

# Comando padrão para informações acerca do contexto operativo
UNAME = {0: 'os', 1: 'name', 2: 'version'}
for i in range(0, 3):
    UNAME[i] = platform.uname()[i]

# Para o cálculo da média do uso da cpu e do fps
Analyt = Analytics()


def sysinfo(FPS=0):
    r"""
    Método destinado à apresentação concisa acerca do ecossistema em execução.

    Args:
        :FPS: float
    """
    if 'psutil' not in sys.modules:
        return
    # Limpa a saída do terminal
    os.system("clear" if os.name != 'nt' else "cls")

    # Segregando para obter a informação necessária
    UNAME[2] = UNAME[2].split('-')[0]

    # Requisitando o número de núcleos e a porcentagem de uso da unidade lógica
    CPU = {0: psutil.cpu_count(), 1: psutil.cpu_percent()}

    # Requisitando o tamanho total, em bytes, e a porcentagem do uso da memória
    RAM = {0: psutil.virtual_memory()[0] // 1073741824, 1: psutil.virtual_memory()[
        2], 2: psutil.Process(PID).memory_percent()}

    Analyt.add(0, CPU[1])
    Analyt.add(1, FPS)

    # Imprime as informações no terminal
    print(" _    _  ")
    print("((ell//\s")
    print("\t{0}\n\tPID: {1}\n\n".format(__version__, PID))
    print("Pygame {0} no Python {1}".format(
        pg.version.ver, sys.version_info[0],))
    print(u"Executando no {0} de versão {1}.\n".format(UNAME[0], UNAME[2]))
    print(u"{0} possuiu {1} núcleos.".format(UNAME[1], CPU[0]))
    print("Uso da CPU: {}%".format(CPU[1]))
    print("Uso da RAM: {0}% de {1:.0f} GB".format(RAM[1], RAM[0]))
    print(u"{0} está usando {1:.1f}% da RAM\n".format(TITLE, RAM[2]))
    print(u"Diretório da aplicação:", APP_DIR)
    if os.name != "nt":
        print(u"Diretório de execução:", os.environ['PWD'])
    print(u"\nEstatísticas")
    print("CPU: {}%".format(Analyt.media[0]))
    print("FPS: {}".format(Analyt.media[1]))

# Primeira execuçãodo sysinfo
if SYS_SHOW:
    sysinfo()

# Sobre os nomes das máquinas de estado
GAMEPLAY = 'gameplay'
MENU = 'menu'
SCORE = 'score'
END = 'end'
CTRL = 'ctrl'
ABOUT = 'credits'
LOAD = 'load'
CONF = 'config'
QUIT = 'quit'

# Sobre as cores
CORES = {
    "Transparent": (255, 255, 255, 0),
    "Active": pg.Color('lightskyblue3'),
    "Inactive": pg.Color('dodgerblue2'),
    "Background": (36, 123, 160)
}

# Sobre a linguagem do jogo
with open(path_join('data/langs/{0}.json'.format(LANG)), 'r', encoding="UTF-8") as file:
    LANG = json.loads(file.read())