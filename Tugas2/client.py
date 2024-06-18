from socket import *
import socket
import threading
import time
import sys


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('localhost', 45000)
clientsocket.connect(server_addr)

try:
    while True:
        req = input("Input your message: ")
        if req == "QUIT":
            clientsocket.sendall(req.encode())
            print("QUITING...")
            clientsocket.close()
            print("Gracefully successful closed the connection")
            exit()
        elif req.startswith("TIME"):
            req += "\r\n"
            clientsocket.sendall(req.encode())
            data = clientsocket.recv(14)
            if len(data) == 14:
                print(data.decode('utf-8'))
            else:
                print("Invalid response")

except Exception as e:
    print(f"ERROR OCCURED {e}")

finally:
    clientsocket.close()
