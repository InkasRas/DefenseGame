import pygame
from need_fncts import load_image
from all_variables import Button


class Menu(pygame.Surface):
    def __init__(self, x, y):
        super().__init__((120, 50))
        self.fill((0, 0, 0))
        self.x = x
        self.y = y
        # self.set_alpha(120)
        self.create_buttons()

    def draw(self, srfc):
        srfc.blit(self, (self.x, self.y))

    def change_pos(self, x, y):
        self.x = x
        self.y = y

    def create_buttons(self):
        archer_img = pygame.transform.scale(load_image('archer/1_IDLE_003.png'), (50, 50))
        archer_btn = Button(archer_img, 'arhcer', 0, 0)
        wall_img = pygame.Surface((50, 50))
        pygame.draw.rect(wall_img, (99, 9, 99), ((0, 0), (50, 50)))
        wall_btn = Button(wall_img, 'wall', 60, 0)
        self.blits(blit_sequence=((wall_img, (wall_btn.x, wall_btn.y)),
                                  (archer_img, (archer_btn.x, archer_btn.y))))
