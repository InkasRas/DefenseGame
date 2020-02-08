import pygame
from all_variables import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl):
        super().__init__()
        self.lvl = lvl
        self.image = pygame.Surface((20, 80))
        self.price = wall_lvls[self.lvl][0]
        self.health = wall_lvls[self.lvl][1]
        self.max_health = wall_lvls[self.lvl][1]
        self.x = x
        self.y = y
        self.board_x = x // CELL_SIZE
        self.board_y = y // CELL_SIZE
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

    def get_board_pos(self):
        return self.board_x, self.board_y

    def hurt(self, k):
        self.health -= k

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
        self.board_x = self.x // CELL_SIZE
        self.board_y = self.y // CELL_SIZE

    def draw(self, srfc):
        sr = pygame.Surface(self.image.get_size())
        sr.blit(self.image, (0, 0))
        rx = round(20 * (self.max_health - self.health) // self.max_health)
        pygame.draw.line(srfc, (255, 0, 0), (self.x, self.y - 2), (self.x + rx, self.y - 2), 2)
        pygame.draw.line(srfc, (0, 255, 0), (self.x + rx, self.y - 2), (self.x + 20, self.y - 2), 2)
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        srfc.blit(text, (0, 0))
        srfc.blit(sr, (self.rect.x, self.rect.y))
