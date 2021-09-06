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

        from wifi_manager import WifiManager
        from websrv import start as webstart

        # Let's turn on the motor as early as possible,
        # that way it can be played with even when the
        # remote control feature isn't used
        import motor
        imotor = motor.TB6612.Motor(26, 27, 25)

        from touchin import readInput
        uasyncio.create_task(readInput(imotor))
        
        #bt = uasyncio.get_event_loop().create_task(led.blink())
        print("Connecting to network...")
        wm = WifiManager(ssid = serviceSSID, password = servicePwd)
        wm.wlan_sta.config(dhcp_hostname=serviceHost)
        wm.connect()
        #bt.cancel()
        #led.led_on()
        
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

        uasyncio.create_task(led.ablink())

    except:
        led.led_red()
        raise
    