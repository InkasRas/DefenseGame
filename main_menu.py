import pygame
from need_fncts import load_image
from game import Game
from all_variables import *


class Main_Menu(pygame.Surface):
    def __init__(self, parent_window):
        super().__init__(parent_window.get_size())
        self.parent = parent_window
        self.bg = load_image('background.jpg')
        self.button_group = pygame.sprite.Group()

        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = pygame.Surface((1, 1))
        self.cursor.rect = pygame.Rect(pygame.mouse.get_pos(), (2, 2))
        self.radius = 1

        self.play_button = pygame.sprite.Sprite()
        self.play_button.image = load_image(play_img, -1)
        self.play_button.image = pygame.transform.scale(self.play_button.image, (100, 100))
        self.play_button.rect = pygame.Rect((640 - 50, 360 - 50), self.play_button.image.get_size())
        self.play_button.radius = 50
        self.play_button.name = 'play'

        self.info_button = pygame.sprite.Sprite()
        self.info_button.image = load_image(help_img, -1)
        self.info_button.image = pygame.transform.scale(self.info_button.image, (100, 100))
        self.info_button.rect = pygame.Rect((0, 720 - 100), self.info_button.image.get_size())
        self.info_button.radius = 50
        self.info_button.name = 'info'

        self.button_group.add(self.play_button)
        self.button_group.add(self.info_button)

    def run(self):
        running = True
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
                elif evnt.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.rect = pygame.Rect(evnt.pos, (2, 2))
                    bt = pygame.sprite.spritecollide(self.cursor, self.button_group, dokill=False)
                    if len(bt) > 0:
                        if bt[0].name == 'play':
                            print(evnt.pos, 'clicked')
                            Game(self.parent, 0)
                            running = False
                        elif bt[0].name == 'info':
                            self.show_info()
            self.blit(self.bg, (0, 0))
            self.button_group.draw(self)
            self.parent.blit(self, (0, 0))
            pygame.display.flip()

    def show_info(self):
        pass


pygame.init()
screen = pygame.display.set_mode((1280, 720))
mn_m = Main_Menu(screen)
mn_m.run()
(579, 301)
