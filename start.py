# Main application process

import led, uasyncio

async def run():
    # Put your code here
    serviceHost = "bluetrain"
    serviceSSID = "BlueTrainController"
    servicePwd = "danitrain"
    
    led.blink(count=2)
    led.on()

    try:
        from hello import say_hello
        say_hello()

        # Let's turn on the motor as early as possible,
        # that way it can be played with even when the
        # remote control feature isn't used
        import motor
        imotor = motor.TB6612.Motor(13, 12, 14, 100) # pins D5-D7
        #imotor.speedTo(75)

        #from touchin import handleInput
        #handleInput(imotor)
        
        from wifi_manager import WifiManager

        print("Connecting to network...")
        wm = WifiManager(ssid = serviceSSID, password = servicePwd)
        wm.wlan_sta.config(dhcp_hostname=serviceHost)
        await wm.connect()
            
        from websrv import start as webstart
        
        led.blink(count=3)
        led.on()

        # Starting web server
        webstart(imotor)

        print("")
        print("-------------------------------------------------------------------")
        print("    Remote train control now accessible on http://%s.local" % serviceHost)
        print("-------------------------------------------------------------------")
        print("")

        led.blink(delay=100, count=4)
        led.on()

    except:
        led.blink(delay=50)
        raise
    