import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)  # makes easier to move, if 500ms pressed, repeat action after 100ms pause
        self.load_data()
        self.save_dt = 0

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map4.txt'))
        self.spritesheet = Spritesheet('Medieval_props_free.png')

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # Making a level and spawning a Player in particular place
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, 'dirt.png')
                if tile == '2':
                    Wall(self, col, row, 'grass.png')
                if tile == 'd':
                    Props(self, col, row, self.spritesheet.get_image(67, 29, 51, 58))
                if tile =='l':
                    Ladders(self, col, row, self.spritesheet.get_image(195, 95, 22, 75))
                if tile == 'P':
                    self.player = Player(self, col, row)  # to spawn player in particular place

        self.camera = Camera(self.map.width, self.map.height)  # creating camera obj

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # for making further moving at consistent speed
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_f:
                    self.player.attack1()
            if event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.player.attack = False
            #         self.player.jumping = True
            # if event.type == pg.KEYUP:
            #     if event.key == pg.K_SPACE:
            #         self.player.jumping = False

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)  # updating camera every loop
        print(self.player.rect.width)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:  # drawing objects in camera
            self.screen.blit(sprite.image, self.camera.apply(sprite))  # adding entity to follow for
        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()

g.show_go_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
