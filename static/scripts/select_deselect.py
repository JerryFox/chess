"""
select_deselect.py
brython script
"""

from browser import document
from browser import document as doc
#from chess_brython import Chess_figure
from chess import Chessboard
from browser import document as doc, timer, alert
from random import choice

def kb_move(move, color):
    """knight base move"""
    pass

def move(source, destination=None, add=None):
    """move figure from source to destination
    """
    if destination is None:
        # coordinates are in list
        destination = source[1]
        source = source[0]
    items = [source, destination]
    for index, item in enumerate(items):
        if type(item) == str:
            col = ord(item[0].lower()) - ord("a")
            row = 8 - int(item[1])
            items[index] = [row, col]
    [source, destination] = items
    sour_figure = None
    dest_figure = None
    ch = doc.ch_board
    result = ch.move(source, destination)
    if result:
        sour_figure = doc.ch_board.figures[source[0]][source[1]][-1]
        if len(ch.moves[-1]) > 2 and "x" in ch.moves[-1][-1]:
            dest_figure = doc.ch_board.figures[destination[0]][destination[1]][-1]
            dest_figure.remove()
        sour_figure.move_to(destination)
        if len(result) > 1:
            # additional move
            source = result[1][0]
            destination = result[1][1]
            sour_figure = doc.ch_board.figures[source[0]][source[1]][-1]
            sour_figure.move_to(destination)
    return (sour_figure, dest_figure)

def add_target(x, y):
    """target = cell rounded with green rectangle
    shown / hidden by click + SHIFT"""
    cursor = document["cursor"]
    clone = cursor.cloneNode()
    clone.removeAttribute("id")
    clone.setAttribute("class", "targets")
    clone.setAttribute("stroke", "darkgreen")
    clone.setAttribute("stroke-width", "4")
    clone.setAttribute("x", x)
    clone.setAttribute("y", y)
    clone.setAttribute("width", "90")
    clone.setAttribute("height", "90")
    clone.setAttribute("transform", "matrix(1 0 0 1 10 10)")
    cursor.insertAdjacentElement('beforebegin', clone)

def set_targets_from_moves(moves):
    """ targets list of rows and columns"""
    remove_targets()
    for target in moves:
        add_target(target[1] * 100, target[0] * 100)

def remove_targets():
    targets = doc.get(selector="rect.targets")
    for target in targets:
        target.remove()

def select_element(evt):
    """
    selecting movable element
    on the mouse down
    """
    document.ch_moving_figure = None
    evt.preventDefault()
    selected_element = evt.target
    me = document.getElementById("moving")
    if me:
        me.removeAttribute("id")
    selected_element.setAttribute("id", "moving")
    # current matrix
    cm = selected_element.getAttribute("transform").split("(")[1].split(")")[0].split()
    cm = [float(i) for i in cm]
    # clone figure outside chessboard
    x = int(selected_element.getAttribute("x"))
    x += cm[4]
    if x > 810:
        clone = selected_element.cloneNode()
        clone.removeAttribute("id")
        selected_element.insertAdjacentElement('beforebegin', clone)
        clone.bind("mousedown", select_element)
    else:
        document.ch_moving_figure = document.ch_board.figures[document.coord[0]][document.coord[1]][-1]
        document.ch_board.figures[document.coord[0]][document.coord[1]].remove(document.ch_moving_figure)
        document.ch_current_coord = document.coord
        #document.ch_move_validation = True
        if hasattr(document, "ch_move_validation") and document.ch_move_validation:
            remove_targets()
            row = document.coord[0]
            col = document.coord[1]
            figure = document.ch_moving_figure
            set_targets_from_moves(figure.get_valid_moves())

    # move selected figure on top
    document.querySelector('.figures').insertAdjacentElement('beforeend',selected_element)
    # save variables to document
    document.ch_current_x = evt.clientX
    document.ch_current_y = evt.clientY
    document.ch_selected_element = selected_element
    document.ch_current_matrix = cm
    # document.ch_zoom_chessboard = zoom_chessboard
    # events binding
    # selected_element.bind("mousemove", move_element)
    # selected_element.bind("mouseout", deselect_element);
    selected_element.bind("mouseup", deselect_element)

