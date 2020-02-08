"""
bx_playback.py
Brython eXercice script
moves playback
control buttons

using:
run this script (from UI or a console) and use the buttons
"""

from browser import timer, document as doc
#from random import choice, randint
#from labels import remove_labels, show_labels, add_label
from select_deselect import move

moves = [[[6, 3], [4, 3]], [[1, 5], [3, 5]], [[6, 4], [4, 4]], [[3, 5], [4, 4], 'x'],
    [[7, 1], [5, 2]], [[0, 6], [2, 5]], [[7, 2], [3, 6]], [[1, 2], [2, 2]], [[6, 5],
    [5, 5]], [[4, 4], [5, 4]], [[3, 6], [5, 4], 'x'], [[1, 3], [3, 3]], [[7, 5],
    [5, 3]], [[1, 6], [2, 6]], [[7, 3], [6, 3]], [[0, 1], [1, 3]], [[7, 4], [7, 2]],
    [[1, 1], [3, 1]], [[5, 4], [2, 7]], [[1, 3], [2, 1]], [[7, 6], [6, 4]], [[3, 1],
    [4, 1]], [[5, 2], [7, 1]], [[1, 0], [3, 0]], [[6, 1], [5, 1]], [[0, 3], [2, 3]],
    [[2, 7], [4, 5]], [[2, 3], [2, 4]], [[7, 3], [7, 4]], [[2, 4], [1, 5]], [[6, 4],
    [5, 6]], [[0, 5], [1, 6]], [[4, 5], [2, 7]], [[0, 4], [0, 6]], [[2, 7], [1, 6], 'x'],
    [[1, 5], [1, 6], 'x'], [[6, 7], [4, 7]], [[2, 2], [3, 2]], [[4, 3], [3, 2], 'x'],
    [[2, 1], [1, 3]], [[6, 3], [5, 4]], [[1, 4], [3, 4]], [[3, 2], [2, 2]], [[3, 0],
    [4, 0]], [[2, 2], [1, 3], 'x'], [[2, 5], [1, 3], 'x'], [[4, 7], [3, 7]], [[4, 0],
    [5, 1], 'x'], [[6, 0], [5, 1], 'x'], [[0, 0], [6, 0]], [[3, 7], [2, 6], 'x'],
    [[3, 4], [4, 4]], [[5, 5], [4, 4], 'x'], [[0, 2], [2, 0]], [[4, 4], [3, 3], 'x'],
    [[1, 3], [3, 2]], [[2, 6], [1, 7], 'x'], [[0, 6], [0, 7]], [[5, 3], [2, 6]], [[1, 6],
    [6, 1]], [[7, 2], [7, 3]], [[6, 0], [7, 0]], [[5, 4], [3, 2], 'x'], [[7, 0],
    [7, 1], 'x'], [[7, 3], [6, 3]], [[0, 5], [6, 5]], [[7, 4], [6, 4]], [[7, 1],
    [7, 7], 'x'], [[3, 2], [4, 1], 'x']]

def play(moves, move_idx_from=0, number_of_moves=None):
    """ replay number of moves """
    if move_idx_from >= len(moves):
        return None
    if number_of_moves is None:
        number_of_moves = len(moves) - move_idx_from
    for index, m in enumerate(moves[move_idx_from : move_idx_from + number_of_moves]):
        move(m)
    return index + move_idx_from + 1

