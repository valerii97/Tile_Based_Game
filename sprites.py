import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites  # adding all objects of this class to all_sprites group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0  # this vars will be used to control player's speed
        self.x = x * TILESIZE  # cause changed in update, need to make initial position of player
        self.y = y * TILESIZE  # cause changed in update, need to make initial position of player

    def get_keys(self):  # creating this method for more convenient change of controls in future
        self.vx, self.vy = 0, 0  # for initial settings
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:  # to make diagonal movement at the same speed as in other dirs
            self.vx *= 0.7071
            self.vy *= 0.7071

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.get_keys()  # to check it at each frame
        self.x += self.vx * self.game.dt  # frame independent movement
        self.y += self.vy * self.game.dt
        self.rect.topleft = (self.x, self.y)
        if pg.sprite.spritecollideany(self, self.game.walls):  # faster than spritecollide
            self.x -= self.vx * self.game.dt
            self.y -= self.vy * self.game.dt
            self.rect.topleft = (self.x, self.y)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
