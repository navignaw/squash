#!/usr/bin/env python

import os
from flask import Flask, render_template
#from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from parse_rest.connection import register

from models.room import *

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


@socketio.on('connect', namespace='/server')
def on_connect():
    emit('response', {'data': 'Connection successful'})
    rooms = Room.Query.all()
    emit('load_rooms', {'rooms': [{'name': room.name, 'users': room.users} for room in rooms]})


@socketio.on('disconnect', namespace='/server')
def on_disconnect():
    emit('response', {'data': 'Disconnection successful'})


@socketio.on('client_connect', namespace='/server')
def on_client_connect(data):
    print 'client connected:', data


@socketio.on('join_room', namespace='/server')
def on_join_room(data):
    username = data['username']
    room_name = data['room']
    room = Room.Query.get(name=room_name) or Room(name=room_name, users=[])
    try:
        room.add_user(username)
        room.save()
        join_room(room_name)
        emit('response', {'data': username + ' has entered the room.'}, room=room_name)
        emit('update_room', {'name': room_name, 'users': room.users}, broadcast=True)
    except Room.ExceededCapacityError:
        emit('response', {'data': 'Error: room is full!'})


@socketio.on('leave_room')
def on_leave_room(data, namespace='/server'):
    username = data['username']
    room_name = data['room']
    room = Room.Query.get(name=room_name)
    room.remove_user(username)
    leave_room(room_name)
    emit('response', {'data': username + ' has left the room.'}, room=room)
    emit('update_room', {'name': room_name, 'users': room.users}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app,
                 host=os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1'),
                 port=int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080)))
