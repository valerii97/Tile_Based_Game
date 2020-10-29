import pygame as pg
from settings import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites  # adding all objects of this class to all_sprites group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('alex22.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.acc = vec(0, 0)  # to make gravity
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.position_bottom = False
        self.hits_y = False
        self.hits_x = False

    def get_keys(self):  # creating this method for more convenient change of controls in future
        self.acc = vec(0, GRAVITY)  # for initial settings
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_SPEED

    def collide_with_walls(self, dir):
        if dir == 'x':
            self.hits_x = pg.sprite.spritecollide(self, self.game.walls, False)
            if self.hits_x:
                if self.vel.x > 0:  # sprite moving to right
                    self.pos.x = self.hits_x[0].rect.left - self.rect.width  # this will stop us, while we moving to the right
                    self.position_bottom = False
                if self.vel.x < 0:
                    self.pos.x = self.hits_x[0].rect.right
                    self.position_bottom = False
                self.vel.x = 0  # if hits in x dir, than we must stop in this ax
                self.rect.x = self.pos.x
        if dir == 'y':
            self.rect.bottom += 2
            self.hits_y = pg.sprite.spritecollide(self, self.game.walls, False)
            self.rect.bottom -= 2
            if self.hits_y:
                if self.vel.y > 0:
                    self.pos.y = self.hits_y[0].rect.top - self.rect.height
                    self.position_bottom = True
                if self.vel.y < 0:
                    self.pos.y = self.hits_y[0].rect.bottom
                    self.position_bottom = False
                self.vel.y = 0
                self.rect.y = self.pos.y
            elif not self.hits_y:
                self.position_bottom = False

    def jump(self):
        if self.position_bottom:
            self.vel.y = -PLAYER_JUMP
            self.position_bottom = False
            pg.mixer.music.load('snd1.wav')
            pg.mixer.music.play()

    def update(self):
        self.get_keys()  # to check it at each frame

        self.acc += self.vel * PLAYER_FRICTION

        self.vel += self.acc

        self.pos += self.vel * self.game.dt + 2 * self.acc * self.game.dt**2

        # Making 2 collision checks: one for each axes, to make possible sliding movement via walls' edges
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(image)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
