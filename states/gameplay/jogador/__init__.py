# !/usr/bin/python3
# -*- coding: utf-8 -*-

from lib.fsm import *
from lib.config import *
from lib.resources import *

# Importando a matança
from .arsenal import *

import math

__author__ = "Leandro Peres"
__all__ = ['Jogador']

class Jogador(pg.sprite.Sprite):
    r"""
        Classe destinada à personificação do jogador.
    """
    def __init__(self, resources, pos=(WIDTH/2, HEIGHT/2)):
        pg.sprite.Sprite.__init__(self)

        self.resources = resources

        # Atribuindo o Vetor2D do pygame
        self.Vector = pg.math.Vector2
        self.image = self.resources['image']['me']
        self.image = pg.transform.scale(self.image, (70,70))

        # Garente a imagem original, sem mudanças daqui pra frente
        self.originalimage = self.image

        # Posição do jogador no centro da tela
        self.posicao = self.Vector(WIDTH / 2, HEIGHT / 2)

        self.rect = self.image.get_rect(center=self.posicao)
        self.mask = pg.mask.from_surface(self.image)

        self.invencibilidade = False
        self.contador_inv = 445

        # Inicializa a velocidade e a aceleração como Vetor
        # Velocidade inicial: 0
        # Aceleração/Desaceleração constante: -0.085 (A negação garante um movimento certeiro e uma contra partida à velocidade)
        self.velocidade = self.Vector(0, 0)
        self.acceleration = self.Vector(0, -0.085)

        self.angle = 0
        self.acc = False

        self.attributes = {
            'HP': 3,
            'WAVE': 1,
            'SCORE': 0
            }

        self.originalShoot = self.resources['image']['bala']
        self.shootSFX = self.resources['sfx']['shot']

    def update(self):
        # Acima da velocidade permitida?
        if self.velocidade.length() > 5:
            self.velocidade.scale_to_length(5)

        # Garante um jogador visível na janela
        if self.posicao.x > WIDTH:
            self.posicao.x = 0
        elif self.posicao.x <= 0:
            self.posicao.x = WIDTH
        elif self.posicao.y <= 0:
            self.posicao.y = HEIGHT
        elif self.posicao.y > HEIGHT:
            self.posicao.y = 0

        self.posicao += self.velocidade
        self.rect.center = self.posicao

        # Efeito de dano
        if self.invencibilidade:

            if self.contador_inv < 0:
                # Retira a invencibilidade
                self.invencibilidade = False
                self.contador_inv = 445
                # Restaura a imagem padrão
                if not self.acc:
                    self.image = pg.transform.rotate(self.originalimage, -self.angle)
                else:
                    self.image = pg.transform.rotate(self.resources['image']['acc'], -self.angle)

                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pg.mask.from_surface(self.image)
            else:
                if not self.acc:
                    self.image = pg.transform.rotate(self.resources['image']['me_'], -self.angle)
                else:
                    self.image = pg.transform.rotate(self.resources['image']['acc_'], -self.angle)

                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pg.mask.from_surface(self.image)

            self.contador_inv -= 4.5


    def move(self, foward):
        r"""
        Método da movimentação do jogador.

        Args:
            :foward: or bool or str or int: Acelerando ou desacelerando? Restaurar? Rotacionar?
        """
        # Acelerar/Desacelerar
        if type(foward) == bool:
            if foward:
                self.velocidade += self.acceleration
                self.image = pg.transform.rotate(self.resources['image']['acc'], -self.angle)
                self.acc = True
            else:
                self.velocidade -= self.acceleration
                self.image = pg.transform.rotate(self.resources['image']['me'], -self.angle)
                self.acc = False

        # Restaurar
        elif type(foward) == str:
            self.image = pg.transform.rotate(self.resources['image']['me'], -self.angle)
            self.acc = False

        # Rotacionar
        elif type(foward) == int:
            # Adciona ao ângulo
            self.angle += foward

            # E existe ângulo de 361 ou -5?
            self.angle %= 360

            # Rotação da aceleração condizente com a direção do jogador
            self.acceleration.rotate_ip(foward)

            # Reorganiza a imagem, retângulo e máscara
            self.image = pg.transform.rotate(self.originalimage, -self.angle)
            self.mask = pg.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=self.rect.center)

    def atira(self, all, group):
        r"""
        Método para iniciar o disparo.

        Params:
            all: all_spritess
            group: balas
        """
        if not self.invencibilidade:
            # Caso as configurações permitem,
            # Setar o volume e dar play
            if SOUNDS:
                a = pg.mixer.Sound(self.shootSFX)
                a.set_volume(VOLUME['sfx'])
                pg.mixer.Sound.play(a)

            # Inicializa o tiro
            bala = Bala(self.posicao, self.angle, self.originalShoot)
            group.add(bala)
            all.add(bala)

    def hit(self):
        r"""
        Método para corresponder o dano sofrido.
        """
        self.invencibilidade = True
        self.attributes['HP'] -= 1
