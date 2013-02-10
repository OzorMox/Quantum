import pygame
import config

class DrawManager:
    def __init__(self):
        pygame.init()
        size = width, height = config.VIEWPORT_WIDTH, config.VIEWPORT_HEIGHT
        self.screen = pygame.display.set_mode(size)


    def loadImage(self, imageName):
        return pygame.image.load(imageName)


    def getScreenWidth(self):
        return self.screen.get_width()


    def getScreenHeight(self):
        return self.screen.get_height()
    

    def draw(self, texture, bounds):
        self.screen.blit(texture, bounds)

               
    def close(self):
        pygame.quit()
