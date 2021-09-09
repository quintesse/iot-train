# Simple LED management

from machine import Pin

# The pin connected to the on-board LED
_pinLED = Pin(2, Pin.OUT)

# Count how many times led_on was called
_ledOnCount = 0

def led_on():
    global _ledOnCount, _pinLED
    _ledOnCount += 1
    # Turn on the LED (setting pin LOW!)
    _pinLED.off()
    
def led_off():
    global _ledOnCount, _pinLED
    if _ledOnCount > 1:
        _ledOnCount -= 1;
    else:
        _ledOnCount = 0
        # Turn off the LED (setting pin HIGH!)
        _pinLED.on()

async def ablink(delay=200):
    import uasyncio
    while True:
        led_on()
        await uasyncio.sleep_ms(delay)
        led_off()
        await uasyncio.sleep_ms(delay)
        
def blink(delay=200):
    import time
    while True:
        led_on()
        time.sleep(delay)
        led_off()
        time.sleep(delay)
        
def led_white():
    led_on()

def led_red():
    led_on()

def led_green():
    led_on()

def led_blue():
    led_on()

def led_yellow():
    led_on()

def led_orange():
    led_on()
