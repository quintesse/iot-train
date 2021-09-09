def say_hello():
    import micropython
    
    # Say hello
    print("")
    print("Hello from Blue Train!")
    print("----------------------")
    print("")
    
    # Show available memory
    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()
