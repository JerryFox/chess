from browser import document, window

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
    document.ch_zoom_chessboard = zoom_chessboard
    x0 = bound_rect.left + window.scrollX
    y0 = bound_rect.top + window.scrollY
    row = min(int((evt.y - 5 - y0) * zoom_chessboard / 100), 7)
    col = min(int((evt.x - 5 - x0) * zoom_chessboard / 100), 9)
    document["chessboard-coordinates"].text = "row:{} col:{}".format(row, col)
    document["cursor"].setAttribute("x", str(col * 100))
    document["cursor"].setAttribute("y", str(row * 100))
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

def select_element(evt):
    evt.preventDefault()
    selected_element = evt.target
    me = document.getElementById("moving")
    if me:
        me.removeAttribute("id")
    selected_element.setAttribute("id", "moving")
    # current matrix
    cm = selected_element.getAttribute("transform").split("(")[1].split(")")[0].split()
    cm = [float(i) for i in cm]
    # clone figure outside chessboard
    x = int(selected_element.getAttribute("x"))
    x += cm[4]
    if x > 810:
        clone = selected_element.cloneNode()
        clone.removeAttribute("id")
        selected_element.insertAdjacentElement('beforebegin', clone)
        clone.bind("mousedown", select_element)
    # move selected figure on top
    document.querySelector('.figures').insertAdjacentElement('beforeend',selected_element)
    # save variables to document
    document.ch_current_x = evt.clientX
    document.ch_current_y = evt.clientY
    document.ch_selected_element = selected_element
    document.ch_current_matrix = cm
    # document.ch_zoom_chessboard = zoom_chessboard
    # events binding
    # selected_element.bind("mousemove", move_element)
    # selected_element.bind("mouseout", deselect_element);
    selected_element.bind("mouseup", deselect_element)

def deselect_element(evt):
    if document.ch_selected_element:
        sel_elem = document.ch_selected_element
        sel_elem.classList.remove("source")
        cm = sel_elem.getAttribute("transform").split("(")[1].split(")")[0].split()
        cm = [int(float(i)) for i in cm]
        #cm = document.ch_current_matrix
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

