# files serving with directory list
# simple bottle application

# chess exercise application for seminar

from bottle import default_app, route, static_file, request, abort
import os, os.path
#import chess_exercise01 as chess
import chess

chess.CHESS_IMG_FOLDER = "/static/images/"
chess.SCRIPT_FOLDER = "/static/scripts/"
chess.CSS_FOLDER = "/static/css/"

ROOT = "/home/vysoky"   # where are files serving from
PATH_PREFIX = "/files"          # path prefix in browser


@route("/")
def kudy_z_nudy():
    return "<h1>nothing here but love...</h1>"


# static file chess.py from root (due to import import chess)
@route('/chessboard/<name:re:.*chess\.py>')
@route('/chess.py')
def send_static_chess(name=""):
    return static_file("chess.py", root='/home/vysoky/projects/chess')


#### python files in root or in /chessboard/...
@route('/<name:re:[^\/]*\.py>')
@route('/chessboard/<name:re:.*\.py>')
def pokus(name=""):
    py_folder = '/home/vysoky/projects/chess/static/scripts'
    file = name.split("/")[-1]
    fpath = py_folder + "/" + file
    # return appropriate file or abort
    if os.path.exists(fpath):
        f = open(fpath)
        pysrc = f.read()
        f.close()
        return(pysrc)
    else:
        abort(404, "python file not found")



# static files
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/vysoky/projects/chess/static')

@route("/chessboard/<position>/reset/<positions>")
def chessboard_reset_fields(position="base", positions=""):
    if request.get_cookie("chess_zoom"):
        zoom = request.get_cookie("chess_zoom")
    else:
        zoom = "60%"
    ch = chess.Chessboard(position)
    ch.remove_figures(positions)
    return ch.get_html(zoom=zoom)

@route("/chessboard/<position>/set/<fig_positions>")
def chessboard_set_fields(position="blank", fig_positions=""):
    if request.get_cookie("chess_zoom"):
        zoom = request.get_cookie("chess_zoom")
    else:
        zoom = "60%"
    ch = chess.Chessboard(position)
    ch.add_figures(fig_positions)
    return ch.get_html(zoom=zoom)

@route("/chessboard")
@route("/chessboard/")
@route("/chessboard/<position>")
def chessboard(position="base"):
    if request.get_cookie("chess_zoom"):
        zoom = request.get_cookie("chess_zoom")
    else:
        zoom = "60%"
    ch = chess.Chessboard(position)
    return ch.get_html(zoom=zoom)

@route(PATH_PREFIX)
@route(PATH_PREFIX + '<filepath:path>')
def server_static(filepath="/"):
    ipath = ROOT + filepath
    if os.path.isdir(ipath):
        list_dir = os.listdir(ipath)
        html_template = """
<html>
    <head>
        <title>List of {path}</title>
        <style>
            li.file {{
                list-style-type: circle;
            }}
            li.folder {{
                list-style-type: square;
            }}
        </style>
    </head>
    <body>
        <h2>Content of {path}</h2>
        <ul>
{items}
        </ul>
    </body>
</html>
"""
        list_isfile = []
        # list of (<isfile>, <name>)
        for i in list_dir:
            list_isfile.append((os.path.isfile(os.path.join(ipath,i)),i))
        # sort - folders first then sorted by names
        list_isfile.sort(key = lambda x: str(x[0]) + x[1])
        items = ""
        for item in list_isfile:
            iclass = "file" if item[0] else "folder"
            line = '<li class="{}"><a href="{}">{}</a></li>\n'
            items += line.format(iclass, PATH_PREFIX + os.path.join(filepath, item[1]), item[1])
        return html_template.format(path=filepath, items=items)
    else:
        return static_file(filepath, root=ROOT)

application = default_app()

