All strings are UTF-8 encoding

Server opens on port 5555
Server waits for a client to connect and then starts the handshake.
server sends string of a dictionary of online players to the client.
server waits for a response from the client of what player they want to be "cyan" or "yellow".
server initiates connection forks thread and starts again for client 2.


Currently there is no way for the server or client to gracefully quit, maybe I am just stupid but I cant figure it out 🤷‍♂️
