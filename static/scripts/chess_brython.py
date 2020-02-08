"""
initial brython script
started from html
"""

from browser import document as doc, alert, window
from chess import Chessboard
from http import cookies
from moves import get_chessboard
from select_deselect import select_element, add_target, remove_targets, set_targets_from_moves
from browser.local_storage import storage
import time

from config import INTER_PATH

doc.ch_selected_element = None

def click_on_chessboard(evt):
    x = doc["cursor"].getAttribute("x")
    y = doc["cursor"].getAttribute("y")
    doc.ch_coord = [int(y) // 100, int(x) // 100]
    if evt.shiftKey:
        targets = doc.get(selector="rect.targets")
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
        doc["selector"].setAttribute("x", x)
        doc["selector"].setAttribute("y", y)
        doc.ch_selector = [int(y) // 100, int(x) // 100]

def move_over_chessboard(evt):
    doc["coordinates"].text = "x:{} y:{}".format(evt.x, evt.y)
    bound_rect = doc["chessboard"].getBoundingClientRect()
    zoom_chessboard = 1007 / bound_rect.width
    doc.ch_zoom_chessboard = zoom_chessboard
    x0 = bound_rect.left + window.scrollX
    y0 = bound_rect.top + window.scrollY
    row = min(int((evt.y - 5 - y0) * zoom_chessboard / 100), 7)
    col = min(int((evt.x - 5 - x0) * zoom_chessboard / 100), 9)
    doc["chessboard-coordinates"].text = "row:{} col:{}".format(row, col)
    doc["cursor"].setAttribute("x", str(col * 100))
    doc["cursor"].setAttribute("y", str(row * 100))
    doc.coord = [row, col]
    # move selected figure
    sel_figure = doc.ch_selected_element
    if sel_figure:
        dx = (evt.clientX - doc.ch_current_x) * doc.ch_zoom_chessboard
        dy = (evt.clientY - doc.ch_current_y) * doc.ch_zoom_chessboard
        cm = list(doc.ch_current_matrix)
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
    doc["output"].html = output
    alert("figures count total: {} \n on board: {}".format(figures_count, on_board))
    #browser.window.open("http://vysoky.pythonanywhere.com/chessboard/" + chessboard.position, "_self")
    return chessboard.position

def go_to_position(event):
    chessboard = Chessboard("blank")
    for figure in doc.get(selector=".chess-figure"):
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
        c = doc.get(selector=".chessboard")[0]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
            doc.cookie = "chess_board=visible; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"
        else:
            c.classList.add("hidden")
            doc.cookie = "chess_board=hidden; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def console_hide_show(event):
    try:
        c = doc["console"]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
            doc.cookie = "chess_console=visible; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"
        else:
            c.classList.add("hidden")
            doc.cookie = "chess_console=hidden; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def zoom_out(event):
    # chessboard svg zoom out
    svg = doc.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "px" in width:
        zoom = int(width.split("px")[0])
        zoom = int((int(zoom/50) - 1) * 50)
        zoom = str(zoom) + "px"
        svg.setAttribute("width", zoom)
        doc["zoom-display"].text = zoom
        doc.cookie = "chess_zoom=" + zoom + "; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"


def zoom_in(event):
    # chessboard svg zoom in
    svg = doc.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "px" in width:
        zoom = int(width.split("px")[0])
        zoom = int((int(zoom/50) + 1) * 50)
        zoom = str(zoom) + "px"
        svg.setAttribute("width", zoom)
        doc["zoom-display"].text = zoom
        doc.cookie = "chess_zoom=" + zoom + "; expires=" + cookies._getdate(60 * 60 * 24 * 365) + "; path=/;"

def import_module(evt=None):
    module = __import__(doc["import-module"].value)

def open_storage(evt=None):
    storage_name = doc["open-select"].value
    doc["editor"].reset_src(storage_name)
    doc["storage-name"].value = storage_name

def save_to_storage(evt=None):
    storage_name = doc["storage-name"].value
    editor = window.ace.edit("editor")
    if not storage_name in storage:
        doc["open-select"].innerHTML += '<option value="{}">{}</option>\n'\
            .format(storage_name, storage_name)
        doc["storage-names"].innerHTML += '<option value="{}"></option>\n'\
            .format(storage_name)
    storage[storage_name] = editor.getValue()
    doc["editor"].storage_name = storage_name
    doc["storage-name"].value = storage_name

def load_file(evt=None):
    editor = window.ace.edit("editor")
    fake_qs = '?foo=%s' %time.time()
    content = open(doc["code-url"].value + fake_qs).read()
    editor.setValue(content)


doc["but-go-to-position"].bind("click", go_to_position)
doc["but-fig-count"].bind("click", figures_counting)
doc["but-chessboard-hide-show"].bind("click", chessboard_hide_show)
doc["but-console-hide-show"].bind("click", console_hide_show)
doc["but-zoom-out"].bind("click", zoom_out)
doc["but-zoom-in"].bind("click", zoom_in)
doc["but-test"].bind("click", import_module)

doc["open"].bind("click", open_storage)
doc["save-to"].bind("click", save_to_storage)
doc["load-from"].bind("click", load_file)

width = doc.get(selector="svg.chessboard")[0].getAttribute("width")
doc["zoom-display"].text = width
# get chess figures, setup mousedown event
figures = doc.get(selector=".chess-figure")
for f in figures:
    f.bind("mousedown", select_element)
#doc.get(selector="body")[0].bind("mousemove", move_over_chessboard)
doc["chessboard"].bind("mousemove", move_over_chessboard)
doc["chessboard"].bind("mousedown", click_on_chessboard)

c = doc.cookie
if c:
    s = {j.split("=")[0]:j.split("=")[1] for j in c.split("; ")}
else:
    s = {}

if "chess_board" in s.keys() and s["chess_board"] == "hidden":
    c = doc.get(selector=".chessboard")[0]
    c.classList.add("hidden")
if "chess_console" in s.keys() and s["chess_console"] == "hidden":
    try:
        c = doc["console"]
    except:
        pass
    else:
        c.classList.add("hidden")

# files in local storage:

doc["open-select"].innerHTML = ""
doc["storage-names"].innerHTML = ""
storage_names = []
for i in storage:
    if i[0] != "_":
        storage_names.append(i)
        doc["open-select"].innerHTML += '<option value="{}">{}</option>\n'.format(i, i)
        doc["storage-names"].innerHTML += '<option value="{}"></option>\n'.format(i)
if "py_src" in storage_names or not storage_names:
    doc["storage-name"].value = "py_src"
    doc["open-select"].value = "py_src"
else:
    doc["storage-name"].value = storage_names[0]
    doc["open-select"].value = storage_names[0]


doc.ch_board = get_chessboard()

