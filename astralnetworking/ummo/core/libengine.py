import sys,os
import time
import engine
import controller
import world
import pickle
if sys.platform=="win32":
    os.environ['SDL_VIDEODRIVER']='windib'
import random
import time

try:
    import android
except:
    android = None
    
engine = engine.Engine()
controller = controller.Controller(engine)

def run():
    engine.running = True
    engine.start()
    engine.world = world.host_or_connect(engine)
    
    
    lt = time.time()
    ticks = 0
    fr = 0
    engine.screen_refresh = 1
    engine.next_screen = engine.screen_refresh

    while engine.running:
        engine.dt = engine.clock.tick(getattr(engine,"framerate",30))
        engine.dt = min(engine.dt*.001*60,100.0)
        engine.update()
        engine.next_screen -= engine.dt
        if engine.next_screen < 0:
            engine.clear_screen()
            engine.world.draw()
            engine.draw_screen()
            engine.next_screen = engine.screen_refresh
        controller.input()
    print "quit"