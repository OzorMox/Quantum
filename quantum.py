import sys, pygame, audio
import ship

class Quantum:
    def __init__(self):
        pygame.init()    
        self.ship = ship.Ship()
        size = width, height = 1024, 768
        self.screen = pygame.display.set_mode(size)


    def load(self):
        self.ship.load()
        audio.play()
        
        
    def run(self):
        while 1:
            self.update()
            self.draw()


    def update(self):
        self.updateInput()


    def updateInput(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
                
        key = pygame.key.get_pressed()
        
        self.ship.update(key)


    def draw(self): 
        black = 0, 0, 0
        
        self.screen.fill(black)
        self.ship.draw(self.screen)
        pygame.display.flip()


quantum = Quantum()
quantum.load()
quantum.run()
