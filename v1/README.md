All strings are UTF-8 encoding

Server opens on port 5555
Server waits for a client to connect and then starts the handshake.
server sends string of a dictionary of online players to the client.
server waits for a response from the client of what player they want to be "cyan" or "yellow".
server sends the current srv_ppos values as a string eg:
client_socket.send(f"{yellow_x} {yellow_y} {cyan_x} {cyan_y}".encode("utf-8"))