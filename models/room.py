#!/usr/bin/env python

from parse_rest.datatypes import Object
from parse_rest.query import QueryResourceDoesNotExist


class Room(Object):
    """ Room for users to play a game. Limited to 6 """
    MAX_CAPACITY = 6

    class ExceededCapacityError(Exception):
        def __init__(self):
            self.message = 'The room you tried to join is full.'

    class DoesNotExistError(Exception):
        def __init__(self):
            self.message = 'The room does not exist.'

    @staticmethod
    def getRoom(**kwargs):
        try:
            return Room.Query.get(**kwargs)
        except QueryResourceDoesNotExist:
            raise Room.DoesNotExistError

    def add_user(self, user):
        if user in self.users:
            return
        if len(self.users) == self.MAX_CAPACITY:
            raise self.ExceededCapacityError
        self.users.append(user)

    def remove_user(self, user):
        try:
            self.users.remove(user)
        except ValueError:
            pass

    def is_empty(self):
        return len(self.users) == 0

    def to_dict(self):
        return {
            'id': self.objectId,
            'name': self.name,
            'users': self.users,
        }
