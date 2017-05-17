from microbit import *

uart.init(115200)
sleep(15000)
uart.init(115200, tx=pin8, rx=pin12)


while True:
    tmp = accelerometer.get_values()
    uart.write(str(tmp[0])+"\t"+str(tmp[1])+"\t"+str(tmp[2])+"\t" + "\n\r")
    if(button_a.was_pressed()):
        while True:
            tmp = compass.get_field_strength()
            uart.write(str(tmp) + "\n\r")
            if (button_a.was_pressed()):
                break
    if(button_b.was_pressed()):
        while True:
            tmp = pin0.read_analog()
            uart.write(str(tmp) + "\n\r")
            if (button_a.was_pressed()):
                break
sleep(25)
