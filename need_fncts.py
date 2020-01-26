import pygame
import os
import random
from all_variables import *


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


def create_enemies(lvl, number):
    from enemy import Enemy
    enemies = []
    enemies_cords = []
    chc = {'top': lambda: (
        random.randrange(0, WINDOW_W // CELL_SIZE + 1, CELL_SIZE), random.randrange(-CELL_SIZE * 4, 1, CELL_SIZE)),
           'left': lambda: (
               random.randrange(-CELL_SIZE * 4, 1, CELL_SIZE),
               random.randrange(0, WINDOW_H // CELL_SIZE + 1, CELL_SIZE)),
           'right': lambda: (random.randrange(WINDOW_W, WINDOW_W + CELL_SIZE * 4 + 1, CELL_SIZE),
                             random.randrange(0, WINDOW_H // CELL_SIZE + 1, CELL_SIZE)),
           'bottom': lambda: (random.randrange(0, WINDOW_W // CELL_SIZE + 1, CELL_SIZE),
                              random.randrange(WINDOW_H, WINDOW_H + CELL_SIZE * 4 + 1, CELL_SIZE))}
    chec_dir = {'top': lambda: (0, 10),
                'left': lambda: (10, 0),
                'right': lambda: (-10, 0),
                'bottom': lambda: (0, -10)}
    for i in range(number):
        word = random.choice(list(chc.keys()))
        cords = chc[word]()

        enemies_cords.append(cords)
        enm = Enemy(cords[0] * CELL_SIZE, cords[1] * CELL_SIZE, lvl, chec_dir[word])
        enemies.append(enm)
    return enemies, enemies_cords
