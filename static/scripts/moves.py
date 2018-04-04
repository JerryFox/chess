from select_deselect import select_element
from select_deselect import Board, ChessFigure
from browser import document as doc


def get_chessboard():
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
    if not doc.ch_board:
        get_chessboard()
    source = doc.ch_board.beside_figures
    for row in range(len(chessboard)):
        for col in range(len(chessboard[row])):
            if chessboard[row][col].strip():
                #add_figure(chessboard[row][col], row, col)
                figure = source[chessboard[row][col]]
                clone = figure.cloneNode()
                x = col * 100 + int(clone.getAttribute("x")) % 100
                y = row * 100 + int(clone.getAttribute("y")) % 100
                clone.setAttribute("x", str(x))
                clone.setAttribute("y", str(y))
                figure.insertAdjacentElement('beforebegin', clone)
                clone.bind("mousedown", select_element)
                doc.querySelector('.figures').insertAdjacentElement('beforeend',clone)
                doc.ch_board.figures[row][col].append(clone)

