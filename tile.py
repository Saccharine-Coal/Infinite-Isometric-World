import pygame as pg

class Tile:
    """This will have more functionality in the future."""
    def __init__(self, value):
        if value == 1:
            self.image = pg.image.load('images/grass_tile.png').convert_alpha()
            self.rect = self.image.get_rect()
        if value == 2:
            self.image = pg.image.load('images/dirt_tile.png').convert_alpha()
            self.rect = self.image.get_rect()
        if value == 3:
            self.image = pg.image.load('images/soil_tile.png').convert_alpha()
            self.rect = self.image.get_rect()
        if value == 4:
            self.image = pg.image.load('images/plowed_field_tile.png').convert_alpha()
            self.rect = self.image.get_rect()
