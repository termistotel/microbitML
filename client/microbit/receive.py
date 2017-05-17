from microbit import *

uart.init(115200)
sleep(15000)
uart.init(115200, tx=pin8, rx=pin12)


while True:
    x = uart.readall()
    display.scroll(x)
