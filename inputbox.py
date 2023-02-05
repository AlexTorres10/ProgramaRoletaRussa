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
                if event.key == pygame.K_RETURN:
                    resposta = self.text
                    self.text = ''
                    return resposta
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode != '~':
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(700, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((400, 400))
#     clock = pygame.time.Clock()
#     input_box1 = InputBox(100, 100, 900, 32, text='Abc')
#     input_box2 = InputBox(100, 300, 140, 32, text='Abc')
#     input_boxes = [input_box1, input_box2]
#     done = False
#
#     while not done:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)
#
#         for box in input_boxes:
#             box.update()
#
#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)
#
#         pygame.display.flip()
#         clock.tick(30)
#
#
# if __name__ == '__main__':
#     main()
#     pygame.quit()