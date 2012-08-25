import sys
sys.path.append("..")
import astral.server.gameserver as gs
import astral.server.elements as stuff

import physics

class UMMOMob(stuff.Mob):
    def init(self):
        super(UMMOMob,self).init()
        self.facing = 0  #0=right, 1=up, 2=left, 3=down
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.ar = 1
        self.dr = 1
        self.maxspeed = 5
        self.clamp = 0.3
        self.health = 100
        self.sprite = "art/char/man.png"
        self.values += ["facing","sprite","vx","vy","ax","ay","maxspeed","ar","dr","clamp","health"]
        self.template = "UMMOMob"
    def process_input(self,time,commands):
        physics.actor_move(self,commands)
    def update(self,server):
        super(UMMOMob,self).update(server)
        for key in server.objects.keys():
            if key == self.key:
                continue
            ob = server.objects[key]
            if ob.sprite=="art/particle/bullet.png":
                if ob.x+16>=self.x and ob.x+16<=self.x+32:
                    if ob.y+16>=self.y and ob.y+16<=self.y+32:
                        self.health -= 5
                        ob.kill = 1
        if self.health<0:
            self.health=0
        if self.health>100:
            self.health=100
            
class Bullet(stuff.Mob):
    def init(self):
        super(Bullet,self).init()
        self.facing = 0  #0=right, 1=up, 2=left, 3=down
        self.vx = 0
        self.vy = 0
        self.ar = 1
        self.dr = 1
        self.maxspeed = 5
        self.clamp = 0.3
        self.health = 100
        self.ttl = 10
        self.sprite = "art/char/man.png"
        self.sticky = 0
        self.values += ["facing","sprite","vx","vy","maxspeed","ar","dr","clamp","health","sticky"]
        self.template = "UMMOMob"
    def update(self,server):
        super(Bullet,self).update(server)
        self.x += self.vx
        self.y += self.vy
        self.ttl -= 1
        if self.ttl<0:
            self.kill = 1

class UMMOServer(gs.GameServer):
    def init(self):
        super(UMMOServer,self).init()
        self.max_players = 2
    def authenticate(self,player):
        super(UMMOServer,self).authenticate(player)
        pc = UMMOMob()
        pc.x = 100
        if len(self.players)==1:
            pc.y = 20
        else:
            pc.y = 120
        self.objects.add(pc)
        player.owns_object(pc)
        bullet = Bullet()
        bullet.x = 100
        bullet.sprite="art/particle/bullet.png"
        self.objects.add(bullet)
    #~ def msg_authenticate(self,data):
        #~ """Only allow 2 players."""
        #~ self.current_player.init()
        #~ self.authenticate(self.current_player)
    def msg_shoot(self,client_tick,cid):
        for k in self.current_player.actors:
            o = self.objects[k]
            if getattr(o,"shooting",False):
                return
            o.shooting = client_tick
            o.shoot_cid = cid
    def update_sim(self):
        for o in self.objects.all():
            #An object is requesting to shoot
            if getattr(o,"shooting",False):
                small = None
                for t in self.state_history:
                    if not small or t[0]<small:
                        small = t[0]
                    #The time the object shot was at this time
                    if t[0]==o.shooting:
                        o.shooting = False
                        state = t[1]
                        #Oops, object did not actually exist then
                        if o.key not in state:
                            break
                        ostate = state[o.key]
                        bullet = Bullet()
                        bullet.x = ostate['x']
                        bullet.y = ostate['y']
                        bullet.vx,bullet.vy = {0:[32,0],1:[0,-32],2:[-32,0],3:[0,32]}[ostate['facing']]
                        bullet.x+=1.2*bullet.vx
                        bullet.y+=1.2*bullet.vy
                        bullet.facing = ostate['facing']
                        bullet.sprite="art/particle/bullet.png"
                        bullet.key = o.shoot_cid
                        self.objects.add(bullet)