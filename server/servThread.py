
import threading
import socket

class servThread (threading.Thread):
	def __init__(self,adresa,funkcija):
		#Prosirujemo Thread klasu:
		threading.Thread.__init__(self)

		#Socket na kojem server-dretva slusa konekcije
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#Funkcija koja ce se ponavljati u dretvi. Kao prvi argument prima objekt tipa servThread.
		self.funkcija = funkcija

		#adresa[0] je ipadresa, adresa[1] je port
		self.adresa = adresa

		#Varijabla koja nam provjerava ako zelimo ugasiti dretvu
		self.thrRunning = False

	#funkcija koja se pokrece s .start() metodom
	def run(self):
		print("Pokrecem server na adresi: "+str(self.adresa[0])+":"+str(self.adresa[1]))
		self.thrRunning = True
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.adresa)
		self.funkcija(self)
		self.socket.close()
		print("Server ugasen")

	#Zaustavljanje dretve
	def stop(self):
		self.thrRunning = False