#!/usr/bin/env python

from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import ValidationError
from models.player import *

def usernameExists(form, field):
    if not Player.getPlayer(username=field.data):
        raise ValidationError('Username does not exist.')

def correctPassword(form, field):
    player = Player.getPlayer(username=form.username.data)
    if player and field.data != player.password:
        raise ValidationError('Password is incorrect.')

class LoginForm(Form):
    username = StringField('Username', [usernameExists])
    password = PasswordField('Password', [correctPassword])

    
