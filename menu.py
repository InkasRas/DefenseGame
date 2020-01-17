import pygame
from need_fncts import load_image
from all_variables import Button


class Menu(pygame.Surface):
    def __init__(self, lvl):
        super().__init__((1280, 40))
        self.fill((0, 0, 0))
        self.x = 0
        self.y = 720 - 60
        self.lvl = lvl
        self.set_alpha(120)
        self.rect = pygame.Rect((self.x, self.y), self.get_size())
        self.create_buttons()

    def draw(self, srfc):
        srfc.blit(self, (self.x, self.y))

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x, self.rect.y = x, y

    def create_buttons(self):
        self.buttons = pygame.sprite.Group()
        for i in range(self.lvl):
            font = pygame.font.Font('freesansbold.ttf', 12)
            text = font.render(str(i + 1), True, (255, 255, 255))
            archer_img = pygame.Surface((40, 40))
            archer_img.blit(pygame.transform.scale(load_image('archer/1_IDLE_003.png'), (40, 40)), (0, 0))
            archer_img.blit(text, (14, 14))
            archer_btn = Button(archer_img, 'archer' + str(i), i * 60 + 5, 0)

            wall_img = pygame.Surface((40, 40))
            pygame.draw.rect(wall_img, (128, 128, 128), ((15, 0), (10, 40)))
            wall_img.blit(text, (17, 17))
            wall_btn = Button(wall_img, 'wall' + str(i), 1280 - (i + 1) * 60 - 10 * i, 0)

            self.buttons.add(wall_btn, archer_btn)
        self.buttons.draw(self)
