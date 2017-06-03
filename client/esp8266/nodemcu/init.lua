function startup()
    if file.open("init.lua") == nil then
        print("init.lua deleted or renamed")
    else
        print("Running")
        file.close("init.lua")
        -- pokrecemo kod u application.lua
        dofile("application.lua")
    end
end

--Dio koda za spajanje na pristupnu tocku
print("Connecting to WiFi access point...")
wifi.setmode(wifi.STATION)
wifi.sta.config("SSID", "sigurnosni kljuc") --Ovdje treba unijeti SSID i sigrnosni kljuc

--Cekamo dok se ne dodjeli IP adresa
tmr.alarm(1, 1000, 1, function()
    if wifi.sta.getip() == nil then
        print("Waiting for IP address...")
    else
        tmr.stop(1)
        print("WiFi connection established, IP address: " .. wifi.sta.getip())
        print("You have 5 seconds to abort")
        print("Waiting...")
        --Cekamo 5 sekundi prije pokretanja glavnog programa da 
        --imamo vremena uploadati novi kod ako nešto nije u redu
        tmr.alarm(0, 5000, 0, startup)
    end
end)
