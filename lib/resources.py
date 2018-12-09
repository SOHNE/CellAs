# !/usr/bin/python3
# -*- coding: utf-8 -*-

# Código adaptado de https://github.com/justinmeister/Mario-Level-1

from .config import *

__all__ = ['load_all_gfx', 'load_all_sfx', 'load_all_music', 'load_all_fonts']

r"""
Copiar não é roubar.
O roubo tira sem somar.
Cópia trás um algo a mais,
O que era um serão dois.

Copiar não é roubar.
Se eu copio, você ainda tem.
Cada qual fica com um.
Ninguém ficará sem nenhum.

Copy Is not Theaft
"""

# Seu funcionamento é dado pos uma lista dos
# arquivos disponíveis do diretótio /data (definido no main.py)
# Deste modo, carrega os sprites (conjuntamento com o método pygame.image.load),
# acerca dos efeitos sonoros e músicas, idem,
# para o restante, retorna o caminho absoluto do arquivo

def load_all_gfx(directory, colorkey=(255,255,255), accept=('.png', '.jpg', '.jpeg','.bmp'), ignore=[]):
    graphics = {}
    directory = path_join(directory)
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(path_join(directory, pic)).convert()
            if pic not in ignore:
                img.set_colorkey(img.get_at((0,0)))
            graphics[name]=img
    return graphics

def load_all_sfx(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    effects = {}
    directory = path_join(directory)
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(path_join(directory, fx))
    return effects

def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    directory = path_join(directory)
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = path_join(directory, song)
    return songs

def load_all_fonts(directory, accept=('.ttf', '.otf')):
    directory = path_join(directory)
    return load_all_music(directory, accept)

