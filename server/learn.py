import numpy as np
import math as m
import os
from numpy.linalg import norm
from random import randint
from select import select

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

import servThread

BUFFER_SIZE = 32

uzastopni = 11

alfa = 1
mi = 0.00001
nfeatures = 4

def h(theta,x):
	return(1/(1+m.e**(x.dot(theta))))

def nauciOld(X,y,theta0,n=500):
	theta = theta0
	for i in range(n):
		theta = theta - alfa*X.T.dot(y1-h(theta,X))
	return theta

def nauci(X,y,theta0):
	theta = theta0
	M = len(X)
	while(True):
		oldTheta = theta;
		theta = theta - alfa*X.T.dot(y-h(theta,X))/M
		if( norm(theta - oldTheta) < mi ):
			break
	return theta

def skala(X):
	mean = np.empty(shape=(len(X[0])))
	sigma = np.empty(shape=(len(X[0])))
	for i in range(len(X[0])):
		mean[i] = np.mean(X[:,i])
		sigma[i] = np.std(X[:,i])

		if (mean[i] == 0) and (sigma[i] == 0):
			sigma[i] = 1

		if sigma[i] == 0:
			sigma[i] = mean[i]
			mean[i] = 0

	return mean,sigma

def skaliraj(X,mean,sigma):
	return np.divide((X -mean),sigma)

def oblikujPodatke(X,y,uzastopni):
	indeksi,=np.where(y==1)
	broj = len(indeksi)
	indeksi2 = np.zeros(shape=(broj,uzastopni),dtype='int32')

	for i in range(uzastopni):
		indeksi2[:,i] = indeksi-2+i

	y1=np.array([])
	#X1 = np.zeros(shape=(2*len(indeksi),4*uzastopni+1))
	X1 = np.empty(shape=(0,4*uzastopni+1))

	#Dodaj pozitivnu klasu
	j= 0
	for red in indeksi2:
		odabrani = X[red,:].ravel()
		#X1[j,:] = np.append([1],odabrani)
		mjerenje = np.append([1],odabrani)
		print(X1.shape)
		print(mjerenje.shape)
		X1 = np.append(X1,[mjerenje],axis=0)
		y1 = np.append(y1,[1])
		j+=1

	X = np.delete(X,indeksi2.ravel(),0)

	#Dodaj negativnu klasu
	for i in range(broj):
		indeksi=np.array(range(uzastopni))-2+randint(uzastopni//2,len(X)-uzastopni//2-1)
		odabrani = X[indeksi,:].ravel()
		#X1[j,:] = np.append([1],odabrani) 
		mjerenje = np.append([1],odabrani)
		X1 = np.append(X1,[mjerenje],axis=0)
		y1 = np.append(y1,[0])
		j+=1
		#X = np.delete(X,indeksi,0)
	return X1,y1

lista = np.fromfile("/home/alion/Projekti/microbitML/server/podaci",sep="\t")
lista = lista.reshape(-1,nfeatures+1)
y=lista[:,nfeatures]
X=lista[:,0:nfeatures]

theta0 = np.zeros(4*uzastopni+1)
X1,y1 = oblikujPodatke(X,y,uzastopni)
mean,sigma = skala(X1)
print(mean)
print(sigma)
X1 = skaliraj(X1,mean,sigma)

broj = 4

theta = nauci(X1,y1,theta0)
dobri = h(theta,X1[0:broj])
losi = h(theta,X1[broj:2*broj])
print(theta)
print("dobri")
print(dobri)
print("losi")
print(losi)
#print(dobri[dobri<0.5])
#print(losi[losi>0.5])

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

"""
TCP_IP = raw_input("Unesi IP adresu")
TCP_PORT = 5005

server = servThread.servThread((TCP_IP,TCP_PORT),provjeravaj)
server.start()

inp=""

while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()"""
