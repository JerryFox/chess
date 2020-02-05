# chessboard the main model file
# used for backend (bottle) and frontend (brython) too
# html with SVG generation

CHESS_IMG_FOLDER = "static/images/"
FIGURES = "RNBKQBNRPrnbkqbnrp"
SCRIPT_FOLDER = "static/scripts/"
CSS_FOLDER = "static/css/"

chessboard = [["" for i in range(8)]for j in range(8)]

chessboard[0] = list("RNBKQBNR")
chessboard[1] = list("P" * 8)
chessboard[6] = list("p" * 8)
chessboard[7] = list("rnbkqbnr")

def packed_to_unpacked_position(position="base"):
    if position == "base":
        position = "rnbqkbnr" + "p" * 8 + "-" * 32 + "P" * 8 + "RNBQKBNR"
    elif position == "blank":
        position = ""
    number_of_blanks = 0
    unpacked_position = ""
    for character in position:
        if character.isdigit():
            number_of_blanks = number_of_blanks * 10 + int(character)
            #print(number_of_blanks)
        else:
            unpacked_position += "-" * number_of_blanks
            number_of_blanks = 0
            unpacked_position += character if character in FIGURES else "-"
    # justify to 64 characters
    unpacked_position = (unpacked_position + "-" * 64)[:64]
    return unpacked_position

def get_img_name(shortcut):
    """file name of figure shortcut's image
    shortcuts:
    RNBKQBNRP - dark figures (d)
    rnbkqbnrp - light figures (l)
    image name format example:
    Chess_klt45.svg - white king
    """
    name = "Chess_{}{}t45.svg".format(shortcut.lower(),
                                      "l" if shortcut.isupper() else "d")
    return name

def image_element_code(row, column, shortcut, beside=False):
    image_template = """<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink"
xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); "
width="80" height="80"
class="chess-figure draggable{}"
transform="matrix(1 0 0 1 0 0)"
onmousedown="if (event.preventDefault) event.preventDefault()"
></image>"""
    return image_template.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut), " source" if beside else "")

def beside_figures_images():
    # images beside chessboard (for adding on chessboard)
    add_board = [["k", "q"], ["r", "b"], ["n", "p"], ["", ""], ["", ""],
                 ["K", "Q"], ["R", "B"], ["N", "P"]]
    images = ""
    for row in range(len(add_board)):
        for column in range(len(add_board[0])):
            if add_board[row][column]:
                images += image_element_code(row, column + 8, add_board[row][column], True) + "\n"
    return images

