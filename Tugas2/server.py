from socket import *
import socket
from datetime import datetime
import threading
import logging

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		while True:
			try:
				data = self.connection.recv(32)
				if data:
					data = data.decode('utf-8')
					if data.startswith("TIME") and data.endswith("\r\n"):
						resp = "JAM " + datetime.strftime(datetime.now(), "%H:%M:%S") + "\r\n"
						print(f"[SENDING] response to client {self.address}")
						self.connection.sendall(resp.encode('utf-8'))
					elif data.startswith("QUIT"):
						print(f"[CLIENT EXIT] client from {self.address} has exited bye bye")
						resp = "invalid req\r\n"
						self.connection.sendall(resp.encode('utf-8'))
					else:
						print(f"[INVALID REQUEST] from {self.address}")
						self.connection.close()
						break
			except OSError as e:
				pass
		self.connection.close()



class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('localhost', 45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			print("[CONNECTION] from {}".format(self.client_address))
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)



def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()


