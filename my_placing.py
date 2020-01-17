import pygame
from enemy import Enemy
import random
from need_fncts import load_image
from all_variables import *
from castle import Castle
from menu import Menu
from archer import Archer
from wall import Wall


def castle_placing(game):
    castle = Castle(0, 0)
    btn_img = pygame.transform.scale(load_image('play.png', -1), (50, 50))
    stop_btn = Button(btn_img, 'castle_btn', 1200, 650)
    running = True
    placing = False
    dx, dy = None, None
    while running:
        for evnt in pygame.event.get():
            if evnt.type == pygame.KEYDOWN and evnt.key == 13:
                game.castle = castle
                fill_board(castle, game.board, val=CASTLE)
                return True
            elif evnt.type == pygame.MOUSEBUTTONDOWN:
                if stop_btn.rect.collidepoint(evnt.pos):
                    game.castle = castle
                    return True
                else:
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
        game.parent.blit(game.bg, (0, 0))
        # draw_cells(game.parent, game)
        pygame.draw.rect(game.parent, (255, 0, 0), castle.rect, 2)
        stop_btn.draw(game.parent)
        castle.draw(game.parent)

        pygame.display.flip()


def draw_cells(srfc, game):
    for y in range(len(game.board)):
        for x in range(len(game.board[-1])):
            pygame.draw.rect(srfc, (255, 255, 255, 100),
                             pygame.Rect((x * game.cell_size, y * game.cell_size),
                                         (game.cell_size, game.cell_size)), 1)


def archer_and_wall_placing(game, lvl):
    moving_srfc('Place archers\nand walls', game.parent)
    clock = pygame.time.Clock()
    cursor = Cursor()
    running = True
    archers = []
    walls = []
    game.menu = Menu(lvl + 1)
    directions = {pygame.K_DOWN: (lambda x: pygame.transform.flip(x.image, True, False)),
                  pygame.K_UP: (lambda x: pygame.transform.flip(x.image, False, True)),
                  pygame.K_LEFT: (lambda x: pygame.transform.rotate(x.image, 90)),
                  pygame.K_RIGHT: (lambda x: pygame.transform.rotate(x.image, -90))}
    img_drawing = False
    font = pygame.font.Font('freesansbold.ttf', 30)
    while running:
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                running = False
            elif evnt.type == pygame.KEYDOWN:
                if evnt.key == 13:
                    return archers, walls
                elif evnt.key in directions.keys() and img_drawing:
                    s_btn.update(directions[evnt.key](s_btn))
            elif evnt.type == pygame.MOUSEBUTTONDOWN:
                cursor.change_pos(*evnt.pos)
                if game.menu.rect.collidepoint(*evnt.pos) and not img_drawing:
                    clicked_btn = pygame.sprite.spritecollideany(cursor.change_offset(game.menu), game.menu.buttons)
                    try:
                        if clicked_btn.name[:-1] == ARCHER:
                            s_btn = Archer(*evnt.pos, int(clicked_btn.name[-1]))
                            img_drawing = True
                            pygame.mouse.set_visible(False)
                        elif clicked_btn.name[:-1] == WALL:
                            s_btn = Wall(*evnt.pos, int(clicked_btn.name[-1]))
                            img_drawing = True
                            pygame.mouse.set_visible(False)
                    except Exception:
                        pass
                elif img_drawing:
                    if game.menu.rect.collidepoint(*evnt.pos):
                        img_drawing = False
                        pygame.mouse.set_visible(True)
                    if game.money - s_btn.price > 0 \
                            and not s_btn.rect.colliderect(game.castle.rect) and not game.menu.rect.collidepoint(
                        *evnt.pos):
                        fill_board(s_btn, game.board)
                        if s_btn.name == ARCHER:
                            archers.append(s_btn)
                            s_btn = Archer(*evnt.pos, s_btn.lvl)
                        else:
                            walls.append(s_btn)
                            s_btn = Wall(*evnt.pos, s_btn.lvl)
                        game.money -= s_btn.price
                    else:
                        img_drawing = False
                        pygame.mouse.set_visible(True)
            elif evnt.type == pygame.MOUSEMOTION:
                if img_drawing:
                    s_btn.change_pos(*evnt.pos)
        game.parent.blit(game.bg, (0, 0))
        game.menu.draw(game.parent)
        game.castle.draw(game.parent)
        if img_drawing:
            if s_btn.rect.colliderect(game.castle.rect):
                game.parent.blit(font.render('NO', True, (255, 0, 0)), (s_btn.rect.x, s_btn.rect.y))
            else:
                pygame.draw.rect(game.parent, (255, 0, 0), s_btn.rect, 2)
                s_btn.draw(game.parent)
        for archer in archers:
            archer.draw(game.parent)
        for wall in walls:
            wall.draw(game.parent)
        text_m = font.render('$' + str(game.money), True, (255, 255, 255))
        text_a = font.render('Archers :' + str(len(archers)), True, (255, 255, 255))
        text_w = font.render('Walls :' + str(len(walls)), True, (255, 255, 255))
        game.parent.blit(text_m, (1280 - text_m.get_size()[0], 0))
        game.parent.blit(text_a, (1280 - text_a.get_size()[0], 50))
        game.parent.blit(text_w, (1280 - text_w.get_size()[0], 100))
        pygame.display.flip()


def fill_board(btn, board, val=True):
    w, h = btn.get_rect().w, btn.get_rect().h
    for i in range(btn.rect.w // CELL_SIZE):
        for j in range(btn.rect.h // CELL_SIZE):
            x = btn.x // CELL_SIZE + i
            y = btn.y // CELL_SIZE + j
            board[y][x] = val


def moving_srfc(text, surf):
    surface = surf.copy()
    clock = pygame.time.Clock()
    srfc = pygame.Surface((1280, 720))
    srfc.fill((0, 0, 0))
    font = pygame.font.Font('freesansbold.ttf', 100)
    txt = font.render(text, True, (255, 255, 255))
    srfc.blit(txt, ((1280 - len(text)) // 2, 310))
    rect = pygame.Rect((-1280, 0), (1280, 720))
    v = 900
    running = True
    while running:
        if rect.x > 1280:
            running = False
        rect.x += v * clock.tick(60) / 1000
        surf.blit(surface, (0, 0))
        surf.blit(srfc, (rect.x, rect.y))
        pygame.display.flip()


def start_placing(game, lvl):
    castle_placing(game)
    return archer_and_wall_placing(game, lvl)
