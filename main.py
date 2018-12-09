# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

# Máquina de estados finitos
from lib.fsm import GameMain

# Estados de máquina
from states import *

r"""
O medo do sangue tende a criar medo para carne.

Introdução de Silent Hill. 1999
"""

# Informações gerais acerca da aplicação
__authors__ = ["Leandro de Gonzaga Peres",
                "Dyego Marques Souza Costa",
                "Victoria Costa Oliveira"]
__url__ = 'https://github.com/SOHNE/CellAs'

# Caso o arquivo main.py seja executado como
# um arquivo a interpretar e não como um módulo
if __name__ == "__main__":
    # Instanciando o loop central do jogo
    game = GameMain(screen, environments)
    game.run()

    # Saindo do programa sem mensagens
    pg.quit()
    sys.exit(0)