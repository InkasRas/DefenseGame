import pygame


class Cursor(pygame.sprite.Sprite):
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

    def get_pos(self):
        return self.rect.x, self.rect.y

    def change_offset(self, srfc):
        return Cursor(self.rect.x - srfc.rect.x, self.rect.y - srfc.rect.y)


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
    surface = surf.copy()
    clock = pygame.time.Clock()
    srfc = pygame.Surface((1280, 720))
    srfc.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 100)
    txt = font.render(text, True, (255, 255, 255))
    srfc.blit(txt, ((1280 - len(text)) // 2, 310))
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


def draw_cells(srfc, game, dr=False):
    for y in range(game.h):
        for x in range(game.w):
            pygame.draw.rect(srfc, (255, 255, 255),
                             pygame.Rect((x * game.cell_size, y * game.cell_size),
                                         (game.cell_size, game.cell_size)), 1)
            if dr and game.board[y][x] == CASTLE:
                pygame.draw.rect(srfc, (0, 0, 255),
                                 pygame.Rect((x * game.cell_size, y * game.cell_size),
                                             (game.cell_size, game.cell_size)))
            elif dr and game.board[y][x]:
                pygame.draw.rect(srfc, (255, 0, 0),
                                 pygame.Rect((x * game.cell_size, y * game.cell_size),
                                             (game.cell_size, game.cell_size)))


GAME_STATE_1 = 'castle_placing'
GAME_STATE_2 = 'archer/wall_placing'
GAME_STATE_3 = 'enemy_generating'
GAME_STATE_4 = '4'
GAME_STATE_5 = '5'
ARCHER = 'archer'
WALL = 'wall'
CASTLE = 'castle'
FPS = 60
CELL_SIZE = 20
pause_img = 'pause.png'
play_img = 'play.png'
help_img = 'help.png'
close_img = 'close.png'
archer_lvls = {0: (90, 3, 5), 1: (100, 4, 6), 2: (200, 5, 8)}
wall_lvls = {0: (10, 4), 1: (15, 5), 2: (20, 6)}
