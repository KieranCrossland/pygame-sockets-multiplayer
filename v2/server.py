import socket, sys, signal, threading, json
import util 

SERVER_NAME = "kieran's server"
HOST = "localhost"
PORT = 5555

online_players = []

srv_ppos = { "yellow": {"x": 120, "y":  120}, "cyan": {"x": 40, "y": 40}}

def handle_client(socket, address):
	try: # SERVER INITIATES HANDSHAKE
		print(f"Starting handshake with {address}")
		print("sending server name")
		socket.send(SERVER_NAME.encode("utf-8"))
		print("receiving client name")
		client_name = socket.recv(1024).decode("utf-8")
		print(client_name)
		print("sending server player-positions")
		util.send_json(socket, srv_ppos)
	except ConnectionResetError:
		print(f"{address} has disconnected")
		print(f"online clients: {online_players}")
		
	finally:
		print(f"closing socket for {address}")
		socket.close()


def start_server():
	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.bind((HOST, PORT))
		server_socket.listen()
		print(f"Started server on {HOST}:{PORT}")
	except ConnectionRefusedError or ConnectionError:
		print(f"Failed to start server on {HOST}:{PORT}")
		return 
	except KeyboardInterrupt:
		server_socket.close()
		return 
	
	while True:
		try:
			client_socket, client_address = server_socket.accept()
			print(f"Client connected {client_address}")
			thread_handle_client = threading.Thread(target=handle_client, args=(client_socket, client_address))
			thread_handle_client.start()
		except KeyboardInterrupt:
			server_socket.close()
			return
		

if __name__ == "__main__":
	start_server()

