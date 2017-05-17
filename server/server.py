import numpy as np
import os
import socket
from select import select
from ast import literal_eval

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

from servThread import servThread

#TCP_IP = raw_input("Unesi IP adresu")
TCP_IP = "192.168.2.102"
TCP_PORT = 5005
BUFFER_SIZE = 32

def cekajResurs(res,timeout):
	j,_,_ = select([res],[],[],timeout)
	return j

def markovaFunkcija(conn):
	data = conn.recv(BUFFER_SIZE)
	print(data)

def nesto1(socket):
	conn, addr = socket.accept()
	print("Konekcija s adrese: "+str(addr))

	while server.thrRunning:
		uspjeh = cekajResurs(conn,1)
		if uspjeh:
			conn.send(raw_input("Sto da posaljem? "))

	conn.close()

	return True



def podaciSaMicrobita(server):
	server.socket.listen(1)
	print("Cekam konekciju 30 sekundi")
	uspjeh = cekajResurs(server.socket,30)
	if uspjeh:
			conn, addr = server.socket.accept()
			print("Konekcija s adrese: "+str(addr))

			while server.thrRunning:
				command = raw_input("Sto da posaljem? ")
				if command == "quit":
					server.thrRunning=False
				else:
					conn.send(command)
					print("Cekam odgovor: ")
					odgovor = conn.recv(BUFFER_SIZE)
					print(odgovor + "\n")

			conn.close()
			server.socket.close()
	else:
		print("Nema konekcije.")


server = servThread((TCP_IP,TCP_PORT),podaciSaMicrobita)
server.start()

server.join()
