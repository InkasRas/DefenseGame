import pygame


class Cursor(pygame.sprite.Sprite):
    '''Cursor class: used to check mouse intersection with different objects'''

    def __init__(self, x=None, y=None):
        self.image = pygame.Surface((2, 2))
        self.image.set_at((0, 1), (255, 255, 4))
        self.image.set_at((1, 0), (255, 255, 4))
        if x is None:
            self.rect = pygame.Rect(pygame.mouse.get_pos(), (2, 2))
        else:
            self.rect = pygame.Rect((x, y), (2, 2))

    def change_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        print()

    def get_pos(self):
        return self.rect.x, self.rect.y

    def change_offset(self, srfc):
        return Cursor(self.rect.x - srfc.rect.x, self.rect.y - srfc.rect.y)


class CommonClass(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl):
        super().__init__()
        self.lvl = lvl
        self.x = x
        self.y = y
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
        self.board_x = self.x
        self.board_y = self.y

    def get_board_pos(self):
        return self.board_x, self.board_y

    def draw(self, srfc):
        sr = pygame.Surface(self.image.get_size())
        sr.blit(self.image, (0, 0))
        green_l = self.health // self.max_health * 10
        red_l = 10 - green_l
        pygame.draw.line(srfc, (255, 0, 0), (self.x, self.y - 2), (self.x + red_l, self.y - 2))
        pygame.draw.line(srfc, (0, 255, 0), (self.x + red_l, self.y - 2), (self.x + red_l + green_l, self.y - 2))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        srfc.blit(text, (0, 0))
        srfc.blit(sr, (self.rect.x, self.rect.y))


class Button(pygame.sprite.Sprite):
    def __init__(self, img, name, x, y):
        super().__init__()
        self.img = img
        self.image = img
        self.name = name
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x, y), img.get_size())

    def change_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x, y), self.img.get_size())

    def draw(self, srfc):
        srfc.blit(self.img, (self.x, self.y))


def moving_srfc(text, surf):
    '''create moving surface: like "Place them"'''
    surface = surf.copy()
    clock = pygame.time.Clock()
    srfc = pygame.Surface((1280, 720))
    srfc.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 100)
    txt = font.render(text, True, (255, 255, 255))
    print('moving srfc', txt.get_size(), text)
    srfc.blit(txt, (1280 // 2 - txt.get_size()[0] // 2, 310))
    rect = pygame.Rect((-1280, 0), (1280, 720))
    v = 700
    running = True
    while running:
        if rect.x > 1280:
            running = False
        rect.x += v * clock.tick(60) / 1000
        surf.blit(surface, (0, 0))
        surf.blit(srfc, (rect.x, rect.y))
        pygame.display.flip()


def draw_cells(board, screen, dr=False, alpha=100):
    '''draw the board on the screen'''
    for y in range(WINDOW_H // CELL_SIZE):
        for x in range(WINDOW_W // CELL_SIZE):
            pygame.draw.rect(screen, pygame.Color(255, 255, 255, alpha),
                             pygame.Rect((x * CELL_SIZE, y * CELL_SIZE),
                                         (CELL_SIZE, CELL_SIZE)), 1)
            if dr and board[y, x] != CLEAR:
                pygame.draw.rect(screen, COLORS[board[y, x]],
                                 pygame.Rect((x * CELL_SIZE, y * CELL_SIZE),
                                             (CELL_SIZE, CELL_SIZE)))


WINDOW_H = 720
WINDOW_W = 1280

ARCHER = 'archer'
WALL = 'wall'

CLEAR = 0
OBSTACLE = 1
CASTLE = 2
ENEMY = 3
PATH_GREEN = 4
PATH_VIOL = 5
PATH_FOUND = 6
COLORS = {OBSTACLE: (255, 0, 0), CASTLE: (0, 0, 255), ENEMY: (255, 0, 0), PATH_GREEN: (0, 255, 0),
          PATH_VIOL: (0, 255, 255), PATH_FOUND: (128, 128, 128)}

FPS = 60

CELL_SIZE = 20

PAUSE_IMG = 'pause.png'
PLAY_IMG = 'play.png'
HELP_IMG = 'help.png'
CLOSE_IMG = 'close.png'
ARCHER_IMG = 'archer/1_IDLE_003.png'

archer_lvls = {0: (25, 3, 5), 1: (50, 4, 6), 2: (100, 5, 8)}
wall_lvls = {0: (10, 4), 1: (15, 5), 2: (20, 6)}
enemy_lvls = {0: (2, 1), 1: (3, 2), 2: (4, 3)}

PAUSE_SONG = 'data/sound/bensound-hipjazz.mp3'
GAME_SONG = 'data/sound/main_song.mp3'
CHEERS_SOUND = 'data/sound/cheers.wav'
CLICK_SOUND = 'data/sound/click.mp3'
