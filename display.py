import pygame
import pyautogui

DISPLAYS = [(1920, 1080), (1024, 576), (1152, 648), (1280, 720),
            (1600, 900), (2560, 1440), (800, 450), (1366, 768)]
displayIndex = 0
res_usuario = pyautogui.size()


def get_display_index():
    global displayIndex
    global DISPLAYS
    displayIndex = None
    if res_usuario in DISPLAYS:
        displayIndex = DISPLAYS.index(res_usuario)
    else:
        for d in DISPLAYS:
            if d[0] == res_usuario[0]:
                displayIndex = DISPLAYS.index(d)
    if displayIndex is None:
        new_display = (int(1920*get_ratio()), int(1080*get_ratio()))
        DISPLAYS.append(new_display)
    else:
        return displayIndex
    displayIndex = DISPLAYS.index(new_display)

    return displayIndex


def get_ratio():
    global res_usuario
    global DISPLAYS
    ratio = res_usuario[0] / DISPLAYS[0][0]
    return ratio


class Image:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        # need to assume a default scale, DISPLAYS[0] will be default for us
        self.rect = self.image.get_rect()
        self.posX = int(x * get_ratio())
        self.posY = int(y * get_ratio())
        self.rect.x = int(x * get_ratio())
        self.rect.y = int(y * get_ratio())
        self.defaultx = (float(self.rect[2]) / DISPLAYS[0][0]) * 100
        self.defaulty = (float(self.rect[3]) / DISPLAYS[0][1]) * 100
        # this is the percent of the screen that the image should take up in the x and y planes

    def update_size(self, ):
        self.image = image_rescaler(self.image, (self.defaultx, self.defaulty))
        self.rect = self.image.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY

    def update_image(self, path):
        self.image = image_rescaler(pygame.image.load(path), (self.defaultx, self.defaulty))

    def draw(self, window):
        resize_display(self)
        window.blit(self.image, (self.rect[0], self.rect[1]))


def image_rescaler(image, original_scale_tuple):  # be sure to restrict to only proper ratios
    new_image = pygame.transform.smoothscale(image, (int(DISPLAYS[displayIndex][0] * (original_scale_tuple[0] / 100)),
                                                     int(DISPLAYS[displayIndex][1] * (original_scale_tuple[1] / 100))))
    return new_image


def resize_display(image):
    # screen = pygame.display.set_mode(DISPLAYS[get_display_index()])
    # this is where you'd have'd probably want your sprite groups set to resize themselves
    # Just gonna call it on icon here
    image.update_size()


def blit_image(window, img):
    resize_display(img)
    window.blit(img.image, (img.rect.x, img.rect.y))


def mostra_essentials(window, essentials):
    for item in essentials:
        item.draw(window)
