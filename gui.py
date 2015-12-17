#!/usr/bin/python

import Tkinter as tk
import FileReader as fileReader
from tile import Piece
from tile import Tile
from tile import combine_pieces
from tile import zero_pieces
from tile import find_locations


class MainWindow(tk.Frame):
    puzzle_name = 'No puzzle selected'

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(
            self, text="Small Puzzle",
            command=lambda puzzle_name='input_small.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Checkerboard",
            command=lambda puzzle_name='input_checkerboard.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Pentominoes 3x20",
            command=lambda puzzle_name='pentominoes3x20.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")

    def create_window(self, puzzle_name):
        t = tk.Toplevel(self)
        t.wm_title("Puzzle: %s" % puzzle_name)
        content = fileReader.read_file(puzzle_name)

        puzzle_pieces_and_board = self.get_puzzle_pieces(content)
        puzzle_pieces = puzzle_pieces_and_board[0]
        game_board = puzzle_pieces_and_board[1]

        board = tk.Canvas(t, bg="grey", height=350, width=600)

        board.button = tk.Button(
            t, text="Solve Puzzle",
            command=lambda puzzle_pieces=puzzle_pieces, game_board=game_board: self.solve_puzzle(puzzle_pieces, game_board)
        )
        board.button.pack(side="top")

        org_x1 = 10
        org_x2 = 20
        org_x3 = 20
        org_x4 = 10
        x1 = org_x1
        y1 = 10
        x2 = org_x2
        y2 = 10
        x3 = org_x3
        y3 = 20
        x4 = org_x4
        y4 = 20
        value1 = ''
        value2 = ''

        for line in content:
            for letter in line:
                if letter == ' ':
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='grey'
                    )
                elif(letter == value1):
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='black'
                    )
                elif(letter == value2):
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='white'
                    )
                elif(letter != value1 and letter != value2 and value1 == ''):
                    value1 = letter
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='black'
                    )
                elif(letter != value1 and letter != value2 and value2 == ''):
                    value2 = letter
                    board.create_polygon(
                        x1, y1, x2, y2, x3, y3, x4, y4, fill='white'
                    )
                x1 = x1 + 10
                x2 = x2 + 10
                x3 = x3 + 10
                x4 = x4 + 10
            y1 = y1 + 10
            y2 = y2 + 10
            y3 = y3 + 10
            y4 = y4 + 10
            x1 = org_x1
            x2 = org_x2
            x3 = org_x3
            x4 = org_x4

        board.pack()
        board.pack(side="top", fill="both", expand=True, padx=50, pady=50)

    # create list of x values used for a tile object
    # remove x values from list once a grey square on the x value
    def get_puzzle_pieces(self, content):
        all_tiles = []
        all_indexes = []
        all_pieces = []

        # find position and color of each tile and store it
        tile_position_y = 0
        color1 = ''
        color2 = ''
        for line in content:
            tile_position_x = 0
            for letter in line:
                if letter != ' ':
                    new_position = [tile_position_x, tile_position_y]
                    new_tile = Tile(new_position)
                    all_indexes.append(new_position)
                    if letter == color2:
                        new_tile.set_color(1)
                    elif color1 == '':
                        color1 = letter
                    elif color2 == '' and letter != color1:
                        color2 = letter
                        new_tile.set_color(1)
                    all_tiles.append(new_tile)

                tile_position_x = tile_position_x + 1
            tile_position_y = tile_position_y + 1

        # searches through list of tiles to find pieces
        piece_to_tile = {}
        for tile in all_tiles:
            position = tile.get_position()
            str_position = str(position)
            check_position_up = [position[0], position[1] - 1]
            check_position_left = [position[0] - 1, position[1]]
            check_position_up_right = [position[0] + 1, position[1] - 1]

            if check_position_up in all_indexes or check_position_left in all_indexes or check_position_up_right in all_indexes:
                for piece in all_pieces:
                    blocks = piece.get_positions()
                    if check_position_up in blocks or check_position_left in blocks or check_position_up_right in blocks:
                        piece.add_block(tile)
                        if str_position in piece_to_tile:
                            # combine current piece and piece with same tile
                            # remove both from all_pieces and add new_piece
                            conflict_piece = piece_to_tile[str_position]
                            new_piece = combine_pieces(piece, conflict_piece)
                            all_pieces.remove(piece)
                            all_pieces.remove(conflict_piece)
                            all_pieces.append(new_piece)

                            piece_to_tile[str_position] = new_piece
                        else:
                            piece_to_tile[str_position] = piece
            else:
                piece = Piece([tile])
                all_pieces.append(piece)
                piece_to_tile[str_position] = piece

        # for key in all_pieces:
        #     print key.get_size()
        all_pieces = zero_pieces(all_pieces)

        # searches through list of pieces to find the board (largest piece)
        largest_piece_index = 0
        largest_size = 0
        piece_index = 0
        for piece in all_pieces:
            if piece.get_size() > largest_size:
                largest_piece_index = piece_index
                largest_size = piece.get_size()
            piece_index = piece_index + 1

        board = all_pieces[largest_piece_index]
        board.set_board(True)
        all_pieces.remove(board)

        import pdb; pdb.set_trace()

        return [all_pieces, board]

    def solve_puzzle(self, puzzle_pieces, game_board):

        y_list = []
        x_list = []
        for value in game_board.get_positions():
            y_list.append(value[1])
            x_list.append(value[0])
        max_x = x_list[len(x_list) - 1]
        max_y = y_list[len(y_list) - 1]

        num_locations = find_locations(puzzle_pieces, game_board, max_x, max_y)

        most_complex_piece = min(num_locations, key=num_locations.get)

        import pdb; pdb.set_trace()

        return []


def backtracking(choice_points, choices, assignable):
    """
    choice_points: is a list of the choice points. Each of them will be
        assigned to a single choice for each solution.
    choices: is a list of choices.
    assignable: is a function that declare if a choice is assignable to a choice point.
          It needs three arguments:
               def assignable(choice, choice_points, solutions):
          In particular, solutions store the assignments of the previous choice points.
          It seems like that {cp0:c0, cp1:c1, ...} where cpI is a choice point and cI is a choice.
    """

    N = len(choices)
    M = len(choice_points)

    # solutions is the dict that has for each choice point (key) a choice (value)
    solutions = {}

    cp = 0
    c = 0
    backtrack = False
    end = False

    while(not end):
        # forward
        while (not backtrack):
            if(assignable(cp, c, solutions)):
                solutions[cp] = c
                if(cp == M-1):
                    yield {choice_points[k]: choices[v] for k, v in solutions.iteritems()}
                    del solutions[cp]
                    if not c == N-1:
                        c += 1
                    else:
                        backtrack = True
                else:
                    cp += 1
                    c = 0
            elif(c != N-1):
                c += 1
            else:
                backtrack = True

        # backward
        end = (cp == 0)
        while(backtrack and not end):
            cp -= 1
            c = solutions.pop(cp)
            if(not c == N-1):
                c += 1
                backtrack = False
            elif(cp == 0):
                end = True

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    root.mainloop()
