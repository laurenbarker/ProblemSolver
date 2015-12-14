#!/usr/bin/python

import Tkinter as tk
import FileReader as fileReader
from tile import Piece
from tile import Tile


class MainWindow(tk.Frame):
    puzzle_name = 'No puzzle selected'

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(
            self, text="Puzzle 1",
            command=lambda puzzle_name='input_small.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Puzzle 2",
            command=lambda puzzle_name='input_checkerboard.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")
        self.button = tk.Button(
            self, text="Puzzle 3",
            command=lambda puzzle_name='pentominoes3x20.txt': self.create_window(puzzle_name)
        )
        self.button.pack(side="top")

    def create_window(self, puzzle_name):
        t = tk.Toplevel(self)
        t.wm_title("Puzzle: %s" % puzzle_name)
        content = fileReader.read_file(puzzle_name)
        puzzle_pieces = self.get_puzzle_pieces(content)
        board = tk.Canvas(t, bg="grey", height=250, width=500)
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
        board.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    # create list of x values used for a tile object
    # remove x values from list once a grey square on the x value
    def get_puzzle_pieces(self, content):
        all_tiles = []
        all_indexes = []
        all_pieces = []
        tile_position_y = 0
        for line in content:
            tile_position_x = 0
            for letter in line:
                if letter != ' ':
                    new_position = [tile_position_x, tile_position_y]
                    new_tile = Tile(new_position)
                    all_tiles.append(new_tile)
                    all_indexes.append(new_position)
                tile_position_x = tile_position_x + 1
            tile_position_y = tile_position_y + 1

        for tile in all_tiles:
            position = tile.get_position()
            check_position_up = [position[0], position[1] - 1]
            check_position_left = [position[0] - 1, position[1]]
            check_position_up_right = [position[0] + 1, position[1] - 1]

            if check_position_up in all_indexes or check_position_left in all_indexes or check_position_up_right in all_indexes:
                for piece in all_pieces:
                    blocks = piece.get_blocks()
                    if check_position_up in blocks or check_position_left in blocks or check_position_up_right in blocks:
                        piece.add_block(position)
            else:
                piece = Piece(position)
                all_pieces.append(piece)

        # import pdb; pdb.set_trace()
        return all_pieces

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    root.mainloop()
