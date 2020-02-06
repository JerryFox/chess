"""
moves.py
brython script
"""

from select_deselect import select_element
from select_deselect import Board, ChessFigure
from browser import document as doc


def get_chessboard():
    """
    creates chessboard object from DOM
    usually called from initial script
    """
    figures_count = 0
    on_board = 0
    chessboard = Board("blank")
    #figures = [[[] for col in range(8)] for row in range(8)]
    beside_figures = {}
    output = ""
    for figure in doc.get(selector=".chess-figure"):
        figures_count += 1
        figure_file = figure.getAttribute("xlink:href")
        figure_shortcut = figure_file.split("_")[1][:2]
        figure_shortcut = figure_shortcut[0] if figure_shortcut[1] == "d" else figure_shortcut[0].upper()
        output += "figure {}:  {} shortcut: {} ".format(figures_count, figure_file, figure_shortcut)
        m = figure.getAttribute("transform")
        m = m.split("(")[1].split(")")[0].split()
        x = int(figure.getAttribute("x")) + int(m[4])
        y = int(figure.getAttribute("y")) + int(m[5])
        column = int(x / 100)
        row = int(y / 100)
        if column < 8 and row < 8:
            figure_object = ChessFigure(figure_shortcut, figure, row, column)
            figure_object.place_on_board(chessboard)
        elif row < 8 and column < 10:
            beside_figures[figure_shortcut] = figure
        output += "x:{} y:{} row: {} col: {}".format(x, y, row, column) + "<br>\n"
        if x < 810:
            on_board += 1
    chessboard.set_position_to_packed()
    output += "<h3>position: {}</h3>\n".format(chessboard.position)
    chboard = str(chessboard.chessboard)
    chboard = chboard.replace("],", "],<br>\n")
    chboard = "<p>" + chboard + "</p>\n"
    output += chboard
    chessboard.output = output
    chessboard.figures_count = figures_count
    chessboard.on_board = on_board
    # chessboard.figures = figures
    chessboard.beside_figures = beside_figures
    #doc["output"].html = output
    #alert("figures count total: {} \n on board: {}".format(figures_count, on_board))
    #browser.window.open("http://vysoky.pythonanywhere.com/chessboard/" + chessboard.position, "_self")
    doc.ch_board = chessboard
    doc.ch_move_validation = True
    doc.ch_last_color = ""
    doc.ch_kb_moves = [['d4', 'f5'], ['e4', 'fxe4'], ['Nc3', 'Nf6'], ['Bg5', 'c6'], ['f3', 'e3'], ['Bxe3', 'd5'], ['Bd3', 'g6'], ['Qd2', 'Nbd7'], ['O-O-O', 'b5'], ['Bh6', 'Nb6'], ['Nge2', 'b4'], ['Nb1', 'a5'], ['b3', 'Qd6'], ['Bf4', 'Qe6'], ['Rde1', 'Qf7'], ['Ng3', 'Bg7'], ['Bh6', 'O-O'], ['Bxg7', 'Qxg7'], ['h4', 'c5'], ['dxc5', 'Nbd7'], ['Qe3', 'e5'], ['c6', 'a4'], ['cxd7', 'Nxd7'], ['h5', 'axb3'], ['axb3', 'Ra2'], ['hxg6', 'e4'], ['fxe4', 'Ba6'], ['exd5', 'Nc5'], ['gxh7+', 'Kh8'], ['Bg6', 'Qb2+'], ['Kd1', 'Ra1'], ['Qxc5', 'Rxb1+'], ['Kd2', 'Rf2+'], ['Re2', 'Rxh1'], ['Qxb4', '0-1']]
    return chessboard

def accept_moves():
    for figure in doc.get(selector=".chess-figure"):
        m = figure.getAttribute("transform")
        m = m.split("(")[1].split(")")[0].split()
        x = int(figure.getAttribute("x")) + int(m[4])
        y = int(figure.getAttribute("y")) + int(m[5])
        m[4] = "0"
        m[5] = "0"
        figure.setAttribute("x", str(x))
        figure.setAttribute("y", str(y))
        figure.setAttribute("transform", "matrix(" + " ".join(m) + ")")

def reset_moves():
    for figure in doc.get(selector=".chess-figure"):
        m = figure.getAttribute("transform")
        m = m.split("(")[1].split(")")[0].split()
        m[4] = "0"
        m[5] = "0"
        figure.setAttribute("transform", "matrix(" + " ".join(m) + ")")
        get_chessboard()

def add_figures(chessboard):
    # chessboard - matrix of figures shortcuts
    if not doc.ch_board:
        get_chessboard()
    source = doc.ch_board.beside_figures
    for row in range(len(chessboard)):
        for col in range(len(chessboard[row])):
            shortcut = chessboard[row][col].strip()
            if shortcut:
                #add_figure(chessboard[row][col], row, col)
                figure_img = source[chessboard[row][col]]
                clone = figure_img.cloneNode()
                x = col * 100 + int(clone.getAttribute("x")) % 100
                y = row * 100 + int(clone.getAttribute("y")) % 100
                clone.setAttribute("x", str(x))
                clone.setAttribute("y", str(y))
                figure_img.insertAdjacentElement('beforebegin', clone)
                clone.bind("mousedown", select_element)
                doc.querySelector('.figures').insertAdjacentElement('beforeend',clone)
                figure = ChessFigure(shortcut, clone, row, col)
                doc.ch_board.figures[row][col].append(figure)


