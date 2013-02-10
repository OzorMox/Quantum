import sys, math, pygame
import drawmanager

class Background:
    def __init__(self):
        self.positionX = 0
        self.positionY = 0


    def load(self, drawManager):
        self.texture = drawManager.loadImage("background.png")
        self.rect = self.texture.get_rect()

            
    def draw(self, drawManager, camera):
        self.texture.get_rect().center = self.rect.center
        tempRect = pygame.Rect.copy(self.rect)
        tempRect.x -= camera.x
        tempRect.y -= camera.y
        drawManager.draw(self.texture, tempRect)
