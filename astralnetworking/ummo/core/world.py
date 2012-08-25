import pygame
import random
import os
from agents import *
import client
import server

class World(object):
    def __init__(self,engine):
        self.engine = engine
        self.objects = []
        self.off = [0,0]
        self.start()
    def add(self,o):
        self.objects.append(o)
    def start(self):
        """Override"""
    def update(self):
        self.sprites = []
        for o in self.objects:
            o.update(self)
            if o.visible:
                self.sprites.append(o)
    def draw(self):
        [s.draw(self.engine,self.off) for s in self.sprites]
    def input(self,controller):
        pass
            
class Button(Agent):
    def set_title(self,text,font):
        self.text = text
        surf = font.render(text,1,[255,255,255])
        self.graphics = self.surface = pygame.Surface([surf.get_width()+4,surf.get_height()+4])
        self.graphics.blit(surf,[2,2])
        return self
        
class Interface(object):
    def __init__(self,world):
        self.world = world
        self.world.input = self.input
    def hit_button(self,p):
        for o in self.world.objects:
            if isinstance(o,Button):
                if o.rect().collidepoint([p[0]//2,p[1]//2]):
                    return o.text.lower()
    def input(self,c):
        click = c.mouse_left_clicked()
        if click:
            action = self.hit_button(click)
            if action:
                self.action(action)
        if hasattr(self.world,"client"):
            if c.check_state(("key",pygame.K_a)):
                self.world.client.buffer_action("left")
            if c.check_state(("key",pygame.K_d)):
                self.world.client.buffer_action("right")
            if c.check_state(("key",pygame.K_s)):
                self.world.client.buffer_action("down")
            if c.check_state(("key",pygame.K_w)):
                self.world.client.buffer_action("up")
            if c.check_state(("key",pygame.K_SPACE))=="down":
                self.world.client.shoot()
    def action(self,action):
        getattr(self.world,"action_"+action)()

mode="podsixnet"
class host_or_connect(World):
    def start(self):
        self.add(Agent("art/bg/grassbleh.png"))
        self.add(Button(pos=[25,25]).set_title("Host",self.engine.font))
        self.add(Button(pos=[25,45]).set_title("Connect",self.engine.font))
        self.gui = Interface(self)
    def setup_server(self):
        self.engine.server = server.UMMOServer()
    def setup_client(self):
        self.engine.client = client.UMMOClient()
    def connect_client_to_server(self,ip=None,port=None):
        if not ip:
            ip,port = open("servers.txt").read().split("\n")[0].split(":")
            port = int(port)
        self.engine.client.connect(ip,port,mode)
        self.engine.client.announce()
        print "starting up"
    def action_host(self):
        ip,port = open("servers.txt").read().split("\n")[0].split(":")
        port = int(port)
        self.setup_server()
        self.setup_client()
        self.engine.world = ServerClientRunner(self.engine)
        self.engine.server.host(ip,port,mode)
        self.connect_client_to_server(ip,port)
    def action_connect(self):
        self.setup_client()
        self.engine.world = ClientRunner(self.engine)
        self.connect_client_to_server()
        
def apply_networked_to_agents(owner,world,tag="client"):
    def key(k):
        return tag+"_"+k
    keys = {}
    for mob in owner.objects.values():
        if mob.template == "UMMOMob" and not hasattr(mob,"agent"):
            mob.agent = PlayerCharacter()
            mob.agent.tag = tag
            mob.agent.key = key(mob.key)
            world.add(mob.agent)
            if getattr(mob,"is_owned",False):
                hb = HealthBar()
                hb.set_parent(mob)
                world.add(hb)
        if hasattr(mob,"agent"):
            keys[key(mob.key)] = 1
            mob.agent.set_state(mob.__dict__)
    for agent in world.objects[:]:
        if hasattr(agent,"key") and agent.key.startswith(tag+"_") and not agent.key in keys:
            world.objects.remove(agent)
            if hasattr(agent,"healthbar"):
                world.objects.remove(agent.healthbar)

def update_camera(client,world):
    if client.owned and client.owned[0] in client.objects:
        o = client.objects[client.owned[0]]
        world.off = [o.x-100,o.y-100]
        
class ServerClientRunner(World):
    """Runs both a server and a client. Some input
    controls the server, other input controls the client. Can draw server's world, clients world, or both"""
    def start(self):
        self.server = self.engine.server
        self.client = self.engine.client
        self.client.msg_connected = self.msg_connected
        self.server.msg_error = self.smsg_error
        self.gui = Interface(self)
    def smsg_error(self,value):
        self.engine.world = host_or_connect(self.engine)
        self.engine.world.start()
        self.engine.world.add(Button(pos=[25,0]).set_title("(Hosting error - same port?)",self.engine.font))
        self.engine.world.update()
    def msg_connected(self):
        self.add(Button(pos=[0,0]).set_title("disconnect",self.engine.font))
    def update(self):
        self.server.update()
        self.client.listen()
        super(ServerClientRunner,self).update()
        apply_networked_to_agents(self.client,self)
        update_camera(self.client,self)
        apply_networked_to_agents(self.server,self,"server")
    def action_disconnect(self):
        self.client.disconnect()
        self.server.disconnect()
        self.engine.world = host_or_connect(self.engine)
        self.engine.world.start()
        self.engine.world.add(Button(pos=[25,0]).set_title("(Player quit)",self.engine.font))
        self.engine.world.update()
        
class ClientRunner(World):
    """Runs a client connected to an external server"""
    def start(self):
        self.client = self.engine.client
        self.client.msg_error = self.msg_error
        self.client.msg_connected = self.msg_connected
        self.client.msg_disconnected = self.msg_disconnected
        self.gui = Interface(self)
    def update(self):
        self.client.listen()
        super(ClientRunner,self).update()
        apply_networked_to_agents(self.client,self)
        update_camera(self.client,self)
    def msg_error(self,value):
        self.engine.world = host_or_connect(self.engine)
        self.engine.world.start()
        self.engine.world.add(Button(pos=[25,0]).set_title("(Connection failed: %s)"%value,self.engine.font))
        self.engine.world.update()
    def msg_connected(self):
        self.add(Button(pos=[0,0]).set_title("disconnect",self.engine.font))
    def msg_disconnected(self):
        self.client.disconnect()
        self.engine.world = host_or_connect(self.engine)
        self.engine.world.start()
        self.engine.world.add(Button(pos=[25,0]).set_title("(Server lost)",self.engine.font))
        self.engine.world.update()
    def action_disconnect(self):
        self.client.disconnect()
        self.engine.world = host_or_connect(self.engine)
        self.engine.world.start()
        self.engine.world.add(Button(pos=[25,0]).set_title("(Player quit)",self.engine.font))
        self.engine.world.update()
