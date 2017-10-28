# chessboard generation
# html with SVG 

chessboard = [["" for i in range(8)]for j in range(8)]

chessboard[0] = list("RNBKQBNR")
chessboard[1] = list("P" * 8)
chessboard[6] = list("p" * 8)
chessboard[7] = list("rnbkqbnr")

def get_img_name(shortcut):
    name = "Chess_{}{}t45.svg".format(shortcut.lower(),
                                      "l" if shortcut.isupper() else "d")
    return name

def img_source_text(row, column, shortcut):
    text = '<image x="{}" y="{}" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{}" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0); " width="80" height="80"></image>'
    return text.format(15 + column * 100, 13 + row * 100, "images/" + get_img_name(shortcut))

def write_svg(chessboard, file_name="chessboard.htm"):
    source = """<svg
class="chessboard" height="810" version="1.1" width="810" xmlns="http://www.w3.org/2000/svg" style="overflow: hidden; position: relative;">
<image x="0" y="0" preserveAspectRatio="xMinYMin" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="images/Chess_Board_01.svg" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></image>
{}</svg>
"""
    images = ""
    for row in range(len(chessboard)):
        for column in range(len(chessboard[0])):
            if chessboard[row][column]: 
                images += img_source_text(row, column, chessboard[row][column]) + "\n"
    f = open(file_name, "w")
    f.write(source.format(images))
    f.close()
    return

write_svg(chessboard)

