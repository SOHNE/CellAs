# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from lib.fsm import *
from lib.config import *

__author__ = "Leandro Peres"

class Bala(pg.sprite.Sprite):
    r"""
        Classe destinada ao arsenal disposto ao jogador.
    """
    def __init__(self, pos, angle, image):
        pg.sprite.Sprite.__init__(self)
        Vector = pg.math.Vector2

        # Inicializa o vetor de velocidade
        self.velocidade = Vector(0, -18)
        # Rotaciona a 'rota' da velocidade
        self.velocidade.rotate_ip(angle)

        self.image = image

        # Adequa a imagem com a rotação do jogador
        self.image = pg.transform.rotate(self.image, -angle)

        # Similariza a posição da bala com o player
        self.posicao = Vector(pos)

        self.rect = self.image.get_rect()

        # Colisão Pixel Perfect
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        r"""
            Método relacionado a cada atualização de frame
        """
        # Aplica a velocidade na posição
        self.posicao += self.velocidade
        # Aplica ao retângulo
        self.rect.center = self.posicao

        # Controle da existência do tiro
        if self.rect.x > WIDTH + 200:
            self.kill()
        elif self.rect.x <= -200:
            self.kill()
        elif self.rect.y <= -200:
            self.kill()
        elif self.rect.y > HEIGHT + 200:
            self.kill()
