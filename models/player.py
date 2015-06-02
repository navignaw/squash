#!/usr/bin/env python

from parse_rest.datatypes import Object

class Player(Object):
    @staticmethod
    def getPlayer(**kw):
        players = Player.Query.filter(**kw)
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
