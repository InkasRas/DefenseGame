class Archer(pygame.sprite.Sprite):
    def __init__(self, x, y, lvl):
        super().__init__()
        self.stand_imgs = []
        for i in range(5):
            self.stand_imgs.append(pygame.transform.scale(load_image(f'archer/1_IDLE_00{i}.png', -1), (40, 40)))
        self.img_id = 0
        self.image = self.stand_imgs[0]
        self.lvl = lvl
        self.price = archer_lvls[self.lvl][0]
        self.health = archer_lvls[self.lvl][1]
        self.max_health = archer_lvls[self.lvl][1]
        self.force = archer_lvls[self.lvl][2]
        self.x = x
        self.y = y
        self.board_x = x // CELL_SIZE
        self.board_y = y // CELL_SIZE
        self.parent_cell_size = CELL_SIZE
        self.rect = pygame.Rect((x, y), self.image.get_size())
        self.name = ARCHER
        self.radius = 80

    def insert_enemies(self, enems):
        self.enms = enems

    def get_clicked(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
        return False

    def attack_enemies(self):
        for enm in self.enms:
            if pygame.sprite.collide_circle(self, enm) and enm.active:
                enm.hurt(self.force)

    def get_board_pos(self):
        return self.board_x, self.board_y

    def update(self, img):
        self.image = img
        self.rect = pygame.Rect((self.x, self.y), self.image.get_size())

    def img_update(self):
        self.img_id = self.img_id + 1 if self.img_id <= len(self.stand_imgs) - 2 else 0
        self.image = self.stand_imgs[self.img_id]

    def get_rect(self):
        return self.rect

    def get_pos(self):
        return self.rect.x, self.rect.y

    def hurt(self, k):
        self.health -= k

    def change_pos(self, x, y):
        prom_x, prom_y = self.parent_cell_size * (x // 20), self.parent_cell_size * (y // 20)
        x = prom_x if x - prom_x < prom_x + self.parent_cell_size - x else prom_x + self.parent_cell_size
        y = prom_y if y - prom_y < prom_y + self.parent_cell_size - y else prom_y + self.parent_cell_size
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.board_x = self.x // CELL_SIZE
        self.board_y = self.y // CELL_SIZE

    def draw(self, srfc):
        srfc.blit(self.image, (self.x, self.y))
        rx = round(40 * (self.max_health - self.health) // self.max_health)
        pygame.draw.line(srfc, (255, 0, 0), (self.x, self.y - 2), (self.x + rx, self.y - 2), 2)
        pygame.draw.line(srfc, (0, 255, 0), (self.x + rx, self.y - 2), (self.x + 40, self.y - 2), 2)
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(str(self.lvl + 1), True, (255, 255, 255))
        srfc.blit(text, (self.x, self.y))
