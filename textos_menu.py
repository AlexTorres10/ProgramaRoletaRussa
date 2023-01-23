import pygame
from display import get_ratio


class Botao:
    def __init__(self, texto, pos_x, pos_y, tam=90, cor=(255, 255, 255), align='topright'):
        self.texto = texto
        self.pos_x = int(pos_x * get_ratio())
        self.pos_y = int(pos_y * get_ratio())
        self.tam = int(tam * get_ratio())
        self.cor = cor
        self.align = align

    def show_texto(self, w):
        texto_tracado = pygame.font.Font('fonts/FreeSansBold.ttf', self.tam).render(self.texto, True, self.cor)
        if self.align == 'topright':
            text_rect = texto_tracado.get_rect(topright=(self.pos_x, self.pos_y))
        elif self.align == 'center':
            text_rect = texto_tracado.get_rect(center=(self.pos_x, self.pos_y))
        else:
            text_rect = texto_tracado.get_rect(topleft=(self.pos_x, self.pos_y))
        # text_rect = texto_tracado.get_rect()
        # text_rect.right = 200
        w.blit(texto_tracado, text_rect)

    def check_click(self):
        mouse = pygame.mouse.get_pos()
        texto_tracado = pygame.font.Font('fonts/FreeSansBold.ttf', self.tam).render(self.texto, True, self.cor)
        if self.align == 'topright':
            text_rect = texto_tracado.get_rect(topright=(self.pos_x, self.pos_y))
        elif self.align == 'center':
            text_rect = texto_tracado.get_rect(center=(self.pos_x, self.pos_y))
        else:
            text_rect = texto_tracado.get_rect(topleft=(self.pos_x, self.pos_y))
        return text_rect.collidepoint(mouse)


class Texto:
    def __init__(self, texto, font, tam, x, y, cor=(255, 255, 255)):
        self.texto = texto
        self.font = pygame.font.Font('fonts/' + font + '.ttf', int(tam * get_ratio()))
        self.x = x
        self.y = y
        self.cor = cor

    def show_texto(self, w, align='center'):
        show = self.font.render(self.texto, True, self.cor)
        if align == 'center':
            text_rect = show.get_rect(center=(int(self.x * get_ratio()), int(self.y * get_ratio())))
        elif align == 'topleft':
            text_rect = show.get_rect(topleft=(int(self.x * get_ratio()), int(self.y * get_ratio())))
        else:
            text_rect = show.get_rect(topright=(int(self.x * get_ratio()), int(self.y * get_ratio())))

        w.blit(show, text_rect)

    def show_texto_cor(self, w, align='center', color='black'):
        show = self.font.render(self.texto, True, self.cor, color)
        if align == 'center':
            text_rect = show.get_rect(center=(int(self.x * get_ratio()), int(self.y * get_ratio())))
        elif align == 'topleft':
            text_rect = show.get_rect(topleft=(int(self.x * get_ratio()), int(self.y * get_ratio())))
        else:
            text_rect = show.get_rect(topright=(int(self.x * get_ratio()), int(self.y * get_ratio())))

        w.blit(show, text_rect)
