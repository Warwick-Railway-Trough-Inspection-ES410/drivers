# Control PCB - CM4 scripts
This repository contains the scripts to control all of the Control PCB's peripherals.

## Installation
For I2C devices (BMI323, MAX17049 and VCNL4030):
```
sudo apt-get install python-smbus 
sudo apt-get install i2c-tools
```

For PWM motor control:\
To be able to use PWM on more than 2 pins, and use it on any pin, the DMA peripheral is required. The easiest way to implement this (and what is done in this script), is with `pigpio`. Follow [this](https://abyz.me.uk/rpi/pigpio/download.html) link for installation instructions.


## References
https://github.com/DFRobot/DFRobot_MAX17043/tree/master/python/raspberry \
https://abyz.me.uk/rpi/pigpio/index.html \
https://github.com/manuelbaum/pyBMI323