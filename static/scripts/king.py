from walk import doc
from random import choice

k = doc.ch_board.add_figure("K", 0, 0)

def move(figure):
    #print("funkce move")
    directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
    if figure.shortcut.upper() == "K":
        direct = choice(directions)
        new_row = figure.row + direct[0]
        new_col = figure.col + direct[1]
        #print(new_row, new_col)
        if new_row in range(8) and new_col in range(8):
            figure.move_to(new_row, new_col)


