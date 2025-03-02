"""
bmi323.py
=========
Library for interfacing with Bosch BMI323 IMU over I2C.

Author(s): Harry Upton

Datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi323-ds000.pdf

Implementation Notes
--------------------
- Runs sensor in 'normal mode':
    - accelerometer: +/- 8g; 50Hz; no averaging; filter to ODR/2
    - gyroscope: +/- 2k deg/s; 800Hz; no averaging; filter to ODR/2


Missing Features (ToDo):
------------------------
- Add support for other modes (low power, etc.)
- Make code more readable by writing custom _writeX and _readX functions that sort out byte order
- Allow changing of BW, ODR, etc.
- Instead of hardcoded scale factors for unit conversion, do automatically depending on mode.

"""
import smbus2 as smb
import time

REG_CHIP_ID = 0x00
REG_DEVICE_STATUS = 0x01
REG_SENSOR_STATUS = 0x02

REG_ACC_CONFIG = 0x20
REG_GYR_CONFIG = 0x21
REG_CMD = 0x7E

REG_ACC_DATA_X = 0x03
REG_ACC_DATA_Y = 0x04
REG_ACC_DATA_Z = 0x05
REG_GYR_DATA_X = 0x06
REG_GYR_DATA_Y = 0x07
REG_GYR_DATA_Z = 0x08

class BMI323:
    def __init__(self, i2c_channel: int = 10, i2c_addr: int = 0x68):
        # Intialise I2C bus
        self.bus = smb.SMBus(i2c_channel)
        self.bus.open(i2c_channel)
        self.addr = i2c_addr
        

    # Configure BME688 (for normal power mode)
    def configure(self) -> None:
        # Check chip status and initialization
        # Note: we must read 4 bytes to perform a 16-bit read, as I2C payloads start with 2 dummy bytes.
        self.chip_id = self.bus.read_i2c_block_data(self.addr, REG_CHIP_ID, 4) # First read.

        self.device_status = self.bus.read_i2c_block_data(self.addr, REG_DEVICE_STATUS, 4)
        if self.device_status != [0,0,0,0]:
            raise RuntimeError(f"BMI323 I2C error: power error with {self.device_status} (device_status != 0b0)")
        time.sleep(0.01)

        self.sensor_status = self.bus.read_i2c_block_data(self.addr, REG_SENSOR_STATUS, 4)
        if (self.sensor_status == [0,0,1,0] or self.sensor_status == [0,0,0,0]) == False:
            raise RuntimeError(f"BMI323 I2C error: initialisation error with {self.sensor_status} (sensor_status != 0b1)")
        time.sleep(0.01)

        # Configure normal power mode
        self.bus.write_i2c_block_data(self.addr, REG_ACC_CONFIG, [0x27,0x40]) #0x4027 = normal
        time.sleep(0.01)
        self.bus.write_i2c_block_data(self.addr, REG_GYR_CONFIG, [0x4B,0x40]) #0x404B = normal
        time.sleep(0.01)

    def read_acceleration(self) -> tuple[float, float, float]:
        # Scale factor: 1 / (4.10 LSB/mg) *  (9.81/1000) = 0.002392
        # Output is in m/s^2
        acc_data = self.bus.read_i2c_block_data(self.addr, REG_ACC_DATA_X, 8)
        acc_data_x = int.from_bytes(acc_data[2:4], byteorder='little', signed=True) * 0.002392
        acc_data_y = int.from_bytes(acc_data[4:6], byteorder='little', signed=True) * 0.002392
        acc_data_z = int.from_bytes(acc_data[6:8], byteorder='little', signed=True) * 0.002392
        return (acc_data_x, acc_data_y, acc_data_z)

    def read_gyro(self) -> tuple[float, float, float]:
        # Scale factor: 1 / (16.4 LSB/deg/s) = 0.06098
        # Output is in deg/s
        gyr_data = self.bus.read_i2c_block_data(self.addr, REG_GYR_DATA_X, 8)
        gyr_data_x = int.from_bytes(gyr_data[2:4], byteorder='little', signed=True) * 0.06098
        gyr_data_y = int.from_bytes(gyr_data[4:6], byteorder='little', signed=True) * 0.06098
        gyr_data_z = int.from_bytes(gyr_data[6:8], byteorder='little', signed=True) * 0.06098
        return (gyr_data_x, gyr_data_y, gyr_data_z)
    
    # Soft reset BMI323 and close I2C bus
    def close(self):
        self.bus.write_i2c_block_data(self.addr, REG_CMD, [0xAF,0xDE]) # 0xDEAF = soft reset
        self.bus.close()

