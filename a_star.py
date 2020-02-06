import numpy
import pygame
import math
from all_variables import draw_cells, CASTLE, OBSTACLE, PATH_GREEN, WINDOW_W, WINDOW_H, CELL_SIZE, PATH_VIOL, PATH_FOUND
import random
import numpy
import pygame
import random


class Node:
    def __init__(self, pos, target=None, parent=None):
        self.parent = parent
        self.pos = pos
        self.target = target
        self.is_wall = False
        if parent is not None:
            self.g = abs(self.pos[0] - self.parent.pos[0]) + abs(self.pos[1] - self.parent.pos[1])
            self.h = abs(self.pos[0] - self.target[0]) + abs(self.pos[1] - self.target[1])
            self.f = self.h + self.g
        else:
            self.f = 0

    def __eq__(self, other):
        return True if self.pos == other.pos else False

    def __repr__(self):
        return f'Node object {self.pos} {self.target}'

    def get_pos(self, x, y):
        pr_x = self.pos[0] + x
        pt_y = self.pos[1] + y
        if pr_x < 0 or pt_y < 0 or pr_x >= WINDOW_H // CELL_SIZE or pt_y >= WINDOW_W // CELL_SIZE:
            return None
        return self.pos[0] + x, self.pos[1] + y


def find_path(game, start, target_p, with_draw=False):
    screen = game.parent
    board = game.board.copy()
    start = Node(start, target_p)
    open_set = [start]
    closed_set = []
    can_find = False
    found = False
    target = Node(target_p)
    cur_n = start
    while True:

        if len(open_set) > 0 and not found and can_find:
            if cur_n != target:
                cur_n = min(open_set, key=lambda x: x.f)
                board[cur_n.pos[0], cur_n.pos[1]] = PATH_VIOL
                open_set.remove(cur_n)
                closed_set.append(cur_n.pos)
            if cur_n == target:
                found = True
                ans = []
                while cur_n.parent is not None:
                    board[cur_n.pos[0], cur_n.pos[1]] = PATH_FOUND
                    ans.insert(0, cur_n.pos)
                    cur_n = cur_n.parent
                # game.board = numpy.where(numpy.logical_or(board == PATH_VIOL, board == PATH_GREEN), 0, board)
                if with_draw:
                    game.parent.blit(game.bg, (0, 0))
                    draw_cells(board, game.parent, True)
                    pygame.display.flip()
                    pygame.time.wait(1200)
                return ans
            else:
                for po in filter(lambda x: x != None,
                                 [cur_n.get_pos(1, 0), cur_n.get_pos(0, 1), cur_n.get_pos(-1, 0),
                                  cur_n.get_pos(0, -1)]):
                    if board[po[0], po[1]] == CASTLE:
                        target_p = po
                        cur_n = Node(po, target=target_p, parent=cur_n)
                        target.pos = po
                        break
                    if po in closed_set or board[po[0], po[1]] == OBSTACLE:
                        continue
                    nod = Node(po, target_p, cur_n)
                    board[nod.pos[0], nod.pos[1]] = PATH_GREEN
                    if nod in open_set:
                        no = open_set[open_set.index(nod)]
                        if nod.g < no.g:
                            no.parent = cur_n
                    else:
                        open_set.append(nod)
        for evnt in pygame.event.get():
            if evnt.type == pygame.KEYDOWN and evnt.key == pygame.K_SPACE:
                can_find = True
        if with_draw:
            game.parent.blit(game.bg, (0, 0))
            draw_cells(board, game.parent, True)
            pygame.display.flip()
        if len(open_set) == 0:
            return None
