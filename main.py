# Main application process

import led, uasyncio

async def run():
    # Put your code here
    serviceHost = "bluetrain"
    serviceSSID = "BlueTrainController"
    servicePwd = "danitrain"
    
    led.led_orange()
    led.led_on()

    try:
        import ulogging as logging
        logging.basicConfig(level=logging.INFO)

        from hello import say_hello
        say_hello()

        # Let's turn on the motor as early as possible,
        # that way it can be played with even when the
        # remote control feature isn't used
        import motor
        imotor = motor.TB6612.Motor(26, 27, 25)
        imotor.speedTo(75)

        from touchin import handleInput
        handleInput(imotor)
        
        await uasyncio.sleep_ms(10)

        from wifi_manager import WifiManager
        from websrv import start as webstart

        await uasyncio.sleep_ms(10)

        print("Connecting to network...")
        wm = WifiManager(ssid = serviceSSID, password = servicePwd)
        wm.wlan_sta.config(dhcp_hostname=serviceHost)
        wm.connect()
            
        await uasyncio.sleep_ms(10)

        # Starting web server
        led.led_blue()
        webstart(imotor)

        print("")
        print("-------------------------------------------------------------------")
        print("    Remote train control now accessible on http://%s.local" % serviceHost)
        print("-------------------------------------------------------------------")
        print("")

        led.led_green()
        await uasyncio.sleep_ms(1000)
        led.led_off()

    except:
        led.led_red()
        raise
    