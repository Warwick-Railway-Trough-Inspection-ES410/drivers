"""
bmi323.py
=========
Library for interfacing with Bosch BMI323 IMU over I2C.

Author(s): Harry Upton

Implementation Notes
--------------------



Missing Features (ToDo):
------------------------
- Add support for other modes (low power, etc.)
- Make code more readable by writing custom _writeX and _readX functions that sort out byte order


"""
import smbus2 as smb
import time

REG_CHIP_ID = 0x00
REG_DEVICE_STATUS = 0x01
REG_SENSOR_STATUS = 0x02

REG_ACC_CONFIG = 0x20
REG_GYR_CONFIG = 0x21
REG_CMD = 0x7E

RED_ACC_DATA_X = 0x03
RED_ACC_DATA_Y = 0x04
RED_ACC_DATA_Z = 0x05
REG_GYR_DATA_X = 0x06
REG_GYR_DATA_Y = 0x07
REG_GYR_DATA_Z = 0x08

class BMI323:
    def __init__(self, i2c_channel: int, i2c_addr: int = 0x68):
        # Intialise I2C bus
        self.bus = smb.SMBus(1)
        self.bus.open(i2c_channel)
        self.addr = i2c_addr
        

    # Configure BME688 (for normal power mode)
    def configure(self) -> None:
        # Check chip status and initialization
        # Note: we must read 4 bytes to perform a 16-bit read, as I2C payloads start with 2 dummy bytes.
        self.chip_id = self.bus.read_i2c_block_data(self.addr, REG_CHIP_ID, 4) # First read.

        self.device_status = self.bus.read_i2c_block_data(self.addr, REG_DEVICE_STATUS, 4)
        if self.device_status != 0b0:
            raise RuntimeError("BMI323 I2C error: power error (device_status != 0b0)")
        time.sleep(0.01)

        self.sensor_status = self.bus.read_i2c_block_data(self.addr, REG_SENSOR_STATUS, 4)
        if self.sensor_status != 0b1:
            raise RuntimeError("BMI323 I2C error: initialisation error (sensor_status != 0b1)")
        time.sleep(0.01)

        # Configure normal power mode
        self.bus.write_i2c_block_data(self.addr, REG_ACC_CONFIG, [0x27,0x40]) #0x4027 = normal
        time.sleep(0.01)
        self.bus.write_i2c_block_data(self.addr, REG_GYR_CONFIG, [0x4B,0x40]) #0x404B = normal
        time.sleep(0.01)
    
    # Soft reset BMI323 and close I2C bus
    def close(self):
        self.bus.write_i2c_block_data(self.addr, REG_CMD, [0xAF,0xDE]) # 0xDEAF = soft reset
        self.bus.close()

