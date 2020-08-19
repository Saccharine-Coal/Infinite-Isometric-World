import pygame as pg

from os import sys

from grid import Grid
from camera import Camera
from tile import Tile
from sprites import *
from settings import *

class Game:
    def __init__(self):
        """Initialize everything needed to run the game."""
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

    def new(self):
        """ Initialize everything needed for a new game."""
        self.background = self.create_layer(Tile)
        # Holds all layers.
        self.layers = [self.background]
        self.player_sprite = pg.sprite.Group()
        self.player = Player(self, 0, 0)
        self.camera = Camera(self.background.width, self.background.height)

    def create_layer(self, object_type):
        """Create a layer and populate it with the appropriate object."""
        layer = Grid(object_type)
        layer.init_chunks()
        layer.init_objects()
        return layer

    def run(self):
        """Runs pygame."""
        while True:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Catch all events here."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                # Moves the player and camera.
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

    def update(self):
        """Everything that needs to be updated is done here."""
        # Update player sprite.
        self.player_sprite.update()
        self.camera.update(self.player)
        # Uses player position to know which chunks to render around it.
        for layer in self.layers:
            layer.render = layer.render_chunks(*self.player.get())
        # Set new limits for the camera.
        self.camera._update_max_size(self.background)

    def draw(self):
        """Draws images and displays it on the screen."""
        # Covers previous screen. Essentially wipes it.
        self.screen.fill(BGCOLOR)
        # Get fps of the game.
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        for layer in self.layers:
            for chunk in layer.render:
                for tile in chunk:
                    self.screen.blit(tile[0], self.camera.apply_rect(tile[1]))
        for sprite in self.player_sprite:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

# Create game object.
g = Game()
g.new()
g.run()
