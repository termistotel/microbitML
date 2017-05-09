import numpy as np
import math as m
import os
from random import randint
from select import select

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

import servThread

BUFFER_SIZE=32
alfa=0.000001
n = 5000
uzastopni=11
theta=np.zeros(3*uzastopni+1)

def h(theta,x):
	return(1/(1+m.e**(x.dot(theta))))

def nauci(X,y,theta0,n=500):
	theta = theta0
	for i in range(n):
		theta = theta - alfa*X.T.dot(y1-h(theta,X))
	return theta


lista = np.fromfile("/home/alion/Projekti/microbitML/server/podaci",sep="\t")
lista = lista.reshape(-1,4)
y=lista[:,3]
X=lista[:,0:3]

indeksi,=np.where(y==1)
broj = len(indeksi)
indeksi2 = np.zeros(shape=(len(indeksi),uzastopni),dtype='int32')

for i in range(uzastopni):
	indeksi2[:,i] = indeksi-2+i

y1=np.array([])

X1 = np.zeros(shape=(2*len(indeksi),3*uzastopni+1))
j= 0
for red in indeksi2:
	odabrani = X[red,:].ravel()
	X1[j,:] = np.append([1],odabrani)
	y1 = np.append(y1,[1])
	j+=1

X = np.delete(X,indeksi2.ravel(),0)

for i in range(broj):
	indeksi=np.array(range(uzastopni))-2+randint(uzastopni//2,len(X)-uzastopni//2-1)
	odabrani = X[indeksi,:].ravel()
	X1[j,:] = np.append([1],odabrani) 
	y1 = np.append(y1,[0])
	j+=1
	X = np.delete(X,indeksi,0)


theta1 = nauci(X1,y1,theta,n)
dobri = h(theta1,X1[0:broj])
losi = h(theta1,X1[broj:2*broj])
print(theta1)
print(dobri)
print(losi)
print(dobri[dobri<0.5])
print(losi[losi>0.5])

def provjeravaj(server):
	server.socket.listen(1)
	print("Cekam konekciju 20 sekundi")
	i,_,_ = select([server.socket],[],[],20)

	if i:
		conn, addr = server.socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:
			akumulator = np.array([])
			for i in range(uzastopni):
				j = False
				while not j:
					j,_,_ = select([conn],[],[],1)
					if not server.thrRunning:
						conn.close()
						return

				data = np.fromstring(conn.recv(BUFFER_SIZE),sep='\t')
				akumulator=np.append(akumulator,data[0:3])
	
			print(h(theta1,np.append([1],akumulator.ravel())))
		conn.close()
		
	else:
		print("Nema konekcije.")
		return

TCP_IP = raw_input("Unesi IP adresu")
TCP_PORT = 5005

server = servThread.servThread((TCP_IP,TCP_PORT),provjeravaj)
server.start()

inp=""

while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()
