# !/usr/bin/python3
# -*- coding: utf-8 -*-

# This code is licensed as CC0 1.0
# (https://creativecommons.org/publicdomain/zero/1.0/legalcode)

# Code disponível originalmente em https://gist.github.com/iminurnamez/8d51f5b40032f106a847
import __future__
import pygame as pg
from . import config

__all__ = ['GameMain', 'BaseState']

r"""
Duas coisas povoam a mente com uma admiração e respeito sempre novos e crescentes...
o céu estrelado por cima e a lei moral dentro de nós.

Kant, I. A Metafísica dos Costumes, 1797
"""

class GameMain(object):
    def __init__(self, screen, states):
        r"""
        Esta classe é responsável pelo gerenciando do
        estado de jogo ativo e o mantêm atualizado.
        Também lida com gerenciando de eventos, filas de execução,
        framerate, atualizando a exibição do estado ativo, ...).
        Possuiu o loop central do jogo.

        Args:
            :screen: object: Objeto de display do pygame
            :states: dict: Um dicionário contendo todos os estados de máquina
        """
        # Sobre a máquina de estado
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = config.FPS
        self.states = states[1]
        self.state_name = states[0]
        self.state = self.states[self.state_name]
        # Tempo de ativação da tecla ESCAPE para sair do jogo
        self.QUIT_TIME = config.QUIT_TIME
        # Tempo entre uma atualização das informações
        self.SHOW = 120
        # Caso o jogo esteja pausado
        self.paused = False

    def event_loop(self):
        r"""
        Lidando com os eventos do pygame e os passando para o estado
        de máquina em execução.
        """
        for event in pg.event.get():
            # Quer sair sem importunação? Pois saia!
            if event.type == pg.QUIT:
                self.done = True
                config.sys.exit(0)

            if not self.paused:
                # Método do estado
                self.state.get_event(event)

            # Altera o título da janela
            if event.type == pg.KEYDOWN:
                # Caso o jogador pressione a tecla de informação do sistema
                if event.key == config.USER_CONFIG['controls']['sys_show']:
                    config.SYS_SHOW = not config.SYS_SHOW
                    config.sysinfo(self.clock.tick(self.fps))

                # Caso o jogador pressione a tecla de pause
                if event.key == config.USER_CONFIG['controls']['pause'] and self.state_name == config.GAMEPLAY:
                    self.paused = not self.paused
                    if self.paused:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()

            # Altera o cronômetro int self.QUIT_TIME
            elif event.type == pg.KEYUP and event.key == config.USER_CONFIG['controls']['exit']:
                self.QUIT_TIME = config.QUIT_TIME

            # Caso o jogador minimize a janela, pause o jogo
            if not self.paused and pg.display.get_active() == 0:
                self.paused = True
                pg.mixer.music.pause()
            elif self.state_name != config.GAMEPLAY and pg.display.get_active() == 1:
                self.paused = False
                pg.mixer.music.unpause()

    def flip_state(self):
        r"""
        Muda para a próxima máquina de estado e executa
        o método startup da máquina que acabara de ser ativada.
        """
        if self.state.next_state != config.QUIT:
            next_state = self.state.next_state
            self.state.done = False
            self.state_name = next_state
            persistent = self.state.persist
            self.state = self.states[self.state_name]
            self.state.startup(persistent)
        else:
            self.done = True

    def update(self, dt):
        r"""
        Verifica o estado da variável done.
        Caso positivo, muda o estado de máquina.

        Args:
            :dt: float: Milisegundos desde à última atualização
        """

        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

        # Verifica se o usuário está pressionando o botão de saída
        pressed = pg.key.get_pressed()
        if pressed[config.USER_CONFIG['controls']['exit']]:
            if self.QUIT_TIME < 10:
                self.done = True
            else:
                self.QUIT_TIME -= .2625

    def draw(self):
        r"""
        Direciona o display do pygame para o estado de máquina
        e desenha os caracteres de informações de saídas.
        """
        self.state.draw(self.screen)

        # Para sair
        if self.QUIT_TIME < config.QUIT_TIME:
            a = pg.font.SysFont("arial", 12).render(config.LANG["system"][0].format(
                self.QUIT_TIME // 10), True, pg.Color("white"))
            self.screen.blit(a, (0, 0))

    def run(self):
        r"""
        Contêm o loop central do jogo.
        Executa os métodos dos estados de máquina,
        e realiza as adequações das informações do sistema
        """
        try:
            # Enquanto não finalizado
            while not self.done:
                dt = self.clock.tick(self.fps)
                # Executar os métodos das máquinas de estado
                self.event_loop()
                if not self.paused:
                    self.update(dt)
                    self.draw()
                    pg.display.update()


                pause_display = config.LANG["system"][1] if self.paused else ""
                if not config.SYS_SHOW:
                    title = "{} {}".format(config.TITLE, pause_display)
                else:
                    title = "{} {} @ {:.2f} FPS ({}, {})".format(
                        config.TITLE, pause_display, self.clock.get_fps(), config.WIDTH, config.HEIGHT)
                    if self.SHOW < 0:
                        config.sysinfo(self.clock.get_fps())
                        self.SHOW = 120
                    else:
                        self.SHOW -= 1

                pg.display.set_caption(title)
                
        except (KeyboardInterrupt):
            config.sys.exit(0)


class BaseState(object):
    r"""
    A base composta por cada máquina de estado.
    """

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.display = pg.display.get_surface()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        r"""
        Executado uma única vez na ativação do estado de máquina.

        Args:
            :persistent: dict: Dicionário compartilhado entre os estados de máquina
        """
        self.persist = persistent

    def get_event(self, event):
        r"""
        Recebe os eventos do pygame e aje de acordo o estipulado por cada
        máquina de estado.

        Args:
            :event: object: Opbjeto gerado pelo pygame contendo as informações sobre os eventos.
        """
        pass

    def update(self, dt):
        r"""
        Método para manutenção do estado de máquina.
        Executada a cada atualização de frame.

        Args:
            :dt: float: Milisegundos desde à última atualização
        """
        pass

    def draw(self, surface):
        r"""
        Desenha o estado de máquina.
        """
        pass