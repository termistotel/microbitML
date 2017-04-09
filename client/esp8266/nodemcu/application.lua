s=net.createConnection(net.TCP,0)

connected=false

uart.on("data", "\r", function (data)
    s:send(data)
  end, 0)

s:on("connection", function(sck,c)
    connected=true
  end)

s:on("receive", function(sck,c)
    uart.write(0,c.."\r\n")
  end)

s:on("reconnection", function(sck,c) print("reconnection") end)

s:on("disconnection", function(sck,c) 
    print("disconnection") 
    connected=false
    sck:connect(5005,"192.168.137.25")
  end)

--s:on("sent", function(sck,c) print("sent") end)

s:connect(5005,"192.168.137.25")
