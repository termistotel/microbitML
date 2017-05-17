from microbit import *

uart.init(115200, tx=pin8, rx=pin12)
sleep(10000)
display.scroll("start")
uart.readall()
sleep(100)
uart.write("Nepotrebna linija\n\r")

while True:
    x = uart.readall()
    if x:
        display.scroll(x)
        uart.write("Zavrseno prikazivanje\n\r")
