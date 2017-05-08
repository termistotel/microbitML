from microbit import *
uart.init(115200)
sleep(15000)
uart.init(115200,tx=pin8,rx=pin12)

while True:
    tmp=accelerometer.get_values()
    uart.write(str(tmp[0])+"\t"+str(tmp[1])+"\t"+str(tmp[2])+"\r")
    sleep(50)
