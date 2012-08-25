import pygame

class Controller:
    def __init__(self,engine):
        self.engine = engine
        self.state = {}
        self.mb_pos = None
    def input(self):
        engine = self.engine
        pygame.event.pump()
        for k in self.state.keys():
            if self.state[k]=="down":
                self.state[k]="held_down"
            elif self.state[k]=="up":
                del self.state[k]
        for e in pygame.event.get():
            if e.type==pygame.ACTIVEEVENT:
                if e.gain==0 and (e.state==6 or e.state==2 or e.state==4):
                    print "minimize"
                    self.engine.pause()
                if e.gain==1 and (e.state==6 or e.state==2 or e.state==4):
                    print "maximize"
                    self.engine.unpause()
            elif e.type==pygame.VIDEORESIZE:
                w,h = e.w,e.h
                engine.swidth = w
                engine.sheight = h
                engine.make_screen()
            elif e.type == pygame.QUIT:
                self.engine.stop()
            elif e.type==pygame.KEYDOWN and\
            e.key==pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                engine.fullscreen = 1-engine.fullscreen
                engine.make_screen()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                self.state[("mouse",e.button)] = "down"
                self.mb_pos = e.pos
            elif e.type==pygame.MOUSEBUTTONUP:
                self.state[("mouse",e.button)] = "up"
            elif e.type==pygame.KEYDOWN:
                self.state[("key",e.key)] = "down"
            elif e.type==pygame.KEYUP:
                self.state[("key",e.key)] = "up"
        if engine.world:
            engine.world.input(self)
    def check_state(self,state):
        if state in self.state:
            return self.state[state]
    def mouse_left_clicked(self):
        if self.check_state(("mouse",1))=="down":
            return self.mb_pos