import socket
import threading
import pygame
import time
HOST = "localhost"
PORT = 5555
client_ppos = { "yellow": {"x": 0, "y":  0}, "cyan": {"x": 0, "y": 0}}
def send_pos(client_socket, player_name):
    while True:
        current_x = client_ppos[player_name]["x"]
        current_y = client_ppos[player_name]["y"]
        try:
            client_socket.send(str(f"{current_x} {current_y} ").encode('utf-8'))
        except:
            print("Failed to send position to server")
        pygame.time.delay(40)

def get_pos(client_socket):
    while True:
        pygame.time.delay(40)
        try:
            message = client_socket.recv(1024).decode('utf-8')
            msgparts = message.split(" ")
            new_x = int(msgparts[0])
            new_y = int(msgparts[1])
            if player_name == "yellow":
                new_x = int(msgparts[0])
                new_y = int(msgparts[1])
                client_ppos["cyan"]["x"] = new_x
                client_ppos["cyan"]["y"] = new_y
            if player_name == "cyan":
                new_x = int(msgparts[0])
                new_y = int(msgparts[1])
                client_ppos["yellow"]["x"] = new_x
                client_ppos["yellow"]["y"] = new_y
        except Exception as e:
            print(f"{e}")


if __name__ == "__main__":    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        #The client waits for a message from the server containing the list online players
        online_players = client.recv(1024).decode("utf-8")
        print(f"Online players: {online_players}")

        # Send the player name to the server
        player_name = input("Select player ") 
        client.send(player_name.encode('utf-8'))
        initial_srv_ppos = client.recv(1024).decode("utf-8")
        ispps = initial_srv_ppos.split(" ")
        client_ppos["yellow"]["x"] = int(ispps[0])
        client_ppos["yellow"]["y"] = int(ispps[1])
        client_ppos["cyan"]["x"] = int(ispps[2])
        client_ppos["cyan"]["y"] = int(ispps[3])
        
        print(f"Recieved initial ppos from srv_ppos: {ispps}")
    except:
        print("Failed to establish connection")
        client.close()
    #Then the client chooses which player they want to be  
    send_pos_thread = threading.Thread(target=send_pos, args=(client, player_name))
    get_pos_thread = threading.Thread(target=get_pos, args=(client,))

    # Start the threads
    get_pos_thread.start()
    send_pos_thread.start()
  

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))

    running = True
    while running:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        try:
            client_ppos[player_name]["x"] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 2
            client_ppos[player_name]["y"] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 2
        except:
            print("Failed to get key input")
        try:
            screen.fill([000, 000, 000])
            pygame.draw.rect(screen, (255, 255, 0), (client_ppos["yellow"]["x"], client_ppos["yellow"]["y"], 40, 40))
            pygame.draw.rect(screen, (0, 255, 255), (client_ppos["cyan"]["x"], client_ppos["cyan"]["y"], 40, 40))
            pygame.display.flip()
        except:
            print("Failed to draw")
        
