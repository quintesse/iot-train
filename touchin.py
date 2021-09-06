from machine import Pin, TouchPad
import led, uasyncio

async def readInput(imotor):
    padFwd = TouchPad(Pin(15, Pin.IN))
    padFwd.config(400)
    padStop = TouchPad(Pin(14, Pin.IN))
    padStop.config(400)
    padBwd = TouchPad(Pin(4, Pin.IN))
    padBwd.config(400)
    while True:
        if __safeRead(padStop) < 100:
            print("Stop")
            imotor.speedTo(0)
        elif __safeRead(padFwd) < 100:
            print("Forward")
            imotor.speedTo(min(imotor.speedTo() + 10, 100))
        elif __safeRead(padBwd) < 100:
            print("Back")
            imotor.speedTo(max(imotor.speedTo() - 10, -100))
        else:
            print("Nothing")
        await uasyncio.sleep_ms(500)
        
def __safeRead(pad):
    try:
        return pad.read()
    except:
        return 1000
