import socket
import time
import sys
import asyncore
import logging
from http import HttpServer

httpserver = HttpServer()
rcv = ""

class ProcessTheClient(asyncore.dispatcher_with_send):
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def run(self):
        try:
            data = self.client_socket.recv(1024)
            if data:
                hasil = httpserver.proses(data.decode())
                self.client_socket.sendall(hasil + b"\r\n\r\n")
        except Exception as e:
            logging.warning(f"Error handling client: {e}")
        finally:
            self.client_socket.close()

class Server(asyncore.dispatcher):
	def __init__(self,portnumber):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('localhost',portnumber))
		self.listen(5)
		logging.warning("running on port {}" . format(portnumber))

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			logging.warning("connection from {}" . format(repr(addr)))
			handler = ProcessTheClient(sock)
			handler.run()

def main():
	portnumber=8887
	try:
		portnumber=int(sys.argv[1])
	except:
		pass
	svr = Server(portnumber)
	asyncore.loop()

if __name__=="__main__":
	main()

