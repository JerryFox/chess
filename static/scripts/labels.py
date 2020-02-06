"""
labels.py
brython script
working with labels in cells
"""

from browser import document as doc

LABEL = """\
    <g id="label_{row}_{col}" transform="matrix(1 0 0 1 {x} {y})">
        <text x="13" y="25">{text}</text>
    </g>"""

def hide_labels():
    doc["labels"].classList.add("hidden")

def show_labels():
    doc["labels"].classList.remove("hidden")

def remove_labels():
    doc["labels"].innerHTML = ""

def add_labels(matrix=None):
    remove_labels()
    if not matrix:
        matrix = [[str(row)+str(col) for col in range(8)]for row in range(8)]
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            html = LABEL.format(row=row, col=col, x=col*100, y=row*100,\
            text=matrix[row][col])
            doc["labels"].innerHTML += html

def remove_label(row, col):
    label = doc.getElementById("label_" + str(row) + "_" + str(col))
    if label:
        label.remove()

def add_label(row, col, text=""):
    remove_label(row, col)
    html = LABEL.format(row=row, col=col, x=col*100, y=row*100, text=text)
    doc["labels"].innerHTML += html

def get_label(row, col):
    text = None
    label = doc.getElementById("label_" + str(row) + "_" + str(col))
    if label:
        text = label.getElementsByTagName("text")[0].innerHTML
    return text