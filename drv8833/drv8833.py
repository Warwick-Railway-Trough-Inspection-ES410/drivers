"""
drv8833.py
==========
Library for controlling DRV8833 motor drivers

Author(s): Harry Upton

Datasheet: https://www.ti.com/lit/ds/symlink/drv8833.pdf

Implementation Notes
--------------------
- After the class has been initialised, you must first call configure_gpio()
- Motor speed goes from 0 -> -255 to 255
- Call cleanup() when you are done

Missing Features (ToDo):
------------------------
- Set PWM frequency
- Ability to change motor default direction

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
                 PIN_nSLEEP: int,
                 PIN_nFAULT: int):
        self.PIN_AIN1 = PIN_AIN1
        self.PIN_AIN2 = PIN_AIN2
        self.PIN_BIN1 = PIN_BIN1
        self.PIN_BIN2 = PIN_BIN2
        self.PIN_nSLEEP = PIN_nSLEEP
        self.PIN_nFAULT = PIN_nFAULT

    def configure_gpio(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(self.PIN_AIN1, pigpio.OUTPUT)
        self.pi.set_mode(self.PIN_AIN2, pigpio.OUTPUT)
        self.pi.set_mode(self.PIN_BIN1, pigpio.OUTPUT)
        self.pi.set_mode(self.PIN_BIN2, pigpio.OUTPUT)

        self.pi.set_mode(self.PIN_nSLEEP, pigpio.OUTPUT)
        self.pi.write(self.PIN_nSLEEP, 1) # Enable the chip
        self.pi.set_mode(self.PIN_nFAULT, pigpio.INPUT)

    def set_motorA_speed(self, speed: int):
        if speed > 255 or speed < -255:
            raise ValueError(f"Speed ({speed}) is outside of suitable range (-255 -> +255)")
        if speed >= 0:
            self.pi.set_PWM_dutycycle(self.PIN_AIN1, speed)
            self.pi.set_PWM_dutycycle(self.PIN_AIN2, 0)
        else:
            self.pi.set_PWM_dutycycle(self.PIN_AIN1, 0)
            self.pi.set_PWM_dutycycle(self.PIN_AIN2, -speed)

    def set_motorB_speed(self, speed: int):
        if speed > 255 or speed < -255:
            raise ValueError(f"Speed ({speed}) is outside of suitable range (-255 -> +255)")
        if speed >= 0:
            self.pi.set_PWM_dutycycle(self.PIN_BIN1, speed)
            self.pi.set_PWM_dutycycle(self.PIN_BIN2, 0)
        else:
            self.pi.set_PWM_dutycycle(self.PIN_BIN1, 0)
            self.pi.set_PWM_dutycycle(self.PIN_BIN2, -speed)

    def set_sleep(self, sleep_state: bool):
        if type(sleep_state) != bool:
            raise TypeError("sleep_state not a boolean value")
        self.pi.write(self.PIN_nSLEEP, int((not sleep_state))) # Pin is nSleep, write LOW to disable chip

    def get_fault(self) -> bool:
        return not bool(self.pi.read(self.PIN_nFAULT)) # Pin is nFault, reads LOW when there is a fault.
    
    def cleanup(self):
        self.pi.stop()
        