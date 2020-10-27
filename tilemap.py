import pygame as pg
from settings import *


class Map:  # creating this class to simplify procedure of loading maps
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:  # to open and close after loading
            for line in f:
                self.data.append(line.strip())  # deleting \n after each line in txt file

        self.tilewidth = len(self.data[0])  # width in tiles
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE  # width in pixels
        self.height = self.tileheight * TILESIZE


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):  # drawing new rect at each loop
        return entity.rect.move(self.camera.topleft)  # moving with entity

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)  # offsetting the camera coords and making target centered
        y = -target.rect.y + int(HEIGHT / 2)
        # limit scrolling to map size
        x = min(0, x)  # offset by x may be only negative, which means that camera cannot move to the left of screen
        y = min(0, y)  # the same as for x
        y = max(-(self.height - HEIGHT), y)  # not less than difference btwn map height and camera height
        x = max(-(self.width - WIDTH), x)
        self.camera = pg.Rect(x, y, self.width, self.height)
