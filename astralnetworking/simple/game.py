from astral.server.gameserver import GameServer as GS
from astral.client.gameclient import GameClient as GC
from astral.server import elements
from astral.client import local
import conf
import random
import time

class State:
    """Baseclass for a simple State object. States can be drawn to the screen, and read
    input to do various things. They also keep a reference to the gameclient in order
    to interface with it."""
    def __init__(self,gc):
        """Initialize the state, and remember the gameclient who created us"""
        self.gc = gc
    def draw(self,screen):
        """Draw to the screen."""
        pass
    def input(self):
        """Read input and do stuff."""
        pass
        
import pygame
pygame.init()
pygame.font.init()
f = pygame.font.SysFont("arial",12)
        
class ConnectState(State):
    """This state is like a menu before the game has connected. It may
    show a choice of servers to connect to, or have further options
    for the player before they are connected. In this game, it just
    demonstrates states and protocol a little bit"""
    def __init__(self,gc):
        self.gc = gc
        self.error = None
    def draw(self,screen):
        """Just a simple draw telling the player to press enter"""
        s = screen
        s.blit(f.render("Press enter to connect.",1,[255,255,255]),[0,0])
        if self.error:
            s.blit(f.render(self.error,1,[255,255,255]),[0,50])
    def msg_error(self,value):
        self.error = "CONNECTION FAILURE!"
    def input(self):
        """If the player hits enter, run gameclient.connect, which opens the actual
        connection to the server, and then gameclient.announce, which formally tells 
        the server we want to log in. A more advanced login process might
        pass a username and password with announce()"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.gc.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.error = "trying to connect...."
                self.gc.connect(conf.HOST,conf.PORT,conf.LIBRARY)
                self.gc.announce()
                
class ChooseCharState(State):
    """A state after login with the server is complete, but before the player
    is officially in the game. In a fps type game, it might let you chat with 
    other players before the game starts. In an mmorpg it might show you
    available characters to choose. In this game, it lets you enter what
    name you want to be known by."""
    name = ""
    def draw(self,screen):
        """Show the players name as it's being entered."""
        s = screen
        s.blit(f.render("Enter a name:"+self.name,1,[255,255,255]),[0,0])
    def input(self):
        """Letter keys to add to the name, press enter to call the choosecharacter
        function on the server, which also sends the name we have chosen. The
        server will record that name, and then start filling us in about the
        actual game state."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.gc.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                self.gc.send({"action":"choosecharacter","name":self.name})
            elif e.type == pygame.KEYDOWN:
                self.name += str(e.unicode)

class ConnectedState(State):
    """This is the meat and potatoes. This state is the actual running game. It
    draws a local representation of the world, and handles passing input to
    manipulate objects and chat. The bulk of the game logic should be
    in the object classes, but drawing and input happen here."""
    key = ""
    entered = ""
    def draw(self,screen):
        """For this simple example, displays each player's name at their location
        in the world. Also shows the last 5 messages in the message log."""
        s = screen
        s.blit(f.render("Connected. /quit to disconnect /name [name] to rename",1,[255,255,255]),[0,0])
        #Draw all objects
        for o in self.gc.objects.all():
            s.blit(f.render(o.name,1,[255,255,255]),[o.x,o.y])
        #Draw 3 lines of chat at bottom, along with the chat entry line
        s.blit(f.render("speak>"+self.entered,1,[255,200,200]),[0,220])
        y = 170
        for m in self.gc.message_log.messages[-5:]:
            s.blit(f.render(m["source"]+"> "+m["message"],1,[255,255,255]),[0,y])
            y += 10
    def input(self):
        """Handles chat input, and passes directional keys to the rest of the
        system with gameclient.buffer_action. The resuls of those actions
        are processed on the client side through prediction, and then repeated
        on the server side."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.gc.running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if self.entered == "/quit":
                    self.gc.disconnect()
                    self.gc.state = ConnectState(self.gc)
                elif self.entered.startswith("/name "):
                    self.gc.set_name(self.entered.split(" ",1)[1])
                    self.entered = ""
                else:
                    self.gc.send({"action":"user_chat","message":self.entered})
                    self.entered = ""
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
                self.entered = self.entered[:-1]
            elif e.type == pygame.KEYDOWN:
                self.entered += e.unicode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.gc.buffer_action("right")
        if keys[pygame.K_LEFT]:
            self.gc.buffer_action("left")
        if keys[pygame.K_UP]:
            self.gc.buffer_action("up")
        if keys[pygame.K_DOWN]:
            self.gc.buffer_action("down")
        if keys[pygame.K_c]:
            print self.gc.update_count-self.gc.server_update_count
            self.gc.objects[self.gc.owned[0]].y = 0
        
