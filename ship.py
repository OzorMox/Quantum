import sys, math, pygame

class Ship:
    def __init__(self, x, y):
        self.THRUST         = 35.0
        self.MAX_SPEED      = 800.0
        self.ROTATION_SPEED = 300.0
        self.GRAVITY        = 5.0
        
        self.positionX = x
        self.positionY = y
        self.rotation  = 0.0
        self.velocityX = 0.0
        self.velocityY = 0.0


    def load(self, drawManager):
        self.texture = drawManager.loadImage("ship.png")
        self.rect = self.texture.get_rect()


    def update(self, gameTime):
        speed = 0.0
        speed = math.sqrt((self.velocityX * self.velocityX) + (self.velocityY * self.velocityY))

        if (speed > self.MAX_SPEED):
            self.velocityX *= self.MAX_SPEED / speed
            self.velocityY *= self.MAX_SPEED / speed
            
        self.velocityY -= self.GRAVITY

        self.positionX -= self.velocityX * gameTime
        self.positionY -= self.velocityY * gameTime

        self.rect.x = self.positionX
        self.rect.y = self.positionY

        
    def updateInput(self, gameTime, key):
        thrust = self.THRUST
        
        if key[pygame.K_RIGHT]:
            self.rotation -= (self.ROTATION_SPEED * gameTime)
        if key[pygame.K_LEFT]:
            self.rotation += (self.ROTATION_SPEED * gameTime)
        if key[pygame.K_UP]:
            self.velocityX += thrust*math.sin(self.rotation*(math.pi/180.0))
            self.velocityY += thrust*math.cos(self.rotation*(math.pi/180.0))
        #if key[pygame.K_SPACE]:
			#self.fire()

            
    def draw(self, drawManager, camera):
        texture = pygame.transform.rotate(self.texture, self.rotation)
        tempRect = texture.get_rect()
        tempRect.center = self.rect.center
        tempRect.x -= (camera.x - (drawManager.getScreenWidth() / 2)) + (self.rect.width / 2)
        tempRect.y -= (camera.y - (drawManager.getScreenHeight() / 2)) + (self.rect.height / 2)
        drawManager.draw(texture, tempRect)


	#def fire():
		#Fire bullet


    def getX(self):
        return self.positionX


    def setX(self, x):
        self.positionX = x


    def getY(self):
        return self.positionY


    def setY(self, y):
        self.positionY = y


    def getVelocityX(self):
        return self.velocityX


    def setVelocityX(self, x):
        self.velocityX = x

    
    def getVelocityY(self):
        return self.velocityY


    def setVelocityY(self, y):
        self.velocityY = y


    def getRotation(self):
        return self.rotation


    def setRotation(self, rotation):
        self.rotation = rotation;
