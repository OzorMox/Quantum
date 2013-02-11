from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

import sys

class ClientChannel(Channel):
    # def Network(self, data):
        # print data


    def Network_update_player(self, data):
        self._server.SendToOthers(self, data)


    def Close(self):
        self._server.DeletePlayer(self)


class GameServer(Server):
    channelClass = ClientChannel
    totalPlayers = 0

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print "Server launched"


    def Connected(self, channel, addr):
        print "New connection:", channel
        self.AddPlayer(channel)
        self.AddEnemyPlayers(channel)

        
    def AddPlayer(self, player):
        print "New player" + str(player.addr)
        self.players[player] = self.totalPlayers
        self.totalPlayers = self.totalPlayers + 1
        self.SendTotalPlayers()
        player.Send({"action":    "add_player",
                     "player_id": self.players[player]})
        self.SendToOthers(player,{"action":    "add_enemy_player",
                                  "player_id": self.players[player]})


    def AddEnemyPlayers(self, player):
        for p in self.players:
            if p != player:
                player.Send({"action":    "add_enemy_player",
                             "player_id": self.players[p]})


    def DeletePlayer(self, player):
        print "Deleting player" + str(player.addr)
        self.SendToOthers(player,{"action":    "remove_enemy_player",
                                  "player_id": self.players[player]})
        del self.players[player]
        self.totalPlayers = self.totalPlayers - 1
        self.SendTotalPlayers()


    def SendTotalPlayers(self):
        self.SendToAll({"action":       "number_of_players",
                        "player_count": self.totalPlayers})


    def SendToAll(self, data):
        [p.Send(data) for p in self.players]


    def SendToOthers(self, player, data):
        for p in self.players:
            if p != player:
                p.Send(data)

                
if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "host:port"
    print "e.g.", sys.argv[0], "localhost:31425"
else:
    host, port = sys.argv[1].split(":")
    gameServer = GameServer(localaddr=(host, int(port)))
    while True:
        gameServer.Pump()
        sleep(0.0001)
