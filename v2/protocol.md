# Protocol V2
all strings are UTF-8 encoded
## HANDSHAKE
server sends the server name to the client
client sends the client name to the server
server adds the client name to the list of online_clients
if client disconnects server removes name from list of online_clients