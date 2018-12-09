# !/usr/bin/python3
# -*- coding: utf-8 -*-
import __future__
from lib.fsm import *
from lib.config import *

# Importando a condição de cliente
import lib.client as client

__author__ = "Leandro Peres"
__all__ = ['Score']

r"""
Espécie de balada da moça de Goiatuba

Em Goiatuba
tem uma moça
que coração
grande ela tem
Em Goiatuba
tem uma moça
que coração
grande ela tem.

A moça de lá
é só chamar vem

De Goiatuba
eu guardo
muitas recordações

De lá eu guardo
muitas recordações

Lá tem rua
que parece bicho
querendo se esconder
por detrás do mato

Lá tem homem
que lutou na revolução

Lá tem farmacêutico
que sabe latim

Lá tem padre que mora
com mulher na rua de cima
e de tarde sobe de lanterna na mão
Lá tem cadeia
assombrada
e tem louco nas grades rindo feito
bicho com fome
Em Goiatuba
tem uma moça
que coração bom ela tem
A moça de lá
desde menina
serve aos homens
com sabedoria
Toda moça no mundo
aprende que corpo
não se pode mostrar
vestido deve vestir
vergonha deve sentir
amor deve esconder
sonho pode sonhar
A moça de lá
não aprendeu a sonhar
A moça de Goiatuba
é como a fonte
que dá de beber
é como a árvore
que dá frutos
é como a noite
que dá as estrelas
Ela só não compreende porque os homens
têm coisa com ela
Um dia indagou:
— “Por que ocêis me mandam
deitar no chão?”
— “Eu visto meu vestido,
eu ponho colar bonito,
eu enfeito os meus cabelos
com flor
Eu estou bonita
com o meu vestido
eu estou bonita
com esta flor
vocês me mandam tirar vestido,
ocês são bobos?”
Lá em Goiatuba
tem uma moça
que coração grande ela tem.
A moça de lá
é só chamar vem.

José Godoy Garcia 
"""

class Score(BaseState):
    def __init__(self, resources):
        super(Score, self).__init__()
        self.items = {
            0: [LANG[SCORE][2], MENU]
        }
        self.resources = resources

    def startup(self, persist):
        self.rank = None

        self.no_con = 5

        # Cabeçalho
        self.cabecalho = ['', LANG[SCORE][0], LANG[SCORE][1]]
        # Posição do eixo Y (|)
        self.hy = 115

        self.selected = 0

        # Tempo para reconectar
        self.timeToTry = 0

        # Itens do menu
        for i in range(len(self.items)):
            current = self.font.render(self.items[i][0], True, (255,255,255))
            self.items[i].append(current)
            self.items[i].append(current.get_rect())

        if client.connect():
            client.Request(12)

    def update(self, dt):
        if self.selected < 0:
            self.selected = list(self.items.keys())[-1]
        elif self.selected > list(self.items.keys())[-1]:
            self.selected = 0

    def draw(self, surface):
        surface.blit(self.resources['image']['score'], (0,0))
        # Requisitando o rank
        # É necessário que seja neste método para
        # previnir interpolação de pedidos junto ao server

        # cabeçalho da tabela
        a = pg.font.SysFont("arial", 16).render(self.cabecalho[0] + ' ', True, pg.Color('white'))
        surface.blit(a, (120 - a.get_width(), self.hy - 60)) 

        a = pg.font.SysFont("arial", 16).render(self.cabecalho[1], True, pg.Color('white'))
        surface.blit(a, (128, self.hy - 60))

        a = pg.font.SysFont("arial", 16).render(self.cabecalho[2], True, pg.Color('white'))
        surface.blit(a,(WIDTH - 128 - a.get_width(), self.hy - 60))

        
        if self.rank is not None:
            for i in range(len(self.rank)):
                self.no_con = 5
                if i < 3: # os topzera
                    color = pg.Color('green')
                else:
                    color = pg.Color('white')
                number = pg.font.SysFont("arial", 16).render('', True, color)
                name = pg.font.SysFont("arial", 16).render(self.rank[i]['name'], True, color)
                score = pg.font.SysFont("arial", 16).render(str(self.rank[i]['score']), True, color)
                surface.blit(number, (128 - number.get_width(), self.hy + number.get_height() + 28 * i))
                surface.blit(name,(128, self.hy + name.get_height() + 28 * i))
                surface.blit(score, (WIDTH - score.get_width() - 128, self.hy + score.get_height() + 28 * i))
        else:
            if self.no_con <= 0:
                no = pg.font.SysFont("arial", 16).render(LANG["system"][2], True, (255,255,255))
                surface.blit(no, ((WIDTH / 2) - no.get_rect().w, (HEIGHT/ 2) - no.get_rect().h))
            else:
                self.no_con -= 1

        
            self.rank = client.Get()

        # Posição |y do primeiro elemento
        desloca = HEIGHT - 50

	    # Voltar
        for i in self.items.items():

            rect = i[1][-1]
            rect.center = ((WIDTH//2) - rect.width, desloca)
            i[1][-2] = rect

            # Se movimentado pelo mouse
            if i[1][-2].collidepoint(pg.mouse.get_pos()):
                self.selected = i[0]
                self.is_selectable = True
                if pg.mouse.get_pressed()[0] == 1 and self.is_selectable:
                    self.next_state = self.items[self.selected][1]
                    self.done = True


            if i[0] == self.selected:
                i[1][-2] = self.font.render(self.items[i[0]][0], True, pg.Color("red"))

            surface.blit(i[1][-2], i[1][-1])
            desloca += 50


    def get_event(self, event):
        # Movimentação do seletor do menu pelo teclado
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                self.next_state = SCORE
                self.done = True
            if event.key == pg.K_RETURN:
                self.next_state = self.items[self.selected][1]
                self.done = True