An Astral Networking Tutorial
-----------------------------

We will be making a simple networked game using astral. 
The concepts will be useful for just about 
any multiplayer game.
I have decided pong is a good example,
because it has enough action to stress the network,
and is really simple to implement.

Several things before we start though. Multiplayer programming
is difficult. Even if you have a magic library (which astral networking has
not yet become), 
the way you think about your game, 
your mainloop, 
and the way objects in your game interact just aren't the same as
in a single player game.

Each player will have a slightly different view of the world,
but you want each player to feel like
all of the other players and objects
are interacting inside his own machine.

It would be tempting to just make your game as normal,
and then try and add some stuff to network some of the commands,
and expect it to work OK.
This is not the case! 
Proper networked games must be built to fit a networked environment,
and it will help us to think a little bit about our game before
we start coding to structure things in a way that makes our lives
a bit easier when we enter the hairy but fun world of multiplayer interactions.



Concepts
.............

First let's clarify some concepts in multiplayer programming,
especially as they are understood in Astral's design.


Client-Server Architecture
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Astral is designed around a client-server archtecture. 
In an ideal world, the entire game would be run on a single machine,
which is the server.



Let's code!
...............


Step One: The game of Pong
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

If you don't know what pong is, check out `this video <http://www.youtube.com/watch?v=LPkUvfL8T1I>`_

Lets go over what is necessary to make a game that is a clone of pong. 
What objects need to be there?
How do they interact?
This may seem a bit trite or simplistic, 
especially if you have made a simple game before,
but when networking it is useful to be analytical about even the simplest elements.

The barest requirements for pong are two paddles, one per player, and a ball.
The ball will constantly be moving, and should change directions when it hits a wall or a paddle.

The ball physics will be simple:
it will reverse it's y velocity when it hits a horizontal obstruction,
and reverse it's x velocity when it hits a vertical obstruction.

Horizontal obstructions will be the top and bottom edges of the screen.
Vertical obstructions will be the left and right edges of the screen,
and the player paddles.

A player will hold down the up key to move his paddle up,
and hold down the down key to move his paddle down.

Each player has a score.
When the ball bounces off the left side of the screen,
player 1 gets a point.
When the ball bounces off the right side of the screen,
player 2 gets a point.

That's it. You could end the game after a certain amount of points, 
have more ball physics,
or other things. But here we aren't going to go past that.

Now that we understand pong, let's see if we can understand networked pong.


Step Two: Net Pong
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Who owns what? This is an important question. When writing a typical game, 
you don't really need to think about this. Everything is running on one computer,
you could think about how the player controls some objects, and the ai
controls others, but it's not really the same. 

With network simulation, and with 2 player networked pong, you have at least
3 different contexts. Player 1 is running a computer, player 2 is running a computer,
and the server is running yet another computer. While the 3 computers
in this example may be running copies of the same code, they are all running
unique instances of it. It's important to think about the game elements and
who is ultimately in charge.

The server will be mostly in charge of it all. With client-server architecture, this is
what you would expect. The ball physics will not be run on the players' computers
at all.

It makes sense that the **paddles** are owned by the players. They control
them after all. Player 1 will own his paddle, and player 2 will own his. We wouldn't
want player 1 to move player 2's paddle - that would be cheating! However, there
are certain bounds that even player1 should not move his paddle.
So he is still not fully in control.

Another thing to consider with network simulation, is the initial and ending states.
With a single context, you just add all of the objects and start it up, and maybe
check for an ending condition and handle from there. Here, we have to think
about it more carefully. When the server is started, there are no players playing,
so we can't add the paddles and the ball and just start it going! Players would
connect and see a game in progress with some very inactive paddles.

That is if we have the server run independant of the players. Another option is for player 1
to start the game which acts as a server and a client, and have player 2 connect to him. This
is what we will be using. So how to start the game?

We will start it with a player 1 paddle and a ball. We will not start the ball moving until player 2
joins, which is when we add the player 2 paddle. We might also want to wait for a tiny
bit after the connection so the players aren't too surprised.

I'm also going to make connection really simple. For a real game you want to do a better job here.
When you run netpong.py, it will ask if you are player 1 or player 2. Player 1 will host the server,
and connect to his own server; player 2 will just connect to player 1's server. The server will listen
at localhost on port 1111.

