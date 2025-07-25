import pygame

from display import *
from jogador import *
from jogar_roleta import *
from textos_menu import *
from inputbox import *
import pandas as pd
from os import listdir
from math import ceil
from random import randrange, shuffle, uniform
import random
import sys
import locale

try:
    # Tente definir o locale no formato que é suportado no Windows
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Tentativa com código de página específico
    sem_locale = False
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')  # Tentativa sem a codificação
        sem_locale = False
    except locale.Error as e:
        sem_locale = True
        print("Não foi possível configurar o locale:", e)
pygame.init()


def load_sounds():
    dict_sounds = {}
    for som in listdir('sons'):
        dict_sounds[som[3:-4]] = pygame.mixer.Sound('sons/' + som)
    return dict_sounds


def limpa_tela(w):
    w.fill('black')
    rr_bg = Image("img/rr_bg.jpg", 0, 0)
    rr_bg.draw(w)

def logo_programa():
    fadein()
    pygame.time.delay(3000)
    fadeout()

def fadeout(width=1920, height=1080, img="img/Roleta_Russa.jpg", x=240, y=0):
    global window
    rr_centro = Image(img, x, y)
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        rr_centro.draw(window)
        window.blit(fade, (0, 0))
        pygame.display.update()


def fadein(width=1920, height=1080, img="img/Roleta_Russa.jpg", x=240, y=0):
    global window
    rr_centro = Image(img, x, y)
    fade = pygame.Surface((width * get_ratio(), height * get_ratio()))
    fade.fill((0, 0, 0))
    for alpha in range(300, 0, -10):
        fade.set_alpha(alpha)
        rr_centro.draw(window)
        window.blit(fade, (0, 0))
        pygame.display.update()


def comeco_jogo():
    global window
    fr = ['Vai começar o Roleta Russa! Um erro, ', 'um vacilo, e você pode ir pro buraco.']
    for i in range(len(fr)):
        frase = Texto(fr[i], 'FreeSans',
                      72, 960, 850 + 80 * i)
        frase.show_texto(window, align='center')


def jogar_roleta(modo, alav, chances_de_cair=0, jogador_em_risco=Jogador('Zé', 1, 0), jogadores=[], final=False):
    global sair_do_jogo
    global essentials
    global window
    global quedas
    global sons
    blit_all(sair_do_jogo, essentials, jogadores)
    comeca = randrange(6)
    giros = 0
    pygame.event.clear()

    if modo == 'normal':
        vermelhos = []
        for i in range(chances_de_cair):
            vermelhos.append(comeca % 6)
            comeca -= 1
        vermelhos_iniciais = vermelhos
        space = False
        sons['jogando_roleta'].play(0)
        buracos_abertos_final = [2, 3, 4, 5, 0, 1][1:chances_de_cair + 1]

        for i in range(13):
            alav.update_image('img/alavanca1-' + str(i) + '.png')
            blit_all(sair_do_jogo, essentials, jogadores)
            if final:
                blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
            pygame.display.update()
        if jogador_em_risco.tipo == 0:
            while not space:
                vermelhos = [(v + 1) % 6 for v in vermelhos]
                blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
                if final:
                    blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                    aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                    blit_varios_buracos(list_buracos=aberto_e_vermelho)

                pygame.display.update()
                pygame.time.delay(50)
                giros += 1
                for events in pygame.event.get():
                    if events.type == pygame.QUIT:
                        space = True
                    if events.type == pygame.KEYDOWN:
                        if events.key == pygame.K_SPACE:
                            return para_roleta('normal', alav, vermelhos=vermelhos, jogador_em_risco=jogador_em_risco,
                                               jogadores=jogadores, final=final, giros=giros,
                                               vermelhos_iniciais=vermelhos_iniciais)
                    if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                        if alav.check_click():
                            return para_roleta('normal', alav, vermelhos=vermelhos, jogador_em_risco=jogador_em_risco,
                                               jogadores=jogadores, final=final, giros=giros,
                                               vermelhos_iniciais=vermelhos_iniciais)
        else:
            jogando_roleta = uniform(0.5, 3)
            start = pygame.time.get_ticks()
            while not space:
                segundos = (pygame.time.get_ticks() - start) / 1000
                vermelhos = [(v + 1) % 6 for v in vermelhos]
                blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
                if final:
                    blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                    aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                    blit_varios_buracos(list_buracos=aberto_e_vermelho)
                pygame.display.update()
                pygame.time.delay(50)
                giros += 1
                if segundos > jogando_roleta:
                    return para_roleta('normal', alav, vermelhos=vermelhos, jogador_em_risco=jogador_em_risco,
                                       jogadores=jogadores, final=final, giros=giros,
                                       vermelhos_iniciais=vermelhos_iniciais)
    elif modo == 'carrasco':
        em_risco = get_em_risco(jogadores)
        pos_risco = randrange(len(em_risco))
        vermelhos_iniciais = [comeca]
        space = False
        for i in range(13):
            alav.update_image('img/alavanca2-' + str(i) + '.png')
            blit_all(sair_do_jogo, essentials, jogadores, display_update=True)

        if len(em_risco) > 1:
            sons['jogando_roleta'].play(0)
            lider = get_leader(jogadores)
            if (lider is not None and lider.tipo == 0) or (lider is None and not todos_bots(jogadores)):
                # Se temos um líder e ele é humano OU não temos líder, joga a roleta.
                while not space:
                    comeca = (comeca + 1) % 6  # São 6 buracos
                    blit_vermelho(sair_do_jogo, essentials, jogadores, [comeca])
                    pygame.display.update()
                    pos_risco = (pos_risco + 1) % len(em_risco)  # Enquanto a roleta joga normal, internamente escolhe 1
                    pygame.time.delay(50)
                    giros += 1
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            space = True
                        if events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_SPACE:
                                roleta_verdadeira = em_risco[pos_risco]
                                return para_roleta('carrasco', alav, eliminado=roleta_verdadeira, vermelhos=[comeca],
                                                   jogadores=jogadores, giros=giros,
                                                   vermelhos_iniciais=vermelhos_iniciais)
                        if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                            if alav.check_click():
                                roleta_verdadeira = em_risco[pos_risco]
                                return para_roleta('carrasco', alav, eliminado=roleta_verdadeira, vermelhos=[comeca],
                                                   jogadores=jogadores, giros=giros,
                                                   vermelhos_iniciais=vermelhos_iniciais)
            else:
                jogando_roleta = uniform(0.5, 4)
                start = pygame.time.get_ticks()
                while not space:
                    segundos = (pygame.time.get_ticks() - start) / 1000
                    comeca = (comeca + 1) % 6  # São 6 buracos
                    blit_vermelho(sair_do_jogo, essentials, jogadores, [comeca])
                    pygame.display.update()
                    pos_risco = (pos_risco + 1) % len(em_risco)  # Enquanto a roleta joga normal, internamente escolhe 1
                    pygame.time.delay(50)
                    giros += 1
                    if segundos > jogando_roleta:
                        roleta_verdadeira = em_risco[pos_risco]
                        return para_roleta('carrasco', alav, eliminado=roleta_verdadeira, vermelhos=[comeca],
                                           jogadores=jogadores, giros=giros,
                                           vermelhos_iniciais=vermelhos_iniciais)
        else:
            start = pygame.time.get_ticks()
            lider = get_leader(jogadores)
            if (lider is not None and lider.tipo == 0) or (lider is None):
                while not space:
                    segundos = (pygame.time.get_ticks() - start) / 1000
                    if segundos > 1.5:
                        for i in range(12, -1, -1):
                            alav.update_image('img/alavanca2-' + str(i) + '.png')
                            blit_all(sair_do_jogo, essentials, jogadores, display_update=True)
                        jogadores_aux = copy_jogadores(jogadores)
                        quedas.append({'modo': 'carrasco', 'vermelhos': [],
                                       'jog_eliminado': jogadores_aux[em_risco[0].pos - 1],
                                       'jogadores': jogadores_aux})
                        em_risco[0].eliminar(jogadores)
                        blit_queda(sair_do_jogo, essentials, jogadores, [], em_risco[0], rodada4=True)
                        sons['queda'].play(0)
                        return em_risco[0]
                    for events in pygame.event.get():
                        if events.type == pygame.QUIT:
                            pygame.quit()
                        if events.type == pygame.KEYDOWN:
                            if events.key == pygame.K_SPACE:
                                for i in range(12, -1, -1):
                                    alav.update_image('img/alavanca2-' + str(i) + '.png')
                                    blit_all(sair_do_jogo, essentials, jogadores)
                                jogadores_aux = copy_jogadores(jogadores)
                                quedas.append({'modo': 'carrasco', 'vermelhos': [],
                                               'jog_eliminado': jogadores_aux[em_risco[0].pos - 1],
                                               'jogadores': jogadores_aux})
                                em_risco[0].eliminar(jogadores)
                                blit_queda(sair_do_jogo, essentials, jogadores, [], em_risco[0], rodada4=True)
                                sons['queda'].play(0)
                                return em_risco[0]
                        if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                            if alav.check_click():
                                for i in range(12, -1, -1):
                                    alav.update_image('img/alavanca2-' + str(i) + '.png')
                                    blit_all(sair_do_jogo, essentials, jogadores)
                                jogadores_aux = copy_jogadores(jogadores)
                                quedas.append({'modo': 'carrasco', 'vermelhos': [],
                                               'jog_eliminado': jogadores_aux[em_risco[0].pos - 1],
                                               'jogadores': jogadores_aux})
                                em_risco[0].eliminar(jogadores)
                                blit_queda(sair_do_jogo, essentials, jogadores, [], em_risco[0], rodada4=True)
                                sons['queda'].play(0)
                                return em_risco[0]
            else:
                start = pygame.time.get_ticks()
                while not space:
                    segundos = (pygame.time.get_ticks() - start) / 1000
                    if segundos > 1.5:
                        for i in range(12, -1, -1):
                            alav.update_image('img/alavanca2-' + str(i) + '.png')
                            blit_all(sair_do_jogo, essentials, jogadores, display_update=True)
                        jogadores_aux = copy_jogadores(jogadores)
                        quedas.append({'modo': 'carrasco', 'vermelhos': [],
                                       'jog_eliminado': jogadores_aux[em_risco[0].pos - 1],
                                       'jogadores': jogadores_aux})
                        em_risco[0].eliminar(jogadores)
                        blit_queda(sair_do_jogo, essentials, jogadores, [], em_risco[0], rodada4=True)
                        sons['queda'].play(0)
                        return em_risco[0]
    elif modo == 'comeco':
        candidatos = get_em_risco(jogadores)  # Não estão bem em risco, só de fazer a primeira pergunta

        pos_azul = randrange(len(candidatos))
        space = False
        for i in range(13):
            alav.update_image('img/alavanca2-' + str(i) + '.png')
            blit_all(sair_do_jogo, essentials, jogadores, display_update=True)

        jogando_roleta = uniform(1, 3)
        start = pygame.time.get_ticks()
        while not space:
            pos_azul = (pos_azul + 1) % len(candidatos)
            segundos = (pygame.time.get_ticks() - start) / 1000
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    space = True
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_SPACE:
                        pygame.mixer.stop()
                        roleta_verdadeira = candidatos[pos_azul]
                        return para_roleta('comeco', alav,
                                           jog_comeca=roleta_verdadeira, vermelhos=[comeca], jogadores=jogadores)
                if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
                    if alav.check_click():
                        pygame.mixer.stop()
                        roleta_verdadeira = candidatos[pos_azul]
                        return para_roleta('comeco', alav,
                                           jog_comeca=roleta_verdadeira, vermelhos=[comeca], jogadores=jogadores)
            if todos_bots(jogadores) and (segundos > jogando_roleta):
                roleta_verdadeira = candidatos[pos_azul]
                return para_roleta('comeco', alav,
                                   jog_comeca=roleta_verdadeira, vermelhos=[comeca], jogadores=jogadores)


