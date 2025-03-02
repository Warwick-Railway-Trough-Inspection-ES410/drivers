"""
drv8833.py
==========
Library for controlling DRV8833 motor drivers

Author(s): Harry Upton

Datasheet: https://www.ti.com/lit/ds/symlink/drv8833.pdf

Implementation Notes
--------------------
- configure_dma() must be ran first, it must be ran once total (not once per DRV8833).
  Typically this is the only static function you need to run yourself.
- Use request_pwm_channel to first get a pwm_channel_id.
  DRV8833.configure_pwm() will do this for all the motor pins automatically, 
  so you do not need to do it for each pin yourself.
- DRV8833.configure_gpio() also needs to be run to setup the sleep and fault signals.
- PWM does have an initial configuration, however can be modified with configure_pwm function.
- Multiple DRV8833 objects can be instantiated (as long as they use different pins).
- You will mostly be interacting with DRV8833.set_motorA_speed/.set_motorB_speed/.set_sleep/.set_fault functions.
- Call DRV8833.cleanup() when you are done. This frees the GPIO and DMA channels.

Missing Features (ToDo):
------------------------
- Configure dma_pwm from Python


"""
import RPi.GPIO as GPIO
import subprocess

ERROR_NUMS = {1: "ECHNLREQ",
    2: "EINVPW",   
    3: "ENOFREECHNL",
    4: "EINVCHNL", 
    5: "EINVDUTY",    
    6: "EINVGPIO",   
    7: "EFREQNOTMET",
    8: "EPWMNOTSET", 
    9: "ENOPIVER", 
    10: "EMAPFAIL",
    11: "ESIGHDNFAIL"}

def request_pwm_channel() -> int:
    # Returns a channel ID given a pin number
    result = subprocess.run(["request_channel"], capture_output=True, text=True, shell=True)
    channel = result.stdout
    if channel in ERROR_NUMS:
        raise OSError(f"DMA request_channel error: {ERROR_NUMS[channel]}")
    if channel == -1:
        raise OSError("Invalid number of command line args.")
    return channel


def free_pwm_channel(channel_id: int) -> int:
    # Will free a channel given its ID
    result = subprocess.run(["free_channel", channel_id], capture_output=True, text=True, shell=True)
    out = result.stdout
    if out != 0:
        raise OSError(f"DMA free_channel error: {out}")
    
    return out

def configure_dma(pages: int, pulse_width: float) -> int:
    # Initial setup for device PWM DMA - call once
    result = subprocess.run(["request_channel", pages, pulse_width], capture_output=True, text=True, shell=True)
    out = result.stdout
    if out in ERROR_NUMS:
        raise OSError(f"DMA configure_dma error: {ERROR_NUMS[out]}")
    if out == -1:
        raise OSError("Invalid number of command line args.")
    
    return out

def configure_channel(channel_id: int, gpio: int, freq: float, duty: float) -> int:
    # Configure a channel (pin num, frequency, duty cycle, etc.)
    result = subprocess.run(["configure_channel", channel_id, gpio, freq, duty], capture_output=True, text=True, shell=True)
    out = result.stdout
    if out in ERROR_NUMS:
        raise OSError(f"DMA configure_dma error: {ERROR_NUMS[out]}")
    if out == -1:
        raise OSError("Invalid number of command line args.")
    
    return out
    

def enable_channel(channel_id: int) -> int:
    # Enable a channel (output PWM signal) 
    result = subprocess.run(["enable_pwm", channel_id], capture_output=True, text=True, shell=True)
    out = result.stdout
    if out in ERROR_NUMS:
        raise OSError(f"DMA enable_pwm error: {ERROR_NUMS[out]}")
    if out == -1:
        raise OSError("Invalid number of command line args.")
    
    return out

def disable_channel(channel_id: int) -> int:
    # Disable a channel (stop outputting PWM signal)
    result = subprocess.run(["disable_pwm", channel_id], capture_output=True, text=True, shell=True)
    out = result.stdout
    if out in ERROR_NUMS:
        raise OSError(f"DMA disable_pwm error: {ERROR_NUMS[out]}")
    if out == -1:
        raise OSError("Invalid number of command line args.")
    
    return out

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
        GPIO.setmode(GPIO.BOARD) # Use board pin numbers, NOT BCM numbers

        GPIO.setup(self.PIN_SLEEP, GPIO.OUT)
        GPIO.setup(self.PIN_FAULT, GPIO.IN)


    def configure_pwm(self):
        self.A1_channel = request_pwm_channel()
        self.A2_channel = request_pwm_channel()
        self.B1_channel = request_pwm_channel()
        self.B2_channel = request_pwm_channel()

        configure_channel(self.A1_channel, self.PIN_AIN1, self.freq, 0)
        configure_channel(self.A2_channel, self.PIN_AIN2, self.freq, 0)
        configure_channel(self.B1_channel, self.PIN_BIN1, self.freq, 0)
        configure_channel(self.B2_channel, self.PIN_BIN2, self.freq, 0)


    def set_motorA_speed(self, speed: float):
        if speed >= 0:
            configure_channel(self.A1_channel, self.PIN_AIN1, self.freq, speed)
            configure_channel(self.A2_channel, self.PIN_AIN2, self.freq, 0)
        else:
            configure_channel(self.A1_channel, self.PIN_AIN1, self.freq, 0)
            configure_channel(self.A2_channel, self.PIN_AIN2, self.freq, speed)
    def set_motorB_speed(self, speed: int):
        if speed >= 0:
            configure_channel(self.B1_channel, self.PIN_BIN1, self.freq, speed)
            configure_channel(self.B2_channel, self.PIN_BIN2, self.freq, 0)
        else:
            configure_channel(self.B1_channel, self.PIN_BIN1, self.freq, 0)
            configure_channel(self.B2_channel, self.PIN_BIN2, self.freq, speed)

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