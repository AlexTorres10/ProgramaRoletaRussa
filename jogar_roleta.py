from textos_menu import *
from display import get_ratio

vermelho = pygame.image.load("img/vermelho.png")
vermelho = pygame.transform.smoothscale(vermelho, (int(vermelho.get_width() * get_ratio()),
                                                   int(vermelho.get_height() * get_ratio())))
azul = pygame.image.load("img/azul.png")
azul = pygame.transform.smoothscale(azul, (int(azul.get_width() * get_ratio()),
                                           int(azul.get_height() * get_ratio())))
caiu = pygame.image.load("img/caiu.png")
caiu = pygame.transform.smoothscale(caiu, (int(caiu.get_width() * get_ratio()),
                                           int(caiu.get_height() * get_ratio())))


                    #0          #1          #2            #3         #4        #5
pos_buracos = [(1062, 370), (884, 466), (717, 370), (717, 180), (884, 80), (1062, 180)]
for i in range(len(pos_buracos)):
    pos_buracos[i] = (int(pos_buracos[i][0] * get_ratio()), int(pos_buracos[i][1] * get_ratio()))


def bota_vermelho(window, list_vermelhos):
    global vermelho
    # blit_image(window, roleta)
    for pos in list_vermelhos:
        window.blit(vermelho, pos_buracos[pos])
    # pygame.display.update()


def bota_azul(window, pos_azul):
    global azul
    # blit_image(window, roleta)
    window.blit(azul, pos_buracos[pos_azul])
    pygame.display.update()


def queda(window, list_vermelhos, jogador):
    global vermelho
    global caiu
    for pos in list_vermelhos:
        window.blit(vermelho, pos_buracos[pos])

    window.blit(caiu, pos_buracos[jogador])

    pygame.display.update()


def assim_o(window):
    global vermelho
    global caiu
    global pos_buracos

    assim = Texto('ASSIM, Ó!', 'FreeSansBold', 140, 960, 820)
    assim.show_texto(window, align='center')
    pygame.display.update()

    window.blit(caiu, pos_buracos[0])

    pygame.display.update()
