#!/usr/bin/env python

import os

from flask import Flask, flash, render_template, session, request, redirect, url_for
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from parse_rest.connection import register

from models.room import *
from models.player import *
from models.loginform import *
from models.registrationform import *

PARSE_APPLICATION_ID = 'LuuyCNuXJZZtMaZYaaV2PHilwjS82STGAVqJn3yu'
PARSE_REST_API_KEY = 'JRtiYnNbKMXS2sXBTfGgDVRqJv9UDlKAAbHVdsyB'
PARSE_MASTER_KEY = 'cyHCdfPpwbzQC8XTLkkBSYM2GgbNawGcmbyNISvn'


# Initialize Flask, SocketIO and Parse apps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'squashthefatties'
app.debug = True  # TODO: change this when we deploy

socketio = SocketIO(app)
register(PARSE_APPLICATION_ID, PARSE_REST_API_KEY, master_key=PARSE_MASTER_KEY)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return Player.getPlayer(objectId=id)


# Socket helper functions
def leave_socket_room(room_id=''):
    """Leave a room on Parse and socketIO"""
    username = current_user.username
    room = Room.getRoom(objectId=(room_id or session['room']))

    # Doesn't seem to work after we leave the room, so do it now:
    emit('response', {'data': username + ' has left the room.'}, room=room_id)

    room.remove_user(username)
    room.save()
    leave_room(room.objectId)
    session['room'] = ''
    if room.is_empty:
        close_room(room.objectId)
    emit('update_room', room.to_dict(), broadcast=True)

def join_socket_room(room_id):
    """Join a room on socketIO"""
    room = Room.getRoom(objectId=room_id)
    join_room(room_id)
    emit('response', {'data': current_user.username + ' has entered the room.'}, room=room_id)
    emit('update_room', room.to_dict(), broadcast=True)

def join_parse_room(room_id):
    """
    Join a room on Parse; may raise ExceededCapacityError or DoesNotExistError.
    Note: joining the socketIO room is separated from this function as it
          must be called via sockets
    """
    room = Room.getRoom(objectId=room_id)
    room.add_user(current_user.username)
    room.save()
    session['room'] = room.objectId
    return room


@socketio.on('connect', namespace='/server')
def on_connect():
    print 'client connected:', current_user.username
    emit('response', {'data': 'Connection successful'})
    rooms = Room.Query.all()
    emit('load_rooms', {'rooms': [room.to_dict() for room in rooms]})

@socketio.on('connect', namespace='/squash')
def on_connect():
    print 'client connected:', current_user.username
    emit('response', {'data': 'Connection successful'})
    room = Room.getRoom(objectId=session['room'])
    emit('load_room', room.to_dict())
    join_socket_room(room.objectId)


@socketio.on('disconnect', namespace='/server')
def on_disconnect():
    print 'client disconnected:', current_user.username
    emit('response', {'data': 'Disconnection successful'})

@socketio.on('disconnect', namespace='/squash')
def on_disconnect():
    print 'client disconnected:', current_user.username
    emit('response', {'data': 'Disconnection successful'})
    if session.get('room', ''):
        leave_socket_room()

@socketio.on('join_room', namespace='/squash')
def on_join_room(data):
    join_socket_room(data['room'])

@socketio.on('leave_room', namespace='/squash')
def on_leave_room(data):
    leave_socket_room(room_id=data['room'])


# Routes
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_user(Player.getPlayer(username=form.username.data), remember=True)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('index'))
    if current_user.is_authenticated():
      return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        form.registerUser()
        flash('User registered successfully.', 'success')
        return redirect(url_for('login'))
    if current_user.is_authenticated():
      return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/squash/room/<room_id>')
@login_required
def squash(room_id):
    try:
      room = join_parse_room(room_id)
    except (Room.ExceededCapacityError, Room.DoesNotExistError) as e:
      flash(e.message, 'error')
      return redirect(url_for('index'))
    return render_template('squash.html', room=room.to_dict())


if __name__ == "__main__":
    socketio.run(app,
                 host=os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1'),
                 port=int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080)))
