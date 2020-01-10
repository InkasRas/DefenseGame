import pygame
from need_fncts import *


class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = pygame.transform.scale(load_image('castle.png', -1), (200, 200))
        self.radius = 100
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect()

        self.x = x
        self.y = y
        self.health = 100

    def draw(self, surfc):
        surfc.blit(self.img, (self.x, self.y))

    def change_pos(self, x, y):
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