def deselect_element(evt):
    """
    unselecting movable element
    on the mouse up
    """
    if document.ch_selected_element:
        sel_elem = document.ch_selected_element
        sel_elem.classList.remove("source")
        cm = sel_elem.getAttribute("transform").split("(")[1].split(")")[0].split()
        cm = [int(float(i)) for i in cm]
        #cm = document.ch_current_matrix
        cm[4] = 100 * (round(cm[4] / 100))
        cm[5] = 100 * (round(cm[5] / 100))
        row = (cm[5] + int(sel_elem.getAttribute("y"))) // 100
        col = (cm[4] + int(sel_elem.getAttribute("x"))) // 100
        m = [str(i) for i in cm]
        sel_elem.setAttribute("transform", "matrix ({})".format(" ".join(m)))
        sel_elem.unbind("mousemove")
        sel_elem.unbind("mouseup")
        sel_elem.unbind("mouseout")
        document.ch_selected_element = None
        x = int(sel_elem.getAttribute("x"))
        x += cm[4]
        if x > 810:
            sel_elem.remove()
        else:
            if document.ch_moving_figure:
                castling = False
                # move validation
                if hasattr(document, "ch_move_validation") and document.ch_move_validation:
                    source = document.ch_current_coord
                    destination = [row, col]
                    ch = doc.ch_board
                    result = ch.move(source, destination)
                    if result:
                        valid = True
                        ch.play_mode = "play"
                        #sour_figure = doc.ch_board.figures[source[0]][source[1]][-1]
                        if len(ch.moves[-1]) > 2 and "x" in ch.moves[-1][-1]:
                            dest_figure = ch.figures[destination[0]][destination[1]][-1]
                            dest_figure.remove()
                        #sour_figure.move_to(destination)
                        if len(result) > 1:
                            # additional move
                            source = result[1][0]
                            destination = result[1][1]
                            sour_figure = doc.ch_board.figures[source[0]][source[1]][-1]
                            sour_figure.move_to(destination)
                    else:
                        # move reset
                        valid = False
                        (row, col) = document.ch_current_coord
                        cm = document.ch_current_matrix
                        m = [str(i) for i in cm]
                        sel_elem.setAttribute("transform", "matrix ({})".format(" ".join(m)))
                if [row, col] != document.ch_current_coord:
                    document.ch_moving_figure.moves.append([row, col])
                    """
                    if not castling:
                        document.ch_board.moves.append([document.ch_current_coord, [row, col]])
                    else:
                        document.ch_board.moves.insert(-1, [document.ch_current_coord, [row, col]])
                    """
                document.ch_board.figures[row][col].append(document.ch_moving_figure)
                #document.ch_board.chessboard[row][col] = document.ch_moving_figure.shortcut
                document.ch_moving_figure.row = row
                document.ch_moving_figure.col = col
            else:
                figure_file = sel_elem.getAttribute("xlink:href")
                figure_shortcut = figure_file.split("_")[1][:2]
                figure_shortcut = figure_shortcut[0] if figure_shortcut[1] == "d" else figure_shortcut[0].upper()
                new_figure = ChessFigure(figure_shortcut, sel_elem, row, col)
                new_figure.place_on_board(document.ch_board)

