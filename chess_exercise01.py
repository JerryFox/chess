FIGURES = "RNBKQBNRPrnbkqbnrp"
CHESS_IMG_FOLDER = "static/images/"

IMAGE_TEMPLATE = """<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink"
xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); "
width="80" height="80"></image>
"""

SVG_TEMPLATE = """<svg class="chessboard" height="810" version="1.1" width="810" \
xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; position: relative;">
<image x="0" y="0" width="810" height="810" preserveAspectRatio="xMinYMin" \
    xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{img_folder}Chess_Board_01.svg"
    style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></image>
{images}</svg>
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
	<head>
		<title>chessboard</title>
		<meta charset=utf-8">
	</head>
	<body>
{insert_html}
	</body>
</html>
"""

def unpacked_to_packed_position(position):
    packed_position = ""
    number_of_blanks = 0
    for character in position:
        if character not in FIGURES:
            number_of_blanks += 1
        else:
            # write number of blanks or single blank before figure
            if number_of_blanks:
                packed_position += "-" if number_of_blanks == 1 else str(number_of_blanks)
                number_of_blanks = 0   # blanks are written
            # write figure
            packed_position += character
    # possible rest in number_of_blanks is ignored
    return packed_position

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

def image_element_code(row, column, shortcut):
    image_template = IMAGE_TEMPLATE
    if shortcut in FIGURES:
        return image_template.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut))
    else:
        return ""

def svg_element_code(chessboard):
    svg_template = SVG_TEMPLATE
    images = ""
    for row in range(len(chessboard)):
        for column in range(len(chessboard[0])):
            if chessboard[row][column]:
                images += image_element_code(row, column, chessboard[row][column])
    return svg_template.format(img_folder=CHESS_IMG_FOLDER, images=images)

def html_source_code(insert_html):
    html_template = HTML_TEMPLATE
    return html_template.format(insert_html=insert_html)

class Chessboard:

    def __init__(self, position="base"):
        self.position = position
        self.chessboard = self.get_chessboard()

    def get_chessboard(self):
        position = packed_to_unpacked_position(self.position)
        chessboard = [[" " if c == "-" else c
                       for c in position[i * 8 : i * 8 + 8]] for i in range(8)]
        return chessboard

    def get_html(self):
        return html_source_code(svg_element_code(self.chessboard))

    def get_position(self):
        return "".join([row[col] for row in self.chessboard for col in range(8)]).replace(" ", "-")

    def get_packed_position(self):
        return unpacked_to_packed_position(self.get_position())

    def set_position(self, position=None):
        if position is None:
            self.position = self.get_position()
        else:
            self.position = position
            self.chessboard = self.get_chessboard()

    def set_position_to_packed(self):
        self.position = self.get_packed_position()

