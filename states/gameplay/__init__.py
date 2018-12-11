# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Compatibilizando, na medida do possível, com o Python2
import __future__

import os

# Biblioteca do próprio jogo
from lib.fsm import *
from lib.config import *

# Componentes da jogatina
from .jogador import *
from .rna import *
from .organism import *

# Importando a condição de cliente
import lib.client as client

__author__ = "Leandro Peres"
__all__ = ['Gameplay']

r"""
Trem de Ferro

Café com pão
Café com pão
Café com pão
Virge Maria que foi isto maquinista?
 
Agora sim
Café com pão
Agora sim
Voa, fumaça
Corre, cerca
Ai seu foguista
Bota fogo
Na fornalha
Que eu preciso
Muita força
Muita força
Muita força
 
Oô...
Foge, bicho
Foge, povo
Passa ponte
Passa poste
Passa pasto
Passa boi
Passa boiada
Passa galho
De ingazeira
Debruçada
No riacho
Que vontade
De cantar!
 
Oô...
Quando me prendero
No canaviá
Cada pé de cana
Era um oficiá
 
Oô...
Menina bonita
Do vestido verde
Me dá tua boca
Pra matá minha sede
Oô...
Vou mimbora vou mimbora
Não gosto daqui
Nasci no Sertão
Sou de Ouricuri
Oô...
 
Vou depressa
Vou correndo
Vou na toda
Que só levo
Pouca gente
Pouca gente
Pouca gente... 

Bandeira, M. Antologia Poética. Rio de Janeiro: J.Olympo, 1976, 8. ed. , p. 96.
"""

class Gameplay(BaseState):
    def __init__(self, resources):
        super(Gameplay, self).__init__()
        self.resources = resources

    def startup(self, persist):
        pg.mouse.set_visible(False)

        # Definindo os sprites
        self.player = Jogador(self.resources)
        self.balas = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.RNA = pg.sprite.Group()
        self.anti = pg.sprite.Group()

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.balas)
        self.all_sprites.add(self.RNA)
        self.all_sprites.add(self.anti)

        # Tempo de anúncio da próxima onda
        self.timeToNext = 120

        self.record = False
        self.timeToTry = 0

        client.connect(blocking=False)
        client.Request(1)

        # Imagem do contador de vidas restantes
        self.lifes = pg.transform.scale(self.resources['image']['me'], (40,40))

        self.font = pg.font.Font(self.resources['fonts']['pixelmix'], 19)

    def get_event(self, event):
        # Caso o jogador atire
        if event.type == pg.KEYDOWN and event.key == USER_CONFIG['controls']['shoot']:
            self.player.atira(self.all_sprites, self.balas)

        # Caso o jogador deixe de acelerar
        if event.type == pg.KEYUP and event.key == USER_CONFIG['controls']['accelerate']:
            self.player.move('restore')

        # Para testes
        if event.type == pg.KEYDOWN and event.key == pg.K_e:
            self.persist['SCORE'] = int(self.player.attributes['SCORE'])
            self.next_state = END
            self.done = True

    def update(self, dt):
        # Checa se o jogador perdeu todas as vidas disponíveis
        if self.player.attributes['HP'] < 0:
            self.persist['SCORE'] = int(self.player.attributes['SCORE'])
            self.next_state = END
            self.done = True

        # Movimentação do personagem
        keys = pg.key.get_pressed()
        if keys[USER_CONFIG['controls']['left']]:
            self.player.move(-4)
        if keys[USER_CONFIG['controls']['right']]:
            self.player.move(4)
        if keys[USER_CONFIG['controls']['accelerate']]:
            self.player.move(True)
        if keys[USER_CONFIG['controls']['decelerate']]:
            self.player.move(False)

        #
        # COLISÃO
        #

        # Colisão entre os sprites do arsenal e rnas
        contato_bala = pg.sprite.groupcollide(self.balas, self.RNA, True, False, pg.sprite.collide_mask)
        if contato_bala:
            for i in contato_bala.items():
                self.player.attributes['SCORE'] += 1 if i[1][0].size != 1 else 10
                i[1][0].divide(self.all_sprites, self.RNA, self.resources['image'], self.player.invencibilidade)

        # Colisão entre os sprites das células do organismo e os corpos estranhos, RNAs.
        contato_rna = pg.sprite.groupcollide(self.anti, self.RNA, False, False, pg.sprite.collide_mask)
        if contato_rna:
            for i in contato_rna:
                self.player.attributes['SCORE'] -= 5 if self.player.attributes['SCORE'] >= 5 else 0
                make_rnas(self.all_sprites, self.RNA, self.player.rect, self.resources['image'], pos=i.injuried(), total=1, size=1)

        # Colisão entre o jogador e os RNAs
        contato = pg.sprite.spritecollide(self.player, self.RNA, False, pg.sprite.collide_mask)
        if contato:
            if not self.player.invencibilidade:
                self.player.hit()
            else:
                contato[0].divide(self.all_sprites, self.RNA, self.resources['image'], self.player.invencibilidade)

        # Requisitando a maior pontuação registrada
        if not self.record:
            request = client.Get(blocking=False)
            if request:
                self.record = int(request[0]['score'])

    def draw(self, surface):
        surface.blit( self.resources['image']['gamepray'], (0,0) )

        # Atualizando e desenhando os sprites
        self.all_sprites.update()
        self.all_sprites.draw(surface)

        # HUD
        for i in range(self.player.attributes['HP']):
            rect = self.lifes.get_rect()
            rect.center = (rect.width + 70 * i, rect.height)
            surface.blit(self.lifes, rect)

        # Mostragem do total de pontos acumulados
        sc = self.font.render(LANG[GAMEPLAY][1].format(self.player.attributes['SCORE']), True, pg.Color("white"))
        surface.blit(sc, (WIDTH - (WIDTH * 0.15) - sc.get_rect().width // 2.525, sc.get_rect().h))

        if self.record not in [None, False] and self.player.attributes['SCORE'] > self.record:
            sc = self.font.render(LANG[GAMEPLAY][-1], True, pg.Color("white"))
            surface.blit(sc, (WIDTH - (WIDTH * 0.15) - sc.get_rect().width // 2.525, sc.get_rect().h*2))

        # Anúncio da onda atual
        if len(self.RNA) == 0 and self.timeToNext > 0:
            # Caso há mudança
            sc = self.font.render(LANG[GAMEPLAY][0].format(self.player.attributes['WAVE']), True, pg.Color("white"))
            surface.blit(sc, (WIDTH // 2 - sc.get_rect().w, sc.get_rect().h ))
            self.timeToNext -= 1
        elif self.timeToNext == 0:
            # Caso o tempo de anúncio se esvai
            make_rnas(self.all_sprites, self.RNA, self.player.rect, self.resources['image'], total=self.player.attributes['WAVE'])
            make_anti(self.all_sprites, self.anti, self.resources['image'])
            self.player.attributes['WAVE'] += 1
            self.timeToNext = 120