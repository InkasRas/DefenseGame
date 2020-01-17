import pygame
from enemy import Enemy
import random
from need_fncts import load_image
from all_variables import *
from castle import Castle
from menu import Menu
from my_placing import start_placing
from play import Play
from enemy import Enemy
from read_levels import get_level


class Cursor(pygame.Surface):
    def __init__(self):
        super().__init__((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self, (0, 0, 0), (3, 2), 1)
        self.mask = pygame.mask.from_surface(self)
        self.rect_s = self.get_rect(center=pygame.mouse.get_pos())


class Game:
    def __init__(self, parent_screen, lvl):
        self.level_info = get_level(lvl)
        self.money = int(self.level_info['money'])
        self.k = float(self.level_info['k'])
        self.parent = parent_screen
        self.cursor = Cursor()
        self.wave = int(lvl)
        self.cell_size = CELL_SIZE
        self.w, self.h = 1280 // CELL_SIZE, 720 // CELL_SIZE
        self.board = []
        self.cell_cords = []
        for y in range(self.h):
            self.board.append([])
            for x in range(self.w):
                self.board[-1].append(False)
        self.main_surface = pygame.Surface(self.parent.get_size())
        self.bg = load_image('background.jpg')
        self.parent.blit(self.bg, (0, 0))
        self.game_state = GAME_STATE_1
        moving_srfc('Wave ' + str(self.wave + 1), self.parent)
        self.archers, self.walls = start_placing(self)
        self.all_sprites = pygame.sprite.Group()
        self.create_enemies(2)
        self.main_loop(self.analyse_archers)

    def analyse_obstacles(self):
        running = True
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
            self.parent.blit(self.bg, (0, 0))
            draw_cells(self.parent, self, True)
            pygame.display.flip()

    def analyse_archers(self):
        for archer in self.archers:
            pygame.draw.circle(self.parent, (255, 0, 0),
                               (archer.rect.x + archer.rect.w // 2, archer.rect.y + archer.rect.h // 2),
                               archer.radius)
            archer.draw(self.parent)

    def draw_necessary(self):
        self.parent.blit(self.bg, (0, 0))
        draw_cells(self.parent, self)
        self.castle.draw(self.parent)
        # [enemy.draw(self.parent) for enemy in self.enemies]
        [archer.draw(self.parent) for archer in self.archers]
        [wall.draw(self.parent) for wall in self.walls]

    def update_enemies(self, time):
        for enemy in self.enemies:
            enemy.update(time)
        print()

    def create_enemies(self, number):
        enemies = []
        enemies_cords = []
        chc = {'top': lambda: (random.randrange(0, 1301, 20), random.randrange(-100, 1, 20)),
               'left': lambda: (random.randrange(-100, 1, 20), random.randrange(0, 761, 20)),
               'bottom': lambda: (random.randrange(0, 1031, 20), random.randrange(720, 800, 20)),
               'right': lambda: (random.randrange(1800, 1860, 20), random.randrange(-100, 1, 20))}
        for i in range(number):
            # cords = chc[random.choice(list(chc.keys()))]()
            cords = chc['left']()

            enemies_cords.append(cords)
            enm = Enemy(*cords, self.castle.rect.center)
            enm.rot(cords[0] - self.castle.rect.center[0])
            enemies.append(enm)
            self.all_sprites.add(enm)
        self.enemies = enemies
        self.enemies_cords = enemies_cords
        # print(enemies_cords)

    def main_loop(self, fnct=None):
        running = True
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
                if evnt.type == pygame.MOUSEBUTTONDOWN:
                    enm = Enemy(*evnt.pos)
            self.draw_necessary()
            if fnct is not None:
                fnct()
            pygame.display.flip()
