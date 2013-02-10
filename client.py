from time import sleep
from PodSixNet.Connection import connection, ConnectionListener
import world

class Client(ConnectionListener):
    def __init__(self, host, port, world):
        self.Connect((host, port))
        self.playerId = -1
        self.world = world
        print "Client started"
        

    def Network_connected(self, data):
        print "You are now connected to the server"


    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    
    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()
        

    def Network_addplayer(self, data):
        print "adding player!"
        
        self.playerId = data["player_id"]
        self.world.addPlayer(400, 400)
        

    def Network_addenemyplayer(self, data):
        print "adding enemy player!"
        
        playerId = data["player_id"]
        self.world.addEnemy(playerId, 500, 400)


    def Network_updateplayer(self, data):
        print data
        playerId = data["player_id"]
        x = data["x"]
        y = data["y"]
        velocityX = data["velocityX"]
        velocityY = data["velocityY"]
        rotation = data["rotation"]
        
        self.world.updateEnemy(playerId, x, y, velocityX, velocityY, rotation)


    def Network_numplayers(self, data):
        print "Total players: ", data["player_count"]


    def UpdateShip(self):
        if self.playerId > -1:
            playerShip = self.world.getPlayerShip()
            connection.Send({"action":    "updateplayer",
                             "player_id": self.playerId,
                             "x":         playerShip.getX(),
                             "y":         playerShip.getY(),
                             "velocityX": playerShip.getVelocityX(),
                             "velocityY": playerShip.getVelocityY(),
                             "rotation":  playerShip.getRotation()})

    def Loop(self):
        self.UpdateShip()
        connection.Pump()
        self.Pump()
