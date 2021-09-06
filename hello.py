def say_hello():
    import tinypico as TinyPICO
    import micropython
    
    # Say hello
    print("")
    print("Hello from TinyPICO!")
    print("--------------------")
    print("")
    
    # Show some info on boot 
    print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
    print("Battery Charge State is {}".format( TinyPICO.get_battery_charging() ) )
    print("")
    
    # Show available memory
    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()
