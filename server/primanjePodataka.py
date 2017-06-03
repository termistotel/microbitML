import numpy as np

import os
from select import select

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

from servThread import servThread

BUFFER_SIZE = 32

#funkcija koja vraca true ako je resurs iskoristen, a false ako je proslo odredeno vrijeme
def resBusy(res,timeout):
	i,_,_ = select([res],[],[],timeout)
	return i
	
#funkcija koja zapisuje podatak u datoteku
def zapisi(file,data):
	with open("podaci",'a') as f:
		f.write(data)
	return True

#funkcija koju server izvrsava dok je upaljen
def podaciSaMicrobita(server):
	server.socket.listen(1)
	print("Cekam konekciju 50 sekundi")
	uspjeh = resBusy(server.socket,50)

	if uspjeh:
		conn, addr = server.socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:
			uspjeh2 = resBusy(conn,1)

			if uspjeh2:
				data = conn.recv(BUFFER_SIZE)
				print(data)
				zapisi('podaci',data)

		conn.close()
		
	else:
		print("Nema konekcije.")
		return



#
# Pokretanje servera
#

TCP_IP = raw_input("Unesi IP adresu racunala: ")
TCP_PORT = 5005

server = servThread((TCP_IP,TCP_PORT),podaciSaMicrobita)
server.start()

inp=""
while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()
