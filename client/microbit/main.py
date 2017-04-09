from microbit import *
uart.init(115200)
sleep(4000)
uart.init(115200,tx=pin8,rx=pin12)
while True:
    uart.write("testinjola\r")
    display.scroll("poslano")
    sleep(2000)