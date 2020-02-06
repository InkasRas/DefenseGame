import pygame
import math
from need_fncts import *
from all_variables import *
from my_placing import start_placing
from read_levels import get_level
from archer import Archer
from a_star import find_path
from enemy import Enemy
import numpy
import random


class Game:
    def __init__(self, parent_screen, lvl, enms, enms_c, music_on):
        '''
        :param parent_screen: screen to display game
        :param lvl: lvl
        :param enms: array of enemies that will be in the game
        :param enms_c: coordinates of enemies
        :param music_on: bool - music off or on
        '''
        print('NEW GAME', enms, enms_c)
        pygame.mixer_music.stop()
        print(music_on, 'gam')
        if music_on:
            pygame.mixer_music.load(GAME_SONG)
            pygame.mixer_music.set_volume(0.4)
            pygame.mixer_music.play(-1)
        self.music_on = music_on

        self.enemies = enms
        self.enemies_cords = enms_c
        self.enm = self.enemies.copy()
        self.all_enms = pygame.sprite.Group()
        self.all_enms.add(*self.enemies)

        # get info about lvl
        self.level_info = get_level(lvl)
        self.money = int(self.level_info['money'])
        self.k = float(self.level_info['k'])
        self.time = int(self.level_info['time'])
        self.enm_num = int(self.level_info['en_nm'])
        self.lvl = lvl

        self.parent = parent_screen
        self.cursor = Cursor()
        self.cell_size = CELL_SIZE
        self.w, self.h = WINDOW_W // CELL_SIZE, WINDOW_H // CELL_SIZE
        self.board = numpy.zeros((self.h, self.w), dtype=int)
        self.cell_cords = []

        self.main_surface = pygame.Surface(self.parent.get_size())

        self.bg = load_image('background.jpg')
        self.parent.blit(self.bg, (0, 0))
        moving_srfc('Wave ' + str(self.lvl + 1), self.parent)

        # player starts placing castle ,walls and archers
        # start_placing - function from my_placing.py
        self.archers, self.walls = start_placing(self, lvl)
        print(self.archers, self.walls)
        # class for finding path for enemies
        # self.path_finder = Path(self)

        pygame.mouse.set_visible(True)

        # run main loop
        self.main_loop(self.analyse_archers)

    def analyse_obstacles(self):
        draw_cells(self, True)

    def analyse_archers(self):
        for archer in self.archers:
            pygame.draw.circle(self.parent, (255, 0, 0),
                               (archer.rect.x + archer.rect.w // 2, archer.rect.y + archer.rect.h // 2),
                               archer.radius)

    def game_over(self):
        '''function for displaying game over'''
        running = True
        while running:
            self.parent.blit(self.bg, (0, 0))
            font = pygame.font.Font('freesansbold.ttf', 200)
            text = font.render('GAME OVER', True, (255, 0, 0))
            self.parent.blit(text, (0, 250))
            restart_btn = Button(pygame.transform.scale(load_image(PLAY_IMG, -1), (50, 50)), 'restart', 1280 // 2 - 50,
                                 600)
            restart_btn.draw(self.parent)
            if pygame.mouse.get_pressed():
                if restart_btn.rect.collidepoint(*pygame.mouse.get_pos()):
                    from main_menu import Main_Menu
                    screen = pygame.display.set_mode((1280, 720))
                    mn_m = Main_Menu(screen)
                    mn_m.run()
            pygame.display.flip()

    def pause(self):
        '''function for displaying pause'''
        pygame.mixer_music.load(PAUSE_SONG)
        pygame.mixer_music.play(-1)
        continue_btn = Button(pygame.transform.scale(load_image(PLAY_IMG, -1),
                                                     (100, 100)), 'continue', 1280 // 2 - 50, 360 - 50)

        font = pygame.font.Font('freesansbold.ttf', 80)
        color_ch = lambda: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        text = font.render('PAUSE', True, color_ch())
        pause_color = pygame.USEREVENT + 1
        pygame.time.set_timer(pause_color, 500)
        img = pygame.transform.scale(load_image('play.png'), (50, 50))
        f_col = color_ch()
        running = True
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
                elif evnt.type == pygame.MOUSEBUTTONDOWN:
                    if continue_btn.rect.collidepoint(*evnt.pos):
                        running = False
                elif evnt.type == pygame.KEYDOWN and evnt.key == pygame.K_ESCAPE:
                    running = False
                elif evnt.type == pause_color:
                    text = font.render('PAUSE', True,
                                       color_ch())
                    f_col = color_ch()
            self.parent.fill(f_col)
            continue_btn.draw(self.parent)
            self.parent.blit(text, (500, 200))
            pygame.display.flip()
        pygame.mixer_music.stop()

    def print_time(self):
        '''check and change time left to play the wave'''
        font = pygame.font.Font('freesansbold.ttf', 30)
        time_txt = font.render(
            str(math.floor(self.time / 60)).rjust(2, '0') + ':' + str(self.time % 60).rjust(2, '0'), True,
            (255, 255, 255))

        self.parent.blit(time_txt, (WINDOW_W - time_txt.get_size()[0], 0))

    def draw_all(self):
        self.castle.draw(self.parent)
        for wall in self.walls:
            wall.draw(self.parent)
        for archer in self.archers:
            archer.draw(self.parent)

        # self.all_enms.draw(self.parent)

    def draw_necessary(self):
        '''draws everythings that is standart'''
        self.parent.blit(self.bg, (0, 0))
        draw_cells(self.parent, self)
        self.castle.draw(self.parent)
        # [enemy.draw(self.parent) for enemy in self.enemies]
        [archer.draw(self.parent) for archer in self.archers]
        [wall.draw(self.parent) for wall in self.walls]

    def main_loop(self, fnct=None):
        '''main loop - all the left of the gme is there'''
        pause_img = pygame.transform.scale(load_image(PAUSE_IMG, -1), (50, 50))
        pause_btn = Button(pause_img, 'pause', 1200, 650)

        '''setting all timers for different events'''
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
        pygame.time.set_timer(pygame.USEREVENT + 5, 500)
        pygame.time.set_timer(pygame.USEREVENT + 6, 200)
        clock = pygame.time.Clock()

        # self.path_finder.find_path((0, 0), self.castle.get_board_pos())
        running = True
        enemy = Enemy(0, 0, self.lvl, self.castle)
        enemy.path = find_path(self, (enemy.get_board_pos()[0] + 1, enemy.get_board_pos()[1]),
                               self.castle.get_board_pos())
        print(enemy, enemy.path)
        self.enemies_w = pygame.sprite.Group()
        self.enemies_w.add(enemy)
        for ar in self.archers:
            ar.insert_enemies(self.enemies_w)
        while running:
            clock.tick(60)
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
                elif evnt.type == pygame.USEREVENT + 2:
                    self.time -= 1
                    print('self tine', self.time)
                    if self.time < 1:
                        pygame.mixer.Sound.play(pygame.mixer.Sound(CHEERS_SOUND))
                        enms, enms_c = create_enemies(1, 7)
                        Game(self.parent, self.lvl + 1, enms, enms_c, self.music_on)
                elif evnt.type == pygame.USEREVENT + 5:
                    for e in self.enemies_w:
                        if e.health <= 0:
                            self.enemies_w.remove(e)
                        else:
                            e.update_pos()
                    for archr in self.archers:
                        archr.attack_enemies()
                    if self.castle.health <= 0:
                        self.game_over()
                elif evnt.type == pygame.USEREVENT + 6:
                    for archer in self.archers:
                        archer.img_update()
                    enemy.update_img()
                if evnt.type == pygame.MOUSEBUTTONDOWN:
                    if pause_btn.rect.collidepoint(*evnt.pos):
                        pygame.mixer_music.stop()
                        self.pause()
            self.parent.blit(self.bg, (0, 0))
            if len(self.enemies_w) == 0:
                pygame.mixer.Sound.play(pygame.mixer.Sound(CHEERS_SOUND))
                enms, enms_c = create_enemies(1, 7)
                Game(self.parent, self.lvl + 1, enms, enms_c, self.music_on)
            if fnct is not None:
                fnct()
            draw_cells(self.board, self.parent)
            self.castle.draw(self.parent)
            self.draw_all()
            for e in self.enemies_w:
                e.draw(self.parent)
            pause_btn.draw(self.parent)
            self.print_time()
            pygame.display.flip()