Step Three: Player 1 paddle
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

So let's make the initial server with a player paddle. We wont be able to see anything
until the next step, where we make the client. In general, clients display stuff but dont
do much, and servers do do much but don't generate displays.

First, make a file netpong.py. You should be able to import astral and subclass 
astral.server.gameserver.GameServer. The server class will have a registry where 
objects can be placed, and already knows how to manage client connections and syncing
things up. ::

    from astral.server.gameserver import GameServer
    class NetpongServer(GameServer):
        pass
    
First, we will want to make sure the server creates a paddle for player 1 when he starts the server.
Well, really he is going to create a server, create a client, and then connect to the server. The server
will do some checks, and then will need some way to know when to create his paddle. Some games could
implement a username/password system, but we will not be that secure. Still, we may want to look
at how the server determines who is let on or not.

The GameServer class has several functions which are called after an event. One of the events
defined by Astral is "msg_authenticate". By default, this will reject players
from connecting if the server is already full.

Speaking of the server being full, how do we control how many people can play at once? Easy,
there is a server attribute called "max_players". We should probably set this to 2, 
our version of pong isn't going to support more than 2 players. Feel free to make a version
that does if you want to experiment later!

You can set server attributes or do other initialization by writing an init() method. This method
is called, surprisingly, after the server has been initialized. ::

    from astral.server.gameserver import GameServer
    class NetpongServer(GameServer):
        def init(self):
            self.max_players = 2
        
Now if a 3rd player tries to connect he will be rejected.

We will also need an object to represent a paddle. It will have an x and a y value, and a width and a height.
This object is going to be the **server** representation of it. The server will know about
everything in netpong. The score, the ball, and the paddles.

Most server objects are called Mobs. This stands for "movable object". You should subclass this to get your
paddle::

    from astral.server import elements
    class Paddle(elements.Mob):
        pass
    
Mobs need to be able to be copied from one computer to another. We need to give our paddle some attributes
and tell it which ones to send to the clients. Mobs, like the GameServer, also have an init() function run
when they are created::

    class ServerPaddle(elements.Mob):
        def init(self):
            super(ServerPaddle,self).init()
            self.x = 0
            self.y = 0
            self.width = 15
            self.height = 126
            self.template = "paddle"
            self.values += ["x","y","width","height"]
            
Paddle.values is a list of all attributes which should be synced across machines. The base object is already smart
enough to know that it can interpolate the x and the y values, and that the width and height don't need
to be sent all the time since they won't be changing. But it's nice to know that if we wanted to change
the height of the paddle during the game, we could, and all players would see the change.

It would be nice to make a paddle for the player when he joins, would it not? When a player joins a
server, it automatically calls self.player_joined(player). The player object will have some information
about his ip address etc. Let's add a paddle to our server, and assign it to our player, when he joins::

    class NetpongServer(GameServer):
        def init(self):
            self.max_players = 2
        def player_joined(self,player):
            p = Paddle()                                   #make paddle
            self.objects.add(p)                           #add paddle to our world
            player.owns_object(p)             #assign object key to player object so we know what the player owns
            
Objects is an astral registry, which is a subclass of a dictionary with some convenience functions. When an object
is added, it is assigned a unique id. These are crucial to ensure that the state of the world remains
consistent across computers.

The player object also has a set of object keys he controls, called 'actors'. When player input comes in, it is
only applied to objects with these keys. So in the last line of player_joined, we assign the paddle to the player.
This command will also broadcast the key of the paddle to the client so that it knows what objects it is
intended to control as well.


Step Four: Client
,,,,,,,,,,,,,,,,,,,,,,,

Before we do too much more, we should code a client so that we can actually see what's going on and test
that the game is working. The client should subclass astral.client.gameclient.GameClient. Just like GameServer,
it has an init() function that is run when the client is first made. For now we are going to set predict_owned
to False. Client-side prediction is a bit tricky to set up so we are going to add it later. If predict_owned is
True, network objects that the player owns (remember player.actors from the last step?) will not have their
properties automatically controlled by the server.::

    from astral.client.gameclient import GameClient
    class NetpongClient(GameClient):
        def init(self):
            self.predict_owned = False
            
