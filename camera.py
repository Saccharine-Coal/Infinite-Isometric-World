import pygame as pg

from settings import *


class Camera:
    """Offsets the position of the grid to create a 'camera' oriented on the player."""

    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.max_x = self.max_y = CHUNKS*CHUNKSIZE
        self.min_x = self.min_y  = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.x
        y = -target.y
        x = min(abs(self.min_x), x)  # left
        y = min(abs(self.min_y), y)  # top
        x = max(-(self.max_x)+1, x)  # right
        y = max(-(self.max_y)+1, y)  # bottom
        x, y = self.convert_cart(x, y)
        self.camera = pg.Rect(
            x + int(WIDTH / 2), y + int(HEIGHT / 2), self.width, self.height
        )

    def _update_max_size(self, obj):
        self.max_x, self.max_y = obj.max_x, obj.max_y
        self.min_x, self.min_y = obj.min_x, obj.min_y

    def convert_cart(self, x, y):
        cart_x = x * TILEHEIGHT_HALF
        cart_y = y * TILEWIDTH_HALF
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        return iso_x, iso_y
