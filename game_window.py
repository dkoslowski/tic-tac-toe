#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame

from game_data   import *

#
# Single tile
#
class Tile(pygame.sprite.Sprite):

    # Tile colors
    color = {
        DataState.EMPTY:    (128, 128, 128), # standard tile
        DataState.SELECTED: (200, 200, 200), # selected tile
        DataState.WINNER_X: (  0, 255,   0), # X wins
        DataState.WINNER_0: (255,   0,   0), # 0 wins
        DataState.ERROR:    (  0,   0, 255), # error
        'fnt':          (  0,   0,   0), # font
    }

    def __init__(self, size, topleft, data_el, *groups) -> None:

        super().__init__(*groups)

        # self.image & self.rect
        self.image        = pygame.Surface((size,size))
        self.rect         = self.image.get_rect()
        self.rect.topleft = topleft

        # font
        self.font        = pygame.font.Font(None, int(size))

        # Corresponding internal data element
        self.data_el      = data_el

    # Update
    def update(self, *args, **kwargs):
        if self.data_el.dirty:
            c = Tile.color[self.data_el.state]
            self.image.fill(c)
            label = self.data_el.get_label()
            if label:
                surf = self.font.render(label, True, Tile.color['fnt'])
                self_w, self_h = self.image.get_size()
                surf_w, surf_h = surf.get_size()
                x = int((self_w - surf_w)/2)
                y = int((self_h - surf_h)/2)
                self.image.blit(surf, (x, y))

            self.data_el.dirty = False            

#
# Game window
#
class GameWindow:

    def __init__(self, data) -> None:

        self.data  = data
        self.tiles = pygame.sprite.RenderUpdates()

        # Calculate sizes
        current_h   = pygame.display.Info().current_h
        tile_size   = int(current_h/8)
        tile_margin = int(tile_size/8)
        screen_size = tile_size * 3 + tile_margin * 2

        # Game screen
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption('Tic-tac-toe')

        # Create tiles
        for i in range(3):
            for j in range(3):
                y = (tile_size + tile_margin) * i
                x = (tile_size + tile_margin) * j
                el = self.data.element_at((i,j))
                t = Tile(
                    tile_size,
                    (x,y),
                    el,
                    self.tiles,
                )

    # Update window content
    def update(self):
        if self.data.dirty:
            self.tiles.update()
            self.data.dirty = False

    # Draw window
    def draw(self):
        self.tiles.draw(self.screen)
        pygame.display.update()