class ChessFigure:

    def __init__(self, shortcut, svg_image=None, row=None, col=None):
        self.shortcut = shortcut
        self.svg_image = svg_image
        self.row = row
        self.col = col
        self.zindex = None
        self.chessboard = None
        self.idtimer = None
        self.timer_interval = 5000
        self.knight_logic = None
        self.moves = []
        self.initial_position = [row, col]

    def place_on_board(self, chessboard):
        self.chessboard = chessboard
        chessboard.figures[self.row][self.col].append(self)
        chessboard.chessboard[self.row][self.col] = self.shortcut

    def move_to(self, row, col=None):
        if col is None:
            col = row[1]
            row = row[0]
        if row in range(len(self.chessboard.chessboard)) and col in range(len(self.chessboard.chessboard[row])):
            oldrow = self.row
            oldcol = self.col
            self.chessboard.figures[self.row][self.col].remove(self)
            self.row = row
            self.col = col
            self.chessboard.figures[self.row][self.col].append(self)
            self.moves.append([row, col])
            # last_color
            if self.svg_image:
                # redisplay svg
                m = self.svg_image.getAttribute("transform")
                m = m.split("(")[1].split(")")[0].split()
                m[4] = str(int(float(m[4])) + 100 * (col - oldcol))
                m[5] = str(int(float(m[5])) + 100 * (row - oldrow))
                self.svg_image.setAttribute("transform", "matrix(" + " ".join(m) + ")")
                doc.querySelector('.figures').insertAdjacentElement('beforeend',self.svg_image)

    def remove(self):
        board = self.chessboard
        board.figures_trash.append(self)
        self.svg_image.remove()
        #self.chessboard = None
        board.figures[self.row][self.col].remove(self)
        #board.chessboard[self.row][self.col] = ""

    def get_valid_moves(self):
        return self.chessboard.get_valid_moves(self.row, self.col, self.shortcut)

    def go(self):
        if self.shortcut.upper() == "N":
            valid_moves = self.get_valid_moves()
            """get_valid
            pos_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
            for move in pos_moves:
                new_row = self.row + move[0]valid
                new_col = self.col + move[1]
                figure_on_destination = None
                if new_row in range(8) and new_col in range(8):
                    if self.chessboard.figures[new_row][new_col]:
                        figure_on_destination = selvalidf.chessboard.figures[new_row][new_col][-1]
                    if not figure_on_destination or figure_on_destination.shortcut.isupper() != \
                        self.shortcut.isupper():
                        valid_moves.append([new_row, new_col])
            """
            if valid_moves:
                if self.knight_logic:
                    self.knight_logic(self, valid_moves)
                else:
                    # find opponents
                    # first move
                    figure_on_destination = None
                    for move in valid_moves:
                        if self.chessboard.figures[move[0]][move[1]]:
                            figure_on_destination = self.chessboard.figures[move[0]][move[1]][-1]
                            break
                    if not figure_on_destination:
                        # second move
                        for m1 in valid_moves:
                            for m in self.get_valid_moves():
                                if self.chessboard.figures[m[0]][m[1]]:
                                    figure_on_destination = self.chessboard.figures[m[0]][m[1]][-1]
                                    move = m1
                                    break
                    if not figure_on_destination:
                        move = choice(valid_moves)
                    # remove other figure
                    if self.chessboard.figures[move[0]][move[1]]:
                        self.chessboard.remove_figure(move[0], move[1])
                    self.move_to(move[0], move[1])
                    self.idtimer = timer.set_timeout(self.go, self.timer_interval)
            else:
                alert("{fig} {row} {col}: nemám kam táhnout".format(fig=self.shortcut, row=self.row, col=self.col))

    def stop(self):
        timer.clear_timeout(self.idtimer)
        self.idtimer = None

