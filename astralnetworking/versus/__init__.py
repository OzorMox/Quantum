"""This is a simple game demonstrating all of astral's features. It contains the basics of almost
everything that a multiplayer game needs, but not much more than that.

The player is given the choice to connect, then they are able to pick a name, and finally
are able to play the game. If disconnected, rather than crashing, the login screen is shown
again, allowing them to reconnect.

In the game, the player's character (in astral, the player object is separate from the character
object) is represented by the name they chose when connecting. They are able to use
the arrow keys to move around the screen - which shows their nametag moving around. If
other players are logged in, they will see their nametags at their respective positions.

On the client, prediction is turned on, so that movements are instant and feel very smooth
and responsive. Other player object's are displayed at positions which are interpolated over
the last known position received from the server. The actual movement is lagged a bit, in
order to keep movement smooth and not jerky. There are some controls in astral for other games
that might want to balance things a little differently, such as having less acuracy but more
responsiveness.

Finally, there is a simple chat log implemented as well.

The code is fairly straightforward, with most of the problem areas of multiplayer programming
hidden away. However the complexity of having a separate server and client, which share
some code (especially for prediction) is still accessible. There are plenty of comments, so
it should not be too difficult to understand how it is set up.

Server and client are best run from the command line:
    python run_server.py 127.0.0.1
        and
    python run_client.py 127.0.0.1
    
Alternately, you can edit conf.py to change the ip and port to connect with. You can also try
to switch from the PodSixNet backend to the Mastermind backend, but it is not as solid.
You can run multiple clients at once to simulate many players.
"""