# Control PCB - CM4 scripts
This repository contains the scripts to control all of the Control PCB's peripherals.

## Installation
For I2C devices (BMI323, MAX17049 and VCNL4030):
```
sudo apt-get install python-smbus 
sudo apt-get install i2c-tools
```

For PWM motor control:
The python script makes use of a program written in C, which in turn depends on https://github.com/besp9510/dma_pwm (included as a submodule in this repo). This needs to be installed system-wide, to do this follow the instructions in the dma_pwm README.md file. Then, you can compile the motor_pwm C program in the drv8833 directory.



## References
https://github.com/DFRobot/DFRobot_MAX17043/tree/master/python/raspberry
https://github.com/besp9510/dma_pwm
https://github.com/manuelbaum/pyBMI323