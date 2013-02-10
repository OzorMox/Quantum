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

        # audio.play()
        
        
    def run(self):
        exitGame = False
        
        clock = pygame.time.Clock()
        
        while not exitGame:
            time = pygame.time.get_ticks()
            gameTime = (time - self.lastTime) / 1000.0

            exitGame = self.updateInput(gameTime)
            self.update(gameTime)
              
            self.lastTime = pygame.time.get_ticks()

            self.draw()

            clock.tick(30) #limits framerate to 30 fps

        self.close()
        
    def update(self, gameTime):
        self.ship.update(gameTime)
        self.camera.update()


    def updateInput(self, gameTime):
        exitGame = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True
                
        key = pygame.key.get_pressed()
        
        if key[pygame.K_ESCAPE]:
            exitGame = True
            
        self.ship.updateInput(gameTime, key);
        
        return exitGame;

    def draw(self): 
        black = 0, 0, 0
        
        self.screen.fill(black)
        
        self.background.draw(self.screen, self.camera)
        self.ship.draw(self.screen, self.camera)
        
        pygame.display.flip()


    def close(self):
        pygame.quit()


quantum = Quantum()
quantum.load()
quantum.run()
