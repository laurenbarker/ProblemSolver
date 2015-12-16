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
        self.positions = []
        for block in blocks:
            self.positions.append(block.get_position())

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            self.increment_size()
            self.positions.append(block.get_position())

    def get_positions(self):
        return sorted(self.positions)

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

    def set_position(self, position):
        self.position = position

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


def zero_pieces(pieces):
    zeroed_pieces = []
    for piece in pieces:
        piece_blocks = sorted(piece.get_positions())
        y_list = []
        for y in piece_blocks:
            y_list.append(y[1])
        first_piece = piece_blocks[0]
        value_x = first_piece[0]
        value_y = sorted(y_list)[0]
        new_blocks = []
        for block in piece.get_blocks():
            new_position_x = block.get_position()[0] - value_x
            new_position_y = block.get_position()[1] - value_y
            block.set_position([new_position_x, new_position_y])
            new_blocks.append(block)
        piece.set_blocks(new_blocks)
        zeroed_pieces.append(piece)

    return zeroed_pieces


def add_rotations(pieces):
    return 0


def add_reflections(pieces):
    return 0
