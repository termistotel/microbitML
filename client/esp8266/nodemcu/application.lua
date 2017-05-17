s=net. createConnection(net.TCP,0)



--s:on("sent", function(sck,c) print("sent") end)
--
--s:on("connection", function(sck,c) 
--    print("connection") 
--    a,b,c,d = uart.getconfig(0)
--    s:send(a.." "..b.." "..c.." "..d)
--  end)
--
s:on("receive", function(sck,c) uart.write(0,c.."\r\n") end)
--
--s:on("reconnection", function(sck,c) print("reconnection") end)
--
--s:on("disconnection", function(sck,c) 
--    print("disconnection")
--    sck:connect(5005,"192.168.2.20")
--  end)
--
--s:on("sent", function(sck,c) print("sent") end)

function funkcija(data)
  s:send(string.sub(data,1,-2))
end

--prvi nesmije poslat jer prvi podatak može biti cudan
function funkcija1(data)
  uart.on("data", "\r", funkcija,0)
end

uart.on("data", "\r", funkcija1,0)

s:connect(5005,"192.168.137.57")
