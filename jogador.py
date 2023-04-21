import pygame
from display import Image, get_ratio, mostra_essentials
from textos_menu import Texto
from copy import copy
from random import randint, choice

pos_players = [(910, 492), (743, 398), (743, 208), (910, 107), (1090, 208)]
pos_nome = [(1722, 80), (1722, 195), (1722, 315), (1722, 435), (1722, 555)]
pos_dinheiro = [(1722, 130), (1722, 250), (1722, 370), (1722, 490), (1722, 610)]

for list_of_pos in [pos_dinheiro, pos_nome]:
    for i in range(len(list_of_pos)):
        list_of_pos[i] = (int(list_of_pos[i][0] * get_ratio()), int(list_of_pos[i][1] * get_ratio()))


class Jogador:
    def __init__(self, nome, pos, tipo):
        self.nome = nome
        self.dinheiro = 0
        self.eliminado = False
        self.pos = pos
        self.image = Image("img/number" + str(pos) + ".png", pos_players[pos - 1][0], pos_players[pos - 1][1])
        self.tam_fonte = int(30 * get_ratio())
        self.tipo = tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

    def pega_dinheiro_do_outro(self, outro_jogador, w, s, ess, jog):
        fatias = int(outro_jogador.dinheiro / 20)
        for i in range(20):
            self.dinheiro += fatias
            outro_jogador.dinheiro -= fatias
            w.fill('black')
            s.show_texto(w)
            mostra_essentials(w, ess)
            mostra_jogadores(w, jog)
            pygame.time.delay(50)
            pygame.display.update()
        if outro_jogador.dinheiro > 0:
            self.dinheiro += outro_jogador.dinheiro
            outro_jogador.dinheiro = 0
            w.fill('black')
            s.show_texto(w)
            mostra_essentials(w, ess)
            mostra_jogadores(w, jog)
            pygame.display.update()

        if (self.dinheiro % 10) >= 8:
            self.dinheiro += (10 - (self.dinheiro % 10))
            w.fill('black')
            s.show_texto(w)
            mostra_essentials(w, ess)
            mostra_jogadores(w, jog)
            pygame.display.update()

    def ganha_dinheiro(self, dinheiro, w, s, ess, jog, img_pergunta):
        fatias = int(dinheiro / 20)
        for i in range(20):
            w.fill('black')
            s.show_texto(w)
            self.dinheiro += fatias
            mostra_essentials(w, ess)
            mostra_jogadores(w, jog)
            img_pergunta.draw(w)
            txt_dinheiro = Texto('R$ ' + str(self.dinheiro), 'ArialBlack', 120, 960, 910)
            txt_dinheiro.show_texto(w, 'center')
            pygame.time.delay(50)
            pygame.display.update()

    def mostra_dinheiro(self, w, img_pergunta):
        for i in range(20):
            img_pergunta.draw(w)
            txt_dinheiro = Texto('R$ ' + str(self.dinheiro), 'ArialBlack', 120, 960, 910)
            txt_dinheiro.show_texto(w, 'center')
            pygame.time.delay(50)
            pygame.display.update()

    def eliminar(self, jogadores):
        self.eliminado = True
        if self.dinheiro > 0:
            count = 0
            for pl in jogadores:
                if not pl.eliminado:
                    count += 1
            if count > 0:
                dinheiro_repartido = int(self.dinheiro / count)
                for pl in jogadores:
                    if not pl.eliminado:
                        pl.dinheiro += dinheiro_repartido

                if count == 1:
                    for pl in jogadores:
                        if not pl.eliminado:
                            if (pl.dinheiro % 10) >= 8:
                                pl.dinheiro += (10 - (pl.dinheiro % 10))

    def change_pos(self, nova_pos):
        self.image = Image("img/number" + str(self.pos) + ".png", pos_players[nova_pos - 1][0],
                           pos_players[nova_pos - 1][1])

    def move_center(self, nova_pos=(910, 300)):
        self.image = Image("img/number" + str(self.pos) + ".png", nova_pos[0], nova_pos[1])

    def display_nome(self, window):
        texto_nome = pygame.font.Font('fonts/FreeSansBold.ttf', self.tam_fonte).render(self.nome, True, (255, 255, 255))
        text_rect = texto_nome.get_rect(center=pos_nome[self.pos - 1])
        window.blit(texto_nome, text_rect)

    def display_dinheiro(self, window):
        texto_dinheiro = pygame.font.Font('fonts/FreeSans.ttf', self.tam_fonte).render("R$ " + str(self.dinheiro),
                                                                                       True, (255, 255, 255))
        text_rect = texto_dinheiro.get_rect(center=pos_dinheiro[self.pos - 1])
        window.blit(texto_dinheiro, text_rect)

    def bot_responde(self, rodada, pergunta_final='', alternativas='', resposta_certa='', tempo_final=0, certas=0):
        # Nível 1 - Bot Carla Perez na final
        # 0% para acertar - 100% para chutar
        # Nível 2 - Bot Leigo
        # 20% para acertar - 80% para chutar
        # Nível 3 - Bot Normal
        # 40% para acertar - 60% para chutar
        # Nível 4 - Bot Inteligente
        # 60% para acertar - 40% para chutar
        # Nível 5 - Bot Cacá Rosset na final
        # 80% para acertar - 20% para chutar
        limiar = 10-2*(self.tipo-1)

        # Será gerado um número entre 1 e 10. Se for maior que o limiar, o bot acerta. Se não for, ele chuta.
        decisao = randint(1, 10)
        respostas = ['A', 'B', 'C', 'D']
        if decisao > limiar:  # Ou seja, se ele for acertar
            if rodada < 5:
                num_resposta = 0
                for alt in alternativas:
                    num_resposta += 1
                    if alt == resposta_certa:  # No momento em que tivermos a certa, ele para
                        break
                # Retorna a resposta certa (1, 2, 3, 4) e o tempo para responder
                print(alternativas[num_resposta-1])
                return num_resposta, randint(2*(self.tipo-1), 15)
            else:
                print(pergunta_final['certa'])
                print(pergunta_final)
                return respostas.index(pergunta_final['certa'])+1, tempo_final - randint(3, 6)
        else:  # SE CHUTAR...
            if rodada < 5:
                chute = choice(alternativas)
                print(chute)
                # Retorna o chute (A, B, C, D) e o tempo para responder
                return alternativas.index(chute)+1, randint(1, 12)
            else:
                limiar_chute = randint(20, 50)

                # Pode ser que o chute seja mais cedo ou mais tarde. Decidi fazer um
                # limiar variável.
                print(pergunta_final)
                if tempo_final < limiar_chute or certas == 7:
                    # Se o tempo for menor que o limiar ou estivermos em 7 certas, o bot chuta.
                    chute = choice(respostas[:-1])
                    return respostas.index(chute)+1, tempo_final - randint(4, 6)
                else:
                    return 0, tempo_final - randint(4, 6)

    def bot_escolhe(self, escolhas, lider, nao_respondeu, rodada, pergunta):
        if rodada == 4 and pergunta == 5:  # Se estiver na última pergunta
            outro = [esc for esc in escolhas if esc != self][0]
            if abs(self.dinheiro - outro.dinheiro) > 2500:
                # Se não alcança o outro se acertar...
                escolhas = [esc for esc in escolhas if esc != self]
                # Desafie o outro obrigatoriamente.
        else:
            for nr in nao_respondeu:  # Quem não respondeu tem mais chances de ser escolhido.
                if nr in escolhas:
                    escolhas.append(nr)
                    if rodada == 1:
                        # Se estivermos na primeira rodada, teremos uma tendência bem maior
                        # a perguntar de quem não respondeu.
                        escolhas.append(nr)
                        escolhas.append(nr)
                        escolhas.append(nr)
                        escolhas.append(nr)
            if lider is not None and lider != self:  # Se temos um líder e não é o bot
                escolhas.append(lider)  # Ele terá um peso a mais para ser escolhido. É o líder.
            if self.dinheiro == 0 and lider is not None:  # Se tá sem grana, tem mais tendência a perguntar ao líder!
                escolhas.append(lider)
                if rodada == 1:  # E também de perguntar ao líder se acabou de perder a grana.
                    escolhas.append(lider)
                    escolhas.append(lider)
                    escolhas.append(lider)
                    escolhas.append(lider)
        print([esc.nome for esc in escolhas])
        return choice(escolhas)


