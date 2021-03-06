"""
configuration for chess application
valid configuration in hiddenconfig.py
"""

PROJECT_DIRECTORY = "/home/vysoky/projects/chess"
HOME_DIRECTORY = "/home/vysoky"
SHOW_HIDDEN = False # items with "hidden" prefix

CHESS_IMG_FOLDER = "/static/images/"
SCRIPT_FOLDER = "/static/scripts/"
CSS_FOLDER = "/static/css/"
TEMPLATE_FOLDER = "/templates/"

ROOT = HOME_DIRECTORY           # where are files serving from
PATH_PREFIX = "/files"          # path prefix in browser
INTER_PATH = ""                 # if app is not in the root of the hosting server

# db = MySQLdb.connect(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
DATABASE_HOST = 'vysoky.mysql.pythonanywhere-services.com'
DATABASE_NAME = 'vysoky$default'
DATABASE_USER = 'vysoky'
DATABASE_PASSWORD = 'abrakadabra'

try:
    from hiddenconfig import *
except ImportError:
    pass
