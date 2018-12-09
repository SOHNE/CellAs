# !/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Leandro Peres"
__all__ = ['Analytics']

class Analytics(object):
    r"""
    Classe destinada às estatísticas de execução.
    Retorna a média do uso da CPU, em porcentagem, e
    a média de quadros gerados.
    """
    def __init__(self):
        # Inicializa o dicionário
        # ID: [SOMA, NÚMERO_TOTAL]
        self.all = {
            0: [0, 0],
            1: [0, 0]
            }

    def add(self, id, n):
        r"""
        Adiciona o valor no dicionário self.all.
            :param id: Identificação. 0 - CPU; 1 - FPS
            :param n: Valor atual
        """
        if n != 0:
            self.all[id][0] += int(n)
            self.all[id][1] += 1

    @property
    def media(self):
        r"""
        Propriedade acerca do cálculo da média.
        """
        try:
            cpu = self.all[0][0] // self.all[0][1]
            fps = self.all[1][0] // self.all[1][1]
            return (cpu, fps)
        except (ZeroDivisionError):
            return (0, 0)