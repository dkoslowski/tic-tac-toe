#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from turtle import position
import pygame
import enum
import queue
import random

from game_data import *

#
# Game state
#
class GameState(enum.Enum):
    TURN_X   = enum.auto()
    TURN_0   = enum.auto()
    WINNER_X = enum.auto()
    WINNER_0 = enum.auto()
    DRAW     = enum.auto()
    FINISHED = enum.auto()

#
# Game logic
#
class GameLogic():

    def __init__(self, data) -> None:
        self.data       = data
        self.prev_state = None
    
    # reset
    def reset(self):
        if self.prev_state and self.prev_state == GameState.TURN_X:
            self.state    = GameState.TURN_0
        else:
            self.state    = GameState.TURN_X
        self.prev_state = self.state
        self.input_q  = queue.SimpleQueue()

    # update game status
    def update(self):
        if self.state == GameState.TURN_X:
            self.turn_X()
        elif self.state == GameState.TURN_0:
            self.turn_0()

    # user input handler
    def user_input_key(self, key):
        self.input_q.put(key)

    # Players's turn
    def turn_X(self):
        while not self.input_q.empty():
            key = self.input_q.get_nowait()
            i, j = self.data.get_selected_pos()
            if key == pygame.K_UP:
                if i > 0:
                    self.data.select((i - 1, j))
            elif key == pygame.K_DOWN:
                if i < 2:
                    self.data.select((i + 1, j))
            elif key == pygame.K_LEFT:
                if j > 0:
                    self.data.select((i, j - 1))
            elif key == pygame.K_RIGHT:
                if j < 2:
                    self.data.select((i, j + 1))
            elif key == pygame.K_SPACE:
                if self.data.get_label((i,j)) == None:
                    self.data.set_label((i,j), 'X')
                    self.next_turn()

    # AI turn
    def turn_0(self):
        while True:
            i = random.randrange(3)
            j = random.randrange(3)
            if self.data.get_label((i,j)) == None:
                self.data.set_label((i,j), '0')
                break
        self.next_turn()

    # Game running?
    def is_running(self):
        return self.state != GameState.FINISHED
    
    # Finish running game
    def finish(self):
        self.state = GameState.FINISHED
    
    # Get the common lable for a line, column or diagonal
    def check_full_line(self, positions):

        label = None
        state = DataState.ERROR
        cnt_X = 0
        cnt_0 = 0

        for pos in positions:
            l = self.data.get_label(pos)
            if l == 'X':
                cnt_X += 1
            elif l == '0':
                cnt_0 += 1
            else:
                break

        if cnt_X == 3:
            print('WINNER X')
            label = 'X'
            self.state = GameState.WINNER_X
            state = DataState.WINNER_X
        elif cnt_0 == 3:
            print('WINNER 0')
            label = '0'
            self.state = GameState.WINNER_0
            state = DataState.WINNER_0

        if label:
            self.data.unselect()
            for pos in positions:
                self.data.set_state(pos, state)
        return label

    # Toggle the next turn
    def next_turn(self):

        # Do we have a winner?
        # Lines
        self.check_full_line([(0,0),(0,1),(0,2)])
        self.check_full_line([(1,0),(1,1),(1,2)])
        self.check_full_line([(2,0),(2,1),(2,2)])

        # Columns
        self.check_full_line([(0,0),(1,0),(2,0)])
        self.check_full_line([(0,1),(1,1),(2,1)])
        self.check_full_line([(0,2),(1,2),(2,2)])

        # Diagonals
        self.check_full_line([(0,0),(1,1),(2,2)])
        self.check_full_line([(0,2),(1,1),(2,0)])

        # No winner, is it a draw?
        if self.state == GameState.TURN_X or self.state == GameState.TURN_0:
            empty_elements = 0
            for i in range(3):
                for j in range(3):
                    if self.data.get_label((i,j)) == None:
                        empty_elements += 1
            if empty_elements == 0:
                self.data.unselect()
                self.state = GameState.DRAW
                print('DRAW')

        # No winner, no draw, continue with the game
        if self.state == GameState.TURN_X:
            self.state = GameState.TURN_0
        elif self.state == GameState.TURN_0:
            self.state = GameState.TURN_X
