#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A tile for the game screen. Contents a single game field.
"""

import pygame

class Tile(pygame.sprite.Sprite):

    # Tile colors
    color = {
        'std': (128, 128, 128), # standard tile
        'sel': (200, 200, 200), # selected tile
        'won': (  0, 255,   0), # winner tile
        'los': (255,   0,   0), # loser tile
        'fnt': (  0,   0,   0), # font
    }

    # Class variables:
    #
    # self.mode        <- tile mode          'std', 'sel', 'won', 'los'
    # self.label       <- tile label         'X', 'O' or None
    # self.label_surf  <- tile label surface None or pygame.Surface
    # self.font        <- font for rendering of lables
    # self.dirty       <- needs update?      True/False

    def __init__(self, size, topleft, *groups) -> None:

        super().__init__(*groups)

        # self.image & self.rect
        self.image        = pygame.Surface((size,size))
        self.rect         = self.image.get_rect()
        self.rect.topleft = topleft

        # font
        self.font        = pygame.font.Font(None, int(size))

        # reset
        self.reset()

    # reset the tile
    def reset(self):
        self.mode       = 'std'
        self.label      = None
        self.label_surf = None
        self.dirty      = True

    # make the tile selected
    def select(self):
        if self.mode == 'std':
            self.mode = 'sel'
            self.dirty  = True

    # make the tile unselected
    def unselect(self):
        if self.mode == 'sel':
            self.mode = 'std'
            self.dirty  = True

    # Mark the tile
    def mark(self, label):
        if not self.label:
            self.label = label
            self.dirty = True

    # Update
    def update(self, *args):
        if self.dirty:
            self.image.fill(Tile.color[self.mode])
            if self.label:
                #print(self.rect)
                surf = self.font.render(self.label, True, Tile.color['fnt'])
                #rect = self.image.get_rect(size=surf.get_size())
                #print(rect)
                self_w, self_h = self.image.get_size()
                surf_w, surf_h = surf.get_size()
                x = int((self_w - surf_w)/2)
                y = int((self_h - surf_h)/2)
                self.image.blit(surf, (x, y))
            self.dirty = False
