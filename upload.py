#!/usr/bin/env python
import sys
import os


if __name__== "__main__":
	args = sys.argv
	nodemcuLoc="client/esp8266/nodemcu/" #relativna lokacija programa za nodemcu za esp8266
	paths = os.environ["PATH"].split(os.pathsep) #env. varijabla path
	paths = paths + os.environ["PYTHONPATH"].split(os.pathsep) #env. varijabla pythonpath
	lokacija = None

	if args[1] == "esp":

		if args[2] =="nodemcu":

			for path in paths:
				if os.path.exists(path) and ("nodemcu-uploader.py" in os.listdir(path)): #trazi nodemcu-uploader.py u path varijabli					
					lokacija = path+("/nodemcu-uploader.py").replace("//","/") #lokacija programa za uploadavanje

			if not lokacija:
				sys.exit("nema nodemcu-uploader.py u PATH ili PYTHONPATH varijablama")

			files = os.listdir(nodemcuLoc)
			for file in filter(lambda x: x[-4:]==".lua" ,files):  #Uzimamo samo one fajlove koji zavrsavaju na .lua
				os.system("sudo python2 "+lokacija+" upload "+nodemcuLoc+file+":"+file)  #nodemcu-uploader.py treba biti instaliran

		else:
			print("drugi argument mora biti nodemcu ili micropython")
	else:
		print("prvi argument je esp ili microbit")