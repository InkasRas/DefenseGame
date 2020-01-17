import pygame
from need_fncts import load_image
from all_variables import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.strength = 20

        self.width = 60
        self.height = 60

        self.x = x
        self.y = y

        self.health = 100
        self.k = 25
        self.speed = 5
        self.pos = pygame.Vector2((x, y))
        self.vel = pygame.Vector2(30, 0)
        self.direction = pygame.Vector2(10, 0)
        self.angle = 0
        self.angle_speed = 0

        self.image = pygame.transform.scale(load_image('enemy/_RUN/_RUN_000.png', -1), (40, 40))
        self.img_num = 0
        self.rect = pygame.Rect((x, y), (40, 40))

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def update(self, time):
        self.pos += self.vel * time // 1000 + self.direction
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.img_num += 1 if self.img_num < 6 else -6
        self.image = pygame.transform.scale(load_image('enemy/_RUN/_RUN_00' + str(self.img_num) + '.png', -1), (40, 40))
        self.image = pygame.transform.rotate(self.image, -self.angle)

    def hurt(self):
        self.health -= self.k

    def rot(self, anf):
        self.angle_speed = anf
        self.angle += self.angle_speed
        self.direction.rotate_ip(self.angle_speed)
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_pos(self):
        return self.x, self.y