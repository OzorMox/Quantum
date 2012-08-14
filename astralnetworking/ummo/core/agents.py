import pygame
import math
import random

memory = {}
class Agent(object):
    def __init__(self,art=None,pos=None,rot=None):
        if not pos:
            pos = [0,0]
        if not rot:
            rot = [1,0]
        self.graphics = None
        self.surface = None
        self.pos = pos
        self.rot = rot
        self.art = art
        self.hotspot = [0,0]
        self.rotation_on_rot = True
        self.visible = True
    def load(self,art=None):
        if not art:
            art = self.art
        if not art in memory:
            memory[art] = pygame.image.load(art).convert()
            memory[art].set_colorkey([255,0,255])
        self.graphics = memory[art]
        self.surface = self.graphics
        return self
    def update(self,world):
        if self.rotation_on_rot and self.surface:
            ang = math.atan2(-self.rot[1],self.rot[0])*180.0/math.pi
            self.surface = pygame.transform.rotate(self.graphics,ang)
    def draw(self,engine,offset):
        if not self.surface and self.art:
            self.load()
        engine.surface.blit(self.surface,[self.pos[0]-self.hotspot[0]-offset[0],self.pos[1]-self.hotspot[1]-offset[1]])
    def rect(self):
        if not self.surface:
            return pygame.Rect([[0,0],[0,0]])
        r = self.surface.get_rect()
        r = r.move(self.pos[0]-self.hotspot[0],self.pos[1]-self.hotspot[1])
        return r
        
class PlayerCharacter(Agent):
    """Visual representation of a player character"""
    def set_state(self,state):
        """Convert from networked object state to graphical state"""
        if "facing" in state:
            self.facing = state['facing']
        if 'x' in state:
            self.pos[0] = state['x']
        if 'y' in state:
            self.pos[1] = state['y']
        if 'sprite' in state:
            self.load(state['sprite'])
    def draw(self,engine,offset):
        down = self.surface.subsurface([[0,0],[32,32]])
        up = self.surface.subsurface([[32,0],[32,32]])
        right = self.surface.subsurface([[64,0],[32,32]])
        left = pygame.transform.flip(right,1,0)
        surfs = [right,up,left,down]
        surf = surfs[int(self.facing)]
        if self.tag == "server":
            surf.set_alpha(50)
        engine.surface.blit(surf,[self.pos[0]-self.hotspot[0]-offset[0],self.pos[1]-self.hotspot[1]-offset[1]])

class HealthBar(Agent):
    def set_parent(self,ob):
        self.ob = ob
        ob.healthbar = self
        self.pos = [0,220]
    def draw(self,engine,off):
        self.surface = self.graphics = pygame.Surface([320,20])
        pygame.draw.rect(self.surface,[255,0,0],[[0,0],[(self.ob.health/100.0)*320,20]])
        #~ if self.tag == "server":
            #~ self.surface.set_alpha(50)
        super(HealthBar,self).draw(engine,off)