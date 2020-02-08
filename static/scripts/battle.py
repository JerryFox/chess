from walk import *
import random


def add_pawn():
    r = random.randint(0, 63)
    doc.ch_board.add_figure("p", r // 8, r % 8)
    doc.ch_pawn_timer = timer.set_timeout(add_pawn, doc.ch_pawn_time)

def count_of_enemies(fig="N"):
    isup = fig.isupper()
    count = 0
    for row in doc.ch_board.figures:
        for col in row:
            for f in col:
                if isup != f.shortcut.isupper():
                    count += 1
    return count

def manager():
    count = count_of_enemies()
    if "\\" in doc["output"].innerHTML:
        prefix = "/"
    else:
        prefix = "\\"
    doc["output"].innerHTML = "<strong>{} count of enemies: {}</strong>".format(prefix, count)
    if count > 10:
        for n in knights:
            if not n.idtimer:
                n.go()
    elif count == 0:
        for n in knights:
            n.stop()
    doc.ch_manag_timer = timer.set_timeout(manager, 200)

doc.ch_pawn_time = 1000
board = doc.ch_board
knights = []

try:
    n1.stop()
except:
    board.remove_figures()
    n1 = board.add_figure("N", 0, 0)
knights.append(n1)

try:
    n2.stop()
except:
    n2 = board.add_figure("N", 0, 1)
knights.append(n2)

try:
    n3.stop()
except:
    n3 = board.add_figure("N", 0, 2)
knights.append(n3)

for n in knights:
    n.timer_interval = 700
    n.go()
