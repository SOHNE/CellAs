# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Código disponível originalmente em:
# https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame/46390412#46390412
# Acesso: 27 de Novembro de 2018
# Código adaptado

from .config import *

__all__ = ['InputBox']

class InputBox(object):
    r"""
    Cria uma caixa de texto capaz de armazenar o texto inserido pelo jogador.

    Args:
        :x: int: Posição no eixo x (-)
        :y: int: Posição no eixo y (|)
        :w: int: Largura do elemento em pixels
        :h: int: Altura do elemento em pixels
        :text: str: Texto inicial do elemento 
        :active: bool: Ativado assim que o elemento for criado?
        :font: str: Caminho absoluto da fonte a ser utilizada
    """

    def __init__(self, x, y, w, h, text='', active=False, font=None):
        self.font = pg.font.Font(font, 22)
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.placeHolder = text
        self.active = active
        if not self.active:
            self.color = CORES['Active']
        else:
            self.color = CORES['Inactive']
        self.txt_surface = self.font.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = CORES['Active'] if self.active else CORES['Inactive']
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN and self.text != self.placeHolder:
                    return self.text
                elif self.text != self.placeHolder and event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    if self.text == "":
                        self.text = self.placeHolder
                elif event.key not in [pg.K_ESCAPE, pg.K_BACKSPACE, pg.K_RETURN, pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT] and (len(self.text) <= 10 or self.text == self.placeHolder):
                    if self.text == self.placeHolder:
                        self.text = ""
                    self.text += event.unicode
                # Re-render the text.
                try:
                    self.txt_surface = self.font.render(self.text, True, self.color)
                except:
                    pass
        self.update()

    def update(self):
        # Resize the box if the text is too long.
        #width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = 200

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)