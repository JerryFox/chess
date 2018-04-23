import sys
import time
import traceback
#import javascript

from browser import document as doc, window

# set height of container to 66% of screen
_height = doc.documentElement.clientHeight
_s = doc['container']
_s.style.height = '%spx' % int(_height * 0.66)

has_ace = True
try:
    editor = window.ace.edit("editor")
    session = editor.getSession()
    session.setMode("ace/mode/python")

    editor.setOptions({
     'enableLiveAutocompletion': True,
     'enableSnippets': True,
     'highlightActiveLine': False,
     'highlightSelectedWord': True
    })
except:
    from browser import html
    editor = html.TEXTAREA(rows=20, cols=70)
    doc["editor"] <= editor
    def get_value(): return editor.value
    def set_value(x):editor.value = x
    editor.getValue = get_value
    editor.setValue = set_value
    has_ace = False

if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None

if 'set_debug' in doc:
    __BRYTHON__.debug = int(doc['set_debug'].checked)

def reset_src(src="py_src"):
    editor.storage_name = src
    if storage is not None and src in storage:
        editor.setValue(storage[src])
    else:
        editor.setValue('for i in range(10):\n\tprint(i)')
    editor.scrollToRow(0)
    editor.gotoLine(0)

def reset_src_area(src="py_src"):
    editor.storage_name = src
    if storage and src in storage:
        editor.value = storage[src]
    else:
        editor.value = 'for i in range(10):\n\tprint(i)'

def to_str(xx):
    return str(xx)

"""
info = sys.implementation.version
doc['version'].text = '%s.%s.%s' % (info.major, info.minor, info.micro)
"""

#output = ''

# load a Python script
def load_script(evt):
    _name = evt.target.value + '?foo=%s' % time.time()
    editor.setValue(open(_name).read())

# run a script, in global namespace if in_globals is True
def run(*args):
    global output
    #doc["console"].value = ''
    src = editor.getValue()
    if storage is not None:
       storage[editor.storage_name] = src

    t0 = time.perf_counter()
    try:
        ns = {'__name__':'__main__'}
        if doc.ch_editor_ns:
            ns = doc.ch_editor_ns
        exec(src, ns)
        state = 1
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        state = 0
    #output = doc["console"].value

    print('<completed in %6.2f ms>' % ((time.perf_counter() - t0) * 1000.0))
    print(">>> ", end="")
    # scroll down
    doc["code"].scrollTop = doc["code"].scrollHeight
    return state

if has_ace:
    reset_src()
    doc["editor"].reset_src = reset_src
else:
    reset_src_area()
    doc["editor"].reset_src = reset_src_area
