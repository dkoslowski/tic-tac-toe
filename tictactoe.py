#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from board import *
from player import *

# testing data
data = [
    [Tile((0,0),  0), Tile((0,1), -1), Tile((0,2), -1)],
    [Tile((1,0), -1), Tile((1,1),  1), Tile((1,2),  1)],
    [Tile((2,0),  1), Tile((2,1),  1), Tile((2,2), -1)],
]

# Game control
class Game():

    # init
    def __init__(self) -> None:
        self.board = Board()
        self.player = {
            1: HumanPlayer(self.board),
            -1: AIPlayer(self.board)
        }

    # main game loop        
    def run(self):
        while True:
            print('Starting new game')
            winner = None
            while winner == None:
                self.player[self.board.turn].move()
                winner = self.board.winner()
            self.board.print()
            if winner == 0:
                print('Draw')
            else:
                print(f'{winner} wins')
            self.board.reset()
    
    # a test...
    def test(self):
        self.board.test()

if __name__ == '__main__':
    game = Game()
    game.run()
#    game.test()
