# Simple LED management

from machine import Pin

# The pin connected to the on-board LED
_pinLED = Pin(2, Pin.OUT)

# Count how many times led_on was called
_ledOnCount = 0

def on():
    global _ledOnCount, _pinLED
    _ledOnCount += 1
    # Turn on the LED (setting pin LOW!)
    _pinLED.off()
    
def off():
    global _ledOnCount, _pinLED
    if _ledOnCount > 1:
        _ledOnCount -= 1;
    else:
        _ledOnCount = 0
        # Turn off the LED (setting pin HIGH!)
        _pinLED.on()

async def ablink(delay=200, count=None):
    import uasyncio
    while count is None or count > 0:
        on()
        await uasyncio.sleep_ms(delay)
        off()
        await uasyncio.sleep_ms(delay)
        count -= 1
        
def blink(delay=200, count=None):
    import time
    while count is None or count > 0:
        on()
        time.sleep_ms(delay)
        off()
        time.sleep_ms(delay)
        count -= 1
        