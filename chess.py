# chessboard generation
# html with SVG

CHESS_IMG_FOLDER = "static/images/"
FIGURES = "RNBKQBNRPrnbkqbnrp"
SCRIPT_FOLDER = "static/scripts/"
CSS_FOLDER = "static/css/"

chessboard = [["" for i in range(8)]for j in range(8)]

chessboard[0] = list("RNBKQBNR")
chessboard[1] = list("P" * 8)
chessboard[6] = list("p" * 8)
chessboard[7] = list("rnbkqbnr")

def packed_to_unpacked_position(position="base"):
    if position == "base":
        position = "rnbqkbnr" + "p" * 8 + "-" * 32 + "P" * 8 + "RNBQKBNR"
    elif position == "blank":
        position = ""
    number_of_blanks = 0
    unpacked_position = ""
    for character in position:
        if character.isdigit():
            number_of_blanks = number_of_blanks * 10 + int(character)
            #print(number_of_blanks)
        else:
            unpacked_position += "-" * number_of_blanks
            number_of_blanks = 0
            unpacked_position += character if character in FIGURES else "-"
    # justify to 64 characters
    unpacked_position = (unpacked_position + "-" * 64)[:64]
    return unpacked_position

def get_img_name(shortcut):
    """file name of figure shortcut's image
    shortcuts:
    RNBKQBNRP - dark figures (d)
    rnbkqbnrp - light figures (l)
    image name format example:
    Chess_klt45.svg - white king
    """
    name = "Chess_{}{}t45.svg".format(shortcut.lower(),
                                      "l" if shortcut.isupper() else "d")
    return name

def image_element_code(row, column, shortcut, beside=False):
    image_template = """<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink"
xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); "
width="80" height="80"
class="chess-figure draggable{}"
transform="matrix(1 0 0 1 0 0)"
onmousedown="if (event.preventDefault) event.preventDefault()"
></image>"""
    return image_template.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut), " source" if beside else "")

def beside_figures_images():
    # images beside chessboard (for adding on chessboard)
    add_board = [["k", "q"], ["r", "b"], ["n", "p"], ["", ""], ["", ""],
                 ["K", "Q"], ["R", "B"], ["N", "P"]]
    images = ""
    for row in range(len(add_board)):
        for column in range(len(add_board[0])):
            if add_board[row][column]:
                images += image_element_code(row, column + 8, add_board[row][column], True) + "\n"
    return images

def svg_element_code(chessboard, zoom="600px"):
    svg_template = """<svg id="chessboard" class="chessboard" viewBox="0 0 1007 810"
version="1.1" width=\""""
    svg_template += zoom + """\" xmlns="http://www.w3.org/2000/svg"
style="overflow: hidden; position: relative;">
<style>
    .draggable {{
        cursor: move;
    }}

    #labels text {{
        font-weight: bold;
        fill: black;
        stroke-width: 0;
        font-size: 16px;
        font-family: serif;
        //text-anchor: middle;
        //xml:space: preserve;
        stroke: black;
    }}
</style>
<!--
chessboard position string:
{position}
{packed_position}
-->
<image x="0" y="0" width="810" height="810" preserveAspectRatio="xMinYMin" \
    xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{img_folder}Chess_Board_01.svg"
    style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);">
</image>
<g id="labels" class="hidden">
    <g id="label_0_0" transform="matrix(1 0 0 1 0 0)">
        <text x="13" y="25">00</text>
    </g>
    <g id="label_0_1" transform="matrix(1 0 0 1 100 0)">
        <text x="13" y="25">01</text>
    </g>
</g>
<g class="cursors">
    <rect id="selector" fill="none" stroke="darkred" stroke-width="6" x="-200" y="-200" width="94" height="94"
        transform="matrix(1 0 0 1 8 8)"/>
    <rect id="cursor" fill="none" stroke="lightgrey" stroke-width="5" x="0" y="0" width="100" height="100"
        transform="matrix(1 0 0 1 5 5)"/>
</g>
<g class="figures">
{images}
{beside_figures}
</g>
</svg>
"""
    position = ""
    images = ""
    for row in range(len(chessboard)):
        for column in range(len(chessboard[0])):
            if chessboard[row][column]:
                images += image_element_code(row, column, chessboard[row][column]) + "\n"
                position += chessboard[row][column]
            else:
                position += "-"
    ch = Chessboard(position)
    pp = ch.get_packed_position()
    beside_figures = beside_figures_images()
    return svg_template.format(position=position, packed_position=pp,
            img_folder=CHESS_IMG_FOLDER, images=images, beside_figures=beside_figures)

