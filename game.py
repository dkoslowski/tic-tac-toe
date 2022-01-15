#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
#  Game logic and representation
#

import pygame

from tile   import *
from matrix import *

class Game():

    def __init__(self) -> None:

        # Calculate sizes
        current_h        = pygame.display.Info().current_h
        self.tile_size   = int(current_h/8)
        self.tile_margin = int(self.tile_size/8)
        self.screen_size = self.tile_size * 3 + self.tile_margin * 2

        # Game screen
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption('Tic-tac-toe')

        # Tile group for sprite handling
        self.tiles = pygame.sprite.RenderUpdates()

        # Tile matrix for quick referencing
        self.matrix = Matrix()

        # Create tiles
        for i in range(3):
            for j in range(3):
                y = (self.tile_size + self.tile_margin) * i
                x = (self.tile_size + self.tile_margin) * j
                t = Tile(self.tile_size, (x,y), self.tiles)
                self.matrix.put((i,j), t)

        # Reset
        self.reset()

    # reset/restart the game
    def reset(self):
        self.matrix.reset()

    # update the game and screen representation, if necessary
    def update(self):
        self.tiles.update()
        self.tiles.draw(self.screen)
        pygame.display.update()

    # "Cursor" movement
    def sel_up(self):
        i, j = self.matrix.get_selected_pos()
        if i > 0:
            self.matrix.select((i - 1, j))

    def sel_down(self):
        i, j = self.matrix.get_selected_pos()
        if i < 2:
            self.matrix.select((i + 1, j))

    def sel_left(self):
        i, j = self.matrix.get_selected_pos()
        if j > 0:
            self.matrix.select((i, j - 1))

    def sel_right(self):
        i, j = self.matrix.get_selected_pos()
        if j < 2:
            self.matrix.select((i, j + 1))
    
    # Mark the tile
    def mark(self):
        self.matrix.get_selected().mark('X')
