import socket, json, time
import util

CLIENT_NAME = "blue"
HOST = "localhost"
PORT = 5555


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

connected_server = sock.recv(1024).decode("utf-8")
print(connected_server)
sock.send(CLIENT_NAME.encode("utf-8"))
ppos = util.receive_json(sock)
print(ppos)
time.sleep(3)
sock.close()
	
