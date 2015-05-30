#!/usr/bin/env python

from parse_rest.datatypes import Object


class Room(Object):
    """ Room for users to play a game. Limited to 6 """
    MAX_CAPACITY = 6

    class ExceededCapacityError(Exception):
        pass

    def add_user(self, user):
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
