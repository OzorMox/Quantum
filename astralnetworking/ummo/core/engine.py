import pygame

def fit(surf,size):
    surf = pygame.transform.scale(surf,size)
    return surf

class Engine:
    def __init__(self):
        self.fullscreen = False
        self.swidth = 640
        self.sheight = 480
        self.iwidth = 320
        self.iheight = 240
        self.window = None
        self.surface = None
        self.blank = None
        self.running = False
        self.paused = False
        self.framerate = 60
        self.dt = 0
        self.show_fps = True
        self.clock = None
        self.world = None
        self.next_tick = 0.0
    def start(self):
        """Separate from __init__ in case we want to make the object before making the screen"""
        pygame.init()
        self.make_screen()
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("fonts/vera.ttf",12)
    def stop(self):
        self.running = False
    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
    def update(self):
        """One tick, according to dt"""
        self.next_tick += self.dt
        if self.world:
            while self.next_tick>0:
                self.next_tick -= 1
                self.world.update()
    def make_screen(self):
        flags = pygame.RESIZABLE|pygame.FULLSCREEN*self.fullscreen
        self.window = pygame.display.set_mode([self.swidth,self.sheight],flags)
        self.surface = pygame.Surface([self.iwidth,self.iheight]).convert()
        self.blank = self.surface.convert()
        self.blank.fill([0,0,0])
        pygame.display.set_icon(pygame.image.load("art/icons/ico.png"))
        if pygame.joystick.get_init():
            pygame.joystick.quit()
        pygame.joystick.init()
        pygame.js1 = None
        if pygame.joystick.get_count():
            pygame.js1 = pygame.joystick.Joystick(0)
            pygame.js1.init()
        def gl():
            return pygame.js1 and pygame.js1.get_numhats() and pygame.js1.get_hat(0)[0]<0
        def gr():
            return pygame.js1 and pygame.js1.get_numhats() and pygame.js1.get_hat(0)[0]>0
        def gu():
            return pygame.js1 and pygame.js1.get_numhats() and pygame.js1.get_hat(0)[1]>0
        def gd():
            return pygame.js1 and pygame.js1.get_numhats() and pygame.js1.get_hat(0)[1]<0
        self.jsleft = gl
        self.jsright = gr
        self.jsup = gu
        self.jsdown = gd
    def clear_screen(self):
        self.surface.blit(self.blank,[0,0])
    def draw_screen(self):
        showfps = self.show_fps
        self.window.fill([10,10,10])
        def draw_segment(dest,surf,pos,size):
            rp = [pos[0]*self.swidth,pos[1]*self.sheight]
            rs = [size[0]*self.swidth,size[1]*self.sheight]
            surf = fit(surf,rs)
            dest.blit(surf,rp)
        draw_segment(self.window,self.surface,[0,0],[1,1])
        if showfps:
            self.window.blit(self.font.render(str(self.clock.get_fps()),1,[0,0,0]),[0,self.window.get_height()-12])
        pygame.display.flip()