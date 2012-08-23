import sys, pygame, audio
import ship

class Quantum:
    def __init__(self):
        pygame.init()    
        self.ship = ship.Ship()
        size = width, height = 1024, 768
        self.screen = pygame.display.set_mode(size)
        self.lastTime = pygame.time.get_ticks()


    def load(self):
        self.ship.load()
        audio.play()
        
        
    def run(self):
        while 1:
            self.update()
            self.draw()


    def update(self):
        time = pygame.time.get_ticks()
        gameTime = (time - self.lastTime) / 1000.0

        self.updateInput(gameTime)

        self.lastTime = pygame.time.get_ticks()
        

    def updateInput(self, gameTime): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
                
        key = pygame.key.get_pressed()
        
        self.ship.update(gameTime, key)


    def draw(self): 
        black = 0, 0, 0
        
        self.screen.fill(black)
        self.ship.draw(self.screen)
        pygame.display.flip()


quantum = Quantum()
quantum.load()
quantum.run()