We also need the client-side version of the paddle that we previously created on the server. There is a
client-side version of mob to inherit from in astral.client.local. We will inherit from that for the paddle. When the
server sends the world state to the client, the client needs to know what kind of object to create. Our
server version of paddle used a template attribute, but the client needs to know what to do with that template.
We do that by assigning our client-side Paddle class to a dictionary called remote_classes.::

    from astral.client import local
    class ClientPaddle(local.Mob):
        def init(self):
            self.template = "paddle"    #We don't really need to set this but it will help with testing

    from astral.client.gameclient import GameClient
    class NetpongClient(GameClient):
        def init(self):
            self.predict_owned = False
            self.remote_classes["Paddle"] = ClientPaddle
            
When the client is connected, the server will send it a world state containing Mobs. When the client sees a
mob with the template "paddle", it will see from self.remote_classes that it needs to create a ClientPaddle
object to represent it. This ClientPaddle will automatically be updated according to the properties we
set in the ServerPaddle object, namely the x, y, width, and height values.

Now we should set up a display so that we can see what's going on in the game. We are going to use
pygame for the display and the control input, but astral is in no way tied to pygame. For the display
itself, we will simply loop through all of the client objects and draw them using the pygame.draw functions.

As this is not a pygame tutorial, I won't be going into detail about the rest of this code. The important part
is how it deals with the server and/or client. I'll be making a Game class which stores either the server
and the client in player 1's case, or just the client in player 2's case. Here's the entire pygame section
of the code.::

    import pygame
    
    class Game(object):
        def __init__(self):
            self.server = None
            self.client = NetpongClient()
            self.screen = pygame.display.set_mode([640,480])
            self.clock = pygame.time.Clock()
            self.running = True
        def draw(self):
            self.screen.fill([0,0,0])
            for mob in self.client.objects.values():    #Iterate through client object dictionary
                if mob.template=="paddle":
                    pygame.draw.rect(self.screen,[255,255,255],[[mob.x,mob.y],[mob.width,mob.height]])
            pygame.display.flip()
        def input(self):
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    self.running = False
        def update(self):
            self.dt = self.clock.tick(30)
            self.draw()
            self.input()
        def run(self):
            while self.running:
                self.update()
                
To actually get a game started and running, we can add Game().run() to the bottom of our script. We
will get a black window that can be closed. Not very exciting is it? Let's just add some paddles to see that
the draw function is working::

    netpong = Game()
    paddle = ClientPaddle()
    paddle.x = 10
    paddle.y = 20
    paddle.width = 20
    paddle.height = 100
    netpong.client.objects.add(paddle)
    netpong.run()
    
Now when you run the game, you will see a paddle! Yay! Too bad it is fake. Time to set up the client-server
connection and get a game actually running.


Step Five: Connecting
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Here we are going to handle setting up a server to listen for connections, setting up a client, connecting
the two, and updating the world every frame. It sounds like a lot, but it amounts to less than 10 lines
of code! Delete the test code at the end of the file which made the fake paddle, and lets start filling
out our game class some more.

First, connection. When the game starts, we need to ask which player is running the game. Lets do this 
in the game's __init__ function. If they press '1', we will make a NetpongServer object, if they press '2'
we will set self.server to None. When we add the server, let's also start it hosting. astral's GameServer
has a method 'host' which does this.

The three arguments to server.host are the ip address, the port number, and the adapter to use. 
The adapter knows how to take message data that is easy to work with, and convert it into a form
that can travel across the network. Adapters are provided for the Mastermind networking library,
the podsixnet library, and pyenet. I like to use podsixnet for testing.

We will also tell the client to connect to the server, and send the 'announce'. The 'announce' is where
the client should give some information to the server to help the server know how to set him up.
This could be sending a player's name or account information, or sending a choice of character type,
or anything else really. Here we are not going to send anything. The server will know which player is
which based on connect order. ::

    class Game(object):
        def __init__(self):
            self.player_number = raw_input("Are you player '1' or player '2'")
            if self.player_number=="1":
                self.server.host("127.0.0.1",1111,"podsixnet")   #Host the server
            else:
                self.server = None
            self.client = NetpongClient()
            self.client.connect("127.0.0.1",1111,"podsixnet")
            self.client.announce({})
            self.screen = pygame.display.set_mode([640,480])
            self.clock = pygame.time.Clock()
            self.running = True
            
Then we need to change the update function to ensure that both the client and the server (if we are
running a server - i.e. if we are player 1) are updating and listening for messages being sent back and
forth. 

