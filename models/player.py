#!/usr/bin/env python

from parse_rest.datatypes import Object

class Player(Object):
    @staticmethod
    def getPlayer(**kwargs):
        players = Player.Query.filter(**kwargs)
        if players.count() == 1:
            return players.get()
        return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.objectId)
