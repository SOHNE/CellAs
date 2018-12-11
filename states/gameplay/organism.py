# !/usr/bin/python3
# -*- coding: utf-8 -*-
from lib.config import *

import random

__author__ = "Leandro Peres"
__all__ = ['Anticorps', 'make_anti']

r"""
A meu pai depois de morto

Podre meu Pai! A morte o olhar lhe vidra.
Em seus lábios que os meus lábios osculam
Micro-organismos fúnebres pululam
Numa fermentação gorda de cidra.

Duras leis as que os homens e a hórrida hidra
A uma só lei biológica vinculam,
E a marcha das moléculas regulam,
Com a invariabilidade da clepsidra!...

Podre meu Pai! E a mão que enchi de beijos
Roída toda de bichos, como os queijos
Sobre a mesa de orgíacos festins!...

Amo meu Pai na atômica desordem
Entre as bocas necrófagas que o mordem
E a terra infecta que lhe cobre os rins!

ANJOS, A. Eu e Outras Poesias. Rio de Janeiro: Civilização Brasileira, 1998.
"""

class Anticorps(pg.sprite.Sprite):

    def __init__(self, resources):
        r"""
        Classe destinada aos anticorpos, dito como células
        saudáveis que integram o próprio organismo.

        Args:
            :resources: dict: Recursos carregados pelo sistema
        """
        pg.sprite.Sprite.__init__(self)

        self.resources = resources
        
        self.image = self.resources['cell']
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.mask = pg.mask.from_surface(self.image)

    def injuried(self):
        r"""
        Caso a célula do organismo sofra dano por parte dos RNAs
        """
        self.kill()
        return self.rect.x, self.rect.y

def make_anti(all, group, resources):
    r"""
    Método para a criação das células saudáveis.

    Args:
        :all: list: Grupo geral de sprites
        :group: list: Grupo local de sprites
        :resources: dict: Arquivos audiovisuais carregados pelo sistema
    """
    temp = Anticorps(resources)
    group.add(temp)
    all.add(temp)