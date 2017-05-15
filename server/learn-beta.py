import os
import numpy as np
import math as m
from numpy.linalg import norm
#import matplotlib.pyplot as plt
#rom mpl_toolkits.mplot3d import Axes3D
from select import select

os.environ["PYTHONDONTWRITEBYTECODE"]="True"

import servThread

BUFFER_SIZE = 32


def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

#alfa = 100
alfa = 0.01
mi = 0.0001
nfeatures = 3	#broj x-eva

def h(theta,x):
	return(1/(1+m.e**(x.dot(theta))))

def nauci(X,y,theta0):
	theta = theta0
	M = len(X)
	while(True):
		oldTheta = theta;
		theta = theta - alfa*X.T.dot(y-h(theta,X))/M
		if( norm(theta - oldTheta) < mi ):
			break
	return theta
			
def scaleData(X):
	mean = np.empty(shape=(len(X[0])))
	std = np.empty(shape=(len(X[0])))
	for i in range(len(X[0])):
		mean[i] = np.mean(X[:,i])
		std[i] = np.std(X[:,i])
	mean[0] = 0
	std[0] = 1
	X1 = np.divide((X -mean),std)
	return mean,std,X1

lista = np.fromfile("server/podaci",sep="\t")
lista = lista.reshape(-1,nfeatures)
y = lista[:,nfeatures-1]
X = lista[:,0:nfeatures-1]
X = np.insert(X, 0, 1, axis=1)
mu, sigma, X = scaleData(X)

theta = np.zeros(len(X[0]))
theta1 = nauci(X,y,theta)


def provjeravaj(server):
	server.socket.listen(1)
	print("Cekam konekciju 50 sekundi")
	i,_,_ = select([server.socket],[],[],50)

	if i:
		conn, addr = server.socket.accept()
		print("Konekcija s adrese: "+str(addr))

		while server.thrRunning:
			j = False
			while not j:
				j,_,_ = select([conn],[],[],1)
				if not server.thrRunning:
					conn.close()
					return

			data = np.fromstring(conn.recv(BUFFER_SIZE),sep='\t')[0:2]
			data = np.append([1],data)
			#print(data)

			broj = h(theta1, np.divide((data-mu),sigma))
			if broj > 0.5:
				print("pozitivno :" + str(broj))
		conn.close()
		
	else:
		print("Nema konekcije.")
		return



TCP_IP = "192.168.137.57"
TCP_PORT = 5005

server = servThread.servThread((TCP_IP,TCP_PORT),provjeravaj)
server.start()

inp=""

while inp!="quit":
	inp= raw_input("Upisi quit za ugasiti\n")

print("RIP server")

server.thrRunning=False
server.join()







"""
testPodatci = np.fromfile("server/podaci",sep="\t")
testPodatci = testPodatci.reshape(-1,nfeatures)
testPodatci = testPodatci[:,0:nfeatures-1]
testPodatci = np.insert(testPodatci, 0, 1, axis=1)
testPodatci = np.divide((testPodatci-mu),sigma)
predection = h( theta1, testPodatci[0:len(testPodatci)] )
print(predection)



fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(xs=X[:,1], ys = X[:,2], zs=y, c="red")

iks1 = np.linspace(-2,2,30)
iks2 = np.linspace(-2,2,30)
iks1,iks2 = np.meshgrid(iks1,iks2)
ax.plot_wireframe(iks1, iks2, 1/(1+ m.e**(theta[0] + iks1* theta[1] + iks2*theta[2])))

plt.show()"""
