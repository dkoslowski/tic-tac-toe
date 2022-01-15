#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Tile references as matrix
#


from tile import Tile

#
#   i,j
#  
#   0,0  0,1  0,2
#   1,0  1,1  1,2
#   2,0  2,1  2,2   
#

class Matrix():

    def __init__(self) -> None:
        self.m = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.sel = None

    # Get element
    def get(self, pos):
        return self.m[pos[0]][pos[1]]

    # Put element
    def put(self, pos, elem):
        self.m[pos[0]][pos[1]] = elem
    
    # Get all elements as list
    def elements(self):
        l = []
        for i in range(3):
            for j in range(3):
                l.append(self.m[i][j])
        return l
    
    # reset
    def reset(self):
        for i in range(3):
            for j in range(3):
                self.m[i][j].reset()
        self.select((1,1))
    
    # Select
    def select(self, pos):
        if self.sel:
            self.get(self.sel).unselect()
        self.sel = pos
        self.get(self.sel).select()
    
    # Selected tile -> position
    def get_selected_pos(self):
        return self.sel

    # Selected tile -> position
    def get_selected(self):
        if self.sel:
            return self.get(self.sel)
        else:
            return None
