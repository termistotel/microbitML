--Stvaramo socket za TCP komunikaciju
sok=net. createConnection(net.TCP,0)

function posaljiPrekoUART(sck,data)
  uart.write(0,data.."\n\r")
end

function posaljiPrekoWiFi(data)
  sok:send(string.sub(data,1,-1))
end

--Kada stignu podaci preko UARTa, samo ih posaljemo preko WiFi-a na racunalo
uart.on("data", "\r", posaljiPrekoWiFi,0)

--Kada stignu podaci preko WiFia, posalji na UART. Ovo omogucuje dvosmjernu komunikaciju
sok:on("receive", posaljiPrekoUART)

--IP adresu treba zamijeniti s adresom racunala
--Port za komunikaciju treba biti isti broj kao i na serveru
sok:connect(5005,"192.168.2.102")