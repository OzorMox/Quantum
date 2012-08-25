"""Spawn a client, using data from conf for ip and port, and using the logic from game.py
Also passes in the screen. Perhaps it would be better if the screen were created in game too"""

import conf

import sys
if len(sys.argv)>1:
    conf.HOST = sys.argv[1]
if len(sys.argv)>2:
    conf.PORT = sys.argv[2]
if len(sys.argv)>3:
    conf.LIBRARY = sys.argv[3]
    
import game

import pygame
import time

client1 = game.GameClient()

screen = pygame.display.set_mode([320,240])
clock = pygame.time.Clock()

running = True
while client1.running and __name__=="__main__":
    dt = clock.tick()
    if dt>0:
        pygame.display.set_caption("%s"%(1/(dt/1000.0)))
    screen.fill([0,0,0])
    client1.listen()
    client1.input()
    client1.draw(screen)
    pygame.display.flip()