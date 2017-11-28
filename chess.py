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

def get_img_name(shortcut):
    """shortcuts:
    RNBKQBNRP - dark figures (d)
    rnbkqbnrp - light figures (l)
    image name format example:
    Chess_klt45.svg - white king
    """
    name = "Chess_{}{}t45.svg".format(shortcut.lower(),
                                      "l" if shortcut.isupper() else "d")
    return name

def img_source_text(row, column, shortcut):
    text = """<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink"
    xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); "
    width="80" height="80"
    class="chess-figure draggable"
    transform="matrix(1 0 0 1 0 0)"
    >
    </image>"""
    return text.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut))

def beside_figures_images():
    add_board = [["K", "Q"], ["R", "B"], ["N", "P"], ["", ""], ["", ""],
                 ["k", "q"], ["r", "b"], ["n", "p"]]
    images = ""
    for row in range(len(add_board)):
        for column in range(len(add_board[0])):
            if add_board[row][column]:
                images += img_source_text(row, column + 8, add_board[row][column]) + "\n"
    return images

def svg_source_text(chessboard):
    source = """<svg id="chessboard" class="chessboard" viewBox="0 0 1105 810"
    version="1.1" width="100%" xmlns="http://www.w3.org/2000/svg"
    style="overflow: hidden; position: relative;">
		<style>
		    .draggable {{
                cursor: move;
		    }}
		</style>
<!--
chessboard position string:
{position}
{packed_position}
-->
<image x="0" y="0" preserveAspectRatio="xMinYMin" \
    xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{img_folder}Chess_Board_01.svg"
    style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);">
</image>
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
                images += img_source_text(row, column, chessboard[row][column]) + "\n"
                position += chessboard[row][column]
            else:
                position += "-"
    ch = Chessboard(position)
    pp = ch.get_packed_position()
    beside_figures = beside_figures_images()
    return source.format(position=position, packed_position=pp,
            img_folder=CHESS_IMG_FOLDER, images=images, beside_figures=beside_figures)

def html_source_text(insert_html):
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
            <button id="but-chessboard-hide-show">chess_hide/show</button>
            <button id="but-console-hide-show">console_hi/sh</button>
            <button id="but-fig-count">count fig.</button>
            <button id="but-zoom-out">◀</button>
            <span id="zoom-display"></span>
            <button id="but-zoom-in">▶</button>
            <span id="coordinates"></span>


            <div id="chess-container">
{insert_html}
            </div>

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
        position = self.position
        if position == "base":
            position = "RNBKQBNR" + "P" * 8 + "-" * 32 + "p" * 8 + "rnbkqbnr"
        elif position == "blank":
            position = "-" * 64
        elif any(character.isdigit() for character in position):
            unpacked_position = ""
            number_in_string = 0
            for character in position:
                if not character.isdigit():
                    unpacked_position += "-" * number_in_string
                    number_in_string = 0
                    unpacked_position += character
                else:
                    number_in_string = number_in_string * 10 + int(character)
            position = unpacked_position
        position = position + "-" * (64 - len(position))
        chessboard = [["" for column in range(8)] for r in range(8)]
        index = 0
        for row in range(len(chessboard)):
            for column in range(len(chessboard[row])):
                cell = position[index]
                cell = "" if (cell[0] in "-_ ") else cell[0]    # free cell
                chessboard[row][column] = cell                  # figure in cell
                index += 1
        return chessboard

    def get_html(self):
        return html_source_text(svg_source_text(self.chessboard))

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
    to_write = html_source_text(svg_source_text(chessboard))
    f.write(to_write)
    f.close()
