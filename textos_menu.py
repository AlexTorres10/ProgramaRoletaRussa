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

class ToggleButton:
    def __init__(self, x, y, w, h, color_on=(50, 200, 50), color_off=(200, 50, 50), 
                 state=True, font='FreeSansBold', tam=30):
        self.rect = pygame.Rect(x * get_ratio(), y * get_ratio(), w * get_ratio(), h * get_ratio())
        self.color_on = color_on
        self.color_off = color_off
        self.state = state  # True = ON, False = OFF
        self.tam = tam
        self.font = pygame.font.Font('fonts/' + font + '.ttf', int(self.tam * get_ratio()))
        self.hover = False

    def draw(self, surf):
        # Cor baseada no estado
        color = self.color_on if self.state else self.color_off
        # Escurece um pouco se hover
        if self.hover:
            color = tuple(max(0, c - 30) for c in color)
        
        pygame.draw.rect(surf, color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        
        # Texto ON ou OFF
        text = "ON" if self.state else "OFF"
        msg = self.font.render(text, 1, (255, 255, 255))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mpos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover:
                self.state = not self.state  # Inverte o estado
                return True  # Retorna True se houve mudança
        return False

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state