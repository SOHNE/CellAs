# !/usr/bin/python3
# -*- coding: utf-8 -*-

from lib.fsm import *
from lib.config import *
from lib.resources import *

# Importando a matança
from .arsenal import *

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
        self.posicao = self.Vector(WIDTH // 2, HEIGHT // 2)

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

        self.attributes = {
            'HP': 3,
            'WAVE': 1,
            'SCORE': 0
            }

        self.originalShoot = self.resources['image']['bala']
        self.shootSFX = self.resources['sfx']['shot']

    def update(self):
        # Garante um jogador visível na janela
        if self.posicao.x > WIDTH:
            self.posicao.x = 0
        elif self.posicao.x <= 0:
            self.posicao.x = WIDTH
        elif self.posicao.y <= 0:
            self.posicao.y = HEIGHT
        elif self.posicao.y > HEIGHT:
            self.posicao.y = 0

        # Acima da velocidade permitida?
        if self.velocidade.length() > 5:
            self.velocidade.scale_to_length(5)

        self.posicao += self.velocidade
        self.rect.center = self.posicao

        # Efeito de blink
        if self.invencibilidade:
            self.contador_inv -= 2.25

            if self.contador_inv < 0:
                self.invencibilidade = False
                self.contador_inv = 445


            # Efeito de transparência alternada
            for _ in range(40):
                if self.contador_inv <= _ * 35 and self.contador_inv > (_ - 1) * 35 and _ % 2 == 0:
                    self.image.fill(CORES['Transparent'])
                    break
                else:
                    self.image = pg.transform.rotate(self.originalimage, -self.angle)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    self.mask = pg.mask.from_surface(self.image)


    def rotate(self, graus):
        r"""
        Método para rotacionar o jogador.

        Params:
            graus: int: Grau a ser adicionado
        """
        # Rotação condizente com o jogador
        self.acceleration.rotate_ip(graus)

        self.angle += graus

        # E existe ângulo de 361 ou -5?
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        # Reorganiza a imagem, retângulo e máscara
        self.image = pg.transform.rotate(self.originalimage, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def atira(self, all, group):
        r"""
        Método para iniciar o disparo.

        Params:
            all: all_spritess
            group: balas
        """
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
        if not self.invencibilidade:
            self.invencibilidade = True
            self.attributes['HP'] -= 1
            # Reseta as condições físicas do jogador
            self.velocidade = self.Vector(0, 0)
            self.acceleration = self.Vector(0, -0.085)
            self.posicao = self.Vector(WIDTH / 2, HEIGHT / 2)
            self.angle = 0