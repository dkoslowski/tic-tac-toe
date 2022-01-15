#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A simple tic-tac-toe game
"""
import pygame
import sys

from pygame import event
from game   import Game

# exit
def bye():
    pygame.quit()
    sys.exit()

pygame.init()
clock = pygame.time.Clock()

# create a game instance
game = Game()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bye()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                bye()
            if event.key == pygame.K_ESCAPE:
                game.reset()
            if event.key == pygame.K_UP:
                game.sel_up()
            if event.key == pygame.K_DOWN:
                game.sel_down()
            if event.key == pygame.K_LEFT:
                game.sel_left()
            if event.key == pygame.K_RIGHT:
                game.sel_right()
            if event.key == pygame.K_SPACE:
                game.mark()

    game.update()
    clock.tick(60)
