import sys, audio, pygame
import background, camera, ship

class World:    
    def __init__(self):
        self.background = background.Background()
        self.camera = camera.Camera()
        self.enemies = {}


    def load(self, drawManager):
        self.drawManager = drawManager
        self.background.load(self.drawManager)

        # audio.play()
        

    def addPlayer(self, x, y):
        self.ship = ship.Ship(x, y)
        self.ship.load(self.drawManager)
        self.camera.setTarget(self.ship)
    

    def addEnemy(self, playerId, x, y):
        enemy = ship.Ship(x, y)
        enemy.load(self.drawManager)
        self.enemies[playerId] = enemy


    def updateEnemy(self, playerId, x, y, velocityX, velocityY, rotation):
        enemy = self.enemies[playerId]
        enemy.setX(x);
        enemy.setY(y);
        enemy.setVelocityX(velocityX)
        enemy.setVelocityY(velocityY)
        enemy.setRotation(rotation)


    def update(self, gameTime):
        self.ship.update(gameTime)
        for e in self.enemies:
            self.enemies[e].update(gameTime)
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


    def draw(self, drawManager):
        self.background.draw(drawManager, self.camera)
        self.ship.draw(drawManager, self.camera)
        for e in self.enemies:
            self.enemies[e].draw(drawManager, self.camera)


    def getPlayerShip(self):
        return self.ship
