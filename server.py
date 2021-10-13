import socket
from _thread import *
from player import Player
import pickle
from game import Game

server = "192.168.1.12"  # server running on that machine
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# verify server / port dispo
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started!")

connected = set()
games = {}
id_count = 0

# threaded to let many connections
# while game (other functions) still running
def threaded_client(conn, p, game_id):
    global id_count
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(2048*2).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing Game ", game_id)
    except:
        pass
    id_count -= 1
    conn.close()


while True:  # wait to grab connections
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2  # every 2 people increase game_id by 1
    if id_count % 2 == 1:  # wait till new player
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:  # ready to launch game
        games[game_id].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, game_id))
