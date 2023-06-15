import pygame
from display import get_ratio

COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:
    def __init__(self, x, y, w, h, font='FreeSansBold', tam=30, text=''):
        self.rect = pygame.Rect(x * get_ratio(), y * get_ratio(), w * get_ratio(), h * get_ratio())
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font('fonts/' + font + '.ttf', int(tam * get_ratio()))
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.espacos = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.txt_surface = self.font.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if self.espacos < 5:
                        self.text = self.text[:-1]
                        self.espacos += 1
                    else:
                        self.text = ''
                        self.espacos = 0
                # elif event.key == pygame.K_EQUALS or event.key == pygame.K_MINUS:
                #     pass
                else:
                    if event.unicode != '~':
                        self.text += event.unicode
                        self.espacos = 0
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class OptionBox:

    def __init__(self, x, y, w, h, color, highlight_color, selected=0, font='FreeSansBold',
                 option_list=None, tam=30):
        if option_list is None:
            option_list = ['Humano', 'Bot Carla Perez na Final', 'Bot Leigo',
                           'Bot Normal', 'Bot Inteligente', 'Bot Cacá Rosset na Final']
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.tam = tam
        self.font = pygame.font.Font('fonts/' + font + '.ttf', int(self.tam * get_ratio()))
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (255, 255, 255))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i == self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (255, 255, 255))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height, self.rect.width,
                          self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.selected = self.active_option
                self.draw_menu = False
                return self.active_option
        return -1
