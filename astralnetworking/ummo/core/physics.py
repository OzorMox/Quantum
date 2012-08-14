def input_left(self):
    self.facing = 2
    self.ax = -1
def input_right(self):
    self.facing = 0
    self.ax = 1
def input_up(self):
    self.facing = 1
    self.ay = -1
def input_down(self):
    self.facing = 3
    self.ay = 1

def actor_move(self,commands):
    self.ax = 0
    self.ay = 0
    for c in commands:
        f = globals().get("input_"+c,None)
        if f:
            f(self)
    self.vx += self.ax*self.ar
    if not self.ax:
        if self.vx<0:
            self.vx+=self.dr
        elif self.vx>0:
            self.vx-=self.dr
        if abs(self.vx-self.dr)<self.clamp:
            self.vx = 0
    if self.vx<-self.maxspeed:
        self.vx=-self.maxspeed
    if self.vx>self.maxspeed:
        self.vx=self.maxspeed
    self.vy += self.ay*self.ar
    if not self.ay:
        if self.vy<0:
            self.vy+=self.dr
        elif self.vy>0:
            self.vy-=self.dr
        if abs(self.vy-self.dr)<self.clamp:
            self.vy = 0
    if self.vy<-self.maxspeed:
        self.vy=-self.maxspeed
    if self.vy>self.maxspeed:
        self.vy=self.maxspeed
    self.x += self.vx
    self.y += self.vy