def mostra_jogadores(window, jogadores):
    for pl in jogadores:
        if not pl.eliminado:
            pl.image.draw(window)
            pl.display_nome(window)
            pl.display_dinheiro(window)


def copy_jogadores(jogadores):
    jogadores_copy = []
    for pl in jogadores:
        jogadores_copy.append(copy(pl))
    return jogadores_copy


def get_leader(jogadores):
    qtd_lideres = 1
    maior_dinheiro = -1
    for pl in jogadores:
        if not pl.eliminado:
            if pl.dinheiro > maior_dinheiro:
                qtd_lideres = 1
                maior_dinheiro = pl.dinheiro
                lider = pl
            elif pl.dinheiro == maior_dinheiro:
                qtd_lideres += 1
                lider = None
    return lider


def get_em_risco(jogadores):
    lider = get_leader(jogadores)
    pode_cair = []
    if lider is None:
        for pl in jogadores:
            if not pl.eliminado:
                pode_cair.append(pl)
        return pode_cair
    else:
        for pl in jogadores:
            if pl != lider and not pl.eliminado:
                pode_cair.append(pl)
        return pode_cair


def click_on_player(jogadores, mouse_pos):
    for pl in jogadores:
        # se clicou na imagem
        if pl.image.rect.collidepoint(mouse_pos):
            return pl


def get_escolhas(jogadores, desafiante):
    escolhas = []
    for pl in jogadores:
        if not pl.eliminado:
            if pl != desafiante:
                escolhas.append(pl)
    if len(escolhas) == 1:
        escolhas.append(desafiante)
    return escolhas


def passa_pra_quem(escolhas, s):
    num_escolhas = [pl.pos for pl in escolhas]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                chosen = click_on_player(escolhas, pygame.mouse.get_pos())
                if s.check_click():
                    pygame.mixer.pause()
                    return None
                if chosen is not None:
                    if chosen.pos in num_escolhas:
                        return chosen
            if ev.type == pygame.KEYDOWN:
                if ((ev.key == pygame.K_1) or (ev.key == pygame.K_KP1)) and (1 in num_escolhas):
                    return [pl for pl in escolhas if pl.pos == 1][0]
                if ((ev.key == pygame.K_2) or (ev.key == pygame.K_KP2)) and (2 in num_escolhas):
                    return [pl for pl in escolhas if pl.pos == 2][0]
                if ((ev.key == pygame.K_3) or (ev.key == pygame.K_KP3)) and (3 in num_escolhas):
                    return [pl for pl in escolhas if pl.pos == 3][0]
                if ((ev.key == pygame.K_4) or (ev.key == pygame.K_KP4)) and (4 in num_escolhas):
                    return [pl for pl in escolhas if pl.pos == 4][0]
                if ((ev.key == pygame.K_5) or (ev.key == pygame.K_KP5)) and (5 in num_escolhas):
                    return [pl for pl in escolhas if pl.pos == 5][0]
