import pygame
from need_fncts import *
from all_variables import *


class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.transform.scale(load_image('castle.png', -1), (200, 200))
        self.radius = 100
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()
        self.parent_cell_size = CELL_SIZE
        self.x = x
        self.y = y
        self.health = 100

    def draw(self, surfc):
        surfc.blit(self.img, (self.x, self.y))

    def get_rect(self):
        return self.rect

    def change_pos(self, x, y):
        if x > 0 and y > 0:
            prom_x, prom_y = self.parent_cell_size * (x // 20), self.parent_cell_size * (y // 20)
            x = prom_x if x - prom_x < prom_x + self.parent_cell_size - x else prom_x + self.parent_cell_size
            y = prom_y if y - prom_y < prom_y + self.parent_cell_size - y else prom_y + self.parent_cell_size
            self.x = x
            self.y = y
            self.rect.x = self.x
            self.rect.y = self.y

    def hurt(self, k):
        self.health -= k
        if self.health <= 0:
            print('lost')

    def get_pos(self):
        return (self.x, self.y)