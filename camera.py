import sys
import config, ship


class Camera:
    ship = None
    
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

        
    def setTarget(self, target):
        self.ship = target


    def update(self):
        if (self.ship):
            if (self.ship.positionX > 0) and (self.ship.positionX < (config.MAP_WIDTH - config.VIEWPORT_WIDTH)):
                self.x = self.ship.positionX
            
            if (self.ship.positionY > 0) and (self.ship.positionY < (config.MAP_HEIGHT - config.VIEWPORT_HEIGHT)):
                self.y = self.ship.positionY
