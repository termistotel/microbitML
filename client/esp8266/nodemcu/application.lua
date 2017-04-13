s=net.createConnection(net.TCP,0)
connected=false

--prvi nesmije poslat jer je uvijek prvi bajt cudan
uart.on("data", "\r", function (data)
    uart.on("data","\r", function (data1)
        s:send(string.sub(data1,1,-2))
      end, 0)
    data = ""
  end, 0)

s:on("connection", function(sck,c)
    print("connection")
    connected=true
  end)

s:on("receive", function(sck,c)
    uart.write(0,c.."\r\n")
  end)

s:on("reconnection", function(sck,c) print("reconnection") end)

s:on("disconnection", function(sck,c) 
    print("disconnection") 
    connected=false
    sck:connect(5005,"192.168.2.20")
  end)

--s:on("sent", function(sck,c) print("sent") end)

s:connect(5005,"192.168.2.20")