class Chessboard:

    def __init__(self, position="base"):
        self.position = position
        self.chessboard = self.get_chessboard()
        self.moves = []
        self.rec_moves = []
        self.last_color = None
        self.move_validation = True
        self.trash = []
        self.move_counter = 0
        self.initial_position = self.position
        self.play_mode = None

    def get_chessboard(self):
        position = packed_to_unpacked_position(self.position)
        chessboard = [["" if c == "-" else c
                       for c in position[i * 8 : i * 8 + 8]] for i in range(8)]
        return chessboard


    def get_html(self, zoom="600px"):
        from bottle import template
        from config import PROJECT_DIRECTORY
        if "px" not in zoom:
            zoom="600px"
        context = {
            "script_folder": "/static/scripts/",
            "css_folder": "/static/css/",
            "img_folder": "/static/images/",
            "zoom": zoom,
            "chessboard": self.chessboard,
            "position": self.position,
            "packed_position": self.get_packed_position(),
            }
        return template(PROJECT_DIRECTORY + "/views/" + "base", context)
        #return html_source_code(svg_element_code(self.chessboard, zoom))

    def get_packed_position(self):
        chessboard = self.chessboard
        position = ""
        number_in_string = 0
        pos_pack = ""
        for row in range(len(chessboard)):
            for column in range(len(chessboard[0])):
                if chessboard[row][column]:
                    position += chessboard[row][column]
                    if number_in_string:
                        if number_in_string > 1:
                            pos_pack += str(number_in_string)
                        else:
                            pos_pack += "-"
                    pos_pack += chessboard[row][column]
                    number_in_string = 0
                else:
                    position += "-"
                    number_in_string += 1
        if number_in_string:
            if number_in_string > 1:
                pos_pack += str(number_in_string)
            else:
                pos_pack += "-"
        return pos_pack

    def set_position_to_packed(self):
        self.position = self.get_packed_position()

    def set_chessboard_from_position(self):
        self.chessboard = self.get_chessboard()

    def add_figures(self, figure_positions):
        """add figures on chessboard
        figure_positions: str - <figure_name><coords>
        coords: 00 or a8
        example: "P00P11pg2ph1"
        """
        while len(figure_positions) > 2:
            figure = figure_positions[:3]
            figure_positions = figure_positions[3:]
            if figure[0] in FIGURES:
                if figure[1].isdigit():     # 00 address
                    row = int(figure[1])
                    col = int(figure[2])
                else:                       # a1 address
                    row = 8 - int(figure[2])
                    col = ord(figure[1].upper()) - 65
            self.chessboard[row][col] = figure[0]
        self.set_position_to_packed()

    def remove_figures(self, positions):
        """remove figures from positions
        positions: str - <coords>
        coords: 00 or a8
        example: "0011g2h1"
        """
        while len(positions) > 1:
            pos = positions[:2]
            positions = positions[2:]
            if pos[0].isdigit():    # 00 address
                row = int(pos[0])
                col = int(pos[1])
            else:                   # a1 address
                row = 8 - int(pos[1])
                col = ord(pos[0].upper()) - 65
            self.chessboard[row][col] = ""
        self.set_position_to_packed()

    def cell_moves(self, row, col=None):
        if col is None:
            col = row[1]
            row = row[0]
        c_moves = [pair[0] for pair in self.moves if pair[0] == [row, col]]
        return bool(c_moves)

    def move(self, src, dst, add=None):
        color = None
        result = []
        sour_figure = self.chessboard[src[0]][src[1]]
        dest_figure = self.chessboard[dst[0]][dst[1]]
        if sour_figure and dst in self.get_valid_moves(src[0], src[1]):
            self.chessboard[src[0]][src[1]] = ""
            self.chessboard[dst[0]][dst[1]] = sour_figure
            self.moves.append([src, dst])
            result.append([src, dst])
            # castlings - king moving two squares towards a rook
            if sour_figure in "Kk" and abs(src[1] - dst[1]) == 2:
                # appropriate rook move
                if dst[1] > src[1]:
                    rook = self.chessboard[src[0]][7]
                    self.chessboard[src[0]][7] = ""
                    self.chessboard[src[0]][5] = rook
                    result.append([[src[0], 7], [src[0], 5]])
                else:
                    rook = self.chessboard[src[0]][0]
                    self.chessboard[src[0]][0] = ""
                    self.chessboard[src[0]][3] = rook
                    result.append([[src[0], 0], [src[0], 3]])
            self.last_color = "w" if sour_figure.isupper() else "b"
            if dest_figure:
                self.trash.append([dest_figure, dst])
                self.moves[-1].append("x")
        return result

    def get_valid_moves(self, row, col, shortcut=None):
        if shortcut is None:
            shortcut = self.chessboard[row][col]
        chessboard = self.chessboard
        valid_moves = []
        if ((self.last_color == "w" and shortcut.isupper()) \
            or (self.last_color == "b" and shortcut.islower())):
            return valid_moves
        if shortcut.upper() == "N":
            pos_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
            valid_moves = []
            for move in pos_moves:
                new_row = row + move[0]
                new_col = col + move[1]
                figure_on_destination = None
                if new_row in range(8) and new_col in range(8):
                    figure_on_destination = chessboard[new_row][new_col]
                    if not figure_on_destination or figure_on_destination.isupper() != \
                        shortcut.isupper():
                        valid_moves.append([new_row, new_col])
        elif shortcut.upper() == "P":
            valid_moves = []
            new_row1 = None
            if shortcut == "P":
                new_row = row - 1;
                if row == 6:
                    new_row1 = row - 2
            else:
                new_row = row + 1
                if row == 1:
                    new_row1 = row + 2
            if new_row in range(8) and not chessboard[new_row][col]:
                valid_moves.append([new_row, col])
                if new_row1 and not chessboard[new_row1][col]:
                    valid_moves.append([new_row1, col])
            for shift in [-1, 1]:
                new_col = col + shift
                if new_row in range(8) and new_col in range(8):
                    figure_on_destination = chessboard[new_row][new_col]
                    if  figure_on_destination and figure_on_destination.isupper() != \
                        shortcut.isupper():
                        valid_moves.append([new_row, new_col])
        elif shortcut.upper() in "QK":
            directions = [[1, 0], [1, 1], [0, 1], [1, -1]]
            coefs = []
            if shortcut.upper() == "Q":
                coefs = [[-row - 1, 8 - row], [-min(row, col) - 1, 8 - max(row, col)], \
                    [-col - 1, 8 - col], [max(-row - 1, col - 8), min(8 - row, col + 1)]]
            else:
                coefs = [[max(-row - 1, -2), min(8 - row, 2)], \
                    [max(-min(row, col) - 1, -2), min(8 - max(row, col),2)], \
                    [max(-col - 1, -2), min(8 - col, 2)], \
                    [max(max(-row - 1, col - 8), -2), min(min(8 - row, col + 1), 2)]]
                # castlings - king moving from original position two squares towards a rook
                # find king moves
                if col == 4 and not self.cell_moves(row, col):
                    if not chessboard[row][col + 1] and not chessboard[row][col + 2] \
                        and chessboard[row][col + 3] and not self.cell_moves([row], [col + 3]):
                        valid_moves.append([row, col + 2])
                    if not chessboard[row][col - 1] and not chessboard[row][col - 2] \
                        and not chessboard[row][col - 3] \
                        and chessboard[row][col - 4] and not self.cell_moves([row], [col - 4]):
                        valid_moves.append([row, col - 2])
        elif shortcut.upper() == "B":
            directions = [[1, 1], [1, -1]]
            coefs = [[-min(row, col) - 1, 8 - max(row, col)], [max(-row - 1, col - 8), min(8 - row, col + 1)]]
        elif shortcut.upper() == "R":
            directions = [[1, 0], [0, 1]]
            coefs = [[-row - 1, 8 - row], [-col - 1, 8 - col]]
        if shortcut.upper() in "QKBR" and coefs:
            for index, direction in enumerate(directions):
                #for coef in range(coefs[index][0], coefs[index][1]):
                for (ifrom, ito, istep) in ((-1, coefs[index][0], -1), (1, coefs[index][1], 1)):
                    for coef in range(ifrom, ito, istep):
                        new_row = row + coef * direction[0]
                        new_col = col + coef * direction[1]
                        #if coef != 0:
                        figure_on_destination = chessboard[new_row][new_col]
                        if  figure_on_destination:
                            if figure_on_destination.isupper() != \
                                shortcut.isupper():
                                valid_moves.append([new_row, new_col])
                            break
                        else:
                            valid_moves.append([new_row, new_col])
        return valid_moves

if __name__ == "__main__":
    f = open("chessboard.htm", "w")
    to_write = html_source_code(svg_element_code(chessboard))
    f.write(to_write)
    f.close()
