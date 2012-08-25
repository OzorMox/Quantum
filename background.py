import sys, math, pygame

class Background:
    def __init__(self):
        self.positionX = 0
        self.positionY = 0

    def load(self):
        self.texture = pygame.image.load("background.png")
        self.rect = self.texture.get_rect()

            
    def draw(self, screen, camera):
        self.texture.get_rect().center = self.rect.center
        tempRect = pygame.Rect.copy(self.rect)
        tempRect.x -= camera.x
        tempRect.y -= camera.y
        screen.blit(self.texture, tempRect)