def para_roleta(modo, alav, eliminado=Jogador('Zé', 1, 0), vermelhos=[0], jogador_em_risco=Jogador('Zé', 1, 0),
                jog_comeca=Jogador('Zé', 1, 0), jogadores=[], final=False, giros=0, vermelhos_iniciais=[]):
    global window
    global essentials
    global sair_do_jogo
    global quedas
    global sons
    blit_all(sair_do_jogo, essentials, jogadores)
    chances_de_cair = len(vermelhos)
    buracos_abertos_final = [2, 3, 4, 5, 0, 1][1:chances_de_cair + 1]
    if modo == 'normal':
        for i in range(12, -1, -1):
            blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
            if final:
                blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                blit_varios_buracos(list_buracos=aberto_e_vermelho)
            alav.update_image('img/alavanca1-' + str(i) + '.png')
            pygame.display.update()
        giros_dramaticos = randint(-1, 3)
        pygame.event.clear()
        for _ in range(giros_dramaticos):  # Não afetam porque fazem uma volta completa
            for _ in range(6):
                vermelhos = [(v + 1) % 6 for v in vermelhos]
                blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
                if final:
                    blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                    aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                    blit_varios_buracos(list_buracos=aberto_e_vermelho)
                pygame.time.delay(75)
        sons['jogando_roleta'].stop()
        pygame.mixer.stop()
        giros_para_parar = randint(4, 12)
        pygame.event.clear()
        for i in range(giros_para_parar):
            vermelhos = [(v + 1) % 6 for v in vermelhos]
            blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
            if final:
                blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                blit_varios_buracos(list_buracos=aberto_e_vermelho)
            sons['zonas_de_risco'].play(0)
            pygame.time.delay(int((1000 / giros_para_parar) * (i + 1)))
        giros_a_mais = randint(-3, 3) if giros_para_parar > 7 else randint(-3, 2)
        for _ in range(giros_a_mais):
            sons['zonas_de_risco'].play(0)
            vermelhos = [(v + 1) % 6 for v in vermelhos]
            blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos)
            if final:
                blit_varios_buracos(list_buracos=buracos_abertos_final, c='final')
                aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                blit_varios_buracos(list_buracos=aberto_e_vermelho)
            pygame.time.delay(1000)
        pygame.time.delay(randint(50, 300))
        if not final:
            if jogador_em_risco.pos in vermelhos:
                sons['queda'].play(0)
                jogadores_aux = copy_jogadores(jogadores)
                quedas.append({'modo': 'normal', 'vermelhos': vermelhos,
                               'jog_eliminado': jogadores_aux[jogador_em_risco.pos - 1],
                               'jogadores': jogadores_aux, 'giros_dramaticos': giros_dramaticos,
                               'giros_para_parar': giros_para_parar, 'giros': giros,
                               'vermelhos_iniciais': vermelhos_iniciais})
                jogador_em_risco.eliminar(jogadores)
                blit_queda(sair_do_jogo, essentials, jogadores, vermelhos, jogador_em_risco)
                return True
            else:
                sons['escapou'].play(0)
                sons['aplausos2'].play()
                return False
        else:
            if 2 in vermelhos:
                jogador_em_risco.eliminar(jogadores)
                blit_queda(sair_do_jogo, essentials, jogadores, vermelhos, jogador_em_risco, final=final)
                blit_varios_buracos(buracos_abertos_final, c='final')
                aberto_e_vermelho = [v for v in vermelhos if v in buracos_abertos_final]
                blit_varios_buracos(list_buracos=aberto_e_vermelho)
                return [True, vermelhos]
            else:
                return [False, vermelhos]
    elif modo == 'carrasco':
        loc_vermelho = vermelhos[0]
        for i in range(12, -1, -1):
            alav.update_image('img/alavanca2-' + str(i) + '.png')
            blit_vermelho(sair_do_jogo, essentials, jogadores, [loc_vermelho])
        giros_dramaticos = randint(1, 10)
        for _ in range(giros_dramaticos):  # Não afetam porque fazem uma volta completa
            for _ in range(6):
                loc_vermelho = (loc_vermelho + 1) % 6
                blit_vermelho(sair_do_jogo, essentials, jogadores, [loc_vermelho])
                pygame.time.delay(75)
        pygame.mixer.stop()
        sons['jogando_roleta'].stop()

        giros_para_parar = randint(4, 12)
        pos_final = (loc_vermelho + giros_para_parar) % 6
        if len(get_em_risco(jogadores)) == 2:
            posicoes_risco = [j.pos for j in get_em_risco(jogadores)]
            dif = min((posicoes_risco[1] - posicoes_risco[0]) % 6, (posicoes_risco[0] - posicoes_risco[1]) % 6)
            if dif == 1:
                giros_para_parar = ((posicoes_risco[0] - 1) - loc_vermelho) % 6 + 6
            elif dif == 2:
                if posicoes_risco == [1, 5]:
                    giros_para_parar = ((posicoes_risco[1] - 1) - loc_vermelho) % 6 + 6
                else:
                    giros_para_parar = ((posicoes_risco[0] - 1) - loc_vermelho) % 6 + 6
        elif len(get_em_risco(jogadores)) >= 3:
            if ((eliminado.pos - pos_final) % 6) > 2:
                if giros_para_parar <= 9:
                    giros_para_parar += 3
                else:
                    giros_para_parar -= 3

        for i in range(giros_para_parar):
            loc_vermelho = (loc_vermelho + 1) % 6
            blit_vermelho(sair_do_jogo, essentials, jogadores, [loc_vermelho])
            sons['zonas_de_risco'].play(0)
            pygame.time.delay(int((1000 / giros_para_parar) * (i + 1)))

        while loc_vermelho != eliminado.pos:
            loc_vermelho = (loc_vermelho + 1) % 6
            blit_vermelho(sair_do_jogo, essentials, jogadores, [loc_vermelho])
            sons['zonas_de_risco'].play(0)
            pygame.time.delay(1000)
        sons['queda'].play(0)
        jogadores_aux = copy_jogadores(jogadores)
        quedas.append({'modo': 'carrasco', 'vermelhos': [loc_vermelho],
                       'jog_eliminado': jogadores_aux[eliminado.pos - 1],
                       'jogadores': jogadores_aux, 'giros_dramaticos': giros_dramaticos,
                       'giros_para_parar': giros_para_parar, 'giros': giros, 'vermelhos_iniciais': vermelhos_iniciais})
        eliminado.eliminar(jogadores)
        blit_queda(sair_do_jogo, essentials, jogadores, [loc_vermelho], eliminado)
        return eliminado
    elif modo == 'comeco':
        pygame.mixer.stop()
        for i in range(12, -1, -1):
            alav.update_image('img/alavanca2-' + str(i) + '.png')
            blit_all(sair_do_jogo, essentials, jogadores, display_update=True)
        sons['jogando_roleta'].play(0)
        comeca = randrange(6)
        blit_azul(sair_do_jogo, essentials, jogadores, comeca)
        giros = randint(20, 70)
        for i in range(giros):
            comeca = (comeca + 1) % 6  # São 6 buracos
            blit_azul(sair_do_jogo, essentials, jogadores, comeca)
            pygame.time.delay(50)
        pygame.mixer.stop()
        sons['jogando_roleta'].stop()

        giros_para_parar = ((jog_comeca.pos - comeca) % 6) + randint(5, 6)

        for i in range(giros_para_parar):
            comeca = (comeca + 1) % 6
            sons['zonas_de_risco'].play(0)
            blit_azul(sair_do_jogo, essentials, jogadores, comeca)
            pygame.time.delay(int((1000 / giros_para_parar) * (i + 1)))

        while comeca != jog_comeca.pos:
            comeca = (comeca + 1) % 6
            sons['zonas_de_risco'].play(0)
            blit_azul(sair_do_jogo, essentials, jogadores, comeca)
            pygame.time.delay(1000)

        sons['quem_comeca'].play(0)
        return jog_comeca


def mostra_quedas():
    global sair_do_jogo
    global essentials
    global quedas
    global window

    sons['tema'].play()
    if quedas[0]['modo'] == 'normal':
        essentials[0].update_image('img/roleta_' + str(quedas[0]['jog_eliminado'].pos) + '.png')
    else:
        essentials[0].update_image('img/roleta.png')
    blit_all(sair_do_jogo, essentials, quedas[0]['jogadores'], display_update=True)

    for q in quedas:
        alav = essentials[2]
        pygame.event.clear()
        if q['modo'] == 'normal':
            essentials[0].update_image('img/roleta_' + str(q['jog_eliminado'].pos) + '.png')
            blit_all(sair_do_jogo, essentials, q['jogadores'], display_update=True)
            wait_until_enter(uniform(1.5, 4))
            sons['jogando_roleta'].play(0)
            for i in range(13):
                alav.update_image('img/alavanca1-' + str(i) + '.png')
                blit_all(sair_do_jogo, essentials, q['jogadores'], display_update=True)

            vermelhos_aux = q['vermelhos_iniciais']
            pygame.event.clear()
            for i in range(q['giros']):
                vermelhos_aux = [(v + 1) % 6 for v in vermelhos_aux]
                blit_vermelho(sair_do_jogo, essentials, q['jogadores'], vermelhos_aux)
                pygame.display.update()
                pygame.time.delay(50)

            # print("Vermelhos", vermelhos_aux)
            pygame.event.clear()
            for i in range(12, -1, -1):
                blit_vermelho(sair_do_jogo, essentials, q['jogadores'], vermelhos_aux)
                alav.update_image('img/alavanca1-' + str(i) + '.png')
                pygame.display.update()

            pygame.event.clear()
            for _ in range(q['giros_dramaticos']):  # Não afetam porque fazem uma volta completa
                for _ in range(6):
                    vermelhos_aux = [(v + 1) % 6 for v in vermelhos_aux]
                    blit_vermelho(sair_do_jogo, essentials, q['jogadores'], vermelhos_aux)
                    pygame.time.delay(75)
            sons['jogando_roleta'].stop()

            pygame.event.clear()

            for i in range(q['giros_para_parar']):
                vermelhos_aux = [(v + 1) % 6 for v in vermelhos_aux]
                blit_vermelho(sair_do_jogo, essentials, q['jogadores'], vermelhos_aux)
                sons['zonas_de_risco'].play(0)
                pygame.time.delay(int((1000 / q['giros_para_parar']) * (i + 1)))

            while vermelhos_aux != q['vermelhos']:
                pygame.event.clear()
                vermelhos_aux = [(v + 1) % 6 for v in vermelhos_aux]
                blit_vermelho(sair_do_jogo, essentials, q['jogadores'], vermelhos_aux)
                sons['zonas_de_risco'].play(0)
                pygame.time.delay(1000)
            pygame.mixer.stop()
            sons['queda'].play(0)

            q['jog_eliminado'].eliminar(q['jogadores'])
            blit_queda(sair_do_jogo, essentials, q['jogadores'], q['vermelhos'], q['jog_eliminado'])

            wait_until_enter(int(sons['queda'].get_length()))
        else:
            essentials[0].update_image('img/roleta.png')
            alav.update_image('img/alavanca2-0.png')
            blit_all(sair_do_jogo, essentials, q['jogadores'], display_update=True)
            

            wait_until_enter(uniform(1.5, 4))
            for i in range(13):
                alav.update_image('img/alavanca2-' + str(i) + '.png')
                blit_all(sair_do_jogo, essentials, q['jogadores'], display_update=True)

            if len(get_em_risco(q['jogadores'])) > 1:
                pygame.event.clear()
                loc_vermelho = q['vermelhos_iniciais'][0]
                sons['jogando_roleta'].play(0)

                for i in range(q['giros']):
                    loc_vermelho = (loc_vermelho + 1) % 6  # São 6 buracos
                    blit_vermelho(sair_do_jogo, essentials, q['jogadores'], [loc_vermelho])
                    pygame.display.update()
                    pygame.time.delay(50)

                for i in range(12, -1, -1):
                    blit_vermelho(sair_do_jogo, essentials, q['jogadores'], [loc_vermelho])
                    alav.update_image('img/alavanca2-' + str(i) + '.png')
                    pygame.display.update()

                for _ in range(q['giros_dramaticos']):  # Não afetam porque fazem uma volta completa
                    for _ in range(6):
                        loc_vermelho = (loc_vermelho + 1) % 6  # São 6 buracos
                        blit_vermelho(sair_do_jogo, essentials, q['jogadores'], [loc_vermelho])
                        pygame.time.delay(75)
                sons['jogando_roleta'].stop()

                pygame.event.clear()

                for i in range(q['giros_para_parar']):
                    loc_vermelho = (loc_vermelho + 1) % 6  # São 6 buracos
                    blit_vermelho(sair_do_jogo, essentials, q['jogadores'], [loc_vermelho])
                    sons['zonas_de_risco'].play(0)
                    pygame.time.delay(int((1000 / q['giros_para_parar']) * (i + 1)))

                while loc_vermelho != q['jog_eliminado'].pos:
                    pygame.event.clear()
                    loc_vermelho = (loc_vermelho + 1) % 6  # São 6 buracos
                    blit_vermelho(sair_do_jogo, essentials, q['jogadores'], [loc_vermelho])
                    sons['zonas_de_risco'].play(0)
                    pygame.time.delay(1000)
                pygame.mixer.stop()
                sons['queda'].play(0)

                q['jog_eliminado'].eliminar(q['jogadores'])
                blit_queda(sair_do_jogo, essentials, q['jogadores'], q['vermelhos'], q['jog_eliminado'])
                wait_until_enter(int(sons['queda'].get_length()))
            else:
                wait_until_enter(1.5)
                for i in range(12, -1, -1):
                    blit_all(sair_do_jogo, essentials, q['jogadores'])
                    alav.update_image('img/alavanca2-' + str(i) + '.png')
                    pygame.display.update()

                q['jog_eliminado'].eliminar(q['jogadores'])
                blit_queda(sair_do_jogo, essentials, q['jogadores'], [], q['jog_eliminado'])
                blit_varios_buracos([q['jog_eliminado'].pos], c='rodada4')
                pygame.mixer.stop()
                sons['queda'].play()
                wait_until_enter(int(sons['queda'].get_length()))
        sons['tema'].play()
    # wait_until_enter(1)
    pygame.mixer.stop()
    sons['rever_quedas'].play()
    rr_quedas = Image('img/rr_quedas.png', 0, 0)
    rr_quedas.draw(window)
    pygame.display.update()
    wait_until_enter(int(sons['rever_quedas'].get_length()))
    essentials[0].update_image("img/roleta_inicio.png")


