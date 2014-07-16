from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import gevent
from img_handler import *

app = Flask(__name__)
app.config.update({
    'DEBUG' : True,
    'SECRET_KEY' : 'development key',
    'USERNAME' : ['admin'],
    'PASSWORD' : ['default'],
    })
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

job_handler = ImageJobHandler()
jobs = []


@app.route('/')
def show_streams():
    return render_template('show_streams.html')


@app.route('/webhandler')
def webhandler(wait=0.1):
    if request.environ.get('wsgi.websocket'):
    return render_template('show_streams.html')


@app.route('/listen_job', methods=['POST'])
def listen_job():
    if not session.get('logged_in'):
        abort(401)
    flash('switch job was successfully posted')
    return redirect(url_for('show_streams'))


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    kill_jobs()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_streams'))


if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