def back():
    """ back for one move """
    ch = doc.ch_board
    if ch.play_mode == "play":
        ch.rec_moves = [list(item) for item in ch.moves]
        ch.play_mode = "replay"
    if ch.moves:
        last_move = ch.moves[-1]
        (l_sour, l_dest) = last_move[:2]
        dr, dc = l_dest
        sr, sc = l_sour
        fig = ch.figures[dr][dc][-1]
        shortcut = ch.chessboard[dr][dc]
        fig.move_to(sr, sc)
        ch.chessboard[sr][sc] = shortcut
        ch.chessboard[dr][dc] = ""
        if len(last_move) > 2 and "x" in last_move[2]:
            deleted = ch.trash[-1]
            if [dr, dc] == deleted[1]:
                ch.chessboard[dr][dc] = deleted[0]
                ch.add_figure(deleted[0], dr, dc)
            else:
                print("something is wrong")
            ch.trash = ch.trash[:-1]
            ch.figures_trash = ch.figures_trash[:-1]
        if shortcut.upper() == "K" and abs(sc - dc) == 2:
            # castling
            if dc == 6:
                rook = ch.figures[dr][dc - 1][-1]
                ch.chessboard[dr][dc - 1] = ""
                rook.move_to(dr, 7)
                ch.chessboard[dr][7] = rook.shortcut
            else:
                rook = ch.figures[dr][dc + 1][-1]
                ch.chessboard[dr][dc + 1] = ""
                rook.move_to(dr, 0)
                ch.chessboard[dr][0] = rook.shortcut
        ch.last_color = "w" if ch.last_color == "b" else "b"
        ch.moves = ch.moves[:-1]
    return len(ch.moves)




def go(evt=None):
    ch = doc.ch_board
    if ch.move_counter < len(ch.rec_moves) and ch.play_mode == "replay":
        ch.move_counter = play(ch.rec_moves, ch.move_counter, 1)
        ch.idtimer = timer.set_timeout(go, ch.timer_interval)

def go_back(evt=None):
    ch = doc.ch_board
    if ch.move_counter > 0:
        ch.move_counter = back()
        ch.idtimer = timer.set_timeout(go_back, ch.timer_interval)

def stop(evt=None):
    ch = doc.ch_board
    timer.clear_timeout(ch.idtimer)
    ch.idtimer = None

def go_end(evt=None):
    ch = doc.ch_board
    while ch.move_counter < len(ch.rec_moves) and ch.play_mode == "replay":
        ch.move_counter = play(ch.rec_moves, ch.move_counter, 1)

def go_step(evt=None):
    ch = doc.ch_board
    if ch.move_counter < len(ch.rec_moves) and ch.play_mode == "replay":
        ch.move_counter = play(ch.rec_moves, ch.move_counter, 1)

def go_back_end(evt=None):
    ch = doc.ch_board
    while ch.move_counter > 0:
        ch.move_counter = back()

def go_back_step(evt=None):
    ch = doc.ch_board
    ch.move_counter = back()

if doc.getElementById("but-test"):
    bgo = doc["but-test"]
    parent = bgo.parentNode
    br = bgo.nextSibling
    parent.removeChild(bgo)
    parent.removeChild(doc.getElementById("import-module"))
    s = doc.createElement("span")
    s.innerHTML = "&nbsp;&nbsp;&nbsp;"
    parent.insertBefore(s, br)

    buttons = [
        {"id": "but-back-end", "text": "🢤🢤🢤", "func": go_back_end},
        {"id": "but-back-step", "text": "🢤🢤", "func": go_back_step},
        {"id": "but-play-back", "text": "◀", "func": go_back},
        {"id": "but-stop", "text": "⏹️", "func": stop},
        {"id": "but-play-fwd", "text": "▶", "func": go},
        {"id": "but-go-step", "text": "🢧🢧", "func": go_step},
        {"id": "but-go-end", "text": "🢧🢧🢧", "func": go_end},
        ]

    for b in buttons:
        if not doc.getElementById(b["id"]):
            but = bgo.cloneNode(True)
            but.text = b["text"]
            but.setAttribute("id", b["id"])
            but.bind("click", b["func"])
            parent.insertBefore(but, br)
            t = doc.createTextNode(" ")
            parent.insertBefore(t, br)

def init():
    ch = doc.ch_board
    ch.position = "base"
    ch.chessboard = ch.get_chessboard()
    ch.refresh_figures()
    ch.last_color = ""
    ch.trash = []
    ch.figures_trash = []
    ch.moves = []
    ch.play_mode = "replay"

    ch.move_counter = 0
    ch.idtimer = None
    ch.rec_moves = moves
    ch.timer_interval = 1000

init()
ch = doc.ch_board

