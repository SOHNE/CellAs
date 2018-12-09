# !/usr/bin/python3
# -*- coding: utf-8 -*-
import __future__
import os
from lib.config import *
from lib.fsm import *
from lib.resources import *

__author__ = "Leandro Peres"
__all__ = ['Menu']

class Menu(BaseState):
    r"""
    Classe sobre máquina de estado dedicada ao menu inicial do jogo.
    """

    def __init__(self, resources):
        r"""
        Executado na primeira inicialização da classe. No caso, em main.py
        """
        super(Menu, self).__init__()
        self.music = resources['music']
        self.sfx = resources['sfx']
        self.image = resources['image']
        self.all_fonts = resources['fonts']

        # Caso a configuração permita sons,
        if SOUNDS:
            # Definir o volume da música
            pg.mixer.music.set_volume(VOLUME['music'])
            # Carregar o arquivo de música
            pg.mixer.music.load(self.music['menu'])
            # Tocar indefinitivamente
            pg.mixer.music.play(-1)

        # Itens centrais do menu
        # ID: [DISPLAY, STATE_NAME, PG_SURFACE, PG_RECT]
        # DISPLAY - Caracteres a serem mostrados
        # STATE_NAME - Nome do estado de máquina
        # PG_SURFACE - Render da fonte introduzido no for range(len(self.items))
        # PG_RECT - retângulo do objeto. setado no for range(len(self.items))
        self.items = {
            0: [LANG[MENU][0], GAMEPLAY],
            1: [LANG[MENU][1], SCORE],
            2: [LANG[MENU][4], QUIT]
        }

        # Insere o surface e o rect em self.items
        for i in range(len(self.items)):
            current = self.font.render(self.items[i][0], True, (255,255,255))
            self.items[i].append(current)
            self.items[i].append(current.get_rect())

        # Fontes centrais
        self.titleFont = pg.font.Font(self.all_fonts['ROBOTECH GP'], 102)
        self.titleFont = self.titleFont.render(TITLE, True, (204,0,0))

        self.bg = self.image['bg']
        self.bg = pg.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.bgRect = self.bg.get_rect()
        self.bgRect.x, self.bgRect.y = 0, 0

        # Inicialmente, contabiliza o primeiro
        self.selected = 0

    def startup(self, persist):
        r"""
        Executado na primeira inicialização do estado

        Args:
            :persist: dict
             Dicionário compartilhado entre os estados de máquina
        """
        pg.mouse.set_visible(True)

    def get_event(self, event):
        # Movimentação do seletor do menu pelo teclado
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_UP, pg.K_LEFT]:
                self.selected -= 1
                if SOUNDS:
                    a = pg.mixer.Sound(self.sfx['misc'])
                    a.set_volume(VOLUME['sfx'])
                    pg.mixer.Sound.play(a)
                    
            elif event.key in [pg.K_DOWN, pg.K_RIGHT]:
                self.selected += 1
                if SOUNDS:
                    a = pg.mixer.Sound(self.sfx['misc'])
                    a.set_volume(VOLUME['sfx'])
                    pg.mixer.Sound.play(a)

            # Validar a seleção do menu e corresponder á máquina de estado
            if event.key == pg.K_RETURN:
                if self.items[self.selected][1] == QUIT:
                    self.quit = True
                else:
                    self.next_state = self.items[self.selected][1]
                    self.done = True


    def update(self, dt):
        # Ajusta a seleção, caso saia do espectro
        if self.selected < 0:
            self.selected = list(self.items.keys())[-1]
        elif self.selected > list(self.items.keys())[-1]:
            self.selected = 0

                

    def draw(self, surface):
        surface.fill( CORES['Background'] )
        surface.blit(self.bg, self.bgRect)

        # Posição |y do primeiro elemento do menu
        desloca = HEIGHT - (HEIGHT * .3125)

        # Configurar o objeto para cada elemento na lista de items do dicionário self.items
        for i in self.items.items():
            # Ajusta a posição do retângulo
            i[1][-1].x = WIDTH - (WIDTH * .225)
            i[1][-1].y = desloca

            # Se movimentado pelo mouse
            if i[1][-1].collidepoint(pg.mouse.get_pos()):
                self.selected = i[0]
                self.is_selectable = True

                # Caso selecionado
                if pg.mouse.get_pressed()[0] == 1 and self.is_selectable:
                    self.next_state = self.items[self.selected][1]
                    self.done = True
            else:
                # Previne a mudança de estado se o jogador clicar com o mouse fora do menu
                self.is_selectable = False

            # Evidencia o selecionado
            if i[0] == self.selected:
                i[1][-2] = self.font.render(self.items[i[0]][0], True, (255, 22, 84) )
            else:
                i[1][-2] = self.font.render(self.items[i[0]][0], True, pg.Color("white"))

            surface.blit(i[1][-2], i[1][-1]) # i[superfície], i[rect]
            desloca += 50

        surface.blit(self.titleFont, ( (WIDTH/2), (HEIGHT/2) - self.titleFont.get_rect().h ) )