def prompt_rever_quedas(w):
    global essentials
    frase_dist = ['Gostaria de rever a queda dos adversários? S/N']
    for i in range(len(frase_dist)):
        frase = Texto(frase_dist[i], 'FreeSansBold', 72, 960, 820 + 80 * i)
        frase.show_texto(w, align='center')
    pygame.display.update()
    loop = True
    while loop:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if sair_do_jogo.check_click():
                    pygame.mixer.stop()
                    return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    pygame.mixer.stop()
                    essentials[0].update_image('img/roleta.png')
                    rr_quedas = Image('img/rr_quedas.png', 0, 0)
                    rr_quedas.draw(w)

                    sons['rever_quedas'].play()
                    pygame.display.update()
                    wait_until_enter(int(sons['rever_quedas'].get_length()))
                    mostra_quedas()
                    sons['aplausos2'].play(0)
                    return True
                if ev.key == pygame.K_n:
                    pygame.mixer.stop()
                    return False


def blit_all(s, ess, jogadores, rodada=0, display_update=False):
    global window
    window.fill('black')
    s.show_texto(window)
    mostra_essentials(window, ess)
    mostra_jogadores(window, jogadores)
    if rodada < 5:
        Texto('Responder - A, B, C, D ou 1, 2, 3, 4',
              'FreeSans', 24, 5, 450).show_texto(window, 'topleft')
        Texto('Jogar roleta - Espaço ou clique na alavanca',
              'FreeSans', 24, 5, 480).show_texto(window, 'topleft')
        Texto('Desafiar jogador - Clicar no ícone ou 1, 2, 3, 4 ou 5',
              'FreeSans', 24, 5, 510).show_texto(window, 'topleft')
    else:
        Texto('Responder - A, B, C ou 1, 2, 3',
              'FreeSans', 24, 5, 450).show_texto(window, 'topleft')
        Texto('Confirmar resposta - ENTER',
              'FreeSans', 24, 5, 480).show_texto(window, 'topleft')
        Texto('Passar a pergunta - P',
              'FreeSans', 24, 5, 510).show_texto(window, 'topleft')
    if display_update:
        pygame.display.update()


def blit_vermelho(s, ess, jogadores, vermelhos):
    global window
    window.fill('black')
    s.show_texto(window)
    mostra_essentials(window, ess)
    bota_vermelho(window, vermelhos)
    mostra_jogadores(window, jogadores)
    pygame.display.update()


def blit_azul(s, ess, jogadores, a):
    global window
    window.fill('black')
    s.show_texto(window)
    mostra_essentials(window, ess)
    bota_azul(window, a)
    mostra_jogadores(window, jogadores)
    pygame.display.update()


def blit_queda(s, ess, jogadores, vermelhos, jogador, final=False, rodada4=False):
    global window
    window.fill('black')
    s.show_texto(window)
    mostra_essentials(window, ess)
    if not final and not rodada4:
        queda(window, vermelhos, jogador.pos)
    elif not final and rodada4:
        queda(window, vermelhos, jogador.pos, c='rodada4')
    else:
        queda(window, vermelhos, 2)
    mostra_jogadores(window, jogadores)
    pygame.display.update()


def blit_varios_buracos(list_buracos, c='caiu'):
    global window
    for b in list_buracos:
        if c == 'caiu':
            window.blit(caiu, pos_buracos[b])
        else:
            window.blit(buraco, pos_buracos[b])
    pygame.display.update()


def blit_pergunta(perg):
    global window
    global img_pergunta

    img_pergunta.draw(window)

    words = perg.split(' ')
    pergunta_split = []
    current_line = ''
    tam_fonte = 36

    for word in words:
        test_line = f"{current_line} {word}".strip()
        line_width, _ = pygame.font.Font('fonts/FreeSans.ttf', int(tam_fonte)).size(test_line)
        if line_width <= 1000:
            current_line = test_line
        else:
            # atualiza lista de linhas e começa nova com a palavra
            pergunta_split.append(current_line)
            current_line = word

    # não esquecer de adicionar a última linha
    if current_line:
        pergunta_split.append(current_line)

    for p, i in zip(pergunta_split, range(len(pergunta_split))):
        pergunta = Texto(p, 'FreeSans', tam_fonte, 560, 805 + 45 * i)
        pergunta.show_texto(window, 'topleft')



def blit_alternativas(perg, alternativas):
    global window
    altern_letras = ['A: ', 'B: ', 'C: ', 'D: ']
    pos_alternativas = [(560, 920), (1075, 920), (560, 970), (1075, 970)]
    blit_pergunta(perg)
    for a, i in zip(alternativas, range(len(alternativas))):
        alternativa = Texto(altern_letras[i] + a, 'FreeSans', 36, pos_alternativas[i][0], pos_alternativas[i][1])
        alternativa.show_texto(window, 'topleft')


def blit_resposta_final(alternativas, num_alternativa, cor=(255, 255, 255)):
    global window
    if num_alternativa > 0 & num_alternativa <= len(alternativas):
        alternativa = Texto(alternativas[num_alternativa - 1], 'FreeSansBold', 48, 560, 920)
        if cor == (255, 255, 255):
            alternativa.show_texto(window, 'topleft')
        else:
            alternativa.show_texto_cor(window, 'topleft', cor)


def blit_resposta_escolhida(perg, alternativas, escolhida):
    global window
    altern_letras = ['A: ', 'B: ', 'C: ', 'D: ']
    pos_alternativas = [(560, 920), (1075, 920), (560, 970), (1075, 970)]
    blit_pergunta(perg)
    for a, i in zip(alternativas, range(len(alternativas))):
        alternativa = Texto(altern_letras[i] + a, 'FreeSans', 36, pos_alternativas[i][0], pos_alternativas[i][1])
        if a == escolhida:
            alternativa.show_texto_cor(window, 'topleft', 'blue')
        else:
            alternativa.show_texto(window, 'topleft')


def blit_certo_errado(perg, alternativas, escolhida, resposta_certa):
    global window
    altern_letras = ['A: ', 'B: ', 'C: ', 'D: ']
    pos_alternativas = [(560, 920), (1075, 920), (560, 970), (1075, 970)]
    blit_pergunta(perg)
    for a, i in zip(alternativas, range(len(alternativas))):
        alternativa = Texto(altern_letras[i] + a, 'FreeSans', 36, pos_alternativas[i][0], pos_alternativas[i][1])
        if (a == escolhida) and (a == resposta_certa):
            alternativa.show_texto_cor(window, 'topleft', (0, 175, 0))
        elif a == escolhida:
            alternativa.show_texto_cor(window, 'topleft', (220, 0, 0))
        elif a == resposta_certa:
            alternativa.show_texto_cor(window, 'topleft', (0, 175, 0))
        else:
            alternativa.show_texto(window, 'topleft')


def seleciona_pergunta(rodada):
    global df_perguntas
    df = df_perguntas.copy()
    df = df[~df['used']]  # Pegando somente as perguntas que não foram feitas

    if df[df['alternativas'] == 3].shape[0] == 0 or \
            df[df['alternativas'] == 4].shape[0] == 0 or \
            df[df['alternativas'] == 5].shape[0] < 8:
        df_perguntas['used'] = False  # Se não houver mais perguntas a serem selecionadas, reinicia a base.
        df = df_perguntas.copy()
        df = df[~df['used']]

    if rodada <= 2:
        df = df[df['alternativas'] == 3]
        list_index = df.index.to_list()
        pos_pergunta = random.choice(list_index)
        df_aux = df.loc[pos_pergunta]
        pergunta = df_aux['pergunta']
        alternativas = [df_aux['resposta_certa'], df_aux['alternativa_1'], df_aux['alternativa_2']]
        alt_aux = [df_aux['resposta_certa'], df_aux['alternativa_1'], df_aux['alternativa_2']]
        emb = str(df_aux['embaralhar'])
        if emb.isdigit():
            for option, i in zip(emb, range(len(alternativas))):
                option = int(option)
                alternativas[i] = alt_aux[option - 1]
        else:
            shuffle(alternativas)
        df_perguntas.loc[df_perguntas['pergunta'] == pergunta, 'used'] = True

        return pergunta, alternativas, df_aux['resposta_certa']
    elif rodada <= 4:
        df = df[df['alternativas'] == 4]
        list_index = df.index.to_list()
        pos_pergunta = random.choice(list_index)
        df_aux = df.loc[pos_pergunta]
        pergunta = df_aux['pergunta']
        alternativas = [df_aux['resposta_certa'], df_aux['alternativa_1'],
                        df_aux['alternativa_2'], df_aux['alternativa_3']]
        alt_aux = [df_aux['resposta_certa'], df_aux['alternativa_1'],
                   df_aux['alternativa_2'], df_aux['alternativa_3']]
        emb = str(df_aux['embaralhar'])
        if emb.isdigit():
            for option, i in zip(emb, range(len(alternativas))):
                option = int(option)
                alternativas[i] = alt_aux[option - 1]
        else:
            shuffle(alternativas)
        df_perguntas.loc[df_perguntas['pergunta'] == pergunta, 'used'] = True
        return pergunta, alternativas, df_aux['resposta_certa']
    else:
        df = df[df['alternativas'] == 5]

        df = df.sample(n=8)
        list_perguntas = []
        list_index = df.index.to_list()
        opcoes = ['A: ', 'B: ', 'C: ']
        for pergunta, alt1 in zip(df['pergunta'], df['resposta_certa']):
            alternativas = pergunta.split('.')[0].replace(' ou ', ', ').split(', ')
            for i in range(len(alternativas)):
                alternativas[i] = opcoes[i] + alternativas[i]
            list_perguntas.append({'pergunta': pergunta, 'certa': alt1, 'status': False, 'alternativas': alternativas})
        for index in list_index:
            df_perguntas.loc[index, 'used'] = True
        return list_perguntas


