#!/usr/bin/env python

import os
from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room
from parse_rest.connection import register

from models.room import *
from models.player import *
from models.loginform import *

PARSE_APPLICATION_ID = 'LuuyCNuXJZZtMaZYaaV2PHilwjS82STGAVqJn3yu'
PARSE_REST_API_KEY = 'JRtiYnNbKMXS2sXBTfGgDVRqJv9UDlKAAbHVdsyB'
PARSE_MASTER_KEY = 'cyHCdfPpwbzQC8XTLkkBSYM2GgbNawGcmbyNISvn'


# Initialize Flask, SocketIO and Parse apps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'squashthefatties'
app.debug = True  # TODO: change this when we deploy

socketio = SocketIO(app)
register(PARSE_APPLICATION_ID, PARSE_REST_API_KEY, master_key=PARSE_MASTER_KEY)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


def leave_socket_room(room_id=''):
    username = session['username']
    room = Room.Query.get(objectId=(room_id or session['room']))

    # Doesn't seem to work after we leave the room, so do it now:
    emit('response', {'data': username + ' has left the room.'}, room=room.name)

    room.remove_user(username)
    room.save()
    leave_room(room.name)
    session['room'] = ''
    if room.is_empty:
        close_room(room.name)
    emit('update_room', room.to_dict(), broadcast=True)


@socketio.on('connect', namespace='/server')
def on_connect():
    emit('response', {'data': 'Connection successful'})
    rooms = Room.Query.all()
    emit('load_rooms', {'rooms': [room.to_dict() for room in rooms]})


@socketio.on('disconnect', namespace='/server')
def on_disconnect():
    emit('response', {'data': 'Disconnection successful'})
    if session.get('room', ''):
        leave_socket_room()


@socketio.on('client_connect', namespace='/server')
def on_client_connect(data):
    session['username'] = data['username']
    print 'client connected:', data['username']


@socketio.on('join_room', namespace='/server')
def on_join_room(data):
    username = session['username']
    room = Room.Query.get(objectId=data['room'])
    try:
        room.add_user(username)
        room.save()
        join_room(room.name)
        session['room'] = room.objectId
        emit('response', {'data': username + ' has entered the room.'}, room=room.name)
        emit('update_room', room.to_dict(), broadcast=True)
    except Room.ExceededCapacityError:
        emit('response', {'data': 'Error: room is full!'})


@socketio.on('leave_room')
def on_leave_room(data, namespace='/server'):
    leave_socket_room(room_id=data['room'])


if __name__ == "__main__":
    socketio.run(app,
                 host=os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1'),
                 port=int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080)))
