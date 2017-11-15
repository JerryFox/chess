# chessboard generation
# html with SVG

CHESS_IMG_FOLDER = "images/"
FIGURES = "RNBKQBNRPrnbkqbnrp"

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
    class="draggable"
    transform="matrix(1 0 0 1 0 0)"
    onmousedown="selectElement(evt)"
    >
    </image>"""
    return text.format(15 + column * 100, 13 + row * 100,
                       CHESS_IMG_FOLDER + get_img_name(shortcut))

def svg_source_text(chessboard):
    source = """<svg class="chessboard"
    height="810" version="1.1" width="1000" xmlns="http://www.w3.org/2000/svg"
    style="overflow: hidden; position: relative;">
		<style>
		    .draggable {{
                cursor: move;
		    }}
		</style>
    <script type="text/ecmascript"><![CDATA[
    var selectedElement = 0;
    var currentX = 0;
    var currentY = 0;
    var currentMatrix = 0;

    function selectElement(evt) {{
      selectedElement = evt.target;
      currentX = evt.clientX;
      currentY = evt.clientY;
      currentMatrix = selectedElement.getAttributeNS(null, "transform").slice(7,-1).split(' ');

      for(var i=0; i<currentMatrix.length; i++) {{
        currentMatrix[i] = parseFloat(currentMatrix[i]);
      }}

      selectedElement.setAttributeNS(null, "onmousemove", "moveElement(evt)");
      selectedElement.setAttributeNS(null, "onmouseout", "deselectElement(evt)");
      selectedElement.setAttributeNS(null, "onmouseup", "deselectElement(evt)");
    }}

    function moveElement(evt) {{
      var dx = evt.clientX - currentX;
      var dy = evt.clientY - currentY;
      currentMatrix[4] += dx;
      currentMatrix[5] += dy;

      selectedElement.setAttributeNS(null, "transform", "matrix(" + currentMatrix.join(' ') + ")");
      currentX = evt.clientX;
      currentY = evt.clientY;
    }}

    function deselectElement(evt) {{
      if(selectedElement != 0){{
          currentMatrix = selectedElement.getAttributeNS(null, "transform").slice(7,-1).split(' ');
          for(var i=0; i<currentMatrix.length; i++) {{
            currentMatrix[i] = parseFloat(currentMatrix[i]);
          }}
          currentMatrix[4] = 100 * Math.round(currentMatrix[4] / 100);
          currentMatrix[5] = 100 * Math.round(currentMatrix[5] / 100);
          selectedElement.setAttributeNS(null, "transform", "matrix(" + currentMatrix.join(' ') + ")");

          selectedElement.removeAttributeNS(null, "onmousemove");
          selectedElement.removeAttributeNS(null, "onmouseout");
          selectedElement.removeAttributeNS(null, "onmouseup");
          selectedElement = 0;
          }}
        }}

    ]]> </script>
<!--
chessboard position string:
{position}
{packed_position}
-->
<image x="0" y="0" preserveAspectRatio="xMinYMin" \
xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{img_folder}Chess_Board_01.svg" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></image>
{images}</svg>
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
    pp = ch.packed_position()
    return source.format(position=position, packed_position=pp, img_folder=CHESS_IMG_FOLDER, images=images)

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
        self.matrix()

    def matrix(self):
        pos = self.position
        if pos == "base":
            pos = "RNBKQBNR" + "P" * 8 + "-" * 32 + "p" * 8 + "rnbkqbnr"
        elif pos == "blank":
            pos = "-" * 64
        elif any(ch.isdigit() for ch in pos):
            iret = ""
            inum = 0
            for c in pos:
                if not c.isdigit():
                    iret += "-" * inum
                    inum = 0
                    iret += c
                else:
                    inum = inum * 10 + int(c)
            pos = iret
        pos = pos + "-" * (64 - len(pos))
        ch = [["" for c in range(8)] for r in range(8)]
        index = 0
        for r in range(len(ch)):
            for c in range(len(ch[r])):
                cell = pos[index]
                cell = "" if (cell[0] in "-") else cell[0]
                ch[r][c] = cell
                index += 1
        self.chessboard = ch
        return ch

    def html(self):
        return html_source_text(svg_source_text(self.matrix()))

    def packed_position(self):
        chessboard = self.chessboard
        position = ""
        inum = 0
        pos_pack = ""
        for row in range(len(chessboard)):
            for column in range(len(chessboard[0])):
                if chessboard[row][column]:
                    position += chessboard[row][column]
                    if inum:
                        if inum > 1:
                            pos_pack += str(inum)
                        else:
                            pos_pack += "-"
                    pos_pack += chessboard[row][column]
                    inum = 0
                else:
                    position += "-"
                    inum += 1
        if inum:
            if inum > 1:
                pos_pack += str(inum)
            else:
                pos_pack += "-"
        self.position = pos_pack
        return pos_pack

    def set(self, figure_pos):
        """set figures on chessboard
        figure_pos: str - <figure_name><coords>
        coords: 00 or a8
        """
        figures = figure_pos
        while len(figures) > 2:
            fig = figures[:3]
            figures = figures[3:]
            if fig[0] in FIGURES:
                if fig[1].isdigit():    # 00 address
                    row = int(fig[1])
                    col = int(fig[2])
                else:                   # a1 address
                    row = 8 - int(fig[2])
                    col = ord(fig[1].upper()) - 65
            self.chessboard[row][col] = fig[0]
        self.position = self.packed_position()

    def reset(self, positions):
        """remove figures from positions
        positions: str - <coords>
        coords: 00 or a8
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
        self.position = self.packed_position()

if __name__ == "__main__":
    f = open("chessboard.htm", "w")
    to_write = html_source_text(svg_source_text(chessboard))
    f.write(to_write)
    f.close()
