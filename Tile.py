#!/usr/bin/python
import sys


class Piece:

    def __init__(self, blocks):
        self.board = False
        self.blocks = blocks
        self.size = len(blocks)
        self.positions = []
        self.rotations = []
        self.reflections = []
        self.locations = []
        for block in blocks:
            self.positions.append(block.get_position())

    def get_blocks(self):
        return self.blocks

    def set_blocks(self, blocks):
        self.blocks = blocks
        self.positions = []
        for block in blocks:
            self.positions.append(block.get_position())
        self.rotations = add_rotations(blocks, self.positions, self)
        self.reflections = add_reflections(blocks)

    def add_block(self, block):
        if block not in self.blocks:
            self.blocks.append(block)
            self.increment_size()
            self.positions.append(block.get_position())

    def get_positions(self):
        return sorted(self.positions)

    def get_rotations(self):
        return sorted(self.rotations)

    def get_reflections(self):
        return sorted(self.reflections)

    def get_locations(self):
        return self.locations

    def set_locations(self, locations):
        self.locations = locations

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
            return self.get_positions() == other.get_positions()
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
        sys.setrecursionlimit(10000)
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


def add_rotations(blocks, positions, piece):
    # [r, c] --> [dist from max_x, dist from max_y]
    rotations = [piece]
    if len(positions) == 1:
        return rotations

    new_positions_1 = []
    new_positions_2 = []
    new_positions_3 = []
    y_list = []
    x_list = []
    for y in positions:
        y_list.append(y[1])
        x_list.append(y[0])
    max_x = sorted(x_list)[len(x_list) - 1]
    max_y = sorted(y_list)[len(y_list) - 1]

    # first rotation right
    for block in blocks:
        position = block.get_position()
        position_x = position[0]
        position_y = position[1]
        new_position = Tile([max_y - position_y,  position_x])
        new_position.set_color(block.get_color())
        new_positions_1.append(new_position)
    piece_1 = Piece(sorted(new_positions_1))
    rotations.append(piece_1)

    # second rotation right
    for block in new_positions_1:
        position = block.get_position()
        position_x = position[0]
        position_y = position[1]
        new_position = Tile([max_x - position_y,  position_x])
        new_position.set_color(block.get_color())
        new_positions_2.append(new_position)
    piece_2 = Piece(sorted(new_positions_2))
    rotations.append(piece_2)

    # third rotation right
    for block in new_positions_2:
        position = block.get_position()
        position_x = position[0]
        position_y = position[1]
        new_position = Tile([max_y - position_y, position_x])
        new_position.set_color(block.get_color())
        new_positions_3.append(new_position)
    piece_3 = Piece(sorted(new_positions_3))
    rotations.append(piece_3)

    return rotations


def add_reflections(positions):
    return []


def find_locations(pieces, board, max_x, max_y):
    # returns dictionary: key = piece, value = # of locations it can be placed

    # Criteria for if it can be place in a location
        # does the piece physically fit on the board
        # do the colors of tiles match the color on board

    # dict piece and number
    location_number = {}

    board_index = {}
    for tile in board.get_blocks():
        board_index[str(tile.get_position())] = tile

    # each available piece
    for piece in pieces:
        number = 0
        rotations = piece.get_rotations()

        # each rotation for a piece
        for rotation in rotations:
            locations = []
            tiles_by_position = {}
            sorted_rotation = sorted(rotation.get_positions())
            for tile in rotation.get_blocks():
                tiles_by_position[str(tile.get_position())] = tile

            last_in_list = len(sorted_rotation) - 1
            # check to see if piece will even fit on board at the location
            if sorted_rotation[last_in_list][0] <= max_x and sorted_rotation[last_in_list][1] <= max_y:
                counter = [0, 0]
                column_counter = 0
                # check each location on board for each rotation
                while column_counter <= max_y:
                    match = False
                    for location in sorted_rotation:
                        board_space = [counter[0] + location[0], counter[1] + location[1]]
                        if board_index.get(str(board_space)) is not None:
                            if board_index.get(str(board_space)).get_color() == tiles_by_position.get(str(location)).get_color():
                                match = True
                            else:
                                match = False
                                break
                        else:
                            match = False
                            break

                    if match is True:
                        first = board_space[0] - location[0]
                        second = board_space[1] - location[1]
                        locations.append([[first, second], rotation.get_positions()])
                        number = number + 1

                    if counter[0] == max_x and counter[1] == max_y:
                        break
                    elif counter[0] == max_x:
                        column_counter = column_counter + 1
                        counter[0] = 0
                        counter[1] = column_counter
                    else:
                        counter[0] = counter[0] + 1
            rotation.set_locations(locations)

            if location_number.get(number) is not None and len(locations) > 0:
                if piece not in location_number[number]:
                    location_number[number].append(rotation)
            elif number != 0 and len(locations) > 0:
                location_number[number] = [rotation]

        # import pdb; pdb.set_trace()

    return location_number
