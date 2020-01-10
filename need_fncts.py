import pygame
import os


def load_image(name, clr_key=None):
    fullname = os.path.join('data', name)
    img = pygame.image.load(fullname).convert()
    if clr_key is not None:
        if clr_key == -1:
            clr_key = img.get_at((0, 0))
        img.set_colorkey(clr_key)
    else:
        img = img.convert_alpha()
    return img


