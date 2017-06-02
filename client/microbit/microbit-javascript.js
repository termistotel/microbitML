let distance = 0
control.waitMicros(15000)
basic.showString("Initializing UART")
serial.redirect(
    SerialPin.P8,
    SerialPin.P12,
    BaudRate.BaudRate115200
)
basic.showString("UART initialized")
while (true) {
    distance = 0
    for (let index = 0; index <= 9; index++) {
        distance += sonar.ping(
            DigitalPin.P1,
            DigitalPin.P2,
            PingUnit.Centimeters
        )
        control.waitMicros(100000)
    }
    distance = distance / 10
    serial.writeLine("" + distance + "\t" + pins.analogReadPin(AnalogPin.P0) + "\t" + pins.digitalReadPin(DigitalPin.P16))
}