def wait_until_enter(segundos, mus=''):
    global sair_do_jogo
    loop_jogo = True
    start = pygame.time.get_ticks()
    pygame.event.clear()
    while loop_jogo:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if sair_do_jogo.check_click():
                    pygame.mixer.stop()
                    menu_principal()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    loop_jogo = False
                if ev.key == pygame.K_F1:
                    segundos = segundos * 10
                if ev.key == pygame.K_F2:
                    if mus != '':
                        pygame.mixer.stop()
                        sons[mus].play()
                if ev.key == pygame.K_F3:
                    pygame.mixer.stop()
                if ev.key == pygame.K_F4:
                    pygame.mixer.stop()
                    sons['final_inicio'].play()
                if ev.key == pygame.K_p:
                    loop_pause = True
                    while loop_pause:
                        frase = Texto('JOGO PAUSADO', 'FreeSansBold', 72, 960, 760, cor=(255, 0, 0))
                        frase.show_texto_cor(window, align='center', color=(0, 0, 0))
                        pygame.display.update()
                        for ev in pygame.event.get():
                            if ev.type == pygame.KEYDOWN:
                                if ev.key == pygame.K_p:
                                    loop_pause = False
        time = pygame.time.get_ticks() - start
        if time > (segundos * 1000):
            loop_jogo = False


def get_pulso(pulso_anterior):
    dif_anterior = randint(-2, 2)
    return pulso_anterior + dif_anterior


def todos_bots(jogadores):
    for pl in jogadores:
        if pl.tipo == 0 and not pl.eliminado:
            return False
    return True


def mostrar_frases(frases, x_inicial=820, tam=72, enter=80, fonte='FreeSans'):
    for i, frase in enumerate(frases):
        Texto(frase, fonte, tam, 960, x_inicial + enter * i).show_texto(window, align='center')
    pygame.display.update()


def dinheiro_inicial(jogadores):
    sons['dinheiro'].play()
    for _ in range(15):
        for j in jogadores:
            j.dinheiro = randint(100, 999)
        blit_all(sair_do_jogo, essentials, jogadores, display_update=True)
        pygame.time.delay(40)

    for j in jogadores:
        j.dinheiro = 1000
    blit_all(sair_do_jogo, essentials, jogadores, display_update=True)

def exibir_pulso(pulso, bpm_txt, img_pulso):
    img_pulso.update_image(f'img/pulso/pulso-{pulso}.png')
    img_pulso.draw(window)
    if pulso == 0:
        bpm_txt = get_pulso(bpm_txt)
    Texto(str(bpm_txt), 'FreeSans', 36, 770, 745).show_texto(window, 'center')
    return (pulso + 1) % 60, bpm_txt


