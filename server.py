import socket
from _thread import *
from player import Player
import pickle

server = "192.168.1.12"  # server running on that machine
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# verify server / port dispo
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started!")

players = [Player(0, 0, 50, 50, (255, 0, 0)),
           Player(100, 100, 50, 50, (0, 0, 255))]

# threaded to let many connections
# while game (other functions) still running
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:  # to receive some data
            data = pickle.loads(conn.recv(2048))  # larger the size = larger time to recv data
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))  # encode info before send to server
        except:
            break

    print("Lost connection")
    conn.close()


current_player = 0
while True:  # wait to grab connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
