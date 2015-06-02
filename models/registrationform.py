#!/usr/bin/env python

from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.validators import ValidationError
from models.player import *
import re

def validUsername(form, field):
    if not re.match('^[^\\s<>&]{1,50}$', field.data):
        raise ValidationError('Invalid username')
    if Player.getPlayer(username=field.data):
        raise ValidationError('Username already exists.')

def validPassword(form, field):
    if not re.match('^[^\\s<>&]{4,50}$', field.data):
        raise ValidationError('Invalid password')

class RegistrationForm(Form):
    username = StringField('Username', [validUsername])
    password = PasswordField('Password', [validPassword])
    confirmPassword = PasswordField('Confirm password', [validators.EqualTo('password', message='Passwords must match.')])
    conditions = BooleanField('Terms and Conditions', [validators.AnyOf([True], 'You must accept the terms and conditions.')])

    def registerUser(self):
        p = Player(username=self.username.data, password=self.password.data)
        p.save()