def iniciar_jogo():
    global window, essentials, sair_do_jogo, df_perguntas, img_pergunta, sons, quedas
    for som in sons.keys():
        sons[som].stop()
    
    window.fill('black')
    df_jogadores = pd.read_json("players.json")
    jogadores = []
    zonas_de_risco = [[0], [0, 3], [0, 2, 4], [0, 2, 3, 4], [0, 1, 2, 3, 4]]
    dinheiro_rodada = [1000, 1200, 1500, 2000, 5000, 10000]
    qtd_alternativas = [3, 3, 4, 4]

    sons['tema'].play(0)
    for i, row in enumerate(df_jogadores.itertuples(index=False), start=1):
        jogadores.append(Jogador(row.nome, i, row.tipo))

    img_pulso = Image("img/pulso/pulso-0.png", 830, 726)

    logo_programa()
    sons['aplausos2'].play()
    roleta.update_image('img/roleta_inicio.png')
    img_dados.update_image('img/jogadores.png')
    blit_vermelho(sair_do_jogo, essentials, jogadores, range(0, 6))
    pygame.display.update()
    wait_until_enter(10)
    blit_all(sair_do_jogo, essentials, jogadores, display_update=True)

    # VAI COMEÇAR O ROLETA RUSSA!
    pygame.mixer.stop()
    sons['tema'].stop()
    sons['prejogo'].play()
    comeco_jogo()
    pygame.display.update()
    wait_until_enter(5)

    blit_all(sair_do_jogo, essentials, jogadores, display_update=True)
    pygame.mixer.stop()
    sons['buraco_abre'].play()
    assim_o(window)
    wait_until_enter(3)

    sons['start_game'].play(0)
    wait_until_enter(2)
    blit_all(sair_do_jogo, essentials, jogadores)
    mostrar_frases([
        'Vamos distribuir R$ 1.000,00 para cada ',
        'um no começo deste jogo e jogar a ',
        'roleta para decidir quem começa jogando!'
    ])

    wait_until_enter(5)
    # Distribuindo dinheiro para cada jogador!
    dinheiro_inicial(jogadores)

    roleta.update_image('img/roleta.png')
    pygame.display.update()
    nao_respondeu_nunca = [pl for pl in jogadores if not pl.eliminado]
    # RODADAS ELIMINATÓRIAS
    for rodada in range(1, 5):
        blit_all(sair_do_jogo, essentials, jogadores, rodada, display_update=True)

        # Primeiro, veremos quem é líder
        lider = get_leader(jogadores)

        if lider is not None:
            desafiante = lider
        else:
            # Não há líder — roleta decide quem começa
            alavanca.update_image('img/alavanca2-0.png')
            roleta.update_image('img/roleta.png')
            blit_all(sair_do_jogo, essentials, jogadores, rodada, display_update=True)
            sons['tema'].stop()

            if rodada > 1:
                mostrar_frases([
                    'Temos um empate na liderança!',
                    'Portanto a roleta deve ser jogada para',
                    'decidir quem começa a rodada!'
                ])

            if todos_bots(jogadores):
                wait_until_enter(5)
                desafiante = jogar_roleta('comeco', alavanca, jogadores=jogadores)
            else:
                esperando_click = True
                while esperando_click:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                            if sair_do_jogo.check_click():
                                pygame.mixer.stop()
                                return
                            elif alavanca.check_click():
                                esperando_click = False
                        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                            esperando_click = False

                desafiante = jogar_roleta('comeco', alavanca, jogadores=jogadores)
        sons['tema'].stop()
        mostrar_frases(['Vamos começar a ' + str(rodada) + 'ª rodada', 'da Roleta Russa!'])
        
        wait_until_enter(6)
        pygame.mixer.stop()
        for som in sons.keys():
            sons[som].stop()
        sons['round'].play()
        wait_until_enter(1)
        sons['aplausos1'].play()
        wait_until_enter(1)
        blit_all(sair_do_jogo, essentials, jogadores, rodada)

        if not sem_locale:
            frase_dist = [
                f"Cada resposta certa valerá {locale.currency(dinheiro_rodada[rodada - 1], grouping=True)}, e",
                f"teremos {qtd_alternativas[rodada - 1]} alternativas para cada pergunta!"
            ]
        else:
            frase_dist = [
                f"Cada resposta certa valerá R$ {dinheiro_rodada[rodada - 1]}, e",
                f"teremos {qtd_alternativas[rodada - 1]} alternativas para cada pergunta!"
            ]

        # Ajustes para a rodada 4
        if rodada == 4:
            frase_dist.extend([
                "Agora é possível responder você mesmo ou",
                "passar para seu adversário se for o desafiante!"
            ])
            mostrar_frases(frase_dist, x_inicial=740, tam=64, enter=72)
        else:
            mostrar_frases(frase_dist)
        pygame.display.update()
        wait_until_enter(15)
        pygame.mixer.stop()
        jog_eliminado = False

        nao_respondeu = [pl for pl in jogadores if not pl.eliminado]
        # PERGUNTAS
        for num_pergunta in range(5):
            if jog_eliminado:
                continue
            pygame.mixer.stop()
            alavanca.update_image('img/alavanca1-0.png')
            roleta.update_image('img/roleta_inicio.png')
            sons['zonas_de_risco'].play(0)
            blit_vermelho(sair_do_jogo, essentials, jogadores, zonas_de_risco[num_pergunta])
            sons['question'].play(loops=5)
            pergunta, alternativas, resposta_certa = seleciona_pergunta(rodada)
            wait_time = uniform(2, 7)
            wait_until_enter(wait_time)  # Um tempinho de ‘suspense’
            roleta.update_image('img/roleta.png')
            img_pergunta.update_image('img/pergunta_espera.png')
            blit_all(sair_do_jogo, essentials, jogadores, rodada)
            blit_pergunta(pergunta)
            pygame.display.update()
            if desafiante.tipo == 0:
                escolhido = passa_pra_quem(get_escolhas(jogadores, desafiante), sair_do_jogo)
            else:
                wait_time = uniform(5, 20)
                wait_until_enter(wait_time)

                escolhido = desafiante.bot_escolhe(get_escolhas(jogadores, desafiante), get_leader(jogadores),
                                                   nao_respondeu, nao_respondeu_nunca, rodada, num_pergunta + 1,
                                                   dinheiro_rodada[rodada - 1])
            if escolhido is None:
                return
            if escolhido in nao_respondeu:
                nao_respondeu.remove(escolhido)
            if escolhido in nao_respondeu_nunca:
                nao_respondeu_nunca.remove(escolhido)

            roleta.update_image("img/roleta_" + str(escolhido.pos) + ".png")
            blit_all(sair_do_jogo, essentials, jogadores, rodada)
            blit_pergunta(pergunta)
            pygame.display.update()
            pygame.mixer.stop()
            sons['chosen'].play(loops=5)

            # PASSOU PARA ALGUÉM — Sem alternativas ainda
            wait_time = 15 if escolhido.tipo == 0 else 4
            wait_until_enter(wait_time, mus='chosen')
            blit_all(sair_do_jogo, essentials, jogadores, rodada)
            blit_alternativas(pergunta, alternativas)
            pygame.display.update()
            # Um tempo para ler as alternativas
            bpm_txt = get_pulso(randint(70, 160))
            pulso = 0
            start = pygame.time.get_ticks()
            # PASSOU PARA ALGUÉM — Mostra alternativas
            loop_jogo = True
            wait_pc = 9000
            time_limit = 25000 if escolhido.tipo == 0 else wait_pc

            while loop_jogo:
                blit_all(sair_do_jogo, essentials, jogadores, rodada)
                blit_alternativas(pergunta, alternativas)

                pulso, bpm_txt = exibir_pulso(pulso, bpm_txt, img_pulso)
                pygame.display.update()
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                    elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        if sair_do_jogo.check_click():
                            pygame.mixer.stop()
                            return
                    elif ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_RETURN:
                            loop_jogo = False
                        elif ev.key == pygame.K_F1:
                            time_limit *= 10

                if pygame.time.get_ticks() - start > time_limit:
                    loop_jogo = False
            img_pergunta.update_image('img/pergunta.png')
            img_pulso.draw(window)
            pygame.display.update()
            start = pygame.time.get_ticks()
            loop_jogo = True

            resposta_escolhida = ''
            # TEMPO!
            if escolhido.tipo != 0:
                pos_resp_escolh, tempo_restante = escolhido.bot_responde(
                    rodada,
                    alternativas=alternativas,
                    resposta_certa=resposta_certa,
                    desafiante=desafiante,
                    escolhido=escolhido
                )

            while loop_jogo:
                time = (15000 - (pygame.time.get_ticks() - start)) / 1000
                seg_texto = str(int(ceil(time))) if time > 0 else '1'
                seg = Texto(seg_texto, 'ArialBlack', 120, 428, 924)

                blit_all(sair_do_jogo, essentials, jogadores, rodada)
                blit_alternativas(pergunta, alternativas)

                pulso, bpm_txt = exibir_pulso(pulso, bpm_txt, img_pulso)

                seg.show_texto(window, 'center')
                pygame.display.update()

                # Som de contagem regressiva
                if time % 1 > 0.9 and time > 0:
                    som = 'sec' if time > 5 else 'sec_finais'
                    sons[som].play(0)
                    pygame.time.delay(100)

                # Bot responde automaticamente
                if escolhido.tipo != 0 and time < tempo_restante:
                    resposta_escolhida = alternativas[pos_resp_escolh - 1]
                    blit_resposta_escolhida(pergunta, alternativas, resposta_escolhida)
                    pygame.display.update()
                    respondeu = True
                    loop_jogo = False

                # Eventos comuns
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        if sair_do_jogo.check_click():
                            pygame.mixer.stop()
                            return

                    # Resposta do jogador
                    if escolhido.tipo == 0 and ev.type == pygame.KEYDOWN:
                        key_map = {
                            pygame.K_a: 0, pygame.K_1: 0, pygame.K_KP1: 0,
                            pygame.K_b: 1, pygame.K_2: 1, pygame.K_KP2: 1,
                            pygame.K_c: 2, pygame.K_3: 2, pygame.K_KP3: 2,
                            pygame.K_d: 3, pygame.K_4: 3, pygame.K_KP4: 3
                        }

                        index = key_map.get(ev.key)
                        if index is not None and index < len(alternativas):
                            # Condicional extra para não permitir tecla D antes da rodada 3
                            if index >= 3 and rodada < 3:
                                continue

                            resposta_escolhida = alternativas[index]
                            blit_resposta_escolhida(pergunta, alternativas, resposta_escolhida)
                            pos_resp_escolh = index + 1
                            respondeu = True
                            loop_jogo = False

                # Timeout do humano
                if escolhido.tipo == 0 and time < -3:
                    pos_resp_escolh = None
                    loop_jogo = False

            if time < -3:
                tempo_restante = 0
            elif time < 0:
                tempo_restante = 1
            else:
                tempo_restante = int(ceil(time))
            seg = Texto(str(tempo_restante), 'ArialBlack', 120, 428, 924)
            seg.show_texto(window, 'center')
            pygame.mixer.stop()
            pygame.display.update()

            # Respondeu a pergunta!
            if escolhido.tipo == 0:
                time_reveal = 20000
            else:
                time_reveal = 5000
            if respondeu:
                sons['respondeu'].play(0)
                start = pygame.time.get_ticks()
                loop_jogo = True

                while loop_jogo:
                    blit_all(sair_do_jogo, essentials, jogadores, rodada)
                    blit_alternativas(pergunta, alternativas)
                    blit_resposta_escolhida(pergunta, alternativas, resposta_escolhida)
                    seg.show_texto(window, 'center')

                    pulso, bpm_txt = exibir_pulso(pulso, bpm_txt, img_pulso)
                    pygame.display.update()

                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                            if sair_do_jogo.check_click():
                                pygame.mixer.stop()
                                return
                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_RETURN:
                                loop_jogo = False
                            elif ev.key == pygame.K_F1:
                                time_reveal = 40000

                    if pygame.time.get_ticks() - start > time_reveal:
                        loop_jogo = False

                pygame.mixer.stop()
            for som in sons.keys():
                sons[som].stop()
            blit_certo_errado(pergunta, alternativas, resposta_escolhida, resposta_certa)
            seg.show_texto(window, 'center')
            pygame.display.update()
            if resposta_escolhida == resposta_certa:
                sons['right'].play(0)
                sons['aplausos1'].play()
                pygame.time.delay(2000)
                blit_all(sair_do_jogo, essentials, jogadores, rodada, display_update=True)
                wait_until_enter(2)
                img_pergunta.update_image('img/grana.png')
                escolhido.mostra_dinheiro(window, img_pergunta)
                wait_until_enter(1)
                sons['dinheiro'].play(0)
                escolhido.ganha_dinheiro(dinheiro_rodada[rodada - 1], window, sair_do_jogo, essentials,
                                         jogadores, img_pergunta)
                pygame.display.update()
                desafiante = escolhido
                wait_until_enter(2)
            else:
                sons['wrong'].play(0)
                pygame.time.delay(1000)
                sons['bg_errado'].play(0)
                wait_until_enter(5)
                if escolhido.dinheiro > 0:
                    sons['dinheiro'].play(0)
                    sons['aplausos1'].play()

                if desafiante != escolhido:
                    if escolhido.dinheiro > 0:
                        desafiante.pega_dinheiro_do_outro(escolhido, window, sair_do_jogo, essentials, jogadores)
                else:
                    outro_jogador = next(pl for pl in jogadores if not pl.eliminado and pl != desafiante)
                    outro_jogador.pega_dinheiro_do_outro(escolhido, window, sair_do_jogo, essentials, jogadores)

                wait_until_enter(5)
                loop = True
                sons['zonas_de_risco'].play(0)  # VOU DESTRAVAR AS ZONAS DE RISCO
                start = pygame.time.get_ticks()
                joga_roleta = False
                time_limit = 5
                while loop:
                    segundos = (pygame.time.get_ticks() - start) / 1000
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()
                        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                            if sair_do_jogo.check_click():
                                pygame.mixer.stop()
                                return
                            if alavanca.check_click():
                                pygame.mixer.stop()
                                caiu_ou_nao = jogar_roleta('normal', alavanca, num_pergunta + 1, escolhido,
                                                           jogadores)
                                loop = False
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_SPACE:
                                pygame.mixer.stop()
                                caiu_ou_nao = jogar_roleta('normal', alavanca, num_pergunta + 1, escolhido,
                                                           jogadores)
                                loop = False
                            if ev.key == pygame.K_RETURN and escolhido.tipo != 0:
                                joga_roleta = True
                            if ev.key == pygame.K_F1 and escolhido.tipo != 0:
                                time_limit *= 10
                            if ev.key == pygame.K_F2:
                                pygame.mixer.stop()
                                sons['bg_errado'].play()
                            if ev.key == pygame.K_F3:
                                pygame.mixer.stop()
                    if (segundos > time_limit and escolhido.tipo != 0) or (joga_roleta and escolhido.tipo != 0):
                        pygame.mixer.stop()
                        caiu_ou_nao = jogar_roleta('normal', alavanca, num_pergunta + 1, escolhido, jogadores)
                        loop = False

                if caiu_ou_nao:
                    jog_eliminado = True
                    wait_until_enter(int(sons['queda'].get_length() - 1))
                    sons['tema'].play()
                else:
                    wait_until_enter(int(sons['escapou'].get_length() - 3))
                    desafiante = escolhido
                
            if not jog_eliminado:
                roleta.update_image('img/roleta.png')
                blit_all(sair_do_jogo, essentials, jogadores, rodada, display_update=True)
                wait_until_enter(1)  # Tempo de espera para próxima pergunta
        if not jog_eliminado:
            roleta.update_image('img/roleta.png')
            blit_all(sair_do_jogo, essentials, jogadores, rodada)
            wait_until_enter(1)
            alavanca.update_image('img/alavanca2-0.png')
            pygame.mixer.stop()
            sons['campainha'].play()
            pygame.time.delay(1000)
            sons['bg_fim_rodada'].play()
            wait_until_enter(20)
            # Roleta fica normal, mostra todos, e o líder (se tiver) vai para o meio
            roleta.update_image('img/roleta.png')
            lider = get_leader(jogadores)
            if lider is not None:
                lider.move_center()

            blit_all(sair_do_jogo, essentials, jogadores, rodada, display_update=True)
            loop = True
            wait_until_enter(1)
            sons['zonas_de_risco'].play()  # VOU DESTRAVAR AS ZONAS DE RISCO

            # Define se precisa esperar entrada ou não
            esperar_entrada = (
                (lider is not None and lider.tipo == 0) or
                (lider is None and not todos_bots(jogadores))
            )

            if not esperar_entrada:
                wait_until_enter(5, mus='bg_fim_rodada')
                pygame.mixer.stop()
                jogar_roleta('carrasco', alavanca, jogadores=jogadores)
            else:
                while loop:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            pygame.quit()

                        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                            if sair_do_jogo.check_click():
                                pygame.mixer.stop()
                                return
                            elif alavanca.check_click():
                                pygame.mixer.stop()
                                jogar_roleta('carrasco', alavanca, jogadores=jogadores)
                                loop = False

                        elif ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_SPACE:
                                pygame.mixer.stop()
                                jogar_roleta('carrasco', alavanca, jogadores=jogadores)
                                loop = False
                            elif ev.key == pygame.K_F2:
                                pygame.mixer.stop()
                                sons['bg_fim_rodada'].play()
                            elif ev.key == pygame.K_F3:
                                pygame.mixer.stop()
                            elif ev.key == pygame.K_F4:
                                pygame.mixer.stop()
                                sons['final_inicio'].play()

            wait_until_enter(int(sons['queda'].get_length() - 1))
            if lider is not None:
                lider.change_pos(lider.pos)
            sons['tema'].play()
        if rodada < 4:
            wait_until_enter(10)
            logo_programa()
            roleta.update_image('img/roleta_inicio.png')
            blit_vermelho(sair_do_jogo, essentials, jogadores, range(0, 6))
            pygame.display.update()
            wait_until_enter(5)
        else:
            get_leader(jogadores).move_center()
            if len(quedas[3]['vermelhos']) > 0:
                blit_queda(sair_do_jogo, essentials, jogadores, quedas[3]['vermelhos'], quedas[3]['jog_eliminado'])
            else:
                blit_queda(sair_do_jogo, essentials, jogadores, quedas[3]['vermelhos'], quedas[3]['jog_eliminado'],
                           rodada4=True)

        # RODADA FINAL
    prompt_rever_quedas(window)

    rodada = 5
    finalista = get_leader(jogadores)  # O líder é logicamente o finalista!
    alavanca.update_image('img/alavanca1-0.png')
    sons['final_inicio'].play()

    img_pergunta.update_image('img/grana.png')
    img_pergunta.draw(window)
    finalista.change_pos(2)
    roleta.update_image('img/roleta_inicio.png')
    blit_all(sair_do_jogo, essentials, jogadores, rodada)
    dinheiro_antes_final = finalista.dinheiro
    finalista.mostra_dinheiro(window, img_pergunta)
    wait_until_enter(25)

    perguntas_da_final = seleciona_pergunta(rodada)

    blit_all(sair_do_jogo, essentials, jogadores, rodada)
    mostrar_frases(['Vamos começar a 5ª e última rodada', 'da Roleta Russa!'])
    wait_until_enter(5)

    pygame.mixer.stop()
    sons['round'].play(0)
    wait_until_enter(2)
    blit_all(sair_do_jogo, essentials, jogadores, rodada)

    # Montar texto com/sem locale
    if not sem_locale:
        frase_dist = [
            f'Você terá 1 minuto para responder 8 perguntas. Cada resposta certa valerá {locale.currency(int(dinheiro_rodada[rodada - 1]), grouping=True).replace(",00", "")}. Se errar,',
            f'cai no buraco. Acertando todas, ganha um bônus de {locale.currency(int(dinheiro_rodada[rodada]), grouping=True).replace(",00", "")} e jogará a roleta com o número de',
            'buracos abertos. Se escapar, ganha o PRÊMIO MÁXIMO DE R$ 500.000!!!!!',
            'Instruções: A ou 1 seleciona a 1ª alternativa, B ou 2 a 2ª, C ou 3 a 3ª,',
            'P passa/pula a pergunta, e ENTER confirma a resposta.'
        ]
    else:
        frase_dist = [
            f'Você terá 1 minuto para responder 8 perguntas. Cada resposta certa valerá R$ {int(dinheiro_rodada[rodada - 1])}. Se errar,',
            f'cai no buraco. Acertando todas, ganha um bônus de R$ {int(dinheiro_rodada[rodada])} e jogará a roleta com o número de',
            'buracos abertos. Se escapar, ganha o PRÊMIO MÁXIMO DE R$ 500.000!!!!!',
            'Instruções: A ou 1 seleciona a 1ª alternativa, B ou 2 a 2ª, C ou 3 a 3ª,',
            'P passa/pula a pergunta, e ENTER confirma a resposta.'
        ]

    mostrar_frases(frase_dist, tam=42, x_inicial=700)
    wait_until_enter(20)

    sons['zonas_de_risco'].play()
    pygame.mixer.stop()

    botao_passar = Botao('PASSAR', 150, 860, 48, align='center')
    botao_passar.show_texto(window)

    roleta.update_image('img/roleta_final_60.png')
    sons['zonas_de_risco'].play(0)
    sons['question'].play(0)

    img_pergunta.update_image('img/pergunta_espera.png')
    loop_1pergunta = True

    buracos_abertos_final = [2, 3, 4, 5, 0, 1]
    qtd_buracos_abertos = 0
    num_pergunta = 0
    num_certas = 0
    errou = False
    start = pygame.time.get_ticks()
    num_resposta = 0
    check_resposta = False
    if finalista.tipo != 0:
        num_resposta, limiar = finalista.bot_responde(
            rodada,
            pergunta_final=perguntas_da_final[num_pergunta],
            tempo_final=60
        )
        if num_resposta > 0:
            check_resposta = True
        limiar = 60
    time_limit = 20000

    while loop_1pergunta:
        blit_all(sair_do_jogo, essentials, jogadores)
        blit_pergunta(perguntas_da_final[num_pergunta]['pergunta'])
        blit_resposta_final(perguntas_da_final[num_pergunta]['alternativas'], num_resposta)

        botao_passar.show_texto(window)
        pygame.display.update()
        time = pygame.time.get_ticks() - start
        if finalista.tipo == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if botao_passar.check_click():
                        num_pergunta = (num_pergunta + 1) % 8
                        loop_1pergunta = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN and num_resposta != 0:
                        check_resposta = True
                        loop_1pergunta = False
                    if ev.key == pygame.K_p:  # Passa
                        num_pergunta = (num_pergunta + 1) % 8
                        num_resposta = 0
                        loop_1pergunta = False
                    if ev.key == pygame.K_F1:
                        time_limit = 150000
                    if ev.key == pygame.K_a or ev.key == pygame.K_1 or ev.key == pygame.K_KP1:
                        num_resposta = 1
                    if ev.key == pygame.K_b or ev.key == pygame.K_2 or ev.key == pygame.K_KP2:
                        num_resposta = 2
                    if ev.key == pygame.K_c or ev.key == pygame.K_3 or ev.key == pygame.K_KP3:
                        num_resposta = 3
            if time > time_limit:
                loop_1pergunta = False
        else:
            if time > 10000:
                if num_resposta == 0:
                    num_pergunta = (num_pergunta + 1) % 8
                loop_1pergunta = False
    
    # 60 SEGUNDOS PARA A GLÓRIA
    pygame.mixer.stop()

    for som in sons.keys():
        sons[som].stop()
    sons['final'].play()
    img_pergunta.update_image("img/pergunta.png")
    roleta.update_image("img/roleta_final_60.png")
    botao_passar = Botao('PASSAR', 150, 860, 48, align='center')

    window.fill('black')
    img_pergunta.draw(window)
    start = pygame.time.get_ticks()
    loop_final = True
    num_pergunta_aux = -1
    pergunta = perguntas_da_final[num_pergunta]
    blit_all(sair_do_jogo, essentials, jogadores, rodada)
    blit_pergunta(pergunta['pergunta'])
    pygame.event.clear()
    while loop_final:
        if check_resposta:
            correta = ['A', 'B', 'C'].index(pergunta['certa']) + 1
            if num_resposta == correta:
                pergunta['status'] = True
                num_certas += 1
                blit_resposta_final(pergunta['alternativas'], num_resposta, cor=(0, 175, 0))
                pygame.display.update()
            else:
                sons['wrong'].play()
                bota_vermelho(window, [2] + buracos_abertos_final[1+qtd_buracos_abertos:])
                mostra_jogadores(window, jogadores)
                blit_resposta_final(pergunta['alternativas'], num_resposta, cor=(220, 0, 0))
                pygame.display.update()
                pygame.time.delay(1000)
                errou = True
                break
            
            if num_certas == 8:
                break
            num_resposta = 0
            check_resposta = False
            num_pergunta = (num_pergunta + 1) % 8
            while perguntas_da_final[num_pergunta]['status']:
                num_pergunta = (num_pergunta + 1) % 8

        pergunta = perguntas_da_final[num_pergunta]
        # PULSO E TEMPO
        window.fill('black')

        # TEMPO
        time = ((72000 - (pygame.time.get_ticks() - start)) / 1000) * (60 / 72)
        if time < 0:
            roleta.update_image('img/roleta_final_0.png')
            errou = True
            break
        seg = Texto(str(int(ceil(time))), 'ArialBlack', 120, 428, 924)
        qtd_certas = Texto(f"{num_certas}/8", 'FreeSansBold', 90, 150, 960)

        # DISPLAY
        blit_all(sair_do_jogo, essentials, jogadores, rodada)
        blit_pergunta(pergunta['pergunta'])
        # blit_resposta_final(pergunta['alternativas'], num_resposta)
        seg.show_texto(window, 'center')
        qtd_certas.show_texto(window, 'center')
        botao_passar.show_texto(window)

        # BOT
        if finalista.tipo != 0:
            if num_pergunta_aux != num_pergunta:
                num_pergunta_aux = num_pergunta
                num_resposta, limiar = finalista.bot_responde(rodada, pergunta_final=pergunta, tempo_final=time, certas=num_certas)
            if time < limiar:
                if num_resposta == 0:
                    num_pergunta = (num_pergunta + 1) % 8
                else:
                    check_resposta = True
            if time < limiar + 1:
                blit_resposta_final(pergunta['alternativas'], num_resposta)
        else:
            blit_resposta_final(pergunta['alternativas'], num_resposta)
        blit_varios_buracos(buracos_abertos_final[1:qtd_buracos_abertos + 1])

        # ZONAS E SOM
        if int(ceil(time)) % 10 == 0 and (time % 1) > 0.9 and time < 55:
            sons['buraco_abre'].play()
            qtd_buracos_abertos += 1
            pygame.time.delay(100)
        if int(ceil(time)) % 10 == 0 and (time % 1) > 0.9:
            roleta.update_image('img/roleta_final_' + str(int(ceil(time))) + '.png')
        if time % 1 > 0.9:
            sons['sec' if time > 10 else 'sec_finais'].play(0)
            pygame.time.delay(120)
        pygame.display.update()
        
        # INPUT HUMANO
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if sair_do_jogo.check_click():
                    pygame.mixer.stop()
                    return
                if botao_passar.check_click():
                    num_pergunta = (num_pergunta + 1) % 8
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    check_resposta = True
                if ev.key == pygame.K_p:
                    num_pergunta = (num_pergunta + 1) % 8
                    num_resposta = 0
                if ev.key in [pygame.K_a, pygame.K_1, pygame.K_KP1]:
                    num_resposta = 1
                if ev.key in [pygame.K_b, pygame.K_2, pygame.K_KP2]:
                    num_resposta = 2
                if ev.key in [pygame.K_c, pygame.K_3, pygame.K_KP3]:
                    num_resposta = 3

    pygame.mixer.stop()

    if errou:
        sons['queda'].play()
        finalista.eliminar(jogadores)
        finalista.dinheiro += dinheiro_rodada[rodada - 1] * num_certas
        blit_varios_buracos(buracos_abertos_final[:qtd_buracos_abertos + 1])
        pygame.display.update()
        wait_until_enter(int(sons['queda'].get_length()))
    else:
        # Acertou todas
        sons['escapou'].play()
        sons['aplausos2'].play()
        finalista.dinheiro += dinheiro_rodada[rodada - 1] * num_certas + dinheiro_rodada[rodada]
        
        roleta.update_image('img/roleta.png')
        img_pergunta.update_image("img/grana.png")
        
        for _ in range(2):  # exibe duas vezes (antes e depois da espera)
            blit_all(sair_do_jogo, essentials, jogadores, rodada)
            blit_varios_buracos(buracos_abertos_final[1:qtd_buracos_abertos + 1], c='final')
            if _ == 0:
                finalista.mostra_dinheiro(window, img_pergunta)
                wait_until_enter(int(sons['escapou'].get_length() - 3))
        pygame.display.update()

        if qtd_buracos_abertos > 0:
            mostrar_frases([
                f"Hora de jogar a roleta com {qtd_buracos_abertos} chances de cair!",
                "Se escapar, ganha R$ 500.000!"
            ])
            pygame.display.update()

            def aciona_roleta():
                pygame.mixer.stop()
                resultado = jogar_roleta(
                    'normal', alavanca,
                    chances_de_cair=qtd_buracos_abertos,
                    jogador_em_risco=finalista,
                    jogadores=jogadores,
                    final=True
                )
                return not resultado[0], resultado[1]  # venceu, vermelhos_finais

            if finalista.tipo == 0:
                loop_500000 = True
                while loop_500000:
                    for ev in pygame.event.get():
                        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and alavanca.check_click():
                            venceu, vermelhos_finais = aciona_roleta()
                            loop_500000 = False
                        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                            venceu, vermelhos_finais = aciona_roleta()
                            loop_500000 = False
            else:
                wait_until_enter(5)
                venceu, vermelhos_finais = aciona_roleta()
        else:
            venceu = True
            vermelhos_finais = []
        if venceu:
            pygame.mixer.stop()
            mostrar_frases([
                f"PARABÉNS, {finalista.nome.upper()}!",
                "VOCÊ GANHOU O PRÊMIO MÁXIMO DE R$ 500.000!",
                "VOCÊ FEZ HISTÓRIA!"
            ], fonte='FreeSansBold')
            sons['vitoria'].set_volume(vol + 0.1)
            sons['vitoria'].play()
            sons['aplausos2'].play()
            finalista.dinheiro = 500000
            wait_until_enter(int(sons['vitoria'].get_length()))
        else:
            sons['queda'].play()
            wait_until_enter(int(sons['queda'].get_length()))
    pygame.mixer.stop()
    sons['tema'].play()

    if errou:
        vermelhos_restantes = [v for v in range(6) if v not in buracos_abertos_final[:qtd_buracos_abertos + 1]]
        blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos_restantes)
        blit_varios_buracos(buracos_abertos_final[:qtd_buracos_abertos + 1])

    else:
        buracos_visiveis = buracos_abertos_final[1:qtd_buracos_abertos + 1] if venceu else buracos_abertos_final[:qtd_buracos_abertos + 1]
        blit_vermelho(sair_do_jogo, essentials, jogadores, vermelhos_finais)
        blit_varios_buracos(buracos_visiveis, c='final')
        aberto_e_vermelho = [v for v in vermelhos_finais if v in buracos_visiveis]
        blit_varios_buracos(list_buracos=aberto_e_vermelho)

    img_pergunta.update_image("img/grana.png")
    finalista.mostra_dinheiro(window, img_pergunta)
    pygame.display.update()
    sons['aplausos2'].play()

    if finalista.tipo == 0:
        df_recordes = pd.read_json("records.json")
        df_vencedor = pd.DataFrame([{
            'nome': finalista.nome,
            'dinheiro': finalista.dinheiro,
            'dinheiro_antes_final': dinheiro_antes_final,
            'final_certas': num_certas
        }])
        df_recordes = pd.concat([df_recordes, df_vencedor], ignore_index=True)
        df_recordes = df_recordes.sort_values(
            by=['dinheiro', 'final_certas', 'dinheiro_antes_final'],
            ascending=False
        ).head(10)
        df_recordes.to_json("records.json", orient="records")

    wait_until_enter(150)

    for som in sons.values():
        som.stop()
    pygame.event.clear()
    return