class GameClient(GC):
    """The GameClient is the master of all client-side networking. The baseclass
    handles most of the nitty gritty work, such as state replication, and how to
    apply inputs to objects. When we subclass GameClient, we can add 
    "msg_*" methods, in order to build on the protocol and customize it to our
    game. This simple gameclient has a game state which it defers to for
    drawing and input operations. As the player moves through the different
    modes, the state will be changed."""
    def __init__(self):
        """Create the GameClient, and start with the ConnectState"""
        self.state = ConnectState(self)
        GC.__init__(self)
    def draw(self,screen):
        """Defer to self.state for drawing"""
        self.state.draw(screen)
    def input(self):
        """Defer to self.state for input"""
        self.state.input()
    def msg_error(self,value):
        if hasattr(self.state,"msg_error"):
            self.state.msg_error(value)
    def msg_authenticated(self,value):
        """The server has told us we have successfully logged in. (Simple game
        doesn't use a username or password, so it always works). Since we
        have logged in, we should change the game state to ChooseCharState
        so the player can choose their character (which in simple game is just
        entering a name to use)"""
        self.state = ChooseCharState(self)
        self.state.key = str(self.client_key)
    def msg_disconnected(self):
        """The server has kicked us out (or we have disconnected some other way.)
        Change to ConnectState, so that we can log in again and play some more."""
        super(GameClient,self).msg_disconnected()
        if not isinstance(self.state,ConnectState):
            self.state = ConnectState(self)
    def msg_characterchosen(self):
        """The character chosen was accepted by the server (which is always true
        in simplegame). Move to the ConnectedState, where the game will
        actually take place."""
        self.state = ConnectedState(self)
    def create_local(self,key,state):
        """The create_local method builds a local instance of an object that exists
        on the server. We will get a key which helps to identify the object, and the first
        state of that object which might need to be used to determine how to create
        it.
        
        All local instances in simple game are clients, which are controlled by other
        players. So we will always use the LocalClient class to create them. Also,
        if the object is the object THIS player is supposed to be controlling, we 
        want to turn on prediction for the local instance."""
        m = LocalClient(key)
        m.use_prediction = key in self.owned
        return m
    def set_name(self,name):
        """Tell the server to change our name"""
        self.send({"action":"set_name","name":name})
        
def mob_input(self,data):
    """This function is used on the server, as well as the client when an object
    is using prediction, to apply input to an object. Data is a list of input commands.
    In simplegame, the only commands are 'right','left','up','down', and each command
    will move the object by 4 pixels in those directions."""
    if "right" in data:
        self.x += 4
    if "left" in data:
        self.x -= 4
    if "up" in data:
        self.y -= 4
    if "down" in data:
        self.y += 4

class MovingMob(elements.Mob):
    """This is the baseclass for character objects
    on the server side. It's update function is to play any
    inputs it has received from it's owner according to the 
    same mob_input function that is used on the client 
    side."""
    def init(self):
        """Initialize the MovingMob. When creating a new object type in astral,
        you will typically subclass elements.Mob. In the init(), after calling
        init on the superclass, and initializing whatever new attributes you need,
        you will need to add the name of each attribute which you want to be
        reproduced on clients to the list self.values.
        
        For simple game, we want other clients to be able to know our name. So
        we make sure this object has a self.name attribute, and call
            self.values.append("name")
        to ensure that that attribute will be synced to all clients."""
        self.template = "LocalClient"
        super(MovingMob,self).init()
        self.name = "X"
        self.values.append("name")  #Make sure the name attribute is networked
    def process_input(self,time,data):
        """What happens to the object for a given timestep, called for each
        set of inputs at a specific rate determined by the server update rate.
        - using the same mob_input function that clients use for prediction. 
        
        Also, when someone moves off the screen, we put them to the other side, like
        some oldschool games do. Since normally objects on client-side are interpolated
        from one position to the next, this is a good situation to test forcing them to warp
        to a new location without smoothly transitioning."""
        mob_input(self,data)
        if self.x<0:
            self.x += 320
            self.warp()
        if self.x>320:
            self.x -= 320
            self.warp()
        if self.y<0:
            self.y += 240
            self.warp()
        if self.y>240:
            self.y -= 240
            self.warp()
        
class LocalClient(local.Mob):
    """The baseclass for character objects on the client side. The only difference
    this has versus the local.Mob class, is that we set the prdiction_func to be the 
    same movement function that the server uses to move the object."""
    def init(self):
        """Set self.prediction_func to be the same function the server uses to move
        objects. This will make prediction accurate. The prediction function is only run
        for objects which THIS client owns, and it is run INSTEAD of interpolating
        from states that the server sends. If this function doesn't match the way
        the server moves objects, then the clients view of the world will be a lie."""
        super(LocalClient,self).init()
        self.prediction_func = mob_input
        
class GameServer(GS):
    """This is the master class for running the server. The base gameserver class
    handles the nitty gritty things, like replicating state to clients, and keeping track
    of who is logged in. In most games, you subclass that, and then add "msg_*"
    methods to handle new protocols that your game may require."""
    def msg_choosecharacter(self,name):
        """The player has chosen a character and is ready to enter the world. First we
        need to create a character object for them, and assign it to their player object.
        We also set the character's name. Finally, we tell the player that they are ok to 
        start rendering the game, and announce to the log to welcome them."""
        pc = self.objects.add(MovingMob())
        self.current_player.owns_object(pc)
        pc.name = name
        self.current_player.name = name
        self.current_player.send({"action":"characterchosen"})
        self.message_log.system_announce("Welcome "+name,self.current_player.addr)
    def msg_user_chat(self,message):
        """A player has sent a chat message. Add it to our log, which also
        transparently will replicate to client logs."""
        self.message_log.user_chat(self.current_player.name,message)
    def msg_set_name(self,name):
        """Change the players name to [name]. Rely on normal replication code
        to actually get that information to clients."""
        for okey in self.current_player.actors:
            self.objects[okey].name = name