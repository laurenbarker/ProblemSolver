#!/usr/bin/python


class Piece:

    def __init__(self, block):
        self.board = False
        self.blocks = [block]
        self.size = 1
        self.positions = [block.get_position()]

    def get_blocks(self):
        return self.blocks

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            self.increment_size()
            self.positions.append(block.get_position())

    def get_positions(self):
        return self.positions

    def set_board(self, board):
        self.board = board

    def get_size(self):
        return self.size

    def increment_size(self):
        self.size = self.size + 1


class Tile:

    def __init__(self, position):
        self.position = position
        self.color = 0

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color
