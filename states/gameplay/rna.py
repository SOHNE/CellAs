# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from lib.fsm import *
from lib.config import *

# Notações matemáticas
import math
import random

__author__ = "Leandro Peres"
__all__ = ['RNA', 'random_rnas', 'make_rnas', 'safe_zone']

class RNA(pg.sprite.Sprite):

    def __init__(self, pos, size, resources):
        r"""
        Classe destinada inteiramente aos corpos estranhos.

        Args:
            :pos: tuple: Identificador da posição
            :size: int: Identificador do tamanho do RNA
            :resources: dict: Arquivos audivisuais carregados pelo sistema
        """
        pg.sprite.Sprite.__init__(self)

        # Acerca do tamanho da célula
        self.size = size

        # Acerca do sprite
        self.image = resources[str(self.size)]
        
        # Instancia a máscara para a colisão
        self.mask = pg.mask.from_surface(self.image)

        # Sobre o retângulo da imagem
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        # Instancia a velocidade da célula
        self.speed = random.randint(1,2)

        # Posição randômica
        temp_pos = self.rand_pos()
        while temp_pos[0] == 0 and temp_pos[0] == 0:
            temp_pos = self.rand_pos()

        self.direction = temp_pos

    def update(self):
        # Controle de posição em tela
        if self.rect.x >= WIDTH:
            self.rect.x = 0
        elif self.rect.x <= 0:
            self.rect.x = WIDTH
        elif self.rect.y <= 0:
            self.rect.y = HEIGHT
        elif self.rect.y >= HEIGHT:
            self.rect.y = 0

        # Acerca da movimentação da célula
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]


    def divide(self, all, group, resources, player):
        r"""
        Método para divisão das células.

        Args:
            :all: list: Grupo geral de sprites
            :group: list: Grupo local de sprites
            :resources: dict: Arquivos audiovisuais carregados pelo sistema
        """
        self.kill()
        temp = []
        pos = 5
        if self.size > 0:
            __ = random.randint(1,2 if not player else random.randint(3,4))
            for _ in range(__):
                temp.append(RNA((self.rect.x + pos, self.rect.y + pos), self.size - 1, resources))
                pos += 5

        all.add(*temp)
        group.add(*temp)

    def rand_pos(self):
        r"""
        Método para geração randômica da posição
        """

        if random.choice([True, False]):
            rand_x = self.speed + (random.random() * - random.choice([2,4]))
        else:
            rand_x = self.speed + random.random()

        if random.choice([False, True]):
            rand_y = self.speed + random.random()
        else:
            rand_y = self.speed + (random.random() * - random.choice([1,3,5]))

        # Formata o ponto flutuante. Afinal, 10 casas decimais é demasiadamente desnecessário
        rand_x = float("{:.3f}".format(rand_x))
        rand_y = float("{:.3f}".format(rand_y))

        return [rand_x, rand_y]

def safe_zone(position, player):
    r"""
    Método que calcula distância entre o jogador e os RNA's, a distância entre dois pontos dados.
    Prevenindo, assim, a criação de inimigos na exata ou
    aproximada localização do jogador.
    sqrt(  (x1 - y1)^2 + (x2 - y2)^2  )

    Args:
        :position: tuple: Posição do RNA
        :player: tuple: Posição do jogador

    Returns:
        :bool:
    """
    return math.sqrt( (position[0] - player[0]) ** 2 + (position[1] - player[1]) ** 2 ) < 180

def random_rnas():
    r"""
    Geração randômica da posição dos RNAs
    """
    return (random.randint(0, WIDTH), random.randint(0, HEIGHT))

def make_rnas(all, group, player, resources, total=1, pos=False, size=2):
    r"""
    Método destinado para criação dos RNAs.

    Args:
        :all: list: Grupo geral de sprites
        :group: list: Grupo local de sprites
        :player: tuple: Posição do jogador
        :resources: dict: Arquivos audiovisuais carregados pelo sistema
        :total: int: Total de RNAs a serem gerados
        :pos: tuple: Posição do RNA
        :size: int: Tamanho do RNA
    """
    total = int(total)
    for i in range(total):
        position = random_rnas() if not pos else pos

        # Recalcula a posição enquanto a distância da posição das células em relação ao jogador for menor que 175.525
        while safe_zone(position, player):
            position = random_rnas()

        # Instância a célula
        temp_rna = RNA(position, size, resources)

        # Pari as células
        all.add(temp_rna)
        group.add(temp_rna)
