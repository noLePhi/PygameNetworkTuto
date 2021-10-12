import socket
from _thread import *
import sys

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


def read_pos(str):  # "45,46" -> (45,46)
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):  # (45,46) -> "45,46"
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (100, 100)]  # hold positions of players

# threaded to let many connections
# while game (other functions) still running
def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:  # to receive some data
            data = read_pos(conn.recv(2048).decode())  # larger the size = larger time to recv data
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))  # encode info before send to server
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
