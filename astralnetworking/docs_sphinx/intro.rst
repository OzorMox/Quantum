What is Astral Networking?
--------------------------

Astral Networking is a package containing tools to help aid in the creation of
networked games or simulations. In some ways it resembles a framework, 
and in others it is more of a library. 

Features
............

* Abstract messaging interface built on a number of lower level libraries
* Client-server architecture
* Client code and server code separated - encourages clean design
* Can share functions between the client and the server where it makes sense
* Syncronization of objects between client and server
* Client-side prediction so players get smooth response of their actions
* World state owned by server to prevent cheating

What can I use astral networking for?
..................................................

* Turn based games such as chess
* Chat clients
* multiplayer action games
* mmos?


It was developed to be independant from any
particular graphics library, and is able to use a wide variety of lower level
networking libraries to send messages back and forth.

Networked Simulation Concepts
..........................................
* Server
* Clients
* Connection
* Disconnection
* Messages
* Syncronization