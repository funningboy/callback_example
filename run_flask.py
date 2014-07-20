from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from pydisplay import *
from pyasync import *
from pycheese import *
import time

app = Flask(__name__)
app.config.update({
    'DEBUG' : True,
    'SECRET_KEY' : 'development key',
    'USERNAME' : ['admin'],
    'PASSWORD' : ['default'],
    })
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Async channel for PyChess to PyDisplay
async = PyAsync()

# thread queue
th_q = {
        # run as PYTHON callback(py c api) or Normal callback(void*) return
        'PYCHEESE'  : PyCheese(typ='PYTOHNCB', async=async),
        'PYDISPLAY' : PyDisplay(async=async),
        }

[th_i.setDaemon(True) for th_i in th_q.values()]
[th_i.on_stop()       for th_i in th_q.values()]


def wap_on_callback_py(name):
    """ as a wap callback vif for py """
    global th_q
    th_q['PYCHEESE'].on_callback_py(name)


def start_callback_py():
    """ start to run callback """
    global th_q
    global async
    [th_i.on_restart() for th_i in th_q.values()]
    time.sleep(1)


def stop_callback_py():
    """ stop to run callback """
    global th_q
    global async
    [th_i.on_stop() for th_i in th_q.values()]
    async.on_clear()
    time.sleep(1)
    return th_q['PYDISPLAY'].on_query()


@app.route('/')
def show_streams():
    return render_template('show_streams.html')


@app.route('/webhandler')
def webhandler(wait=0.1):
    return render_template('show_streams.html')


@app.route('/listen_job', methods=['POST'])
def listen_job():
    if not session.get('logged_in'):
        abort(401)
    req = request.form['cb_proc']
    if req in ['StartCallBack']:
        start_callback_py()
        flash('switch job was successfully posted')
        return redirect(url_for('show_streams'))
    elif req in ['StopCallBack']:
        entries = stop_callback_py() # query result event
        flash('switch job was successfully posted')
        return redirect(url_for('show_streams', entries=entries))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global th_q
    global async
    error = None
    if request.method == 'POST':
        if request.form['username'] not in app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] not in app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_streams'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    global th_q
    global async
    session.pop('logged_in', None)
    flash('You were logged out')
    stop_callback_py()
    return redirect(url_for('show_streams'))


if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()


