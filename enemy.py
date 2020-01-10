import pygame
from need_fncts import load_image


class Enemy:
    def __init__(self, x, y):
        self.strength = 20

        self.width = 60
        self.height = 60

        self.x = x
        self.y = y

        self.health = 100
        self.k = 25

        self.img = load_image('enemy/_ATTACK/_ATTACK_000.png', -1)
        self.img = pygame.transform.scale(self.img, (100, 100))

    def change_pos(self, x, y):
        self.x = x
        self.y = y

    def hurt(self):
        self.health -= self.k

    def get_pos(self):
        return self.x, self.y

    def draw(self, surfc):
        surfc.blit(self.img, (self.x, self.y))
