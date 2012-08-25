import sys, pygame, audio
import background, camera, config, ship


class Quantum:
    def __init__(self):
        pygame.init()
        size = width, height = config.VIEWPORT_WIDTH, config.VIEWPORT_HEIGHT
        self.screen = pygame.display.set_mode(size)

        self.background = background.Background()
        self.ship = ship.Ship()
        self.camera = camera.Camera()

        self.lastTime = pygame.time.get_ticks()


    def load(self):
        self.background.load()
        self.ship.load()
        self.camera.setTarget(self.ship)

        audio.play()
        
        
    def run(self):
        clock = pygame.time.Clock()
        
        while 1:
            time = pygame.time.get_ticks()
            gameTime = (time - self.lastTime) / 1000.0

            self.updateInput(gameTime)
            self.update(gameTime)
              
            self.lastTime = pygame.time.get_ticks()

            self.draw()

            clock.tick(30)

    def update(self, gameTime):
        self.ship.update(gameTime)
        self.camera.update()


    def updateInput(self, gameTime): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
                
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            sys.exit()

        self.ship.updateInput(gameTime, key);


    def draw(self): 
        black = 0, 0, 0
        
        self.screen.fill(black)
        
        self.background.draw(self.screen, self.camera)
        self.ship.draw(self.screen, self.camera)
        
        pygame.display.flip()


quantum = Quantum()
quantum.load()
quantum.run()
