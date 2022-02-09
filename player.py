#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# An abstract player
class Player():

    # init
    def __init__(self, board) -> None:
        self.board = board
        self.id = None

    # do your move
    def move(self):
        pass
    
# An AI player    
class AIPlayer(Player):

    # init
    def __init__(self, board) -> None:
        super().__init__(board)
        self.id = 'AI'

    # do your move
    def move(self):
        # self.board.print()
        move = self.board.best_move()
        print(f'AI move: {move}')
        self.board.mark(move)

# A human player
class HumanPlayer(Player):

    # init
    def __init__(self, board) -> None:
        super().__init__(board)
        self.id = 'Human player'

    # do your move
    def move(self):
        while True:
            try:
                self.board.print()
                move = eval(input('Your move: '))
                self.board.mark(move)
            except (KeyboardInterrupt):
                print('\nGoodbye!\n')
                quit()
            except (NameError, IndexError, TypeError, SyntaxError, Exception):
                print('Invalid input')
            else:
                break
