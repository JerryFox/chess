from browser import timer, document as doc
from random import choice, randint
from labels import remove_labels, show_labels, add_label

CIRCLE_KNIGHT_WALK = [
    [15, 12, 37, 34, 17, 2, 39, 0],
    [36, 33, 16, 13, 38, 63, 18, 3],
    [11, 14, 35, 52, 55, 58, 1, 40],
    [32, 53, 60, 57, 62, 49, 4, 19],
    [25, 10, 51, 54, 59, 56, 41, 48],
    [28, 31, 26, 61, 50, 45, 20, 5],
    [9, 24, 29, 44, 7, 22, 47, 42],
    [30, 27, 8, 23, 46, 43, 6, 21]
    ]

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

def start(time=3000):
    doc.ch_g = gen_figures()
    doc.ch_time = time
    gen()

def pause():
    timer.clear_timeout(doc.ch_idtimer)

def cont():
    gen()

def step(n=1):
    for i in range(n):
        next(doc.ch_g)

def go(evt=None):
    remove_labels()
    show_labels()
    # select figure under selector (graphical cursor)
    row = int(doc["selector"].getAttribute("y")) // 100
    col = int(doc["selector"].getAttribute("x")) // 100
    figure = None
    if doc.ch_board.figures[row][col]:
        figure = doc.ch_board.figures[row][col][-1]
        figure.counter = 0
        add_label(row, col, str(figure.counter).zfill(2))
        figure.timer_interval = 1000
        figure.knight_logic = globals()[doc["import-module"].value]
        figure.go()
    #print(row, col, shortcut)
    return figure

def run():
    f = doc.ch_board.add_figure("n")
    f.timer_interval = 2000
    f.go()

def knight_walk0(self, valid_moves):
    move = choice(valid_moves)
    # remove other figure
    if self.chessboard.figures[move[0]][move[1]]:
        self.chessboard.remove_figure(move[0], move[1])
    self.chessboard.add_figure("p" if self.shortcut.islower() else "P", self.row, self.col)
    self.move_to(move[0], move[1])
    self.counter += 1
    add_label(move[0], move[1], str(self.counter).zfill(2))
    self.idtimer = timer.set_timeout(self.go, self.timer_interval)

def knight_walk1(self, valid_moves):
    # minimise distance from borders
    #print(valid_moves)
    moves_dists = []
    for (index, move) in enumerate(valid_moves):
        dists = [move[0], move[1], 7 - move[0], 7 - move[1]]
        dists.sort()
        moves_dists.append([dists, index])
    moves_dists.sort()
    #print(moves_dists)
    #print()
    move = valid_moves[moves_dists[0][1]]
    # remove other figure
    if self.chessboard.figures[move[0]][move[1]]:
        self.chessboard.remove_figure(move[0], move[1])
    self.chessboard.add_figure("p" if self.shortcut.islower() else "P", self.row, self.col)
    self.move_to(move[0], move[1])
    self.counter += 1
    add_label(move[0], move[1], str(self.counter).zfill(2))
    self.idtimer = timer.set_timeout(self.go, self.timer_interval)

def test():
    pass

def add_fig():
    fig = "p"
    doc.ch_time = 2000
    where = randint(0, 63)
    doc.ch_board.add_figure(fig, where // 8, where % 8)
    doc.ch_idtimer = timer.set_timeout(add_fig, doc.ch_time)


doc["but-test"].text = "go"
doc["import-module"].value = "knight_walk1"
doc["but-test"].unbind("click")
doc["but-test"].bind("click", go)

