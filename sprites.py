import pygame as pg

from settings import *


class Player(pg.sprite.Sprite):
    """Class that holds everything for the Player Character."""

    def __init__(self, game, x, y):
        self.groups = game.player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(
            "images/player_tile.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        """Moves the position of the player in cartesian coordinates."""
        self.x += dx
        self.y += dy

    def update(self):
        """Updates the isometric position of the player."""
        self.rect.x, self.rect.y = self._convert_cart(self.x, self.y)

    def get(self):
        """Current position of the player in isometric coordinates."""
        return self.x, self.y

    def _convert_cart(self, x, y):
        cart_x = x * TILEWIDTH_HALF
        cart_y = y * TILEHEIGHT_HALF
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2
        return iso_x, iso_y

    def _get_rect(self):
        return self.rect.x, self.rect.y
