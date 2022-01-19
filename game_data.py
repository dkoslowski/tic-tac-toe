#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import enum

#
# Possible data element states
#
class DataState(enum.Enum):
    EMPTY    = enum.auto()
    SELECTED = enum.auto()
    WINNER_X = enum.auto()
    WINNER_0 = enum.auto()
    ERROR    = enum.auto()

#
# Data element
#
class DataElement():

    def __init__(self, pos) -> None:
        self.pos = pos
        self.reset()

    # Reset
    def reset(self):
        self.label = None
        self.state = DataState.EMPTY
        self.dirty = True

    # Get tile state
    def get_state(self):
        return self.state

    # Set tile state
    def set_state(self, state):
        self.state = state
        self.dirty = True

    # Is this element marked?
    def get_label(self):
        return self.label

    # Mark this element
    def set_label(self, label):
        self.label = label
        self.dirty = True

#
# Internal game data
#
class GameData():

    def __init__(self) -> None:

        # Init internal data
        self.data  = []
        for i in range(3):
            for j in range(3):
                d = DataElement((i,j))
                self.data.append(d)

        self.selected_pos = None
        self.reset()

    # Reset
    def reset(self):
        for d in self.data:
            d.reset()
        self.select((1,1))
        self.dirty = True

    # Get the element at position (i,j)
    def element_at(self, pos):
        return self.data[pos[0]*3 + pos[1]]

    # Unselect 
    def unselect(self):
        if self.selected_pos:
            el = self.element_at(self.selected_pos)
            if el.get_state() == DataState.SELECTED:
                el.set_state(DataState.EMPTY)
                self.dirty = True

    # Select an element
    def select(self, pos):
        self.unselect()
        self.selected_pos = pos
        self.element_at(self.selected_pos).set_state(DataState.SELECTED)
        self.dirty = True
    
    # Get selected position
    def get_selected_pos(self):
        return self.selected_pos

    # Get selected element
    def get_selected_el(self):
        return self.element_at(self.selected_pos)

    # Get label of selected element
    def get_label(self, pos):
        return self.element_at(pos).get_label()

    # Set label of selected element
    def set_label(self, pos, label):
        self.element_at(pos).set_label(label)
        self.dirty = True
    
    # Set tile state
    def set_state(self, pos, state):
        self.element_at(pos).set_state(state)