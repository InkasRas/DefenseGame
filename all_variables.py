import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, img, name, x, y):
        super().__init__()
        self.img = img
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


GAME_STATE_1 = 'castle_placing'
GAME_STATE_2 = 'archer/wall_placing'
GAME_STATE_3 = 'enemy_generating'
GAME_STATE_4 = '4'
GAME_STATE_5 = '5'
