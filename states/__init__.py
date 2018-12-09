# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Componentes aqui presentes que podem
# ser importados pelo 'import *'
__all__ = ['pg', 'screen', 'environments']

# Variáveis de configurações, além de acessos principais
from lib.config import *

# Carregador dos dados audiovisuais, todos os recursos do jogo
import lib.resources as resources

# Importando os estados de máquina
from .menu import Menu
from .gameplay import Gameplay
from .end import End
from .score import Score

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Precavendo o atraso do audio
pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()

# Dicionário com todos os recursos de /data devidamente carregados
# ou com o seu absoluto caminho absoluto
resources = {
    'fonts': resources.load_all_fonts('data/fonts'),
    'image': resources.load_all_gfx('data/image', ignore=['bg.png', 'trab.png', 'bg.jpg']),
    'music': resources.load_all_music('data/audio/music'),
    'sfx': resources.load_all_sfx('data/audio/sfx')
}

# Definindo o ícone da janela
pg.display.set_icon(resources['image']['icon'])

r'''
Atribuindo os estados de máquina
Lista de 2 elementos.
[0] = Estado inicial. O primeiro a ser executado.
[1] = Dicionário com os estados de máquina a serem usados:
MENU - Menu principal,
SCORE - Lista das pontuações dos jogadores,
GAMEPLAY - Jogatina em si e por si,
END - Tela final do jogo,
CRTL - Listagens dos controles permissivos.
'''
environments = [MENU, {
    MENU: Menu(resources),
    SCORE: Score(resources),
    GAMEPLAY: Gameplay(resources),
    END: End(resources)
}]
