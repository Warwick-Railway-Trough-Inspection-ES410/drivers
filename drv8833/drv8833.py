"""
drv8833.py
==========
Library for controlling DRV8833 motor drivers

Author(s): Harry Upton

Datasheet: https://www.ti.com/lit/ds/symlink/drv8833.pdf

Implementation Notes
--------------------


Missing Features (ToDo):
------------------------


"""
import pigpio
import time

# One of these can be instantiated per chip
class DRV8833:
    def __init__(self,
                 PIN_AIN1: int,
                 PIN_AIN2: int,
                 PIN_BIN1: int,
                 PIN_BIN2: int,
                 PIN_SLEEP: int,
                 PIN_FAULT: int,
                 FREQUENCY: float = 100):
        self.PIN_AIN1 = PIN_AIN1
        self.PIN_AIN2 = PIN_AIN2
        self.PIN_BIN1 = PIN_BIN1
        self.PIN_BIN2 = PIN_BIN2
        self.PIN_SLEEP = PIN_SLEEP
        self.PIN_FAULT = PIN_FAULT
        self.freq = FREQUENCY

    def configure_gpio(self):
        pass


    def configure_pwm(self):
        pass


    def set_motorA_speed(self, speed: float):
        if speed >= 0:
            pass
        else:
            pass
    def set_motorB_speed(self, speed: int):
        if speed >= 0:
            pass
        else:
            pass

    def set_sleep(self, sleep_state: bool):
        if type(sleep_state) != bool:
            raise TypeError("sleep_state not a boolean value")
        pass

    def get_fault(self) -> bool:
        return not GPIO.input(self.PIN_FAULT)
    
    def cleanup(self):
        pass