"""
bx_ajax.py
Brython eXercise
get data from web server using ajax
"""

from browser import ajax, document as doc

def on_complete(req):
    # function runnig after request is complete
    if req.status == 200 or req.status == 0:
        doc["output"].innerHTML = req.text
    else:
        #doc["output"].innerHTML = req.text
        doc["output"].innerHTML = "ERROR {}".format(req.status)


def get(url):
    req = ajax.ajax()
    req.bind('complete',on_complete)
    req.open('GET',url,True)
    req.set_header('content-type','application/x-www-form-urlencoded')
    req.send()
    return req

doc["output"].innerHTML = ""
doc.ch_brython_exercises = ""
url = "http://vysoky.pythonanywhere.com/get_brython_exercises"
req = get(url)


