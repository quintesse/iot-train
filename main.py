
# Determines if boot process should be halted
def halt_boot():
    # Check if pin 2 is LOW2
    from machine import Pin
    p = Pin(2, Pin.IN)
    return p.value() == 0
    
if halt_boot():
    print("Boot process interrupted!")
else:
    import start, uasyncio as asyncio
    asyncio.run(start.run())
    asyncio.get_event_loop().run_forever()

def reload(mod):
    import gc
    from sys import modules
    mod_name = mod.__name__
    del modules[mod_name]
    gc.collect()
    return __import__(mod_name)

