"""
bmi323.py
=========
Library for interfacing with Vishay VCNL4030X01 proximity/ambient light sensor over I2C.

Author(s): Harry Upton

Datasheet: https://www.vishay.com/docs/84250/vcnl4030x01.pdf

Implementation Notes
--------------------
- 4 different IDs depending on the part number (0x60, 0x51, 0x40, and 0x41).

Missing Features (ToDo):
------------------------
- Add configure function to change settings. The sensor does have default valeus that 
 enable it to work immediately, though.

"""
import smbus2 as smb
import time

REG_PS_DATA = 0x08
REG_ALS_DATA = 0x0B
REG_WHITE_DATA = 0x0C

class VCNL4030:
    def __init__(self, i2c_channel: int = 1, i2c_addr: int = 0x60):
        # Intialise I2C bus
        self.bus = smb.SMBus(i2c_channel)
        self.bus.open(i2c_channel)
        self.addr = i2c_addr

    def configure(self):
        pass

    def read_als(self):
        # Ambient light sensor
        als_data = self.bus.read_i2c_block_data(self.addr, REG_ALS_DATA, 2)
        als = (als_data[1] << 8) | (als_data[0])
        return als
        

    def read_proximity(self):
        # ToF distance sensor
        prox_data = self.bus.read_i2c_block_data(self.addr, REG_PS_DATA, 2)
        prox = (prox_data[1] << 8) | (prox_data[0])
        return prox