# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# Determines if boot process should be halted
def halt_boot():
    # Check if pin 4 is HIGH
    from machine import Pin
    p = Pin(4, Pin.IN, Pin.PULL_DOWN)
    return p.value() == 1
    
if halt_boot():
    print("Boot process interrupted!")
else:
    import main, uasyncio as asyncio
    asyncio.run(main.run())
    asyncio.get_event_loop().run_forever()

def reload(mod):
    import gc
    from sys import modules
    mod_name = mod.__name__
    del modules[mod_name]
    gc.collect()
    return __import__(mod_name)

