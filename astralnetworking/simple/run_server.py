"""Spawn a server, using data from conf for ip and port, and using the logic from game.py
Doesn't really need a pygame screen, but it might if we want to display things later"""

import conf
import game

import sys
if len(sys.argv)>1:
    conf.HOST = sys.argv[1]
if len(sys.argv)>2:
    conf.PORT = sys.argv[2]
if len(sys.argv)>3:
    conf.LIBRARY = sys.argv[3]

import pygame
import time
import os

server = game.GameServer()
server.host(conf.HOST,conf.PORT,conf.LIBRARY)

try:
    screen = pygame.display.set_mode([640,240])
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    screen = pygame.display.set_mode([640,240])
left = screen.subsurface([[0,0],[320,240]])
right = screen.subsurface([[320,0],[320,240]])
clock = pygame.time.Clock()

while server.running and __name__=="__main__":
    dt = clock.tick()
    if dt>0:
        pygame.display.set_caption("%s"%(1/(dt/1000.0)))
    screen.fill([0,0,0])
    server.update()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            print "cancelling server looping"
            server.running = False
    pygame.display.flip()