def fuja_vermelho():
    global window
    global essentials
    global sair_do_jogo
    global sons
    limpa_tela(window)

    for som in sons.keys():
        sons[som].stop()
    sons['tema'].play(0)
    logo_programa()
    j = []

    sons['aplausos2'].play()
    roleta.update_image('img/roleta_inicio.png')
    img_dados.update_image('img/fv/jogador.png', x=353, y=107)
    blit_vermelho(sair_do_jogo, essentials, j, range(0, 6))
    pygame.display.update()
    wait_until_enter(10)

    iniciar_fv = Botao('INICIAR JOGO', 960, 775, tam=50, align='center')
    input_jogador = InputBox(760, 705, 400, 45, text='')

    pygame.display.update()
    pygame.mixer.stop()
    sons['start_game'].play()
    loop_nome = True
    while loop_nome:

        window.fill('black')
        blit_all(sair_do_jogo, essentials, j)
        iniciar_fv.show_texto(window)

        seu_nome = Texto('Insira seu nome!', 'FreeSansBold', 36, 960, 675)
        seu_nome.show_texto(window, 'center')

        regras_fv = 'As regras são simples: A cada rodada, você joga a roleta e conforme vai escapando, seu dinheiro ' \
                    'acumula. Em cada rodada, 3 de 6 buracos contêm o \nvalor máximo, e outros, valores menores. Ao ' \
                    'escapar, pode decidir pegar o dinheiro ou seguir até o final. Se escapar de 5 vermelhos, o \n' \
                    'dinheiro é dobrado, podendo ter um máximo de R$ 500.000.\nPara selecionar o buraco, aperte um' \
                    'número de 1 a 6.'
        texto_split = regras_fv.split('\n')

        for t, i in zip(texto_split, range(len(texto_split))):
            txt_regras = Texto(t, 'FreeSans', 27, 960, 830 + 30 * i)
            txt_regras.show_texto(window, 'center')
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if sair_do_jogo.check_click():
                    pygame.mixer.stop()
                    return
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if iniciar_fv.check_click():
                    if input_jogador.text != '':
                        new_player = Jogador(input_jogador.text, 1, 0)
                        new_player.image = Image("img/fv/milton.png", 0, 0)
                        new_player.move_center(fv=True)
                        j.append(new_player)
                        loop_nome = False
            input_jogador.handle_event(ev)

        input_jogador.update()
        input_jogador.draw(window)

        pygame.display.update()

    blit_all(sair_do_jogo, essentials, j)
    pygame.display.update()
    wait_until_enter(5)

    premios = [
        [5000, 5000, 5000, 2500, 1500, 1000],
        [20000, 20000, 20000, 10000, 7500, 5000],
        [50000, 50000, 50000, 25000, 15000, 10000],
        [75000, 75000, 75000, 50000, 25000, 15000],
        [100000, 100000, 100000, 75000, 50000, 25000]
    ]

    for rodada in range(5):
        chances_de_cair = rodada + 1
        valores_buraco = shuffle(premios[0])

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if (ev.key == pygame.K_1) or (ev.key == pygame.K_KP1):
                        valor_da_roleta = valores_buraco[1]
                        break
                    if (ev.key == pygame.K_2) or (ev.key == pygame.K_KP2):
                        valor_da_roleta = valores_buraco[2]
                        break
                    if (ev.key == pygame.K_3) or (ev.key == pygame.K_KP3):
                        valor_da_roleta = valores_buraco[3]
                        break
                    if (ev.key == pygame.K_4) or (ev.key == pygame.K_KP4):
                        valor_da_roleta = valores_buraco[4]
                        break
                    if (ev.key == pygame.K_5) or (ev.key == pygame.K_KP5):
                        valor_da_roleta = valores_buraco[5]
                        break
                    if (ev.key == pygame.K_6) or (ev.key == pygame.K_KP6):
                        valor_da_roleta = valores_buraco[0]
                        break


