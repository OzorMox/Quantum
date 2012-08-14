import sys;sys.path.append("..")
from astral.server.gameserver import GameServer
import random

class NetpongServer(GameServer):
    def init(self):
        self.max_players = 2
    def player_joined(self,player):
        p = ServerPaddle()                                   #make paddle
        self.objects.add(p)                           #add paddle to our world
        player.owns_object(p)             #assign object key to player object so we know what the player owns
        self.objects.add(ServerBall())
        print "player joined"

from astral.server import elements
class ServerPaddle(elements.Mob):
    def init(self):
        super(ServerPaddle,self).init()
        self.x = 0
        self.y = 0
        self.width = 15
        self.height = 126
        self.template = "paddle"
        self.values += ["x","y","width","height"]
    def process_input(self,time,data):
        if "down" in data:
            self.y += 20
            if self.y>480-self.height:
                self.y=480-self.height
        if "up" in data:
            self.y -= 20
            if self.y<0:
                self.y = 0
class ServerBall(elements.Mob):
    def init(self):
        super(ServerBall,self).init()
        self.x = 320
        self.y = 240
        self.width = 10
        self.height = 10
        self.template = "ball"
        self.vx = 1
        self.vy = random.choice([-1,1])
        self.speed = 5
        self.values += ["x","y","width","height"]
    def update(self,server):
        ox = self.x
        oy = self.y
        
        self.x += self.vx*self.speed
        self.y += self.vy*self.speed
        hitright = hitleft = hitup = hitdown = 0
        for p in server.objects.values():
            if p.template=="paddle":
                if self.vx<0 and self.x<p.x+p.width and ox+self.width>p.x+p.width and self.y>=p.y and self.y+self.height<p.y+p.height:
                    hitleft = 1
                    self.x=p.x+p.width
                elif self.vx>0 and self.x+self.width>p.x and ox<p.x and self.y>=p.y and self.y<p.y+p.height:
                    hitright = 1
                    self.x=p.x-self.width

        if self.x>=630:
            hitright = 1
        if self.x<=0:
            hitleft = 1
        if self.y>=470:
            hitdown = 1
        if self.y<=0:
            hitup = 1
            
        if hitright:
            self.vx = -1
        if hitleft:
            self.vx = 1
        if hitdown:
            self.vy = -1
        if hitup:
            self.vy = 1

from astral.client import local
class ClientPaddle(local.Mob):
    def init(self):
        self.template = "paddle"
class ClientBall(local.Mob):
    def init(self):
        self.template = "ball"

from astral.client.gameclient import GameClient
class NetpongClient(GameClient):
    def init(self):
        self.predict_owned = False
        self.remote_classes["paddle"] = ClientPaddle
        self.remote_classes["ball"] = ClientBall
            
import pygame

class Game(object):
    def __init__(self):
        self.player_number = raw_input("Are you player '1' or player '2'? ")
        if self.player_number=="1":
            self.server = NetpongServer()
            self.server.host("127.0.0.1",1111,"podsixnet")
        else:
            self.server = None
        self.client = NetpongClient()
        self.client.connect("127.0.0.1",1111,"podsixnet")
        self.client.announce({})
        self.screen = pygame.display.set_mode([640,480])
        self.clock = pygame.time.Clock()
        self.running = True
    def draw(self):
        self.screen.fill([0,0,0])
        for mob in self.client.objects.values():    #Iterate through client object dictionary
            if mob.template=="paddle":
                pygame.draw.rect(self.screen,[255,255,255],[[mob.x,mob.y],[mob.width,mob.height]])
            elif mob.template=="ball":
                pygame.draw.rect(self.screen,[100,100,255],[[mob.x,mob.y],[mob.width,mob.height]])
        pygame.display.flip()
    def input(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.client.buffer_action("down")
        if keys[pygame.K_UP]:
            self.client.buffer_action("up")
    def update(self):
        if self.server:
            self.server.update()
        self.client.listen()
        self.dt = self.clock.tick(30)
        self.draw()
        self.input()
    def run(self):
        while self.running:
            self.update()

netpong = Game()
netpong.run()