from microbit import *
uart.init(115200)
sleep(15000)
uart.init(115200,tx=pin8,rx=pin12)

while True:
    tmp=accelerometer.get_values()
    y = "0"
    if button_a.was_pressed():
    	y="1"

    uart.write(str(tmp[0])+"\t"+str(tmp[1])+"\t"+str(tmp[2])+"\t"+y+"\r")
    sleep(50)
