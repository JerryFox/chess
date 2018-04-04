from browser import timer, document as doc
import random
from walk import knight_walk0, knight_walk1


def gen_figures():
    figures = ["R", "N", "B", "K", "q", "b", "n", "r"]
    for row in range(8):
        for col in range(8):
            doc.ch_board.add_figure(figures[col], row, col)
            yield (row, col)

def gen():
    dest = next(doc.ch_g)
    if dest != (7, 7):
        doc.ch_idtimer = timer.set_timeout(gen, doc.ch_time)

def start(evt=None, time=None):
    if type(time) == int:
        doc.ch_time = time
    doc.ch_board.remove_figures()
    doc.ch_g = gen_figures()
    gen()

def pause():
    timer.clear_timeout(doc.ch_idtimer)

def cont():
    gen()

def step(n=1):
    for i in range(n):
        next(doc.ch_g)

def go(evt=None):
    # select figure under selector (graphical cursor)
    row = int(doc["selector"].getAttribute("y")) // 100
    col = int(doc["selector"].getAttribute("x")) // 100
    figure = None
    if doc.ch_board.figures[row][col]:
        figure = doc.ch_board.figures[row][col][-1]
        figure.timer_interval = 1000
        figure.knight_logic = knight_walk0
        figure.go()
    #print(row, col, shortcut)
    return figure

def run(evt=None):
    exec(doc["import-module"].value)


doc["but-test"].text = "go"
doc["but-test"].unbind("click")
doc["import-module"].value = "start(time=1000)"
doc["but-test"].bind("click", run)