def html_source_code(insert_html):
    html_template = """<!DOCTYPE html>
<html>
	<head>
		<title>chessboard</title>
		<meta charset=utf-8">
		<link rel="stylesheet" type="text/css" href="{css_folder}chess.css">
        <script src="{script_folder}brython.js"></script>
        <script src="{script_folder}brython_stdlib.js"></script>

        <!--Brython - editor - HEAD -->
        <link rel="stylesheet" type="text/css"
              href="https://fonts.googleapis.com/css?family=Roboto">
        <link rel="stylesheet" href="{css_folder}editor.css">

        <script src="{script_folder}ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="{script_folder}ace/ext-language_tools.js" type="text/javascript" charset="uteditorf-8"></script>
        <script src="{script_folder}ace/mode-python3.js" type="text/javascript" charset="utf-8"></script>
        <script src="{script_folder}ace/snippets/python.js" type="text/javascript" charset="utf-8"></script>

<script type="text/python3" id="tests_editor">
from browser import document as doc
import editor

def editor_hide_show(event):
    try:
        c = doc["container"]
    except:
        pass
    else:
        if "hidden" in c.getAttribute("class"):
            c.classList.remove("hidden")
        else:
            c.classList.add("hidden")

# bindings
doc['run'].bind('click',editor.run)
#doc["editor-button"].bind("click", editor_hide_show)
#doc["console-clr-button"].bind("click", console_clr)

</script>

        <!--/Brython - editor - HEAD -->

        <script type="text/python3" src="{script_folder}chess_brython.py"></script>
 	</head>
    <body onload="brython(1)">
        <div id="chess-outer-container" class="wrapper">
            <div class="gr-header">
                <button id="but-chessboard-hide-show">chess_hi/sh</button>
                <button id="but-console-hide-show">console_hi/sh</button>
                <button id="but-fig-count">count fig.</button>
                <button id="but-go-to-position">goto pos.</button>
                <button id="but-test">test</button>
                <input id="import-module" type="text" name="import-module" value="walk" size="10"><br>
                <button id="but-zoom-out">◀</button>
                <span id="zoom-display"></span>
                <button id="but-zoom-in">▶</button>
                <span id="coordinates"></span>
                <span id="chessboard-coordinates"></span>
            </div>


            <div id="chess-container" class="gr-chessboard">
{insert_html}
            </div>

            <div id="console" class="console gr-console">
                <!-- Brython console -->
                <textarea id=code class=codearea rows=20></textarea>
                <div id=content></div>
                <script type="text/python3" src="{script_folder}console.py" id="__main__"></script>
                <!-- /Brython console -->
            </div>

            <div id="output" class="gr-output">
            </div>
        </div>

    	    <div id="container" class="editorarea gr-editor">
    	        <div id="editor-buttons">
        			<button id="run">&nbsp;▶ Run (Save)&nbsp;</button>
        			<button id="save-to">&nbsp;SaveTo&nbsp;</button>
                    <input id="storage-name" list="storage-names" name="storage-name" size="10">
                    <datalist id="storage-names">
                    </datalist>

        			<button id="open">&nbsp;Open&nbsp;</button>
                    <select id="open-select">
                    </select>
                    <button id="load-from">&nbsp;LoadFrom&nbsp;</button>
                    <input id="code-url" type="text" name="code-url"
                        value="http://vysoky.pythonanywhere.com/chessboard/static/walk.py" size="20">
    	        </div>
    		    <div id="editor"></div>
    	    </div>

        <script type="text/python3">
            from browser import window
            window.scrollTo(0, 0)
        </script>

	</body>
</html>
"""
    return html_template.format(script_folder=SCRIPT_FOLDER,
        css_folder=CSS_FOLDER, insert_html=insert_html)

