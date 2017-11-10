# chessboard generation
# html with SVG

chessboard = [["" for i in range(8)]for j in range(8)]

chessboard[0] = list("RNBKQBNR")
chessboard[1] = list("P" * 8)
chessboard[6] = list("p" * 8)
chessboard[7] = list("rnbkqbnr")

def get_img_name(shortcut):
    """shortcuts:
    RNBKQBNRP - dark figures (d)
    rnbkqbnrp - light figures (l)
    """
    name = "Chess_{}{}t45.svg".format(shortcut.lower(),
                                      "l" if shortcut.isupper() else "d")
    return name

def img_source_text(row, column, shortcut):
    text = '<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); " width="80" height="80"></image>'
    return text.format(15 + column * 100, 13 + row * 100, "images/" + get_img_name(shortcut))

def svg_source_text(chessboard):
    source = """<svg
class="chessboard" height="810" version="1.1" width="810" xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; position: relative;">
<image x="0" y="0" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="images/Chess_Board_01.svg" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></image>
{images}</svg>
"""
    images = ""
    for row in range(len(chessboard)):
        for column in range(len(chessboard[0])):
            if chessboard[row][column]:
                images += img_source_text(row, column, chessboard[row][column]) + "\n"
    return source.format(images=images)

def write_html(insert_html, file_name="chessboard.htm"):
    html_template = """<!DOCTYPE html>
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
    f = open(file_name, "w")
    to_write = html_template.format(insert_html=insert_html)
    f.write(to_write)
    f.close()
    return to_write

write_html(svg_source_text(chessboard))
