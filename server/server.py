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

def blank():
	pass

def cekajResurs(res,timeout,funkcija1,funkcija2=blank)
	j,_,_ = select([res],[],[],timeout)
	if j:
		return funkcija1(res)
	else:
		return funkcija2(res)

def markovaFunkcija(conn):
	data = conn.recv(BUFFER_SIZE)
	print(data)

__
def nesto1(socket):
	conn, addr = socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:
			#cekajResurs(conn,1, markovaFunkcija)
			conn.send("didaktika")

		conn.close()

	return True


def nesto2(socket):
	print("Nema konekcije.")
	return False


def podaciSaMicrobita(server):
	server.socket.listen(1)
	print("Cekam konekciju 30 sekundi")
	cekajResurs(server.socket,30,nesto1,nesto2)



server = servThread((TCP_IP,TCP_PORT),podaciSaMicrobita)
server.start()



inp=""
while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()