Try to run the game. Choose '1', and the game will begin.
Hey look at that, it's drawing a paddle! The ServerPaddle we coded at the beginning
is being added to the Server when the player connects. The client, during it's listen(), will get the state
of all the objects the server knows about, including that ServerPaddle we created.

Next we need to make it so the player can control the paddle.


Step Six: Input
,,,,,,,,,,,,,,,,,,,,

Edit the Game input function to send actions to the server when keys are pressed::

    def input(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                self.running = False
                
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.client.buffer_action("down")
        if keys[pygame.K_UP]:
            self.client.buffer_action("up")
            
Edit the ServerPaddle and add a new method process_input::

    def process_input(self,time,data):
        if "down" in data:
            self.y += 20
            if self.y>480-self.height:
                self.y=480-self.height
        if "up" in data:
            self.y -= 20
            if self.y<0:
                self.y = 0
                
Step Seven: Ball
,,,,,,,,,,,,,,,,,,,,,,

Now we need to make a ball - a server version::

    class ServerBall(elements.Mob):
        def init(self):
            super(ServerBall,self).init()
            self.x = 320
            self.y = 240
            self.width = 10
            self.height = 10
            self.template = "ball"
            self.vx = 1
            self.vy = random.choic([-1,1])
            self.speed = 5
            self.values += ["x","y","width","height"]
        def update(self,server):
            self.x += self.vx*self.speed
            self.y += self.vy*self.speed
            
We need to create the ball when player 1 joins::
    
    #In NetpongServer
    def player_joined(self,player):
        p = ServerPaddle()
        self.objects.add(p)
        player.owns_object(p)
        self.objects.add(ServerBall())      #Create a ball and add it to the objects
        print "player joined"
        
The client does not know what to do with the template = "ball". Let's make a client version
of the ball, and add a section in the draw function to draw it::

    #Client-side ball class
    class ClientBall(local.Mob):
        def init(self):
            self.template = "ball"
    
    #Updated NetpongClient, add the new ball class to the remote_classes
    class NetpongClient(GameClient):
        def init(self):
            self.predict_owned = False
            self.remote_classes["paddle"] = ClientPaddle
            self.remote_classes["ball"] = ClientBall
    
    #Updated Game.draw function
    def draw(self):
        self.screen.fill([0,0,0])
        for mob in self.client.objects.values():
            if mob.template=="paddle":
                pygame.draw.rect(self.screen,[255,255,255],[[mob.x,mob.y],[mob.width,mob.height]])
            #How to draw the ball is the same as the paddle, just a rectangle. Lets make it blue for fun
            elif mob.template=="ball":
                pygame.draw.rect(self.screen,[100,100,255],[[mob.x,mob.y],[mob.width,mob.height]])
        pygame.display.flip()
        
On starting the game as player 1, you should see the ball moving to the right, either right-up or right-down.
Time to add bouncing! ::

    def update(self,server):
        #Save last position
        ox = self.x
        oy = self.y
        
        self.x += self.vx*self.speed
        self.y += self.vy*self.speed
        
        #Record whether we hit something and on which side we did
        hitright = hitleft = hitup = hitdown = 0
        
        #Scan through paddles
        for p in server.objects.values():
            if p.template=="paddle":
                if self.vx<0 and self.x<p.x+p.width and ox+self.width>p.x+p.width and self.y>=p.y and self.y+self.height<p.y+p.height:
                    hitleft = 1
                    self.x=p.x+p.width
                elif self.vx>0 and self.x+self.width>p.x and ox<p.x and self.y>=p.y and self.y<p.y+p.height:
                    hitright = 1
                    self.x=p.x-self.width

        #Detect collision with walls. Later hitting left and right wall should yield appropriate score
        if self.x>=630:
            hitright = 1
        if self.x<=0:
            hitleft = 1
        if self.y>=470:
            hitdown = 1
        if self.y<=0:
            hitup = 1
        
        #Change the direction of movement for a bounce
        if hitright:
            self.vx = -1
        if hitleft:
            self.vx = 1
        if hitdown:
            self.vy = -1
        if hitup:
            self.vy = 1
            
We almost have a game! But it's kind of only one player right now. We never added logic on the server to make a player
2 paddle in the correct spot.


