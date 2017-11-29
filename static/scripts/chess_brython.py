from browser import document, alert, window
from chess import Chessboard


def click_on_chessboard(evt):
    x = document["cursor"].getAttribute("x")
    y = document["cursor"].getAttribute("y")
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
            #<rect class="targets" fill="none" stroke="#00ff00" stroke-width="2" x="200" y="200" width="92" height="92"
            #    transform="matrix(1 0 0 1 9 9)"/>
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
    else:
        document["selector"].setAttribute("x", x)
        document["selector"].setAttribute("y", y)

def move_over_chessboard(evt):
    document["coordinates"].text = "x:{} y:{}".format(evt.x, evt.y)
    bound_rect = document["chessboard"].getBoundingClientRect()
    zoom_chessboard = 1007 / bound_rect.width
    x0 = bound_rect.x + window.scrollX
    y0 = bound_rect.y + window.scrollY
    row = min(int((evt.y - 5 - y0) * zoom_chessboard / 100), 7)
    col = min(int((evt.x - 5 - x0) * zoom_chessboard / 100), 9)
    document["chessboard-coordinates"].text = "row:{} col:{}".format(row, col)
    document["cursor"].setAttribute("x", str(col * 100))
    document["cursor"].setAttribute("y", str(row * 100))

def select_element(evt):
    selected_element = evt.target
    me = document.getElementById("moving")
    if me:
        me.removeAttribute("id")
    selected_element.setAttribute("id", "moving")
    zoom_chessboard = 100 * (document["chessboard"].getBoundingClientRect().width / 1007)
    #if "%" in chessboard_width:
    #    zoom_chessboard = float(chessboard_width.split("%")[0])
    # current matrix
    cm = selected_element.getAttribute("transform").split("(")[1].split(")")[0].split()
    cm = [int(i) for i in cm]
    # clone figure outside chessboard
    x = int(selected_element.getAttribute("x"))
    x += cm[4]
    if x > 810:
        clone = selected_element.cloneNode()
        selected_element.insertAdjacentElement('beforebegin', clone)
        clone.bind("mousedown", select_element)
    # move selected figure on top
    document.querySelector('.figures').insertAdjacentElement('beforeend',selected_element)
    # save variables to document
    document.ch_current_x = evt.clientX
    document.ch_current_y = evt.clientY
    document.ch_selected_element = selected_element
    document.ch_current_matrix = cm
    document.ch_zoom_chessboard = zoom_chessboard
    # events binding
    selected_element.bind("mousemove", move_element)
    selected_element.bind("mouseout", deselect_element);
    selected_element.bind("mouseup", deselect_element)

def deselect_element(evt):
    if document.ch_selected_element:
        sel_elem = document.ch_selected_element
        cm = document.ch_current_matrix
        cm[4] = 100 * (round(cm[4] / 100))
        cm[5] = 100 * (round(cm[5] / 100))
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

def move_element(evt):
    #alert("x:{} y:{} zoom:{} transform:{}".format(document.ch_current_x, document.ch_current_y, document.ch_zoom_chessboard,
    #    document.ch_current_matrix))
    dx = evt.clientX - document.ch_current_x
    dy = evt.clientY - document.ch_current_y
    cm = document.ch_current_matrix
    if dx or dy:
        dx1 = round(100 * dx / document.ch_zoom_chessboard)
        dy1 = round(100 * dy / document.ch_zoom_chessboard)
        if dx1 or dy1:
            cm[4] += dx1
            cm[5] += dy1
            m = [str(i) for i in cm]
            #alert(str(m))
            document.ch_current_matrix = cm
            document.ch_selected_element.setAttribute("transform", "matrix ({})".format(" ".join(m)))
    document.ch_current_x = evt.clientX
    document.ch_current_y = evt.clientY






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
    output += "<h3>position: {}</h3>".format(chessboard.position)
    document["output"].html = output
    alert("figures count total: {} \n on board: {}".format(figures_count, on_board))
    #browser.window.open("http://vysoky.pythonanywhere.com/chessboard/" + chessboard.position, "_self")
    return chessboard.position

def go_to_position(event):
    import browser
    chessboard = Chessboard("blank")
    for figure in document.get(selector=".chess-figure"):
        figure_file = figure.getAttribute("xlink:href")
        figure_shortcut = figure_file.split("_")[1][:2]
        figure_shortcut = figure_shortcut[0] if figure_shortcut[1] == "d" else figure_shortcut[0].upper()
        m = figure.getAttribute("transform")
        m = m.split("(")[1].split(")")[0].split()
        x = int(figure.getAttribute("x")) + int(m[4])
        y = int(figure.getAttribute("y")) + int(m[5])
        column = int(x / 100)
        row = int(y / 100)
        if column < 8 and row < 8:
            chessboard.chessboard[row][column] = figure_shortcut
    chessboard.set_position_to_packed()
    browser.window.open("http://vysoky.pythonanywhere.com/chessboard/" + chessboard.position, "_self")
    return chessboard.position

def chessboard_hide_show(event):
    try:
        c = document.get(selector=".chessboard")[0]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
        else:
            c.classList.add("hidden")

def console_hide_show(event):
    try:
        c = document["console"]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
        else:
            c.classList.add("hidden")

def zoom_out(event):
    # chessboard svg zoom out
    svg = document.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "%" in width:
        zoom = int(width.split("%")[0])
        zoom = int((int(zoom/5) - 1) * 5)
        zoom = str(zoom) + "%"
        svg.setAttribute("width", zoom)
        document["zoom-display"].text = zoom


def zoom_in(event):
    # chessboard svg zoom in
    svg = document.get(selector="svg.chessboard")[0]
    width = svg.getAttribute("width")
    if "%" in width:
        zoom = int(width.split("%")[0])
        zoom = int((int(zoom/5) + 1) * 5)
        zoom = str(zoom) + "%"
        svg.setAttribute("width", zoom)
        document["zoom-display"].text = zoom



document["but-go-to-position"].bind("click", go_to_position)
document["but-fig-count"].bind("click", figures_counting)
document["but-chessboard-hide-show"].bind("click", chessboard_hide_show)
document["but-console-hide-show"].bind("click", console_hide_show)
document["but-zoom-out"].bind("click", zoom_out)
document["but-zoom-in"].bind("click", zoom_in)

width = document.get(selector="svg.chessboard")[0].getAttribute("width")
document["zoom-display"].text = width
# get chess figures, setup mousedown event
figures = document.get(selector=".chess-figure")
for f in figures:
    f.bind("mousedown", select_element)
document.get(selector="body")[0].bind("mousemove", move_over_chessboard)
document["chessboard"].bind("mousedown", click_on_chessboard)


