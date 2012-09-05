import sys, math, pygame

class Ship:
    def __init__(self):
        self.THRUST         = 35.0
        self.MAX_SPEED      = 800.0
        self.ROTATION_SPEED = 300.0
        self.GRAVITY        = 5.0
        
        self.positionX = 0.0
        self.positionY = 0.0
        self.rotation  = 0.0
        self.velocityX = 0.0
        self.velocityY = 0.0


    def load(self):
        self.texture = pygame.image.load("ship.png")
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

            
    def draw(self, screen, camera):
        texture = pygame.transform.rotate(self.texture, self.rotation)
        tempRect = texture.get_rect()
        tempRect.center = self.rect.center
        tempRect.x -= (camera.x - (screen.get_width() / 2)) + (self.rect.width / 2)
        tempRect.y -= (camera.y - (screen.get_height() / 2)) + (self.rect.height / 2)
        screen.blit(texture, tempRect)


	#def fire():
		#Fire bullet
