"""
max17049.py
===========
Library for interfacing with MAX17049 Fuel Gauge over I2C.

Author(s): Harry Upton

Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/max17048-max17049.pdf

Implementation Notes
--------------------


Missing Features (ToDo):
------------------------
- ALL configuration stuff
- Quick start (not sure if necessary yet)
- Temperature compensation stuff


"""
import smbus2 as smb
import time

MAX17049_VCELL = 0x02
MAX17049_SOC = 0x04
MAX17049_MODE = 0x06
MAX17049_VERSION = 0x08
MAX17049_CONFIG = 0x0c
MAX17049_COMMAND = 0xfe

class MAX17049:
    def __init__(self, i2c_channel: int = 1, i2c_addr: int = 0x36):
        # Intialise I2C bus
        self.bus = smb.SMBus(i2c_channel)
        self.bus.open(i2c_channel)
        self.addr = i2c_addr

    def configure(self):
        pass

    def read_soc(self):
        # Scale factor: 1 / (1%/256) = 0.00390625/%
        # Output is in %
        soc_data = self.bus.read_i2c_block_data(self.addr, MAX17049_SOC, 2)
        soc = ((soc_data >> 8) + 0.00390625 * (soc_data & 0x00ff))
        return soc


    def read_cell_voltage(self):
        # Scale factor: 78.125 uV/cell = 7.8125e-05 V/cell
        # Output is in V/cell
        voltage_data = self.bus.read_i2c_block_data(self.addr, MAX17049_VCELL, 2)
        volts = ((voltage_data[0] << 8) | voltage_data[1])
        return (volts * 7.8125e-05)
