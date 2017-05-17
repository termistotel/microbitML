s=net. createConnection(net.TCP,0)

s:on("receive", function(sck,c) uart.write(0,c.."\r\n") end)

function funkcija(data)
  s:send(string.sub(data,1,-2))
end

--prvi nesmije poslat jer prvi podatak može biti cudan
function funkcija1(data)
  uart.on("data", "\r", funkcija,0)
end

uart.on("data", "\r", funkcija1,0)

s:connect(5005,"192.168.137.57")
