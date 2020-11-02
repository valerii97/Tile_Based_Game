import pygame as pg
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites  # adding all objects of this class to all_sprites group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        # self.radius = self.rect.height // 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.width = 0.5 * self.rect.width
        self.acc = vec(0, 0)  # to make gravity
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.position_bottom = False
        self.hits_y = False
        self.hits_x = False
        self.attack = False

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
                    self.pos.x = self.hits_x[0].rect.left - self.rect.width  # this will stop us, while we moving to
                    # the right
                    self.position_bottom = False
                if self.vel.x < 0:
                    self.pos.x = self.hits_x[0].rect.right
                    self.position_bottom = False
                self.vel.x = 0  # if hits in x dir, than we must stop in this ax
                self.rect.x = self.pos.x
        if dir == 'y':
            self.rect.bottom += 1
            self.hits_y = pg.sprite.spritecollide(self, self.game.walls, False)
            self.rect.bottom -= 1
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
            # pg.mixer.music.load('snd1.wav')
            # pg.mixer.music.play()

    def attack1(self):
        self.attack = True

    def load_images(self):
        self.idle = [pg.image.load('Idle/HeroKnight_Idle_0.png'),
                     pg.image.load('Idle/HeroKnight_Idle_1.png'),
                     pg.image.load('Idle/HeroKnight_Idle_2.png'),
                     pg.image.load('Idle/HeroKnight_Idle_3.png'),
                     pg.image.load('Idle/HeroKnight_Idle_4.png'),
                     pg.image.load('Idle/HeroKnight_Idle_5.png'),
                     pg.image.load('Idle/HeroKnight_Idle_6.png'),
                     pg.image.load('Idle/HeroKnight_Idle_7.png')]
        for frame in self.idle:
            frame.set_colorkey(BLACK)

        self.walking_frames_r = [pg.image.load('Run/HeroKnight_Run_0.png'),
                                 pg.image.load('Run/HeroKnight_Run_1.png'),
                                 pg.image.load('Run/HeroKnight_Run_2.png'),
                                 pg.image.load('Run/HeroKnight_Run_3.png'),
                                 pg.image.load('Run/HeroKnight_Run_4.png'),
                                 pg.image.load('Run/HeroKnight_Run_5.png'),
                                 pg.image.load('Run/HeroKnight_Run_6.png'),
                                 pg.image.load('Run/HeroKnight_Run_7.png'),
                                 pg.image.load('Run/HeroKnight_Run_8.png'),
                                 pg.image.load('Run/HeroKnight_Run_9.png')]
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)

        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))

        self.jumping_frame_r = [pg.image.load('Jump/HeroKnight_Jump_0.png'),
                              pg.image.load('Jump/HeroKnight_Jump_1.png'),
                              pg.image.load('Jump/HeroKnight_Jump_2.png')]
        for frame in self.jumping_frame_r:
            frame.set_colorkey(BLACK)

        self.jumping_frame_l = []
        for frame in self.jumping_frame_r:
            self.jumping_frame_l.append(pg.transform.flip(frame, True, False))

        self.attack_frame_r = [pg.image.load('Attack1/HeroKnight_Attack1_0.png'),
                               pg.image.load('Attack1/HeroKnight_Attack1_1.png'),
                               pg.image.load('Attack1/HeroKnight_Attack1_2.png'),
                               pg.image.load('Attack1/HeroKnight_Attack1_3.png'),
                               pg.image.load('Attack1/HeroKnight_Attack1_4.png'),
                               pg.image.load('Attack1/HeroKnight_Attack1_5.png')]
        for frame in self.attack_frame_r:
            frame.set_colorkey(BLACK)

        self.attack_frame_l = []
        for frame in self.attack_frame_r:
            self.attack_frame_l.append(pg.transform.flip(frame, True, False))

    def animation(self):
        now = pg.time.get_ticks()
        if self.vel.x > 5:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[self.current_frame]
                self.rect = self.image.get_rect()

        if self.vel.x < -5:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()

        if self.vel.y < -3 and (self.vel.x > 5 or abs(self.vel.x) <= 5):
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frame_r)
                self.image = self.jumping_frame_r[self.current_frame]
                self.rect = self.image.get_rect()

        if self.vel.y < -3 and self.vel.x < 5:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frame_l)
                self.image = self.jumping_frame_l[self.current_frame]
                self.rect = self.image.get_rect()

        if abs(self.vel.x) <= 5:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle)  # WAT?
                self.image = self.idle[self.current_frame]
                self.rect = self.image.get_rect()

        if self.attack and (self.vel.x > 5 or abs(self.vel.x) <= 5):
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frame_r)  # WAT?
                self.image = self.attack_frame_r[self.current_frame]
                self.rect = self.image.get_rect()

        if self.attack and self.vel.x < 5:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frame_l)  # WAT?
                self.image = self.attack_frame_l[self.current_frame]
                self.rect = self.image.get_rect()

    def update(self):

        self.get_keys()  # to check it at each frame
        self.animation()

        self.acc += self.vel * PLAYER_FRICTION

        self.vel += self.acc

        self.pos += self.vel * self.game.dt + 2 * self.acc * self.game.dt ** 2

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


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width, height))
        return image


class Props(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Ladders(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
