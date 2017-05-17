from microbit import *
uart.init(115200)
sleep(15000)
uart.init(115200,tx=pin8,rx=pin12)


while True:
    tmp=accelerometer.get_values()
    y = "0"
    if pin16.read_digital():
    	y="1"

    r2 = tmp[0]**2 + tmp[1]**2 + tmp[2]**2 

    uart.write(str(tmp[0])+"\t"+str(tmp[1])+"\t"+str(tmp[2])+"\t"+ str(r2) + "\t" + y+"\n\r")
    sleep(25)
