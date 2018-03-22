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
        position = "RNBKQBNR" + "P" * 8 + "-" * 32 + "p" * 8 + "rnbkqbnr"
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
    add_board = [["K", "Q"], ["R", "B"], ["N", "P"], ["", ""], ["", ""],
                 ["k", "q"], ["r", "b"], ["n", "p"]]
    images = ""
    for row in range(len(add_board)):
        for column in range(len(add_board[0])):
            if add_board[row][column]:
                images += image_element_code(row, column + 8, add_board[row][column], True) + "\n"
    return images

def svg_element_code(chessboard, zoom="60%"):
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

        <script type="text/python3" src="{script_folder}chess_brython.py"></script>
 	</head>
    <body onload="brython(1)">
        <div>
            <button id="but-chessboard-hide-show">chess_hi/sh</button>
            <button id="but-console-hide-show">console_hi/sh</button>
            <button id="but-fig-count">count fig.</button>
            <button id="but-go-to-position">goto pos.</button>
            <button id="but-test">test</button>
            <button id="but-zoom-out">◀</button>
            <span id="zoom-display"></span>
            <button id="but-zoom-in">▶</button>
            <span id="coordinates"></span>
            <span id="chessboard-coordinates"></span>


            <div id="chess-container">
{insert_html}
            </div>

        </div>
        <div>
        </div>
        <div id="console" class="console">
            <!-- Brython console -->
            <textarea id=code class=codearea rows=20></textarea>
            <div id=content></div>
            <script type="text/python3" src="{script_folder}console.py" id="__main__"></script>
            <!-- /Brython console -->
        </div>
        <div id="output">
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

    def get_chessboard(self):
        position = packed_to_unpacked_position(self.position)
        chessboard = [["" if c == "-" else c
                       for c in position[i * 8 : i * 8 + 8]] for i in range(8)]
        return chessboard


    def get_html(self, zoom="60%"):
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

if __name__ == "__main__":
    f = open("chessboard.htm", "w")
    to_write = html_source_code(svg_element_code(chessboard))
    f.write(to_write)
    f.close()
