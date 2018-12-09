# !/usr/bin/python3
# -*- coding: utf-8 -*-
from lib.fsm import *
from lib.config import *
from lib.InputBox import *

# Importando a condição de cliente
import lib.client as client

__author__ = "Leandro Peres"
__all__ = ['End']

r"""
Se te queres matar, porque não te queres matar?
Ah, aproveita! que eu, que tanto amo a morte e a vida,
Se ousasse matar-me, também me mataria...
Ah, se ousares, ousa!
De que te serve o quadro sucessivo das imagens externas
A que chamamos o mundo?
A cinematografia das horas representadas
Por actores de convenções e poses determinadas,
O circo policromo do nosso dinamismo sem fim?
De que te serve o teu mundo interior que desconheces?
Talvez, matando-te, o conheças finalmente...
Talvez, acabando, comeces...
E de qualquer forma, se te cansa seres,
Ah, cansa-te nobremente,
E não cantes, como eu, a vida por bebedeira,
Não saúdes como eu a morte em literatura!

Fazes falta? Ó sombra fútil chamada gente!
Ninguém faz falta; não fazes falta a ninguém...
Sem ti correrá tudo sem ti.
Talvez seja pior para outros existires que matares-te...
Talvez peses mais durando, que deixando de durar...

A mágoa dos outros?... Tens remorso adiantado
De que te chorem?
Descansa: pouco te chorarão...
O impulso vital apaga as lágrimas pouco a pouco,
Quando não são de coisas nossas,
Quando são do que acontece aos outros, sobretudo a morte,
Porque é a coisa depois da qual nada acontece aos outros...

Primeiro é a angústia, a surpresa da vinda
Do mistério e da falta da tua vida falada...
Depois o horror do caixão visível e material,
E os homens de preto que exercem a profissão de estar ali.
Depois a família a velar, inconsolável e contando anedotas,
Lamentando a pena de teres morrido,
E tu mera causa ocasional daquela carpidação,
Tu verdadeiramente morto, muito mais morto que calculas...
Muito mais morto aqui que calculas,
Mesmo que estejas muito mais vivo além...

Depois a trágica retirada para o jazigo ou a cova,
E depois o princípio da morte da tua memória.
Há primeiro em todos um alívio
Da tragédia um pouco maçadora de teres morrido...
Depois a conversa aligeira-se quotidianamente,
E a vida de todos os dias retoma o seu dia...

Depois, lentamente esqueceste.
Só és lembrado em duas datas, aniversariamente:
Quando faz anos que nasceste, quando faz anos que morreste;
Mais nada, mais nada, absolutamente mais nada.
Duas vezes no ano pensam em ti.
Duas vezes no ano suspiram por ti os que te amaram,
E uma ou outra vez suspiram se por acaso se fala em ti.

Encara-te a frio, e encara a frio o que somos...
Se queres matar-te, mata-te...
Não tenhas escrúpulos morais, receios de inteligência!...
Que escrúpulos ou receios tem a mecânica da vida?

Que escrúpulos químicos tem o impulso que gera
As seivas, e a circulação do sangue, e o amor?
Que memória dos outros tem o ritmo alegre da vida?

Ah, pobre vaidade de carne e osso chamada homem,
Não vês que não tens importância absolutamente nenhuma?

És importante para ti, porque é a ti que te sentes.
És tudo para ti, porque para ti és o universo,
E o próprio universo e os outros
Satélites da tua subjectividade objectiva.
És importante para ti porque só tu és importante para ti.
E se és assim, ó mito, não serão os outros assim?

Tens, como Hamlet, o pavor do desconhecido?
Mas o que é conhecido? O que é que tu conheces,
Para que chames desconhecido a qualquer coisa em especial?

Tens, como Falstaff, o amor gorduroso da vida?
Se assim a amas materialmente, ama-a ainda mais materialmente:
Torna-te parte carnal da terra e das coisas!
Dispersa-te, sistema físico-químico
De células nocturnamente conscientes
Pela nocturna consciência da inconsciência dos corpos,
Pelo grande cobertor não-cobrindo-nada das aparências,
Pela relva e a erva da proliferação dos seres,
Pela névoa atómica das coisas,
Pelas paredes turbilhonantes
Do vácuo dinâmico do mundo...

Poesias de Álvaro de Campos. Fernando Pessoa. Lisboa: Ática, 1944 (imp. 1993).  - 22.
"""

class End(BaseState):
    r"""
    Máquina de estado destinada para o fim da jogatina.

    Args:
        :resources: dict: Recursos carregados
    """

    def __init__(self, resources):
        super(End, self).__init__()
        self.resources = resources

    def startup(self, persist):
        pg.mouse.set_visible(True)
        # Recebe do estado gameplay um dicionário compartilhado entre os estados
        self.persist = persist

        self.font = pg.font.Font(self.resources['fonts']['Stencil8bit'], 28)

        self.end = self.font.render(
            LANG['end'][0], True, pg.Color("white"), 36)
        self.winOrlose = self.font.render(
            LANG['end'][1], True, pg.Color("white"), 36)
        self.finalScore = self.font.render(
            LANG['end'][2].format(self.persist['SCORE']), True, pg.Color("white"), 36)
        self.nick = self.font.render(
            LANG['end'][-3], True, pg.Color("white"), 36)
        self.press = self.font.render(
            LANG['end'][-1], True, pg.Color("white"), 36)
        self.dc = self.font.render(
            LANG['end'][-2], True, pg.Color("red"), 36)

        # Inicializa a caixa de texto para inserção do apelido do jogador
        self.Box = InputBox((WIDTH - self.nick.get_rect().w) / 2, (HEIGHT / 3) +
                            ((HEIGHT * 0.275) - self.nick.get_rect().height), 140, 32, text=LANG['end'][-3], active=True,
                            font=self.resources['fonts']['pixelmix'])

        self.disconnect = False

    def get_event(self, event):
        # Envia para o InputBox os eventos para o devido tratamento
        name = self.Box.handle_event(event)
        if name and name != LANG['end'][-3]:
            # Envia para o servidor a pontuação.
            # Muda o estado de máquina para a lista de pontuações
            if client.connect():
                client.Insert(name, self.persist['SCORE'])
                while client.Get() != None:
                    pass
                self.next_state = SCORE
                self.done = True
            else:
                self.disconnect = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))

        surface.blit(self.end, ((WIDTH - self.end.get_rect().w) / 2, (HEIGHT / 3) -
                                ((HEIGHT * 0.25) - self.end.get_rect().height)))

        surface.blit(self.winOrlose, ((WIDTH - self.winOrlose.get_rect().w) / 2, (HEIGHT /
                                                                                  3) - ((HEIGHT * 0.15) - self.winOrlose.get_rect().height)))

        surface.blit(self.finalScore,
                     ((WIDTH - self.finalScore.get_rect().w) / 2, HEIGHT / 2))

        surface.blit(self.press, ((WIDTH - self.press.get_rect().w) /
                                  2, HEIGHT - self.press.get_rect().height * 2.25))

        if self.disconnect:
            surface.blit(self.dc, ((WIDTH - self.dc.get_rect().w) /
                                  2, HEIGHT - self.dc.get_rect().height * 4.25))

        self.Box.draw(surface)
