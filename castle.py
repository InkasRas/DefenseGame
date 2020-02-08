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
        self.board_x = 0
        self.board_y = 0
        self.health = 300
        self.max_health = 300

    def draw(self, surfc):
        surfc.blit(self.img, (self.x, self.y))
        rx = round(200 * (self.max_health - self.health) // self.max_health)
        pygame.draw.line(surfc, (255, 0, 0), (self.x, self.y - 2), (self.x + rx, self.y - 2), 3)
        pygame.draw.line(surfc, (0, 255, 0), (self.x + rx, self.y - 2), (self.x + 200, self.y - 2), 3)

    def get_rect(self):
        return self.rect

    def get_board_pos(self):
        return self.board_y, self.board_x

    def get_board_all_pos(self):
        return [[(i, j) for j in range(self.board_x, self.board_x + 200 // CELL_SIZE, 1)] for i in
                range(self.board_y, self.board_y + 200 // CELL_SIZE, 1)]

    def change_pos(self, x, y):
        if x > 0 and y > 0:
            prom_x, prom_y = self.parent_cell_size * (x // 20), self.parent_cell_size * (y // 20)
            x = prom_x if x - prom_x < prom_x + self.parent_cell_size - x else prom_x + self.parent_cell_size
            y = prom_y if y - prom_y < prom_y + self.parent_cell_size - y else prom_y + self.parent_cell_size
            self.x = x
            self.y = y
            self.rect.x = self.x
            self.rect.y = self.y
            self.board_x = self.x // CELL_SIZE
            self.board_y = self.y // CELL_SIZE

    def hurt(self, k):
        self.health -= k
        print(self.health)
        if self.health <= 0:
            return True
        return False

    def get_pos(self):
        return (self.x, self.y)
