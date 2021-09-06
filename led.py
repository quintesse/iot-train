# Simple LED management

from machine import SPI, Pin
from dotstar import DotStar
import tinypico as TinyPICO

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
_spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
_dotstar = DotStar(_spi, 1, brightness = 0.5 ) # Just one led, half brightness
# Count how many times led_on was called
_ledOnCount = 0

def led_on():
    global _ledOnCount, _dotstar
    _ledOnCount += 1
    # Turn on the power to the DotStar
    TinyPICO.set_dotstar_power( True )
    _dotstar.show()

def led_off():
    global _ledOnCount
    if _ledOnCount > 1:
        _ledOnCount -= 1;
    else:
        _ledOnCount = 0
        # Turn off the power to the DotStar
        TinyPICO.set_dotstar_power( False )

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
    global _dotstar
    _dotstar[0] = (255, 255, 255)

def led_red():
    global _dotstar
    _dotstar[0] = (255, 0, 0)

def led_green():
    global _dotstar
    _dotstar[0] = (0, 255, 0)

def led_blue():
    global _dotstar
    _dotstar[0] = (0, 0, 255)

def led_yellow():
    global _dotstar
    _dotstar[0] = (255, 255, 0)

def led_orange():
    global _dotstar
    _dotstar[0] = (255, 165, 0)
