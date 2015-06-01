#!/usr/bin/env python

from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import ValidationError
from models.player import *

def checkUsername(form, field):
    if not Player.getPlayer(field.data):
        raise ValidationError('Username does not exist')

def checkPassword(form, field):
    player = Player.getPlayer(form.username.data)
    if player and field.data != player.password:
        raise ValidationError('Incorrect password')

class LoginForm(Form):
    username = StringField('Username', [checkUsername])
    password = PasswordField('Password', [checkPassword])

    
