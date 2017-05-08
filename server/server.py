import numpy as np
import os
import socket
from select import select
from ast import literal_eval

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

import servThread

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 32

def zapisi(file,data):
	put = os.path.realpath(os.path.dirname(__file__))
        with open(os.path.join(put,file),'a') as f:
	        f.write(data)
	return True


def podaciSaMicrobita(server):
	server.socket.listen(1)
	print("Cekam konekciju 20 sekundi")
	i,_,_ = select([server.socket],[],[],20)

	if i:
		conn, addr = server.socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:
			j,_,_ = select([server.socket],[],[],1)
			if (j):
				data = conn.recv(BUFFER_SIZE)
				zapisi('podaci',data)
				#f = open('podaci','a')
				#f.write(data)
				#f.close()
	else:
		print("Nema konekcije.")
		return



server = servThread.servThread((TCP_IP,TCP_PORT),podaciSaMicrobita)
server.start()

inp=""

while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()