class Chessboard:

    def __init__(self, position="base"):
        self.position = position
        self.chessboard = self.get_chessboard()
        self.moves = []
        self.last_color = None
        self.move_validation = True
        self.trash = []

    def get_chessboard(self):
        position = packed_to_unpacked_position(self.position)
        chessboard = [["" if c == "-" else c
                       for c in position[i * 8 : i * 8 + 8]] for i in range(8)]
        return chessboard


    def get_html(self, zoom="600px"):
        if "px" not in zoom:
            zoom="600px"
        return html_source_code(svg_element_code(self.chessboard, zoom))

    def get_packed_position(self):
        chessboard = self.chessboard
        position = ""
        number_in_string = 0
        pos_pack = ""
        for row in range(len(chessboard)):
            for column in range(len(chessboard[0])):
                if chessboard[row][column]:
                    position += chessboard[row][column]
                    if number_in_string:
                        if number_in_string > 1:
                            pos_pack += str(number_in_string)
                        else:
                            pos_pack += "-"
                    pos_pack += chessboard[row][column]
                    number_in_string = 0
                else:
                    position += "-"
                    number_in_string += 1
        if number_in_string:
            if number_in_string > 1:
                pos_pack += str(number_in_string)
            else:
                pos_pack += "-"
        return pos_pack

    def set_position_to_packed(self):
        self.position = self.get_packed_position()

    def set_chessboard_from_position(self):
        self.chessboard = self.get_chessboard()

    def add_figures(self, figure_positions):
        """add figures on chessboard
        figure_positions: str - <figure_name><coords>
        coords: 00 or a8
        example: "P00P11pg2ph1"
        """
        while len(figure_positions) > 2:
            figure = figure_positions[:3]
            figure_positions = figure_positions[3:]
            if figure[0] in FIGURES:
                if figure[1].isdigit():     # 00 address
                    row = int(figure[1])
                    col = int(figure[2])
                else:                       # a1 address
                    row = 8 - int(figure[2])
                    col = ord(figure[1].upper()) - 65
            self.chessboard[row][col] = figure[0]
        self.set_position_to_packed()

    def remove_figures(self, positions):
        """remove figures from positions
        positions: str - <coords>
        coords: 00 or a8
        example: "0011g2h1"
        """
        while len(positions) > 1:
            pos = positions[:2]
            positions = positions[2:]
            if pos[0].isdigit():    # 00 address
                row = int(pos[0])
                col = int(pos[1])
            else:                   # a1 address
                row = 8 - int(pos[1])
                col = ord(pos[0].upper()) - 65
            self.chessboard[row][col] = ""
        self.set_position_to_packed()
        
    def cell_moves(self, row, col=None):
        if col is None: 
            col = row[1]
            row = row[0]  
        c_moves = [pair[0] for pair in self.moves if pair[0] == [row, col]]
        return bool(c_moves)

    def move(self, src, dst, add=None): 
        color = None
        sour_figure = self.chessboard[src[0]][src[1]]
        dest_figure = self.chessboard[dst[0]][dst[1]]
        if sour_figure and dst in self.get_valid_moves(src[0], src[1]): 
            self.chessboard[src[0]][src[1]] = ""
            self.chessboard[dst[0]][dst[1]] = sour_figure
            self.moves.append([src, dst])
            # castlings - king moving two squares towards a rook
            if sour_figure in "Kk" and abs(src[1] - dst[1]) == 2: 
                # appropriate rook move
                if dst[1] > src[1]: 
                    rook = self.chessboard[src[0]][7]
                    self.chessboard[src[0]][7] = ""
                    self.chessboard[src[0]][5] = rook
                else: 
                    rook = self.chessboard[src[0]][0]
                    self.chessboard[src[0]][0] = ""
                    self.chessboard[src[0]][3] = rook
            self.last_color = "w" if sour_figure.isupper() else "b"
            if dest_figure: 
                self.trash.append([dest_figure, dst])
                self.moves[-1].append("x")
            return True
        return False

    def get_valid_moves(self, row, col, shortcut=None):
        if shortcut is None: 
            shortcut = self.chessboard[row][col]
        chessboard = self.chessboard
        valid_moves = []
        if ((self.last_color == "w" and shortcut.isupper()) \
            or (self.last_color == "b" and shortcut.islower())): 
            return valid_moves
        if shortcut.upper() == "N":
            pos_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]
            valid_moves = []
            for move in pos_moves:
                new_row = row + move[0]
                new_col = col + move[1]
                figure_on_destination = None
                if new_row in range(8) and new_col in range(8):
                    figure_on_destination = chessboard[new_row][new_col]
                    if not figure_on_destination or figure_on_destination.isupper() != \
                        shortcut.isupper():
                        valid_moves.append([new_row, new_col])
        elif shortcut.upper() == "P": 
            valid_moves = []
            new_row1 = None
            if shortcut == "P": 
                new_row = row - 1;
                if row == 6: 
                    new_row1 = row - 2
            else:
                new_row = row + 1
                if row == 1: 
                    new_row1 = row + 2
            if new_row in range(8) and not chessboard[new_row][col]: 
                valid_moves.append([new_row, col])
                if new_row1 and not chessboard[new_row1][col]: 
                    valid_moves.append([new_row1, col])
            for shift in [-1, 1]: 
                new_col = col + shift
                if new_row in range(8) and new_col in range(8): 
                    figure_on_destination = chessboard[new_row][new_col]
                    if  figure_on_destination and figure_on_destination.isupper() != \
                        shortcut.isupper():
                        valid_moves.append([new_row, new_col])
        elif shortcut.upper() in "QK":
            directions = [[1, 0], [1, 1], [0, 1], [1, -1]]
            coefs = []
            if shortcut.upper() == "Q":
                coefs = [[-row - 1, 8 - row], [-min(row, col) - 1, 8 - max(row, col)], \
                    [-col - 1, 8 - col], [max(-row - 1, col - 8), min(8 - row, col + 1)]] 
            else: 
                coefs = [[max(-row - 1, -2), min(8 - row, 2)], \
                    [max(-min(row, col) - 1, -2), min(8 - max(row, col),2)], \
                    [max(-col - 1, -2), min(8 - col, 2)], \
                    [max(max(-row - 1, col - 8), -2), min(min(8 - row, col + 1), 2)]]
                # castlings - king moving from original position two squares towards a rook
                # find king moves
                if col == 4 and not self.cell_moves(row, col): 
                    if not chessboard[row][col + 1] and not chessboard[row][col + 2] \
                        and chessboard[row][col + 3] and not self.cell_moves([row], [col + 3]): 
                        valid_moves.append([row, col + 2])
                    if not chessboard[row][col - 1] and not chessboard[row][col - 2] \
                        and not chessboard[row][col - 3] \
                        and chessboard[row][col - 4] and not self.cell_moves([row], [col - 4]): 
                        valid_moves.append([row, col - 2])
        elif shortcut.upper() == "B":
            directions = [[1, 1], [1, -1]]
            coefs = [[-min(row, col) - 1, 8 - max(row, col)], [max(-row - 1, col - 8), min(8 - row, col + 1)]]
        elif shortcut.upper() == "R":
            directions = [[1, 0], [0, 1]]
            coefs = [[-row - 1, 8 - row], [-col - 1, 8 - col]]
        if shortcut.upper() in "QKBR" and coefs: 
            for index, direction in enumerate(directions): 
                #for coef in range(coefs[index][0], coefs[index][1]): 
                for (ifrom, ito, istep) in ((-1, coefs[index][0], -1), (1, coefs[index][1], 1)):
                    for coef in range(ifrom, ito, istep): 
                        new_row = row + coef * direction[0]
                        new_col = col + coef * direction[1]
                        #if coef != 0: 
                        figure_on_destination = chessboard[new_row][new_col]
                        if  figure_on_destination:
                            if figure_on_destination.isupper() != \
                                shortcut.isupper():
                                valid_moves.append([new_row, new_col])
                            break
                        else: 
                            valid_moves.append([new_row, new_col])
        return valid_moves
        
if __name__ == "__main__":
    f = open("chessboard.htm", "w")
    to_write = html_source_code(svg_element_code(chessboard))
    f.write(to_write)
    f.close()
