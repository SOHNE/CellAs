# !/usr/bin/python3
# -*- coding: utf-8 -*-
import __future__
import os
import sys
import platform
import time
import datetime
try:
    import psutil
except (ImportError):
    print(u"!! Este servidor requere o módulo 'psutil'.\nInstale-o por 'pip install -r requeriments' !!")
    sys.exit(0)

__author__ = "Leandro Peres"
__all__ = ['path_join', 'sysinfo']

APP_DIR = os.path.dirname(os.path.abspath(__file__))
TITLE, __version__ = 'CellAs server', '3.12.2018a'

NOW = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H.%M.%S')

def path_join(*args):
    r"""
        Relativo à informação acerca do diretório em execução

        * Args:
            args (str): O nome do arquivo.

        Returns:
            str: Retorna o caminho absoluto do arquivo.
    """
    return os.path.join(APP_DIR, *args)


# Recuperar o id de execução do CellAs
PID = os.getpid()

# Comando padrão para informações acerca do contexto operativo
UNAME = {0: 'os', 1: 'name', 2: 'version'}
for i in range(0, 3):
    UNAME[i] = platform.uname()[i]

def sysinfo():
    r"""
    Relativo à informação acerca do ecosistema em execução

    prints:
        str: Kernel name / Kernel version
        str: Machine name / CPU cores

        str: CPU usage in %
        str: RAM usage in %
    """
    # Limpa a saída do terminal
    os.system("clear" if os.name != 'nt' else "cls")

    # Segregando para obter a informação necessária
    UNAME[2] = UNAME[2].split('-')[0]

    # Requisitando o número de núcleos e a porcentagem de uso da unidade lógica
    CPU = {0: psutil.cpu_count(), 1: psutil.cpu_percent()}

    # Requisitando o tamanho total, em bytes, e a porcentagem do uso da memória
    RAM = {0: psutil.virtual_memory()[0] // 1073741824, 1: psutil.virtual_memory()[
        2], 2: psutil.Process(PID).memory_percent()}

    # Imprime as informações no terminal
    print(" _    _  ")
    print("((ell//\server")
    print("\t{0}\n\tPID: {1}".format(__version__, PID))
    print("=" * 17)
    print("Python {}".format(sys.version_info[0]))
    print(u"Executando no {0} de versão {1}.\n".format(UNAME[0], UNAME[2]))
    print(u"{0} possuiu {1} núcleos.".format(UNAME[1], CPU[0]))
    print("Uso da CPU: {}%".format(CPU[1]))
    print("Uso da RAM: {0}% de {1:.0f} GB".format(RAM[1], RAM[0]))
    print(u"{0} está usando {1:.1f}% da RAM\n".format(TITLE, RAM[2]))
    print(u"Diretório da aplicação:", APP_DIR)
    print(u"Diretório de execução:", os.environ['PWD'] if 'PWD' in os.environ else "?", end='\n')
