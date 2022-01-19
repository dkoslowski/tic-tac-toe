#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys

from game_window import *
from game_logic  import *
from game_data   import *

pygame.init()
clock = pygame.time.Clock()

# Create data container
data = GameData()
# create main window
window = GameWindow(data)
# create a game instance
game = GameLogic(data)

# Main loop
main_loop = True
while main_loop:

    # new game
    data.reset()
    game.reset()
    game_loop = True
    print('Starting new game')

    while game.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.finish()
                main_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game.finish()
                    main_loop = False
                elif event.key == pygame.K_ESCAPE:
                    game.finish()
                else:
                    game.user_input_key(event.key)

        game.update()
        window.update()
        window.draw()

# exit
pygame.quit()
sys.exit()



