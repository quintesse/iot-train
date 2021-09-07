from machine import Pin, TouchPad
from primitives.pushbutton import Pushbutton
import led, uasyncio

def handleInput(imotor):
    padFwd = TouchPad(Pin(15, Pin.IN))
    padFwd.config(400)
    padStop = TouchPad(Pin(14, Pin.IN))
    padStop.config(400)
    padBwd = TouchPad(Pin(4, Pin.IN))
    padBwd.config(400)
    pbFwd = Pushbutton(PadPin(padFwd))
    pbFwd.press_func(__fwd, (imotor, ))
    pbStop = Pushbutton(PadPin(padStop))
    pbStop.press_func(__stop, (imotor, ))
    pbBwd = Pushbutton(PadPin(padBwd))
    pbBwd.press_func(__bwd, (imotor, ))
    
async def readInput(imotor):
    padFwd = TouchPad(Pin(15, Pin.IN))
    padFwd.config(400)
    padStop = TouchPad(Pin(14, Pin.IN))
    padStop.config(400)
    padBwd = TouchPad(Pin(4, Pin.IN))
    padBwd.config(400)
    while True:
        if __safeRead(padStop) < 100:
            __stop(imotor)
        elif __safeRead(padFwd) < 100:
            __fwd(imotor)
        elif __safeRead(padBwd) < 100:
            __bwd(imotor)
        else:
            print("Nothing")
        await uasyncio.sleep_ms(200)
        
def __safeRead(pad):
    try:
        return pad.read()
    except:
        return 1000

def __stop(imotor):
    print("Stop")
    imotor.speedTo(0)
    
def __fwd(imotor):
    print("Forward")
    imotor.speedTo(min(imotor.speedTo() + 10, 100))
    
def __bwd(imotor):
    print("Back")
    imotor.speedTo(max(imotor.speedTo() - 10, -100))
    
class PadPin():
    
    def __init__(self, pad):
        self.pad = pad
        
    def value(self):
        if __safeRead(self.pad) < 100:
            return 1
        else:
            return 0
