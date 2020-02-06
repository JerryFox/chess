"""
move_figures.py
brython training script
"""

from browser import document as doc, timer

b = doc.ch_board

def go_board(self):
    """
    moving all figures to the right
    """
    figures = []
    for row in self.figures:
        for col in row:
            for fig in col:
                figures.append(fig)
    rest = False
    for fig in figures:
        if fig.col == 7:
            fig.remove()
        else:
            fig.move_to(fig.row, fig.col + 1)
            rest = True
    if rest:
        self.timer_interval = 1000
        self.idtimer = timer.set_timeout(self.go, self.timer_interval)

def shift_images(self):
    """
    shifting images out of screen
    """
    figures = []
    for row in self.figures:
        for col in row:
            for fig in col:
                figures.append(fig)
    dshiftx = 20
    dshifty = -10
    self.shift[0] += dshiftx
    self.shift[1] += dshifty
    for fig in figures:
        x = int(fig.svg_image.getAttribute("x"))
        fig.svg_image.setAttribute("x", str(x + dshiftx))
        y = int(fig.svg_image.getAttribute("y"))
        fig.svg_image.setAttribute("y", str(y + dshifty))
    if self.shift[0] < 1000:
        self.timer_interval = 10
        self.idtimer = timer.set_timeout(self.sh, self.timer_interval)

def reshift_images(self):
    """
    readjusting images after shifting
    """
    figures = []
    for row in self.figures:
        for col in row:
            for fig in col:
                figures.append(fig)
    for fig in figures:
        x = int(fig.svg_image.getAttribute("x"))
        y = int(fig.svg_image.getAttribute("y"))
        fig.svg_image.setAttribute("x", str(x - self.shift[0]))
        fig.svg_image.setAttribute("y", str(y - self.shift[1]))
    self.shift[0] = 0
    self.shift[1] = 0

def bind(instance, method):
    """
    function for method binding to an instance
    """
    def binding_scope_fn(*args, **kwargs):
        return method(instance, *args, **kwargs)
    return binding_scope_fn

# add methods to chessboard
b.go = bind(b, go_board)
#b.go()
b.shift = [0, 0]
b.sh = bind(b, shift_images)
b.resh = bind(b, reshift_images)



