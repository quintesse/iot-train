# Control motor speed

from machine import Pin, PWM

class IMotor:
    def speed(self):
        return 0

    # When no value is supplied returns current speed
    # as a normalized value between -100 and 100.
    # Otherwise immediately sets speed to new value.
    # Value can be between -100 and 100.
    # If supported by the hardware setting the speed
    # to 0 will let the motor "coast".
    # It then returns the old speed before the change
    # (can possibly be None if speed could not
    # be determined).
    def speed(self, val=None):
        return 0
    
    # When no value is supplied returns current target
    # speed as a normalized value between -100 and 100.
    # The motor will gradually accellerate or
    # decellerate to match the new speed.
    # Value can be between -100 and 100.
    # If supported by the hardware setting the
    # speed to 0 will let the motor "coast".
    # Returns the old speed before the change
    # (can possibly be None if speed could not
    # be determined).
    def speedTo(self, val=None):
        return self.speed(val)
    
    # Immediately brakes the motor.
    # By default this just calls `speed(0)` but
    # an implementation might provide its own.
    # Returns the old speed before the change
    # (can possibly be None if speed could not
    # be determined).
    def brake(self):
        return self.speed(0)
    
    @staticmethod
    def __pin(arg):
        if isinstance(arg, int):
            pin = Pin(arg, Pin.OUT)
        elif isinstance(arg, Pin):
            pin = arg
        else:
            raise TypeError("pin is not of type int or Pin")
        return pin
        
    @staticmethod
    def __pwm(arg, freq):
        if isinstance(arg, PWM):
            pwm = arg
        else:
            if isinstance(arg, int):
                pin = Pin(arg, Pin.OUT)
            elif isinstance(arg, Pin):
                pin = arg
            else:
                raise TypeError("pin is not of type int, Pin or PWM")
            pwm = PWM(pin, freq)
        return pwm
        
    @staticmethod
    def __normalize(duty):
        return round(duty * 100 / 1023)
    
    @staticmethod
    def __denormalize(speed):
        return round(abs(speed) * 1023 / 100)
    

class L9110:
    
    class Motor(IMotor):
        
        # The constructor takes two required parameters
        # defining the two motor input pins on the HBridge
        # board. The pinIA and pinIB can either be ints
        # (for which standard IN Pins will be created),
        # Pin objects (for which PWMs object will be
        # created) or PWM objects.
        def __init__(self, pinIA, pinIB, freq=25):
            self.pwmIA = self.__class__.__pwm(pinIA, freq)
            self.pwmIB = self.__class__.__pwm(pinIB, freq)

        def speed(self, val=None):
            if val is None:
                dutyA = self.pwmIA.duty()
                dutyB = self.pwmIB.duty()
                if dutyA == 0 and dutyB == 0:
                    val = 0
                elif dutyA > 0 and dutyB > 0:
                    val = None
                elif dutyA > 0:
                    val = self.__class__.__normalize(dutyA)
                else:
                    val = -self.__class__.__normalize(dutyB)
                return val
            else:
                assert val >= -100 and val <= 100, "speed must be between -100 and 100"
                old = self.speed()
                if val >= 0:
                    self.pwmIB.duty(0)
                    self.pwmIA.duty(self.__class__.__denormalize(val))
                else:
                    self.pwmIA.duty(0)
                    self.pwmIB.duty(self.__class__.__denormalize(val))
                return old


class TB6612:
    
    class Motor(IMotor):
        
        # The constructor takes three required parameters
        # defining the three motor input pins on the HBridge
        # board. The pinI1 and pinI2 can either be ints
        # (for which standard IN Pins will be created) or
        # Pin objects. The pinPWM can either be an int
        # (for which a standard IN Pin will be created),
        # a Pin object (for which a PWM object will be
        # created) or a PWM object.
        def __init__(self, pinI1, pinI2, pinPWM, freq=25):
            self.pinI1 = self.__class__.__pin(pinI1)
            self.pinI2 = self.__class__.__pin(pinI2)
            self.pinPWM = self.__class__.__pwm(pinPWM, freq)

        def speed(self, val=None):
            if val is None:
                valI1 = self.pinI1.value()
                valI2 = self.pinI2.value()
                duty = self.pinPWM.duty()
                if (valI1 == 0 and valI2 == 0) or (valI1 == 1 and valI2 == 1):
                    val = 0
                elif valI1 == 1:
                    val = self.__class__.__normalize(duty)
                else:
                    val = -self.__class__.__normalize(duty)
                return val
            else:
                assert val >= -100 and val <= 100, "speed must be between -100 and 100"
                old = self.speed()
                if val > 0:
                    self.pinI2.off()
                    self.pinI1.on()
                elif val < 0:
                    self.pinI1.off()
                    self.pinI2.on()
                else:
                    self.pinI1.off()
                    self.pinI2.off()
                self.pinPWM.duty(self.__class__.__denormalize(val))
                return old

        def brake(self):
            old = self.speed()
            self.pinI1.on()
            self.pinI2.on()
            return old
