#!/usr/bin/python


class Tile:

    def __init__(self, blocks):
        self.board = False
        self.blocks = blocks
        self.size = 0

    def get_blocks(self):
        return self.blocks

    def set_board(self, board):
        self.board = board

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size


class Letter:

    def __init__(self, position):
        self.position = position

    def get_position(self):
        return self.position
