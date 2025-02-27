"""
drv8833.py
===========
Library for controlling DRV8833 motor drivers

Author(s): Harry Upton

Datasheet: https://www.ti.com/lit/ds/symlink/drv8833.pdf

Implementation Notes
--------------------
- A PWMController object must be created first and passed to the DRV8833 objects.
 There must ONLY BE ONE of these, it runs the dma_pwm C functions.
- PWM does have an initial configuration, however can be modified with configure_pwm function.
- Multiple DRV8833 objects can be instantiated (as long as they use different pins)

Missing Features (ToDo):
------------------------

"""
import RPi.GPIO as GPIO
import os

def create_pwm_channel(pin_number: int) -> int:
    # Returns a channel ID given a pin number
    return 0

def free_pwm_channel(channel_id: int):
    # Will free a channel given its ID
    pass

def configure_dma() -> int:
    # Initial setup for device PWM DMA - call once
    pass

def configure_channel() -> int:
    # Configure a channel (frequency, duty cycle, etc.)
    pass

def enable_channel() -> int:
    # Enable a channel (output PWM signal) 
    pass

def disable_channel() -> int:
    # Disable a channel (stop outputting PWM signal)
    pass

def set_channel_duty_cycle() -> int:
    # Adjust channel duty cycle (control motor speed)
    pass

# One of these can be instantiated per chip
class DRV8833:
    def __init__(self,
                 PIN_AIN1: int,
                 PIN_AIN2: int,
                 PIN_BIN1: int,
                 PIN_BIN2: int,
                 PIN_SLEEP: int,
                 PIN_FAULT: int):
        self.PIN_AIN1 = PIN_AIN1
        self.PIN_AIN2 = PIN_AIN2
        self.PIN_BIN1 = PIN_BIN1
        self.PIN_BIN2 = PIN_BIN2
        self.PIN_SLEEP = PIN_SLEEP
        self.PIN_FAULT = PIN_FAULT

    def configure_gpio(self):
        GPIO.setmode(GPIO.BOARD) # Use board pin numbers, NOT BCM numbers

        GPIO.setup(self.PIN_SLEEP, GPIO.OUT)
        GPIO.setup(self.PIN_FAULT, GPIO.IN)


    def configure_pwm(self):
        self.A1_channel = create_pwm_channel(self.PIN_AIN1)
        self.A2_channel = create_pwm_channel(self.PIN_AIN2)
        self.B1_channel = create_pwm_channel(self.PIN_BIN1)
        self.B2_channel = create_pwm_channel(self.PIN_BIN2)


    def set_motorA_speed(self, speed: int):
        pass

    def set_motorB_speed(self, speed: int):
        pass

    def set_sleep(self, sleep_state: bool):
        if type(sleep_state) != bool:
            raise TypeError("sleep_state not a boolean value")
        
        GPIO.output(self.PIN_SLEEP, (not sleep_state))

    def get_fault(self) -> bool:
        return not GPIO.input(self.PIN_FAULT)
    
    def cleanup(self):
        GPIO.cleanup()
        free_pwm_channel(self.A1_channel)
        free_pwm_channel(self.A2_channel)
        free_pwm_channel(self.B1_channel)
        free_pwm_channel(self.B2_channel)