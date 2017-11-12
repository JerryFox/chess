# chessboard generation
# html with SVG

CHESS_IMG_FOLDER = "images/"

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
    text = '<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); " width="80" height="80"></image>'
    return text.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut))

def svg_source_text(chessboard):
    source = """<svg
class="chessboard" height="810" version="1.1" width="810" xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; position: relative;">
<image x="0" y="0" preserveAspectRatio="xMinYMin" \
xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{img_folder}Chess_Board_01.svg" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></image>
{images}</svg>
"""
    images = ""
    for row in range(len(chessboard)):
        for column in range(len(chessboard[0])):
            if chessboard[row][column]:
                images += img_source_text(row, column, chessboard[row][column]) + "\n"
    return source.format(img_folder=CHESS_IMG_FOLDER, images=images)

def html_source_text(insert_html):
    html_template = """<!DOCTYPE html>
    <title>Chessboard</title>
    <meta
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
    return html_template.format(insert_html=insert_html)

class Chessboard:

    def __init__(self, position="base"):
        self.position = position

    def matrix(self):
        pos = self.position
        if pos == "base":
            pos = "RNBKQBNR" + "P" * 8 + "-" * 32 + "p" * 8 + "rnbkqbnr"
        elif pos == "blank":
            pos = "-" * 64
        pos = pos + "-" * (64 - len(pos))
        ch = [["" for c in range(8)] for r in range(8)]
        index = 0
        for r in range(len(ch)):
            for c in range(len(ch[r])):
                cell = pos[index]
                cell = "" if (cell[0] in "-") else cell[0]
                ch[r][c] = cell
                index += 1
        return ch

    def html(self):
        return html_source_text(svg_source_text(self.matrix()))
    
if __name__ == "__main__":
    f = open("chessboard.htm", "w")
    to_write = html_source_text(svg_source_text(chessboard))
    f.write(to_write)
    f.close()
