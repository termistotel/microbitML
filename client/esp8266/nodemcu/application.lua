sok=net. createConnection(net.TCP,0)



--sok:on("sent", function(sck,c) print("sent") end)
--sok:on("connection", function(sck,c) 
--    --print("connection") 
--    a,b,c,d = uart.getconfig(0)
--    s:send(a.." "..b.." "..c.." "..d)
--  end)

sok:on("receive", function(sck,c) uart.write(0,c.."\n\r") end)

--sok:on("reconnection", function(sck,c) print("reconnection") end)
--
--sok:on("disconnection", function(sck,c) 
--    print("disconnection")
--    sck:connect(5005,"192.168.2.20")
--  end)
--
--sok:on("sent", function(sck,c) print("sent") end)

function funkcija(data)
  sok:send(string.sub(data,1,-2))
end

--prvi nesmije poslat jer prvi podatak može biti cudan
function funkcija1(data)
  uart.on("data", "\r", funkcija,0)
end

uart.on("data", "\r", funkcija1,0)

sok:connect(5005,"192.168.2.102")
