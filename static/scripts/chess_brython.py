"""
initial brython script
started from html
"""

from browser import document, alert, window
from chess import Chessboard
from http import cookies
from moves import get_chessboard
from select_deselect import select_element, add_target, remove_targets, set_targets_from_moves
from browser.local_storage import storage
import time

from config import INTER_PATH

document.ch_selected_element = None

def click_on_chessboard(evt):
    x = document["cursor"].getAttribute("x")
    y = document["cursor"].getAttribute("y")
    document.ch_coord = [int(y) // 100, int(x) // 100]
    if evt.shiftKey:
        targets = document.get(selector="rect.targets")
        remove = False
        for t in targets:
            if t.getAttribute("x") == x and t.getAttribute("y") == y:
                t.remove()
                remove = True
                break
        if not remove:
            # add new target
            add_target(x, y)
    else:
        document["selector"].setAttribute("x", x)
        document["selector"].setAttribute("y", y)
        document.ch_selector = [int(y) // 100, int(x) // 100]

def move_over_chessboard(evt):
    document["coordinates"].text = "x:{} y:{}".format(evt.x, evt.y)
    bound_rect = document["chessboard"].getBoundingClientRect()
    zoom_chessboard = 1007 / bound_rect.width
    document.ch_zoom_chessboard = zoom_chessboard
    x0 = bound_rect.left + window.scrollX
    y0 = bound_rect.top + window.scrollY
    row = min(int((evt.y - 5 - y0) * zoom_chessboard / 100), 7)
    col = min(int((evt.x - 5 - x0) * zoom_chessboard / 100), 9)
    document["chessboard-coordinates"].text = "row:{} col:{}".format(row, col)
    document["cursor"].setAttribute("x", str(col * 100))
    document["cursor"].setAttribute("y", str(row * 100))
    document.coord = [row, col]
    # move selected figure
    sel_figure = document.ch_selected_element
    if sel_figure:
        dx = (evt.clientX - document.ch_current_x) * document.ch_zoom_chessboard
        dy = (evt.clientY - document.ch_current_y) * document.ch_zoom_chessboard
        cm = list(document.ch_current_matrix)
        cm[4] += dx
        cm[5] += dy
        m = [str(i) for i in cm]
        #alert(str(m))
        sel_figure.setAttribute("transform", "matrix ({})".format(" ".join(m)))


def figures_counting(event):
    figures_count = 0
    on_board = 0
    chessboard = Chessboard("blank")
    output = ""
    for figure in document.get(selector=".chess-figure"):
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
            chessboard.chessboard[row][column] = figure_shortcut
        output += "x:{} y:{} row: {} col: {}".format(x, y, row, column) + "<br>\n"
        if x < 810:
            on_board += 1
    chessboard.set_position_to_packed()
    output += "<h3>position: {}</h3>\n".format(chessboard.position)
    chboard = str(chessboard.chessboard)
    chboard = chboard.replace("],", "],<br>\n")
    chboard = "<p>" + chboard + "</p>\n"
    output += chboard
    document["output"].html = output
    alert("figures count total: {} \n on board: {}".format(figures_count, on_board))
    #browser.window.open("http://vysoky.pythonanywhere.com/chessboard/" + chessboard.position, "_self")
    return chessboard.position

def go_to_position(event):
    chessboard = Chessboard("blank")
    for figure in document.get(selector=".chess-figure"):
        figure_file = figure.getAttribute("xlink:href")
        figure_shortcut = figure_file.split("_")[1][:2]
        figure_shortcut = figure_shortcut[0] if figure_shortcut[1] == "d" else figure_shortcut[0].upper()
        m = figure.getAttribute("transform")
        m = m.split("(")[1].split(")")[0].split()
        x = int(figure.getAttribute("x")) + float(m[4])
        y = int(figure.getAttribute("y")) + float(m[5])
        column = int(x / 100)
        row = int(y / 100)
        if column < 8 and row < 8:
            chessboard.chessboard[row][column] = figure_shortcut
    chessboard.set_position_to_packed()
    window.open(INTER_PATH + "/chessboard/" + chessboard.position, "_self")
    return chessboard.position

def chessboard_hide_show(event):
    try:
        c = document.get(selector=".chessboard")[0]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
            document.cookie = "chess_board=visible; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"
        else:
            c.classList.add("hidden")
            document.cookie = "chess_board=hidden; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def console_hide_show(event):
    try:
        c = document["console"]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
            document.cookie = "chess_console=visible; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"
        else:
            c.classList.add("hidden")
            document.cookie = "chess_console=hidden; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def zoom_out(event):
    # chessboard svg zoom out
    svg = document.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "px" in width:
        zoom = int(width.split("px")[0])
        zoom = int((int(zoom/50) - 1) * 50)
        zoom = str(zoom) + "px"
        svg.setAttribute("width", zoom)
        document["zoom-display"].text = zoom
        document.cookie = "chess_zoom=" + zoom + "; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"


def zoom_in(event):
    # chessboard svg zoom in
    svg = document.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "px" in width:
        zoom = int(width.split("px")[0])
        zoom = int((int(zoom/50) + 1) * 50)
        zoom = str(zoom) + "px"
        svg.setAttribute("width", zoom)
        document["zoom-display"].text = zoom
        document.cookie = "chess_zoom=" + zoom + "; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def import_module(evt=None):
    module = __import__(document["import-module"].value)

def open_storage(evt=None):
    storage_name = document["open-select"].value
    document["editor"].reset_src(storage_name)
    document["storage-name"].value = storage_name

def save_to_storage(evt=None):
    storage_name = document["storage-name"].value
    editor = window.ace.edit("editor")
    if not storage_name in storage:
        document["open-select"].innerHTML += '<option value="{}">{}</option>\n'\
            .format(storage_name, storage_name)
        document["storage-names"].innerHTML += '<option value="{}"></option>\n'\
            .format(storage_name)
    storage[storage_name] = editor.getValue()
    document["editor"].storage_name = storage_name
    document["storage-name"].value = storage_name

def load_file(evt=None):
    editor = window.ace.edit("editor")
    fake_qs = '?foo=%s' %time.time()
    content = open(document["code-url"].value + fake_qs).read()
    editor.setValue(content)


document["but-go-to-position"].bind("click", go_to_position)
document["but-fig-count"].bind("click", figures_counting)
document["but-chessboard-hide-show"].bind("click", chessboard_hide_show)
document["but-console-hide-show"].bind("click", console_hide_show)
document["but-zoom-out"].bind("click", zoom_out)
document["but-zoom-in"].bind("click", zoom_in)
document["but-test"].bind("click", import_module)

document["open"].bind("click", open_storage)
document["save-to"].bind("click", save_to_storage)
document["load-from"].bind("click", load_file)

width = document.get(selector="svg.chessboard")[0].getAttribute("width")
document["zoom-display"].text = width
# get chess figures, setup mousedown event
figures = document.get(selector=".chess-figure")
for f in figures:
    f.bind("mousedown", select_element)
#document.get(selector="body")[0].bind("mousemove", move_over_chessboard)
document["chessboard"].bind("mousemove", move_over_chessboard)
document["chessboard"].bind("mousedown", click_on_chessboard)

c = document.cookie
if c:
    s = {j.split("=")[0]:j.split("=")[1] for j in c.split("; ")}
else:
    s = {}

if "chess_board" in s.keys() and s["chess_board"] == "hidden":
    c = document.get(selector=".chessboard")[0]
    c.classList.add("hidden")
if "chess_console" in s.keys() and s["chess_console"] == "hidden":
    try:
        c = document["console"]
    except:
        pass
    else:
        c.classList.add("hidden")

# files in local storage:

document["open-select"].innerHTML = ""
document["storage-names"].innerHTML = ""
storage_names = []
for i in storage:
    if i[0] != "_":
        storage_names.append(i)
        document["open-select"].innerHTML += '<option value="{}">{}</option>\n'.format(i, i)
        document["storage-names"].innerHTML += '<option value="{}"></option>\n'.format(i)
if "py_src" in storage_names or not storage_names:
    document["storage-name"].value = "py_src"
    document["open-select"].value = "py_src"
else:
    document["storage-name"].value = storage_names[0]
    document["open-select"].value = storage_names[0]


document.ch_board = get_chessboard()

