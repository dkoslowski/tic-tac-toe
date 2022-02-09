#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

# min/max guarantee
MINMAX = 52000

# A single board tile
class Tile():

    # init
    def __init__(self, pos, marker = 0) -> None:
        self.pos    = pos
        self.marker = marker
    
    # reset
    def reset(self):
        self.marker = 0
    
    # string representation
    def __repr__(self) -> str:
        # return f'{self.marker:>2}'
        if self.marker == 1:
            return 'X'
        elif self.marker == -1:
            return '0'
        else:
            return '-'

# The game board
class Board():

    # init
    def __init__(self, tiles = None) -> None:
        if tiles:
            self.tiles = tiles
        else:
            self.tiles = [[Tile((i,j)) for j in range(3)] for i in range(3)]
        self.elements = [self.tiles[i][j] for i in range(3) for j in range(3)]

        # Winning full lines
        self.lines  \
            = [[self.tiles[i][j]   for j in range(3)] for i in range(3)] \
            + [[self.tiles[i][j]   for i in range(3)] for j in range(3)] \
            + [[self.tiles[i][i]   for i in range(3)]]                   \
            + [[self.tiles[i][2-i] for i in range(3)]]

        self.depth   = 0
        self.starter = 1
        self.turn    = self.starter
        for _ in self.marked():
            self.depth += 1
            self.turn *= -1

    # reset board data
    def reset(self):
        for tile in self.elements:
            tile.reset()
        self.depth   = 0
        self.starter *= -1
        self.turn    = self.starter
        
    # list of marked board elements
    def marked(self):
        return [tile for tile in self.elements if tile.marker != 0]

    # list of unmarked board elements
    def unmarked(self):
        return [tile for tile in self.elements if tile.marker == 0]

    # list of possible moves
    def moves(self):
        return [tile.pos for tile in self.unmarked()]

    # string representation
    def __repr__(self) -> str:
        s \
            = f'{self.tiles[0][0]} {self.tiles[0][1]} {self.tiles[0][2]}\n' \
            + f'{self.tiles[1][0]} {self.tiles[1][1]} {self.tiles[1][2]}\n' \
            + f'{self.tiles[2][0]} {self.tiles[2][1]} {self.tiles[2][2]}'
        return s
    
    # mark a board element
    def mark(self, pos):
        tile = self.tiles[pos[0]][pos[1]]
        if tile.marker != 0:
            raise Exception('Tile already marked')
        tile.marker = self.turn
        self.turn *= -1
        self.depth += 1

    # unmark a board element
    def unmark(self, pos):
        tile = self.tiles[pos[0]][pos[1]]
        if tile.marker == 0:
            raise Exception('Tile not marked')
        tile.marker = 0
        self.turn *= -1
        self.depth -= 1

    # board printout
    def print(self):
        for i in range(3):
            print(f'| {self.tiles[i][0]} {self.tiles[i][1]} {self.tiles[i][2]} |')

    # board lines score 
    def lines_score(self):
        other_turn = self.turn * -1
        score  = 0
        for line in self.lines:
            count_none  = 0
            count_own   = 0
            count_other = 0
            for tile in line:
                if tile.marker == 0:
                    count_none += 1
                elif tile.marker == other_turn:
                    count_own += 1
                elif tile.marker == self.turn:
                    count_other += 1
            if count_other == 0:
                score += 10**count_own
        return score

    # do we have a draw/winner?
    def winner(self):
        prev_turn = self.turn * -1
        draw = True
        winner = 0
        for line in self.lines:
            count = 0
            for tile in line:
                if tile.marker == 0:
                    draw = False
                elif tile.marker == prev_turn:
                    count += 1
            if count == 3:
                winner = prev_turn
        if not winner and not draw:
            winner = None
        return winner

    # minimax evaluation
    def negamax(self, alpha = -MINMAX, beta = MINMAX):
 
        # A leaf?
        value = None
        winner = self.winner()
        if winner != None:
            if winner == 0:
                value = 0
            else:
                value = -(10 - self.depth) # negative bc the other wins

        # Not a leaf, recursion
        if value == None:
            value = -MINMAX
            for move in self.moves():
                self.mark(move)
                child_value = -self.negamax(-beta, -value)
                self.unmark(move)
                if child_value > value:
                    value = child_value
                    if value >= beta:
                        # prune search path
                        break
        return value

    # the best possible move
    def best_move(self):
        best_value = -MINMAX
        best_moves = []
        for move in self.moves():
            self.mark(move)
            value = -self.negamax()
            self.unmark(move)
            if value > best_value:
                best_value = value
                best_moves.clear()
            if best_value == value:
                best_moves.append(move)
        best_score = -MINMAX
        scored_moves = []
        for move in best_moves:
            self.mark(move)
            score = self.lines_score()
            self.unmark(move)
            if score > best_score:
                best_score = score
                scored_moves.clear()
            if score == best_score:
                scored_moves.append(move)
        best_move = random.choice(scored_moves)
        return best_move
    
    # a test...
    def test(self):
        for move in self.moves():
            self.mark(move)
            print(f'{move}: {-self.negamax():>3}')
            self.unmark(move)
