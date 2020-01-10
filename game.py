import pygame
from enemy import Enemy
import random
from need_fncts import load_image
from all_variables import *
from castle import Castle
from menu import Menu


class Cursor(pygame.Surface):
    def __init__(self):
        super().__init__((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(self, (0, 0, 0), (3, 2), 1)
        self.mask = pygame.mask.from_surface(self)
        self.rect_s = self.get_rect(center=pygame.mouse.get_pos())


class Game:
    def __init__(self, parent_screen, wave):
        self.parent = parent_screen
        self.cursor = Cursor()
        self.wave = wave
        self.menu = Menu(0, 0)
        self.main_surface = pygame.Surface(self.parent.get_size())
        self.bg = load_image('background.jpg')
        self.parent.blit(self.bg, (0, 0))
        self.game_state = GAME_STATE_1
        self.castle_placing()

    def castle_placing(self):
        castle = Castle(0, 0)
        btn_img = pygame.transform.scale(load_image('play.png', -1), (50, 50))
        stop_btn = Button(btn_img, 'castle_btn', 1200, 650)
        running = True
        placing = False
        dx, dy = None, None
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.KEYDOWN and evnt.key == 13:
                    print('evnt.keydown', pygame.K_KP_ENTER, evnt.key)
                    self.castle = castle
                    self.arch_and_walls()
                    print('pressed', evnt.key, pygame.K_KP_ENTER)
                elif evnt.type == pygame.MOUSEBUTTONDOWN:
                    if stop_btn.rect.collidepoint(evnt.pos):
                        self.castle = castle
                        self.arch_and_walls()
                    else:
                        print(castle.rect, evnt.pos)
                        print('setting moue down')
                        print('tst')
                        placing = True
                        dx = evnt.pos[0] - castle.x
                        dy = evnt.pos[1] - castle.y
                elif evnt.type == pygame.MOUSEMOTION and placing:
                    castle.change_pos(evnt.pos[0] - dx, evnt.pos[1] - dy)
                elif evnt.type == pygame.MOUSEBUTTONUP:
                    placing = False
                    dx, dy = None, None
                elif evnt.type == pygame.QUIT:
                    exit()
            self.parent.blits(blit_sequence=((self.bg, (0, 0)), (stop_btn.img, (stop_btn.x, stop_btn.y))))
            castle.draw(self.parent)
            pygame.display.flip()

    def arch_and_walls(self):
        running = True
        while running:
            for evnt in pygame.event.get():
                if evnt.type == pygame.QUIT:
                    exit()
            self.parent.blits(blit_sequence=((self.bg, (0, 0)), (self.menu, (0, 660))))
            pygame.display.flip()

    def new_enemies(self, wave):
        enemies = []
        for i in range(10 * wave):
            enm = Enemy(random.randint(10, 1000), random.randint(10, 500))
            enemies.append(enm)
        return enemies
