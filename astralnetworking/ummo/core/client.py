import sys
sys.path.append("..")
import astral.client.gameclient as gc
import astral.client.local as local
import physics

class UMMOMob(local.Mob):
    template = "UMMOMob"
    def init(self):
        super(UMMOMob,self).init()
        self.prediction_func = physics.actor_move
        self.add_property(local.NetworkedProperty("facing",predicted=True,interpolation="one"))
        self.add_property(local.NetworkedProperty("health",predicted=False,interpolation="linear"))
        for p in ["vx","vy","ax","ay"]:
            self.add_property(local.NetworkedProperty(p,predicted=True))
        self.max_buffer = 2
        
class Bullet(UMMOMob):
    def init(self):
        super(Bullet,self).init()
        self.prediction_func = self.up
        self.max_buffer = 2
    def up(self,self2,commands):
        self.x+=self.vx
        self.y+=self.vy

class UMMOClient(gc.GameClient):
    remote_classes = globals()
    def __init__(self,*args,**kwargs):
        super(UMMOClient,self).__init__(*args,**kwargs)
        #self.predict_owned = False
        self.keep_updates = 20
        #self.update_rate = 1
        self.interpolation_rate = 0.02
        self.rate_skew = 4
        self.shooting = 0
    def shoot(self):
        self.send({"action":"shoot","client_tick":self.update_count,"cid":str(id(self))})
        self.shooting = 1
        bullet = Bullet(str(id(self)))
        bullet.sprite="art/particle/bullet.png"
        bullet.facing = self.objects[self.owned[0]].facing
        bullet.vx,bullet.vy = {0:[32,0],1:[0,-32],2:[-32,0],3:[0,32]}[bullet.facing]
        bullet.x=self.objects[self.owned[0]].x+1.2*bullet.vx
        bullet.y=self.objects[self.owned[0]].y+1.2*bullet.vy
        if bullet.key not in self.owned:
            self.owned.append(bullet.key)
        bullet.sticky = True
        bullet.use_prediction = True
        self.objects.add(bullet)
    def tick(self):
        #Can't move while in shoot animation
        if self.shooting:
            self.shooting -= 1
    def buffer_action(self,action):
        if self.shooting:
            return
        return super(UMMOClient,self).buffer_action(action)
    def update_objects(self):
        if self.shooting:
            return
        return super(UMMOClient,self).update_objects()