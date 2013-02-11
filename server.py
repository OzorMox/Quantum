from time import sleep
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def Network(self, data):
        print data


    def Network_updateplayer(self, data):
        self._server.SendToOthers(self, data)


    def Close(self):
        self._server.DeletePlayer(self)


class GameServer(Server):
    channelClass = ClientChannel
    totalPlayers = 0

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print "Server Launched"


    def Connected(self, channel, addr):
        print "New connection:", channel
        self.AddPlayer(channel)
        self.AddEnemyPlayers(channel)

        
    def AddPlayer(self, player):
        print "New Player" + str(player.addr)
        self.players[player] = self.totalPlayers
        self.totalPlayers = self.totalPlayers + 1
        self.SendTotalPlayers()
        player.Send({"action": "addplayer", "player_id": self.players[player]})
        self.SendToOthers(player,{"action":"addenemyplayer", "player_id": self.players[player]})


    def AddEnemyPlayers(self, player):
        for p in self.players:
            if p != player:
                player.Send({"action":"addenemyplayer", "player_id": self.players[p]})


    def DeletePlayer(self, player):
        print "Deleting Player" + str(player.addr)
        del self.players[player]
        self.totalPlayers = self.totalPlayers - 1
        self.SendTotalPlayers()


    def SendTotalPlayers(self):
        self.SendToAll({"action": "numplayers", "player_count": self.totalPlayers})


    def SendToAll(self, data):
                [p.Send(data) for p in self.players]


    def SendToOthers(self, player, data):
        for p in self.players:
            if p != player:
                p.Send(data)
                

host = "127.0.0.1"
port = 3000
gameServer = GameServer(localaddr=(host, int(port)))
while True:
    gameServer.Pump()
    sleep(0.0001)
