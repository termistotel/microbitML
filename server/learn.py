import math
import numpy as np
from numpy.linalg import norm
from random import randint

import os
from select import select

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

from servThread import servThread

BUFFER_SIZE = 32

alfa = 1
mi = 0.001
nfeatures = 4

#funkcija koja pokusava predvidjeti y
def h(theta,x):
	return(1/(1+math.e**(x.dot(theta))))

#Ucenje koje uzima fiksan broj iteracija
def nauciIter(X,y,theta0,n=500):
	theta = theta0
	for i in range(n):
		theta = theta - alfa*X.T.dot(y1-h(theta,X))
	return theta

#funkcija koja uci dok razlika parametara u uzastopnim iteracijama ne postane dovoljno mala
def nauci(X,y,theta0):
	theta = theta0
	M = len(X)
	while(True):
		oldTheta = theta;
		theta = theta - alfa*X.T.dot(y-h(theta,X))/M
		razlika = norm(theta - oldTheta)
		print("Razlika starog i novog: " + str(razlika))

		if( razlika < mi ):
			break
	return theta

#funkcija koja nam vraca srednju vrijednost i standardnu devijaciju mjerenih podataka
def skala(X):
	mean = np.empty(shape=(len(X[0])))
	sigma = np.empty(shape=(len(X[0])))
	for i in range(len(X[0])):
		mean[i] = np.mean(X[:,i])
		sigma[i] = np.std(X[:,i])

		#Specijalni slucajevi
		if (mean[i] == 0) and (sigma[i] == 0):
			sigma[i] = 1

		if sigma[i] == 0:
			sigma[i] = mean[i]
			mean[i] = 0

	return mean,sigma

#funkcija za skaliranje podataka
def skaliraj(X,mean,sigma):
	return np.divide((X -mean),sigma)

#funkcija za drugacije oblikovanj podataka, nepotrebna i nekoristena
def oblikujPodatke(X,y,uzastopni):
       #u X1 i y1 spremamo nove, oblikovane podatke za treniranje
       y1=np.array([])
       X1 = np.empty(shape=(0,4*uzastopni+1))

       #Dodajemo pozitivnu klasu y = 1
       indeksi,=np.where(y==1)
       broj = len(indeksi) #broj mjerenja s y = 1
       indeksi2 = np.zeros(shape=(broj,uzastopni),dtype='int32')

       #Spremamo indekse okolnih mjerenja koje cemo poslije spojiti u oblik podataka za treniranje
       for i in range(uzastopni):
               indeksi2[:,i] = indeksi-2+i

       for red in indeksi2:
               odabrani = X[red,:].ravel()
               #dodajemo x0 = 1 na pocetak novih podataka
               mjerenje = np.append([1],odabrani)
               X1 = np.append(X1,[mjerenje],axis=0)
               y1 = np.append(y1,[1])

       #Brisemo sva mjerenja koja smo uzeli kao pozitivnu klasu
       X = np.delete(X,indeksi2.ravel(),0)

       #Dodajemo negativnu klasu y = 0, dodajemo isti broj mjerenja koji imamo za pozitivnu klasu
       for i in range(broj):
               #Za negativnu klasu uzimamo nasumicno odabrana mjerenja iz preostalih
               centralniIndeks = randint(uzastopni//2,len(X)-uzastopni//2 - 2)
               indeksi=np.array(range(uzastopni))-uzastopni//2 + centralniIndeks

               odabrani = X[indeksi,:].ravel()
               mjerenje = np.append([1],odabrani)
               X1 = np.append(X1,[mjerenje],axis=0)
               y1 = np.append(y1,[0])
       
       return X1,y1


#funkcija koja vraca true ako je resurs od servera iskoristen, a false ako je proslo odredeno vrijeme
def resBusy(res,timeout):
	i,_,_ = select([res],[],[],timeout)
	return i

def provjeravaj(server):
	server.socket.listen(1)
	print("Cekam konekciju 50 sekundi")
	uspjeh = resBusy(server.socket,50)

	if uspjeh:
		conn, addr = server.socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:

			#Provjerava jesu li podatci poslani preko konekcije i treba li u meduvremenu ugasiti server
			uspjeh2 = resBusy(conn,1)
			if uspjeh2:
				#Prihvacamo podatke preko mreze i pretvaramo ih u numpy array
				data = np.fromstring(conn.recv(BUFFER_SIZE),sep='\t')

				#Odbacujemo y, dodajemo x0 na pocetak i skaliramo mjerenje
				praviData = data[:nfeatures]
				praviData = np.append([1],praviData)
				praviData = skaliraj(praviData,mean,sigma)

				#Ispisujemo ako je vjerojatnost preko 50%
				predvidanje = h(theta, praviData)
				if predvidanje > 0.5:
					print("Pozitivno: "+ str(predvidanje))

		conn.close()
		
	else:
		print("Nema konekcije.")
		return



#
# Kod za ucenje
#

#Citanje podataka iz file-a
lista = np.fromfile("podaci",sep="\t")
lista = lista.reshape(-1,nfeatures+1)

#y nam je zadnji stupac
y=lista[:,nfeatures]
m = np.size(y)

#X0 je prvi stupac jedinica
X0 = np.ones(shape=(m,1))

#Potpuna matrica s traning data
X= np.append(X0, lista[:,0:nfeatures], axis=1)

#Pocetni koeficijenti theta
theta0 = np.zeros(nfeatures+1)

#Skaliranje svih stupaca za bolju konvergenciju ucenja
mean,sigma = skala(X)
X = skaliraj(X,mean,sigma)

#Ucenje koeficijenata
theta = nauci(X,y,theta0)



#
# Pokretanje servera
#

TCP_IP = raw_input("Unesi IP adresu racunala: ")
TCP_PORT = 5005

server = servThread((TCP_IP,TCP_PORT),provjeravaj)
server.start()

inp=""
while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()
