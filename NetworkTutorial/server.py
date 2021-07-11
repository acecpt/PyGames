import socket   # connections to server on a port
from _thread import *  # threading requests
import sys

server = "192.168.0.213"    # CHANGE THIS Host Server IP
port = 5555     # typically open port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to port and socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)  # opens up the port to start listening limite in ( )
print("Waiting for a connection, Server Started")

def read_pos(str):  # convert "77, 45" to (77, 45) from server
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):  # convert tup into a string to server
    return str(tup[0]) + "," + str(tup[1])

pos = [(0, 0), (100, 100)]     # starting pos (p1), (p2)

def threaded_client(conn, player):
    # send some ack when a connection starts
    # conn.send(str.encode("Connected"))
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:     # continually run while client connected
        try:
            # if error *8 - but the bigger it is, the slower the connection
            data = read_pos(conn.recv(2048).decode())
                    # from eg "46, 67" to (45, 67)
            # reply = data.decode("utf-8")    # encoded in utf-8 over network
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

            # encode into a bytes object to send and decode on other end
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0   # track how many players are connecte

while True:     # continuousely look for connections
    conn, addr = s.accept()     # Accept incoming connections
    print("Connected to: ", addr)   # prints IP address of connection

    # don't let one client block while loop
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
