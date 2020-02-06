import pygame
from need_fncts import load_image
from all_variables import *
from a_star import find_path


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl, castle):
        super().__init__()
        self.x = x
        self.y = y
        self.board_x = self.x // CELL_SIZE
        self.board_y = self.y // CELL_SIZE
        self.lvl = lvl
        self.health = enemy_lvls[lvl][0]
        self.max_health = enemy_lvls[lvl][0]
        self.force = enemy_lvls[lvl][1]
        self.run_images = []
        for i in range(7):
            self.run_images.append(pygame.transform.scale(load_image(f'enemy/_RUN/_RUN_00{i}.png', -1), (40, 40)))
        self.attack_images = []
        for i in range(7):
            self.attack_images.append(
                pygame.transform.scale(load_image(f'enemy/_ATTACK/_ATTACK_00{i}.png', -1), (40, 40)))
        self.image = self.run_images[0]
        self.img_id = 0
        self.castle = castle
        self.on_field = False
        self.radius = 10
        self.active = True
        self.is_attack = False
        self.rect = pygame.Rect((x, y), (40, 40))

    def get_board_pos(self):
        return self.board_x, self.board_y

    def hurt(self, f):
        self.health -= f
        if self.health <= 0:
            self.active = False

    def break_castle(self):
        return self.castle.hurt(self.force)

    def update_pos(self):
        if self.path is not None:
            if len(self.path) == 0:
                self.is_attack = True
                a = self.break_castle()
                print(a)
                if a is True:
                    return True
            else:
                new_pos = self.path.pop(0)
                self.board_x = new_pos[1]
                self.board_y = new_pos[0] - 1
                self.x = self.board_x * CELL_SIZE
                self.y = self.board_y * CELL_SIZE
                self.rect.x = self.x
                self.rect.y = self.y
            return False
        else:
            if self.board_x < self.castle.board_x:
                self.board_x += 1
            else:
                self.board_x -= 1
            self.x = self.board_x * CELL_SIZE
            self.rect.x = self.x

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def draw(self, srfc):
        srfc.blit(self.image, (self.x + 4, self.y + 4))
        rx = round(40 * (self.max_health - self.health) // self.max_health)
        pygame.draw.line(srfc, (255, 0, 0), (self.x, self.y - 2), (self.x + rx, self.y - 2), 2)
        pygame.draw.line(srfc, (0, 255, 0), (self.x + rx, self.y - 2), (self.x + 40, self.y - 2), 2)

    def update_img(self):
        self.img_id += 1 if self.img_id < 6 else -6
        if not self.is_attack:
            self.image = self.run_images[self.img_id]
        else:
            self.image = self.attack_images[self.img_id]

    def get_pos(self):
        return self.x, self.y
