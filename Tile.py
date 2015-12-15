#!/usr/bin/python


class Piece:

    def __init__(self, blocks):
        self.board = False
        self.blocks = blocks
        self.size = 1
        self.positions = []
        for block in blocks:
            self.positions.append(block.get_position())

    def get_blocks(self):
        return self.blocks

    def set_blocks(self, blocks):
        self.blocks = blocks

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

    def set_size(self, size):
        self.size = size

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


def combine_pieces(piece1, piece2):
    blocks1 = piece1.get_blocks()
    blocks2 = piece2.get_blocks()
    new_blocks = blocks1
    for block in blocks2:
        if block not in new_blocks:
            new_blocks.append(block)
    new_piece = Piece(new_blocks)
    new_piece.set_size(len(new_blocks))
    return new_piece
