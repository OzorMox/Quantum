import sys, audio, pygame
import world, drawmanager, client

class Quantum:
    def __init__(self, host, port, playerName):
        self.drawManager = drawmanager.DrawManager()
        self.world = world.World()
        self.client = client.Client("192.168.0.5", 3000, playerName, self.world)
        self.lastTime = pygame.time.get_ticks()

        
    def load(self):
        self.world.load(self.drawManager)

        
    def run(self):
        exitGame = False
        
        clock = pygame.time.Clock()
        
        while not exitGame:   
            time = pygame.time.get_ticks()
            gameTime = (time - self.lastTime) / 1000.0

            self.client.Loop()

            exitGame = self.update(gameTime)
            
            self.lastTime = pygame.time.get_ticks()

            self.draw()
            
            clock.tick(30) #limits framerate to 30 fps

        self.close()


    def update(self, gameTime):

        exitGame = self.world.updateInput(gameTime)
        self.world.update(gameTime)

        return exitGame
    

    def draw(self):    
        self.world.draw(self.drawManager)
        pygame.display.flip()
        
        
    def close(self):
        self.drawManager.close()

if len(sys.argv) != 3:
    print "Usage:", sys.argv[0], "host:port user"
    print "e.g.", sys.argv[0], "localhost:31425 bob"
else:
    host, port = sys.argv[1].split(":")
    playerName = sys.argv[2]
    
    quantum = Quantum(host, port, playerName)
    quantum.load()
    quantum.run()