class Board(Chessboard):

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.figures = [[[] for col in range(len(self.chessboard[row]))] for row in range(len(self.chessboard))]
        self.figures_trash = []
        self.timer_interval = 1000
        self.idtimer = None

    def add_figure(self, figure="P", row=0, col=0):
        """
        add new figure on the top
        """
        new_figure = ChessFigure(figure)
        """
        if not doc.ch_board:
            get_chessboard()
        """
        source = doc.ch_board.beside_figures
        clone = source[figure].cloneNode()
        x = col * 100 + int(clone.getAttribute("x")) % 100
        y = row * 100 + int(clone.getAttribute("y")) % 100
        clone.setAttribute("x", str(x))
        clone.setAttribute("y", str(y))
        clone.setAttribute("transform", "matrix (1 0 0 1 0 0)")
        source[figure].insertAdjacentElement('beforebegin', clone)
        clone.bind("mousedown", select_element)
        doc.querySelector('.figures').insertAdjacentElement('beforeend',clone)
        new_figure.row = row
        new_figure.col = col
        new_figure.svg_image = clone
        new_figure.chessboard = self
        self.figures[row][col].append(new_figure)
        self.add_figures(figure + str(row) + str(col))
        return new_figure

    def remove_figures(self, chessboard=None, top_only=False):
        """
        remove top figures or all figures
        chessboard - delete mask
        """
        if not chessboard:
            chessboard = [["x" for col in range(8)] for row in range(8)]
        ch = self.figures
        for row in range(len(chessboard)):
            for col in range(len(chessboard[row])):
                if chessboard[row][col] and ch[row][col]:
                    if top_only:
                        ch[row][col][-1].svg_image.remove()
                        ch[row][col][-1].chessboard = None
                        ch[row][col].remove(ch[row][col][-1])
                    else:
                        for img in ch[row][col]:
                            img.svg_image.remove()
                            img.chessboard = None
                        ch[row][col] = []
                    if not ch[row][col]:
                        self.chessboard[row][col] = ""
                    else:
                        self.chessboard[row][col] = ch[row][col][-1].shortcut

    def remove_figure(self, row, col=None):
        """
        remove bottom figure from the cell
        """
        if col is None:
            col = row[1]
            row = row[0]
        if self.figures[row][col]:
            self.figures[row][col][0].svg_image.remove()
            self.figures[row][col][0].chessboard = None
            self.figures[row][col].remove(self.figures[row][col][0])
            if not self.figures[row][col]:
                self.chessboard[row][col] = ""
            else:
                self.chessboard[row][col] = self.figures[row][col][-1].shortcut

    def add_figures_from_board(self, chessboard=None):
        if chessboard is None:
            chessboard = Chessboard().chessboard
        for ri, row in enumerate(chessboard):
            for ci, col in enumerate(row):
                if col:
                    self.add_figure(col, ri, ci)

    def refresh_figures(self):
        chboard = [[col for col in row] for row in self.chessboard]
        self.remove_figures()
        self.add_figures_from_board(chboard)


def get_knight_moves(row, col):
    """chess - knight moves
    g is a list of generators
    Each generator generates a list of pairs of coordinates.
    g[0] - starting position (SP), g[1] - SP, first moves, g[2] - SP, first m.,
    second m., ...
    """
    pos_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                 [1, 2], [1, -2], [-1, 2], [-1, -2]]

    g0 = ([[row, col]] for i in range(1))
    g = [g0]

    for i in range(10):
        index = len(g) - 1
        # with any of commented lines generator doesn't work - why???!!!:
        """
>>> g = get_knight_moves(0, 0)
>>> count = 0
>>> for i in g[5]: count = count + 1
Traceback (most recent call last):
  module <module> line 1
    for i in g[5]: count = count + 1
ValueError: generator already executing
        """
        #g += [(moves + [[moves[-1][0] + move[0], moves[-1][1] + move[1]]] for moves in g[-1] for move in pos_moves if (moves[-1][0] + move[0]) in range(8) and (moves[-1][1] + move[1]) in range(8) and not [moves[-1][0] + move[0], moves[-1][1] + move[1]] in moves)]
        #g += [(moves + [[moves[-1][0] + move[0], moves[-1][1] + move[1]]] for moves in g[len(g) - 1] for move in pos_moves if (moves[-1][0] + move[0]) in range(8) and (moves[-1][1] + move[1]) in range(8) and not [moves[-1][0] + move[0], moves[-1][1] + move[1]] in moves)]
        g += [(moves + [[moves[-1][0] + move[0], moves[-1][1] + move[1]]] for moves in g[index] for move in pos_moves if (moves[-1][0] + move[0]) in range(8) and (moves[-1][1] + move[1]) in range(8) and not [moves[-1][0] + move[0], moves[-1][1] + move[1]] in moves)]
    return g

def get_generators():
    # returns list of generators
    # generator with index n generates from generator with index n-1
    g = [([] + [0] for i in range(1))] # initial list

    for i in range(10):
        index = len(g) - 1
        g += [(x + [x[-1] + 1] for x in g[-1])]
        #g += [(x + [x[-1] + 1] for x in g[index])]
        # with any of commented lines generator doesn't work - why???!!!:
        """
>>> g = get_knight_moves(0, 0)
>>> count = 0
>>> for i in g[5]: count = count + 1
Traceback (most recent call last):
  module <module> line 1
    for i in g[5]: count = count + 1
ValueError: generator already executing
        """
    return g

