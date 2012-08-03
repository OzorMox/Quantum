import sys, pygame, audio

class Quantum:
    def __init__(self):
        pygame.init()
        size = width, height = 1024, 768
        self.screen = pygame.display.set_mode(size)


    def load(self):                
        self.ship = pygame.image.load("ship.png")
        self.shiprect = self.ship.get_rect()
        audio.play()

        
    def run(self):
        while 1:
            self.update()
            self.draw()


    def update(self):
        self.updateInput()


    def updateInput(self):
        speed = [1, 1]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
                
        key = pygame.key.get_pressed()
        
        if key[pygame.K_DOWN]:
            speed = [0, 1]
            self.shiprect = self.shiprect.move(speed)
        if key[pygame.K_RIGHT]:
            speed = [1, 0]
            self.shiprect = self.shiprect.move(speed)
        if key[pygame.K_UP]:
            speed = [0, -1]
            self.shiprect = self.shiprect.move(speed)
        if key[pygame.K_LEFT]:
            speed = [-1, 0]
            self.shiprect = self.shiprect.move(speed)


    def draw(self): 
        black = 0, 0, 0
        
        self.screen.fill(black)
        self.screen.blit(self.ship, self.shiprect)
        pygame.display.flip()


quantum = Quantum()
quantum.load()
quantum.run()
