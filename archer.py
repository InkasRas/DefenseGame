import pygame
from enemy import Enemy
import random
from need_fncts import load_image
from all_variables import *
from castle import Castle
from menu import Menu


class Archer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(load_image('archer/1_IDLE_003.png', -1), (40, 40))
        self.lvl = 0
        self.price = wall_lvls[self.lvl][0]
        self.health = wall_lvls[self.lvl][1]
        self.x = x
        self.y = y
        self.parent_cell_size = CELL_SIZE
        self.rect = pygame.Rect((x, y), self.image.get_size())
        self.name = ARCHER
        self.radius = 70

    def get_clicked(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
        return False

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
        srfc.blit(self.image, (self.x, self.y))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        srfc.blit(text, (self.x, self.y))
