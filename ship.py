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


    def update(self, gameTime, key):
        thrust = 1000.0
        
        if key[pygame.K_RIGHT]:
            self.rotation -= 0.5
        if key[pygame.K_LEFT]:
            self.rotation += 0.5
        if key[pygame.K_UP]:
            self.velocityX += thrust*math.sin(self.rotation*(math.pi/180.0))
            self.velocityY += thrust*math.cos(self.rotation*(math.pi/180.0))

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
        
        
        if self.rect.x < 0:
            self.rect.x = 800
        if self.rect.x > 800:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 600
        if self.rect.y > 600:
            self.rect.y = 0
        
            
    def draw(self, screen):
        texture = pygame.transform.rotate(self.texture, self.rotation)
        texture.get_rect().center = self.rect.center
        screen.blit(texture, self.rect)
