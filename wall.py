import pygame
from enemy import Enemy
import random
from need_fncts import load_image
from all_variables import *
from castle import Castle
from menu import Menu


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.lvl = 0
        self.image = pygame.Surface((20, 80))
        self.price = wall_lvls[self.lvl][0]
        self.health = wall_lvls[self.lvl][1]
        self.x = x
        self.y = y
        self.parent_cell_size = CELL_SIZE
        pygame.draw.rect(self.image, (128, 128, 128), ((0, 0), (20, 80)))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        self.image.blit(text, (0, 0))
        self.rect = pygame.Rect((x, y), (20, 80))
        self.name = WALL

    def get_clicked(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
        return False

    def __str__(self):
        return 'Button ' + self.name + ' ' + str(self.rect)

    def update(self, img):
        self.image = img
        self.rect = pygame.Rect((self.x, self.y), self.image.get_size())

    def get_rect(self):
        return self.rect

    def change_pos(self, x, y):
        prom_x, prom_y = self.parent_cell_size * (x // 20), self.parent_cell_size * (y // 20)
        x = prom_x if x - prom_x < prom_x + self.parent_cell_size - x else prom_x + self.parent_cell_size
        y = prom_y if y - prom_y < prom_y + self.parent_cell_size - y else prom_y + self.parent_cell_size
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, srfc):
        sr = pygame.Surface(self.image.get_size())
        sr.blit(self.image, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        srfc.blit(text, (0, 0))
        srfc.blit(sr, (self.rect.x, self.rect.y))
