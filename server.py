import socket
import threading
import time
import signal
import sys
HOST = "localhost"
PORT = 5555
online_players = []
srv_ppos = { "yellow": {"x": 120, "y":  120}, "cyan": {"x": 40, "y": 40}}

enable_print_ppos = False

def print_srv_ppos():
    while enable_print_ppos:
        time.sleep(5)
        print(f"srv_ppos: {srv_ppos}")

def handle_client(client_socket, player_name):
    online_players.append(player_name)
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            msgparts = message.split(" ")
            
            #recieve position from client and update the srv_ppos (server player positions)
            if player_name and len(msgparts) >= 2:
                try:
                    new_x = int(msgparts[0])
                    new_y = int(msgparts[1])
                except:
                    print("index out of rainge failed to set new_x or new_y")
                srv_ppos[player_name]["x"] = new_x
                srv_ppos[player_name]["y"] = new_y  
            
            # Send the message back to the client (send the opposite players srv_ppos)
            if player_name == "cyan":
                
                x_snd = srv_ppos["yellow"]["x"]
                y_snd = srv_ppos["yellow"]["y"]
                try:
                    client_socket.send(f"{x_snd} {y_snd}".encode("utf-8"))
                except:
                    print("cant send cyan")
            if player_name == "yellow":
                x_snd = srv_ppos["cyan"]["x"]
                y_snd = srv_ppos["cyan"]["y"]
                try:
                    client_socket.send(f"{x_snd} {y_snd}".encode("utf-8"))
                except:
                    print("cant send yellow")
        except ConnectionResetError:
            print(f"{player_name} disconnected")
            online_players.remove(player_name)
            break

    client_socket.close()

def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(2)
    except:
        print("Failed to start server")
        return
    print(f"Started server on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Initiating handshake with {addr}")
        #first message server sends is the list of online players
        print(f"Sending player list")
        client_socket.send(str(online_players).encode("utf-8"))
        print("Awaiting response from client")
        #Then the server waits for a response of the player "cyan" or "yellow"
        player_name = client_socket.recv(1024).decode('utf-8').strip().lower()
        print(f"{addr} has connected as {player_name}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, player_name.strip()))
        client_handler.start()

def main():
    print_srv_pos_thread = threading.Thread(target=print_srv_ppos, daemon=True)
    print_srv_pos_thread.start()
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

if __name__ == "__main__":
    main()
