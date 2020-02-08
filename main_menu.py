import pygame
from need_fncts import load_image, create_enemies
from game import Game
from all_variables import *
from read_levels import get_level


# starter class, run this to play game
class Main_Menu(pygame.Surface):
    def __init__(self, parent_window):
        super().__init__(parent_window.get_size())
        self.parent = parent_window
        self.bg = load_image('background.jpg')
        self.button_group = pygame.sprite.Group()

        # curasor for checking clicks
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = pygame.Surface((1, 1))
        self.cursor.rect = pygame.Rect(pygame.mouse.get_pos(), (2, 2))
        self.radius = 1

        # all the Button objects are from all_variables.py
        # button to play game
        self.play_button = pygame.sprite.Sprite()
        self.play_button.image = load_image(PLAY_IMG, -1)
        self.play_button.image = pygame.transform.scale(self.play_button.image, (100, 100))
        self.play_button.rect = pygame.Rect((WINDOW_W // 2 - 50, WINDOW_H // 2 - 50), self.play_button.image.get_size())
        self.play_button.radius = 50
        self.play_button.name = 'play'

        # button to show game info
        self.info_button = pygame.sprite.Sprite()
        self.info_button.image = load_image(HELP_IMG, -1)
        self.info_button.image = pygame.transform.scale(self.info_button.image, (50, 50))
        self.info_button.rect = pygame.Rect((0, WINDOW_H - 50), self.info_button.image.get_size())
        self.info_button.radius = 50
        self.info_button.name = 'info'

        # button to turn music on/off
        self.music_button = pygame.sprite.Sprite()
        self.music_button.image = load_image(CLOSE_IMG, -1)
        self.music_button.image = pygame.transform.scale(self.music_button.image, (50, 50))
        self.music_button.rect = pygame.Rect((60, WINDOW_H - 50), self.music_button.image.get_size())
        self.music_button.radius = 50
        self.music_button.name = 'music_off'

        # group to draw buttons
        self.button_group.add(self.play_button)
        self.button_group.add(self.info_button)
        self.button_group.add(self.music_button)

    def run(self):
        running = True
        music_on = True
        pygame.mixer_music.load(GAME_SONG)
        pygame.mixer_music.set_volume(0.4)
        pygame.mixer_music.play(-1)
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
                elif evnt.type == pygame.MOUSEBUTTONDOWN:
                    # check if mouse clicked on button
                    self.cursor.rect = pygame.Rect(evnt.pos, (2, 2))
                    bt = pygame.sprite.spritecollide(self.cursor, self.button_group, dokill=False)
                    if len(bt) > 0:
                        if bt[0].name == 'play':
                            # play - play game
                            an = get_level(0)
                            # enms, enms_c = create_enemies(0, int(an['en_nm']))
                            Game(self.parent, 0, [], [], music_on)
                            running = False
                        elif bt[0].name == 'info':
                            # info - show info
                            self.show_info()
                        elif bt[0].name == 'music_off':
                            # music - play music + resizing image to identify  the state
                            music_on = not music_on
                            if music_on:
                                pygame.mixer_music.unpause()
                                self.music_button.image = pygame.transform.scale(load_image(CLOSE_IMG, -1), (50, 50))
                                self.music_button.rect.h = self.music_button.rect.w = 50
                                self.music_button.rect.move(-10, -10)
                            else:
                                pygame.mixer_music.pause()
                                self.music_button.image = pygame.transform.scale(load_image(CLOSE_IMG, -1), (40, 40))
                                self.music_button.rect.h = self.music_button.rect.w = 40
                                self.music_button.rect.move(10, 10)

            self.blit(self.bg, (0, 0))
            self.button_group.draw(self)
            self.parent.blit(self, (0, 0))
            pygame.display.flip()

    def show_info(self):
        pass


pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
mn_m = Main_Menu(screen)
mn_m.run()
