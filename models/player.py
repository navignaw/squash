#!/usr/bin/env python

from parse_rest.datatypes import Object

class Player(Object):
    @staticmethod
    def getPlayer(username):
        players = Player.Query.filter(username=username)
        if players.count() == 1:
            return players.get()
        return None
