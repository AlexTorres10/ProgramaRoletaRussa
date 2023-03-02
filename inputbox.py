import pygame
from display import get_ratio

COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox:
    def __init__(self, x, y, w, h, font='FreeSansBold', tam=30, text=''):
        self.rect = pygame.Rect(x*get_ratio(), y*get_ratio(), w*get_ratio(), h*get_ratio())
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
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if self.espacos < 5:
                        self.text = self.text[:-1]
                        self.espacos += 1
                    else:
                        self.text = ''
                        self.espacos = 0
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_MINUS:
                    pass
                else:
                    if event.unicode != '~':
                        self.text += event.unicode
                        self.espacos = 0
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