def configuracoes():
    global window
    global volta_menu
    global sons
    global vol
    global df_perguntas
    global nome_da_base

    nome_inicial = nome_da_base
    limpa_tela(window)
    sons['start_game'].play()
    x = 60
    y = 170

    df_jogadores = pd.read_json("players.json")
    df_jogadores = df_jogadores.copy()
    input_boxes = []
    opcoes_bot = []
    config_salva = False
    tudo_salvo = Texto('Configurações salvas com sucesso!', 'FreeSansBold', tam=36, x=1880, y=985)
    tipos = []

    for n, t in zip(df_jogadores['nome'], df_jogadores['tipo']):
        input_box = InputBox(x, y, 355, 45, text=n)
        input_boxes.append(input_box)

        option_box_tipo = OptionBox(x + 360, y, 375, 45, (25, 25, 25), (120, 120, 120), selected=t)
        opcoes_bot.append(option_box_tipo)
        tipos.append(t)
        # x += 360
        y += 50

    txt_base = Texto('Base de perguntas', 'FreeSansBold', tam=48, x=1100, y=170)
    bases = [b for b in listdir('base') if '.csv' in b]

    main_loc = bases.index(nome_da_base)
    base = OptionBox(900, 220, 400, 45, (25, 25, 25), (120, 120, 120), option_list=bases, selected=main_loc)
    loop_config = True

    salvar = Botao('Salvar configurações', 1880, 880, align='topright')
    while loop_config:

        limpa_tela(window)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if volta_menu.check_click():
                    pygame.mixer.stop()
                    return
                if salvar.check_click():
                    novos_jogadores = []
                    for box in input_boxes:
                        novos_jogadores.append(str(box.text))
                    for i in range(len(novos_jogadores)):
                        df_jogadores.loc[i, 'nome'] = novos_jogadores[i]
                        df_jogadores.loc[i, 'tipo'] = opcoes_bot[i].selected
                    df_jogadores.to_json("players.json", orient="records")
                    pygame.mixer.music.set_volume(vol)
                    for som in sons.keys():
                        sons[som].set_volume(vol)

                    nome_da_base = base.option_list[base.selected]
                    if nome_da_base != nome_inicial:
                        df_perguntas = pd.read_csv('base/' + nome_da_base, encoding='utf-8', sep=';')
                        df_perguntas['used'] = False
                        df_perguntas = df_perguntas.fillna('-')

                        nome_inicial = nome_da_base
                    config_salva = True
                for i in range(len(tipos)):
                    opcoes_bot[i].update(ev)
                base.update(ev)

            if ev.type == pygame.QUIT:
                pygame.quit()
            for box in input_boxes:
                box.handle_event(ev)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_MINUS:
                    vol -= 0.1
                    vol = 0 if vol < 0 else vol
                    # pygame.mixer.music.set_volume(vol)
                if ev.key == pygame.K_EQUALS or ev.key == pygame.K_PLUS:
                    vol += 0.1
                    vol = 1 if vol > 1 else vol
                    # pygame.mixer.music.set_volume(vol)

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(window)

        volta_menu.show_texto(window)
        if config_salva:
            tudo_salvo.show_texto(window, align='topright')

        titulo = Texto('CONFIGURAÇÕES', 'FreeSansBold', 48, 960, 40)
        titulo.show_texto(window, 'center')

        txt_jogadores = Texto('Jogadores', 'FreeSansBold', 48, 45, 100)
        txt_jogadores.show_texto(window, 'topleft')

        txt_controles = Texto('Como jogar: ', 'FreeSansBold', 48, 45, 450)
        txt_controles.show_texto(window, 'topleft')

        txt_controles_1 = Texto('ESPAÇO - Jogar a roleta ', 'FreeSans', 30, 60, 525)
        txt_controles_1.show_texto(window, 'topleft')

        txt_controles_1 = Texto(
            'ENTER - Pular (caso alguma ação do jogo esteja demorando); Inserir resposta na rodada final',
            'FreeSans', 30, 60, 575)
        txt_controles_1.show_texto(window, 'topleft')

        txt_controles_2 = Texto('Para passar a pergunta - Clicar no número do jogador ou digitar o número do jogador',
                                'FreeSans', 30, 60, 625)
        txt_controles_2.show_texto(window, 'topleft')

        txt_controles_2 = Texto('Para responder a pergunta - Digitar a letra da alternativa (A a D) ou o número (1 a '
                                '4)',
                                'FreeSans', 30, 60, 675)
        txt_controles_2.show_texto(window, 'topleft')

        txt_controles_2 = Texto('P - Pausar o jogo (menos na rodada final). Na rodada final, pula a pergunta.',
                                'FreeSans', 30, 60, 725)
        txt_controles_2.show_texto(window, 'topleft')

        txt_volume = Texto('Volume: ' + str(int(vol * 100)) + '%', 'FreeSansBold', 48, 45, 800)
        txt_volume.show_texto(window, 'topleft')

        txt_volume = Texto('+ - aumenta o volume; - diminui o volume', 'FreeSansBold', 36, 45, 860)
        txt_volume.show_texto(window, 'topleft')

        txt_base.show_texto(window, 'center')

        salvar.show_texto(window)

        for op in opcoes_bot:
            if not op.draw_menu:
                op.draw(window)
        for op in opcoes_bot:
            if op.draw_menu:
                op.draw(window)
        base.draw(window)

        pygame.display.update()


def mostra_regras():
    global window
    global volta_menu
    limpa_tela(window)
    sons['question'].play()
    titulo = 'REGRAS: ROLETA RUSSA'
    frase = '"Um vacilo, um erro, e um de vocês irá para o buraco. ASSIM Ó!" - Milton Neves'

    # Fonte usada para medir largura
    import pygame.freetype
    font_path = 'fonts/FreeSans.ttf'
    font_size = 27
    font = pygame.freetype.Font(font_path, font_size)
    max_width = 1840

    # Texto bruto (sem quebras)
    texto_bruto = (
        'O jogo possui exatamente 6 buracos, 5 jogadores, 4 rodadas de eliminação e a rodada final. No início do '
        'jogo, cada jogador recebe R$ 1.000. Ao final de cada uma das rodadas, um jogador é eliminado. Cada rodada '
        'tem até 5 perguntas, que serão repassadas de jogador para jogador, com exceção da 4ª rodada, onde é possível '
        'repassar para si mesmo. O jogador terá 15 segundos para responder a pergunta. Se não responder, é eliminado '
        'e cai no buraco automaticamente, perdendo seu dinheiro para o desafiante e encerrando a rodada. Se acertar a '
        'pergunta, ele ganha dinheiro. Mas se errar, ele perde seu dinheiro para o desafiante e deverá jogar a roleta '
        'com uma determinada chance de cair, representada pela quantidade de buracos vermelhos apresentados antes da '
        'pergunta. Se o vermelho não parar no jogador, a rodada continua e ele será o próximo desafiante, caso não '
        'seja a última pergunta da rodada. Caso pare, o jogador cai no buraco, está eliminado e a rodada está '
        'encerrada. A cada pergunta, o risco de cair aumenta. Na 1ª pergunta, um erro dá 1 chance em 6 de cair, na 2ª '
        'pergunta, serão 2 chances de cair e assim por diante até a 5ª pergunta. Se após as 5 perguntas, ninguém for '
        'eliminado, o jogador que tiver mais dinheiro entre todos, denominado líder, está imune e jogará a roleta para '
        'eliminar um de seus oponentes. Caso haja um empate entre dois ou mais jogadores, ninguém fica imune e a '
        'roleta deverá ser jogada com todos os jogadores tendo chance de cair. O jogador que for eliminado terá seu '
        'dinheiro repartido igualmente entre os jogadores restantes. Da 1ª à 4ª rodada, os valores da resposta certa '
        'são R$ 1.000, R$ 1.200, R$ 1.500 e R$ 2.000, respectivamente. Nas 1ª e 2ª rodadas, cada pergunta terá 3 '
        'alternativas de resposta, e na 3ª e 4ª rodadas, serão 4 alternativas de resposta. Ao restar 1 jogador apenas, '
        'este será o finalista e participará da rodada final. O finalista já tem garantido, no mínimo, todo o dinheiro '
        'acumulado até então no jogo. Na rodada final, ele terá 1 minuto para responder corretamente 8 perguntas. A '
        'cada 10 segundos, um buraco se abre. Caso a resposta esteja certa, ele ganha R$ 5.000, se não souber ele pode '
        'passar a pergunta e respondê-la em outro momento. Se ele errar ou o tempo acabar, o jogador cai no buraco '
        'ganhando o dinheiro inicial + R$ 5.000 por cada resposta certa. Se conseguir acertar as 8 perguntas em menos '
        'de 1 minuto, a contagem é parada, e além dos R$ 5.000 por cada resposta certa, receberá um adicional de '
        'R$ 10.000, totalizando R$ 50.000 por ter passado pelas 8 perguntas. Depois, são contados os buracos abertos '
        'durante as perguntas para ver quantas chances o finalista terá para ganhar o prêmio máximo de R$ 500.000. '
        'Por exemplo, se 5 buracos se abriram, a roleta será jogada com 5 chances de cair e 1 de continuar. Se o '
        'finalista escapar do vermelho, ganha os R$ 500.000. Caso contrário, ele cai no buraco, mas com todo o dinheiro '
        'ganho até então.'
    )

    # Quebra de linha automática
    palavras = texto_bruto.split()
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        tentativa = f"{linha_atual} {palavra}".strip()
        largura = font.get_rect(tentativa).width
        if largura <= max_width:
            linha_atual = tentativa
        else:
            linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)

    # Título
    txt_titulo = Texto(titulo, 'FreeSansBold', 48, 960, 40)
    txt_titulo.show_texto(window, 'center')

    volta_menu.show_texto(window)

    # Renderizar texto linha por linha
    for i, linha in enumerate(linhas):
        txt = Texto(linha, 'FreeSans', font_size, 45, 80 + 35 * i)
        txt.show_texto(window, 'topleft')

    txt_frase = Texto(frase, 'FreeSansBold', 48, 960, 1020)
    txt_frase.show_texto(window, 'center')

    # Loop
    loop_regras = True
    while loop_regras:
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if volta_menu.check_click():
                    pygame.mixer.stop()
                    loop_regras = False


