import sys, math, pygame

class Ship:
    def __init__(self):
        self.MAX_SPEED = 300.0
        self.positionX = 0.0
        self.positionY = 0.0
        self.rotation = 0.0
        self.velocityX = 0.0;
        self.velocityY = 0.0;


    def load(self):
        self.texture = pygame.image.load("ship.png")
        self.rect = self.texture.get_rect()


    def update(self, gameTime):
        speed = 0.0
        speed = math.sqrt((self.velocityX * self.velocityX) + (self.velocityY * self.velocityY))

        if (speed > self.MAX_SPEED):
            self.velocityX *= self.MAX_SPEED / speed
            self.velocityY *= self.MAX_SPEED / speed

        self.velocityX *= gameTime
        self.velocityY *= gameTime

        self.positionX -= self.velocityX;
        self.positionY -= self.velocityY;

        self.rect.x = self.positionX
        self.rect.y = self.positionY

        
    def updateInput(self, gameTime, key):
        thrust = 1000.0
        
        if key[pygame.K_RIGHT]:
            self.rotation -= (100.0 * gameTime)
        if key[pygame.K_LEFT]:
            self.rotation += (100.0 * gameTime)
        if key[pygame.K_UP]:
            self.velocityX += thrust*math.sin(self.rotation*(math.pi/180.0))
            self.velocityY += thrust*math.cos(self.rotation*(math.pi/180.0))

            
    def draw(self, screen, camera):
        texture = pygame.transform.rotate(self.texture, self.rotation)
        texture.get_rect().center = self.rect.center
        tempRect = self.rect;
        tempRect.x -= (camera.x - (screen.get_width() / 2)) + (self.rect.width / 2)
        tempRect.y -= (camera.y - (screen.get_height() / 2)) + (self.rect.height / 2)
        screen.blit(texture, tempRect)
