import socket, sys, signal, threading, json

def receive_json(sock):
	json_data = sock.recv(1024).decode()
	return json.loads(json_data)

def send_json(client_socket, data):
	json_data = json.dumps(data)
	client_socket.send(json_data.encode())

def is_value_in_list(value, mylist):
	for item in mylist:
		if value == item:
			return True

