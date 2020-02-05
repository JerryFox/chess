<!DOCTYPE html>
<html>
	<head>
		<title>chessboard</title>
		<meta charset=utf-8">
		<link rel="stylesheet" type="text/css" href="{{css_folder}}chess.css">
        <script src="{{script_folder}}brython.js"></script>
        <script src="{{script_folder}}brython_stdlib.js"></script>

        <!--Brython - editor - HEAD -->
        <link rel="stylesheet" type="text/css"
              href="https://fonts.googleapis.com/css?family=Roboto">
        <link rel="stylesheet" href="{{css_folder}}editor.css">

        <script src="{{script_folder}}ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="{{script_folder}}ace/ext-language_tools.js" type="text/javascript" charset="uteditorf-8"></script>
        <script src="{{script_folder}}ace/mode-python3.js" type="text/javascript" charset="utf-8"></script>
        <script src="{{script_folder}}ace/snippets/python.js" type="text/javascript" charset="utf-8"></script>

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

        <script type="text/python3" src="{{script_folder}}chess_brython.py"></script>
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
%#{{insert_html}}
<svg id="chessboard" class="chessboard" viewBox="0 0 1007 810"
version="1.1" width="{{zoom}}" xmlns="http://www.w3.org/2000/svg"
style="overflow: hidden; position: relative;">
<style>
    .draggable {
        cursor: move;
    }

    #labels text {
        font-weight: bold;
        fill: black;
        stroke-width: 0;
        font-size: 16px;
        font-family: serif;
        //text-anchor: middle;
        //xml:space: preserve;
        stroke: black;
    }
</style>
<!--
chessboard position string:
{{position}}
{{packed_position}}
-->
<image x="0" y="0" width="810" height="810" preserveAspectRatio="xMinYMin" \
    xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="{{img_folder}}Chess_Board_01.svg"
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
<%
images = ""
from chess import image_element_code, beside_figures_images
for row in range(len(chessboard)):
    for column in range(len(chessboard[0])):
        if chessboard[row][column]:
            images += image_element_code(row, column, chessboard[row][column]) + "\n"
        end
    end
end
beside_figures = beside_figures_images()
%>
{{!images}}
{{!beside_figures}}
</g>
</svg>



            </div>

            <div id="console" class="console gr-console">
                <!-- Brython console -->
                <textarea id=code class=codearea rows=20></textarea>
                <div id=content></div>
                <script type="text/python3" src="{{script_folder}}console.py" id="__main__"></script>
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
                    <input id="code-url" type="text" name="code-url" value="walk.py" size="20">
    	        </div>
                <div id="editor"></div>
            </div>

        <script type="text/python3">
            from browser import window
            window.scrollTo(0, 0)
        </script>

	</body>
</html>