def mostra_creditos():
    global window
    global volta_menu
    limpa_tela(window)
    volta_menu.show_texto(window)
    sons['creditos'].play()

    titulo = 'CRÉDITOS'
    txt_titulo = Texto(titulo, 'FreeSansBold', 48, 960, 40)
    txt_titulo.show_texto(window, 'center')

    cred = [
        'Códigos e imagens - Alex Torres',
        'Tecnologias utilizadas - Biblioteca Pygame',
        'Músicas de fundo - Network Music Ensemble (c) 2011',
        'Inspiração de código - QWERule Studios (autores da versão russa do jogo que colocaram parte do código no GitHub)',
        'Criação do formato de jogo e outras músicas de fundo e sons - Gunnar Wetterberg e Sony Pictures Television'
    ]

    agrad = 'AGRADECIMENTOS'
    list_ag = [
        '- Jesus Cristo. Primeiramente e principalmente, a Ele, pois sem Ele nada sou. O desejo de fazer o jogo da versão brasileira do Roleta Russa (havia as versões americana e russa) sempre esteve na minha mente e só consigo ver Ele como a pessoa que nunca tirou esse pensamento da mente. Foi somente quando encontrei uma por uma as músicas de fundo usadas quando vi que esse jogo poderia ser feito. Não é dos mais sofisticados, na verdade é o primeiro jogo que fiz, mas é feito com muito amor. Não tenho intenção de lucrar com o jogo (tanto que está no GitHub) nem infringir direitos autorais, apenas de divertir (e dar um upgrade no currículo, né?).',
        '- Meus pais Alex & Juliana - Por me fazerem a pessoa que eu sou. Inclusive eles assistiam o programa e eu por consequência também, aos meros 5 anos. E gostei tanto do programa que fiz um jogo.',
        '- Misael Castro - Meu discipulador que me motivou a fazer o jogo após eu ter encontrado as músicas utilizadas no programa.',
        '- Alexandre Simplício - Líder da minha célula que inspira muito a todos em seu redor.',
        '- Emilia Tainá - Amiga de célula, professora de português que revisou meus textos do jogo.',
        '- Célula HOME (@gdshome no Instagram) - Ter amigos como vocês é 1000000x melhor do que escapar de 5 vermelhos.',
        '- RecordTV - Por ter trazido este magnífico programa à televisão brasileira.',
        '- Milton Neves - Por ter conduzido cada Roleta Russa com maestria, emoção e dedicação. Olho para o Milton e continuo o associando muito mais ao Roleta Russa do que programas esportivos.',
        '- Stack Overflow - E qual programador não agradeceria?'
    ]

    font = pygame.font.Font('fonts/FreeSans.ttf', 30)
    max_width = 1700
    y = 80

    for linha in cred:
        palavras = linha.split()
        linha_atual = ""
        for palavra in palavras:
            tentativa = f"{linha_atual} {palavra}".strip()
            largura = font.size(tentativa)[0]
            if largura <= max_width:
                linha_atual = tentativa
            else:
                txt = Texto(linha_atual, 'FreeSans', 30, 100, y)
                txt.show_texto(window, 'topleft')
                y += 35
                linha_atual = palavra
        if linha_atual:
            txt = Texto(linha_atual, 'FreeSans', 30, 100, y)
            txt.show_texto(window, 'topleft')
            y += 35

    # Título dos agradecimentos
    txt_titulo_2 = Texto(agrad, 'FreeSansBold', 48, 960, y + 50)
    txt_titulo_2.show_texto(window, 'center')
    y += 100

    for bloco in list_ag:
        if bloco.strip() == "":
            y += 16  # espaço extra
            continue
        palavras = bloco.split()
        linha_atual = ""
        primeira_linha = True
        for palavra in palavras:
            tentativa = f"{linha_atual} {palavra}".strip()
            largura = font.size(tentativa)[0]
            if largura <= max_width:
                linha_atual = tentativa
            else:
                if primeira_linha and bloco.strip().startswith('-'):
                    linha_atual = "     " + linha_atual
                    primeira_linha = False
                txt = Texto(linha_atual, 'FreeSans', 30, 100, y)
                txt.show_texto(window, 'topleft')
                y += 35
                linha_atual = palavra
        if linha_atual:
            if primeira_linha and bloco.strip().startswith('-'):
                linha_atual = "     " + linha_atual
            txt = Texto(linha_atual, 'FreeSans', 30, 100, y)
            txt.show_texto(window, 'topleft')
            y += 35

    loop_creditos = True
    while loop_creditos:
        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if volta_menu.check_click():
                    pygame.mixer.stop()
                    loop_creditos = False


def mostra_recordes():
    global window
    global volta_menu
    limpa_tela(window)
    volta_menu.show_texto(window)

    df_recordes = pd.read_json("records.json")
    df_recordes = df_recordes.sort_values(by=['dinheiro', 'final_certas', 'dinheiro_antes_final'], ascending=False)
    df_recordes = df_recordes.head(10)
    sons['final_inicio'].play()

    titulo = 'RECORDES'
    tam_fonte = 54
    intervalo = 72

    for n, d, daf, f, i in zip(df_recordes['nome'], df_recordes['dinheiro'],
                               df_recordes['dinheiro_antes_final'], df_recordes['final_certas'], range(10)):
        if n != '--':
            if d == 500000:
                dinheiro_final = 'R$ ' + str(d) + ' (R$ ' + str(daf) + ')'
            else:
                dinheiro_final = 'R$ ' + str(d)

            txt_dinheiro_final = Texto(dinheiro_final, 'ArialBlack', tam_fonte, 960, 235 + intervalo * i)
            txt_final = Texto(str(f) + ' de 8', 'FreeSans', tam_fonte, 1560, 235 + intervalo * i)
        else:
            txt_dinheiro_final = Texto('--', 'ArialBlack', tam_fonte, 960, 235 + intervalo * i)
            txt_final = Texto('--', 'FreeSans', tam_fonte, 1560, 235 + intervalo * i)
        txt_nome = Texto(n, 'FreeSansBold', tam_fonte, 330, 235 + intervalo * i)

        txt_nome.show_texto(window, 'center')
        txt_dinheiro_final.show_texto(window, 'center')
        txt_final.show_texto(window, 'center')

    txt_titulo = Texto(titulo, 'FreeSansBold', 90, 960, 60)
    txt_titulo.show_texto(window, 'center')

    txt_tabela = Texto('Campeão', 'FreeSansBold', 72, 330, 150)
    txt_tabela.show_texto(window, 'center')

    txt_tabela = Texto('Premiação', 'FreeSansBold', 72, 960, 150)
    txt_tabela.show_texto(window, 'center')

    txt_tabela = Texto('Rodada Final', 'FreeSansBold', 72, 1560, 150)
    txt_tabela.show_texto(window, 'center')

    loop_recordes = True
    while loop_recordes:

        pygame.display.update()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if volta_menu.check_click():
                    pygame.mixer.stop()
                    loop_recordes = False


def menu_principal():
    global quedas
    loop = True
    while loop:
        quedas = []
        window.fill('black')
        roleta_logo.draw(window)
        iniciar.show_texto(window)
        # fuja_verm.show_texto(window)
        config.show_texto(window)
        regras.show_texto(window)
        recordes.show_texto(window)
        creditos.show_texto(window)
        sair.show_texto(window)
        versao_do_jogo.show_texto(window, align='topleft')

        pygame.display.update()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if iniciar.check_click():
                    iniciar_jogo()
                # if fuja_verm.check_click():
                #     fuja_vermelho()
                if config.check_click():
                    configuracoes()
                if regras.check_click():
                    mostra_regras()
                if recordes.check_click():
                    mostra_recordes()
                if creditos.check_click():
                    mostra_creditos()
                if sair.check_click():
                    sys.exit()


infoObject = pygame.display.Info()
res_usuario = (infoObject.current_w, infoObject.current_h)

window = pygame.display.set_mode(DISPLAYS[get_display_index()], pygame.FULLSCREEN)
# window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

icon = pygame.image.load('img/rr_icon.png')
pygame.display.set_caption('Roleta Russa')
pygame.display.set_icon(icon)

roleta_logo = Image("img/Roleta_Russa.jpg", 0, 0)

roleta = Image("img/roleta_inicio.png", 660, 50)
img_dados = Image("img/jogadores.png", 1545, 50)
alavanca = Image("img/alavanca1-0.png", 0, 75)
essentials = [roleta, img_dados, alavanca]

iniciar = Botao('Iniciar Jogo', 1850, 25)
fuja_verm = Botao('Minigame - Fuja do Vermelho!', 1850, 150)
config = Botao('Configurações', 1850, 150)
regras = Botao('Regras', 1850, 275)
recordes = Botao('Recordes', 1850, 400)
creditos = Botao('Créditos', 1850, 850)
sair = Botao('Sair', 1850, 950)
sair_do_jogo = Botao('Sair do jogo', 10, 10, tam=30, align='topleft')
volta_menu = Botao('Voltar para o menu', 10, 10, tam=30, align='topleft')
versao_do_jogo = Texto('Versão 3.7.1', 'FreeSansBold', 48, 40, 1000)

img_pergunta = Image('img/pergunta_espera.png', 310, 680)

try:
    nome_da_base = 'main.csv'
    df_perguntas = pd.read_csv('base/main.csv', encoding='utf-8', sep=';')
except:
    nome_da_base = listdir('base')[0]
    df_perguntas = pd.read_csv('base/'+nome_da_base, encoding='utf-8', sep=';')
df_perguntas['used'] = False
df_perguntas = df_perguntas.fillna('-')

sons = load_sounds()
vol = round(0.10, 2)
for som in sons.keys():
    sons[som].set_volume(vol)
pygame.mixer.music.set_volume(vol)
main_loop = True
quedas = []
menu_principal()